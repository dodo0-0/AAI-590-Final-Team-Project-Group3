"""Synthetic candidate/multiplicity checks, not empirical run evidence."""

import json
from pathlib import Path
import sqlite3

import pytest

from reliability.reconciliation import (
    METADATA_FIELDS, RADIO_FIELDS, build_reconciliation, compare_records, comparison_key, main,
)


def obs(identifier, **values):
    return {"id": identifier, "values": values}


def test_exact_numeric_equality_does_not_round():
    report = compare_records([obs(0, cqi=1), obs(1, cqi=1.0000000001)],
                             [obs(20, cqi=1.0)], ("cqi",))
    assert report["source_counts"]["unique_candidate_pair"] == 1
    assert report["source_counts"]["no_candidate"] == 1


@pytest.mark.parametrize("source_n,database_n", [(2, 1), (1, 2), (2, 2)])
def test_repeated_values_remain_ambiguous_without_consumption(source_n, database_n):
    report = compare_records([obs(i, cqi=10) for i in range(source_n)],
                             [obs(100+i, cqi=10) for i in range(database_n)], ("cqi",))
    assert report["source_counts"]["ambiguous_candidate_group"] == source_n
    assert report["database_counts"]["ambiguous_candidate_group"] == database_n
    assert report["source_counts"]["unique_candidate_pair"] == 0
    assert len(report["groups"]) == 1


def test_missing_and_invalid_keys_are_not_wildcard_matches():
    report = compare_records([obs(0), obs(1, cqi=None), obs(2, cqi=True),
                              obs(3, cqi="1"), obs(4, cqi=float("inf"))],
                             [obs(10, cqi=1)], ("cqi",))
    assert report["source_counts"]["unusable_key"] == 5
    assert report["database_counts"]["no_candidate"] == 1
    assert report["unusable_sources"][0]["missing_or_null_fields"] == ["cqi"]
    assert report["unusable_sources"][2]["invalid_fields"] == ["cqi"]


def test_labels_are_not_used_to_force_candidate_agreement():
    report = compare_records([obs(0, cqi=10, attack_category="DoS")],
                             [obs(10, cqi=10, attack_category="Benign")], ("cqi",))
    assert report["source_counts"]["unique_candidate_pair"] == 1


def test_metadata_disagreement_breaks_stronger_match():
    source = [obs(0, cqi=10, timestamp=1000, rnti="ab")]
    database = [obs(10, cqi=10, timestamp=2000, rnti="ab")]
    assert compare_records(source, database, ("cqi",))["source_counts"]["unique_candidate_pair"] == 1
    assert compare_records(source, database, ("cqi", "timestamp", "rnti"))["source_counts"]["no_candidate"] == 1
    assert comparison_key({"rnti": "ab"}, ("rnti",)) != comparison_key({"rnti": "AB"}, ("rnti",))


def test_empty_sides_and_duplicate_ids():
    report = compare_records([], [obs(10, cqi=1)], ("cqi",))
    assert report["database_counts"]["no_candidate"] == 1
    assert sum(report["source_counts"].values()) == 0
    with pytest.raises(ValueError, match="IDs must be unique"):
        compare_records([obs(1, cqi=1), obs(1, cqi=2)], [], ("cqi",))


def test_order_independent_group_output_and_complete_accounting():
    source = [obs(1, cqi=3), obs(0, cqi=1), obs(2)]
    db = [obs(20, cqi=1), obs(21, cqi=2), obs(22)]
    report = compare_records(source, db, ("cqi",))
    assert report == compare_records(list(reversed(source[:2])) + source[2:], list(reversed(db[:2])) + db[2:], ("cqi",))
    assert sum(report["source_counts"].values()) == len(source)
    assert sum(report["database_counts"].values()) == len(db)


def test_readonly_pipeline_preserves_missing_metadata_and_label_disagreement(tmp_path):
    root = tmp_path / "radio"
    source = root / "DoS/DoS/Lower_Layer/sample.txt"
    source.parent.mkdir(parents=True)
    first = {field: 1 for field in RADIO_FIELDS}
    first.update(timestamp=1000, ue_id=1, cellid=1, in_sync=1, rnti="ab")
    second = {field: 2 for field in RADIO_FIELDS}  # No observed metadata.
    source.write_text(json.dumps(first) + '\n' + json.dumps(second) + '\n', encoding="utf-8")
    fields = RADIO_FIELDS + METADATA_FIELDS + ("traffic_type", "attack_category", "attack_subcategory")
    columns = ', '.join('"' + field + '" ' + ('TEXT' if field in ('rnti', 'attack_category', 'attack_subcategory') else 'REAL') for field in fields)
    database = root / "Lower_Layer_Data.db"
    with sqlite3.connect(database) as conn:
        conn.execute(f"CREATE TABLE lower_layer_data ({columns})")
        second_db = {**second, "timestamp": 2000, "ue_id": 1, "cellid": 1, "in_sync": 1, "rnti": None}
        for values, category in [(first, "DoS"), (second_db, "Probe")]:
            values = {**values, "traffic_type": 1, "attack_category": category, "attack_subcategory": "example"}
            conn.execute('INSERT INTO lower_layer_data VALUES (' + ','.join('?' for _ in fields) + ')',
                         [values[field] for field in fields])
    before = {p: p.read_bytes() for p in (source, database)}
    report = build_reconciliation(root)
    assert report["profiles"]["radio_exact"]["source_counts"]["unique_candidate_pair"] == 2
    assert report["profiles"]["radio_metadata_exact"]["source_counts"]["unusable_key"] == 1
    assert report["profiles"]["radio_metadata_exact"]["database_counts"]["unusable_key"] == 1
    assert report["profiles"]["radio_exact"]["unique_pair_folder_label_disagreements"] == [{"source_id": 1, "database_rowid": 2}]
    assert report["source_records"][1]["line"] == 2
    assert report["database_records"][1]["rowid"] == 2
    assert all(p.read_bytes() == contents for p, contents in before.items())
    assert report == build_reconciliation(root)


def test_cli_rejects_output_among_inputs(tmp_path, monkeypatch):
    monkeypatch.setattr("sys.argv", ["reconciliation", "--root", str(tmp_path), "--output", str(tmp_path / "output.json")])
    with pytest.raises(SystemExit) as exc:
        main()
    assert exc.value.code == 2
    assert not (tmp_path / "output.json").exists()
