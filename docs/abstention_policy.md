# Abstention policy - draft v0.2

**Status: AP-1 APPROVED; ABS-01 IN PROGRESS - 2026-11-16.**
This develops Gaurav's policy responsibility. EP-6 already approves the three
outcomes, quality-only baseline direction, missing-quality behavior, evaluation
accounting and file decision rule. Gaurav approved AP-1 completeness and equality
on 2026-11-16 (D020). Required KPIs, numerical cutoffs and security/coverage
constraints remain pending. No model
or degradation implementation is introduced.

References: [evaluation protocol](evaluation_protocol.md), sections 5 and 7-10;
[reviewed threat model](threat_model.md); [team dependencies](../planning/team_dependencies.md).

AP-2's [input and observability proposal](abstention_input_proposal.md) maps
verified local manifest fields to pending producer inputs. It is an unagreed
review draft, not a required-KPI selection or adopted API.

## 1. Purpose and applicability

Return BENIGN, ATTACK or ABSTAIN for every planned primary window. ABSTAIN
means insufficient supported evidence for classification. It is not benign,
successful detection, automatic mitigation or an assumed human response.
Truth labels enter evaluation only, never policy decision inputs.

The primary grid has 4,406 windows, including 74 retained tails, from 43,704
reports in 40 provisional source-file groups. Ten reports do not mean ten
seconds. The 1,540 secondary uncertain-clock rows remain outside this temporal
policy; an order-free secondary policy needs declared eligible inputs.
File groups are not proven independent captures.

## 2. Inputs and ownership - proposed concepts, not an agreed API

| Input concept | Purpose / owner | Requirement or unresolved point |
| --- | --- | --- |
| Planned window/file IDs and expected report references | Gaurav's fixed manifests | Preserve all planned cases and group/partition membership |
| Expected report count E_w | Gaurav's grid; operational source needs justification | Ten for full windows; actual clean tail length for tails, never automatically ten |
| Visible report/KPI masks before imputation | Marco's aligned conditions / agreed observation adapter | Available at decision time; no hidden injection labels or clean-test values |
| Required KPI set K and validity rules | Gaurav proposal agreed with Nitendra's model requirements | Pending; distinguish required/optional inputs, exclude identifiers/labels |
| Finite attack score and type/direction | Nitendra | Larger means more attack evidence; a raw score is not calibrated confidence |
| Short-input support/representation | Nitendra | Pending; no padding/masking or model support asserted |
| Frozen quality cutoff q_min and classifier threshold tau | Gaurav's selection ledger | Pending values; validation only, no invented defaults |

Clean reference IDs/counts support offline pairing. Their use as a policy
denominator requires an equivalent observable expected schedule/grid in the
intended setting. Otherwise required quality is unavailable. Do not claim
operational completeness is measurable from this archive alone.

An unset/unapproved KPI set, cutoff or score contract is an incomplete
experiment configuration: stop configuration validation. Do not manufacture
an all-ABSTAIN experiment to conceal unfinished policy design. Missing required
quality in an otherwise configured case yields ABSTAIN under EP-6.

## 3. Approved completeness measure - AP-1

For each required KPI k in K, let O_wk count distinct expected report positions
with an observed, valid value before imputation. Approved:

```text
c_wk = O_wk / E_w
q_w  = min(c_wk for k in K)
```

This checks the least-observed required KPI; healthy KPIs cannot conceal an
absent required one. AP-1 adopts this definition, with unknown KPI names and
validity contracts still gated. E_w must
be positive and K nonempty. Duplicates, padding, imputed values and reports
outside the expected grid cannot increase O_wk. Unknown mask/denominator
means unknown quality, not quality 1. Known missing values differ from unknown
metadata. Validity needs a typed contract; do not infer physical KPI bounds
from whole-dataset extrema.

Illustration only: two required KPIs observed at ten and six positions of a
ten-position window give q_w=0.6. This is neither a dataset result nor a cutoff.
A complete three-report tail would have q_w=1 with its three-position
denominator, but could still be unsupported by a model (SHORT_WINDOW).

No physical-time freshness/staleness/irregularity gate is proposed under the
raw-clock EP-3 policy. Constancy alone does not establish staleness. Confidence
gates remain deferred to supported calibration and a separately reviewed
extension; Nitendra owns calibration.

## 4. Decision rules and explanation

The approved EP-6 direction is:

1. Preserve each planned window, even if no observations/prediction arrive.
2. ABSTAIN for no usable observations, unsupported short input, missing/invalid
   score, unavailable required quality, or completeness below q_min.
3. Otherwise ATTACK if score >= tau; otherwise BENIGN.

Approved completeness acceptance is q_w >= q_min: equality passes. Numerical
q_min is pending. High attack scores do not bypass the quality gate. Retain
multiple known causes where applicable; reason precedence/schema remains a
proposal. Do not let NaN comparisons silently become BENIGN.

| Reason | Meaning | Status |
| --- | --- | --- |
| NO_OBSERVATIONS | No usable observations for a planned input | EP-6 concept approved; precise usability depends on required inputs |
| SHORT_WINDOW | Input shorter than the model supports | EP-4/6 approved; capability pending |
| INVALID_SCORE | Score absent, nonfinite or incompatible with agreed semantics | EP-6 concept approved; contract pending |
| QUALITY_UNAVAILABLE | Required mask/expected-count/quality metadata unavailable | EP-6 behavior approved |
| LOW_COMPLETENESS | Available completeness fails the reviewed rule | EP-6/AP-1 definition approved; cutoff pending |

Require an outcome for every planned case. Reject duplicate/unknown IDs;
align missing predictions to explicit missing-score cases. Contradictory
lineage/truth requires data validation, not silent removal.

File decisions follow EP-6: ATTACK if any accepted child window is ATTACK;
BENIGN only if every planned child is accepted BENIGN and at least one exists;
otherwise ABSTAIN. Missing children remain planned cases. The file ranking
score is maximum available window score with coverage disclosed; ranking is
separate from the quality-gated decision and cannot override abstention.
Use file_proxy_* until independent captures are verified.

## 5. Selection, freezing and reproducibility

No tau/q_min is selected. Agree inputs and quality definition first. Gaurav
must choose security/coverage costs or constraints before quality selection.
Do not set a convenient budget after test inspection or maximize retained
accuracy alone.

Use approved validation-only assessment-level utility:
U = 0.5 * (TP/N_A + TN/N_B). Abstentions remain in class denominators and earn
no TP/TN. EP-6 specifies >= score decisions, distinct boundaries including
all-attack/all-benign, and higher-threshold utility ties. Evaluate actual final
outcomes including quality gates/file aggregation; ranking performance is not
a substitute. Detailed quality-candidate search and its constraint/tie rules
remain pending ABS-01.

Save KPI/validity definitions, observable masks/counts, score/model identity,
split IDs, candidate choices, validation support, utility/coverage/constraint
results, selected parameters, reasons and configuration hashes. If infeasible,
report failure; do not silently relax constraints. Selection requires both
classes. Two Benign validation groups cannot justify very low-FPR guarantees.

Freeze model/policy/threshold before test. Use the same reference grid and
frozen policy for paired clean/degraded conditions, retaining completely
missing windows/UEs. No per-scenario test retuning. Marco owns scenario levels
and playback; Nitendra supplies model/calibration artifacts.

## 6. Reporting and later verification

Use the full EP-6 table: TP, FN, U_A, FP, TN, U_B. Report total/class coverage,
abstention, full attack detection TP/N_A, unresolved/missed attacks
(FN+U_A)/N_A, benign false positives, retained error and attack/benign
abstention separately. Undefined ratios remain NA with reasons. U_A is not
successful detection.

For abstained cases with scores, report counterfactual classifier errors
separately from unscorable cases; never fabricate them. AP/ROC on scored
cases need availability counts and paired common-score attrition; they do not
replace full-population security reporting.

The existing outcome_metrics.py tests accounting only. Later policy tests
must cover missing/invalid score/quality, no observations, threshold equality,
required/optional masks, tail denominators/support, wholly missing windows,
conservative file decisions and prevention of label/oracle inputs. No policy
execution or empirical policy evaluation is claimed here.

## 7. Pending decisions and acceptance gate

| ID | Pending choice / dependency | Next evidence |
| --- | --- | --- |
| AP-1 APPROVED | Minimum per-required-KPI completeness; equality passes | Gaurav approval 2026-11-16; D020 |
| AP-2 PENDING | Required KPIs, validity, score and partial-input contracts | Input proposal v0.1; Nitendra requirements, Marco observable masks/counts and Gaurav agreement still required |
| AP-3 | Security/coverage constraints, quality search and tie rules | Gaurav decision before validation selection |
| AP-4 | Numerical quality cutoff and classifier threshold | Supported validation evidence and frozen ledger |

ABS-01 remains in progress. Reviewing this draft cannot approve unknown
parameters/contracts. Next document AP-2's smallest supported input contract.
Do not implement a policy requiring invented inputs/cutoffs.

## 8. Limited AP-1 implementation

`src/reliability/completeness.py` computes completeness from explicit expected
position IDs and pre-imputation observed-valid masks. True is observed-valid;
False is known missing/invalid; None or absent mask entries mean unknown
metadata. Unknown required metadata yields quality unavailable, with known
counts retained. Optional KPIs are ignored. Invalid/duplicate configurations
and out-of-grid required masks fail. The helper does not establish mask
validity, operational observability or input provenance; callers must do so.
Its signature is internal, not an agreed producer contract. It chooses no
required KPIs or cutoff and emits no prediction or quality-gate decision.
The approved equality rule remains specified for later configured policy
execution. Synthetic tests are logic evidence, not empirical policy results.
