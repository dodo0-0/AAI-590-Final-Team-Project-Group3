"""Synthetic logic tests, not empirical dataset evidence."""

import hashlib
import json
from pathlib import Path
import sqlite3

import pytest

from reliability.data_audit import build_inventory, inspect_jsonl, inspect_sqlite, timestamp_summary, main


def fixture_root(tmp_path: Path) -> Path:
    root = tmp_path / "radio"
    source = root / "Benign/Benign/Lower_Layer/sample.txt"
    source.parent.mkdir(parents=True)
    source.write_text('{"timestamp": 1000, "ue_id": 1}\n', encoding="utf-8")
    with sqlite3.connect(root / "Lower_Layer_Data.db") as conn:
        conn.execute('CREATE TABLE "odd""table" (timestamp REAL, attack_category TEXT, "null" TEXT)')
        conn.executemany('INSERT INTO "odd""table" VALUES (?,?,?)',
                         [(1000, "Benign", None), (None, "DoS", None)])
    return root


def test_missing_database_does_not_create_file(tmp_path):
    missing = tmp_path / "missing.db"
    with pytest.raises(FileNotFoundError):
        inspect_sqlite(missing)
    assert not missing.exists()


def test_quoted_sql_identifiers_nulls_and_label_counts(tmp_path):
    root = fixture_root(tmp_path)
    database = root / "Lower_Layer_Data.db"
    before = database.read_bytes()
    table = inspect_sqlite(database)["tables"]['odd"table']
    assert table["rows"] == 2
    assert table["columns"][2]["null_count"] == 2
    assert table["labels"]["attack_category"] == [
        {"value": "Benign", "rows": 1}, {"value": "DoS", "rows": 1}]
    assert table["timestamp"]["finite_numeric"] == 1
    assert database.read_bytes() == before


def test_jsonl_absent_null_invalid_records_and_physical_lines(tmp_path):
    source = tmp_path / "source.txt"
    source.write_text('\ufeff{"timestamp": 1000, "x": null}\n\n'
                      '{"x": 2}\n{bad}\n[]\n{"timestamp": NaN}\n', encoding="utf-8")
    report = inspect_jsonl(source)
    assert report["valid_object_records"] == 2
    assert report["blank_lines"] == 1
    assert [e["line"] for e in report["invalid_records"]] == [4, 5, 6]
    assert report["fields"]["timestamp"]["absent"] == 1
    assert report["fields"]["x"]["null"] == 1
    assert report["timestamp"]["finite_numeric"] == 1


def test_timestamp_numbers_do_not_include_boolean_or_nonfinite():
    summary = timestamp_summary([False, None, "1000", float("inf"), 1000, 1000, 2000])
    assert summary["invalid_nonnull"] == 3
    assert summary["finite_numeric"] == 3
    assert summary["distinct_numeric"] == 2
    assert summary["units_and_timezone"] == "unverified"


def test_inventory_determinism_and_manifest_tampering(tmp_path):
    root = fixture_root(tmp_path)
    records = [{"archive_member": p.relative_to(root).as_posix(),
                "bytes": p.stat().st_size, "sha256": hashlib.sha256(p.read_bytes()).hexdigest()}
               for p in sorted(root.rglob("*")) if p.is_file()]
    (root / "extraction_manifest.json").write_text(json.dumps({"files": records}), encoding="utf-8")
    first = build_inventory(root)
    assert first == build_inventory(root)
    assert first["input_hashes_unchanged"]
    source = root / "Benign/Benign/Lower_Layer/sample.txt"
    source.write_text('{}\n', encoding="utf-8")
    with pytest.raises(ValueError, match="manifest mismatch"):
        build_inventory(root)


def test_empty_source_collection_is_not_silently_accepted(tmp_path):
    root = fixture_root(tmp_path)
    (root / "Benign/Benign/Lower_Layer/sample.txt").unlink()
    with pytest.raises(ValueError, match="No source"):
        build_inventory(root)


def test_manifest_missing_member_is_not_silently_ignored(tmp_path):
    root = fixture_root(tmp_path)
    (root / "extraction_manifest.json").write_text('{"files": []}', encoding="utf-8")
    with pytest.raises(ValueError, match="differ from extraction manifest"):
        build_inventory(root)


def test_cli_rejects_output_in_input_directory(tmp_path, monkeypatch):
    root = fixture_root(tmp_path)
    output = root / "inventory.json"
    monkeypatch.setattr("sys.argv", ["data_audit", "--root", str(root), "--output", str(output)])
    with pytest.raises(SystemExit) as error:
        main()
    assert error.value.code == 2
    assert not output.exists()
