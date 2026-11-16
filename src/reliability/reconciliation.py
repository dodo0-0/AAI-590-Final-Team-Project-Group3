"""Exact, multiplicity-preserving source/database diagnostics; no run assignment."""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from contextlib import closing
import hashlib
import json
import math
from pathlib import Path
import sqlite3

try:
    from .data_audit import build_inventory, sha256
except ImportError:  # Direct script execution from the project root.
    from data_audit import build_inventory, sha256


RADIO_FIELDS = (
    "dlBytes", "dlMcs", "dlBler", "ulBytes", "ulMcs", "ulBler", "ri",
    "phr", "pcmax", "rsrq", "sinr", "rsrp", "rssi", "cqi", "pucchSnr", "puschSnr",
)
METADATA_FIELDS = ("timestamp", "ue_id", "cellid", "in_sync", "rnti")
PROFILES = {"radio_exact": RADIO_FIELDS, "radio_metadata_exact": RADIO_FIELDS + METADATA_FIELDS}
STATUSES = ("unique_candidate_pair", "ambiguous_candidate_group", "no_candidate", "unusable_key")


def comparison_key(record: dict, fields: tuple[str, ...]) -> tuple | dict:
    """Exact rational numbers equate 1 with 1.0, without rounding/coercion.

    Missing/null and invalid fields are unusable, never filled or wildcarded.
    RNTI strings are case-sensitive; numeric strings and booleans are rejected.
    """
    missing, invalid, key = [], [], []
    for field in fields:
        value = record.get(field)
        if value is None:
            missing.append(field)
        elif field == "rnti":
            if isinstance(value, str) and value:
                key.append(("text", value))
            else:
                invalid.append(field)
        elif type(value) is int:
            key.append(("number", value, 1))
        elif type(value) is float and math.isfinite(value):
            numerator, denominator = value.as_integer_ratio()
            key.append(("number", numerator, denominator))
        else:
            invalid.append(field)
    if missing or invalid:
        return {"missing_or_null_fields": missing, "invalid_fields": invalid}
    return tuple(key)


def compare_records(sources: list[dict], database: list[dict], fields: tuple[str, ...]) -> dict:
    """Index both sides without consuming occurrences or assigning provenance.

    Each input has a unique integer 'id' and a 'values' dictionary. Groups
    reference these IDs; all unusable occurrences retain their reason codes.
    """
    if not fields or len(set(fields)) != len(fields):
        raise ValueError("Comparison fields must be nonempty and unique")
    indices = [{}, {}]
    unusable = [[], []]
    for side, records in enumerate((sources, database)):
        ids = [record["id"] for record in records]
        if len(set(ids)) != len(ids):
            raise ValueError("Observation IDs must be unique within each side")
        index = defaultdict(list)
        for observation in records:
            key = comparison_key(observation["values"], fields)
            if isinstance(key, dict):
                unusable[side].append({"id": observation["id"], **key})
            else:
                index[key].append(observation["id"])
        indices[side] = index

    source_counts = Counter({status: 0 for status in STATUSES})
    database_counts = Counter({status: 0 for status in STATUSES})
    source_counts["unusable_key"] = len(unusable[0])
    database_counts["unusable_key"] = len(unusable[1])
    groups = []
    for key in indices[0].keys() | indices[1].keys():
        source_ids = sorted(indices[0].get(key, []))
        database_ids = sorted(indices[1].get(key, []))
        if not source_ids or not database_ids:
            status = "no_candidate"
        elif len(source_ids) == len(database_ids) == 1:
            status = "unique_candidate_pair"
        else:
            status = "ambiguous_candidate_group"
        source_counts[status] += len(source_ids)
        database_counts[status] += len(database_ids)
        groups.append({
            "key_sha256": hashlib.sha256(json.dumps(key, separators=(",", ":")).encode()).hexdigest(),
            "status": status, "source_ids": source_ids, "database_rowids": database_ids,
        })
    groups.sort(key=lambda group: group["key_sha256"])
    assert sum(source_counts.values()) == len(sources)
    assert sum(database_counts.values()) == len(database)
    return {"fields": list(fields), "source_counts": dict(source_counts),
            "database_counts": dict(database_counts), "groups": groups,
            "unusable_sources": unusable[0], "unusable_database": unusable[1]}


def _breakdown(profile: dict, source_refs: dict, database_refs: dict) -> tuple[list, list, list]:
    by_file = {ref["path"]: Counter({s: 0 for s in STATUSES}) for ref in source_refs.values()}
    by_category = {ref["attack_category"]: Counter({s: 0 for s in STATUSES}) for ref in database_refs.values()}
    label_disagreements = []
    aliases = {"DDOS": "DDoS", "Web": "Web Attacks"}  # Diagnostic display only.
    for group in profile["groups"]:
        for source_id in group["source_ids"]:
            by_file[source_refs[source_id]["path"]][group["status"]] += 1
        for rowid in group["database_rowids"]:
            by_category[database_refs[rowid]["attack_category"]][group["status"]] += 1
        if group["status"] == "unique_candidate_pair":
            source_ref = source_refs[group["source_ids"][0]]
            database_ref = database_refs[group["database_rowids"][0]]
            category = aliases.get(source_ref["folder_category"], source_ref["folder_category"])
            if category != database_ref["attack_category"]:
                label_disagreements.append({"source_id": source_ref["id"], "database_rowid": database_ref["rowid"]})
    for item in profile["unusable_sources"]:
        by_file[source_refs[item["id"]]["path"]]["unusable_key"] += 1
    for item in profile["unusable_database"]:
        by_category[database_refs[item["id"]]["attack_category"]]["unusable_key"] += 1
    return ([{"path": path, **dict(counts)} for path, counts in sorted(by_file.items())],
            [{"category": category, **dict(counts)} for category, counts in sorted(by_category.items(), key=lambda item: str(item[0]))],
            label_disagreements)


def build_reconciliation(root: Path) -> dict:
    root = root.resolve()
    inventory = build_inventory(root)  # Verify extraction manifest before reading.
    if any(source["invalid_records"] for source in inventory["sources"]):
        raise ValueError("Resolve malformed/non-object source lines before reconciliation")
    sources, source_refs = [], {}
    for source in inventory["sources"]:
        with (root / source["path"]).open(encoding="utf-8-sig") as stream:
            for line_number, line in enumerate(stream, 1):
                if not line.strip():
                    continue
                source_id = len(sources)
                sources.append({"id": source_id, "values": json.loads(line)})
                source_refs[source_id] = {"id": source_id, "path": source["path"],
                                          "line": line_number, "folder_category": source["category_from_folder"]}
    database, database_refs = [], {}
    with closing(sqlite3.connect((root / "Lower_Layer_Data.db").as_uri() + "?mode=ro", uri=True)) as conn:
        conn.execute("PRAGMA query_only=ON")
        conn.row_factory = sqlite3.Row
        for row in conn.execute('SELECT rowid AS __audit_rowid__, * FROM lower_layer_data ORDER BY rowid'):
            record = dict(row)
            rowid = record.pop("__audit_rowid__")
            database.append({"id": rowid, "values": record})
            database_refs[rowid] = {"rowid": rowid, **{field: record[field] for field in
                                   ("attack_category", "attack_subcategory", "traffic_type", "timestamp", "ue_id", "rnti")}}

    profiles = {}
    for name, fields in PROFILES.items():
        profile = compare_records(sources, database, fields)
        files, categories, disagreements = _breakdown(profile, source_refs, database_refs)
        profile.update(source_files=files, database_categories=categories,
                       unique_pair_folder_label_disagreements=disagreements)
        profiles[name] = profile
    for item in inventory["input_files"]:
        if sha256(root / item["path"]) != item["sha256"]:
            raise ValueError(f"Input changed during reconciliation: {item['path']}")
    return {
        "format_version": 1,
        "semantics": "Exact candidate agreement on stated projections; not authoritative provenance or run identity. No rounding, timestamps filled, candidate consumption or row exclusion. PMI representations not compared.",
        "input_files": inventory["input_files"],
        "extraction_manifest_check": inventory["extraction_manifest_check"],
        "input_hashes_unchanged": True,
        "source_records": list(source_refs.values()), "database_records": list(database_refs.values()),
        "profiles": profiles,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    if args.output.resolve().is_relative_to(args.root.resolve()):
        parser.error("Write diagnostics outside the input directory")
    if args.output.exists():
        parser.error("Output already exists; choose a new filename")
    report = build_reconciliation(args.root)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(report, stream, indent=2, sort_keys=True, allow_nan=False)
        stream.write("\n")
    for name, profile in report["profiles"].items():
        print(name, "sources:", profile["source_counts"], "database:", profile["database_counts"])
    print("Saved", args.output, "; input hashes unchanged")


if __name__ == "__main__":
    main()
