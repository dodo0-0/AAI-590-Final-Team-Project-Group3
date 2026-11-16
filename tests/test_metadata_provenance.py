"""Synthetic projected-clock diagnostics, never inferred capture histories."""

from copy import deepcopy

import pytest

from reliability.metadata_provenance import summarize_projected_clocks


def case(path, line, rowid, timestamp):
    return {"source_path": path, "source_line": line, "database_rowid": rowid,
            "database_compared_metadata": {"timestamp": timestamp, "ue_id": 1, "cellid": 7, "in_sync": 1}}


def test_database_order_is_not_substituted_for_source_order():
    cases = [case("a", 3, 1, 2000), case("a", 1, 3, 3000), case("a", 2, 2, 1000)]
    before = deepcopy(cases)
    result = summarize_projected_clocks(cases)
    sequence = result["files"][0]["projected_database_clock_in_source_line_order"]
    assert sequence["negative_steps"] == 1
    assert sequence["positive_steps"] == 1
    assert cases == before
    assert result == summarize_projected_clocks(list(reversed(cases)))


def test_tuple_reuse_across_files_is_not_deduplicated():
    result = summarize_projected_clocks([case("a", 1, 1, 1000), case("b", 1, 2, 1000)])
    assert result["cases"] == 2
    assert result["distinct_usable_metadata_tuples"] == 1
    assert result["repeated_tuple_excess"] == 1
    assert result["tuple_multiplicity_histogram"] == [{"multiplicity": 2, "distinct_tuples": 1}]


def test_missing_clock_remains_unknown_and_breaks_adjacency():
    result = summarize_projected_clocks([case("a", 1, 1, 1000), case("a", 2, 2, None), case("a", 3, 3, 3000)])
    file = result["files"][0]
    assert file["projected_database_clock_in_source_line_order"]["adjacent_comparable_pairs"] == 0
    assert len(file["unusable_metadata_keys"]) == 1
    assert result["usable_metadata_tuples"] == 2


def test_duplicate_candidate_references_fail_instead_of_selecting_one():
    with pytest.raises(ValueError, match="unique source occurrence"):
        summarize_projected_clocks([case("a", 1, 1, 1000), case("a", 1, 2, 2000)])
