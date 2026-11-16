"""Describe source timing and metadata coincidences; never assign runs/clocks."""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from contextlib import closing
from itertools import combinations
import json
import math
from pathlib import Path
import sqlite3
from statistics import median
from zipfile import ZipFile

try:
    from .data_audit import sha256
    from .reconciliation import RADIO_FIELDS, PROFILES, build_reconciliation, comparison_key
except ImportError:
    from data_audit import sha256
    from reconciliation import RADIO_FIELDS, PROFILES, build_reconciliation, comparison_key


STREAM_FIELDS = ("cellid", "ue_id", "rnti")
COINCIDENCE_FIELDS = ("timestamp", "ue_id", "cellid", "in_sync")


def finite_number(value: object) -> bool:
    return type(value) is int or (type(value) is float and math.isfinite(value))


def describe_sequence(observations: list[dict]) -> dict:
    """Use physical source order; invalid/missing clocks break adjacency."""
    valid = [o["timestamp"] for o in observations if finite_number(o.get("timestamp"))]
    deltas, exceptions = [], []
    for previous, current in zip(observations, observations[1:]):
        if not (finite_number(previous.get("timestamp")) and finite_number(current.get("timestamp"))):
            continue
        delta = current["timestamp"] - previous["timestamp"]
        deltas.append(delta)
        if delta <= 0:
            exceptions.append({"previous_line": previous["line"], "line": current["line"], "delta_raw": delta})
    positives = [d for d in deltas if d > 0]
    return {
        "records": len(observations), "finite_timestamps": len(valid),
        "missing_or_invalid_timestamps": len(observations) - len(valid),
        "raw_min": min(valid) if valid else None, "raw_max": max(valid) if valid else None,
        "distinct_timestamps": len(set(valid)), "repeated_timestamp_occurrences": len(valid) - len(set(valid)),
        "adjacent_comparable_pairs": len(deltas), "positive_steps": len(positives),
        "zero_steps": sum(d == 0 for d in deltas), "negative_steps": sum(d < 0 for d in deltas),
        "positive_step_median_raw": median(positives) if positives else None,
        "positive_step_max_raw": max(positives) if positives else None,
        "delta_histogram_raw": [{"delta": d, "count": n} for d, n in sorted(Counter(deltas).items())],
        "nonpositive_step_locations": exceptions,
    }


def describe_streams(observations: list[dict]) -> tuple[list, dict, list]:
    """Group only for diagnostics by source path/cellid/ue_id/rnti, not run ID."""
    grouped = defaultdict(list)
    unusable = []
    for o in observations:
        identity = comparison_key(o["values"], STREAM_FIELDS)
        if isinstance(identity, dict):
            unusable.append({"path": o["path"], "line": o["line"], **identity})
        else:
            grouped[(o["path"], identity)].append(o)
    summaries, internals = [], {}
    for (path, key), records in sorted(grouped.items()):
        identity = {field: records[0]["values"][field] for field in STREAM_FIELDS}
        summary = {"path": path, "identity": identity,
                   **describe_sequence([{"line": o["line"], "timestamp": o["values"].get("timestamp")} for o in records])}
        stream_id = len(summaries)
        summaries.append({"stream_index": stream_id, **summary})
        timestamps = {o["values"]["timestamp"] for o in records if finite_number(o["values"].get("timestamp"))}
        fingerprints = Counter()
        for o in records:
            fingerprint = comparison_key(o["values"], PROFILES["radio_metadata_exact"])
            if not isinstance(fingerprint, dict):
                fingerprints[fingerprint] += 1
        internals[stream_id] = {"identity_key": key, "timestamps": timestamps, "fingerprints": fingerprints}
    return summaries, internals, unusable


def describe_overlaps(streams: list[dict], internals: dict) -> dict:
    comparable = 0
    overlaps = []
    for left, right in combinations(streams, 2):
        a, b = internals[left["stream_index"]], internals[right["stream_index"]]
        if left["path"] == right["path"] or a["identity_key"] != b["identity_key"]:
            continue
        if not a["timestamps"] or not b["timestamps"]:
            continue
        comparable += 1
        start, end = max(left["raw_min"], right["raw_min"]), min(left["raw_max"], right["raw_max"])
        if start <= end:
            overlaps.append({
                "left_stream_index": left["stream_index"], "right_stream_index": right["stream_index"],
                "left_path": left["path"], "right_path": right["path"], "identity": left["identity"],
                "raw_overlap_start": start, "raw_overlap_end": end,
                "common_distinct_timestamps": len(a["timestamps"] & b["timestamps"]),
                "shared_radio_metadata_occurrences": sum((a["fingerprints"] & b["fingerprints"]).values()),
            })
    return {"same_identity_cross_file_pairs_compared": comparable, "range_overlaps": overlaps}


def metadata_coincidences(sources: list[dict], questionable: list[dict]) -> list[dict]:
    """Compare four fields only; coincidences do not identify metadata origin."""
    index = defaultdict(list)
    for o in sources:
        key = comparison_key(o["values"], COINCIDENCE_FIELDS)
        if not isinstance(key, dict):
            index[key].append(o)
    rows = []
    for case in questionable:
        key = comparison_key(case["values"], COINCIDENCE_FIELDS)
        candidates = [] if isinstance(key, dict) else index.get(key, [])
        radio_key = comparison_key(case["values"], RADIO_FIELDS)
        rows.append({
            "source_path": case["source_path"], "source_line": case["source_line"],
            "database_rowid": case["database_rowid"],
            "database_compared_metadata": {f: case["values"].get(f) for f in COINCIDENCE_FIELDS},
            "comparison_issue": key if isinstance(key, dict) else None,
            "coincident_source_observations": [
                {"path": o["path"], "line": o["line"],
                 "radio_values_also_equal": not isinstance(radio_key, dict) and radio_key == comparison_key(o["values"], RADIO_FIELDS)}
                for o in candidates],
        })
    return rows


def inspect_archive(path: Path | None) -> dict:
    if path is None:
        return {"status": "not supplied; archive inspection optional"}
    with ZipFile(path) as archive:
        files = [e for e in archive.infolist() if not e.is_dir()]
        extensions = Counter(Path(e.filename).suffix.lower() for e in files)
        candidates = [e.filename for e in files if Path(e.filename).suffix.lower() in
                      (".py", ".ipynb", ".md", ".pdf", ".yaml", ".yml") or
                      any(s in Path(e.filename).name.lower() for s in ("manifest", "readme", "metadata", "preprocess", "process", "label"))]
    return {"status": "central directory inspected only", "filename": path.name,
            "bytes": path.stat().st_size, "file_entries": len(files),
            "extension_counts": dict(sorted(extensions.items())), "provenance_filename_candidates": candidates,
            "limitation": "Filename/extension search only; JSON/CSV content not searched, no full archive integrity/hash check. ZIP packaging dates are not capture dates."}


def build_timing_audit(root: Path, archive: Path | None = None) -> dict:
    root = root.resolve()
    reconciliation = build_reconciliation(root)
    observations, files = [], []
    paths = sorted({s["path"] for s in reconciliation["source_records"]})
    for path in paths:
        records = []
        with (root / path).open(encoding="utf-8-sig") as stream:
            for line_number, line in enumerate(stream, 1):
                if line.strip():
                    record = {"path": path, "line": line_number, "values": json.loads(line)}
                    records.append(record)
                    observations.append(record)
        valid = sum(finite_number(o["values"].get("timestamp")) for o in records)
        missing = sum(o["values"].get("timestamp") is None for o in records)
        files.append({"path": path, "records": len(records), "finite_timestamps": valid,
                      "missing_or_null_timestamps": missing, "invalid_nonnull_timestamps": len(records) - valid - missing})
    streams, internals, unusable = describe_streams(observations)
    source_refs = {s["id"]: s for s in reconciliation["source_records"]}
    metadata_unusable = {s["id"] for s in reconciliation["profiles"]["radio_metadata_exact"]["unusable_sources"]}
    candidate_refs = []
    for g in reconciliation["profiles"]["radio_exact"]["groups"]:
        if g["status"] == "unique_candidate_pair" and g["source_ids"][0] in metadata_unusable:
            candidate_refs.append((source_refs[g["source_ids"][0]], g["database_rowids"][0]))
    database = {}
    with closing(sqlite3.connect((root / "Lower_Layer_Data.db").as_uri() + "?mode=ro", uri=True)) as conn:
        conn.execute("PRAGMA query_only=ON")
        conn.row_factory = sqlite3.Row
        for row in conn.execute("SELECT rowid AS __audit_rowid__, * FROM lower_layer_data ORDER BY rowid"):
            database[row["__audit_rowid__"]] = dict(row)
    questionable = [{"source_path": s["path"], "source_line": s["line"],
                     "database_rowid": rowid, "values": database[rowid]}
                    for s, rowid in sorted(candidate_refs, key=lambda pair: pair[1])]
    coincidences = metadata_coincidences(observations, questionable)
    for item in reconciliation["input_files"]:
        if sha256(root / item["path"]) != item["sha256"]:
            raise ValueError(f"Input changed during timing inspection: {item['path']}")
    return {
        "format_version": 1, "units_and_timezone": "unverified; all differences in raw units",
        "stream_fields": list(STREAM_FIELDS), "coincidence_fields": list(COINCIDENCE_FIELDS),
        "semantics": "Descriptive identity groups, never independent runs. Original within-stream order retained. No gap threshold, time conversion, synthetic clock, rate transformation or exclusion.",
        "input_files": reconciliation["input_files"], "input_hashes_unchanged": True,
        "extraction_manifest_check": reconciliation["extraction_manifest_check"],
        "source_files": files, "streams": streams, "unusable_stream_identity_records": unusable,
        "overlap_diagnostics": describe_overlaps(streams, internals),
        "questionable_metadata_coincidences": coincidences,
        "archive_inventory": inspect_archive(archive),
        "limitations": "Coincidence does not prove copying or authenticate clocks. Reused UE identities may span captures; disjoint intervals do not prove independence. Unidentified source rows cannot be assigned to a stream; deltas among identified rows need not be consecutive reports.",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--archive", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.resolve().is_relative_to(args.root.resolve()) or args.output.exists():
        parser.error("Choose a new output path outside the input directory")
    report = build_timing_audit(args.root, args.archive)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(report, stream, indent=2, sort_keys=True, allow_nan=False)
        stream.write("\n")
    print("Saved", args.output, "; diagnostic identity groups:", len(report["streams"]),
          "; interval overlaps:", len(report["overlap_diagnostics"]["range_overlaps"]))


if __name__ == "__main__":
    main()
