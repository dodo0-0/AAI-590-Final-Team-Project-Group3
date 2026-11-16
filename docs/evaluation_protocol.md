# Evaluation protocol — v1.0

**Status: EP-1 THROUGH EP-6 APPROVED; TEAM INTERFACES AND QUALITY PARAMETERS GATED — 2026-11-15.**
Gaurav approved timing separation, provisional whole-source-file grouping,
initial use of raw timestamp units/source-report order, and ten-report windows
with retained tails, and grouped partitions/training-only CV. Cohort, group,
window and partition manifests are materialized without modifying raw data.
EP-6 definitions are approved. No models, selected operating thresholds, clock conversion
or model-specific partial-input encoding have been implemented.
EVAL-01's definition-review gate is satisfied with interfaces explicitly gated.
Approval does not establish model compatibility, capture independence or
performance. Optional extensions marked proposed below remain unadopted.

Gaurav owns evaluation, threats and abstention; Nitendra owns models and
calibration; Marco owns degradation and playback. Their interfaces below are
proposals. The seven-week scope favors one binary evaluation, a fixed set of
shortcut comparisons and a simple abstention baseline. Multiclass model
development, new training frameworks and simulators are outside this draft.

## 1. Review decisions and recommended starting point

**EP-1 through EP-6 are approved.** D012–D017 record the approvals and limits.

| ID | Definition / proposal | Alternative / consequence | Approval gate |
| --- | --- | --- | --- |
| EP-1 | Primary sequence/temporal cohort: 43,704 database rows with unique radio-plus-metadata source candidates. Preserve the other 1,540 rows for separately labeled non-temporal diagnostics. | Defer temporal evaluation and limit initial work to non-temporal diagnostics; or analyze all 45,244 rows with database clocks only as an explicitly unverified sensitivity condition, never the source-supported primary condition. | **APPROVED 2026-11-15** by Gaurav, including restricted DoS coverage. |
| EP-2 | Provisional split groups: entire source files, merging files whenever documented capture linkage requires it. Call results file-group benchmarks until independent captures are verified. | Require authoritative run IDs before any performance evaluation; this may leave the study descriptive. | **APPROVED 2026-11-15** by Gaurav, with capture independence explicitly unverified. |
| EP-3 | Start with report-index analysis and raw timestamp diagnostics. Physical-time experiments require a separately approved clock interpretation. | Unix-millisecond/UTC interpretation was not selected. Calendar dates, per-second rates and physical-time claims remain deferred until an explicit later amendment. | **APPROVED 2026-11-15** by Gaurav: raw units and source-report order first. |
| EP-4 | Ten observed reports per source/UE identity, stride ten, source order; retain partial tails and count unsupported short inputs as SHORT_WINDOW abstentions. | A changed grid needs a protocol amendment. Model-specific variable-length/masked encoding remains a pending Nitendra interface. | **APPROVED 2026-11-15** by Gaurav for the evaluation grid and retained-tail rule. |
| EP-5 | Approximately 60%/20%/20% of split groups for training/validation/test, seed 42; three grouped training-only CV folds and explicit support checks. | Any revised strategy needs review before scores; never fall back to random rows or redraw a favorable seed. | **APPROVED 2026-11-15** by Gaurav. Primary allocation 24/8/8; full allocation 25/9/9 includes one secondary-only group per partition. |
| EP-6 | Binary scoring, aggregation and validation-only threshold utility in sections 5 and 7–9; quality-only abstention first. | Any change to adopted definitions needs review before testing. | **APPROVED 2026-11-15** by Gaurav. Required quality KPIs, numerical cutoffs/security budgets and teammate interfaces remain separately gated. |

EP-1 approval separates evidence conditions; it is
not a claim that 43,704 rows have authenticated clocks or independent runs.
No rows are deleted from the audit inventory under any option.

## 2. Established evidence and what it does not establish

Evidence: [structural findings](data_audit_findings.md),
[reconciliation](reconciliation_findings.md), [timing](timing_findings.md),
and [provenance review](provenance_sources.md). Their local JSON artifacts
identify inputs by path, size and SHA-256. Kaggle revision is unavailable;
do not invent a release number. Preserve the downloaded archive and manifests
outside Git. No model performance has been evaluated in this workspace.

The database has 45,244 rows; 49 source files contain 50,213 objects.
Radio-plus-metadata comparison identifies 43,704 unique candidate pairs.
The approved EP-1 primary temporal cohort has this composition:

| Literal database category | Proposed primary rows | Full database rows |
| --- | ---: | ---: |
| Benign | 10,664 | 10,664 |
| BruteForce | 3,057 | 3,057 |
| DDoS | 15,084 | 15,084 |
| DoS | 3,181 | 4,721 |
| Probe | 8,445 | 8,445 |
| Web Attacks | 3,273 | 3,273 |
| Total | 43,704 | 45,244 |

This subset has candidates in 40 source files, including 10 Benign files.
Those counts are not counts of independent runs. The 88 identity groups,
52 preliminary gap reconstructions and 42 reported paired runs are not
validated independent capture IDs.

**Coverage consequence:** EP-1 omits all current database DoS_ACK (648) and
DoS_SYN (892) rows from the primary temporal condition. Its remaining DoS
rows are ICMP, UDP and Slowloris. Therefore primary results cannot support
claims about single-source ACK/SYN temporal detection. All six broad category
names remaining present does not preserve all attack mechanisms.

The 1,540 omitted rows have unique radio candidates lacking source clocks/UE
metadata. Their database metadata coincide elsewhere, and projected clocks
show reversals. This warns about provenance; it does not prove a particular
assignment algorithm. The 4,969 source-only radio-unmatched observations are
also retained in the inventory. Expanding to them would require a separately
reviewed source-labeling/cohort definition; do not silently merge them into
the database population or select a condition because its scores look better.

The full 45,244-row database is retained, with the 1,540 uncertain-clock
rows separately identified for non-temporal diagnostics under EP-1. Specific
secondary reporting follows EP-6 where its inputs are available. For those rows, restrict
diagnostics to order-free, non-temporal eligible KPIs: no date, freshness,
sequence, elapsed-time or rate claims. Use a split-group manifest covering the
union of declared populations before applying cohort filters; common source
groups retain the same partition. Any additional secondary-only files receive
their partition before modeling, not after inspecting primary test results.
An aggregate difference between these two populations is not a paired
robustness effect. Comparisons require a common row/feature subset or must be
labeled as composition-sensitive descriptive results.

## 3. Dataset preparation and evidence gates

1. Verify selected-file hashes and record audit/reconciliation code hashes,
   environment versions and artifact hashes. Retain original physical lines,
   database rowids and candidate multiplicity; these are references, not run IDs.
2. Validate literal labels rowwise: category/subcategory/binary flag consistency,
   absent/unknown labels and mixed-label files. Proposed binary map: Benign=0;
   the five other documented categories=1. Web/Web Attacks and DDOS/DDoS aliases
   require an explicit mapping manifest. Do not turn unknown labels into benign.
3. Build row-level provenance flags: source-clock available, strong candidate,
   radio-only candidate, ambiguous or unmatched; keep them out of predictors.
   Unique projection agreement does not authenticate every field or collection
   condition. Resolve contradictory labels before using affected units.
4. Retain raw timestamps. Group order diagnostics by source plus observed
   cell/UE/RNTI, without treating those identities as independent captures.
   Never sort questionable database clocks to manufacture a plausible timeline.
   Physical line order alone does not certify event order. Epoch, units,
   event-versus-arrival semantics and synchronization remain explicit assumptions.
5. Separate semantic exclusions from learned processing. Exclude source/run/date
   IDs, rowids, timestamp values, cellid, ue_id, rnti and label columns from
   model inputs. Keep in_sync/identity missingness as audit/quality metadata,
   not an attack shortcut. PMI conversion is unavailable until representation
   semantics are verified. Fit constant/variance filtering only on training data;
   global structural diagnostics do not authorize fitted feature selection.
6. Investigate missingness beyond SQL NULL: absent keys, empty strings,
   sentinels, invalid ranges and nonfinite numbers. Preserve raw masks before
   any imputation. Fit imputation/scaling/selection on training partitions only.
   A KPI entirely unavailable in training cannot acquire a held-out-fitted fill.
7. Validate whether dlBytes/ulBytes are cumulative, their units and reset/wrap
   behavior. If approved as counters and clocks are usable, derive
   `rate = (counter_now - counter_previous) / elapsed_time` within the same
   source/UE/capture context and partition. Positive elapsed time is required;
   first observations, negative deltas and unresolved resets yield missing
   rates with reason flags. Never difference across captures or split boundaries.
   Do not label values bytes/second before time and byte units are approved.
   If not validated, omit absolute counters from primary predictors and mark
   the rate-based traffic diagnostic unavailable rather than invent values.
8. Persist a cohort/attrition manifest by category, subtype, source and reason.
   Never resolve repeated candidate groups by arbitrary first-match selection.
   No test-score-driven cleaning or exclusion is allowed.

The earlier notebooks inspected dataset-wide structure. Disclose that history:
the future test population is performance-held-out, not previously unseen
at the schema/integrity level. No global distribution is used to fit a model
or choose transformations. Training-only processing follows the
[official leakage guidance](https://scikit-learn.org/stable/common_pitfalls.html).

## 4. Grouping, partitions and leakage prevention

Distinguish four units: source observation; model decision window; assessment
unit (source file provisionally, validated run if available); and split group
(all related assessment units that must stay together). An assessment unit
is not necessarily the unit of statistical independence.

Preferred split groups are authenticated independent captures. Under EP-2,
all UE streams, windows and segments from a source file stay in one group.
Merge documented related files into connected components before partitioning,
including overlapping/repeated recordings if lineage establishes a link.
Do not create links from class labels or model scores. Equal radio values alone
do not establish a shared capture. A record with unresolved multi-file lineage
cannot be placed arbitrarily; merge its candidate files or keep it outside
that comparison under an explicitly reviewed rule.

The fallback is **source-file-disjoint**, not proven independent-run-disjoint.
No statement of cross-day/site generalization follows from it. Zero overlap
under an exact cell/UE/RNTI key is not proof of independence. Random row splits,
splitting UE streams of one file across folds, and gap-derived subsegments
treated as independent replicates are prohibited for primary evaluation.

After approval, create the group manifest before preprocessing/windowing.
Use the approved approximate 60/20/20 allocation and seed 42 with support constraints:
both binary classes in training, validation and test; document attack-family
support in each. Fractions are targets at group level, not row quotas. Use
deterministic label-support checks rather than searching for a favorable score.
If a constraint is impossible, report infeasibility and seek a revised plan.

Actual EP-5 assignment, constructed without model scores:

| Partition | Primary groups | Primary Benign groups | Primary reports | Primary windows | Retained partial windows | Secondary-only groups | Secondary rows |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Train | 24 | 6 | 26,455 | 2,669 | 46 | 1 | 768 |
| Validation | 8 | 2 | 8,306 | 838 | 17 | 1 | 648 |
| Test | 8 | 2 | 8,943 | 899 | 11 | 1 | 124 |

The full group allocation is 25/9/9, approximately 58%/21%/21%. Each of the
three secondary-only files receives a partition to preserve secondary-condition
support; no primary assignment is moved for that purpose. This satisfies the
approved approximate group proportions, not an exact row-ratio requirement.
Very small benign validation/test counts limit threshold precision and
false-positive claims. The secondary-only test file is tcp_test.txt (124 rows);
it does not provide held-out ACK coverage. Do not redraw the split to improve
that outcome after seeing scores.

Implementation uses sorted IDs/category names, isolated Python random.Random(42)
permutations and fixed constrained integer allocation. Primary Benign/attack
targets are apportioned first; attack-family allocations keep outer-partition
support where feasible. No mixed-category group is reduced to a majority
label: the current allocator stops for review. Split and CV references are in
results/split_manifest_ep1_ep5_2026-11-15.json.

Three training folds retain both binary classes in fitting and held-out groups,
but not every attack family. In the current CV fold 1, the primary fitting
groups lack DoS because the sole primary training DoS group is held out.
This must be reported as an attack-family support limitation; it is not a
fully supported multiclass experiment. Full fold support tables are saved.

The deterministic within-file window reference grid was materialized before
partition assignment, after source groups were fixed; no fitting or model
scores were involved. Group assignments now propagate to every row/window.
No window crosses a source boundary. Learned preprocessing remains strictly
after splitting and training-fold-only. The earlier preview is historical.

Within training, use the approved three grouped CV folds, re-fitting all preprocessing
and feature selection on each fold's training groups. A
[grouped stratification helper](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.StratifiedGroupKFold.html)
can assist, but cannot guarantee feasible class balance or capture independence.
Inspect actual group intersections/support and save the folds. Stratification
must not let long files silently dictate the intended group-level allocation.

Nitendra selects model hyperparameters using training CV. Fit the chosen
preprocessor/model on training only. Validation is for calibration, operating
thresholds and abstention choices; its selected performance is developmental.
If validation is reused for several choices, disclose that reuse and limit
the search. Do not refit on validation after freezing its thresholds without
new independent calibration/selection data and review.

Final test groups, labels for scoring, and their clean/degraded counterparts
remain locked until the model, preprocessing, feature comparisons, thresholds
and scenario configurations are frozen. Shared test labels may be used only
for final reporting, not model or exclusion decisions. Reuse identical group
partitions across models/feature groups. Repeated runs/seeds are not additional
independent captures. No best-test-fold/seed selection is permitted.

## 5. Decision windows, labels and aggregation

EP-4 approves W=10 reports and stride=W within each source/UE identity, in
original order. This is a report-index window, not a verified ten-second
window. Record its raw span and gaps; variable physical duration is a limitation.
Do not infer new runs or silently cut unusually large gaps. If fixed-duration
windows or a maximum-gap boundary are required, approve that numeric policy
and clock assumption first. Never bridge a known capture boundary, backwards
clock transition, or unresolved ordering interval. Reset model state at source/
capture boundaries; any carried within-source state must be documented.

Freeze the clean reference window grid and stable window IDs before degradation.
Retain partial tails and short streams in the coverage ledger. Nitendra must
agree how shorter inputs are represented; an unsupported input yields ABSTAIN
with SHORT_WINDOW, not a silently deleted case. Window eligibility and handling
must be common across comparisons. Missing metadata/rows must not be removed
and remaining fragments glued into a different apparent sequence.

The materialized EP-4 grid covers 87 diagnostic identity streams in 40 files,
with 43,704 reports: 4,332 complete windows and 74 partial tails containing
384 reports, or 4,406 windows total. One stream has only eight reports;
34 files have a tail. These are not 87 independent runs. No gap threshold
or inferred run boundary is introduced. Actual window references and raw-span
diagnostics are in results/window_manifest_ep1_ep4_2026-11-15.json; the earlier
preview remains a historical check. Construction fails on non-increasing
source clocks, unselected interior records or inconsistent labels, requiring
review rather than silently reordering, gluing fragments or repairing time.

Partial-input support matters: under the approved conservative assessment
rule in section 9, an unscorable tail can leave a file ABSTAIN unless an
accepted child window detects an attack. Agree variable-length/masked-input
support with Nitendra; approval of the evaluation grid does not assert model
compatibility. Unsupported tails remain SHORT_WINDOW abstentions, not dropped
denominator entries. That aggregation rule is approved under EP-6.

Approved window truth is the documented scenario label shared by its source
records, after consistency checks. It is not proof that every UE in an attack
capture is itself attacking. Mixed or uncertain truth requires resolution or
explicitly reported unknown-label units outside supervised metric denominators;
report those counts separately. No time-to-detection claim is possible without
validated attack onset, clocks and exposure intervals.

Models export a finite score s_w increasing with attack evidence. Report its
type: probability or raw decision score. Row-level baselines use the arithmetic
mean of their report attack scores within the same window; sequence models
produce one window score. This adapter must be agreed with Nitendra. Raw scores
are not automatically calibrated confidence. Multiclass probability outputs,
if supplied, may be summed over the approved attack categories for the binary
score; a multiclass evaluation is not automatically added to scope.

Assessment score is the maximum available window score across its UE streams.
If no score exists, it is unavailable, not zero. Report scored-window fraction
for each assessment unit, since a maximum from partial observations differs
from a complete maximum. Longer captures offer more opportunities to alarm;
report window counts and, only with approved clocks, exposure duration.

Until capture IDs are validated, label assessment metrics `file_proxy_*`.
Reserve `run_*` for verified runs. Aggregation is fixed across clean/degraded
conditions; do not change a maximum to a mean after seeing test performance.

## 6. Feature-group shortcut audit

The following are provisional semantic groups, not validated allowlists:

| Comparison | Candidate definition | Required check |
| --- | --- | --- |
| Downlink channel-only | rsrp, rsrq, rssi, sinr, cqi only where their downlink meaning is confirmed | Verify exporter/dictionary direction; exclude uplink power/SNR. |
| Traffic-only | Rates derived from dlBytes and ulBytes | Validate cumulative/time/reset semantics; otherwise unavailable. |
| Uplink power/SNR-only | phr, pcmax, pucchSnr, puschSnr where semantics are confirmed | Verify units/direction; do not describe pcmax as measured power without evidence. |
| All eligible | Approved radio KPIs plus validated rates, after semantic exclusions and training-only filtering | dlMcs/ulMcs and dlBler/ulBler may enter here; do not silently relabel them as pure traffic or channel measurements. |

Keep the same cohort, windows, folds, tuning budget and score aggregation for
comparisons. If a feature group is unavailable or changes score coverage,
report that fact; do not substitute a different definition to obtain a score.
Inspect per-file and per-fold variation, not just pooled accuracy. Channel
performance alone is evidence of association, not proof of an environmental
shortcut or causal attack behavior.

EP-3 currently authorizes raw units/order only. Date conversion requires an
explicit later amendment. If Unix-millisecond conversion is then
provisionally used, label dates as derived UTC dates under that assumption;
UTC is a reporting convention, not a claim about the capture locale. Exclude
questionable clocks from primary date diagnostics. Build category-by-date
support using source/capture groups, not row counts. Show absent combinations.

For same-day Benign-versus-attack contrasts, require actual support for both
conditions and disjoint source/capture groups. Do not fabricate benign data,
reuse windows across partitions, or infer availability from file names.
Use the common supported contrasts across feature comparisons and state which
attacks/dates are absent. Missing support is a scientific limitation.

Recording-date prediction is a separate diagnostic task with date as target;
timestamp/date/identifiers are excluded from predictors. A held-out source
group must exist for a date represented in training to evaluate that date
class. Unsupported dates/folds are reported, not silently pooled or treated
as new classes the classifier was trained to recognize.

If recording date and attack category are inseparable, the dataset cannot
isolate attack effects from date/environment effects. Neither grouped splitting
nor a high date-prediction score fixes this identifiability problem. Report
the supported claim and any negative/non-estimable result explicitly.

## 7. Threshold selection and primary reporting

Approved primary task is Benign versus any supported attack, with attack=1.
Report per-attack-family recall as a diagnostic; source-provided scenario labels
do not establish exploit success. Keep one threshold per model/feature condition,
selected before test from validation assessment-unit scores. No class-specific
test thresholds, scenario-specific retuning or test-optimal operating points.

Approved validation utility is `U = 0.5 * (TP / N_A + TN / N_B)` at the
assessment level, where abstained/unscorable units remain in N_A/N_B and
contribute neither TP nor TN. Without abstention this is balanced accuracy.
It is an approved equal-class research utility; operational costs remain gated.
Search validation scores' distinct decision boundaries, including all-attack
and all-benign boundaries; predict ATTACK for s >= threshold. Break utility
ties by the larger threshold. Save candidates, chosen value, utility and counts.
With only one validation class, selection is unsupported; do not tune on test.

EP-6 approves this rule. A replacement requires a protocol amendment before
testing. Very few benign groups make fine false-positive targets unsupported.
Calibration remains Nitendra's responsibility. Confidence abstention requires
validation evidence of calibration; the baseline below needs no such claim.

Approved primary ranking summary is assessment-level AP, with ROC-AUC and window-level
summaries alongside detection/false-positive/coverage counts. All comparisons
must disclose which units have scores. A candidate model cannot win model
selection by silently failing to score difficult clean units; scoring-coverage
requirements and any common-comparison subset must be frozen before comparison.

## 8. Metrics and undefined cases

Compute metrics at the window level and the approved assessment level,
stating cohort, condition, aggregation, threshold, class prevalence, number
of sources/split groups and scored/total units. File/run score AUCs are computed
across multiple assessment units with both labels, not within homogeneous
single-class files and then averaged.

Benign-window FPR is not false alarms per hour. An exposure-normalized rate
requires approved clocks, a defined alarm-episode/cooldown rule and valid
observation exposure. Do not count parallel UE time repeatedly as capture
wall-clock exposure. Until those definitions are available, report window
counts and benign assessment-unit alarm counts, without a per-hour claim.

| Metric | Definition / interpretation |
| --- | --- |
| ROC-AUC | Area under TPR versus FPR as the continuous-score threshold varies; hard decisions alone are insufficient. |
| PR summary | Approved primary: average precision, AP = sum of recall increments times precision at the corresponding thresholds. Label outputs `AP`, or explicitly `PR summary (AP)`. |
| Trapezoidal PR-AUC | If also reported, integrate the PR curve with a stated interpolation convention and a distinct name; do not interchange it with AP. |
| Detection | Window and file-proxy/run attack recall at the locked threshold, with raw numerator/denominator and attack-family counts. |
| False-positive behavior | FP/N_B over all benign units and FP/(FP+TN) over accepted benign units; show abstention separately. At file/run level also report number of benign units with any alarm. |
| Variation | Per-file/capture outcomes, training-CV fold summaries and valid/undefined-fold counts; no window-independence assumption. |
| Paired robustness | Degraded-minus-clean differences at fixed cohort/units, with coverage and failed/unscorable pairs exposed. |

ROC-AUC uses prediction scores as described in the
[official definition](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.roc_auc_score.html).
AP and trapezoidal PR area differ; the
[official AP definition](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.average_precision_score.html)
specifies recall-increment weighting without linear interpolation.

Protocol convention: when an evaluated set lacks either binary class, report
ROC-AUC and discriminative AP comparisons as NA with `NO_POSITIVES` or
`NO_NEGATIVES`. A library may return a number for some one-class AP inputs;
that does not make this study's discrimination comparison estimable. Recall
with no attacks, FPR with no benign units and precision with no predicted
attacks are NA with explicit denominator reasons, not silently zero or one.
Undefined entries do not become perfect scores. Show the number and support
of valid folds when summarizing them; do not hide omitted folds behind nanmean.

AUC/AP on scored units remain conditional on score availability. Report
unscorable attacks and benign units alongside them; do not substitute a benign
score for absent predictions. For clean/degraded ranking comparisons also
report the common-scorable aligned subset and its attrition. Its AUC change
does not replace full-denominator operational detection/abstention reporting.

Use one vote per assessment unit for assessment-level metrics; long files
contribute more windows to pooled window metrics, which must be labeled as
such. Do not average window metrics and file/run metrics into one score.
Report actual prevalence with AP. Training class weights/resampling, if used
by Nitendra, are learned/applied within training only; validation/test keep
their observed composition.

Do not pool unrelated raw-score scales across CV folds into a primary AUC.
Report fold metrics and mean/range with denominators; optional pooled calibrated
out-of-fold scores need an explicit common score interpretation. Fold variation
is not a confidence interval for final-test performance.

Where independent captures are verified, uncertainty may resample whole capture
groups, retaining every nested UE/window and paired condition. Proposed optional
bootstrap: 2,000 resamples, seed 42, percentile 95% intervals, reporting invalid
single-class resamples and their counts. No row bootstrap or seed-as-run
replicates. With provisional source groups, label such output only as a
grouping-conditional sensitivity interval, not independence-backed confidence.
If support is too weak, provide counts/ranges and state that uncertainty is
not reliably estimable. Zero observed false alarms does not establish a very
low deployment FPR; ten available Benign files are not ten proven independent
benign captures, and only a fraction may reach the final test.

## 9. Abstention accounting and simple baseline

An evaluated outcome is BENIGN, ATTACK or ABSTAIN. Abstention is not correct
classification, automatic mitigation or a detected attack. No downstream
human response is assumed unless actually specified and evaluated.

Approved quality-only baseline direction: ABSTAIN for no usable observations, invalid/
missing score, unavailable required quality metadata, or required-KPI
completeness below q_min. Otherwise apply the locked attack threshold.
Use reason codes such as NO_OBSERVATIONS, INVALID_SCORE, QUALITY_UNAVAILABLE,
LOW_COMPLETENESS and SHORT_WINDOW. Compute completeness from visible raw masks
before imputation. Required KPIs and q_min are pending ABS-01 decisions;
do not invent a numerical threshold or assume absent metadata means healthy.
Freshness/staleness/irregularity gates require identifiable metadata and approved
units. A constant KPI alone is not evidence of stale data.

Choose quality thresholds using validation only, showing coverage versus
retained-error and full-denominator missed-attack tradeoffs. Gaurav must first
choose coverage/security costs or constraints; if no feasible point meets
them, report failure rather than quietly relaxing a requirement. Freeze the
policy before test. Keep model/threshold unchanged in the clean-to-degraded
baseline; any adaptation is a separately approved experiment.

Let N_A and N_B be all labeled attack/benign units. Use the full 2-by-3 table:
TP (attack predicted attack), FN (attack predicted benign), U_A (attack
abstained), FP (benign predicted attack), TN (benign predicted benign), U_B
(benign abstained). Then:

- Coverage: `(TP + FN + FP + TN) / (N_A + N_B)`; abstention rate: its complement.
- Attack/benign coverage: `(TP + FN)/N_A`, `(TN + FP)/N_B`.
- Retained error: `(FP + FN)/(N_A + N_B - U_A - U_B)`.
- Retained attack recall: `TP/(TP + FN)`; full-denominator detection: `TP/N_A`.
- Unresolved/missed attacks: `(FN + U_A)/N_A`, with FN and U_A separately.
- Report `U_A/N_A` versus `U_B/N_B` and their difference to expose disproportionate
  attack abstention. Keep all zero-denominator cases NA.

For abstained units with an available underlying score, report whether the
locked classifier would have erred, with its own scored-abstention denominator.
Separate unscorable abstentions; do not fabricate their counterfactual errors.
All U_A cases remain unresolved security outcomes even if the underlying score
would have been correct.

At assessment level: ATTACK if any accepted child window predicts ATTACK;
BENIGN only if every planned child window is accepted BENIGN and at least one
exists; otherwise ABSTAIN. This prevents partial observation from silently
certifying a benign capture. Report both levels. A quality policy can abstain
more on attacks even if retained accuracy improves; that is not a security gain.

## 10. Paired degradation with Marco

Freeze held-out clean units first and create degraded counterparts of the same
source/capture and window IDs. Retain the clean reference grid for labels and
pairing even when every report of a window or a UE disappears. Such cases
remain denominator entries and usually produce ABSTAIN; they are not removed
as nonexistent observations. Do not use clean test values, labels or future
observations as model/policy inputs to repair degraded telemetry.

The clean reference grid belongs to the evaluator, not the prediction policy.
Quality signals passed to that policy must be available from visible masks or
a causal reporting/schedule contract. A completeness ratio requiring oracle
knowledge of clean future reports is not part of the deployable baseline.
The evaluator can assign NO_OBSERVATIONS to an offline reference window;
online emission deadlines and silence detection need a specified schedule.
Report-index pairing alone is not a real-time deployment demonstration.

Candidate scenarios are dropped reports, reduced report frequency, stale values,
missing UE observations and, if arrival/event times are supported, delay.
Marco must define the generator, unit of loss (report, UE or KPI), burst/
correlation behavior, reference schedule, causal availability metadata and
alignment. A report-index reduction is not automatically a realistic E2
configuration. Specify levels only after agreement and justification; no
arbitrary percentage or interval is presented here as operational realism.

Use one frozen scenario manifest with levels/seeds and identical realizations
across models. Distinguish validation scenarios used for policy selection from
locked final scenarios; unseen severity is a separately labeled condition.
Multiple random realizations of one capture are nested replicates, not new
captures. Aggregate realizations within a capture before cross-capture summaries
and resample capture pairs together for conditional uncertainty.

For each metric define delta as degraded minus clean, with units/direction
stated. Detection/coverage losses may be negative; FPR/miss increases positive.
Report per-assessment outcome changes and paired cohort metrics. AUC differences
are computed from the aligned cohort scores in each condition; do not average
undefined per-file single-class AUC differences. If score availability changes,
show common-scorable ranking deltas plus full-population detection, coverage
and abstained-attack counts. A higher conditional AUC with lower attack coverage
must not be described as improved robustness.

Train the initial model on clean training data. Training with degradation or
retuning per condition would be a new reviewed experiment owned jointly with
the appropriate teammate, not an implicit part of this evaluation utility.

## 11. Proposed handoff contract and reproducibility artifacts

These field concepts are not yet an agreed API. Validate availability with
Nitendra and Marco before writing a loader or policy around them:

| Producer | Proposed required concepts |
| --- | --- |
| Gaurav's manifests | Input hashes, cohort membership/reasons, source path/line and row references, provenance flags, assessment/split-group/window IDs, truth label and mapping version. |
| Nitendra | Model/config/code identity, training-group IDs, preprocessing/calibration provenance, window ID, attack score/type/direction, missing-score reason and model input requirements. |
| Marco | Source/window alignment, scenario/level/seed, observable report/KPI masks, expected-count metadata where operationally supported, event/arrival times when available, missing-UE/stale/delay indicators with units and causal semantics. |

Store a protocol version and approval record; file/label/feature/group/window
manifests; exact partitions/CV folds; all seeds and RNG/software versions;
trained transformation/model/calibrator references; threshold/policy selection
ledger; scenario configurations and justification; prediction/outcome tables;
metric denominators/NA reasons and paired reports; executable commands and
limitations. Capture a code commit or code hashes until Git is initialized.
Raw data and large artifacts stay outside Git. Selected report summaries must
remain traceable to those local artifacts, not notebook execution state.

Before final test execution, validate group disjointness, within-source lineage,
no label/identifier features, training-only fitted artifacts, frozen thresholds,
consistent windows across comparisons, complete planned-case accounting,
and one-to-one clean/degraded alignment. Necessary utility tests must exercise
those failure cases, missing classes, zero denominators and abstention accounting.
This document adds no implementation tests or experiment results itself.

## 12. Approval and next implementation gate

EP-1 through EP-6 are approved. Next implement one small evaluation utility.
Record each accepted/revised choice and its limits
in decisions.md. A changed primary population, endpoint or test plan requires
an updated protocol version before execution. Any later departure motivated
by observed test scores must be labeled post hoc and cannot reuse that test
as a fresh confirmatory holdout.

EVAL-01's review gate is satisfied: Gaurav approved definitions and explicitly
kept quality KPIs, numerical cutoffs/security budgets and teammate interfaces
separately gated. No producer adapter, score ingestion or empirical comparison
may assume those pending contracts are agreed. The approved subset/group manifest is now
materialized along with report windows and group-disjoint partition/CV
assignments. No predictions or fitting have occurred. Model training remains
Nitendra's responsibility. If independent
capture IDs remain unavailable, retain the provisional benchmark label and
limit conclusions; do not claim the true-run recovery task is complete.

The first EVAL-02 component, outcome_metrics.py, implements only the full
two-by-three counts, supported ratios and explicit NA reasons from section 9.
It requires every planned labeled unit and an explicit final outcome; it
cannot verify external-file completeness without a later manifest-aware
adapter. It performs no scoring, policy selection, ranking or aggregation.
Its input signature is an internal utility, not an agreed teammate contract.
