import math
import json
from hashlib import sha256

import pytest

from reliability.eda_summary import describe, correlation, build_summary


def test_quantiles_spread_and_sample_sd():
    s=describe([0,10,20,30])
    assert s["median"]==15 and s["q25"]==7.5 and s["q75"]==22.5
    assert s["p05"]==pytest.approx(1.5) and s["p95"]==pytest.approx(28.5) and s["iqr"]==15
    assert s["mean"]==15 and s["std_sample"]==pytest.approx(math.sqrt(500/3))


def test_missing_invalid_and_empty_are_explicit():
    s=describe([None,False,"2",float("nan"),float("inf"),2])
    assert s["finite"]==1 and s["missing"]==1 and s["invalid_nonmissing"]==4
    assert s["std_sample"] is None and s["median"]==2
    assert describe([])["median"] is None and describe([])["missing_pct"] is None


def test_correlation_uses_pairs_and_exposes_constant_or_too_few():
    assert correlation([(1,2),(2,4),(3,6),(None,8)])["r"]==pytest.approx(1)
    assert correlation([(1,2),(2,4),(3,6),(None,8)])["excluded"]==1
    assert correlation([(1,3),(2,2),(3,1)])["r"]==pytest.approx(-1)
    assert correlation([(1,2),(1,3)])["reason"]=="CONSTANT_INPUT"
    assert correlation([(False,2),(1,3)])["reason"]=="TOO_FEW_PAIRS"


def test_large_offsets_do_not_destroy_correlation():
    assert correlation([(10**12+i, 10**12+2*i) for i in range(10)])["r"]==pytest.approx(1)


def test_wrong_parent_or_timing_snapshot_fails_before_reading_database(tmp_path):
    paths=[tmp_path/name for name in ['cohort.json','windows.json','splits.json','timing.json']]
    def write(path,data):
        path.write_text(json.dumps(data),encoding='utf-8')
        return sha256(path.read_bytes()).hexdigest()
    ch=write(paths[0],{'input_files':[]})
    wh=write(paths[1],{'cohort_manifest_sha256':'wrong'})
    write(paths[2],{'cohort_manifest_sha256':ch,'window_manifest_sha256':wh})
    write(paths[3],{'input_files':[]})
    with pytest.raises(ValueError,match='Parent manifest'):
        build_summary(tmp_path,*paths)
    wh=write(paths[1],{'cohort_manifest_sha256':ch})
    write(paths[2],{'cohort_manifest_sha256':ch,'window_manifest_sha256':wh})
    write(paths[3],{'input_files':[{'path':'different'}]})
    with pytest.raises(ValueError,match='snapshots disagree'):
        build_summary(tmp_path,*paths)
