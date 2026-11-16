# AP-2 input and observability proposal - v0.1

**Status: UNAGREED REVIEW DRAFT - 2026-11-16.** This document proposes the
smallest handoff needed for Gaurav's [abstention policy](abstention_policy.md).
It assigns no model, calibration, degradation or playback implementation to
Gaurav. Field concepts below are discussion points, not an adopted file format
or producer API. AP-1 defines completeness; it does not select required KPIs.

## 1. Verified local inputs and unresolved inputs

Inspected the current cohort/window/split JSON structures and SQLite column
names read-only. Artifact hashes and structural checks are recorded in
results/abstention_input_proposal_validation_2026-11-16.json. This check adds
no model scores, raw-feature statistics or deployment evidence.

| Input concept | Available local evidence | Limit / required agreement |
| --- | --- | --- |
| Planned window identity | Window manifest: window_id, source_path, provisional_group_id | Stable offline references, not observed live capture IDs |
| Expected report positions/count | report_references contains database_rowid and source_line; expected_report_count and is_partial are explicit | Clean retained grid only; live expected schedule remains unverified |
| Cohort/lineage | Cohort rows: cohort, source_path/source_line, lineage_basis, provisional_group_id | Primary 43,704 rows; secondary 1,540 outside temporal grid; capture independence unknown |
| Frozen partitions | Split manifest: window_assignments has partition and training_cv_heldout_fold | Evaluation metadata only; never model predictors |
| Labels | traffic_type, attack_category, attack_subcategory | Evaluation truth only; never policy inputs or quality features |
| Raw radio fields | Database column names inspected; source schema varies as documented in the audit | Presence is not feature eligibility, physical validity or a required-KPI decision |
| Attack score/type/direction | No Nitendra score artifact has been agreed or inspected for this proposal | Nitendra supplies semantics, provenance and failure behavior |
| Model support for short inputs | Manifest retains 74 tails | Nitendra specifies supported lengths and encoding; completeness does not establish support |
| Observed-valid masks | No Marco producer/mask contract has been agreed or inspected | Marco and Nitendra establish observable masks and validity; no mask is manufactured here |
| Arrival time, schedule, expected UE population | No verified operational contract from inspected schema/manifests | No freshness, delay, missing-UE or live completeness claim |

The grid has 4,406 windows in 40 source-file groups. Counts of planned
positions sum to 43,704. All tails keep their actual expected length. These
are offline evaluation facts, not evidence that each report was received
successfully or that every KPI value is physically valid.

## 2. Minimum alignment proposal

Use the existing window_id as the common reference across scores, quality
and clean/degraded conditions. Preserve every planned window, including
all-missing windows. Keep the source file/group and partition in Gaurav's
manifest; do not let a producer redraw groups or renumber surviving windows.

Within a window, propose a stable position reference derived from its
existing database_rowid, accompanied by the source-line reference for audit.
The completeness helper uses opaque string position IDs; conversion from
manifest references must be agreed before an adapter is implemented. Database
row IDs are snapshot-specific references, not features or authenticated events.

For each evaluated condition, distinguish window, model/configuration and
scenario/realization identities. Multiple models or realizations may legitimately
share window IDs; uniqueness applies within the agreed context. Attach code,
configuration and parent-manifest hashes so incompatible snapshots cannot join.
Representation and exact field names remain pending.

Reject contradictory/unknown references or duplicates within a context.
Expected cases absent from a producer result remain in the evaluation ledger
with missing-score/quality status; do not inner-join them away. Separate
evaluation truth from policy inputs. This is a proposed adapter requirement,
not an implemented loader.

## 3. Questions for Nitendra - model and score contract

| Needed decision | Requested information | Why Gaurav needs it |
| --- | --- | --- |
| Required versus optional inputs | Exact input names per model/feature condition, transformations and permitted missingness | Define the required KPI set without choosing model features on his behalf |
| Validity | Which raw values are valid, missing or invalid; evidence for any bounds/sentinels | Build pre-imputation masks without whole-dataset extrema or guessed physics |
| Score semantics | Finite attack score, increasing direction, raw/probability type, class mapping and missing-score status | Apply approved aggregation/threshold rules without assuming confidence |
| Row/window adaptation | Row baseline report scores versus sequence window scores; aggregation compatibility | EP-6 report-mean/window rule must match actual exports |
| Partial windows | Supported lengths, masks/encoding, unsupported-input status | Retain tails and apply SHORT_WINDOW when unsupported |
| Fitting provenance | Input feature/config identity, training-group IDs, transform/model/calibrator identity | Verify training-only fitting and fixed comparisons |

The known radio-comparison fields are dlBytes, dlMcs, dlBler, ulBytes, ulMcs,
ulBler, ri, phr, pcmax, rsrq, sinr, rsrp, rssi, cqi, pucchSnr and puschSnr.
This list describes the existing comparison projection, **not required K** or
an approved model feature set. Byte-counter semantics and transformations
remain unresolved. IDs, timestamp and label fields remain audit metadata;
source pmi variants need semantic resolution rather than guessed mapping.

Propose identifying K per declared model/feature condition, with the distinction
between the same completeness formula and different required inputs visible
in comparisons. Whether a common quality-KPI set is preferable must be reviewed;
no cross-model quality convention is adopted here.

## 4. Questions for Marco - observable quality and pairing

Request an agreed mapping to the fixed window/report references, scenario and
realization identity, expected-count provenance, and pre-imputation visible
report/KPI masks. For each quality indicator, document whether it is observable
at decision time, inferred from a justified schedule or known only to an
injection harness. Harness-only condition labels and clean values are for
evaluation/pairing, not policy inputs.

For AP-1's internal helper, True means observed-valid, False means known
missing/invalid, and None/absent metadata means unknown. Marco/Nitendra must
agree how their outputs map to those states; this does not impose that Python
representation on their producers. Removing a report from an array without
retaining its expected position is insufficient to distinguish loss from
unknown coverage. Padding/imputation cannot restore an observed-valid mask.

Do not infer that raw timestamps are arrival times, that identity fields define
an expected UE inventory, or that constant values imply stale data. EP-3 still
defers physical-time gates. Scenario levels, causal semantics and playback
remain Marco's work.

## 5. Agreement and implementation gate

AP-2 remains pending. Before implementing a producer adapter or configured
quality policy, record Gaurav's agreement and the relevant producer's agreement
on the input concepts, required/optional KPI set, validity, position alignment,
missing/unknown behavior, score semantics and partial-input support. Record
unavailable capabilities explicitly; no one has been contacted by this task.

Then inspect a small producer-supplied example against the fixed manifest,
including a full window, a tail, a known missing required value, unavailable
quality and a missing score. These are requested acceptance cases, not claims
that exports already exist. Reject unknown or contradictory IDs; preserve
planned cases and metadata provenance. Do not mark AP-2 complete on this
draft alone.

AP-3 security/coverage constraints and quality-search rules remain a separate
Gaurav decision. AP-4 numeric thresholds need validation evidence. No required
KPI list, producer schema, adapter, mask-generation algorithm or numerical
policy setting is adopted by this proposal.
