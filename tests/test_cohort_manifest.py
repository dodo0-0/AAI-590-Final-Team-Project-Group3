"""Approved eligibility/grouping logic tested with synthetic references."""

from copy import deepcopy
import json
import hashlib

import pytest

from reliability.cohort_manifest import assemble_manifest, build_manifest


def report():
    return {
        "source_records": [{"id": i, "path": path, "line": i+1}
                           for i, path in enumerate(["a.txt", "a.txt", "b.txt", "c.txt"])],
        "database_records": [{"rowid": i+10, "attack_category": "DoS", "attack_subcategory": "example", "traffic_type": 1} for i in range(4)],
        "profiles": {
            "radio_metadata_exact": {"groups": [
                {"status": "unique_candidate_pair", "source_ids": [i], "database_rowids": [i+10]} for i in range(3)]},
            "radio_exact": {"groups": [
                {"status": "unique_candidate_pair", "source_ids": [3], "database_rowids": [13]}]},
        }, "input_files": [],
    }


def test_primary_secondary_membership_and_whole_file_grouping():
    source = report()
    before = deepcopy(source)
    manifest = assemble_manifest(source)
    assert manifest["cohort_counts"] == {"primary_temporal": 3, "secondary_non_temporal_only": 1}
    assert manifest["rows"][0]["provisional_group_id"] == manifest["rows"][1]["provisional_group_id"]
    assert len(manifest["groups"]) == 3
    assert all("split" not in r and "timestamp" not in r for r in manifest["rows"])
    assert source == before


def test_transitive_capture_links_merge_files_with_evidence():
    links = [{"files": ["a.txt", "b.txt"], "evidence": "manifest A"},
             {"files": ["b.txt", "c.txt"], "evidence": "manifest B"}]
    merged = assemble_manifest(report(), links)
    assert len(merged["groups"]) == 1
    assert merged["groups"][0]["source_files"] == ["a.txt", "b.txt", "c.txt"]
    assert merged == assemble_manifest(report(), list(reversed(links)))


def test_unknown_or_unsupported_capture_links_rejected():
    with pytest.raises(ValueError, match="evidence reference"):
        assemble_manifest(report(), [{"files": ["a.txt", "b.txt"], "evidence": ""}])
    with pytest.raises(ValueError, match="unknown source file"):
        assemble_manifest(report(), [{"files": ["a.txt", "other.txt"], "evidence": "source note"}])


def test_ambiguous_lineage_is_not_resolved_by_first_match():
    value = report()
    value["profiles"]["radio_exact"]["groups"][0] = {
        "status": "ambiguous_candidate_group", "source_ids": [2, 3], "database_rowids": [13]}
    with pytest.raises(ValueError, match="manual review required"):
        assemble_manifest(value)


def test_snapshot_validation_detects_changed_input(tmp_path):
    root = tmp_path / "raw"
    root.mkdir()
    source = root / "source.txt"
    source.write_bytes(b"original")
    value = report()
    value["input_files"] = [{"path": "source.txt", "bytes": 8, "sha256": hashlib.sha256(b"original").hexdigest()}]
    artifact = tmp_path / "reconciliation.json"
    artifact.write_text(json.dumps(value), encoding="utf-8")
    assert build_manifest(root, artifact)["input_snapshot_verified"]
    source.write_bytes(b"modified")
    with pytest.raises(ValueError, match="differs from reconciled snapshot"):
        build_manifest(root, artifact)


def test_inconsistent_candidate_profiles_are_rejected():
    value = report()
    value["profiles"]["radio_exact"]["groups"].append(
        {"status": "unique_candidate_pair", "source_ids": [2], "database_rowids": [10]})
    with pytest.raises(ValueError, match="disagree"):
        assemble_manifest(value)
    value = report()
    value["profiles"]["radio_metadata_exact"]["groups"][1]["source_ids"] = [0]
    with pytest.raises(ValueError, match="duplicated candidate"):
        assemble_manifest(value)
