"""Hand-computed EP-6 outcome cases; synthetic cases are not research results."""

import pytest

from reliability.outcome_metrics import summarize_outcomes


def test_full_two_by_three_table_and_denominators():
    report = summarize_outcomes([1, 1, 1, 0, 0, 0],
                               ["ATTACK", "BENIGN", "ABSTAIN", "ATTACK", "BENIGN", "ABSTAIN"])
    assert report["counts"] == dict(TP=1, FN=1, U_A=1, FP=1, TN=1, U_B=1)
    assert report["support"] == dict(attack=3, benign=3, total=6, accepted=4)
    expected = {"coverage": 2/3, "abstention_rate": 1/3, "retained_error": 1/2,
                "full_attack_detection": 1/3, "retained_attack_recall": 1/2,
                "unresolved_missed_attack_rate": 2/3, "attack_coverage": 2/3,
                "benign_coverage": 2/3, "attack_abstention_rate": 1/3,
                "benign_abstention_rate": 1/3, "full_benign_false_positive_rate": 1/3,
                "accepted_benign_false_positive_rate": 1/2, "attack_precision": 1/2,
                "equal_class_utility": 1/3, "attack_minus_benign_abstention_rate": 0}
    for name, value in expected.items():
        assert report["metrics"][name]["value"] == pytest.approx(value)
        assert report["metrics"][name]["na_reason"] is None
    assert report["metrics"]["full_attack_detection"]["denominator"] == 3
    assert report["metrics"]["retained_attack_recall"]["denominator"] == 2


def test_abstaining_on_missed_attacks_does_not_improve_detection_or_utility():
    before = summarize_outcomes([1, 1, 0], ["ATTACK", "BENIGN", "BENIGN"])
    after = summarize_outcomes([1, 1, 0], ["ATTACK", "ABSTAIN", "BENIGN"])
    for name in ("full_attack_detection", "equal_class_utility", "unresolved_missed_attack_rate"):
        assert before["metrics"][name] == after["metrics"][name]
    assert after["metrics"]["retained_error"]["value"] == 0
    assert after["metrics"]["retained_attack_recall"]["value"] == 1
    assert after["metrics"]["coverage"]["value"] < before["metrics"]["coverage"]["value"]


def test_all_abstentions_preserve_support_and_are_not_success():
    report = summarize_outcomes([1, 0], ["ABSTAIN", "ABSTAIN"])
    assert report["support"]["total"] == 2
    for name in ("coverage", "full_attack_detection", "equal_class_utility"):
        assert report["metrics"][name]["value"] == 0
    assert report["metrics"]["unresolved_missed_attack_rate"]["value"] == 1
    assert report["metrics"]["retained_error"]["value"] is None
    assert report["metrics"]["retained_error"]["na_reason"] == "NO_ACCEPTED_UNITS"


def test_empty_and_one_class_inputs_have_explicit_na_reasons():
    empty = summarize_outcomes([], [])
    assert empty["support"]["total"] == 0
    assert all(m["value"] is None and m["na_reason"] for m in empty["metrics"].values())
    benign = summarize_outcomes([0], ["BENIGN"])
    assert benign["metrics"]["full_attack_detection"]["na_reason"] == "NO_ATTACKS"
    assert benign["metrics"]["attack_precision"]["na_reason"] == "NO_PREDICTED_ATTACKS"
    attack = summarize_outcomes([1], ["ATTACK"])
    assert attack["metrics"]["full_benign_false_positive_rate"]["na_reason"] == "NO_BENIGN"
    assert attack["metrics"]["equal_class_utility"]["value"] is None


@pytest.mark.parametrize("truth,outcomes", [([1], []), ([True], ["ATTACK"]),
    ([1.0], ["ATTACK"]), ([2], ["ATTACK"]), (["1"], ["ATTACK"]),
    ([1], [None]), ([1], ["attack"]), ([0], [0])])
def test_invalid_or_silently_missing_units_fail(truth, outcomes):
    with pytest.raises(ValueError):
        summarize_outcomes(truth, outcomes)


def test_inputs_are_preserved_and_order_does_not_change_counts():
    truth, outcomes = [1, 0, 1], ["ABSTAIN", "BENIGN", "ATTACK"]
    report = summarize_outcomes(truth, outcomes)
    assert report == summarize_outcomes(list(reversed(truth)), list(reversed(outcomes)))
    assert truth == [1, 0, 1] and outcomes == ["ABSTAIN", "BENIGN", "ATTACK"]
