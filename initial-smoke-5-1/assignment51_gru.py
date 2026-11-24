"""Assignment 5.1 educational GRU smoke test; not a vendor-restriction study.

Reuses the audited cohorts, windows and split validation. Fits preprocessing
and weights on primary OUTER TRAINING reports only. No validation/test scores,
thresholds, calibration or final-model claim are produced.
"""

import argparse
from collections import Counter
from contextlib import closing
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import platform
import random
import sqlite3
import sys
import time

import torch
from torch import nn
from torch.nn.utils.rnn import pack_padded_sequence
from torch.utils.data import DataLoader, TensorDataset

from reliability.data_audit import sha256
from reliability.split_manifest import build_splits

# Explicit assignment-only numeric inputs. Exclude IDs, labels, timestamps,
# constants/ambiguous PMI and byte counters whose semantics remain unresolved.
# This is not an approved vendor profile, minimum KPI set or final model.
FEATURES = ("dlMcs", "dlBler", "ulMcs", "ulBler", "phr", "pcmax", "rsrq",
            "sinr", "rsrp", "rssi", "cqi", "pucchSnr", "puschSnr")
MAX_REPORTS = 10
PARENTS = ("cohort_group_manifest_ep1_ep2_2026-11-15.json",
           "window_manifest_ep1_ep4_2026-11-15.json",
           "split_manifest_ep1_ep5_2026-11-15.json")


class GRUBinaryClassifier(nn.Module):
    """Randomly initialized, unidirectional GRU -> one raw attack logit.

    Packing prevents padded positions from affecting the final hidden state.
    Each forward starts with the default zero hidden state; no state is carried
    across windows, files or partitions. Dropout defaults to zero for one layer.
    """
    def __init__(self, input_size=len(FEATURES), hidden_size=32, layers=1, dropout=0.0):
        super().__init__()
        self.gru = nn.GRU(input_size, hidden_size, num_layers=layers,
                          dropout=dropout if layers>1 else 0.0,
                          batch_first=True, bidirectional=False)
        self.dropout = nn.Dropout(dropout)
        self.output = nn.Linear(hidden_size, 1)

    def forward(self, x, lengths):
        if lengths.ndim!=1 or len(lengths)!=len(x) or torch.any(lengths<1) or torch.any(lengths>x.shape[1]):
            raise ValueError("Invalid sequence lengths")
        packed = pack_padded_sequence(x, lengths.cpu(), batch_first=True, enforce_sorted=False)
        _, hidden = self.gru(packed)
        return self.output(self.dropout(hidden[-1])).squeeze(-1)


def encode_training_windows(rows, windows, refs):
    """Check boundaries/order/labels, fit train-only scaler, retain short tails.

    Only referenced training reports enter mean/population-SD estimates.
    Nonfinite input fails instead of inventing an imputation/validity policy.
    """
    seen, ordered_ids, sequences, labels = set(), [], [], []
    seen_windows = set()
    for window in windows:
        if window["window_id"] in seen_windows:
            raise ValueError("Duplicate window")
        seen_windows.add(window["window_id"])
        reports = window["report_references"]
        if not 1<=len(reports)<=MAX_REPORTS or len(reports)!=window["expected_report_count"]:
            raise ValueError("Invalid expected window length")
        ids, lines, clocks = [], [], []
        truth = 0 if window["attack_category"]=="Benign" else 1
        if window["traffic_type"]!=truth:
            raise ValueError("Window binary label mismatch")
        for reference in reports:
            rowid = reference["database_rowid"]
            if rowid in seen:
                raise ValueError("Report duplicated across training windows")
            row, ref = rows[rowid], refs[rowid]
            if (ref["cohort"]!="primary_temporal" or ref["source_path"]!=window["source_path"]
                    or ref["provisional_group_id"]!=window["provisional_group_id"]
                    or ref["source_line"]!=reference["source_line"]):
                raise ValueError("Source/cohort/group boundary mismatch")
            if row["attack_category"]!=window["attack_category"] or row["traffic_type"]!=truth:
                raise ValueError("Mixed or contradictory labels")
            if any(row[field]!=value for field,value in window["identity"].items()):
                raise ValueError("UE/cell/RNTI boundary mismatch")
            clock = row["timestamp"]
            if type(clock) not in (int,float) or not math.isfinite(clock):
                raise ValueError("Unsupported clock")
            if any(type(row[f]) not in (int,float) or not math.isfinite(row[f]) for f in FEATURES):
                raise ValueError("Missing/nonfinite features; no implicit imputation")
            seen.add(rowid); ordered_ids.append(rowid); ids.append(rowid)
            lines.append(reference["source_line"]); clocks.append(clock)
        if any(a>=b for a,b in zip(lines,lines[1:])) or any(a>=b for a,b in zip(clocks,clocks[1:])):
            raise ValueError("Non-increasing source order or raw clocks")
        if clocks[0]!=window["raw_timestamp_first"] or clocks[-1]!=window["raw_timestamp_last"]:
            raise ValueError("Window clock endpoints disagree")
        sequences.append(ids); labels.append(truth)
    if not ordered_ids:
        raise ValueError("No primary training windows")
    if set(labels)!={0,1}:
        raise ValueError("Training smoke test requires both binary classes")
    values = torch.tensor([[rows[i][f] for f in FEATURES] for i in ordered_ids],dtype=torch.float64)
    mean = values.mean(dim=0)
    std = values.std(dim=0,correction=0)
    constant = std==0
    scale = torch.where(constant,torch.ones_like(std),std)
    transformed = ((values-mean)/scale).float()
    by_id = {rowid:transformed[i] for i,rowid in enumerate(ordered_ids)}
    x = torch.zeros(len(sequences),MAX_REPORTS,len(FEATURES),dtype=torch.float32)
    lengths = torch.tensor([len(s) for s in sequences],dtype=torch.int64)
    for index,sequence in enumerate(sequences):
        x[index,:len(sequence)] = torch.stack([by_id[i] for i in sequence])
    scaler = {"features":list(FEATURES),"mean":mean.tolist(),"scale_population_std":scale.tolist(),
              "constant_training_features":[f for f,c in zip(FEATURES,constant.tolist()) if c],
              "fit_report_count":len(ordered_ids),"fit_partition":"primary outer train only"}
    return x,lengths,torch.tensor(labels,dtype=torch.float32),scaler,ordered_ids


def load_training_data(project):
    root = project/"data/radio"
    cp,wp,sp = [project/"results"/name for name in PARENTS]
    hashes = {p.name:sha256(p) for p in (cp,wp,sp)}
    # Existing tested split utility checks input hashes, row/window coverage,
    # group allocations and training-only CV. Do not create a new random split.
    expected = build_splits(root,cp,wp)
    splits = json.loads(sp.read_text(encoding="utf-8"))
    if splits!=expected:
        raise ValueError("Saved split differs from validated fixed policy")
    groups = [set(splits["partitions"][name]["group_ids"]) for name in ("train","validation","test")]
    if groups[0]&groups[1] or groups[0]&groups[2] or groups[1]&groups[2]:
        raise ValueError("Outer group leakage")
    cohort = json.loads(cp.read_text(encoding="utf-8"))
    window_manifest = json.loads(wp.read_text(encoding="utf-8"))
    assignment = {w["window_id"]:w for w in splits["window_assignments"]}
    windows = sorted((w for w in window_manifest["windows"] if assignment[w["window_id"]]["partition"]=="train"),key=lambda w:w["window_id"])
    refs = {r["database_rowid"]:r for r in cohort["rows"]}
    ids = sorted(r["database_rowid"] for w in windows for r in w["report_references"])
    if len(set(ids))!=len(ids):
        raise ValueError("Duplicate training references")
    rows = {}
    # Select ONLY training values. Held-out window features/scores never enter
    # preprocessing, training, hyperparameter choice or metrics in this run.
    fields = [*FEATURES,"timestamp","cellid","ue_id","rnti","traffic_type","attack_category"]
    with closing(sqlite3.connect((root/"Lower_Layer_Data.db").resolve().as_uri()+"?mode=ro",uri=True)) as db:
        db.row_factory = sqlite3.Row
        for start in range(0,len(ids),900):
            chunk = ids[start:start+900]
            query = 'SELECT rowid AS database_rowid,'+','.join('"'+f+'"' for f in fields)+' FROM lower_layer_data WHERE rowid IN ('+','.join('?' for _ in chunk)+')'
            rows.update((r["database_rowid"],dict(r)) for r in db.execute(query,chunk))
    if set(rows)!=set(ids):
        raise ValueError("Training rows missing")
    data = encode_training_windows(rows,windows,refs)
    audit = {"label_leakage_fields_excluded":True,"group_disjoint_outer_partitions":True,
             "raw_clocks_strictly_increasing_within_each_window":True,
             "source_and_UE_boundaries_checked":True,"capture_independence":"UNVERIFIED; SMOKE TEST ONLY",
             "validation_test_features_or_scores_used":False,
             "parent_sha256":hashes,"training_window_ids":[w["window_id"] for w in windows],
             "training_group_ids":sorted({w["provisional_group_id"] for w in windows}),
             "partial_training_windows":sum(w["is_partial"] for w in windows),
             "source_snapshot":cohort["input_files"]}
    if any(sha256(project/"results"/name)!=digest for name,digest in hashes.items()):
        raise ValueError("Parent changed during preparation")
    return data,audit


def parameter_hash(model):
    digest = hashlib.sha256()
    for name,p in model.state_dict().items():
        digest.update(name.encode())
        digest.update(bytes(p.detach().cpu().contiguous().view(torch.uint8).flatten().tolist()))
    return digest.hexdigest()


def run_smoke(project, output, epochs=1):
    project,output = Path(project).resolve(),Path(output).resolve()
    if epochs<1 or output.exists() or output.is_relative_to(project/"data"):
        raise ValueError("Positive epochs and a new output directory outside data required")
    random.seed(42);torch.manual_seed(42)
    torch.set_num_threads(1);torch.use_deterministic_algorithms(True)
    (x,lengths,y,scaler,report_ids),audit = load_training_data(project)
    model = GRUBinaryClassifier()
    optimizer = torch.optim.Adam(model.parameters(),lr=0.001)
    loss_fn = nn.BCEWithLogitsLoss()
    loader = DataLoader(TensorDataset(x,lengths,y),batch_size=64,shuffle=True,
                        generator=torch.Generator().manual_seed(42),num_workers=0,drop_last=False)
    config = {"features":list(FEATURES),"input_size":len(FEATURES),"max_reports":10,
              "hidden_size":32,"layers":1,"dropout":0.0,"bidirectional":False,
              "output":"one raw attack logit; no sigmoid before loss","loss":"BCEWithLogitsLoss, unweighted mean",
              "optimizer":"Adam","learning_rate":0.001,"batch_size":64,"epochs":epochs,
              "seed":42,"num_workers":0,"device":"cpu","cpu_threads":1,"deterministic_algorithms":True}
    initial = parameter_hash(model)
    history = []
    print("ASSIGNMENT 5.1 TRAINING SMOKE TEST ONLY; independent captures unverified",flush=True)
    for epoch in range(1,epochs+1):
        start=time.perf_counter();total=steps=0
        model.train()
        for features,lens,truth in loader:
            optimizer.zero_grad(set_to_none=True)
            loss = loss_fn(model(features,lens),truth)
            if not torch.isfinite(loss):raise ValueError("Nonfinite loss")
            loss.backward()
            if any(p.grad is not None and not torch.isfinite(p.grad).all() for p in model.parameters()):
                raise ValueError("Nonfinite gradients")
            optimizer.step();total+=loss.item()*len(truth);steps+=1
        record={"epoch":epoch,"training_loss":total/len(y),"optimizer_steps":steps,
                "windows_seen":len(y),"seconds":time.perf_counter()-start}
        history.append(record);print(json.dumps(record),flush=True)
    final = parameter_hash(model)
    if initial==final:raise ValueError("No weight update")
    # Verify all raw inputs again before committing completed-run evidence.
    for item in audit["source_snapshot"]:
        if sha256(project/"data/radio"/item["path"])!=item["sha256"]:
            raise ValueError("Raw input changed")
    for name,digest in audit["parent_sha256"].items():
        if sha256(project/"results"/name)!=digest:raise ValueError("Parent changed")
    output.mkdir(parents=True,exist_ok=False)
    checkpoint=output/"checkpoint_epoch_final.pt"
    torch.save({"model_state_dict":model.state_dict(),"optimizer_state_dict":optimizer.state_dict(),
                "config":config,"scaler":scaler,"epoch":epochs},checkpoint)
    restored=GRUBinaryClassifier();restored.load_state_dict(torch.load(checkpoint,map_location="cpu",weights_only=True)["model_state_dict"])
    if parameter_hash(restored)!=final:raise ValueError("Checkpoint reload mismatch")
    evidence={"experiment":"SMOKE TEST ONLY; no held-out or vendor-restriction result",
              "executed_at_utc":datetime.now(timezone.utc).isoformat(),"config":config,"history":history,
              "training_reports":len(report_ids),"training_windows":len(y),
              "window_class_counts":dict(Counter(int(v) for v in y.tolist())),
              "parameters":sum(p.numel() for p in model.parameters()),"scaler":scaler,"audit":audit,
              "initial_parameter_sha256":initial,"trained_parameter_sha256":final,
              "checkpoint":str(checkpoint.relative_to(project)) if checkpoint.is_relative_to(project) else str(checkpoint),
              "checkpoint_sha256":sha256(checkpoint),"checkpoint_reload_verified":True,
              "environment":{"python":sys.version,"interpreter":sys.executable,"torch":str(torch.__version__),
                 "platform":platform.platform(),"processor":platform.processor(),"machine":platform.machine(),
                 "cuda_available":torch.cuda.is_available(),"torch_cuda":torch.version.cuda,"torch_hip":torch.version.hip},
              "code_sha256":sha256(Path(__file__))}
    (output/"training_evidence.json").write_text(json.dumps(evidence,indent=2,sort_keys=True,allow_nan=False)+"\n",encoding="utf-8")
    (output/"training_log.jsonl").write_text(''.join(json.dumps(r,sort_keys=True)+"\n" for r in history),encoding="utf-8")
    print("Checkpoint:",checkpoint,flush=True)
    return evidence


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project",type=Path,default=Path.cwd())
    parser.add_argument("--output",type=Path,required=True)
    parser.add_argument("--epochs",type=int,default=1)
    args=parser.parse_args()
    run_smoke(args.project,args.output,args.epochs)
