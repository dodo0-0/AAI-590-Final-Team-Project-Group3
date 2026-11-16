# Threat model - reviewed bounded model v1.0

**Status: BOUNDED ANALYTICAL MODEL ACCEPTED - 2026-11-15.** This is an offline
radio-telemetry security/reliability study, not a verified deployment design.
Gaurav accepted v0.2 with its stated limitations. Version 1.0 records that
review without changing the analytical assumptions. The model uses local evidence and approved EP-1
through EP-6 definitions. It introduces no new attack experiment or teammate
implementation.

## 1. Protected system and objectives

The project brief identifies NetsLab-5GORAN-IDD v2 and radio-based intrusion
detection. Protected interests considered here are reliable operator security
decisions and network-service availability. Availability motivates the work;
this evaluation does not directly measure protection of network services.

The studied pipeline consumes recorded radio measurements, produces attack
scores and returns BENIGN, ATTACK or ABSTAIN. The approved task is Benign versus
any supported attack scenario. Report detection, false alarms, coverage and
unresolved attacks together. Classification does not establish exploit success,
causal attribution, prevention or mitigation. No automated response is assumed.
The observed research boundary starts at extracted files; upstream collection
is contextual and remains incompletely documented.

## 2. Evidence register

| ID | Inspected basis | Established fact or decision | Limit |
| --- | --- | --- | --- |
| E1 | [Structural audit](data_audit_findings.md) | 45,244 database rows, 49 source JSONL files, 50,213 source objects; no explicit database source/run-ID column | Field names/counts do not authenticate capture lineage or KPI semantics |
| E2 | [Reconciliation](reconciliation_findings.md) | 43,704 unique radio-plus-metadata source/database candidate pairs; 1,540 other database rows have unique radio candidates without source clocks/identity metadata | Correspondence is not independent-capture or scenario-truth verification |
| E3 | [Timing and projection audit](timing_findings.md) | Questionable database metadata coincide with other source observations; projected database clocks have backward steps | Does not establish malicious tampering, a merge algorithm or observed source-clock reversal |
| E4 | [Provenance review](provenance_sources.md) | Extracted content is hash-identified; inspected public-code snapshot did not resolve metadata origin; Gaurav has no revision/export notes available | Original clock semantics, processing history and capture IDs remain unknown |
| E5 | [Evaluation protocol v1.0](evaluation_protocol.md), D012-D017 in [decisions](decisions.md) | EP-1 through EP-6 approved: populations, provisional groups, raw clocks, retained-tail windows, splits and binary metrics | Approval is not measured performance or an agreed producer API |

Artifacts, code identities and executed checks are recorded in these reports
and the [progress log](progress.md). Earlier meeting claims about one-second
sampling, 52 reconstructed versus 42 paired runs, recording-day confounding
and a fixed number of informative features remain hypotheses where unverified.
This revision adds no new external literature or deployment-topology review.

## 3. Assets, observation points and trust boundaries

Relevant assets are measurement integrity/availability, source and label
lineage, held-out evaluation integrity, and honest security decision reporting.
Subscriber privacy and infrastructure access controls are not experimentally
evaluated here.

```text
Network activity -> radio measurements -> collector/export
            [placement, E2 mapping and timing semantics unverified]
            -> source JSONL / summary database
            -> cohort/group/window/split manifests
            -> Nitendra's preprocessing/model and scores
            -> Gaurav's evaluation/abstention -> reported outcome
```

Marco supplies proposed aligned degradation/playback conditions at an agreed
interface. Its exact insertion point and operationally observable metadata
remain proposals. Dataset rows are not authenticated E2 reports. RU/DU/CU/RIC
placement, E2 service model and reporting configuration have not been verified
from inspected files. The conceptual diagram asserts no deployed component/API.

| Boundary | Required trust/check | Consequence and handling |
| --- | --- | --- |
| B1: activity to measurements | Measurements contain relevant evidence of the labeled scenario | A separable radio signature may not exist; no causal attack-effect claim |
| B2: measurement to collection/export | Identity, schedule, ordering and event/arrival clocks have known meanings | Loss, delay and staleness can be confused; raw units only, quality semantics gated |
| B3: files/database to population | Correspondence, labels and capture linkage are defensible | Misassociation/dependence biases evaluation; preserve hashes, lineage and uncertain cohort |
| B4: data to learned artifacts | Groups remain separated; fitting uses training only; metadata do not become predictors | Leakage and shortcuts inflate scores; require frozen partitions and preprocessing provenance |
| B5: scores/quality to decision | Score direction, available quality and planned-case coverage are explicit | Missing evidence may appear benign; preserve ABSTAIN and full denominators |
| B6: decisions to claims | Cohort, family support, abstained attacks and uncertainty are reported | Selective reporting overstates security; limit low-FPR, run-independence and mitigation claims |

Hashes detect changes relative to recorded local content. They do not
authenticate original measurements, labels or collection security.

## 4. Scenario labels and bounded attacker model

Literal database categories are Benign, BruteForce, DDoS, DoS, Probe and
Web Attacks (E1). Benign is a reference scenario. Attack categories represent
dataset scenario labels, not verified exploit outcomes. Folder names and
tool-like filenames alone do not establish attack execution details.

The bounded analytical attacker is a network-activity originator associated
with the labeled attack scenarios. Location, access path, compromised hosts,
privileges, target, rates, coordination and UE control are **unknown**. A DoS
label does not establish RAN infrastructure access. A measured UE in an attack
file is not necessarily an attacker. More specific capabilities need capture
documentation; the draft does not supply them by inference.

Attacker control of collectors, E2 messages, clocks, labels, model training or
decision interfaces is not assumed. Infrastructure compromise, malicious
telemetry forgery, poisoning, adversarial query/evasion and active mitigation
are outside current experiments. These are scope limits, not impossibility
claims.

EP-1 primary coverage is 43,704 rows. Its DoS examples include ICMP/UDP/Slowloris
labels but exclude all current database DoS_ACK (648) and DoS_SYN (892) rows.
Those 1,540 rows remain secondary non-temporal diagnostics. Primary results
cannot establish temporal ACK/SYN detection. Six broad category names do not
preserve every attack mechanism. Source-only records remain inventoried;
adding them requires a reviewed population/label amendment.

## 5. Observation failures and benign conditions

These are candidate reliability conditions, distinct from attack labels.
Their presence or cause in a live system is not established here. Telemetry
loss is not presumed malicious.

| Condition | Evaluation concern | Required evidence/metadata |
| --- | --- | --- |
| Dropped reports / reduced frequency | Missing evidence changes detection and coverage | Expected grid/schedule, visible masks and Marco's justified scenario |
| Stale/repeated values | Old observations may appear current | Age/provenance or justified stale-injection metadata; constancy alone is insufficient |
| Missing UE observations | Partial observations appear complete | Expected UE inventory or an operationally available equivalent |
| Delay / irregular arrival | Decision-time evidence differs from event order | Event/arrival clocks, units and a causal availability rule |
| Missing KPIs / invalid score | Decision input is unsupported | Agreed input contract and observable missingness/reason codes |
| Benign load/environment change | Distribution shift resembles attack scenarios | Suitable controls/documented captures; current coverage unknown |

Marco owns degradation generation, realism and playback; Gaurav specifies
reliability evaluation and abstention. No numerical degradation severity or
physical-time freshness cutoff is adopted here. Report-count omissions do not
prove packet loss or a particular E2 failure. Retained partial tails are known
short inputs, not evidence of telemetry loss; unsupported tails are SHORT_WINDOW
abstentions under EP-4. Hidden clean references/injection labels cannot serve
as policy quality inputs unless operational observability is established.

## 6. Assumptions and interpretation constraints

| ID | Assumption or unresolved requirement | Consequence if unsupported |
| --- | --- | --- |
| A1 | Archive scenario labels serve as supervised references | Interpret as scenario discrimination; no event-level exploit ground truth |
| A2 | Whole source files are provisional split groups; established capture links require merging (EP-2) | File-disjointness is not capture independence; revisit affected partitions before further experiments |
| A3 | Raw timestamp units/source order only (EP-3) | No UTC dates, per-second rates, hourly alarms, freshness duration or time-to-detection claims |
| A4 | IDs/labels/audit timestamps remain metadata; counter and feature semantics need validation | No unverified rate conversion or assumption that every numeric field is eligible |
| A5 | Training-only fitted transforms; validation-only operating selection | Test-motivated changes are post hoc and cannot preserve a fresh-holdout claim |
| A6 | All planned labeled cases remain visible, including missing scores/tails | Missing predictions cannot count as benign or successful defense |
| A7 | Required quality metadata are observable at decision time | Missing metadata remain explicit; policy cannot use hidden oracle information |

Recording-day/environment shortcuts are a concern, not an established account
of model behavior. Calendar-date diagnostics are deferred by EP-3. Even with
validated dates, inseparable date/class support cannot identify an independent
attack effect. Feature contrasts/date-prediction diagnostics need verified
semantics and Nitendra's agreed outputs; this draft does not implement them.

There are ten primary Benign file groups, allocated six/two/two to
training/validation/test. They are not ten verified independent captures.
Two validation/test Benign groups cannot establish very low false-alarm rates.
Training CV supports both binary classes, but one fitting fold lacks primary
DoS; complete multiclass CV coverage is not established.

## 7. Risk-to-evaluation matrix

Priority expresses consequence for research validity, not measured likelihood
or operational risk. These entries connect existing work, not new experiments
or completed empirical results.

| Risk | Boundary / consequence | Priority | Evaluation/control | Residual limit / ownership |
| --- | --- | --- | --- | --- |
| R1: uncertain clocks/lineage | B2/B3: misleading sequence/population | High | E2/E3; EP-1 separation, EP-3 raw clocks, hashes and retained secondary cohort | Origin unknown; Gaurav documents limits |
| R2: related captures across groups | B3/B4: optimistic held-out scores | High | Whole-file groups, merge established links, fixed splits/CV (EP-2/5) | Capture independence unknown; Gaurav owns evaluation grouping |
| R3: date/identity/environment shortcuts | B4: correlates mistaken for attack evidence | High | Metadata exclusions; verified feature groups and planned support/shortcut contrasts | Confounding may prevent contrasts; Nitendra supplies models |
| R4: preprocessing/test leakage | B4: biased comparison | High | Training-only transforms, fixed folds, validation-only threshold rule (EP-5/6) | Await Nitendra learned-artifact provenance |
| R5: missing/stale/less frequent observations | B2/B5: missed attacks/false alarms | High | Paired aligned conditions, fixed evaluation grid, all-case accounting | Marco owns scenarios; arbitrary levels do not prove E2 realism |
| R6: attack-concentrated abstention | B5/B6: retained accuracy hides misses | High | EP-6 two-by-three table, class coverage, (FN+U_A)/N_A | KPIs, cutoffs and budgets pending ABS-01; Gaurav owns policy |
| R7: score/aggregation mismatch | B5: inconsistent alarms | High | Agreed score type/direction, report-mean and file-max rules, conservative file decisions | Nitendra adapter and partial-input support pending |
| R8: unsupported generalization | B6: inflated low-FPR/causal/run-level claims | High | File-proxy units, family support, explicit NA and conditional uncertainty | No proven independence, cross-site transfer or mitigation evidence |

## 8. Ownership and review gate

Gaurav owns threat analysis, evaluation definitions, abstention policy and
interpretation. Nitendra owns models, learned preprocessing and calibration.
Marco owns degradation/playback. Interfaces remain proposals until agreed;
this draft transfers no implementation ownership.

Gaurav selected **Accept the bounded model and stated limitations (Recommended)**
on 2026-11-15. The bounded analytical review gate is satisfied.
Unavailable capture/topology information remains unknown even after review;
approval cannot turn assumptions into verified deployment knowledge.

Accepted review scope (the reviewed questions are retained below):

1. Does the bounded offline scope and exclusion of unsupported attacker
   capabilities match the intended study?
2. Are factual claims supported by E1-E5, with missing deployment/capture
   evidence explicit?
3. Do risks map to evaluation/abstention work while preserving teammates'
   model and degradation ownership?

Next, draft the dedicated abstention-policy specification using EP-6. Quality
inputs, numerical cutoffs and security/coverage budgets remain pending; no
threshold or performance result follows from this threat model alone.
