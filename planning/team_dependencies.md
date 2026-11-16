# Team dependencies and proposed handoffs

These are information requests and interface topics, not agreed contracts.
Gaurav must approve definitions and interfaces before implementation depends
on them. No messages have been sent to teammates by this assistant.

| Owner | Needed information/artifact | Enables |
| --- | --- | --- |
| Gaurav/team | Local radio data now present and hash-identified; Kaggle revision unavailable to Gaurav; no team exporter/capture notes available | Continue independent evidence assessment; do not wait for assumed existing team artifacts |
| Gaurav/team | Recording manifest with source capture/run/date/timezone, paired radio/network mapping if available | Independent grouping and class/date support assessment |
| Nitendra | Eligible model inputs, window length/stride, label convention, score/class mapping, split IDs, preprocessing provenance and calibration plan | Compatible evaluation and confidence policy; prevent cross-boundary windows |
| Marco | Observation point, available quality metadata, clean/degraded alignment, scenario semantics and justified levels/seeds | Paired quality/robustness evaluation without assuming E2 realism |
| Gaurav | Review threat assumptions, evaluation unit/aggregation and abstention objective once data support is known | Freeze research definitions before held-out evaluation |

Proposed discussion fields: stable run and window identifiers; event and
arrival timestamps with units/timezone; true label and attack score meaning;
scenario and seed; telemetry-quality fields with explicit unavailable values.
Availability of any field is unknown. Retain run/date identifiers as audit
metadata, never model predictors. Calibration belongs to Nitendra; degradation
generation belongs to Marco. Gaurav's utilities consume agreed outputs.

2026-11-15 clarification: Gaurav reports he is the only person who has started
the work. Nitendra/Marco handoffs remain future dependencies, not claims that
their components exist. Their implementation ownership is unchanged. Unknown
processing history must be investigated or bounded as a limitation; do not
reconstruct it as established fact.

The [evaluation protocol](../docs/evaluation_protocol.md) records approved
EP-1 through EP-6 definitions and proposed handoff field concepts. Definitions
are approved; this document does not assert an agreed producer API.
Window/score/calibration requirements need Nitendra's agreement, and causal
quality metadata, scenario alignment and justified levels need Marco's.

The [reviewed bounded threat model](../docs/threat_model.md) separates inspected file
evidence from unresolved deployment/attacker assumptions. It adds no capture,
model, degradation or playback implementation requirement. Gaurav accepted
the bounded model and limits on 2026-11-15; topology/capture facts remain unknown.

The [abstention-policy draft](../docs/abstention_policy.md) proposes input
concepts, not a producer API. Required KPI/validity and short-input support
need Nitendra agreement; observable masks and expected counts need Marco's
agreement. Gaurav approved AP-1 completeness on 2026-11-16; quality/security
settings remain pending. The internal completeness helper does not establish
producer field names, mask validity, observability or a numerical cutoff.

AP-2's [input proposal](../docs/abstention_input_proposal.md) maps actual
manifest/schema evidence and lists the unresolved Nitendra/Marco handoffs.
No required KPI list or producer representation is adopted. Agree a small
example export and its lineage/missingness semantics before implementing a
producer adapter. This is a local review document; no teammate message was sent.
