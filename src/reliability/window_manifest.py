"""Approved EP-4 report windows; no model inputs, predictions or split assignments."""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path

try:
    from .data_audit import sha256
    from .reconciliation import comparison_key
    from .timing_audit import finite_number, STREAM_FIELDS
except ImportError:
    from data_audit import sha256
    from reconciliation import comparison_key
    from timing_audit import finite_number, STREAM_FIELDS


REPORTS_PER_WINDOW = 10
POLICY_ID = "EP-4_report_count_10_stride_10_retained_tails_v1"


def build_windows(root: Path, cohort_path: Path) -> dict:
    root = root.resolve()
    cohort_hash = sha256(cohort_path)
    cohort = json.loads(cohort_path.read_text(encoding="utf-8"))
    pinned = {item["path"]: item for item in cohort["input_files"]}
    for path, item in pinned.items():
        target = (root / path).resolve()
        if not target.is_relative_to(root) or not target.is_file():
            raise ValueError("Missing input or input outside data root")
        if target.stat().st_size != item["bytes"] or sha256(target) != item["sha256"]:
            raise ValueError(f"Input snapshot mismatch: {path}")

    group_files = {g["group_id"]: set(g["source_files"]) for g in cohort["groups"]}
    all_file_groups = defaultdict(set)
    by_path = defaultdict(dict)
    rowids = set()
    counts = Counter()
    for row in cohort["rows"]:
        if row["database_rowid"] in rowids:
            raise ValueError("Duplicate database row reference")
        rowids.add(row["database_rowid"])
        path, group = row["source_path"], row["provisional_group_id"]
        if path not in group_files.get(group, set()):
            raise ValueError("Row/file does not belong to its declared group")
        all_file_groups[path].add(group)
        counts[row["cohort"]] += 1
        if row["cohort"] == "primary_temporal":
            if path not in pinned or row["source_line"] in by_path[path]:
                raise ValueError("Unpinned source or duplicate source-line reference")
            by_path[path][row["source_line"]] = row
        elif row["cohort"] != "secondary_non_temporal_only":
            raise ValueError("Unknown cohort membership")
    if any(len(groups) != 1 for groups in all_file_groups.values()):
        raise ValueError("One source file spans multiple provisional groups")
    if dict(counts) != cohort["cohort_counts"] or not by_path:
        raise ValueError("Cohort counts disagree or primary cohort is empty")

    windows = []
    stream_count = 0
    for path, references in sorted(by_path.items()):
        streams = defaultdict(list)
        found = set()
        first, last = min(references), max(references)
        with (root / path).open(encoding="utf-8-sig") as source:
            for line_number, line in enumerate(source, 1):
                if not line.strip():
                    continue
                if line_number not in references:
                    if first < line_number < last:
                        raise ValueError(f"Unselected interior source records require continuity review: {path}")
                    continue
                values = json.loads(line)
                identity = comparison_key(values, STREAM_FIELDS)
                if isinstance(identity, dict) or not finite_number(values.get("timestamp")):
                    raise ValueError(f"Primary observation lacks usable identity/clock: {path}:{line_number}")
                sequence = streams[identity]
                if sequence and values["timestamp"] <= sequence[-1]["timestamp"]:
                    raise ValueError(f"Non-increasing source clock requires review: {path}:{line_number}")
                sequence.append({"source_line": line_number, "timestamp": values["timestamp"],
                                 "identity": {f: values[f] for f in STREAM_FIELDS},
                                 "reference": references[line_number]})
                found.add(line_number)
        if found != references.keys():
            raise ValueError(f"Source-line reference absent from file: {path}")
        for _, sequence in sorted(streams.items()):
            stream_count += 1
            for offset in range(0, len(sequence), REPORTS_PER_WINDOW):
                chunk = sequence[offset:offset + REPORTS_PER_WINDOW]
                labels = {(o["reference"]["traffic_type"], o["reference"]["attack_category"],
                           o["reference"]["attack_subcategory"]) for o in chunk}
                if len(labels) != 1 or any(v is None for v in next(iter(labels))):
                    raise ValueError("Mixed or missing source-provided window labels require review")
                lines = [o["source_line"] for o in chunk]
                identity_payload = {"policy": POLICY_ID, "source_path": path,
                                    "source_sha256": pinned[path]["sha256"], "source_lines": lines}
                identifier = "report_window:" + hashlib.sha256(
                    json.dumps(identity_payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
                first_row = chunk[0]["reference"]
                deltas = [b["timestamp"] - a["timestamp"] for a, b in zip(chunk, chunk[1:])]
                windows.append({
                    "window_id": identifier, "source_path": path,
                    "provisional_group_id": first_row["provisional_group_id"],
                    "identity": chunk[0]["identity"], "reports": len(chunk),
                    "is_partial": len(chunk) < REPORTS_PER_WINDOW,
                    "expected_report_count": len(chunk),
                    "short_input_reason_if_unsupported": "SHORT_WINDOW" if len(chunk) < REPORTS_PER_WINDOW else None,
                    "attack_category": first_row["attack_category"],
                    "attack_subcategory": first_row["attack_subcategory"],
                    "traffic_type": first_row["traffic_type"],
                    "raw_timestamp_first": chunk[0]["timestamp"], "raw_timestamp_last": chunk[-1]["timestamp"],
                    "raw_span": chunk[-1]["timestamp"] - chunk[0]["timestamp"],
                    "largest_step_raw": max(deltas) if deltas else None,
                    "report_references": [{"database_rowid": o["reference"]["database_rowid"],
                                           "source_line": o["source_line"]} for o in chunk],
                })
    referenced = [r["database_rowid"] for w in windows for r in w["report_references"]]
    if len(referenced) != len(set(referenced)) or len(referenced) != counts["primary_temporal"]:
        raise ValueError("Primary window accounting is incomplete or duplicated")
    for path, item in pinned.items():
        if sha256(root / path) != item["sha256"]:
            raise ValueError("Input changed during window construction")
    if sha256(cohort_path) != cohort_hash:
        raise ValueError("Cohort manifest changed during window construction")
    return {
        "format_version": 1, "policy_id": POLICY_ID, "policy_references": ["EP-1", "EP-2", "EP-3", "EP-4"],
        "cohort_manifest_sha256": cohort_hash, "input_hashes_unchanged": True,
        "reports_per_window": REPORTS_PER_WINDOW, "stride_reports": REPORTS_PER_WINDOW,
        "clock_policy": "raw source values and original report order; no time conversion or gap-based run inference",
        "grouping_status": "provisional source-file groups; independent capture identity unverified",
        "model_compatibility": "partial input encoding/scoring not agreed; retain tails and abstain SHORT_WINDOW if unsupported",
        "input_files": cohort["input_files"], "primary_rows": counts["primary_temporal"],
        "secondary_rows_kept_outside_temporal_windows": counts["secondary_non_temporal_only"],
        "source_files": len(by_path), "identity_streams": stream_count,
        "complete_windows": sum(not w["is_partial"] for w in windows),
        "partial_windows": sum(w["is_partial"] for w in windows), "windows": windows,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--cohort-manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.resolve().is_relative_to(args.root.resolve()) or args.output.exists():
        parser.error("Choose a new output path outside the input directory")
    result = build_windows(args.root, args.cohort_manifest)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x", encoding="utf-8", newline="\n") as output:
        json.dump(result, output, indent=2, sort_keys=True, allow_nan=False)
        output.write("\n")
    print("Saved", args.output, "; full windows:", result["complete_windows"],
          "; retained partials:", result["partial_windows"], "; primary reports:", result["primary_rows"])


if __name__ == "__main__":
    main()
