"""Synthetic timing tests; stream identities are deliberately not run IDs."""

from copy import deepcopy
from zipfile import ZipFile

from reliability.reconciliation import RADIO_FIELDS
from reliability.timing_audit import (
    describe_sequence, describe_streams, describe_overlaps, metadata_coincidences, inspect_archive,
)


def record(path, line, timestamp, ue=1, radio=1):
    return {"path": path, "line": line, "values": {
        **{f: radio for f in RADIO_FIELDS}, "timestamp": timestamp,
        "ue_id": ue, "cellid": 7, "rnti": "a", "in_sync": 1,
    }}


def test_original_order_backwards_zeros_and_missing_adjacency():
    rows = [{"line": i+1, "timestamp": t} for i, t in enumerate([1000, 2000, 1500, 1500, None, 3000])]
    before = deepcopy(rows)
    summary = describe_sequence(rows)
    assert summary["finite_timestamps"] == 5
    assert summary["adjacent_comparable_pairs"] == 3
    assert summary["positive_steps"] == summary["negative_steps"] == summary["zero_steps"] == 1
    assert summary["positive_step_max_raw"] == 1000
    assert summary["repeated_timestamp_occurrences"] == 1
    assert summary["nonpositive_step_locations"][0] == {"previous_line": 2, "line": 3, "delta_raw": -500}
    assert rows == before


def test_interleaved_ues_do_not_create_zero_steps():
    records = [record("a", 1, 1000, ue=1), record("a", 2, 1000, ue=2),
               record("a", 3, 2000, ue=1), record("a", 4, 2000, ue=2)]
    streams, _, unusable = describe_streams(records)
    assert len(streams) == 2 and not unusable
    assert all(s["zero_steps"] == 0 and s["positive_step_median_raw"] == 1000 for s in streams)


def test_interval_overlap_is_not_shared_observation():
    observations = [record("a", 1, 0), record("a", 2, 10), record("b", 1, 5), record("b", 2, 15)]
    streams, internals, _ = describe_streams(observations)
    overlap = describe_overlaps(streams, internals)["range_overlaps"][0]
    assert overlap["raw_overlap_start"] == 5 and overlap["raw_overlap_end"] == 10
    assert overlap["common_distinct_timestamps"] == 0
    assert overlap["shared_radio_metadata_occurrences"] == 0


def test_exact_shared_occurrences_preserve_multiplicity():
    observations = [record("a", 1, 1000), record("a", 2, 1000), record("b", 1, 1000)]
    streams, internals, _ = describe_streams(observations)
    overlap = describe_overlaps(streams, internals)["range_overlaps"][0]
    assert overlap["common_distinct_timestamps"] == 1
    assert overlap["shared_radio_metadata_occurrences"] == 1


def test_different_identities_are_not_merged_by_timestamp():
    observations = [record("a", 1, 1000, ue=1), record("b", 1, 1000, ue=2)]
    streams, internals, _ = describe_streams(observations)
    assert describe_overlaps(streams, internals)["same_identity_cross_file_pairs_compared"] == 0


def test_coincidences_retain_all_locations_without_claiming_radio_equality():
    sources = [record("a", 1, 1000, radio=1), record("b", 4, 1000, radio=1), record("c", 2, 1000, ue=2)]
    query = {"source_path": "no_clock", "source_line": 3, "database_rowid": 99,
             "values": record("unused", 0, 1000, radio=2)["values"]}
    rows = metadata_coincidences(sources, [query])
    assert [(r["path"], r["line"]) for r in rows[0]["coincident_source_observations"]] == [("a", 1), ("b", 4)]
    assert not any(r["radio_values_also_equal"] for r in rows[0]["coincident_source_observations"])


def test_missing_or_invalid_clocks_not_invented():
    sources = [record("a", 1, None), record("a", 2, True), record("a", 3, "1000")]
    streams, _, _ = describe_streams(sources)
    assert streams[0]["finite_timestamps"] == 0
    query = {"source_path": "a", "source_line": 1, "database_rowid": 1, "values": sources[0]["values"]}
    result = metadata_coincidences(sources, [query])[0]
    assert result["comparison_issue"]["missing_or_null_fields"] == ["timestamp"]
    assert not result["coincident_source_observations"]


def test_unusable_identity_is_preserved_separately():
    observation = record("a", 1, 1000)
    del observation["values"]["ue_id"]
    streams, _, unusable = describe_streams([observation])
    assert streams == []
    assert unusable[0]["line"] == 1 and unusable[0]["missing_or_null_fields"] == ["ue_id"]


def test_archive_inventory_checks_names_without_extracting(tmp_path):
    archive = tmp_path / "sample.zip"
    with ZipFile(archive, "w") as z:
        z.writestr("README.md", "capture notes")
        z.writestr("radio.txt", "example")
    report = inspect_archive(archive)
    assert report["file_entries"] == 2
    assert report["provenance_filename_candidates"] == ["README.md"]
    assert not (tmp_path / "README.md").exists()
    assert inspect_archive(None)["status"].startswith("not supplied")
