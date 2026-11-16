"""Summarize database clocks projected onto radio-candidate source order."""

from collections import Counter, defaultdict

from .reconciliation import comparison_key
from .timing_audit import COINCIDENCE_FIELDS, describe_sequence


def summarize_projected_clocks(cases: list[dict]) -> dict:
    """These clocks are not observed source clocks and cannot authenticate time.

    Use source line order only as a diagnostic. Reject duplicate source/row
    references rather than silently deduplicate or choose a preferred match.
    """
    source_refs = [(c["source_path"], c["source_line"]) for c in cases]
    database_refs = [c["database_rowid"] for c in cases]
    if len(set(source_refs)) != len(source_refs) or len(set(database_refs)) != len(database_refs):
        raise ValueError("Expected unique source occurrence and database row references")
    grouped = defaultdict(list)
    all_keys = []
    files = []
    for case in cases:
        grouped[case["source_path"]].append(case)
    for path, rows in sorted(grouped.items()):
        rows.sort(key=lambda c: c["source_line"])
        keys = []
        unusable = []
        for case in rows:
            key = comparison_key(case["database_compared_metadata"], COINCIDENCE_FIELDS)
            if isinstance(key, dict):
                unusable.append({"source_line": case["source_line"], "database_rowid": case["database_rowid"], **key})
            else:
                keys.append(key)
        all_keys.extend(keys)
        sequence = [{"line": c["source_line"],
                     "timestamp": c["database_compared_metadata"].get("timestamp")} for c in rows]
        files.append({"path": path, "cases": len(rows),
                      "distinct_usable_metadata_tuples": len(set(keys)),
                      "repeated_tuple_excess": len(keys) - len(set(keys)),
                      "unusable_metadata_keys": unusable,
                      "projected_database_clock_in_source_line_order": describe_sequence(sequence)})
    counts = Counter(all_keys)
    return {"interpretation": "Database clock projection onto candidate source line order; not measured source event time or proof of a metadata assignment algorithm.",
            "cases": len(cases), "usable_metadata_tuples": len(all_keys),
            "distinct_usable_metadata_tuples": len(counts),
            "repeated_tuple_excess": len(all_keys) - len(counts),
            "tuple_multiplicity_histogram": [{"multiplicity": m, "distinct_tuples": n}
                                             for m, n in sorted(Counter(counts.values()).items())],
            "files": files}
