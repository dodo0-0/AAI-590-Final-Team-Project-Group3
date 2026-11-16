"""Synthetic AP-1 mask cases; no dataset or model-quality claims."""

from copy import deepcopy

import pytest

from reliability.completeness import summarize_completeness


def test_least_observed_required_kpi_controls_quality():
    positions = [str(i) for i in range(10)]
    masks = {'a': dict.fromkeys(positions, True),
             'b': {p: i < 6 for i, p in enumerate(positions)}}
    report = summarize_completeness(positions, ['a', 'b'], masks)
    assert report['quality'] == 0.6 and report['reason'] is None
    assert report['per_kpi']['b'] == dict(observed_valid_count=6,
        known_missing_or_invalid_count=4, unknown_count=0, fraction=0.6)


def test_known_absent_required_kpi_cannot_be_hidden_by_healthy_kpi():
    report = summarize_completeness(['p'], ['a', 'b'], {'a': {'p': True}, 'b': {'p': False}})
    assert report['quality'] == 0 and report['reason'] is None


def test_complete_tail_uses_actual_expected_count_and_optional_kpi_is_ignored():
    report = summarize_completeness(['1', '2', '3'], ['a'],
        {'a': {'1': True, '2': True, '3': True}, 'optional': None})
    assert report['quality'] == 1 and report['expected_report_count'] == 3
    assert set(report['per_kpi']) == {'a'}


@pytest.mark.parametrize('masks', [None, {}, {'a': None}, {'a': {}}, {'a': {'p': None}}])
def test_unknown_metadata_is_not_zero_or_perfect_quality(masks):
    report = summarize_completeness(['p'], ['a'], masks)
    assert report['quality'] is None and report['reason'] == 'QUALITY_UNAVAILABLE'
    assert report['per_kpi']['a']['unknown_count'] == 1


def test_partially_unknown_mask_retains_known_counts_without_a_quality_estimate():
    report = summarize_completeness(['1', '2', '3'], ['a'], {'a': {'1': True, '2': False}})
    assert report['quality'] is None
    assert report['per_kpi']['a'] == dict(observed_valid_count=1,
        known_missing_or_invalid_count=1, unknown_count=1, fraction=None)


def test_unavailable_expected_grid_has_unknown_quality():
    report = summarize_completeness(None, ['a'], None)
    assert report == dict(quality=None, reason='QUALITY_UNAVAILABLE',
                          expected_report_count=None, per_kpi={})


@pytest.mark.parametrize('positions,required', [([], ['a']), (['p', 'p'], ['a']),
    (['p'], []), (['p'], ['a', 'a']), ('p', ['a']), (['p'], 'a'), ([''], ['a']), ([1], ['a'])])
def test_invalid_or_duplicate_configuration_fails(positions, required):
    with pytest.raises(ValueError):
        summarize_completeness(positions, required, None)


@pytest.mark.parametrize('masks', [{'a': {'outside': True}}, {'a': {'p': 1}},
    {'a': {'p': 'true'}}, {'a': [True]}, [True]])
def test_invalid_masks_and_out_of_grid_reports_fail(masks):
    with pytest.raises(ValueError):
        summarize_completeness(['p'], ['a'], masks)


def test_order_invariance_and_inputs_preserved():
    positions, required = ['p', 'q'], ['b', 'a']
    masks = {'a': {'p': True, 'q': False}, 'b': {'p': True, 'q': True}}
    before = deepcopy((positions, required, masks))
    report = summarize_completeness(positions, required, masks)
    assert report == summarize_completeness(list(reversed(positions)), list(reversed(required)), masks)
    assert (positions, required, masks) == before
