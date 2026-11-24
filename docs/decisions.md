# Decision log

## D001 — 2026-11-08: Start with evidence and a threat skeleton

Decision: scaffold tracking and draft the threat model before implementing
analysis. This follows the user's initial instruction to work incrementally.
The workspace contained no data or code, so data-specific implementation
would require invented schema assumptions. Consequence: empirical work waits
for actual files; no results are reported.

## D002 — 2026-11-08: Preserve ownership and provisional interfaces

Decision: document dependencies without implementing Nitendra's modeling or
Marco's degradation. Interface fields are discussion proposals. Evaluation
definitions, threshold objectives, scenario levels and scope changes require
Gaurav's decision; none have been frozen in this session.

## D003 — 2026-11-08: Separate preliminary claims from evidence

Decision: retain October 29 findings in an explicitly unverified evidence
register. Source-run recovery, channel/uplink separation and the search for
same-day benign data stay open. Generated drafts are not treated as reviewed
deliverables, and no empirical task is marked complete.

## D004 — 2026-11-08: Six milestones and a minimal development environment

The user's initialization request explicitly calls for M1–M6. Preserve task
IDs and scope; split prior M5 into paired robustness (M5) and reporting/handoff
(M6). Map every task to a milestone in the checklist; keep status there only.
Use a local virtual environment, an empty `src/reliability` package, pytest
configuration and one pinned direct test dependency. Do not add ML libraries,
placeholder research functions or artificial passing tests. No-test collection
is a setup diagnostic, never evidence of passing implementation tests.

## D005 — 2026-11-13: Extract the current radio modality only

The user supplied the complete local ZIP and asked for selective extraction.
Inspection confirmed a root radio database and Lower_Layer source directories
for all six current classes. Extract those 50 files, preserving member paths,
without overwriting anything. Record selected-file hashes and ZIP metadata.
Leave network and legacy data in the original archive for later targeted
access if needed. This implements the prior modality selection plan; it does
not change the class population, validate independent runs or freeze feature
eligibility. Do not treat file counts as run counts.

## D006 — 2026-11-13: Inventory raw structure before interpreting time/runs

Implement the authorized next step as a standard-library read-only inventory
with deterministic JSON output, extraction-manifest checks and synthetic
pytest fixtures. Report absent versus NULL source fields, raw timestamp
availability and literal label values; do not silently normalize Web Attacks
to Web or assume timestamp units/timezone. The observed source/database row
mismatch and missing source timestamps require lineage investigation before
group construction. Do not discard unmatched records, synthesize timing,
convert counters to rates or freeze run definitions in this session.
These are deferred research decisions for Gaurav after supporting evidence.

## D007 — 2026-11-13: Use the notebook as the research narrative

The user approved creating notebooks/01_dataset_understanding.ipynb. Keep
reusable auditing in src/reliability/data_audit.py, correctness checks in
pytest, and tables/explanation in the notebook. Recompute from inputs rather
than rely on an earlier kernel or cached results. Record environment and code
hashes; use relative paths and verify fresh-kernel execution from both project
root and notebooks directory. Preserve the existing root-level EDA notebook;
its timestamp interpretation is not adopted without validation.

Folder/category aliases in comparison tables are presentation only, not
approved label remapping. Source reconciliation is a documented next step,
not an implemented or completed experiment. Distinguish canonical UTF-8/LF
JSON report hashes from platform-specific artifact hashes; compare parsed
report content across newline encodings. Research scope and pending approval
of evaluation/grouping rules remain unchanged.

## D008 — 2026-11-13: Diagnostic candidate comparison before provenance claims

The user authorized the next source-to-database reconciliation step. Use
exact shared radio values and a separately reported stronger metadata key;
explain both before implementation. Compare all six current classes without
labels in keys, so DoS/Probe findings have controls and potential category
disagreements remain visible. Preserve duplicate-key multiplicity and report
unusable fields separately from unmatched records. Never allocate arbitrary
pairs or fill timing. Leave PMI representation differences unresolved.

These are explicit diagnostic projections, not approved model inputs,
authoritative run IDs, population restrictions or evaluation definitions.
Matched source references do not validate database metadata absent in the
source. Create notebook 02 for this next step, preserving the user's saved
notebook 01. Investigation of grouping/eligibility remains subject to review
after provenance evidence; no teammate implementation ownership changed.

## D009 — 2026-11-15: Keep timing diagnostics separate from run definitions

The user authorized the next metadata-provenance/timing investigation. Use
original source order within a source-path/cellid/ue_id/rnti diagnostic group.
Report all missing/invalid observations. Keep clock units raw and compare
cross-file intervals only under exact identity; neither a group nor disjoint
intervals establish independent runs. Do not set a gap threshold or convert
to rates/dates. Compare actual four-field database metadata against source
observations for the unresolved DoS candidates; retain every coincidence and
test radio agreement separately. Coincidence does not establish metadata origin.

Review archive names and pinned author code read-only. Keep external-source
limitations distinct from empirical findings. Add notebook 03 rather than
overwriting the user's saved notebooks. No evaluation definition, population
restriction, synthetic clock or teammate interface change is approved here.

## D010 — 2026-11-15: Hash-identified evidence and bounded provenance claims

The user reports no available Kaggle revision or team capture/export notes;
he is the first teammate to start. Record those inputs as unavailable. Use
selected-file hashes to identify analyzed content, without claiming a platform
revision or authenticated processing lineage. Assumed existing team artifacts
are not a prerequisite for forensic diagnostics or draft documentation.
Future model/degradation interfaces still need agreement.

Quantify metadata reuse and database-clock order projected onto source lines
as diagnostics, never as observed event time. Failure to identify the original
assignment mechanism is a valid outcome. Exclusion, clock replacement,
population restriction or fallback grouping remains a decision for Gaurav;
none is implemented by this follow-up.

## D011 — 2026-11-15: Prepare an evaluation draft without adopting it

The user authorized drafting docs/evaluation_protocol.md after reviewing the
timing evidence. Draft v0.1 separates six pending research decisions (EP-1 to
EP-6) from observed data facts. It proposes source-supported primary temporal
analysis with explicitly separate uncertain-clock diagnostics and provisional
source-file split groups, disclosing lost DoS ACK/SYN coverage and unverified
capture independence. These are recommendations, not approved exclusions,
grouping rules or clock interpretations.

Define denominators, NA behavior, paired conditions and abstention outcomes
before implementation. Prefer one binary study and a simple quality baseline
within the seven-week scope; model development/calibration remains Nitendra's
and degradation/playback Marco's. Dataset and interface uncertainties can be
documented while drafting proceeds; they are not silently resolved. Request
Gaurav's decision on EP-1 first, then review the remaining choices. EVAL-01
stays in progress until the approval/interface acceptance gate is met.

## D012 — 2026-11-15: EP-1 timing separation approved by Gaurav

Approval evidence: Gaurav selected **Approve EP-1 timing separation
(Recommended)** in response to the explicit cohort/coverage question.

Adopt the primary temporal eligibility definition of 43,704 database rows
with unique radio-plus-metadata source candidates. Retain the other 1,540
uncertain-clock rows for separate order-free, non-temporal diagnostics. Keep
every input in the audit inventory. This omits all current database DoS_ACK
(648) and DoS_SYN (892) examples from primary temporal coverage; Gaurav's
approval question explicitly included that consequence.

This approves the population distinction only. It does not authenticate source
clocks, recover capture independence, approve Unix-millisecond conversion,
assign groups/windows, choose splits/thresholds, or agree teammate interfaces.
EP-2 through EP-6 remain pending. Protocol v0.2 records this partial approval;
physical data and experiment configurations have not been changed.

## D013 — 2026-11-15: EP-2 provisional source-file grouping approved

Gaurav explicitly selected **Approve provisional source-file grouping
(Recommended)**. Keep every source file's UE streams, segments and windows
in the same split group. Merge files when capture linkage is established;
record the evidence. No capture links are currently established/applied.
Do not infer merges solely from the questionable metadata coincidences.
Label resulting performance as a source-file benchmark, with independent
capture identity unverified. This does not complete true-run recovery.

Materialize only the already approved EP-1/EP-2 definitions now: a row-level
manifest retains all 45,244 database rows, 43,704 primary temporal and 1,540
secondary non-temporal, in 43 provisional file groups (40 with primary rows).
Group IDs identify sorted source-file components, not authenticated captures.
No windows, partition assignments, clock conversion or thresholds are created.
EP-3 through EP-6 and teammate handoffs remain pending; protocol stays draft.

## D014 — 2026-11-15: EP-3 raw units and source-report order approved

Gaurav explicitly selected **Use raw units and report order first
(Recommended)**. Initial analyses retain raw timestamp values and original
source-report order; no Unix-millisecond/UTC interpretation is adopted.
Calendar-date prediction/contrasts, per-second rates and physical-time
freshness/delay/exposure claims remain deferred pending an explicit later
amendment. Clock provenance is not authenticated by this choice.

EP-1/EP-2 stay approved; EP-4 through EP-6 and model/degradation interfaces
remain pending. A read-only ten-report-window preview informs EP-4 but does
not create windows or adopt a length, stride, padding or gap threshold.
The earlier EP-1/EP-2 manifest is a historical materialization of those
definitions; its generation-time pending-decision metadata is not current
approval authority. Current review state lives in the checklist/protocol.

## D015 — 2026-11-15: EP-4 ten-report grid with retained tails approved

Gaurav explicitly selected **Approve the 10-report grid with retained tails
(Recommended)**. Build non-overlapping windows of ten reports per source and
cell/UE/RNTI identity in physical source order. Retain partial tails; unsupported
short inputs count as SHORT_WINDOW abstentions instead of disappearing. No
padding/masking implementation or model compatibility is asserted; Nitendra
retains that responsibility and interface agreement remains pending.

Materialize stable window references for the 43,704 primary rows. Keep the
1,540 secondary-only rows in the cohort manifest outside temporal windows.
Use raw clocks and existing provisional groups, without conversion or gap-
inferred run IDs. Stop on snapshot changes, unselected interior intervals,
non-increasing clocks or inconsistent labels rather than invent handling.
The current snapshot yields 4,332 complete windows and 74 tails (384 reports).
EP-5/EP-6 remain pending; no split, prediction or operating threshold created.

## D016 — 2026-11-15: EP-5 grouped split and training CV approved

Gaurav explicitly selected **Approve the grouped split plan (Recommended)**:
approximate 60/20/20 provisional-group partitions, seed 42, three grouped CV
folds inside training and explicit label-support checks. Do not use model
scores to select/redraw partitions. Provisional grouping/independence limits
and the small Benign-group count remain acknowledged.

Materialized primary groups 24/8/8, with Benign 6/2/2. Keep one of the three
secondary-only groups in each partition to preserve secondary-condition
support, giving full groups 25/9/9; this is within the approved approximate
allocation and does not move shared primary groups. Use sorted IDs, fixed
label-support allocation and isolated random.Random(42) permutations. Record
full outer/CV support; do not silently force mixed groups into majority labels.
In particular primary fitting CV fold 1 lacks DoS, and secondary test coverage
is tcp_test.txt rather than an ACK capture. Do not conceal or tune these facts.

Propagate every whole-file group's partition and training-CV ID to its rows
and windows, including tails. No preprocessing/model/calibration is fitted,
no clock conversion occurs, and no threshold/quality cutoff is selected.
EP-6 and model/degradation interface agreements remain pending. Window-grid
construction preceded partitions inside fixed file groups without learning;
all learned transformations must occur after splitting, within training only.

## D017 — 2026-11-15: EP-6 evaluation definitions approved

Gaurav explicitly selected **Approve EP-6 definitions (Recommended)**. Protocol
v1.0 adopts Benign versus supported attack, primary file-proxy AP, secondary
ROC-AUC/window summaries, report-mean baseline window scores and file-maximum
window scores. Use validation-only equal-class utility
U = 0.5 * (TP/N_A + TN/N_B), retaining abstentions in class denominators;
freeze the chosen threshold before test. The specified score boundary/tie
rules remain in the protocol. No actual threshold has been selected.

Adopt full two-by-three outcome/coverage reporting with explicit undefined
metrics. File decisions are ATTACK for any accepted attacking child, BENIGN
only when every planned child is accepted benign, otherwise ABSTAIN.
Quality-only abstention is the baseline direction. Required quality KPIs,
numerical cutoffs, security/coverage budgets and teammate interfaces remain
separately gated, as stated in the approval question. No operational cost
model, authenticated clocks, independent captures or calibrated scores are
established by this decision. Optional bootstrap settings are still proposals.

EVAL-01's review gate is met through the six approvals and explicitly gated
interfaces. Begin EVAL-02 with outcome accounting only, independent of producer
formats. Synthetic checks validate formulas, not empirical detector performance.
## D018 - 2026-11-15: Scope reaffirmed; threat-model revision prepared

Gaurav reaffirmed ownership of threat modeling, evaluation protocol and
abstention policy, then authorized continuing with the threat model. The
v0.2 draft replaces the initial skeleton using existing local audit evidence
and approved EP-1 through EP-6. It distinguishes observed facts, adopted
evaluation choices and unresolved deployment/attacker assumptions. It treats
telemetry failures separately from attack labels and does not attribute
metadata anomalies to malicious tampering.

This is a preparation record, not approval of the threat model or a new
experimental assumption. No attack scope, numerical policy cutoff, evaluation
definition or teammate API is changed. Nitendra retains model/calibration and
Marco retains degradation/playback ownership. TM-01 remains in progress for
Gaurav review; missing capture/topology evidence remains unknown.

## D019 - 2026-11-15: Bounded threat model accepted; policy drafting begins

Gaurav selected **Accept the bounded model and stated limitations (Recommended)**.
The accepted analytical scope is offline dataset-scenario classification,
telemetry failures separated from attacks, no assumed collector/RAN compromise
and no mitigation claim. Deployment topology, specific attacker privileges and
capture independence remain unknown. This accepts v0.2's analytical model,
recorded as threat_model.md v1.0 without changing its substantive assumptions.
TM-01's bounded review gate is satisfied; no deployment validation or complete
M1 milestone is claimed. Capture/provenance tasks retain their own open gates.

Prepared abstention_policy.md v0.1 from EP-6. The new minimum-per-required-KPI
completeness formula (AP-1) and equality handling are proposals, not approved
policy details. Required inputs/contracts, security/coverage constraints and
numerical quality/classifier thresholds remain pending. The draft distinguishes
an unfinished policy configuration from unavailable quality in a configured
case. It implements no model, degradation, calibration or executable policy.

## D020 - 2026-11-16: AP-1 completeness definition approved

Gaurav selected **Approve AP-1 completeness definition (Recommended)**.
Completeness is the minimum observed-valid fraction over required KPIs, counted
before imputation against distinct expected report positions. Retained tails
use their actual planned count. Quality passes at q >= q_min; model-unsupported
short inputs still abstain. An operational use requires an observable expected
grid. Required KPI names, validity/producer contracts, numerical q_min and
security/coverage budgets remain pending; no threshold is selected.

Added an internal pure completeness calculator with synthetic tests. It
distinguishes known missing/invalid values from unknown masks, ignores optional
KPIs and rejects invalid/duplicate grid configuration and out-of-grid required
mask entries. Callers establish validity, provenance and causal observability;
the calculator does not establish them. Its signature is not a producer API.
Policy v0.2 records AP-1 approval; ABS-01 remains in progress. Only this
approved quality subcomponent advances ABS-02; configured policy execution
still requires the remaining gates. No teammate implementation is introduced.

## D021 - 2026-11-16: AP-2 handoff proposal prepared, not adopted

Following Gaurav's instruction to prepare AP-2, inspected existing cohort,
window and split manifest structures and the SQLite column names read-only.
Prepared docs/abstention_input_proposal.md v0.1, separating available offline
references/counts from unverified operational metadata and pending model/score
and quality-mask contracts. It documents agreement questions and example
acceptance cases, not an implemented loader or agreed producer API.

The existing radio-comparison fields are an inventory, not required KPIs.
Whether required quality inputs vary per model/feature condition or use a
common set remains a review question. Gaurav and the relevant producers must
agree before any adapter or configured policy depends on those choices.
AP-2 through AP-4 remain pending. No numerical settings, evaluation definitions
or team interfaces changed, and no teammate messages were sent.

## D022 - 2026-11-17: Vendor-restricted visibility confirmed as primary

Gaurav selected **Yes—vendor-restricted visibility is primary (Recommended)**
for: how reliably can intrusion detection operate when O-RAN vendor
implementations expose only a restricted telemetry subset, and when should
it abstain? Shortcut checks support evaluation validity; dropped/stale-report
experiments are secondary and need separate justification. This records
Gaurav's intended priority, not an official team/instructor scope change.

Align current title, scope and work plan with that priority. Retain historical
titles/notes, completed audits and approved EP-1–EP-6/AP-1 foundations rather
than reinterpreting them as vendor evidence. No vendor capability matrix,
restriction profiles, minimum telemetry set or final comparison protocol has
been established. CAP-01/CAP-02 now define the primary evidence/review path.
No raw data, population, clock interpretation, windows, splits, metric formula,
policy cutoff, model strategy or producer contract changes in this amendment.

Working title for alignment is Intrusion Detection with Vendor-Restricted
O-RAN Telemetry, subject to team/instructor review. Structural absence of a
required measurement must not be hidden by silently shrinking K. An agreed
compatible reduced-input model or explicit abstention needs specification.
Model/calibration and degradation/playback ownership remain Nitendra/Marco's.

## D023 - 2026-11-24: Descriptive EDA feedback follow up

Gaurav authorized the focused professor-feedback update. Add reproducible
descriptive summaries and a cleaning/interpretation ledger, with distinct
full, primary, secondary and primary-training populations. Use the existing
fixed manifests and raw-unit timing diagnostics. No model feature removal,
physical bounds, vendor profile, clock interpretation or operating threshold
is adopted. Quantiles use linear interpolation at (n-1)p and SD is sample SD.

Clarify legacy UTC/calendar outputs as provisional, preserving their code and
saved results. Append a cohort-aware section to the combined notebook while
retaining its original 23 audit code cells. Use correlations as descriptive
evidence, not redundancy or causality claims. Learned preprocessing/model
selection stays training-only and Nitendra-owned. CAP-01 remains the primary
next task; this feedback does not replace the vendor-visibility objective.

