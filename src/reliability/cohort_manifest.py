"""Materialize approved EP-1/EP-2 membership, without splits or clock conversion."""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path

try:
    from .data_audit import sha256
except ImportError:
    from data_audit import sha256


def assemble_manifest(reconciliation: dict, capture_links: list[dict] | None = None) -> dict:
    """Use approved candidate rules; only evidence-bearing file links merge groups.

    Capture links contain a 'files' list and nonempty 'evidence' reference.
    A link is an explicit supplied input, not inferred from matching clocks.
    """
    sources = {r["id"]: r for r in reconciliation["source_records"]}
    database = {r["rowid"]: r for r in reconciliation["database_records"]}
    if len(sources) != len(reconciliation["source_records"]) or len(database) != len(reconciliation["database_records"]):
        raise ValueError("Duplicate source/database reference IDs")

    def unique_pairs(profile: dict) -> dict:
        result = {}
        used_sources = set()
        for group in profile["groups"]:
            if group["status"] != "unique_candidate_pair":
                continue
            if len(group["source_ids"]) != 1 or len(group["database_rowids"]) != 1:
                raise ValueError("Unique-pair status has non-unique references")
            source_id, rowid = group["source_ids"][0], group["database_rowids"][0]
            if source_id not in sources or rowid not in database or rowid in result or source_id in used_sources:
                raise ValueError("Unknown or duplicated candidate reference")
            result[rowid] = source_id
            used_sources.add(source_id)
        return result

    strong = unique_pairs(reconciliation["profiles"]["radio_metadata_exact"])
    radio = unique_pairs(reconciliation["profiles"]["radio_exact"])
    if any(strong[rowid] != radio[rowid] for rowid in strong.keys() & radio.keys()):
        raise ValueError("Unique radio and metadata candidate references disagree")
    selected = {}
    for rowid in database:
        if rowid in strong:
            selected[rowid] = (strong[rowid], "primary_temporal", "unique_radio_metadata")
        elif rowid in radio:
            selected[rowid] = (radio[rowid], "secondary_non_temporal_only", "unique_radio_only")
        else:
            raise ValueError(f"Row {rowid} lacks unique source lineage under approved rules; manual review required")

    paths = sorted({sources[source_id]["path"] for source_id, _, _ in selected.values()})
    parents = {path: path for path in paths}

    def find(path: str) -> str:
        while parents[path] != path:
            parents[path] = parents[parents[path]]
            path = parents[path]
        return path

    normalized_links = []
    for link in capture_links or []:
        files = sorted(set(link["files"]))
        if len(files) < 2 or not isinstance(link.get("evidence"), str) or not link["evidence"].strip():
            raise ValueError("Capture link requires at least two files and an evidence reference")
        if not set(files).issubset(parents):
            raise ValueError("Capture link references an unknown source file")
        representative = find(files[0])
        for path in files[1:]:
            parents[find(path)] = representative
        normalized_links.append({"files": files, "evidence": link["evidence"]})
    components = {}
    for path in paths:
        components.setdefault(find(path), []).append(path)
    groups = []
    file_group = {}
    for files in sorted(components.values()):
        identifier = "source_group:" + hashlib.sha256(json.dumps(files, separators=(",", ":")).encode()).hexdigest()
        groups.append({"group_id": identifier, "source_files": files})
        file_group.update({path: identifier for path in files})
    rows = []
    for rowid, (source_id, cohort, basis) in sorted(selected.items()):
        source, record = sources[source_id], database[rowid]
        rows.append({"database_rowid": rowid, "source_path": source["path"],
                     "source_line": source["line"], "cohort": cohort, "lineage_basis": basis,
                     "provisional_group_id": file_group[source["path"]],
                     "attack_category": record["attack_category"], "attack_subcategory": record["attack_subcategory"],
                     "traffic_type": record["traffic_type"]})
    return {"format_version": 1, "policy_reference": "EP-1/EP-2; D012/D013",
            "grouping_status": "provisional source-file groups; capture independence unverified",
            "applied_capture_links": sorted(normalized_links, key=lambda x: (x["files"], x["evidence"])),
            "linkage_limit": "No supplied links means none applied, not proof that files are independent.",
            "cohort_counts": dict(sorted(Counter(r["cohort"] for r in rows).items())),
            "source_file_count": len(paths), "groups": groups, "rows": rows}


def build_manifest(root: Path, reconciliation_path: Path, capture_links: list[dict] | None = None) -> dict:
    root = root.resolve()
    report_hash = sha256(reconciliation_path)
    report = json.loads(reconciliation_path.read_text(encoding="utf-8"))
    for item in report["input_files"]:
        path = (root / item["path"]).resolve()
        if not path.is_relative_to(root) or not path.is_file():
            raise ValueError("Input reference is missing or outside data root")
        if path.stat().st_size != item["bytes"] or sha256(path) != item["sha256"]:
            raise ValueError(f"Input differs from reconciled snapshot: {item['path']}")
    manifest = assemble_manifest(report, capture_links)
    if sha256(reconciliation_path) != report_hash:
        raise ValueError("Reconciliation artifact changed during manifest construction")
    manifest.update(reconciliation_sha256=report_hash, input_files=report["input_files"],
                    input_snapshot_verified=True,
                    pending_decisions=["EP-3", "EP-4", "EP-5", "EP-6"])
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--reconciliation", type=Path, required=True)
    parser.add_argument("--capture-links", type=Path, help="Optional JSON list of reviewed evidence-bearing file links")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.resolve().is_relative_to(args.root.resolve()) or args.output.exists():
        parser.error("Choose a new output path outside the raw input directory")
    links = json.loads(args.capture_links.read_text(encoding="utf-8")) if args.capture_links else []
    result = build_manifest(args.root, args.reconciliation, links)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(result, stream, indent=2, sort_keys=True, allow_nan=False)
        stream.write("\n")
    print("Saved", args.output, result["cohort_counts"], "; provisional groups:", len(result["groups"]))


if __name__ == "__main__":
    main()
