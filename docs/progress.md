# Progress log

## 2026-11-08 — Initial evidence-first setup

**Completed work:** Read the attached research instructions and inspected the
workspace and immediate project context. The workspace was empty and not a
Git repository; no applicable AGENTS.md was found in the inspected locations.
Created a minimal scaffold, actionable milestones, ownership/dependency map,
unverified dataset evidence register and draft threat-model skeleton.

**Current work:** TM-01 threat review. SET-01 scaffold verification is complete.
The checklist remains the status authority.

**Problems/blockers:** Dataset, source capture manifests, prior audit code,
reference paper and meeting notes are unavailable in this workspace.
Source-run reconstruction, class/date support and feature semantics cannot be
validated. Model/window/score and degradation/quality interfaces are pending.

**Decisions:** Follow the user's incremental initial instruction. Implement no
data-specific utilities before schema inspection. Treat meeting claims as
unverified; preserve teammate ownership. Evaluation and policy definitions
remain pending approval (D001–D003).

**Verification:** Python 3.11.5 is available. `python -m pytest --version`
failed because pytest is not installed; no pytest tests ran. A read-only
Python document integrity check passed for 11 scaffold Markdown files,
7 local links and 13 unique task rows with statuses and required columns.
The first integrity-check attempt failed because the check incorrectly
expected 14 tasks; the expectation was corrected to the actual 13 tasks and
the check reran successfully. No product code or experimental logic was
changed to make the check pass. No Python implementation, empirical analysis
or experiment has been run. The draft threat model is not reviewed and is
not a completed research deliverable.

**Next recommended action:** Obtain actual dataset/source locations and
version/provenance, then implement and test the smallest read-only schema
inventory. Review the threat skeleton against capture documentation.

## 2026-11-08 — Workstream initialization follow-up

**Existing material inspected:** Read AGENTS.md, checklist and progress before
work, then inspected the README, milestones, teammate dependencies, decisions,
dataset evidence register, threat model and ignore rules. Existing material
was documentation only: M1-M5, 13 tracked tasks and an unreviewed threat model.
No Git metadata, dataset, implementation or tests were present.

**Completed work:** Expanded tracking to M1-M6 and 15 detailed tasks while
preserving prior IDs/evidence. Separated paired robustness from report/handoff.
Added pyproject.toml, requirements-dev.txt, src/reliability/__init__.py and
tests/README.md. Created a local .venv and installed pytest 8.3.5. Updated the
README and missing-input register. No research algorithm was implemented.

**Verification and evidence:**

- `python -m venv .venv` succeeded. The first pip installation was blocked by
  sandbox network access; the approved retry succeeded.
- `.\.venv\Scripts\python.exe -m pytest --version`: pytest 8.3.5.
- `.\.venv\Scripts\python.exe -m pytest --collect-only -q`: no tests collected.
  PowerShell's command wrapper reported exit 1. A subsequent Python subprocess
  invocation of `-m pytest --collect-only` confirmed native pytest exit 5,
  project root/configfile pyproject.toml and testpaths tests. This is the
  expected empty-suite outcome, not passing implementation tests.
- Read-only Python checks passed for the package import from src, TOML
  configuration, 12 Markdown files, 7 relative links and 15 unique task rows
  with required columns/statuses mapped to M1-M6. No scientific validation.
- `.\.venv\Scripts\python.exe -m pip freeze` recorded: colorama 0.4.6,
  iniconfig 2.3.1, packaging 26.3, pluggy 1.7.0, pytest 8.3.5. Python 3.11.5
  on Windows. requirements-dev.txt pins only the direct pytest dependency;
  it is not a full environment lock.

**Current work:** M1 evidence acquisition and threat-model review. Only setup
tasks SET-01/02 are complete; no milestone or research task is complete.

**Problems/blockers:** No actual radio data or provenance supplied. Source
manifests, data dictionary, attack documentation, paper and previous audits
are missing here. Teammate output/quality interfaces remain proposals.

**Decisions:** D004 records the requested six milestones and minimal setup.
Model training/calibration stays with Nitendra; degradation/playback stays
with Marco. Scope and evaluation assumptions remain unchanged.

**Next recommended action:** DATA-00: supply and verify the actual data
location and release provenance. Then inspect its format and implement/test
one read-only inventory utility (DATA-01). Review threats against the supplied
capture documentation. Do not start full evaluation or abstention code yet.

## 2026-11-08 — Selective download guidance

**Completed work:** Inspected the user's 145.96 GB Kaggle explorer screenshot,
the authors' dataset landing page, Zenodo file-role documentation and official
Kaggle individual-file download documentation. Updated the evidence register
with source links, remote-inspection limits and staged acquisition guidance.

**Current work:** DATA-00 is in progress: a likely author-linked source is
identified; exact Kaggle release and local access are still unverified.
No additional task is complete.

**Problems/blockers:** Kaggle's dynamic tree was not readable by the web tool.
The screenshot does not reveal nested filenames, lower-layer total size or
version. Zenodo's listed 5.4 MB database size does not establish Kaggle size
or release equivalence. No dataset content or run provenance inspected.

**Decisions:** Recommend staged acquisition by modality: radio summary first,
then source radio files across all six current classes. Defer packet captures,
network summaries and legacy data unless a documented dependency requires
them. This preserves the proposed study population; no evaluation definitions
or teammate interfaces changed.

**Tests executed:** None; documentation/advice only. Browsed source pages;
did not install the Kaggle CLI, download data or claim empirical validation.

**Next recommended action:** Download Lower_Layer_Data.db from the selected
Kaggle release and provide its local location/version. Inspect schema and
provenance, then identify the exact source radio paths required for validation.

## 2026-11-13 — Selective local ZIP extraction

**Completed work:** Read AGENTS.md and current tracking. Inspected
data/archive_2.zip (25,101,375,790 bytes) without full extraction: 320 file
entries, 145,957,931,888 listed uncompressed bytes. Extracted only the root
Lower_Layer_Data.db and all 49 source files in the six current Lower_Layer
directories. Preserved original paths under data/radio/. Selected output
totals 22,786,276 bytes (22.79 MB). Original ZIP is unchanged; network and
legacy content remain compressed.

**Verification:** The extraction command succeeded. Checked destination
containment, duplicate destinations and no-overwrite conditions before
writing. ZIP CRC checks passed while reading all 50 selected members; verified
written sizes and re-read SHA-256 hashes. Recorded per-file evidence in
data/radio/extraction_manifest.json. No pytest tests or research experiments
ran; this was a standard-library extraction operation, not a new project
utility. The entire archive has not been integrity-tested or hashed.

**Current work:** DATA-00 remains in progress because Kaggle release and
source provenance remain incomplete. DATA-01 is now in progress: archive
inventory/extraction done; schema, label and timestamp inspection pending.
No research task is marked complete. Source-run validation remains pending.

**Problems/blockers:** Unknown Kaggle platform version and no validated
source-to-summary/run manifest. Twelve Benign text files were recovered, but
their independence, dates and relationship to the summary are unknown.

**Decisions:** D005 records selective radio extraction with all six classes
and filenames preserved. No model, degradation or evaluation assumptions
were changed.

**Next recommended action:** Inspect the extracted SQLite schema and source
text format read-only, then implement the smallest reproducible inventory
utility with synthetic logic tests. Do not equate 49 source files with the
preliminary 52 reconstructed or reported 42 paired runs.

## 2026-11-13 — Read-only schema and source inventory

**Completed work:** Inspected the database with SQLite read-only mode and
sampled each class's source format. Implemented src/reliability/data_audit.py
and synthetic tests in tests/test_data_audit.py. Added a reproducible command
to README and documented actual-data findings in docs/data_audit_findings.md.
Updated the dataset evidence register and task dependencies.

**Observed evidence:** One database table with 45,244 rows and 25 columns,
six category values (including literal Web Attacks), no explicit source/run
column. All 49 sources parsed as JSONL: 50,213 valid objects, no invalid
records, but only 44,452 objects have finite numeric timestamps. Eight files
have none; Probe/portscan_udp.txt is mixed (573 of 1,142 timestamped).
The DoS database count (4,721) differs from both total source DoS objects
(8,187) and timestamped source DoS objects (3,929). No cause inferred.

**Tests executed and results:**

- `.\.venv\Scripts\python.exe -m pytest -q`: initially 6 passed in 0.22s;
  after adding manifest-membership and CLI output-path protection tests,
  final suite: **8 passed in 0.25s**.
- `.\.venv\Scripts\python.exe src/reliability/data_audit.py --root data/radio --output results/radio_inventory_2026-11-13.json`: succeeded.
- Repeated with output results/radio_inventory_2026-11-13_repeat.json:
  succeeded. A separate byte comparison confirmed identical outputs.
- Both actual-data executions verified all 50 input sizes/hashes against the
  extraction manifest and rechecked SHA-256 after inspection; inputs unchanged.
  Separate assertions confirmed 49 sources, 50,213 objects and 44,452 numeric
  timestamps. Results are local ignored artifacts; findings are in docs.

**Current work:** DATA-01 remains in progress: structural inventory portion
is evidenced, but field semantics, lineage and time interpretation are not
validated. DATA-02 remains blocked on these issues; no run IDs recovered and
no research milestone completed. Tests are logic evidence, not label/run proof.

**Problems/blockers:** Unknown Kaggle release/processing provenance, varying
source schemas and missing timestamps, unexplained source/database mismatch.
Repeated database timestamps may represent multiple UEs and do not establish
duplicates. No sampling frequency, class/date support or benign independence
has been validated.

**Decisions:** D006 keeps timestamps raw and labels literal. No imputation,
row exclusion, counter transformation, model training or evaluation changes.
Nitendra's and Marco's implementation ownership remains unchanged.

**Next recommended action:** Reconcile source records against the database,
starting with DoS and mixed-schema Probe, retaining all ambiguous/unmatched
cases. Seek processing documentation and Kaggle version in parallel. Use
that evidence to propose run/group rules for Gaurav's review, not to silently
infer missing timestamps or independent runs.

## 2026-11-13 — Executed dataset-understanding notebook

**Completed work:** Read tracking and inspected existing files. Discovered
and inspected AAI590_Data_Cleaning_EDA.ipynb (17 cells) without modifying it.
Created notebooks/01_dataset_understanding.ipynb (16 cells, 7 code cells) with
environment provenance, fresh audit execution, schema/label tables, source
versus database comparison, missing timestamp diagnostics, schema variation,
methodological limits and a pending reconciliation plan. All reusable parsing
continues to live in the existing audit module. Added notebook usage notes
and optional requirements-notebooks.txt; installed direct pins nbformat
5.10.4, nbclient 0.10.2 and ipykernel 6.29.5 into the existing .venv after
approved network access. Initial sandbox installation was network-blocked.

**Verification and actual results:**

- Validated the notebook against nbformat 4.5 schema.
- Executed the final notebook in two fresh project-.venv kernels via
  nbclient.NotebookClient: once from project root, once from notebooks/.
  Each completed all 7 code cells in order with no errors; aggregate cell
  outputs were identical across launch directories. Saved executed outputs.
- In each final execution, extraction-manifest verification passed for all
  50 inputs and before/after hashes remained unchanged. The fresh inventory
  matched the prior CLI report as parsed JSON. Findings remain 45,244 database
  rows, 50,213 source objects, and 44,452 timestamped source objects.
- The pre-existing EDA notebook SHA-256 remained
  ad7998dd8bb8ae5e38e7118b5de181d88f9b1981128995cb25b48fce7fa577a9.
- `.\.venv\Scripts\python.exe -m pytest -q`: **8 passed in 0.27s**.
  No audit implementation changed in this session.
- Local evidence: results/notebook_execution_validation_2026-11-13.json and
  results/notebook_environment_2026-11-13.txt (resolved pip freeze snapshot).
  Optional requirements pin direct dependencies, not the full environment.

**Verification issues resolved:** An early check compared canonical LF JSON
bytes with the Windows CLI artifact's CRLF bytes and reported a different
hash. The final notebook explicitly distinguishes canonical and original-file
hashes and compares parsed JSON content; no data or scientific definition was
changed. One verification harness attempt used nbformat.from_dict on serialized
notebook JSON, leaving cell source as lists; replaced it with nbformat.reads.
These failed verification attempts did not complete the task; only the two
successful final fresh-kernel executions above support NOTE-01 completion.
Initial kernel runs emitted non-fatal Windows event-loop/profile warnings;
final verification used a Windows selector loop and local runtime directories
under results/.

**Current work and checklist:** NOTE-01 complete with execution evidence.
DATA-01 remains in progress; DATA-02 remains blocked on lineage/timing
evidence. No research milestone, reconciliation or run validation is complete.

**Decisions:** D007 records notebook/module separation and preservation of
the existing EDA. No model training, degradation implementation, counter
conversion, timestamp imputation, row exclusion or evaluation split created.

**Problems/blockers:** Kaggle release and author processing provenance remain
unknown; source/database mismatch and missing source clocks are unexplained.
Dataset assumptions in the existing EDA were not silently adopted.

**Next recommended action:** Review the notebook tables together, then carry
out the smallest source-to-database reconciliation diagnostic, beginning with
DoS and mixed-schema Probe. Propose comparison keys/multiplicity handling
before making run/group or eligibility decisions.

## 2026-11-13 — Optional notebook package metadata fix

**Problem and completed fix:** User ran the notebook with rocm-jupyter
(Python 3.11.14, SQLite 3.51.0). Provenance display incorrectly required pytest
metadata and stopped with PackageNotFoundError. Updated only notebook setup
and instructions: optional tool lookup now catches PackageNotFoundError,
reports absence, and notes a non-project interpreter without blocking the
standard-library audit. No packages were installed into rocm-jupyter.

**Tests executed and results:** Ran all seven code cells sequentially in a
fresh process using the user's actual rocm-jupyter/python.exe. Confirmed pytest
is absent, missing-package reporting succeeds, the inventory matches the prior
report as JSON content, and input hashes remain unchanged. This verifies the
actual interpreter, not an interactive rocm kernel/UI session. Separately
executed all seven cells in a fresh project kernel from notebooks/ and saved
updated notebook outputs. `python -m pytest -q` in the project .venv:
8 passed in 0.64s. Notebook schema validation passed.

**Checklist and decisions:** NOTE-02 complete with regression evidence.
Missing optional development metadata must not prevent descriptive auditing;
environment differences are disclosed. Research definitions, audit module and
all pending dataset-validation statuses remain unchanged.

**Problems/blockers:** Original provenance/lineage questions remain; no new
dependency is needed in the user's notebook environment for this fix.

**Next action:** Reload the notebook from disk, restart the selected kernel,
and Run All. Then review the count differences before reconciliation.

## 2026-11-13 — Review of user's saved notebook results

**Completed work:** Inspected the user's saved notebook outputs without
changing or rerunning the notebook. All seven substantive cells have outputs
(execution counts 2-8), no saved errors, plus one harmless empty cell. Saved
environment is rocm-jupyter Python 3.11.14 / SQLite 3.51.0. Validated notebook
format and compared the saved canonical report hash, 25 schema rows, all six
category comparison rows, and all nine incomplete-timestamp source rows to a
fresh read-only inventory. Every comparison passed and all 50 input hashes
remained unchanged. Saved local review evidence under results/.

**Results/interpretation:** Confirmed 45,244 database rows, 50,213 source
objects and 44,452 timestamped source objects. The total difference of 4,969
is concentrated in Benign (934), DoS (3,466) and Probe (569). Missing clocks
could explain the Benign/Probe count differences, but no record-level lineage
has been proven. DoS remains inconsistent with a simple timestamp-presence
filter. Fresh-kernel history cannot be inferred solely from saved counters.

**Files modified:** Findings document, DATA-01 evidence in checklist and this
log. Notebook and source data preserved. No new methodological decision.

**Checks/tests:** Notebook schema, saved-output assertions and fresh input
integrity checks passed. No pytest suite rerun; no code changed.

**Current work/blockers:** DATA-01 remains in progress, DATA-02 blocked on
source lineage/timing validation. No research task marked complete from this
review. Kaggle release and processing provenance remain unresolved.

**Next action:** Diagnostic source-to-database reconciliation, starting with
DoS and mixed-schema Probe, reporting unique/ambiguous/unmatched occurrences.

## 2026-11-13 — Exact candidate reconciliation

**Objective and method:** Read current instructions/tracking, inspect DoS and
Probe schemas/subtypes, then implement one diagnostic task. Declared two
comparison keys before implementation: 16 exact numeric radio fields and
those fields plus five metadata fields. No labels in keys, PMI conversion,
numeric tolerance, missing-value filling or candidate consumption. All six
classes are included as context; DoS/Probe are the focus.

**Completed work/files:** Added src/reliability/reconciliation.py and
tests/test_reconciliation.py. Added independently executable notebook
notebooks/02_source_database_reconciliation.ipynb (16 cells, seven code cells),
preserving the user's saved notebook 01. Added docs/reconciliation_findings.md
and updated README, notebook/test instructions, dataset inventory, decisions
and checklist. Detailed occurrence/group output is local ignored JSON at
results/radio_reconciliation_2026-11-13.json (44,223,398 bytes).

**Actual evidence:** Radio-only comparison has 44,819 unique candidate pairs
and 425 occurrences per side in 61 repeated-key groups; 4,969 source records
have no candidate, and every database row has at least one radio candidate.
Radio-plus-metadata comparison has 43,704 unique candidate pairs, 748 source
records with no candidate, 5,761 source records with unusable keys and 1,540
database rows with unusable keys. No ambiguity remains under that stronger
key; neither profile has a unique-pair folder/category disagreement.

The 1,540 DoS radio-only candidates are tcp-ack_hping3.txt (648),
tcp-syn_hping3.txt (768) and tcp_test.txt (124). These sources lack timestamp
and UE metadata, so the corresponding populated database metadata cannot be
validated here. The 748 timestamped tcp_npig.txt source records have no exact
radio candidate. Probe portscan_udp.txt contributes 573 unique candidates
under both keys and 569 radio-unmatched, metadata-free source records. The
Benign unmatched radio records are benign_10.txt (900) and benign_test.txt
(34). These are exact observed correspondences, not author processing claims.

**Tests executed and results:**

- `.\.venv\Scripts\python.exe -m pytest -q`: initial matching logic suite
  17 passed in 0.44s; after read-only end-to-end and output-path tests,
  final suite **19 passed in 0.44s**.
- `.\.venv\Scripts\python.exe src/reliability/reconciliation.py --root data/radio --output results/radio_reconciliation_2026-11-13.json`: succeeded, all occurrences accounted for and input hashes unchanged.
- Notebook 02 validated with nbformat, then executed all seven cells in a
  fresh project kernel from notebooks/. Its complete report matched CLI JSON.
  Saved executed outputs; notebook 01 hash was unchanged.
- Executed all notebook 02 code cells in a fresh process using the user's
  actual rocm-jupyter Python 3.11.14 / SQLite 3.51.0. Complete report content
  matched CLI and the project-kernel result. This is interpreter verification,
  not an interactive rocm UI session. No packages installed in that environment.
- All actual executions verified the extraction manifest and all 50 input
  hashes before/after. Detailed report SHA-256:
  dab06dc5e92f5ed526a07fc4c7e7e89ddfa5575ae3ec523ad662ea7be8962c25.
  Matching module SHA-256:
  45a8de2d300ab6c579bed20c30c6873f4720d32df066f7f9dad9fc61ca32fea6.

**Checklist and decisions:** RECON-01 complete against diagnostic acceptance
criteria; DATA-01 remains in progress and DATA-02 remains blocked on clock
provenance/independence evidence. D008 documents comparison semantics. No run
IDs recovered, no research milestone complete, and no eligibility/split rule
approved. Model/calibration and degradation ownership remain with teammates.

**Problems/blockers:** Candidate matches do not provide an authoritative
capture manifest. Unverified metadata for the 1,540 DoS rows prevents treating
all database timing as source-observed. Kaggle release, source processing,
PMI representation correspondence and independent-run boundaries remain open.

**Next recommended action:** Review notebook 02 and investigate metadata
provenance for those DoS rows. Inspect within-source/per-UE ordering, overlaps
and reporting cadence only as diagnostics with explicit clock assumptions;
seek Gaurav's review before fallback grouping or population restrictions.

## 2026-11-15 — Review of user's saved reconciliation outputs

**Completed work:** Read instructions/checklist/progress and reconciliation
findings. Inspected notebook 02 saved outputs: seven substantive code cells
numbered 1-7, no errors, one empty trailing cell. Validated notebook format.
Environment output is rocm-jupyter Python 3.11.14 / SQLite 3.51.0.

**Checks executed/results:** Ran a fresh independent read-only reconciliation.
The complete report matches the prior CLI JSON, canonical SHA-256
dab06dc5e92f5ed526a07fc4c7e7e89ddfa5575ae3ec523ad662ea7be8962c25.
Saved summary rows, both category tables, both DoS/Probe file tables and all
three metadata-gap rows agree exactly. Saved code hash matches the current
module. All 50 input hashes unchanged; notebook SHA-256 also unchanged.
No notebook re-execution or pytest rerun; no implementation changed. Review
evidence: results/reconciliation_saved_output_review_2026-11-15.json.

**Interpretation:** 43,704 database rows agree uniquely on radio plus observed
metadata; 1,540 DoS radio candidates lack supporting source metadata. The
4,969 radio-unmatched source records explain the count difference. All 425
radio-ambiguous occurrences have stronger-key unique candidates. Unusable
keys must not be interpreted as absent records, and candidate agreement is
not evidence of independent runs or author processing provenance.

**Files/status:** Updated reconciliation findings, RECON-01 evidence and this
log; preserved notebooks and raw data. RECON-01 stays complete for its
diagnostic scope. DATA-01 remains in progress; DATA-02 remains blocked on
clock/capture provenance. No additional task marked complete.

**Decisions/open questions:** No new methodological decisions. How the 1,540
DoS rows acquired populated metadata and which boundaries identify independent
captures remain unresolved, as does the exact Kaggle release.

**Next recommended action:** Investigate source/processing metadata for those
DoS candidates, then audit per-source/per-UE timing and overlaps descriptively.
Do not infer missing clocks, restrict the population or freeze split groups
without supporting evidence and Gaurav's review.

## 2026-11-15 — Timing, overlaps and metadata provenance

**Objective:** Perform the authorized next diagnostic without choosing time
units, gap thresholds, independent runs or eligibility restrictions. Read
current instructions/tracking and inspect original source/database fields.

**Completed work:** Added src/reliability/timing_audit.py,
tests/test_timing_audit.py and independently executable notebook 03 (17 cells,
eight code cells). Added docs/timing_findings.md and docs/provenance_sources.md;
updated README, notebook/test instructions, decisions and tracking. Preserved
the user's notebooks 01/02 and all raw inputs. Artifact:
results/timing_audit_2026-11-15.json (2,085,273 bytes).

**Method/actual observations:** Group descriptively within each source path
by cellid/ue_id/rnti, retaining original order. All 50,213 source records are
accounted for: 44,452 in 88 usable identity groups, 5,761 with unavailable
identity. No backward or repeated timestamps within those groups. Each has
median positive step 1,000 raw units; largest positive step 143,993. Compared
102 exact-identity cross-file pairs; zero overlapping raw timestamp ranges.
Neither these 88 groups nor the lack of overlap establishes independent runs.

For all 1,540 database rows whose unique radio candidates lack source
metadata, the actual database timestamp/ue_id/cellid/in_sync tuple coincides
with exactly one observation in another source file. Counts by other file:
icmp_nping.txt 487, slowloris2.txt 529, udp_nping.txt 524. None agrees on all
16 radio values. This is an observed association warning, not proof of copied
or synthetic metadata. An initial exploratory probe used the observed constant
cell ID; the implemented/tested final comparison uses each actual database
cellid and in_sync, with no assumed constant or wildcard.

**Provenance investigation:** ZIP directory inventory contains 320 files and
no script/document/manifest filename candidates under the stated search. JSON
and CSV contents were not exhaustively searched. Reviewed the descriptor,
author dataset pages and the linked author repository read-only, pinned at
add5de9fe2a1491a8d0bf4ccf0239c553c286634. Its radio notebook (82 cells) and
higher-layer notebook (91 cells) use legacy names and do not explain the
current summary metadata construction. External code was not executed.
Source links, blob IDs and review limits are in docs/provenance_sources.md.
Asked the user asynchronously whether revision/export notes are available;
no answer was assumed and no messages to teammates/authors were sent.

**Tests/checks executed:**

- `.\.venv\Scripts\python.exe -m pytest -q`: **28 passed in 0.43s**.
- `.\.venv\Scripts\python.exe src/reliability/timing_audit.py --root data/radio --archive data/archive_2.zip --output results/timing_audit_2026-11-15.json`: succeeded.
- Notebook 03 nbformat validation and fresh project-kernel execution from
  notebooks/: all eight code cells completed without errors; full report
  content equals CLI. Saved executed outputs; notebook 01/02 hashes unchanged.
- Executed all eight code cells in a fresh process with the actual
  rocm-jupyter Python 3.11.14 / SQLite 3.51.0; full timing report equals CLI
  and project-kernel content. This is interpreter verification, not a rocm UI
  session. All actual runs verified extraction-manifest/input hashes and
  source coverage. No packages installed in that environment.
- Report SHA-256:
  1327941727dc090df7404c6558d5fa0a988fbffb75cd7dedb81da2cec6508cdf.
  Timing module SHA-256:
  17c13af7fc7f68871aaf73274292c55b7ad562be0c679bb5830b419eff28f5e5.

**Status/decisions:** TIME-01 complete for its descriptive acceptance gate.
DATA-00/01 remain in progress; DATA-02 remains blocked on authoritative
clock/capture provenance. D009 documents raw timing and coincidence semantics.
No true run IDs, validated units, rates, exclusions or evaluation groups
created; no milestone marked complete. Teammate ownership is unchanged.

**Problems/blockers:** Kaggle revision, export/merge history and independent
capture manifest remain unavailable. Coincidences cannot authenticate clocks
or identify the processing mechanism. Disjoint exact identities do not prove
statistical independence.

**Next recommended action:** Review notebook 03 and seek the missing exporter/
capture evidence. Draft the evaluation protocol with timing provenance and
fallback grouping/population choices explicitly pending Gaurav's review;
drafting does not freeze or implement those research definitions. Continue
threat-model documentation while provenance is sought.

## 2026-11-15 — User clarification and projected-clock follow-up

**Clarification:** Gaurav reports no available Kaggle revision and that he is
the first teammate to begin. No team exporter/capture notes are available.
Recorded this without asserting that Kaggle lacks platform versioning. Keep
the content snapshot identified by the already verified 50-file hashes and
mark platform revision unavailable. Do not wait for assumed existing team
artifacts; implementation ownership remains unchanged.

**Completed work:** Added metadata_provenance.py and four synthetic pytest
tests. Appended section 9 to notebook 03, preserving its earlier analysis and
notebooks 01/02. This follow-up projects database timestamps onto the physical
line order of unique radio-candidate sources; it does not label those clocks
source-observed event time. Updated provenance, timing findings, dependencies,
decisions and tracking. No row exclusions or replacement clocks implemented.

**Actual findings:** 1,540 questionable database rows use 1,143 distinct
timestamp/UE/cell/sync tuples, with 397 excess repeat occurrences. Projected
clock steps across the three source files: 760 backward, 776 forward and one
zero. Original source event-time order is not authenticated. Metadata
reassignment/resampling is a possible explanation, not a recovered algorithm.
The earlier zero-reversal result concerned observed clocks in other source
identity groups and remains unchanged; these are separate diagnostics.

**Executed checks:** Project `.venv` pytest: **32 passed in 0.43s**. Updated
notebook schema validated; all nine code cells completed in a fresh project
kernel from notebooks/. All nine also completed in a fresh process using
the actual rocm-jupyter interpreter. The original complete timing report still
matches CLI content, input hashes remain unchanged, and projected counts were
asserted independently. Saved executed notebook and local evidence at
results/metadata_projection_2026-11-15.json. The user's environment was not
modified. A documentation patch initially failed its context check; no files
were changed by that failed patch, and corrected documentation applied.

**Status/decisions:** D010 records hash-identified evidence and bounded
provenance claims. Added PROV-01 in progress: forensic diagnostics are
evidenced, but exact origin and handling of uncertain timing are unresolved.
DATA-00/01 and DATA-02 retain their existing incomplete statuses. No research
task is marked complete merely because an external identifier is unavailable.

**Next recommended action:** Review section 9, then prepare the evaluation
protocol as a concrete draft separating established file evidence from
proposed temporal eligibility and grouping assumptions. Gaurav must approve
those research decisions before implementation; their absence need not block
drafting or continued threat-model documentation.

## 2026-11-15 — Review of updated notebook 03 outputs

**Completed work:** Read instructions/checklist/progress and inspected the
user's saved notebook 03, including section 9. All nine substantive code cells
have outputs (counts 1-9), no errors, and valid notebook format. Saved kernel
is rocm-jupyter Python 3.11.14 / SQLite 3.51.0.

**Checks executed/results:** Fresh read-only build_timing_audit and
summarize_projected_clocks match the prior complete timing and projection
artifacts. Verified saved report and both module hashes, all seven saved data
tables, overlap counters and projected tuple totals. All input hashes remain
unchanged; notebook SHA-256 before/after is
ec7a73bc46869abda007bbcb906394888cb7250d4dd34fdbf7d0d020c9c9e441.
Saved local evidence: results/timing_saved_output_review_2026-11-15.json.
No notebook re-execution or pytest rerun; no implementation changed.

**Interpretation:** The outputs are internally consistent: observed-source
groups have no reversals, while questionable database clocks projected onto
other source-file order have 760 backward steps. The 1,143 distinct metadata
tuples and 397 excess repeats describe 1,540 rows. These are separate evidence
populations, not a contradiction. Neither proves the original processing
mechanism, time units or independent capture boundaries.

**Files/checklist:** Updated findings, PROV-01 evidence and this log; preserved
notebook and raw data. No status advanced: PROV-01 remains in progress and
DATA-02 remains blocked on authoritative provenance/grouping evidence.

**Open questions/decisions:** No new research choices. Unknown metadata origin
and the treatment of uncertain clocks remain explicit; no exclusion, repair
or fallback grouping is approved.

**Next recommended action:** Prepare a concrete draft evaluation protocol
with evidence-backed observations separated from proposed handling of clock
uncertainty and group independence, for Gaurav's review before implementation.

## 2026-11-15 — Evaluation protocol draft v0.1

**Objective/completed work:** The user authorized the concrete protocol draft.
Read tracking, threat model, prior decisions, teammate dependencies and actual
audit findings. Created docs/evaluation_protocol.md with 12 sections and six
explicitly pending choices EP-1 to EP-6. Updated README, dependencies, decisions
and checklist. No Python code, notebooks, raw data or configurations changed.

**Content and proposed choices:** Primary sequence/temporal cohort proposed as
43,704 uniquely source-supported database rows; uncertain 1,540 rows retained
for separate non-temporal diagnostics. Prominently disclosed that this omits
all current single-source DoS ACK/SYN examples from primary temporal coverage.
Proposed source-file/component split proxies with limited independence claims,
report-index windows, training-only preprocessing/CV and validation-only
threshold/policy selection. Proposed numeric defaults (W/stride 10, approximate
60/20/20 group split, three training folds, seed 42) are recommendations, not
an approved configuration. Clock interpretation remains a separate decision.

Defined window/assessment/split-group units, score aggregation, AP versus
trapezoidal PR area, ROC-AUC, NA reasons, full 2-by-3 abstention denominators,
false-positive behavior, paired clean/degraded effects and group uncertainty
limits. Kept all planned no-observation windows in coverage reporting. Separated
offline reference grids from causal policy metadata to prevent an oracle-based
quality claim. Feature groups, model score inputs, calibration and degradation
interfaces remain proposals requiring the responsible teammate's agreement.

**Source checks:** Consulted official scikit-learn documentation for AP,
ROC-AUC, StratifiedGroupKFold and training-only preprocessing. Links are beside
the relevant definitions. No package installation or model framework added.

**Checks executed/results:** Read-only Python document checks passed: 12
numbered sections, six pending decisions, 21 local links across changed
entry-point documents, category counts matching the prior complete
reconciliation report, primary total 43,704 versus full 45,244, and 40 candidate
source files including 10 Benign files. Checked illustrative 2-by-3 table
arithmetic (coverage, retained error, unconditional detection and attack
abstention), not an implementation. Evidence:
results/evaluation_protocol_draft_validation_2026-11-15.json.
No pytest suite rerun for this documentation-only change. These checks do
not establish scientific approval, independent captures or feasible partitions.

**Status/decisions:** D011 records draft preparation without adoption. EVAL-01
is in progress; none of EP-1 through EP-6 is approved and no exclusions, split
manifest, thresholds or window IDs were created. All existing provenance/run
limitations remain. Model/calibration and degradation ownership unchanged.

**Open questions/next action:** Request Gaurav's decision on EP-1 first using
the reviewable cohort table and ACK/SYN tradeoff. Then review grouping/clock
assumptions and window/split/metric choices sequentially. After approval, add
only the smallest necessary manifest-validation utility and tests; do not
start model training or treat the draft as a frozen protocol.

## 2026-11-15 — EP-1 approval recorded

**User decision:** Gaurav explicitly selected the recommended EP-1 timing
separation. Primary temporal eligibility is 43,704 unique source-metadata
candidate rows; 1,540 uncertain-clock rows remain for separate non-temporal
diagnostics, with the DoS ACK/SYN coverage loss expressly acknowledged.

**Files changed/status:** Updated protocol to draft v0.2 with only EP-1
approved, decisions.md D012 and EVAL-01 checklist evidence. EVAL-01 remains
in progress; EP-2 through EP-6 and all teammate interfaces remain unapproved.
No data deletion, cohort extraction, grouping, split, window, threshold,
clock conversion or model implementation occurred. Historical draft v0.1
validation evidence remains a record of that earlier document state.

**Evidence/checks:** Re-read current instructions/tracking and proposal before
recording approval. The existing full reconciliation report has 40 source
files with strong candidates (10 Benign) and 43 with any database radio
candidate (including the three secondary-only DoS sources). These are
prospective file groups, not independent runs. Document approval-state and
cohort arithmetic checks are recorded in
results/evaluation_protocol_ep1_approval_2026-11-15.json. No pytest suite
rerun for this documentation-only approval update.

**Next action/open question:** Review EP-2: keep each whole source file's UE
streams/windows together as a provisional split group, merging files when
capture linkage is established, and restrict claims to a source-file benchmark
until independence is verified. Alternative: defer performance evaluation
until authoritative capture IDs are available. No group rule is adopted yet.

## 2026-11-15 — EP-2 approval and cohort/group manifest

**User decision:** Gaurav explicitly selected the recommended provisional
source-file grouping. Whole source files keep all their UE streams, segments
and windows together; files merge if capture linkage is established. Results
remain source-file benchmarks, not validated independent-run evaluations.
EP-3 through EP-6 remain pending. D013 and protocol draft v0.3 record this.

**Completed work:** After recording the authorized scope in commentary,
implemented only EP-1/EP-2 membership/group materialization in
src/reliability/cohort_manifest.py, with six synthetic tests. Input is the
previously validated reconciliation artifact, checked against actual input
file sizes/hashes. The builder retains all database rows and original source
path/line references; refuses unresolved/contradictory unique candidates;
groups whole files; and supports transitive merges only from supplied
evidence-bearing links. No capture links are established/applied currently.

**Actual artifact:** results/cohort_group_manifest_ep1_ep2_2026-11-15.json
contains all 45,244 database rows: 43,704 primary_temporal and 1,540
secondary_non_temporal_only. There are 43 provisional file groups overall,
40 with primary rows. Stable group IDs identify source-file components, not
true independent runs. No split/window IDs, timestamp conversion, selection
thresholds, filtering of raw inputs or model implementation were added.

**Tests/checks executed:** `.\.venv\Scripts\python.exe -m pytest -q` initially
37 passed in 0.47s; after adding contradictory-profile/reference checks,
final **38 passed in 0.46s**. Executed cohort_manifest.py with data/radio and
the prior reconciliation artifact; output succeeded. Independent reconstruction
using the final code matched the saved manifest. Checked unique accounting of
45,244 rowids, exact approved cohort sizes, file-to-group consistency, group
counts and absence of split/window/timestamp assignments. All 50 input hashes
were unchanged. Evidence: results/cohort_manifest_validation_2026-11-15.json.

**Files/status:** Updated protocol, decisions, checklist, README/test usage
and this log. Added tested module/tests and local ignored manifest. MAN-01 is
complete against its limited acceptance gate. EVAL-01 remains in progress;
true-run recovery and capture independence remain unresolved. Original
notebooks and model/degradation ownership unchanged.

**Next action/open question:** Review EP-3: recommended initial report-index
windows and raw timestamp diagnostics, postponing physical seconds/dates/rates;
alternative is an explicitly provisional Unix-millisecond/UTC interpretation
of source-supported clocks. Neither choice authenticates the 1,540 excluded
temporal rows or approves windows/split proportions/metrics automatically.

## 2026-11-15 — EP-3 approval and EP-4 coverage preview

**User decision:** Gaurav selected raw units and report order first. Recorded
EP-3 approval as D014 and protocol draft v0.4; no Unix-millisecond conversion,
calendar-date claim or per-second/physical-time metric is approved. EP-4
through EP-6 remain pending. Existing source/clock limitations persist.

**Work/checks:** Read instructions/tracking and current proposal. A read-only
preview traced approved primary manifest rows to actual source lines and
counted per-file/cell/UE/RNTI stream lengths. All 43,704 rows are accounted for
in 87 identity streams across 40 files. A proposed length/stride of 10 reports
would give 4,332 full windows plus 74 tails (384 reports); 34 files have a tail,
and one stream has eight reports. There are no unselected nonblank rows inside
the retained primary spans of these source files; no deleted interval was
silently bridged in this preview. No gap-splitting policy is applied.

Verified all 50 input hashes. Saved results/window_policy_preview_2026-11-15.json.
These are conditional counts, not implemented windows, models or scored cases.
No Python implementation changed, and no pytest suite was rerun. Updated only
protocol/decision/checklist/progress documents and local review evidence.

**Status/open question:** EVAL-01 remains in progress. EP-4 needs Gaurav's
evaluation-grid decision and explicit model compatibility discussion with
Nitendra. Retaining partial tails matters for coverage: unsupported tails
would be SHORT_WINDOW abstentions and can affect file-level decisions under
the still-proposed conservative EP-6 aggregation. No tails are dropped.

**Next action:** Review a ten-report, stride-ten, source-ordered window grid
with retained partial tails, no inferred seconds or additional gap cuts, and
explicit abstention for unsupported short inputs. Nitendra's encoding/model
support remains a separate pending interface agreement; split fractions and
operating metrics are not approved by a window decision.

## 2026-11-15 — EP-4 approval and primary window manifest

**User decision:** Gaurav explicitly approved the ten-report grid with
retained tails. Recorded D015 and protocol draft v0.5. EP-1 through EP-4 are
approved; EP-5/EP-6 and model-specific partial-input encoding remain pending.

**Completed work:** Added src/reliability/window_manifest.py and seven
synthetic tests. Materialized only primary temporal report references:
results/window_manifest_ep1_ep4_2026-11-15.json. It preserves each source/
cell/UE/RNTI stream's physical order and inherited file group, uses stable
content/line-reference window IDs and retains all partial tails. It validates
snapshot hashes, source-line coverage, label consistency, clock monotonicity
and whole-file group consistency. It refuses interior exclusions rather than
gluing fragments. No gap-based run inference, time conversion, padding,
predictions, operating thresholds or split assignments were added.

**Actual evidence:** 4,332 full windows and 74 tails (384 reports), 4,406 windows
total, account for all 43,704 primary rows exactly once in 87 identity streams
from 40 provisional file groups. The 1,540 secondary rows remain retained in
the cohort manifest outside temporal windows. Partial windows retain their
actual expected report count; SHORT_WINDOW is a conditional unsupported-input
reason, not a prediction emitted by this builder.

**Tests/checks:** `.\.venv\Scripts\python.exe -m pytest -q`: **45 passed in
0.59s**. Executed window_manifest.py on actual inputs successfully. Separate
checks verify unique row coverage, tail arithmetic, deterministic reconstruction,
parent group consistency, input hashes and no split/prediction fields. Evidence:
results/window_manifest_validation_2026-11-15.json.

**Files/status:** Added module/tests/local manifest and updated protocol,
decisions, README/test usage, checklist and this log. WIN-01 completes its
limited manifest gate. EVAL-01 remains in progress; independent capture/run
validation remains unresolved. No model/calibration/degradation work assumed.

**Next action/open question:** Review EP-5's proposed approximate 60/20/20
group split, seed 42 and three grouped training-CV folds. The primary cohort
has 40 provisional groups including ten Benign; a 24/8/8 primary allocation
would have approximately six/two/two Benign groups. Such limited validation/
test benign support cannot support very low-FPR claims. No partitions selected.

## 2026-11-15: EP-5 approval and reproducible grouped partitions

**Current milestone:** M2. Gaurav approved the approximate 60/20/20 grouped
split, seed 42 and three grouped training-only CV folds. Recorded D016 and
protocol v0.6. EP-1 through EP-5 are approved; EP-6 remains pending.

**Completed task/deliverable:** Added src/reliability/split_manifest.py and
seven synthetic tests. Materialized results/split_manifest_ep1_ep5_2026-11-15.json
without fitting transformations/models or using model scores. Primary groups
are 24/8/8 (Benign 6/2/2); one secondary-only group in each partition gives
full counts 25/9/9. All 45,244 rows and 4,406 windows inherit their group's
partition; all 74 tails remain. Training/validation/test primary row counts
are 26,455/8,306/8,943; secondary counts are 768/648/124.

**Tests and evidence:** `.\.venv\Scripts\python.exe -m pytest -q` returned
**52 passed in 0.66s**. Executed the split CLI documented in README.md.
Separate actual-data checks confirmed byte-identical reconstruction, all 50
input snapshot hashes, disjoint complete outer groups, row/window inheritance,
and training-only disjoint CV with both binary classes. Saved
results/split_manifest_validation_2026-11-15.json. Split artifact SHA-256:
2a10a1d330f03e271669bf94e8ddb9d6a6c4111bca1a138e637b94edf0be4a66.

**Files/checklist:** Added split module/tests and local result/validation JSON;
updated README.md, tests/README.md, evaluation protocol, decisions, checklist
and this log. SPLIT-01 meets its acceptance gate. EVAL-01 remains in progress;
EVAL-02 has not started. Existing notebooks and raw inputs were not edited.
Git status cannot be inspected because this directory is not a Git repository;
code and artifact hashes supply local identity until Git is initialized.

**Dependencies/limitations:** Source-file separation does not establish
capture independence. Primary fitting CV fold 1 lacks DoS; other folds also
have family gaps. Both binary classes are supported, but complete multiclass
CV is not established. Secondary test coverage is tcp_test.txt only and has
no ACK capture. Two Benign validation/test groups cannot support very low-FPR
claims. No favorable partition redraw was performed. Model score/partial-input
and degradation interfaces still require Nitendra/Marco agreement.

**Next action/open question:** Review EP-6 binary metrics, score/decision
aggregation, validation-only threshold utility and abstention accounting in
docs/evaluation_protocol.md sections 5 and 7-9. Required quality KPIs, numerical
cutoffs and coverage/security budgets remain later ABS-01 decisions. Implement
one evaluation utility only after its definitions are approved.

## 2026-11-15: EP-6 approval and outcome-accounting component

**Current milestone:** M2. Gaurav selected Approve EP-6 definitions
(Recommended). D017 and protocol v1.0 record the binary endpoint, aggregation,
primary file-proxy AP/secondary ROC-AUC/window reporting, validation-only
equal-class utility and full two-by-three abstention accounting. Required
quality KPIs, numerical cutoffs/security budgets and teammate interfaces remain
explicitly gated. Optional bootstrap settings remain proposals.

**Completed task/deliverable:** Added src/reliability/outcome_metrics.py and
tests/test_outcome_metrics.py. This pure component consumes explicit binary
truth and BENIGN/ATTACK/ABSTAIN outcomes. It preserves class/population counts,
reports full and accepted denominators, separates unresolved attacks and gives
explicit NA reasons for unsupported ratios. Empty/one-class inputs remain
visible; invalid labels, unequal lengths and missing/unknown outcomes fail.
It reports fixed-outcome utility without selecting a threshold. Callers must
supply every planned labeled unit; completeness against an external manifest
requires a later adapter. This is an internal helper, not a teammate contract.

**Tests executed/results:** `.\.venv\Scripts\python.exe -m pytest -q`
returned **65 passed in 0.64s**, including 13 new cases. Hand-computed examples
exercise every confusion-table cell, all-abstain/empty/one-class inputs,
invalid inputs and order invariance. Replacing a missed attack with abstention
improves retained error while leaving full detection/utility unchanged: the
test guards against claiming that selection effect as improved security.
Saved results/outcome_metrics_validation_2026-11-15.json with synthetic inputs,
report, executed-test record and code/test/protocol hashes. These are formula
checks, not measured model results. Checklist column/ID checks also passed.

**Files/checklist:** Added the module/tests and local validation JSON; modified
README.md, tests/README.md, docs/evaluation_protocol.md, docs/decisions.md,
planning/checklist.md and this log. EVAL-01 meets its review gate because all
six choices are approved and interfaces explicitly gated. COUNT-01 is complete;
EVAL-02 remains in progress. Raw data, existing manifests and notebooks were
not modified. No training, prediction ingestion, quality-policy execution,
ranking, window aggregation or threshold search was performed.

**Dependencies/open questions:** Nitendra's score direction/type and short-input
support, Marco's observable quality metadata and paired scenarios, and ABS-01
quality KPIs/cutoffs/security budgets remain pending. Capture independence and
small Benign support limitations still apply. No additional approval is needed
to implement the already approved metric formulas as isolated helpers.

**Recommended next task:** Implement and test binary AP/ROC-AUC on explicitly
scored units, with ties, absent-class NA reasons and score-availability counts.
Keep empirical score ingestion gated on the producer interface. Continue with
aggregation and validation-only threshold selection as separate small tasks.

## 2026-11-15: Scope confirmation and evidence-grounded threat-model draft

**Current milestone/next task:** M1, TM-01. Following Gaurav's scope check,
prioritized the threat model over more evaluation code. Gaurav authorized
continuing. Completed evaluation definitions and dataset support work remain
within his workstream; models/calibration and degradation/playback retain
Nitendra/Marco ownership.

**Work completed:** Replaced the initial docs/threat_model.md skeleton with
v0.2, an evidence-grounded review draft. It identifies protected interests,
the offline observation boundary, evidence E1-E5, trust boundaries B1-B6,
bounded attacker capabilities, separate telemetry failure conditions,
assumptions A1-A7 and risk-to-evaluation mappings R1-R8. It incorporates the
approved protocol, primary ACK/SYN coverage restriction, raw-clock constraint,
provisional capture independence and small Benign support. It distinguishes
scenario labels from exploit outcomes and provenance anomalies from malicious
tampering. No deployed topology, E2 realism, new attacker capability or
performance result is asserted.

**Files created/modified:** docs/threat_model.md, docs/decisions.md (D018
preparation record, not methodological approval), planning/checklist.md,
planning/team_dependencies.md, README.md and this progress log; added local
results/threat_model_draft_validation_2026-11-15.json. Corrected the stale
team-dependency statement that EP-1 through EP-6 were still pending; producer
interfaces remain unagreed. No Python, notebooks, raw data or existing result
manifests were edited.

**Checks executed/results:** Python document-consistency checks passed:
eight sections; complete evidence/boundary/assumption/risk IDs; 25 local links;
population counts agree with saved cohort; Benign 6/2/2 agrees with saved
split; checklist IDs/columns and in-progress TM-01 state verified. Saved
validation includes document and parent-artifact hashes. These checks validate
document consistency, not deployment facts. No pytest rerun was needed for
this documentation-only change; the previous code run was 65 passed in 0.64s.

**Checklist/open questions:** TM-01 remains in progress because the draft is
unreviewed and deployment/capture facts remain unresolved. Existing protocol
approval does not approve this threat-model draft. Need Gaurav's review of
the bounded offline model, capability exclusions and factual limits. There
are no available team capture/export notes to assume or repeatedly request.

**Recommended next step:** Review v0.2 and record any corrections/acceptance
without treating unavailable evidence as verified. Then prepare the dedicated
abstention-policy draft, leaving required KPIs, numerical quality cutoffs and
security/coverage budgets pending and teammate interfaces proposed.

## 2026-11-15: Threat-model acceptance and abstention-policy specification

**Current milestone:** M1/M4. Gaurav explicitly accepted the bounded threat
model and stated limitations. Recorded D019 and threat_model.md v1.0. The
reviewed offline model does not establish deployment topology, specific
attacker privileges or capture independence. TM-01's bounded analytical review
gate is satisfied; M1 and remaining provenance/capture tasks are not complete.

**Completed work/current deliverable:** Created docs/abstention_policy.md
v0.1. It specifies applicability, proposed observable input concepts, approved
EP-6 decision/reporting rules, reason meanings, file aggregation, validation
selection/freeze requirements and future test cases. It proposes AP-1:
minimum completeness across required KPIs, measured at distinct expected
positions before imputation, accepting quality equality at q_min. This is
unapproved. Required KPI/validity contracts (AP-2), security/coverage constraints
and quality-search rules (AP-3), and actual thresholds (AP-4) remain pending.

The draft retains actual tail denominators and unsupported SHORT_WINDOW cases,
separates hidden injection metadata from observable quality, and distinguishes
incomplete experiment configuration from missing quality in configured cases.
No physical-time gate, calibration assumption, numerical cutoff or producer
API is invented. Ranking scores remain distinct from quality-gated decisions.

**Files created/modified:** Added docs/abstention_policy.md; modified
docs/threat_model.md, docs/decisions.md, docs/progress.md, planning/checklist.md,
planning/team_dependencies.md and README.md. Local consistency evidence is
results/abstention_policy_draft_validation_2026-11-15.json. No Python, raw data,
notebooks or existing manifests were changed.

**Checks/results:** Document/link/status checks and saved-window counts are
checked separately in that local validation artifact. No pytest rerun for
this documentation-only change; the previous code suite was 65 passed in
0.64s. Illustrative completeness values are arithmetic examples, not observed
policy performance. No policy execution, threshold selection or empirical
model/degradation evaluation has occurred.

**Checklist/dependencies:** TM-01 complete for the accepted bounded analytical
model. ABS-01 in progress; ABS-02 not started. Nitendra's required inputs,
score semantics and short-input support, and Marco's visible masks/counts and
paired scenario contract remain dependencies. Their implementations remain
theirs. No unavailable capture notes are assumed.

**Next action/open question:** Review AP-1's per-required-KPI minimum and
equality rule, without approving an unknown KPI list or cutoff. Then establish
the smallest supported input contract and predeclare security/coverage
constraints before selecting any numerical quality threshold.

## 2026-11-16: AP-1 approval and completeness calculator

**Current milestone:** M4. Gaurav explicitly approved AP-1 completeness:
minimum observed-valid fraction over required KPIs before imputation, using
actual planned tail counts, with quality equality passing at q_min. Recorded
D020 and abstention-policy v0.2. Required KPIs/validity, producer contracts,
numerical cutoffs and security/coverage budgets remain pending.

**Completed work:** Added src/reliability/completeness.py and
tests/test_completeness.py. The pure helper takes explicit expected position
IDs, required KPI names and observed-valid masks. It retains per-KPI observed,
known-missing/invalid and unknown counts; returns unknown quality for unknown
required metadata; ignores optional KPIs; and rejects duplicate/invalid
configuration, invalid mask values and out-of-grid required entries. Complete
tails use their actual denominator. It selects no KPI list, cutoff or validity
rule, performs no prediction/gating and does not implement a producer API.
Callers remain responsible for pre-imputation validity, provenance and causal
observability. Model support for tails is separate from completeness.

**Tests/results:** `.\.venv\Scripts\python.exe -m pytest -q` returned
**89 passed in 0.71s**, including 24 new synthetic cases. Separate document
checks passed for local links, unique checklist IDs/columns/statuses and
AP-1 approval with remaining gates explicit. Saved synthetic ten-report,
complete-tail, unknown-mask and known-missing examples plus code/test/policy
hashes in results/completeness_validation_2026-11-16.json. These are formula
checks, not measured data quality, model performance or empirical policy results.

**Files/checklist:** Added calculator/tests/local evidence; modified
docs/abstention_policy.md, docs/decisions.md, docs/progress.md,
planning/checklist.md, planning/team_dependencies.md, README.md and
tests/README.md. COMP-01 meets its limited acceptance gate. ABS-01 and ABS-02
remain in progress; configured quality-gate and decision execution are not
complete. No raw files, existing manifests or notebooks changed. Nitendra
and Marco retain all model/calibration and degradation/playback ownership.

**Next action/dependencies:** Prepare AP-2's minimal input/observability
proposal from verified available fields, identifying which requirements need
Nitendra's model/score/short-input agreement and Marco's masks/expected-count
agreement. Do not adopt a required KPI list or producer schema without agreement.
AP-3 constraints/search choices and AP-4 numerical thresholds remain later
gates; no additional AP-1 approval is needed.

## 2026-11-16: AP-2 input and observability proposal

**Current milestone/task:** M4, ABS-01/AP-2. Gaurav authorized preparing the
input proposal. Inspected AGENTS/tracking, policy, internal completeness
helper, protocol handoff concepts, actual cohort/window/split structures and
SQLite column names. Kept model/calibration and degradation/playback ownership
with Nitendra/Marco.

**Deliverable:** Created docs/abstention_input_proposal.md v0.1, an unagreed
review draft. It maps existing window IDs, source/row references, actual tail
counts, groups and partitions to proposed alignment needs. It separates
evaluation truth from policy inputs, identifies operational observability
gaps, and requests producer score/validity/short-input and mask/pairing
decisions. It proposes stable report-position references without adopting a
producer schema. Listed radio-comparison fields are inventory only, not a
required KPI set. Model-specific versus common quality-KPI sets remain a
review question, not an implicit new evaluation choice.

**Checks executed/results:** Read-only Python checks passed: parent-manifest
hash links; 4,406 windows, 74 tails and 40 primary groups; 43,704 unique primary
references; expected report counts and source references; current database
hash matches the cohort snapshot; 25 database column names inspected; 27
local document links; checklist columns/IDs and in-progress policy statuses.
Verified database hash again after schema inspection. Evidence:
results/abstention_input_proposal_validation_2026-11-16.json. These checks
establish local consistency, not deployment observability or producer agreement.
No pytest rerun for documentation-only work; last code suite was 89 passed
in 0.71s. No raw-feature statistics or predictions were computed.

**Files/status:** Added the input proposal and local validation artifact;
updated policy cross-reference, team dependencies, README, D021, checklist
evidence and this log. AP-2 remains pending/unagreed; ABS-01/ABS-02 remain in
progress. No task marked complete on a generated proposal. No Python,
notebooks, raw data or existing manifests modified; no teammate messages sent.

**Next action/dependencies:** Review the proposal with Nitendra (required
inputs/validity, score semantics, partial-input support) and Marco (observable
masks, expected counts and fixed-grid pairing). Record Gaurav/producer agreement
and inspect a small supplied example before implementing adapters. While those
dependencies are pending, Gaurav can consider AP-3 security/coverage constraints
and quality-search options without selecting numerical thresholds. AP-4 still
requires validation evidence; do not fabricate inputs to advance it.

## 2026-11-16: Combined audit notebook requested by Gaurav

**Current milestone/task:** M1 presentation/reproducibility, NOTE-03. Gaurav
requested one new notebook combining audits 01, 02 and 03. This is a packaging
change, not a new experiment or research definition.

**Files created/modified:** Created notebooks/00_combined_dataset_audit.ipynb
with 57 cells, including all 23 nonempty original code cells unchanged.
Added contents/navigation, three sequential parts, source/cell provenance
metadata and a note that historical decision gates do not override current
approved documents. Removed empty cells, demoted Markdown headings and adjusted
restart instructions for continuous execution. Preserved the three originals
byte-for-byte. Updated README.md, notebooks/README.md, planning/checklist.md and
this log. Saved local results/combined_notebook_validation_2026-11-16.json.

**Checks executed/results:** nbformat validation passed. Fresh nbclient runs
using the actual rocm-jupyter kernel completed all 23 code cells from project
root (39.42s) and notebooks directory (44.53s), with no cell errors. Outputs
matched between launch locations; freshly computed inventory, reconciliation
and timing report contents matched their three prior local artifacts. Verified
all original notebook hashes and 50 extracted input hashes unchanged. Local
README links resolve. Evidence records original/combined hashes and runs.
An earlier verification attempt did not produce a completed evidence record;
the recorded final runs above supply acceptance evidence. Kernel history was
disabled for those verification runs because the sandbox cannot write the
external IPython history database; notebook analysis code was not changed.
Host kernel permission/teardown warnings did not become cell errors.

No pytest rerun: reusable Python modules were unchanged; notebook execution
is the relevant check. Last Python suite remains 89 passed in 0.71s. No model,
degradation, threshold selection or abstention-policy execution was added.

**Checklist/dependencies/next action:** NOTE-03 meets its consolidation gate.
AP-2/ABS-01/ABS-02 retain their existing pending/in-progress states. Gaurav may
use the combined notebook instead of running three separate files: select
Python 3.11+, restart once and Run All, without restarting between parts.
Further runs are optional because the combined notebook has fresh saved
outputs. Then resume AP-2 handoff review or AP-3 security/coverage discussion.

## 2026-11-16: Review of Gaurav's saved combined-notebook outputs

**Current milestone/task:** M1, NOTE-03 verification follow-up. Inspected
the user's current notebooks/00_combined_dataset_audit.ipynb without editing
it. nbformat validation passed. All 23 code cells have execution counts 1-23
in order, no error outputs, and unchanged source code matching the three
original notebooks. Original notebook hashes still match their source record.

**Checks executed/results:** Ran a deep copy in a fresh rocm-jupyter kernel
from notebooks/ using nbclient, with history disabled for sandbox execution.
All 23 cells completed without error in 40.95s. Compared every saved stream
and all 31 display MIME bundles to the fresh outputs; all matched. Stream
chunks were concatenated and only Interpreter-path casing was normalized
for Windows. Verified all 50 extracted input hashes before/after against the
cohort snapshot. The saved reports confirm content equality with prior
inventory, reconciliation and timing JSON. Preserved the user's saved
notebook byte-for-byte (SHA-256
047e784bf4c03e33f22c6068b9cc2148a97343a85a16fd93bed2f78d4f1bfd61).

**Interpretation:** Results remain 45,244 database rows versus 50,213 source
objects, 43,704 unique radio-plus-metadata candidates and 1,540 database rows
whose candidate source metadata are missing. Timing has 88 descriptive
identity groups, no tested within-stream reversals and no range overlap in
102 same-identity file-pair comparisons; independence is still unproven.
Questionable projected clocks concern database metadata placed onto source
order, not observed source-event clocks. Historical pending text in earlier
parts does not revoke later protocol approvals.

**Files/status:** Added
results/combined_notebook_saved_output_review_2026-11-16.json and updated
NOTE-03 evidence plus this progress log. No notebook, raw-data, reusable code,
protocol or decision changes. No pytest rerun; fresh notebook execution is
the relevant check. NOTE-03 stays complete; no other task status advanced.

**Next step/open limits:** No notebook correction or rerun needed. Continue
AP-2 producer review or AP-3 security/coverage discussion. Timestamp semantics,
capture independence, producer agreements and numerical quality parameters
remain unresolved as already documented.

## 2026-11-16: GitHub/Drive handoff preparation requested by Gaurav

**Current task:** HAND-01, preparatory M6 handoff. Gaurav asked what to push,
what to share via Drive and how to orient teammates. Inspected the file tree,
ignore rules, status, dependency/setup documents and local artifact sizes.
Confirmed this workspace is not a Git repository; no Git initialization,
commit, remote action, upload or teammate message was performed.

**Deliverables/files:** Added docs/handoff.md with explicit GitHub allowlist,
new-versus-existing-repository instructions, Drive restoration/setup commands,
artifact precedence, supported completion states, limitations, walkthrough and
owner-specific next actions. Created ignored handoff/ containing
AAI590_shared_artifacts_2026-11-16.zip, handoff_package_manifest_2026-11-16.json,
SHA256SUMS.txt and local package_validation.json. Upload ZIP, inventory and
checksums when ready; package_validation.json is an additional local record.
Added /handoff/ to .gitignore. Updated README, data/results README explanations,
checklist and this log. Root legacy EDA notebook remains local/preserved and
outside the initial reviewed publish allowlist.

**Checks executed/results:** Bundle size 9,964,936 bytes (about 9.96 MB),
with 51 selected-radio files (50 audited inputs plus extraction manifest) and
30 existing result artifacts. Payload before compression: 109,776,924 bytes.
Verified all 50 inputs against cohort hashes, ZIP CRC, every packaged payload
SHA-256 against inventory and unchanged source files after packaging. Included
code/test/notebook/core-method identities in the inventory; Git commit remains
unavailable until publication. Excluded the 25,101,375,790-byte original archive,
environments and model artifacts. ZIP SHA-256:
20aa778189ed7fadd05bb5ae5cb08a62cd8a7d85600459b462658d9c4447f00e.
No pytest rerun because no Python/notebook logic changed; previous code run
was 89 passed in 0.71s. Packaging checks do not prove scientific completeness.

**Checklist/dependencies:** HAND-01 remains in progress for Gaurav review and
recording actual sharing details; REPORT-01 and all research gates remain
unchanged. Dataset license/source/revision information is not invented.
The guide distinguishes existing code/audits from missing producer agreements,
model/degradation implementations and policy settings.

**Recommended next step:** Review the guide and staged-file allowlist, identify
the actual team repository/branch and Drive destination, publish only the
listed code/docs/notebooks, and share the small artifact bundle with its
checksum plus actual code commit. Walk teammates through the combined notebook
and AP-2 proposal; Nitendra/Marco retain their implementation ownership.

## 2026-11-17: Assignment 4.1 background section draft

**Current task:** BACK-01, report-background drafting. Gaurav supplied the
assignment rubric and Downloads/AAI590 Capstone Project Template.docx.
Read the template's Section 3 Literature Review, narrative-writing and APA 7
requirements, plus its page/style XML. Kept the original DOCX unchanged.
This section addresses existing work, not our methods, parameter choices or
project findings; no model implementation ownership changed.

**Files/deliverables:** Created docs/assignment_4_1_background.md (editable
manuscript), docs/assignment_4_1_review_notes.md (rubric mapping/limits) and
output/pdf/AAI590_Assignment_4_1_Background_Draft.pdf. Updated checklist and
this log. The PDF has two pages of connected literature-review prose and
one Works Cited page, with 12 alphabetical primary references. Covers O-RAN,
signature/anomaly/protocol analysis, radio datasets, random forests, GRU/TCN
development, published intrusion-classification examples, evaluation bias,
calibration and selective prediction. Distinguishes non-radio evidence from
proof of performance on radio telemetry. Does not declare finalized teammate
models, new study settings, novelty or experimental results.

**Checks/results:** Verified publisher/proceedings/author/NIST/arXiv sources,
including Cao/Song study contexts and the Polese final paper's actual
1376-1411 page range. Content checks passed for 12 alphabetical references,
no first-person project-method claims and no internal split/count/cutoff
details. Used ReportLab with embedded Times New Roman and source-template
page/body conventions; this is a standalone section, not a populated full
report. Read final PDF back with pypdf, rendered all three pages with
pdftoppm and visually inspected every page. Removed an almost-empty overflow
page during layout revision. Final layout/text checks passed. Evidence:
results/assignment_4_1_background_validation_2026-11-17.json.

PDF packages were installed into ignored results/assignment41_work/deps
with approved network escalation after sandbox failure. Renderer initialization
and required artifact marker needed approved escalation; the original template
and research environments were not edited. Temporary builder and page PNGs
remain in that ignored work directory. No research pytest rerun because
project code did not change; prior suite remains 89 passed in 0.71s.

**Status/next action:** BACK-01 remains in progress as an unreviewed assignment
draft. Gaurav should review content/citations and any instructor-specific
identification/length expectations before uploading the PDF to Canvas. No
submission occurred. REPORT-01 and empirical research gates are unchanged.
Existing dated Drive bundle is not rebuilt; these new report files are not
represented as part of that earlier snapshot.

## 2026-11-17: Assignment 4.1 revision following supplied review

**Current task:** BACK-01. Gaurav requested two directly relevant O-RAN
sources, a shorter model discussion and closer article-template formatting.
Verified the Fard/Komarov/Wunder arXiv record and full HTML, and the Wen et al.
NDSS-hosted record plus full PDF. The latter is a FutureG 2026 workshop paper
(DOI 10.14722/futureg.2026.23040), not labeled an NDSS main-conference paper.
No literature assumptions were silently adopted as experimental methodology.

**Content changes:** Added the cross-layer detection study with metric-specific
fusion findings, its paired-test qualification and representation/testbed/
clock limitations. Added TELERAN's telemetry-availability motivation and
distinguished acquisition from evaluation under restricted visibility. Shortened
generic IDS, random forest, GRU/TCN and calibration/selective-classification
background; removed Chung, leaving 13 alphabetical references. Retained brief
abstention context because it is Gaurav's approved responsibility, without
promising a confidence-based gate or implemented calibration. All text remains
existing-work background, not our own methods/results or a novelty claim.

**Formatting correction:** The initial template inspection missed section
transitions. Inspection of all sectPr elements establishes one initial column,
three author columns and TWO columns in the main body, with 480-twip/24-point
gutter. Rebuilt the standalone section using that main-body layout, 240-point
columns and 12-point embedded Times New Roman. References flow continuously
through the columns instead of a forced new-page break. Retained hanging
indents/journal-volume italics; measured URL line breaks preserve all full
hyperlink targets. Kept reference entries together within columns. Fixed a
URL overflow and near-empty fourth page during render iterations.

**Files/checks:** Updated docs/assignment_4_1_background.md, review notes,
the PDF at output/pdf/AAI590_Assignment_4_1_Background_Draft.pdf, checklist and
this log. Prior PDF/text preserved in ignored results/assignment41_work/.
Final PDF is three pages; all three rendered pages visually inspected with
no clipping/overlap. Content checks passed for 11 literature paragraphs,
13 alphabetical references and all 13 intact URL targets. Verified unchanged
original DOCX and exact final-section column/gutter settings. Evidence:
results/assignment_4_1_background_revision_2_validation_2026-11-17.json.
Required PDF edit marker and rendering used approved escalation for external
tool settings. No research-code change/pytest rerun or empirical experiment.

**Status/next action:** BACK-01 remains in progress for user/instructor review
and submission. No Canvas upload occurred. Review the revised PDF; source
template remains unchanged, and earlier Drive snapshot has not been rebuilt.
Research scope, approved clock/cohort/split policies, numerical policy settings
and teammate implementation ownership remain unchanged.

## 2026-11-17: Title and author block correction requested

Gaurav identified that the section-only PDF omits the template's article title
and member blocks. Reinspected the reference front matter: centered 18-point
title, optional subtitle, then three author columns containing name, program,
school/university and email, followed by the two-column article body. The
revised PDF has not yet been changed in this follow-up. BACK-01 remains in
progress; the missing front matter is a correction still to deliver.

Known member first names are Gaurav, Nitendra and Marco. Requested their full
names and desired USD emails, with first-name-only formatting available if
preferred. Use the existing project working title unless Gaurav supplies a
replacement. Do not invent surnames or addresses. Next action after that
input is to add the title and three member blocks, preserve the literature
content and visually check the new pagination before delivering the PDF.

## 2026-11-17: Title and supplied author names added

Gaurav requested names only and supplied Gaurav SS, Marco Gonzalez Ortiz and
Nitendra Tiwari. Added docs/assignment_4_1_front_matter.json with those exact
names and the existing working project title/subtitle. Generated
output/pdf/AAI590_Assignment_4_1_Background_With_Title_and_Authors.pdf with
centered 18-point title, 14-point subtitle and three name blocks above the
two-column literature review. No email addresses or affiliations invented.

The old PDF could not be overwritten (PermissionError), so the corrected
version uses a new filename; verified the old PDF remains unchanged. The
literature Markdown is byte-identical to revision 2. Adjusted front-matter
and reference paragraph spacing to avoid a nearly empty fourth page, retaining
12-point body/references and all 13 complete reference hyperlink targets.
Final version is three pages. Rendered and visually inspected all three pages;
verified title/subtitle, supplied names exactly once on page 1, no email,
front matter before Section 3, reference targets and unchanged manuscript.
Evidence: results/assignment_4_1_background_revision_3_validation_2026-11-17.json.

Updated review notes, checklist deliverable/evidence and this log. BACK-01
remains in progress for review/submission. No research-code or experiment
change and no pytest rerun; document/content/render checks were the relevant
validation. No upload or submission occurred. Next action: review the new
title-and-authors PDF rather than the earlier section-only filename.

## 2026-11-17: Vendor-restricted visibility confirmed as the primary scope

**User decision/current task:** Gaurav selected Yes—vendor-restricted visibility
is primary for the explicit question about reliable intrusion detection with
vendor-restricted telemetry subsets and when to abstain. Recorded D022 as
Gaurav's intended priority, not an asserted team/instructor scope approval.
This session aligns documents/planning; it implements no restriction experiment.

**Changes/files:** Added docs/research_scope.md as the framing reference, with
structural absence distinguished from report failure and unknown provenance.
Updated README, protocol v1.1, threat model v1.1, policy v0.3, AP-2 proposal,
decisions, milestones, team dependencies, handoff notice, checklist and this
log. Shortcut checks now explicitly support evaluation validity; dropped/stale
report conditions are secondary and separately justified. Required K cannot
silently shrink to disguise an unavailable measurement. No real vendor profile,
minimum input set, model/retraining treatment or producer API is adopted.

Added not-started CAP-01 (capability evidence), CAP-02 (restriction protocol
review) and VEND-01 (restricted-visibility evaluation) to the checklist.
Updated M3/M5 priorities and retained ROB-01 as secondary. Foundational
EP-1–EP-6/AP-1 approvals and historical evidence remain; they do not approve
the missing restriction extension. No task completes on this clarification.

**Report alignment:** Updated editable front matter to the working title
Intrusion Detection with Vendor-Restricted O-RAN Telemetry and subtitle
Reliability and Abstention under Limited Measurement Visibility, subject to
team/instructor review. Generated a new three-page PDF:
output/pdf/AAI590_Assignment_4_1_Vendor_Restricted_Telemetry.pdf. Preserved the
three exact member names, unchanged literature text and 13 full reference URL
targets. Updated report review notes; earlier PDFs remain historical. No
methodology/results text was inserted into the existing-work background.

**Checks/results:** 55 local document links, checklist IDs/columns/statuses,
19 unchanged code/test hashes and three unchanged cohort/window/split manifest
hashes passed. Verified unchanged literature manuscript against prior evidence.
Read the new PDF back, checked title/names/13 links and visually inspected all
three rendered pages with no clipping. Evidence:
results/scope_alignment_validation_2026-11-17.json. PDF marker/rendering used
approved escalation. No research pytest rerun because no research code changed;
last suite remains 89 passed in 0.71s. No data/model/policy experiments or
remote messages/uploads. The earlier Drive ZIP was not rebuilt and is
explicitly labeled as a pre-clarification artifact snapshot.

**Dependencies/next action:** CAP-01 is next: prepare a source-backed telemetry
capability inventory with implementation/version/interface context and explicit
unknowns. Hypothetical profiles must be labeled hypothetical. CAP-02 needs
Gaurav review plus relevant Nitendra/Marco agreement before experiments. Their
implementation ownership is unchanged; do not substitute further shortcut or
degradation work for the missing primary capability evidence.

## 2026-11-24: Implemented professor EDA feedback follow up

**Current milestone/task:** M1/M3, EDA-01. Gaurav authorized the focused
descriptive/interpretation update before handoff. Primary scope remains
vendor-restricted visibility; this does not replace CAP-01 or transfer
Nitendra's model/learned-preprocessing work to Gaurav.

**Implementation/files:** Added src/reliability/eda_summary.py and five
meaningful synthetic tests. Computes finite/missing/invalid counts, sample
SD, linear percentiles, median/IQR for 17 audit metrics and per-category
subsets of full/primary/secondary/primary-training populations. Reports
paired BLER correlations by category and primary file, preserving undefined
constant-input cases. Uses existing timing/window diagnostics for raw-step
and window-span distributions. Verifies 50 inputs and artifact relationships,
complete row references and timing coverage; all access is read-only.
CLI output: results/eda_summary_2026-11-24.json.

Created docs/eda_cleaning_addendum.md with actual statistics, interpretations,
cleaning-operation ledger, leakage/semantic limitations and owner-specific
handoff implications. It remains a draft for Gaurav review. Added Part 4 to
notebooks/00_combined_dataset_audit.ipynb, preserving the original 23 code
cells and appending one descriptive cell. Added only Markdown clarifications
to the root legacy EDA, preserving all its code and saved outputs: UTC/date
views are historical/provisional, not adopted EP-3 clock semantics. Original
notebooks 01-03 remain byte-for-byte unchanged. Pre-edit notebook backups are
in ignored results/ with the November 24 date.

**Actual findings:** Full-database pooled BLER r=0.9719, primary r=0.9755,
primary-training r=0.9749; scenario/file associations vary. Only 38 of 40
primary-file correlations are defined, spanning approximately 0.0230-0.9884.
No safe redundancy/feature-dropping claim follows. Training CQI IQR is zero
but range is 13-15. Stored byte measurements are skewed; no rate conversion
is adopted. Primary timing has 87 streams, 43,617 comparable adjacent pairs
(40,075 at raw step 1,000), largest raw step 143,993. Complete-window span
median is 9,000, range 8,998-150,147. No loss/staleness/physical-time cause is
inferred from these spans; secondary clocks stay outside temporal analysis.

**Tests/checks:** Final `.\.venv\Scripts\python.exe -m pytest -q` returned
**94 passed in 1.12s**. Initial new percentile test used strict float equality;
changed its assertion to numerical tolerance without changing the estimator.
Ran CLI on actual inputs successfully. Fresh rocm-jupyter execution from
notebooks/ completed all 24 code cells in 64.81s with no cell errors; full
summary content matches CLI. Verified legacy code/output identity, original
23 combined source cells, three original notebook hashes, notebook format
and 37 document links. Evidence:
results/eda_feedback_notebook_validation_2026-11-24.json. Notebook kernel-history
was disabled for sandbox execution as before. Existing raw data and fixed
manifests remain unchanged. No model, feature selection or policy experiment.

**Tracking/docs:** Updated D023, checklist, README/notebook/test usage,
handoff notice and audit-findings cross-reference. EDA-01 remains in progress
only for Gaurav's interpretation review; broader DATA-01/provenance and
CAP-01/CAP-02 statuses are unchanged. The dated Drive ZIP was not rebuilt;
current code/notebook regenerates this follow-up from its existing parents.

**Recommended next step:** Review Part 4 and the addendum before handoff;
then resume CAP-01 capability evidence. Agree model/required-KPI and observable
mask contracts with Nitendra/Marco; use training-only fitting for any later
feature-selection/preprocessing decision. No rerun is required to inspect
the already executed combined notebook.

## 2026-11-24: Clarified supplemental Drive handoff

Gaurav asked whether the new Drive folder/upload/restore instructions were
documented. The guide mentioned the follow-up but did not specify the exact
supplemental layout. Added a November 24 EDA update subsection to docs/handoff.md
with the EDA_Update_2026-11-24 folder, two JSON filenames, local source paths,
recipient restore destination and requirement to obtain matching current code.
Updated results/README.md and linked the subsection from the root README.

The original three-file November 16 package stays unchanged; its checksum
does not cover the supplement. No duplicate raw-data upload or archive rebuild
is needed. Added the notebook-presentation issue Gaurav raised as a remaining
review item, separate from successful execution validation. No upload or push
was performed or claimed. HAND-01 remains in progress; other research task
statuses unchanged. Documentation link/filename checks are recorded in the
current session; no code change or pytest rerun.
