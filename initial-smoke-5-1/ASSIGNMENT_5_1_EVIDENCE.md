# Assignment 5.1 GRU implementation and training evidence

**Executed 2026-11-24. Classification: TRAINING SMOKE TEST ONLY.**
A custom randomly initialized PyTorch GRU binary classifier completed one real
training epoch. True capture independence remains unverified. This demonstrates
implementation and optimization, not held-out detection quality or reliability
under vendor-restricted visibility.

Gaurav explicitly authorized this assignment demonstration. It does not take
ownership of Nitendra's final models/calibration or finalize a producer API.
The [primary research scope](research_scope.md) and pending capability/profile
review remain unchanged. No pretrained model or unrelated architecture was used.

## Implemented work

- src/reliability/assignment51_gru.py: custom GRUBinaryClassifier(nn.Module),
  audited data loading, train-only standardization, padded/packed sequence
  handling, reproducible CPU training and checkpoint/evidence persistence.
- notebooks/04_assignment_5_1_gru_smoke.ipynb: architecture and executed-run
  viewer with checksum/reload checks; optional new-run switch defaults False.
- tests/test_assignment51_gru.py: optimization/checkpoint round-trip, padding
  invariance, train-only scaler and source/clock/label/identity/duplicate/value
  failure cases. PyTorch is an optional dependency for the earlier workstream.
- requirements-training.txt pins the optional direct torch dependency. It is
  not a full environment lock.

Reused the fixed cohort/window/split JSON and tested build_splits validation,
the original SQLite database and existing EDA findings. There was no reusable
model-ready preprocessing pipeline to import: the legacy EDA preserves an audit
copy and flags issues. Added only train-fitted scaling for these assignment
inputs; did not rewrite its cleaning or adopt its provisional UTC conversion.
Existing notebooks/modules were left intact.

## Exact architecture and inputs

| Setting | Executed value |
| --- | --- |
| Task/labels | Benign=0; the five other existing archive categories=1; reject contradictions |
| Features in tensor order | dlMcs, dlBler, ulMcs, ulBler, phr, pcmax, rsrq, sinr, rsrp, rssi, cqi, pucchSnr, puschSnr |
| Input shape | batch x at most 10 observed reports x 13 features; float32 after scaling |
| Sequence length | Existing EP-4 ten-report/stride-ten grid; variable-length retained tails, no conversion to seconds |
| GRU | One layer, 32 hidden units, unidirectional, batch_first=True |
| Dropout | 0.0; no recurrent dropout for the single layer; output dropout also 0 |
| Output | Final true hidden state -> Linear(32,1) -> one raw attack logit |
| Trainable parameters | 4,545 |
| Initialization | Random weights from seed 42; no pretrained state |
| Sequence state | Fresh zero hidden state for each window; no carried state between windows/files |
| Tail handling | Zero tensor padding for batching; packed lengths exclude padding from recurrent computation |

The assignment feature list is an engineering demonstration, not an approved
vendor profile, required KPI set or claim of a minimum telemetry set. Excluded
IDs, labels/target metadata, timestamp values, cellid, in_sync, rnti, ue_id,
constant/ambiguous ri/PMI and unresolved dlBytes/ulBytes counters. Missing or
nonfinite selected values fail explicitly; no imputation or clipping was used.
Finite values are not proof of physically validated KPI semantics.

Means/population SD were fitted on the 26,455 unique referenced primary outer
training reports in float64; transformed tensors use float32. Padding never
enters scaler estimates. A zero training SD would use scale 1 without dropping
the feature; no selected feature had zero SD in this run. Scaler values and
feature order are persisted in the checkpoint/evidence.

This implements a custom model class with PyTorch's GRU layer; it does not
manually reimplement the GRU kernels. PyTorch's documented
[GRU](https://docs.pytorch.org/docs/2.9/generated/torch.nn.GRU.html),
[packed sequences](https://docs.pytorch.org/docs/2.9/generated/torch.nn.utils.rnn.pack_padded_sequence.html)
and [BCEWithLogitsLoss](https://docs.pytorch.org/docs/2.9/generated/torch.nn.BCEWithLogitsLoss.html)
define those building blocks. No sigmoid is applied before the loss, which
already combines sigmoid and binary cross entropy.

## Exact training configuration and hardware

| Setting | Executed value |
| --- | --- |
| Loss | BCEWithLogitsLoss, unweighted mean; no class weights |
| Optimizer | Adam, learning rate 0.001; default betas (0.9,0.999), eps 1e-8, weight_decay 0, amsgrad False |
| Batch size | 64; shuffled training windows, final batch retained |
| Epochs | 1; no early stopping, hyperparameter search or model selection |
| Random seed | 42 for Python, Torch and an isolated DataLoader generator |
| DataLoader workers | 0 |
| Device | CPU explicitly selected; 1 Torch CPU thread; deterministic algorithms enabled |
| Runtime | Python 3.11.14; PyTorch 2.9.1+cpu; Windows 10.0.26200 / AMD64 |
| Reported CPU identifier | AMD64 Family 25 Model 68 Stepping 1, AuthenticAMD |
| Accelerator | torch.cuda.is_available=False; torch CUDA/HIP runtime=None; no GPU training attempted |
| Interpreter | C:\Users\saiga\miniforge3\envs\rocm-jupyter\python.exe |

Despite the environment name, this installed Torch build is CPU-only. No
framework packages or GPU drivers were installed/changed for this task.

## What was actually executed

From the project root, the actual training command was:

```powershell
$env:PYTHONPATH = 'src'
& 'C:\Users\saiga\miniforge3\envs\rocm-jupyter\python.exe' -m reliability.assignment51_gru --project . --output results/assignment_5_1_gru_smoke_2026-11-24 --epochs 1
```

Console output was also captured through Tee-Object into
results/assignment_5_1_training_console_2026-11-24.txt. The structured JSON/JSONL
files below are the authoritative machine-readable evidence.

| Training quantity | Actual observation |
| --- | ---: |
| Primary training reports | 26,455 |
| Training windows | 2,669 |
| Provisional primary training file groups | 24 |
| Retained partial training windows | 46 |
| Window label counts | Benign 615; attack 2,054 |
| Epoch 1 optimizer updates | 42 |
| Epoch 1 reports/windows visited | All 2,669 windows once; no dropped last batch |
| Epoch 1 mean training BCE loss | 0.571900883934479 |
| Epoch optimization time | 0.30494419997558 seconds, excluding data preparation/checkpoint IO |

Loss is the sample-weighted mean of minibatch losses encountered while
parameters are being updated. It is not a validation/test loss, final frozen
model evaluation or claim that loss decreased from a measured baseline.
There is no reported accuracy, AUC, selected operating threshold or calibrated
confidence. Class imbalance is retained and disclosed.

Saved files, outside Git under results/assignment_5_1_gru_smoke_2026-11-24/:

| File | Evidence |
| --- | --- |
| training_evidence.json | Exact config, scaler, environment, parent/input hashes, training IDs/counts, epoch metrics and weight/checkpoint hashes |
| training_log.jsonl | Actual epoch record |
| checkpoint_epoch_final.pt | Trained model and Adam state, scaler/config and epoch |

Checkpoint SHA-256:
`1e4f64256654f6d30189d14d73f9d4fcfa8da0bcf91678c52ffd34a4cb45ea75`.

Parameter-state SHA-256 changed from
`38734729eac83b8a1b4fb1d35b6a26b7d62115882b94a54643be9d48456a9e0b`
to `0daca02d95afbd01aac174f28a4b77794b69c89557dbf62940800bec1655df32`.
The checkpoint was loaded into a fresh custom model with weights_only=True;
its parameter digest matched the trained digest. This and the finite-loss/
gradient checks establish actual optimization and a reloadable artifact.

Tests were actually run with the Torch interpreter and the existing project
pytest library appended read-only to sys.path, without installing pytest into
that interpreter. The full suite returned **102 passed in 5.85s**, including
eight new GRU cases. Exact command:

```powershell
$env:PYTEST_DISABLE_PLUGIN_AUTOLOAD = '1'
& 'C:\Users\saiga\miniforge3\envs\rocm-jupyter\python.exe' -c "import sys, torch; sys.path.append(r'C:\Users\saiga\Documents\Master of AAI - Sandiego\AAI-590\project\.venv\Lib\site-packages'); import pytest; raise SystemExit(pytest.main(['-q']))"
```

In another environment, install requirements-dev.txt and requirements-training.txt
into that environment and use python -m pytest -q. The earlier project .venv
lacks Torch and will skip the optional GRU tests; that skip is not training
evidence. requirements-notebooks.txt supplies optional notebook execution tools.

The new notebook was also actually executed in a fresh rocm-jupyter kernel
from notebooks/: all three code cells completed without cell errors in
7.69 seconds, displaying the saved run and verifying its checkpoint hash and
reloaded parameter digest. This viewer execution did not train again.
Validation: results/assignment_5_1_notebook_validation_2026-11-24.json.

## Leakage ordering and boundary checks

- Rebuilt expected assignments using existing tested split validation and
  required exact agreement with the saved manifest; no new partition drawn.
- Checked train/validation/test group disjointness. Selected only training
  windows and fetched only their report values from read-only SQLite.
- Labels are separate targets. The 13-column input allowlist excludes IDs,
  raw clocks, label fields and byte counters. No held-out features/scores were
  used to fit scaling, weights or settings. Earlier global EDA is disclosed;
  the holdout has been inspected structurally, not evaluated for performance.
- Checked each report's primary cohort, source file/group, original line order,
  UE/cell/RNTI identity, category/binary truth and raw timestamp endpoints.
  Raw clocks must increase within each window; no reordering, gap-based run
  inference, clock repair or cross-file sequence is allowed.
- Verified all 50 raw input hashes before/after, plus parent cohort/window/split
  identities. Parent and input identities are saved in training_evidence.json.

## Limitations and unresolved issues

True independent capture boundaries remain unverified; file/identity windows
are provisional. This run is therefore **smoke test only**, even though group
separation and within-window ordering pass. Source clock authenticity/units,
semantic KPI validity and some source/database lineage remain unresolved.
The primary cohort omits current uncertain-clock single-source ACK/SYN temporal
examples; the 1,540 secondary rows were not used here.

No vendor capability mapping/profile is implemented. No restricted-visibility
comparison, final feature set, hyperparameter study, class weighting,
calibration, threshold selection or abstention evaluation has been completed.
Packed tails are an assignment-only choice, not Nitendra's agreed final input
contract. One epoch of training loss does not substantiate generalization,
false-positive rates, robustness or scientific novelty.

## Next steps

Review the assignment code/evidence with Gaurav and Nitendra. Continue
CAP-01/CAP-02 capability evidence/profile approval and AP-2 input agreement.
Keep the fixed manifests, train-only fitting and full retained-tail accounting.
Only after those gates, plan model selection and supported validation/test
evaluation; do not tune on the held-out test set. Nitendra retains final model
and calibration ownership. Keep checkpoints/local evidence in Drive or a
reviewed artifact store, not Git; code, notebook and this evidence summary can
be committed. No upload or submission was performed.
