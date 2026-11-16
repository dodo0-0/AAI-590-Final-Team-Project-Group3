"""Label-support allocation and leakage guards using synthetic group references."""

from copy import deepcopy
import hashlib
import json

import pytest

from reliability.split_manifest import assemble_splits, apportion, build_splits


def fixture():
    rows, windows = [], []
    counts = {"Benign": 10, "BruteForce": 4, "DDoS": 9, "DoS": 3, "Probe": 7, "Web Attacks": 7}
    for category, n in counts.items():
        for i in range(n):
            rowid = len(rows)+1
            group = f"{category}_{i}"
            rows.append({"database_rowid": rowid, "provisional_group_id": group,
                         "source_path": group+'.txt', "cohort": "primary_temporal",
                         "attack_category": category, "traffic_type": int(category != "Benign")})
            windows.append({"window_id": f"w{rowid}", "provisional_group_id": group,
                            "is_partial": i == 0, "report_references": [{"database_rowid": rowid}]})
    for i in range(3):
        rows.append({"database_rowid": len(rows)+1, "provisional_group_id": f"secondary_{i}",
                     "source_path": f"secondary_{i}.txt", "cohort": "secondary_non_temporal_only",
                     "attack_category": "DoS", "traffic_type": 1})
    return {"rows": rows}, {"windows": windows}


def test_group_partitions_cover_every_row_and_window_without_overlap():
    cohort, windows = fixture()
    result = assemble_splits(cohort, windows)
    groups = [set(result['partitions'][name]['group_ids']) for name in ('train','validation','test')]
    assert not (groups[0]&groups[1] or groups[0]&groups[2] or groups[1]&groups[2])
    assert len(set.union(*groups)) == 43
    assert [sum(result['partitions'][name]['primary_category_group_counts'].values()) for name in ('train','validation','test')] == [24,8,8]
    assert [result['partitions'][name]['primary_category_group_counts']['Benign'] for name in ('train','validation','test')] == [6,2,2]
    assert [len(g) for g in groups] == [25,9,9]
    assert len(result['row_assignments']) == 43 and len(result['window_assignments']) == 40
    assert sum(w['is_partial'] for w in result['window_assignments']) == 6


def test_cv_is_training_only_and_has_both_classes():
    cohort, windows = fixture()
    result = assemble_splits(cohort, windows)
    train = set(result['partitions']['train']['group_ids'])
    heldout_union = set()
    for fold in result['cv_folds']:
        fitting, heldout = set(fold['fit_group_ids']), set(fold['heldout_group_ids'])
        assert not fitting&heldout and fitting|heldout == train
        assert not heldout_union&heldout
        heldout_union |= heldout
        for support in (fold['primary_fit_category_counts'],fold['primary_heldout_category_counts']):
            assert support['Benign']>0 and sum(support.values())>support['Benign']
    assert heldout_union == train
    assert all(r['training_cv_heldout_fold'] is None for r in result['row_assignments'] if r['partition']!='train')


def test_reproducible_independent_of_input_order_and_unused_scores():
    cohort, windows = fixture()
    before = deepcopy((cohort,windows))
    expected = assemble_splits(cohort,windows)
    assert (cohort,windows)==before
    changed = deepcopy(cohort)
    changed['rows'].reverse()
    for i,row in enumerate(changed['rows']):row['unused_model_score']=i/100
    assert expected==assemble_splits(changed,{'windows':list(reversed(windows['windows']))})


def test_inadequate_group_support_fails_instead_of_row_split():
    with pytest.raises(ValueError,match='Insufficient groups'):
        apportion(2)


def test_unknown_label_or_mixed_group_fails():
    cohort, windows = fixture()
    cohort['rows'][0]['traffic_type']=1
    with pytest.raises(ValueError,match='inconsistent'):
        assemble_splits(cohort,windows)
    cohort, windows = fixture()
    cohort['rows'][10]['provisional_group_id']=cohort['rows'][0]['provisional_group_id']
    with pytest.raises(ValueError,match='Mixed-category'):
        assemble_splits(cohort,windows)


def test_window_group_mismatch_or_missing_primary_window_fails():
    cohort, windows = fixture()
    windows['windows'][0]['provisional_group_id']=cohort['rows'][1]['provisional_group_id']
    with pytest.raises(ValueError,match='disagrees'):
        assemble_splits(cohort,windows)
    cohort, windows = fixture()
    windows['windows'].pop()
    with pytest.raises(ValueError,match='complete primary cohort'):
        assemble_splits(cohort,windows)


def test_parent_artifact_and_raw_snapshot_mismatches_fail(tmp_path):
    root=tmp_path/'raw'
    root.mkdir()
    raw=root/'snapshot.txt'
    raw.write_bytes(b'original')
    cohort,windows=fixture()
    cohort['input_files']=[{'path':'snapshot.txt','bytes':8,'sha256':hashlib.sha256(raw.read_bytes()).hexdigest()}]
    cp,wp=tmp_path/'cohort.json',tmp_path/'windows.json'
    cp.write_text(json.dumps(cohort),encoding='utf-8')
    windows['cohort_manifest_sha256']=hashlib.sha256(cp.read_bytes()).hexdigest()
    wp.write_text(json.dumps(windows),encoding='utf-8')
    assert build_splits(root,cp,wp)['input_snapshot_verified']
    windows['cohort_manifest_sha256']='wrong'
    wp.write_text(json.dumps(windows),encoding='utf-8')
    with pytest.raises(ValueError,match='identities disagree'):
        build_splits(root,cp,wp)
    windows['cohort_manifest_sha256']=hashlib.sha256(cp.read_bytes()).hexdigest()
    wp.write_text(json.dumps(windows),encoding='utf-8')
    raw.write_bytes(b'modified')
    with pytest.raises(ValueError,match='snapshot mismatch'):
        build_splits(root,cp,wp)
