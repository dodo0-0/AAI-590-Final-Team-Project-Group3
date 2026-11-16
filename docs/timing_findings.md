# Source timing and metadata coincidence diagnostic — 2026-11-15

## Method and evidence boundary

`src/reliability/timing_audit.py` recomputes reconciliation, then reads the
original source order. A diagnostic identity group is one source path plus
`(cellid, ue_id, rnti)`. These groups are not run IDs. All source observations,
including missing/invalid identity or clocks, remain accounted for. Source
hashes are verified before/after inspection; no data are changed.

Timestamp units, epoch and timezone remain unverified. All steps and ranges
below use raw numeric units. No time conversion, gap threshold, imputation,
counter rates, row exclusion or evaluation split was introduced. Missing or
invalid timestamps break within-group adjacency. Rows without identity cannot
be assigned to a group, so adjacent identified observations are not guaranteed
to be consecutive physical reports.

Local artifact: `results/timing_audit_2026-11-15.json`. Notebook 03 presents the
same diagnostic by calling the module. External source review is separately
recorded in [provenance sources](provenance_sources.md); notebook execution has
no network dependency.

## Coverage, ordering and raw cadence

| Source folder | Diagnostic identity groups |
| --- | ---: |
| Benign | 14 |
| BruteForce | 4 |
| DDOS | 43 |
| DoS | 6 |
| Probe | 13 |
| Web | 8 |
| Total | 88 |

The 50,213 source objects comprise 44,452 observations in these identity
groups and 5,761 observations without usable identity. In this snapshot the
grouped observations all have finite numeric timestamps, and the ungrouped
observations are the metadata-free source records already identified.

Within each of the 88 groups:

- No backward timestamp step was observed in original order.
- No repeated timestamp was observed within the group.
- The median positive timestamp step is 1,000 raw units.

The largest positive step is 143,993 raw units in benign.txt; other groups
have different maxima. These are measurements of numeric spacing, not
boundaries or diagnosed telemetry failures. A 1,000-unit step is compatible
with one second if the unit is milliseconds; it does not independently verify
that interpretation or justify filling missing reports.

## Cross-file overlap checks

Compared 102 cross-file group pairs with exactly the same cell/UE/RNTI
identity and usable timestamp ranges. None had overlapping raw min/max ranges.
The diagnostic separately supports common-timestamp and exact
radio-plus-metadata multiplicity counts for overlapping intervals.

This result is limited to that identity key. Identifiers can change within
related captures or be reused across sessions. Zero such overlaps does not
prove independence or establish that the source files are true runs.
The 88 identity groups do not validate the preliminary 52 versus 42 run claims.

## Questionable DoS metadata: all tuples coincide elsewhere

For the 1,540 database rows with unique radio candidates but insufficient
source metadata, compared the actual database `(timestamp, ue_id, cellid,
in_sync)` against all source observations. No assumed constant cell ID or
wildcard was used. RNTI is not part of this separate four-field comparison.

Each of the 1,540 rows has exactly one coincident source observation in one
of the following other files:

| Metadata-free radio candidate source | icmp_nping.txt | slowloris2.txt | udp_nping.txt | Total database rows |
| --- | ---: | ---: | ---: | ---: |
| tcp-ack_hping3.txt | 199 | 213 | 236 | 648 |
| tcp-syn_hping3.txt | 243 | 272 | 253 | 768 |
| tcp_test.txt | 45 | 44 | 35 | 124 |
| Total | 487 | 529 | 524 | 1,540 |

None of those coincident source observations also agrees on all 16 radio
values. Thus these are metadata coincidences with different radio vectors,
not repeated copies of an identical compared measurement. Detailed source
line and database row references are retained in the local report.

This pattern raises a specific association/provenance concern. It does not
prove copying, synthetic timestamps, incorrect labels, synchronization error,
or any particular author processing mechanism. Source records without clocks
cannot authenticate those populated database timestamps. Clock and identity
validation remain required before temporal evaluation of these rows.

## Consequences and next review gate

The source-order and coincidence diagnostics are complete for this snapshot.
Authoritative metadata origin and capture independence remain unresolved.
The local archive and inspected author repository snapshot did not resolve
the current summary's metadata population; see the scoped source review.

Obtain available team/author exporter scripts, capture manifests and Kaggle
revision. Before approving an evaluation contract, Gaurav should review any
fallback clock interpretation, grouping or population restriction, with the
unverified DoS rows explicitly accounted for. No such choice has been made
by this diagnostic, and no teammate model/degradation implementation changed.

## Follow-up: database-clock projection, not observed source chronology

With no team export notes available, examined the questionable metadata using
src/reliability/metadata_provenance.py. For each unique radio candidate, placed
its database timestamp into the physical line order of the matching source.
Those clocks remain database values, not timestamps present in the source.
Physical file order is not independently authenticated event order.

| Radio candidate source | Rows | Distinct metadata tuples | Within-file repeat excess | Backward projected steps | Forward steps | Zero steps |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| tcp-ack_hping3.txt | 648 | 572 | 76 | 317 | 330 | 0 |
| tcp-syn_hping3.txt | 768 | 655 | 113 | 383 | 383 | 1 |
| tcp_test.txt | 124 | 121 | 3 | 60 | 63 | 0 |

Across the three files, 1,540 rows use 1,143 distinct four-field metadata tuples
(397 occurrences beyond one per distinct tuple). Per-file distinct counts do
not sum to the global count because tuples repeat across files. The 760
backward steps are projected database clocks, not reversals in original source
clocks. This does not contradict the zero-reversal observed-source finding.

Reuse and nonmonotone projected clocks strengthen the provenance warning.
Metadata reassignment/resampling is a possible explanation, not an established
procedure. Do not infer a random seed, repair clocks or call actual event times
recovered. Exact metadata origin remains unresolved. Evidence:
results/metadata_projection_2026-11-15.json and notebook 03 section 9.

## Review of Gaurav's saved notebook 03 — 2026-11-15

All nine substantive code cells have saved outputs with execution counts 1-9
and no errors. A fresh independent read-only timing calculation and projected-
clock summary matched both prior complete JSON artifacts. All seven saved
data tables (coverage, median steps, largest steps, coincidence multiplicity,
coincident source pairs, archive extensions and projected clocks) matched
fresh values. Saved code/report hashes also agree. Inputs and notebook were
preserved. Evidence: results/timing_saved_output_review_2026-11-15.json.

There is no contradiction between zero backward steps in observed source
identity groups and 760 backward steps in database clocks projected onto
metadata-free candidate source records. These concern separate clock evidence.
Reuse comprises 1,143 distinct tuples over 1,540 questionable rows (397 excess
occurrences). This verifies the diagnostic outputs, not the generating
mechanism, clock authenticity or independent-run identities.
