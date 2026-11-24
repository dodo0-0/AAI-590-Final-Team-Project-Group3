# AAI-590: Intrusion detection with vendor-restricted O-RAN telemetry

Working title: **Intrusion Detection with Vendor-Restricted O-RAN Telemetry**.
Primary question confirmed by Gaurav on 2026-11-17: how reliably can detection
operate with vendor-restricted measurements, and when should it abstain?
See [the scope clarification](docs/research_scope.md). Shortcut checks support
evaluation validity; dropped/stale-report scenarios are secondary. No vendor
capability profile or restriction experiment has yet been validated.

This workspace supports Gaurav's threat modeling, evaluation protocol, and
abstention policy responsibilities. Nitendra owns ML baselines, GRU/TCN models,
and calibration; Marco owns E2-based degradation models and playback.

Start each session with [the checklist](planning/checklist.md) and
[the progress log](docs/progress.md). The checklist is the task status authority.
For GitHub/Drive sharing and teammate onboarding, use the
[handoff guide](docs/handoff.md).
Its [November 24 EDA update instructions](docs/handoff.md#november-24-eda-update)
show exactly which two files to add to Drive and where teammates restore them.

## Current state

The workspace was empty at inspection on 2026-11-08. As of 2026-11-15,
the current radio subset is extracted, three original audit notebooks and a
combined audit notebook are available,
and tested utilities document structural and provenance findings. No model
performance experiment has been executed here. Evaluation definitions EP-1
through EP-6 are approved; quality parameters and teammate interfaces remain gated.

- [Dataset inventory and evidence gaps](docs/dataset_inventory.md)
- [EDA cleaning ledger and interpretation follow-up](docs/eda_cleaning_addendum.md)
- [Reviewed bounded threat model](docs/threat_model.md)
- [Abstention-policy draft and pending decisions](docs/abstention_policy.md)
- [AP-2 input proposal for teammate review](docs/abstention_input_proposal.md)
- [Milestones](planning/milestones.md)
- [Team dependencies](planning/team_dependencies.md)
- [Methodological decisions](docs/decisions.md)
- [Approved evaluation definitions and remaining gates](docs/evaluation_protocol.md)

The protocol records approvals and remaining interface/quality-policy gates.
A dedicated abstention-policy draft is available. AP-1 completeness is approved;
required quality inputs, numerical cutoffs and security budgets remain pending.
`src/reliability/completeness.py` computes the approved minimum from explicit
expected positions and observed-valid masks. It chooses no KPIs/cutoffs and
does not execute an abstention policy or establish a producer contract.
`src/reliability/data_audit.py` implements
the first read-only structural inventory with synthetic pytest coverage.
The six milestones are recorded in the checklist; models, run reconstruction
and quality-policy execution are not implemented. The pure
`src/reliability/outcome_metrics.py` helper counts supplied binary truth against
BENIGN/ATTACK/ABSTAIN outcomes and reports denominators/NA reasons. It requires
all planned labeled units; it does not load predictions, choose thresholds,
aggregate windows or compute ranking metrics. Synthetic tests are not measured
detector results.

## Development setup (PowerShell, Python 3.11+)

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m pytest -q
```

Pytest is pinned as a direct development dependency; this is not a complete
environment lock. Record resolved package versions with implementation and
experiment artifacts. Run tests from the project root: pytest adds `src/` to
its import path. No editable package installation is needed at this stage.
Tests cover inventory logic; they do not establish research findings.

## Read-only inventory

```powershell
.\.venv\Scripts\python.exe src/reliability/data_audit.py --root data/radio --output results/radio_inventory_2026-11-13.json
```

Use a new output filename on reruns: the command refuses to overwrite an
existing output or write inside the source directory. It verifies extracted
file hashes against the extraction manifest when supplied, inventories the
SQLite schema/NULLs/distinct values/labels and JSONL source fields/timestamp
availability, and checks source hashes again afterward. It does not interpret
timestamp units, reconstruct runs, reconcile rows or select model features.
See [initial findings](docs/data_audit_findings.md).

## Research notebook

For all three audits in one place, open
[00_combined_dataset_audit.ipynb](notebooks/00_combined_dataset_audit.ipynb).
Select Python 3.11+ (including your rocm-jupyter kernel), restart once and
Run All. Do not restart between parts. It includes the 23 original nonempty
code cells unchanged, with a contents list and sequential sections.
The November 24 Part 4 adds one descriptive-summary cell (24 code cells total)
and links the cleaning/interpretation ledger. Existing result manifests must
be restored under results/ to execute that section. Original
decision-gate text describes the audit stage; current approvals live in the linked documents
and checklist. The three original notebooks remain unchanged.

Open [01_dataset_understanding.ipynb](notebooks/01_dataset_understanding.ipynb)
and select the project `.venv` interpreter. Restart the kernel and Run All.
It recomputes the tested audit and explains schema, labels, count differences,
timestamp availability and pending lineage questions without altering inputs.
See [notebook setup and execution](notebooks/README.md) for optional
dependencies and the command for execution without an interactive editor.
The root-level EDA notebook's analysis code and saved outputs are preserved;
its Markdown now clarifies the provisional UTC interpretation and links the addendum.

## Source-to-database diagnostics

[02_source_database_reconciliation.ipynb](notebooks/02_source_database_reconciliation.ipynb)
explains exact radio/metadata candidate comparisons and retains ambiguous,
unmatched and unusable occurrences. It runs independently of notebook 01.
The saved notebook 01 was preserved. Matching logic lives in a tested module:

```powershell
.\.venv\Scripts\python.exe src/reliability/reconciliation.py --root data/radio --output results/radio_reconciliation_2026-11-13.json
```

Choose a new filename on reruns. Output is written outside the input folder
without overwriting files. The local detailed JSON includes candidate groups,
source path/line references and database rowids. These references are not run
IDs. See [reconciliation findings](docs/reconciliation_findings.md) for methods,
results and unresolved timing provenance.

## Timing and provenance diagnostics

[03_timing_and_metadata_provenance.ipynb](notebooks/03_timing_and_metadata_provenance.ipynb)
describes original-order raw timestamp steps, exact-identity cross-file
overlaps and the questionable DoS metadata coincidences. It preserves all
records and does not assign runs. The ZIP directory inspection is optional.

```powershell
.\.venv\Scripts\python.exe src/reliability/timing_audit.py --root data/radio --archive data/archive_2.zip --output results/timing_audit_2026-11-15.json
```

Omit `--archive` if the ZIP is unavailable; choose a new output filename on
reruns. See [timing findings](docs/timing_findings.md) and
[external provenance review](docs/provenance_sources.md). Raw-unit clock
diagnostics do not verify timestamp semantics or independent capture IDs.

## Approved cohort and provisional group manifest

EP-1 timing separation and EP-2 source-file grouping are approved; the rest
of the evaluation protocol remains a draft. Reproduce the row-level manifest:

```powershell
.\.venv\Scripts\python.exe src/reliability/cohort_manifest.py --root data/radio --reconciliation results/radio_reconciliation_2026-11-13.json --output results/cohort_group_manifest_ep1_ep2_2026-11-15.json
```

Choose a new output filename on reruns. The command verifies the reconciled
input snapshot and records all database rows, cohort flags, source path/line
and provisional group IDs. No windows, split assignments or clock conversions
are made. Current output has 43 provisional source-file groups, with 40 in
the primary temporal cohort. Capture independence is unverified. Optional
`--capture-links` accepts reviewed file links with evidence references;
no links are currently applied. Unknown or contradictory source references
stop construction instead of choosing an arbitrary match.

## Approved report-window manifest

EP-3 retains raw units/source order; EP-4 approves length/stride ten with
partial tails preserved. Reproduce the primary-cohort window references:

```powershell
.\.venv\Scripts\python.exe src/reliability/window_manifest.py --root data/radio --cohort-manifest results/cohort_group_manifest_ep1_ep2_2026-11-15.json --output results/window_manifest_ep1_ep4_2026-11-15.json
```

Choose a new output filename on reruns. Output covers all 43,704 primary
reports in 4,332 full windows and 74 tails. Raw inputs are hash-verified before
and after construction. Tails retain their actual expected report count;
SHORT_WINDOW is a conditional reason for later unsupported scoring, not an
already emitted prediction. No padding, time conversion, partitions or scores
are produced. Model compatibility remains to be agreed with Nitendra.

## Approved group partitions and training CV

EP-5 fixes approximate 60/20/20 source-group partitions, seed 42, and three
training-only grouped CV folds. Reproduce the references:

```powershell
.\.venv\Scripts\python.exe src/reliability/split_manifest.py --root data/radio --cohort-manifest results/cohort_group_manifest_ep1_ep2_2026-11-15.json --window-manifest results/window_manifest_ep1_ep4_2026-11-15.json --output results/split_manifest_ep1_ep5_2026-11-15.json
```

Choose a new output filename on reruns. Primary groups are 24/8/8; full groups
are 25/9/9 with one secondary-only group in each. Every row/window inherits
one parent group's assignment. CV excludes outer validation/test groups.
File-group separation is not proven capture independence. Per-family support
gaps are recorded in the protocol and artifact. No model scores, preprocessing
fits, thresholds or predictions are involved in constructing these partitions.

## Data handling

Keep raw data outside version control. `data/` and `results/` contents are
ignored by default; keep only their committed README files. Current locations
and evidence are recorded in the dataset inventory. Record known source/version
information, checksums, time semantics and source-to-run provenance, and mark
unavailable fields explicitly. Experimental claims must respect those limits.
Never commit credentials or raw telemetry.
