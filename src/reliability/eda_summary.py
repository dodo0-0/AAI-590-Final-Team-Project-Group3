"""Read-only descriptive follow-up; no cleaning, feature selection or models."""

import argparse
from collections import Counter, defaultdict
from contextlib import closing
import json
import math
from pathlib import Path
import sqlite3
from statistics import fmean, median, stdev

from reliability.data_audit import sha256
from reliability.reconciliation import RADIO_FIELDS

METRIC_FIELDS = (*RADIO_FIELDS, "pmi")


def describe(values):
    """Finite numeric summary; linear quantiles at (n-1)*p, sample SD."""
    values = list(values)
    finite = sorted(v for v in values if type(v) in (int, float) and math.isfinite(v))
    missing = sum(v is None for v in values)
    result = {"rows": len(values), "finite": len(finite), "missing": missing,
              "invalid_nonmissing": len(values)-missing-len(finite),
              "missing_pct": 100*missing/len(values) if values else None}
    def quantile(p):
        if not finite:
            return None
        index = (len(finite)-1)*p
        lo, hi = math.floor(index), math.ceil(index)
        return finite[lo] + (finite[hi]-finite[lo])*(index-lo)
    result.update(mean=fmean(finite) if finite else None,
                  std_sample=stdev(finite) if len(finite)>1 else None,
                  min=finite[0] if finite else None, p05=quantile(.05),
                  q25=quantile(.25), median=median(finite) if finite else None,
                  q75=quantile(.75), p95=quantile(.95), max=finite[-1] if finite else None)
    result["iqr"] = result["q75"]-result["q25"] if finite else None
    return result


def correlation(pairs):
    """Pearson on finite paired values with explicit undefined reasons."""
    pairs = list(pairs)
    valid = [(x,y) for x,y in pairs if all(type(v) in (int,float) and math.isfinite(v) for v in (x,y))]
    if len(valid)<2:
        return {"paired": len(valid), "excluded": len(pairs)-len(valid), "r": None, "reason": "TOO_FEW_PAIRS"}
    mx, my = fmean(x for x,y in valid), fmean(y for x,y in valid)
    xx = math.fsum((x-mx)**2 for x,y in valid)
    yy = math.fsum((y-my)**2 for x,y in valid)
    r = math.fsum((x-mx)*(y-my) for x,y in valid)/math.sqrt(xx*yy) if xx and yy else None
    return {"paired":len(valid), "excluded":len(pairs)-len(valid),
            "r":max(-1.,min(1.,r)) if r is not None else None,
            "reason":None if r is not None else "CONSTANT_INPUT"}


def summarize(records):
    groups = defaultdict(list)
    for row in records:
        groups[row["attack_category"]].append(row)
    def metrics(rows):
        return {field:describe(r[field] for r in rows) for field in METRIC_FIELDS}
    return {"rows":len(records), "category_counts":dict(sorted(Counter(r["attack_category"] for r in records).items())),
            "metrics":metrics(records),
            "metrics_by_category":{label:metrics(rows) for label,rows in sorted(groups.items())},
            "bler":correlation((r["dlBler"],r["ulBler"]) for r in records),
            "bler_by_category":{label:correlation((r["dlBler"],r["ulBler"]) for r in rows) for label,rows in sorted(groups.items())}}


def build_summary(root, cohort_path, window_path, split_path, timing_path):
    root = Path(root).resolve()
    paths = [Path(p) for p in (cohort_path,window_path,split_path,timing_path)]
    hashes = [sha256(p) for p in paths]
    cohort,windows,splits,timing = [json.loads(p.read_text(encoding="utf-8")) for p in paths]
    if windows["cohort_manifest_sha256"]!=hashes[0] or splits["cohort_manifest_sha256"]!=hashes[0] or splits["window_manifest_sha256"]!=hashes[1]:
        raise ValueError("Parent manifest identities disagree")
    if timing["input_files"]!=cohort["input_files"]:
        raise ValueError("Timing/cohort input snapshots disagree")
    def verify_inputs():
        for item in cohort["input_files"]:
            p = (root/item["path"]).resolve()
            if not p.is_relative_to(root) or p.stat().st_size!=item["bytes"] or sha256(p)!=item["sha256"]:
                raise ValueError("Input snapshot mismatch")
    verify_inputs()
    with closing(sqlite3.connect((root/"Lower_Layer_Data.db").as_uri()+"?mode=ro",uri=True)) as db:
        db.row_factory = sqlite3.Row
        records = [dict(r) for r in db.execute('SELECT rowid AS database_rowid, * FROM lower_layer_data ORDER BY rowid')]
    refs = {r["database_rowid"]:r for r in cohort["rows"]}
    assignments = {r["database_rowid"]:r for r in splits["row_assignments"]}
    if len(refs)!=len(cohort["rows"]) or len(assignments)!=len(splits["row_assignments"]) or set(refs)!=set(assignments) or set(refs)!={r["database_rowid"] for r in records}:
        raise ValueError("Incomplete or duplicate row references")
    for row in records:
        ref, assignment = refs[row["database_rowid"]], assignments[row["database_rowid"]]
        if row["attack_category"]!=ref["attack_category"] or ref["provisional_group_id"]!=assignment["provisional_group_id"]:
            raise ValueError("Label/group mismatch")
    primary = [r for r in records if refs[r["database_rowid"]]["cohort"]=="primary_temporal"]
    secondary = [r for r in records if refs[r["database_rowid"]]["cohort"]=="secondary_non_temporal_only"]
    if len(primary)+len(secondary)!=len(records):
        raise ValueError("Unknown cohort")
    training = [r for r in primary if assignments[r["database_rowid"]]["partition"]=="train"]
    by_source = defaultdict(list)
    for row in primary:
        by_source[refs[row["database_rowid"]]["source_path"]].append(row)
    streams = [s for s in timing["streams"] if s["path"] in by_source]
    if sum(s["records"] for s in streams)!=len(primary):
        raise ValueError("Timing stream coverage differs from primary cohort")
    delta_counts = Counter()
    for stream in streams:
        delta_counts.update({h["delta"]:h["count"] for h in stream["delta_histogram_raw"]})
    result = {"interpretation":"Descriptive audit only; no feature-selection rule, vendor profile, clock conversion or fitting.",
              "parent_sha256":{p.name:h for p,h in zip(paths,hashes)},
              "cohorts":{name:summarize(rows) for name,rows in [("full_database",records),("primary",primary),("secondary_non_temporal",secondary),("primary_training",training)]},
              "primary_bler_by_source":{path:correlation((r["dlBler"],r["ulBler"]) for r in rows) for path,rows in sorted(by_source.items())},
              "primary_timing":{"streams":len(streams),"records":len(primary),
                 "negative_steps":sum(s["negative_steps"] for s in streams),
                 "zero_steps":sum(s["zero_steps"] for s in streams),
                 "positive_step_medians_raw":describe(s["positive_step_median_raw"] for s in streams),
                 "largest_step_raw":max((s["positive_step_max_raw"] for s in streams if s["positive_step_max_raw"] is not None),default=None),
                 "delta_histogram_raw":[{"delta":k,"count":v} for k,v in sorted(delta_counts.items())],
                 "complete_window_span_raw":describe(w["raw_span"] for w in windows["windows"] if not w["is_partial"]),
                 "partial_window_span_raw":describe(w["raw_span"] for w in windows["windows"] if w["is_partial"])}}
    verify_inputs()
    if [sha256(p) for p in paths]!=hashes:
        raise ValueError("Parent artifacts changed")
    result["input_hashes_unchanged"] = True
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root",type=Path,default=Path("data/radio"))
    parser.add_argument("--output",type=Path,required=True)
    args=parser.parse_args()
    if args.output.exists() or args.output.resolve().is_relative_to(args.root.resolve()):
        parser.error("Choose a new output outside input directory")
    result=build_summary(args.root,*[Path("results")/name for name in [
        "cohort_group_manifest_ep1_ep2_2026-11-15.json","window_manifest_ep1_ep4_2026-11-15.json",
        "split_manifest_ep1_ep5_2026-11-15.json","timing_audit_2026-11-15.json"]])
    args.output.parent.mkdir(parents=True,exist_ok=True)
    with args.output.open("x",encoding="utf-8",newline="\n") as f:
        json.dump(result,f,indent=2,sort_keys=True,allow_nan=False);f.write("\n")
    print("Saved",args.output)
