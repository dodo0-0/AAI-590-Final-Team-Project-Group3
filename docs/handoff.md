# Gaurav workstream handoff - 2026-11-16

Start here, then consult [the checklist](../planning/checklist.md), the sole
task-status authority. This is a handoff of methodology and tested support
utilities, not a completed detector or finished capstone. Nothing has been
pushed or uploaded by this preparation step. Repository/Drive URLs and the
published commit ID must be added when the team actually shares the files.

## 1. What to put on GitHub

Commit these project-relative paths:

```text
.gitignore
AGENTS.md
README.md
pyproject.toml
requirements-dev.txt
requirements-notebooks.txt
src/
tests/
docs/
planning/
notebooks/README.md
notebooks/00_combined_dataset_audit.ipynb
notebooks/01_dataset_understanding.ipynb
notebooks/02_source_database_reconciliation.ipynb
notebooks/03_timing_and_metadata_provenance.ipynb
data/README.md
results/README.md
```

Keep the combined notebook as the team's entry point; originals retain the
investigation history. Its saved aggregate outputs have been reviewed.
Environment messages can contain local interpreter paths; they are provenance,
not a portable setup requirement. The older root-level
AAI590_Data_Cleaning_EDA.ipynb was preserved and is outside this initial
reviewed publish list; keep the local copy until separately reviewed.

Exclude data contents, result JSON, archive_2.zip, handoff bundles, .venv,
caches, .env and notebook checkpoints. Existing .gitignore covers these;
handoff/ is now ignored too. No large-data Git/LFS setup is required here.

This folder currently has no .git directory. If joining an existing team
repository, clone that repository and copy only the listed project files into
the agreed project location on a working branch. Preserve any existing team
work. Do not initialize a competing repository in that case.

For a new standalone repository only, from this project root:

```powershell
git init -b main
git add .gitignore AGENTS.md README.md pyproject.toml requirements-dev.txt requirements-notebooks.txt src tests docs planning notebooks data/README.md results/README.md
git diff --cached --stat
git diff --cached --name-only
```

Review the staged list against the paths above before committing. No raw data,
results JSON, local environment or handoff ZIP should appear. Then create the
commit and connect the actual team remote:

```powershell
git commit -m "Add Gaurav research methodology and audit handoff"
git remote add origin ACTUAL_TEAM_REPOSITORY_URL
git push -u origin main
git rev-parse HEAD
```

Replace ACTUAL_TEAM_REPOSITORY_URL; do not run placeholder text literally.
The existing-team-repository flow uses that team's branch/PR process instead.
Record the actual commit ID next to the Drive bundle so teammates know which
code generated/consumes the artifacts. These commands are guidance, not an
executed push.

## 2. What to upload to Drive

The prepared local handoff/ directory contains a shared-artifacts ZIP, its
SHA256SUMS.txt and an inventory manifest. Upload those three files into a
dated team folder alongside the GitHub commit reference. The ZIP restores:

```text
data/radio/                 # selected database, 49 source files, extraction manifest
results/                   # existing local audit/manifests/validation evidence
results/handoff_package_manifest_2026-11-16.json
```

Keep these internal paths. No notebook or Python dependency is bundled here;
those come from GitHub/environment setup. The full archive_2.zip is excluded.
It can remain your backup; packet/network/legacy modalities are not needed
for the current radio workstream. This bundle does not include all Kaggle data.
Dataset/source links and unavailable revision information are documented in
[the inventory](dataset_inventory.md) and [provenance review](provenance_sources.md).

All existing results are included to retain historical evidence, but the
current assignments to consume are these three files, not previews:

| Artifact | Use |
| --- | --- |
| cohort_group_manifest_ep1_ep2_2026-11-15.json | All 45,244 database references, primary/secondary membership and provisional groups |
| window_manifest_ep1_ep4_2026-11-15.json | 4,406 primary windows, including 74 tails, and report references |
| split_manifest_ep1_ep5_2026-11-15.json | Fixed partitions and training-only CV propagated to rows/windows |

Approval JSON and preview files record their generation stage. They do not
override later decisions or the checklist. The package inventory preserves
file sizes/hashes plus code, notebook and core-method-document identities;
it supplies snapshot identity while the Git commit is not yet available.
No model predictions, weights, fitted transforms or selected thresholds exist
in this handoff.

## 3. How teammates reproduce the work

1. Obtain the agreed GitHub checkout. Download the dated Drive bundle and
   verify its SHA-256 against SHA256SUMS.txt, for example with
   `Get-FileHash -Algorithm SHA256 -LiteralPath 'C:\path\bundle.zip'`.
2. Extract it into the project root so data/radio/Lower_Layer_Data.db and
   results/ appear at the documented paths. Avoid flattening nested source
   directories. Extracting into a fresh checkout avoids mixing snapshots.
3. In that project root create their own Python 3.11+ environment:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-notebooks.txt
.\.venv\Scripts\python.exe -m pytest -q
```

4. Select that environment in the notebook editor; no ROCm installation is
   required for these audits. Open
   [00_combined_dataset_audit.ipynb](../notebooks/00_combined_dataset_audit.ipynb),
   restart once and Run All. Do not restart between parts. If using an existing
   Python 3.11+ kernel, ensure IPython/ipykernel are available. Notebook execution
   does not require pytest installed in that separate kernel.
5. Expect 23 code cells to complete, hash checks to pass and the three fresh
   audit reports to match the restored results. Input changes require review,
   not overwriting a mismatch. Builders in README refuse existing output paths;
   use a new filename if deliberately rebuilding artifacts.

Last code suite: 89 tests passed in 0.71s (2026-11-16). The user-saved combined
notebook was independently checked against a fresh 23-cell ROCm-kernel run,
including 31 display bundles and all 50 input hashes. These are prior executed
checks, not a claim that the recipient has reproduced them.

## 4. What is done and what remains

| Area | Evidence-backed state | Remaining work |
| --- | --- | --- |
| Threat model | Bounded analytical model accepted, v1.0 | Topology, attacker privileges and capture independence remain unknown |
| Evaluation definitions | EP-1 through EP-6 approved, v1.0 | Ranking/aggregation/threshold utilities and agreed producer adapters incomplete |
| Data provenance | Structural/reconciliation/timing audits and combined notebook verified | True capture IDs and metadata origin unresolved |
| Cohorts/windows/splits | Materialized with checked hashes and deterministic references | Revisit only through reviewed changes; never redraw using favorable scores |
| Abstention | AP-1 completeness approved and tested; outcome accounting tested | AP-2 input agreements, AP-3 constraints/search and AP-4 numerical settings pending |
| Models/degradation/results | No empirical model or policy experiments executed here | Producer implementations and paired evaluation remain future work |

Important limits to explain: primary population is 43,704 source-metadata-matched
rows; 1,540 uncertain-clock rows remain non-temporal only. Primary temporal
coverage omits current single-source DoS ACK/SYN examples. Source files are
provisional groups, not verified independent captures. Clocks remain raw units.
Two Benign validation and two Benign test groups cannot establish very low FPR.
One CV fitting fold lacks primary DoS; binary support is not complete multiclass
support. Neither data volume nor repeated windows fixes these limitations.

## 5. Where each person picks up

| Owner | Read first | First action |
| --- | --- | --- |
| Nitendra | Evaluation protocol sections 4-7; fixed split/window artifacts; AP-2 input proposal | Agree required/optional model inputs, validity, score semantics and short-window support; then own model/preprocessing/calibration implementation using fixed groups |
| Marco | Threat model sections 3/5; evaluation protocol section 10; AP-2 proposal | Agree fixed-grid pairing, observable masks/expected counts and justified scenarios; then own degradation/playback implementation |
| Gaurav | Abstention policy sections 5/7; checklist; AP-2 proposal | Record input agreements; define AP-3 security/coverage constraints/search before selecting policy settings; finish evaluation/policy utilities incrementally |

The detailed [AP-2 proposal](abstention_input_proposal.md) is not an agreed API.
Do not tell producers they must implement a finalized schema. No assistant
message has been sent to teammates. Handoff review should record decisions
and who agreed before adapters depend on them.

For a short walkthrough: open this page and checklist; show the three method
documents and their approval states; show the combined notebook's three parts;
point to the three fixed artifacts; explain the limitations above; close with
the three owner-specific next actions. No model performance claim is supported
by audit completion or passing synthetic tests.
