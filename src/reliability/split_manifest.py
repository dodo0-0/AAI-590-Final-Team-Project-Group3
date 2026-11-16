"""EP-5 label-support partitions of provisional groups; never selects by scores."""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import json
from pathlib import Path
import random

try:
    from .data_audit import sha256
except ImportError:
    from data_audit import sha256


SEED = 42
CV_FOLDS = 3
PARTITIONS = ("train", "validation", "test")
FRACTIONS = (0.6, 0.2, 0.2)
CATEGORIES = {"Benign", "BruteForce", "DDoS", "DoS", "Probe", "Web Attacks"}


def apportion(total: int, minimum: int = 1) -> list[int]:
    """Fixed-size greedy least-squares apportionment; ties train/val/test."""
    if total < minimum * 3:
        raise ValueError("Insufficient groups for required partition support")
    counts = [minimum] * 3
    ideals = [total * f for f in FRACTIONS]
    while sum(counts) < total:
        index = min(range(3), key=lambda i: (2*counts[i] + 1 - 2*ideals[i], i))
        counts[index] += 1
    return counts


def _allocate_families(families: dict[str, list], targets: list[int]) -> dict[str, list[int]]:
    """Keep each family in train; support all three partitions when >=3 groups."""
    allocations = {name: ([1, 1, 1] if len(groups) >= 3 else [1, 0, 0])
                   for name, groups in sorted(families.items())}
    used = [sum(a[i] for a in allocations.values()) for i in range(3)]
    if any(used[i] > targets[i] for i in range(3)):
        raise ValueError("Family-support constraints exceed partition capacity")
    while used != targets:
        choices = []
        for name, groups in sorted(families.items()):
            current = allocations[name]
            if sum(current) >= len(groups):
                continue
            for i in range(3):
                if used[i] < targets[i]:
                    cost = 2*current[i] + 1 - 2*len(groups)*FRACTIONS[i]
                    choices.append((cost, name, i))
        if not choices:
            raise ValueError("No feasible family-support allocation")
        _, name, i = min(choices)
        allocations[name][i] += 1
        used[i] += 1
    return allocations


def assemble_splits(cohort: dict, windows: dict) -> dict:
    rows = cohort["rows"]
    row_by_id = {r["database_rowid"]: r for r in rows}
    if len(row_by_id) != len(rows):
        raise ValueError("Duplicate database row references")
    grouped = defaultdict(list)
    for row in rows:
        if row["attack_category"] not in CATEGORIES or row["traffic_type"] != (0 if row["attack_category"] == "Benign" else 1):
            raise ValueError("Archive category/binary flag is inconsistent or unknown")
        if row["cohort"] not in ("primary_temporal", "secondary_non_temporal_only"):
            raise ValueError("Unknown cohort membership")
        grouped[row["provisional_group_id"]].append(row)
    metadata = {}
    file_groups = defaultdict(set)
    for group, records in sorted(grouped.items()):
        categories = {r["attack_category"] for r in records}
        if len(categories) != 1:
            raise ValueError("Mixed-category group requires stratification review; do not break the group")
        metadata[group] = {"category": next(iter(categories)),
                           "primary_present": any(r["cohort"] == "primary_temporal" for r in records),
                           "source_files": sorted({r["source_path"] for r in records})}
        for path in metadata[group]["source_files"]:
            file_groups[path].add(group)
    if any(len(groups) != 1 for groups in file_groups.values()):
        raise ValueError("A source file spans more than one group")
    primary = [g for g in sorted(metadata) if metadata[g]["primary_present"]]
    benign = [g for g in primary if metadata[g]["category"] == "Benign"]
    attack = [g for g in primary if metadata[g]["category"] != "Benign"]
    totals = apportion(len(primary))
    benign_targets = apportion(len(benign))
    attack_targets = [totals[i] - benign_targets[i] for i in range(3)]
    if min(benign_targets) < 1 or min(attack_targets) < 1:
        raise ValueError("A partition lacks one binary class")
    families = defaultdict(list)
    for group in attack:
        families[metadata[group]["category"]].append(group)
    allocations = _allocate_families(families, attack_targets)
    allocations["Benign"] = benign_targets
    families["Benign"] = benign
    rng = random.Random(SEED)
    assignments = {}
    for category, groups in sorted(families.items()):
        shuffled = sorted(groups)
        rng.shuffle(shuffled)
        offset = 0
        for i, partition in enumerate(PARTITIONS):
            for group in shuffled[offset:offset + allocations[category][i]]:
                assignments[group] = partition
            offset += allocations[category][i]
    secondary_only = [g for g in sorted(metadata) if not metadata[g]["primary_present"]]
    if secondary_only:
        # Preserve a secondary condition in each partition rather than rounding
        # three secondary groups into train/val only; does not move primary groups.
        allocation = apportion(len(secondary_only))
        rng.shuffle(secondary_only)
        offset = 0
        for partition, n in zip(PARTITIONS, allocation):
            for group in secondary_only[offset:offset+n]:
                assignments[group] = partition
            offset += n
    if set(assignments) != set(metadata):
        raise ValueError("Group assignment is incomplete")

    cv_assignment = {}
    cv_rng = random.Random(SEED)
    for role in ("Benign", "attack"):
        training = [g for g in sorted(metadata) if assignments[g] == "train" and metadata[g]["primary_present"]
                    and (metadata[g]["category"] == "Benign") == (role == "Benign")]
        if len(training) < CV_FOLDS:
            raise ValueError("Training groups cannot support three binary-stratified CV folds")
        cv_rng.shuffle(training)
        for i, group in enumerate(training):
            cv_assignment[group] = i % CV_FOLDS
    for group in secondary_only:
        if assignments[group] == "train":
            # Balance training fold counts without changing primary fold IDs.
            fold = min(range(CV_FOLDS), key=lambda f: (sum(v == f for v in cv_assignment.values()), f))
            cv_assignment[group] = fold

    def support(groups: list[str], primary_only: bool = False) -> dict:
        selected = [g for g in groups if not primary_only or metadata[g]["primary_present"]]
        return dict(sorted(Counter(metadata[g]["category"] for g in selected).items()))

    partitions = {}
    for name in PARTITIONS:
        groups = sorted(g for g, value in assignments.items() if value == name)
        partitions[name] = {"group_ids": groups, "primary_category_group_counts": support(groups, True),
                            "full_category_group_counts": support(groups)}
    folds = []
    training_groups = set(partitions["train"]["group_ids"])
    for fold in range(CV_FOLDS):
        heldout = sorted(g for g in training_groups if cv_assignment[g] == fold)
        fitting = sorted(training_groups - set(heldout))
        for subset in (heldout, fitting):
            counts = support(subset, True)
            if not counts.get("Benign") or not sum(n for category, n in counts.items() if category != "Benign"):
                raise ValueError("CV fitting/held-out subset lacks one binary class")
        folds.append({"fold": fold, "fit_group_ids": fitting, "heldout_group_ids": heldout,
                      "primary_fit_category_counts": support(fitting, True),
                      "primary_heldout_category_counts": support(heldout, True)})

    row_assignments = [{"database_rowid": r["database_rowid"], "cohort": r["cohort"],
                        "provisional_group_id": r["provisional_group_id"],
                        "partition": assignments[r["provisional_group_id"]],
                        "training_cv_heldout_fold": cv_assignment.get(r["provisional_group_id"])}
                       for r in sorted(rows, key=lambda r: r["database_rowid"])]
    window_assignments = []
    seen_windows, seen_rows = set(), set()
    for w in windows["windows"]:
        if w["window_id"] in seen_windows or w["provisional_group_id"] not in assignments:
            raise ValueError("Duplicate window or unknown group")
        seen_windows.add(w["window_id"])
        for ref in w["report_references"]:
            row = row_by_id.get(ref["database_rowid"])
            if row is None or row["cohort"] != "primary_temporal" or row["provisional_group_id"] != w["provisional_group_id"]:
                raise ValueError("Window reference disagrees with its primary group")
            if row["database_rowid"] in seen_rows:
                raise ValueError("Primary report appears in multiple windows")
            seen_rows.add(row["database_rowid"])
        group = w["provisional_group_id"]
        window_assignments.append({"window_id": w["window_id"], "provisional_group_id": group,
                                   "partition": assignments[group], "training_cv_heldout_fold": cv_assignment.get(group),
                                   "is_partial": w["is_partial"]})
    if seen_rows != {r["database_rowid"] for r in rows if r["cohort"] == "primary_temporal"}:
        raise ValueError("Window references do not cover the complete primary cohort")
    return {"format_version": 1, "policy_reference": "EP-5; D016", "seed": SEED, "training_cv_folds": CV_FOLDS,
            "algorithm": "Sorted group IDs and categories; random.Random(42) permutations; constrained integer least-squares allocations. Primary partitions/folds fixed before secondary-only assignment. No model scores.",
            "target_group_fractions": dict(zip(PARTITIONS, FRACTIONS)),
            "independence_status": "provisional source-file benchmark; capture independence unverified",
            "group_assignments": [{"group_id": g, **metadata[g], "partition": assignments[g],
                                   "training_cv_heldout_fold": cv_assignment.get(g)} for g in sorted(metadata)],
            "partitions": partitions, "cv_folds": folds, "row_assignments": row_assignments,
            "window_assignments": sorted(window_assignments, key=lambda w: w["window_id"])}


def build_splits(root: Path, cohort_path: Path, window_path: Path) -> dict:
    root = root.resolve()
    hashes = (sha256(cohort_path), sha256(window_path))
    cohort = json.loads(cohort_path.read_text(encoding="utf-8"))
    windows = json.loads(window_path.read_text(encoding="utf-8"))
    if windows["cohort_manifest_sha256"] != hashes[0]:
        raise ValueError("Window/cohort manifest identities disagree")
    for item in cohort["input_files"]:
        path = (root / item["path"]).resolve()
        if not path.is_relative_to(root) or not path.is_file() or path.stat().st_size != item["bytes"] or sha256(path) != item["sha256"]:
            raise ValueError("Input snapshot mismatch")
    result = assemble_splits(cohort, windows)
    if hashes != (sha256(cohort_path), sha256(window_path)):
        raise ValueError("Parent manifest changed during split construction")
    result.update(cohort_manifest_sha256=hashes[0], window_manifest_sha256=hashes[1],
                  input_files=cohort["input_files"], input_snapshot_verified=True)
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--cohort-manifest", type=Path, required=True)
    parser.add_argument("--window-manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.resolve().is_relative_to(args.root.resolve()) or args.output.exists():
        parser.error("Choose a new output path outside the input directory")
    result = build_splits(args.root, args.cohort_manifest, args.window_manifest)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x", encoding="utf-8", newline="\n") as output:
        json.dump(result, output, indent=2, sort_keys=True, allow_nan=False)
        output.write("\n")
    print("Saved", args.output)
    for name, partition in result["partitions"].items():
        print(name, "groups:", len(partition["group_ids"]), "primary support:", partition["primary_category_group_counts"])


if __name__ == "__main__":
    main()
