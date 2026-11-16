# Tests

`test_data_audit.py` uses explicitly synthetic fixtures, not dataset evidence.
It covers missing database files, quoted SQL identifiers, missing/null fields,
malformed JSONL and physical error line numbers, invalid numeric timestamps,
determinism, extraction-manifest mismatches, missing sources and protection
against writing audit output into the input directory.

Run from the project root with `.\.venv\Scripts\python.exe -m pytest`.
Empirical validation is separate: run the audit on the extracted files and
inspect its report and limitations. Passing logic tests does not validate
dataset labels, timestamp semantics or independent runs.

`test_reconciliation.py` checks exact numeric agreement without rounding,
repeated candidate multiplicity on either side, unusable/missing fields,
label-independent keys, metadata disagreement, occurrence accounting,
duplicate reference IDs, a read-only synthetic end-to-end pipeline and output
path protection. Fixtures deliberately include a category disagreement and
metadata-free source data to prevent silent label forcing or wildcard joins.

`test_timing_audit.py` exercises original-order reversal detection, repeated
times, missing-clock adjacency, separation of interleaved UEs, interval overlap
without shared samples, multiplicity of shared observations, exact identity
comparison, retained metadata-coincidence locations and read-only ZIP listing.
Synthetic timestamps have arbitrary units and never stand in for capture data.

`test_metadata_provenance.py` verifies projected source-line order versus
database order, tuple multiplicity across files, missing-clock adjacency,
input preservation and rejection of duplicate candidate references.

`test_cohort_manifest.py` checks primary/secondary membership, whole-file
grouping, transitive evidence-bearing links, invalid or ambiguous lineage,
inconsistent candidate profiles and changed input snapshots. No synthetic
fixture is evidence of actual capture independence.

`test_window_manifest.py` checks interleaved UE separation, exact row accounting,
tail retention, deterministic IDs, linked files kept in separate windows,
unselected-interior guards, non-increasing clocks, mixed labels, snapshot
changes and rejection of files spread across groups.

`test_split_manifest.py` checks group disjointness, binary support, training-only
CV, row/window coverage and tails, reproducibility independent of record order
or unused score fields, infeasible support, label/group inconsistencies, wrong
parent references and input/manifest snapshot mismatches.

`test_outcome_metrics.py` checks a hand-computed full two-by-three table,
full versus retained denominators, abstained attacks receiving no detection
credit, all-abstain/empty/one-class inputs, explicit NA reasons, invalid or
missing outcomes and order invariance. These are synthetic logic tests;
they do not measure a model or implement a quality policy.

`test_completeness.py` checks AP-1's minimum across required KPIs, fully missing
versus unknown masks, optional KPI exclusion, actual tail denominator, partial
unknown counts, duplicate/out-of-grid configuration guards, strict mask values
and order invariance. Inputs are synthetic pre-imputation masks; the tests do
not establish KPI validity, mask provenance or operational observability.
