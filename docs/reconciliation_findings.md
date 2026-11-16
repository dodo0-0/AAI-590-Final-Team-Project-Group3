# Source/database reconciliation diagnostic — 2026-11-13

## Question and reproducible method

Which source occurrences agree with database rows, and can that account for
the count mismatch without inventing timing or choosing arbitrary matches?

`src/reliability/reconciliation.py` reads all six current classes, using the
inventory/extraction manifest to verify inputs before inspection and checking
all input hashes afterward. SQLite access is read-only. The local detailed
artifact is `results/radio_reconciliation_2026-11-13.json`.

Two explicitly fixed projections compare fields without class labels:

- `radio_exact`: dlBytes, dlMcs, dlBler, ulBytes, ulMcs, ulBler, ri, phr,
  pcmax, rsrq, sinr, rsrp, rssi, cqi, pucchSnr and puschSnr (16 fields).
- `radio_metadata_exact`: those fields plus timestamp, ue_id, cellid, in_sync
  and literal rnti (21 fields).

No rounding/tolerance is applied. Integer and float representations of the
same exact numeric value agree through rational representation. Numeric
strings and booleans are not coerced. Missing/null/invalid comparison fields
make a key unusable, never a wildcard. PMI representations are not converted
or compared. Agreement on a projection is not equality of every raw field.

All occurrences of each key are indexed together. A group with one occurrence
on each side is a unique candidate pair. A group with occurrences on both
sides and multiplicity greater than one on either side remains ambiguous.
No candidates are consumed or matched by order. Usable keys absent on the
other side are recorded as no candidate. Every occurrence is accounted for.

The report contains original relative paths and physical source line numbers,
database row references and labels, and candidate groups for both projections.
Source IDs and SQLite rowids are report-local references, not independent
capture/run IDs. Source folder/category aliases are used only to check label
agreement after comparison, not to force candidate matches.

## Actual-data results

| Profile / side | Unique candidate pair | Ambiguous group occurrences | No candidate | Unusable key | Total |
| --- | ---: | ---: | ---: | ---: | ---: |
| Radio / source | 44,819 | 425 | 4,969 | 0 | 50,213 |
| Radio / database | 44,819 | 425 | 0 | 0 | 45,244 |
| Radio + metadata / source | 43,704 | 0 | 748 | 5,761 | 50,213 |
| Radio + metadata / database | 43,704 | 0 | 0 | 1,540 | 45,244 |

Every database row has at least one exact radio-value source candidate. The
425 ambiguous occurrences on each side form 61 repeated radio-key groups,
all associated with Benign. Adding metadata yields unique candidate pairs
for all 10,664 database Benign rows. Repeated telemetry values are not proof
of duplicated captures, staleness or cross-file dependence.

Neither projection found a folder/category disagreement among its unique
candidate pairs after the stated DDOS/DDoS and Web/Web Attacks aliases. This
does not validate subtype semantics, binary-label consistency, attack timing
or the authenticity of the labels.

## DoS: the mismatch is now localized

| Source file | Source records | Unique radio candidates | No radio candidate |
| --- | ---: | ---: | ---: |
| icmp_hping3.txt | 1,125 | 0 | 1,125 |
| icmp_nping.txt | 1,037 | 1,037 | 0 |
| slowloris.txt | 1,007 | 0 | 1,007 |
| slowloris2.txt | 1,104 | 1,104 | 0 |
| tcp-ack_hping3.txt | 648 | 648 | 0 |
| tcp-syn_hping3.txt | 768 | 768 | 0 |
| tcp_npig.txt | 748 | 0 | 748 |
| tcp_test.txt | 124 | 124 | 0 |
| udp_hping3.txt | 586 | 0 | 586 |
| udp_nping.txt | 1,040 | 1,040 | 0 |
| Total | 8,187 | 4,721 | 3,466 |

All 1,540 database DoS rows with NULL rnti have unique radio-value candidates
in these source files:

- tcp-ack_hping3.txt: 648, database subtype DoS_ACK.
- tcp-syn_hping3.txt: 768, database subtype DoS_SYN.
- tcp_test.txt: 124, database subtype DoS_SYN.

Those source records lack timestamp, ue_id, cellid, in_sync and rnti. Database
timestamps and other populated metadata for these candidate pairs cannot be
validated from those source records. The diagnostic does not establish how
that metadata was obtained. Do not call it measured, synthetic or erroneous
without additional evidence.

The other 3,181 DoS database rows have unique agreement on both radio and all
five compared metadata fields. The 748 timestamped records in tcp_npig.txt
have no exact radio counterpart in the entire current database, not just its
DoS partition. The count mismatch therefore is not simply removal of records
without timestamps. Timing provenance remains a gate for rate conversion and
run reconstruction; no eligibility/exclusion decision is made here.

## Probe and remaining classes

The 573 timestamped records in portscan_udp.txt have unique candidates under
both projections; its 569 metadata-free records have no exact radio candidate.
All other Probe files have unique candidates under both projections. This
accounts for the observed Probe count difference on the compared fields.

Benign's unmatched radio records are benign_10.txt (900) and benign_test.txt
(34), both lacking metadata. BruteForce, DDoS and Web source occurrences all
have unique candidates under both projections. These observations describe
this snapshot; they do not establish general processing rules for the dataset.

## Interpretation and next gate

The 4,969 unmatched radio source occurrences account for the raw count gap
without discarding anything from the audit. Candidate agreement is strong
evidence of correspondence on the stated fields within these files, not an
authoritative lineage manifest or evidence of independent runs. PMI equality,
source collection boundaries, overlapping files, event clock semantics and
independence still require validation. None of the preliminary 52 reconstructed
versus reported 42 paired runs has been confirmed.

Next investigate metadata provenance for the 1,540 DoS rows through author
processing scripts/capture documentation. Timestamp-order, overlap and cadence
diagnostics can then describe supportable source streams without assigning
runs. Any fallback grouping, population restriction or exclusion requires
Gaurav's decision. No evaluation split, training, degradation or abstention
policy has been created by this diagnostic.

## Saved notebook output review — 2026-11-15

Reviewed Gaurav's saved notebook 02 without modifying or rerunning it. All
seven nonempty code cells have saved outputs (execution counts 1-7), with no
saved errors; one trailing empty cell is harmless. Environment output reports
rocm-jupyter Python 3.11.14 / SQLite 3.51.0.

A fresh independent read-only reconciliation reproduced the complete prior
JSON report. The saved report/code hashes, four summary rows, both database
category tables, both DoS/Probe source tables and the three metadata-gap rows
all matched independently computed values. All 50 input hashes were unchanged.
Local evidence: results/reconciliation_saved_output_review_2026-11-15.json.

This verifies the reported candidate comparisons; it does not authenticate
the metadata missing from source records or establish independent runs.
Unusable metadata keys remain distinct from absent radio candidates. No
grouping, exclusion or preprocessing decision was made during this review.
