"""Read-only structural inventory. No run inference or feature selection.

From the workspace root:
  python src/reliability/data_audit.py --root data/radio --output results/inventory.json
"""

from __future__ import annotations

import argparse
from collections import Counter
from contextlib import closing
import hashlib
import json
import math
from pathlib import Path
import sqlite3


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def quote_identifier(value: str) -> str:
    return '"' + value.replace('"', '""') + '"'


def timestamp_summary(values: list[object]) -> dict:
    """Describe raw numbers without assigning units, timezone or gap boundaries."""
    numeric = [v for v in values if type(v) in (int, float) and math.isfinite(v)]
    return {
        "present_nonnull": sum(v is not None for v in values),
        "finite_numeric": len(numeric),
        "invalid_nonnull": sum(v is not None for v in values) - len(numeric),
        "raw_min": min(numeric) if numeric else None,
        "raw_max": max(numeric) if numeric else None,
        "distinct_numeric": len(set(numeric)),
        "units_and_timezone": "unverified",
    }


def inspect_jsonl(path: Path) -> dict:
    """Count records and absent/null fields; retain physical error line numbers."""
    present: Counter = Counter()
    nulls: Counter = Counter()
    types: dict[str, Counter] = {}
    timestamps = []
    errors = []
    records = blanks = lines = 0

    def reject_constant(value: str) -> None:
        raise ValueError(f"Non-standard JSON constant: {value}")

    with path.open(encoding="utf-8-sig") as stream:
        for lines, line in enumerate(stream, 1):
            if not line.strip():
                blanks += 1
                continue
            try:
                record = json.loads(line, parse_constant=reject_constant)
                if not isinstance(record, dict):
                    raise ValueError("Expected a JSON object")
            except ValueError as exc:
                errors.append({"line": lines, "error": str(exc)})
                continue
            records += 1
            timestamps.append(record.get("timestamp"))
            for key, value in record.items():
                present[key] += 1
                nulls[key] += value is None
                types.setdefault(key, Counter())[type(value).__name__] += 1
    fields = {
        key: {"present": present[key], "absent": records - present[key],
              "null": nulls[key], "types": dict(sorted(types[key].items()))}
        for key in sorted(present)
    }
    return {"physical_lines": lines, "blank_lines": blanks,
            "valid_object_records": records, "invalid_records": errors,
            "fields": fields, "timestamp": timestamp_summary(timestamps)}


def inspect_sqlite(path: Path) -> dict:
    """Open an existing SQLite database read-only; never create a missing DB."""
    if not path.is_file():
        raise FileNotFoundError(path)
    tables = {}
    with closing(sqlite3.connect(path.resolve().as_uri() + "?mode=ro", uri=True)) as conn:
        conn.execute("PRAGMA query_only=ON")
        names = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' "
            "AND name NOT LIKE 'sqlite_%' ORDER BY name"
        ).fetchall()
        for (name,) in names:
            table = quote_identifier(name)
            columns = []
            for _, column, declared_type, notnull, default, pk in conn.execute(
                f"PRAGMA table_info({table})"
            ):
                quoted = quote_identifier(column)
                null_count, distinct_count = conn.execute(
                    f"SELECT COUNT(*)-COUNT({quoted}), COUNT(DISTINCT {quoted}) FROM {table}"
                ).fetchone()
                columns.append({"name": column, "declared_type": declared_type,
                                "notnull": bool(notnull), "default": default,
                                "primary_key": pk, "null_count": null_count,
                                "distinct_nonnull": distinct_count})
            column_names = {c["name"] for c in columns}
            labels = {}
            for label in ("traffic_type", "attack_category", "attack_subcategory"):
                if label in column_names:
                    q = quote_identifier(label)
                    labels[label] = [
                        {"value": value, "rows": count}
                        for value, count in conn.execute(
                            f"SELECT {q}, COUNT(*) FROM {table} GROUP BY {q} ORDER BY {q}"
                        )
                    ]
            timestamps = [row[0] for row in conn.execute(f'SELECT "timestamp" FROM {table}')] if "timestamp" in column_names else []
            tables[name] = {
                "rows": conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0],
                "columns": columns, "labels": labels,
                "timestamp_column_present": "timestamp" in column_names,
                "timestamp": timestamp_summary(timestamps),
            }
    return {"tables": tables}


def build_inventory(root: Path) -> dict:
    root = root.resolve()
    database = root / "Lower_Layer_Data.db"
    if not database.is_file():
        raise FileNotFoundError(database)
    sources = sorted(root.glob("*/*/Lower_Layer/*.txt"))
    if not sources:
        raise ValueError("No source radio text files found at */*/Lower_Layer/*.txt")
    files = [database, *sources]
    before = {p.relative_to(root).as_posix(): sha256(p) for p in files}
    manifest_path = root / "extraction_manifest.json"
    manifest_status = "not supplied"
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        expected = {r["archive_member"]: r for r in manifest["files"]}
        if expected.keys() != before.keys():
            raise ValueError("Discovered radio files differ from extraction manifest")
        for p in files:
            key = p.relative_to(root).as_posix()
            if before[key] != expected[key]["sha256"] or p.stat().st_size != expected[key]["bytes"]:
                raise ValueError(f"Extraction manifest mismatch: {key}")
        manifest_status = "all selected file sizes and SHA-256 verified"
    report = {"inventory_format_version": 1, "extraction_manifest_check": manifest_status,
              "database": inspect_sqlite(database), "sources": []}
    for path in sources:
        key = path.relative_to(root).as_posix()
        report["sources"].append({"path": key, "category_from_folder": path.relative_to(root).parts[0],
                                  "label_status": "folder-derived, not validated against database",
                                  **inspect_jsonl(path)})
    for path in files:
        key = path.relative_to(root).as_posix()
        if sha256(path) != before[key]:
            raise ValueError(f"Input changed during inspection: {key}")
    report["input_files"] = [{"path": key, "sha256": before[key],
                               "bytes": (root / key).stat().st_size} for key in sorted(before)]
    report["input_hashes_unchanged"] = True
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.resolve().is_relative_to(args.root.resolve()):
        parser.error("Write inventory outside the input directory")
    report = build_inventory(args.root)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x", encoding="utf-8") as stream:
        json.dump(report, stream, indent=2, sort_keys=True, allow_nan=False)
        stream.write("\n")
    print(f"Wrote {args.output}: {len(report['sources'])} source files; input hashes unchanged")


if __name__ == "__main__":
    main()
