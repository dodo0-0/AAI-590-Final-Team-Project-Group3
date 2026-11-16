"""EP-6 binary outcome accounting; no score, threshold or quality-policy fitting.

This pure helper is independent of the pending teammate data contracts. Callers
must supply every planned labeled unit, including explicit ABSTAIN outcomes.
It cannot establish completeness of an external prediction file on its own.
"""

from collections.abc import Sequence


OUTCOMES = frozenset({"BENIGN", "ATTACK", "ABSTAIN"})


def _ratio(numerator: int, denominator: int, reason: str) -> dict:
    return {"value": numerator / denominator if denominator else None,
            "numerator": numerator, "denominator": denominator,
            "na_reason": None if denominator else reason}


def summarize_outcomes(truth: Sequence[int], outcomes: Sequence[str]) -> dict:
    """Count 0=Benign/1=attack truth against three explicit final outcomes.

    No rows are dropped or inferred. Empty/one-class inputs produce counts and
    explicit undefined ratios. Unknown labels/outcomes and unequal lengths fail.
    Returned values are unrounded fractions; None denotes an undefined metric.
    These metrics do not implement AP/ROC, aggregation or threshold selection.
    """
    if len(truth) != len(outcomes):
        raise ValueError("Truth and outcome lengths differ; do not drop planned units")
    counts = dict.fromkeys(("TP", "FN", "U_A", "FP", "TN", "U_B"), 0)
    cells = {1: {"ATTACK": "TP", "BENIGN": "FN", "ABSTAIN": "U_A"},
             0: {"ATTACK": "FP", "BENIGN": "TN", "ABSTAIN": "U_B"}}
    for label, outcome in zip(truth, outcomes):
        if type(label) is not int or label not in (0, 1):
            raise ValueError("Truth must contain integer binary labels 0 or 1")
        if not isinstance(outcome, str) or outcome not in OUTCOMES:
            raise ValueError("Outcome must be BENIGN, ATTACK or explicit ABSTAIN")
        counts[cells[label][outcome]] += 1
    tp, fn, ua, fp, tn, ub = (counts[k] for k in ("TP", "FN", "U_A", "FP", "TN", "U_B"))
    na, nb = tp + fn + ua, fp + tn + ub
    total, accepted = na + nb, tp + fn + fp + tn
    metrics = {
        "coverage": _ratio(accepted, total, "NO_UNITS"),
        "abstention_rate": _ratio(ua + ub, total, "NO_UNITS"),
        "attack_coverage": _ratio(tp + fn, na, "NO_ATTACKS"),
        "benign_coverage": _ratio(tn + fp, nb, "NO_BENIGN"),
        "retained_error": _ratio(fp + fn, accepted, "NO_ACCEPTED_UNITS"),
        "retained_attack_recall": _ratio(tp, tp + fn, "NO_ACCEPTED_ATTACKS"),
        "full_attack_detection": _ratio(tp, na, "NO_ATTACKS"),
        "unresolved_missed_attack_rate": _ratio(fn + ua, na, "NO_ATTACKS"),
        "attack_abstention_rate": _ratio(ua, na, "NO_ATTACKS"),
        "benign_abstention_rate": _ratio(ub, nb, "NO_BENIGN"),
        "full_benign_false_positive_rate": _ratio(fp, nb, "NO_BENIGN"),
        "accepted_benign_false_positive_rate": _ratio(fp, fp + tn, "NO_ACCEPTED_BENIGN"),
        "attack_precision": _ratio(tp, tp + fp, "NO_PREDICTED_ATTACKS"),
    }
    # Equal-class utility includes all labeled units in its class denominators.
    # This reports a fixed set of outcomes; it does not select a threshold.
    metrics["equal_class_utility"] = {
        "value": 0.5 * (tp / na + tn / nb) if na and nb else None,
        "na_reason": None if na and nb else "BOTH_CLASSES_REQUIRED"}
    metrics["attack_minus_benign_abstention_rate"] = {
        "value": ua / na - ub / nb if na and nb else None,
        "na_reason": None if na and nb else "BOTH_CLASSES_REQUIRED"}
    return {"counts": counts, "support": {"attack": na, "benign": nb,
                                             "total": total, "accepted": accepted},
            "metrics": metrics}
