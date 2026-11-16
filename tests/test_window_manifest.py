"""Synthetic report-index grids; no model or clock-unit assumptions."""

import hashlib
import json

import pytest

from reliability.window_manifest import build_windows


def fixture(tmp_path):
    root = tmp_path / "raw"
    source = root / "DoS/DoS/Lower_Layer/example.txt"
    source.parent.mkdir(parents=True)
    values = []
    for i in range(13):
        values.append({"timestamp": 1000*(i+1), "ue_id": 1, "cellid": 7, "rnti": "a"})
        if i < 8:
            values.append({"timestamp": 1000*(i+1), "ue_id": 2, "cellid": 7, "rnti": "b"})
    source.write_text(''.join(json.dumps(v)+'\n' for v in values), encoding="utf-8")
    path = source.relative_to(root).as_posix()
    manifest = {"input_files": [{"path": path, "bytes": source.stat().st_size,
                                 "sha256": hashlib.sha256(source.read_bytes()).hexdigest()}],
                "groups": [{"group_id": "g", "source_files": [path]}],
                "cohort_counts": {"primary_temporal": len(values)},
                "rows": [{"database_rowid": i+1, "source_line": i+1, "source_path": path,
                          "provisional_group_id": "g", "cohort": "primary_temporal",
                          "traffic_type": 1, "attack_category": "DoS", "attack_subcategory": "example"}
                         for i in range(len(values))]}
    p = tmp_path / "cohort.json"
    p.write_text(json.dumps(manifest), encoding="utf-8")
    return root, source, p, manifest


def test_interleaved_streams_retained_tails_and_exact_accounting(tmp_path):
    root, source, p, _ = fixture(tmp_path)
    before = source.read_bytes()
    result = build_windows(root, p)
    assert result["complete_windows"] == 1 and result["partial_windows"] == 2
    assert sorted(w["reports"] for w in result["windows"]) == [3, 8, 10]
    assert all(w["expected_report_count"] == w["reports"] for w in result["windows"])
    assert len({r["database_rowid"] for w in result["windows"] for r in w["report_references"]}) == 21
    assert all(w["short_input_reason_if_unsupported"] == "SHORT_WINDOW" for w in result["windows"] if w["is_partial"])
    assert all("split" not in w and "prediction" not in w for w in result["windows"])
    assert result == build_windows(root, p)
    assert source.read_bytes() == before


def test_linked_files_share_group_but_not_windows(tmp_path):
    root, source, p, manifest = fixture(tmp_path)
    second = source.with_name("second.txt")
    second.write_bytes(source.read_bytes())
    second_path = second.relative_to(root).as_posix()
    manifest["input_files"].append({"path": second_path, "bytes": second.stat().st_size,
                                   "sha256": hashlib.sha256(second.read_bytes()).hexdigest()})
    manifest["groups"][0]["source_files"].append(second_path)
    manifest["rows"] += [{**r, "source_path": second_path, "database_rowid": r["database_rowid"]+21} for r in list(manifest["rows"])]
    manifest["cohort_counts"]["primary_temporal"] = 42
    p.write_text(json.dumps(manifest), encoding="utf-8")
    result = build_windows(root, p)
    assert len(result["windows"]) == 6
    assert len({w["window_id"] for w in result["windows"]}) == 6
    assert {w["provisional_group_id"] for w in result["windows"]} == {"g"}


def test_unselected_interior_observation_not_silently_bridged(tmp_path):
    root, _, p, manifest = fixture(tmp_path)
    manifest["rows"][4]["cohort"] = "secondary_non_temporal_only"
    manifest["cohort_counts"] = {"primary_temporal": 20, "secondary_non_temporal_only": 1}
    p.write_text(json.dumps(manifest), encoding="utf-8")
    with pytest.raises(ValueError, match="continuity review"):
        build_windows(root, p)


def test_nonincreasing_clock_not_sorted_or_repaired(tmp_path):
    root, source, p, manifest = fixture(tmp_path)
    rows = [json.loads(line) for line in source.read_text().splitlines()]
    rows[2]["timestamp"] = 500
    source.write_text(''.join(json.dumps(v)+'\n' for v in rows), encoding="utf-8")
    manifest["input_files"][0].update(bytes=source.stat().st_size, sha256=hashlib.sha256(source.read_bytes()).hexdigest())
    p.write_text(json.dumps(manifest), encoding="utf-8")
    with pytest.raises(ValueError, match="Non-increasing"):
        build_windows(root, p)


def test_mixed_window_labels_require_review(tmp_path):
    root, _, p, manifest = fixture(tmp_path)
    manifest["rows"][0]["attack_subcategory"] = "different"
    p.write_text(json.dumps(manifest), encoding="utf-8")
    with pytest.raises(ValueError, match="Mixed or missing"):
        build_windows(root, p)


def test_changed_source_snapshot_is_rejected(tmp_path):
    root, source, p, _ = fixture(tmp_path)
    source.write_bytes(source.read_bytes()+b'\n')
    with pytest.raises(ValueError, match="snapshot mismatch"):
        build_windows(root, p)


def test_one_file_cannot_span_groups(tmp_path):
    root, _, p, manifest = fixture(tmp_path)
    manifest["groups"].append({"group_id": "other", "source_files": manifest["groups"][0]["source_files"]})
    manifest["rows"][0]["provisional_group_id"] = "other"
    p.write_text(json.dumps(manifest), encoding="utf-8")
    with pytest.raises(ValueError, match="multiple provisional groups"):
        build_windows(root, p)
