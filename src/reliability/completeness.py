"""AP-1 completeness from explicit pre-imputation observed-valid masks.

Internal pure utility, not an agreed producer API. Callers establish mask
validity, causal availability and grid provenance; this helper cannot verify
those properties. It selects no KPIs/cutoffs and makes no prediction.
"""

from collections.abc import Mapping, Sequence


def _ids(values: Sequence[str], name: str) -> list[str]:
    if isinstance(values, (str, bytes)):
        raise ValueError(f"{name} must be a sequence of distinct nonempty strings")
    items = list(values)
    if not items or any(not isinstance(v, str) or not v for v in items) or len(set(items)) != len(items):
        raise ValueError(f"{name} must be distinct nonempty strings")
    return items


def summarize_completeness(
    expected_positions: Sequence[str] | None,
    required_kpis: Sequence[str],
    masks: Mapping[str, Mapping[str, bool | None] | None] | None,
) -> dict:
    """Return minimum required-KPI completeness, or unknown quality.

    True means observed and valid; False means known missing/invalid. None,
    absent position keys or unavailable masks mean unknown metadata. Masks
    must refer to distinct expected positions, never imputed/padded values.
    Optional KPI masks do not affect the result. Empty/duplicate configuration
    and out-of-grid required-mask entries fail rather than inflate counts.
    A tail's expected_positions must describe its actual planned length.
    """
    required = _ids(required_kpis, "required_kpis")
    if masks is not None and not isinstance(masks, Mapping):
        raise ValueError("masks must be a mapping or unavailable (None)")
    if expected_positions is None:
        return {"quality": None, "reason": "QUALITY_UNAVAILABLE",
                "expected_report_count": None, "per_kpi": {}}
    positions = _ids(expected_positions, "expected_positions")
    expected = set(positions)
    per_kpi = {}
    for kpi in sorted(required):
        mask = masks.get(kpi) if masks is not None else None
        if mask is not None:
            if not isinstance(mask, Mapping):
                raise ValueError("Each required KPI mask must be a mapping or None")
            if set(mask) - expected:
                raise ValueError("Required KPI mask contains out-of-grid positions")
        observed = missing = unknown = 0
        for position in positions:
            value = mask.get(position) if mask is not None else None
            if value is True:
                observed += 1
            elif value is False:
                missing += 1
            elif value is None:
                unknown += 1
            else:
                raise ValueError("Mask values must be explicit bool or unknown (None)")
        per_kpi[kpi] = {"observed_valid_count": observed,
                        "known_missing_or_invalid_count": missing,
                        "unknown_count": unknown,
                        "fraction": observed / len(positions) if unknown == 0 else None}
    unavailable = any(v["unknown_count"] for v in per_kpi.values())
    return {"quality": None if unavailable else min(v["fraction"] for v in per_kpi.values()),
            "reason": "QUALITY_UNAVAILABLE" if unavailable else None,
            "expected_report_count": len(positions), "per_kpi": per_kpi}
