# Initial structural inventory — 2026-11-13

Scope: actual extracted current-class radio files only. Evidence is the
machine-readable `results/radio_inventory_2026-11-13.json`, generated using
`src/reliability/data_audit.py` (command in README). Inputs are identified by
relative paths, sizes and SHA-256 in that report and the extraction manifest.
No external paper or meeting assertion was used to derive these counts.

## Observed database structure

`Lower_Layer_Data.db` contains one user table, `lower_layer_data`, with
**45,244 rows and 25 columns**: 22 non-label columns plus `traffic_type`,
`attack_category`, and `attack_subcategory`. The 22 non-label columns include
identifiers/timestamp and must not be called 22 eligible model predictors.
There is no explicit source filename or run-ID column in this schema.

| Database attack_category (literal) | Rows | Source folder | Source objects | Source objects with finite numeric timestamp |
| --- | ---: | --- | ---: | ---: |
| Benign | 10,664 | Benign | 11,598 | 10,664 |
| BruteForce | 3,057 | BruteForce | 3,057 | 3,057 |
| DDoS | 15,084 | DDOS | 15,084 | 15,084 |
| DoS | 4,721 | DoS | 8,187 | 3,929 |
| Probe | 8,445 | Probe | 9,014 | 8,445 |
| Web Attacks | 3,273 | Web | 3,273 | 3,273 |
| Total | 45,244 | All six | 50,213 | 44,452 |

Folder names provide provisional source categories, not verified per-record
labels. Equal category counts are not proof that rows match. Differences
cannot yet be attributed to filtering, deduplication, relabeling or synthetic
timestamps. In particular, the database has 792 more DoS rows than there are
timestamped DoS source objects, while the source collection overall is larger.

`traffic_type` contains 0 (10,664 rows) and 1 (34,580 rows). Counts alone do
not establish its intended mapping or rowwise agreement with attack_category.
There are 19 attack_subcategory values; all three database label columns have
zero SQL NULLs. Rowwise consistency and label semantics remain to be checked.

Observed NULLs: `rnti` is NULL in 1,540 rows; the other 24 columns have no
SQL NULLs. This is not an audit of empty strings, sentinels or physical validity.
`ri`, `cellid`, `in_sync`, and `pmi` each have one distinct non-NULL database
value. These are structural diagnostics, not a fitted feature-selection rule.
All learned transforms and variability-based selection must still use only
training partitions under the future approved protocol.

## Source format and timestamp availability

All **49 text files** contain newline-delimited JSON objects. All 50,213
nonblank object records parsed; no malformed JSON/non-object lines were found.
Schemas vary: some records use `pmi`, others `pmi_0`/`pmi_1`, and some omit
timestamp and UE metadata. No transformation between these forms was inferred.

Files with no finite numeric timestamps:

- Benign: `benign_10.txt` (900 records), `benign_test.txt` (34).
- DoS: `icmp_hping3.txt` (1,125), `slowloris.txt` (1,007),
  `tcp-ack_hping3.txt` (648), `tcp-syn_hping3.txt` (768),
  `tcp_test.txt` (124), `udp_hping3.txt` (586).

Probe's `portscan_udp.txt` has 1,142 objects but only 573 finite numeric
timestamps. Missing-field counts and raw numeric ranges are in the JSON report.
Keep all these files; no exclusion or eligibility decision was made.

All 45,244 database timestamps are finite numbers, with 31,550 distinct values
and raw range 1,746,799,506,701 to 1,751,375,357,835. Epoch milliseconds are a
plausible interpretation of this magnitude, but units and clock/timezone
semantics remain unverified. No dates, reporting cadence, gap threshold or
run count were inferred. Shared timestamps may reflect multiple UEs; repeated
timestamps do not by themselves prove duplicate observations.

## Reliability and limits

The audit opened SQLite with `mode=ro` and `PRAGMA query_only=ON`. Every
selected file matched its extraction-manifest size/SHA-256 before inspection,
and all 50 input hashes were unchanged afterward. The report is deterministic
for identical input bytes and audit code. No random sampling was used.

This is an integrity/feasibility inventory, not performance evaluation or
feature selection. It does not validate counter units/resets, duplicates,
within-UE time ordering, class/date support, independent benign runs, label
correctness, or source-to-summary correspondence. Do not reuse these global
descriptive statistics to fit preprocessing on a future held-out partition.

## Next task

Reconcile source records to database rows using documented fields, tracking
ambiguous, unmatched and repeated matches without inventing timing or choosing
one arbitrary match. First inspect the database's timestamped DoS records and
the mixed-schema Probe source to explain the mismatch. Only then propose
source-file/group eligibility and run validation rules for Gaurav's review.
Kaggle release and dataset processing scripts are still needed for provenance.

## Review of Gaurav's saved notebook run — 2026-11-13

Reviewed the saved outputs in notebooks/01_dataset_understanding.ipynb without
modifying or rerunning that notebook. Its seven nonempty code cells have
consecutive execution counts 2 through 8 and no saved errors; the additional
empty code cell is harmless. Counters alone do not establish a fresh kernel.
The saved environment is rocm-jupyter, Python 3.11.14 / SQLite 3.51.0; missing
pytest is correctly reported as optional.

A fresh independent read-only audit matched the saved canonical report hash
and all displayed schema rows, six category-count comparisons, and nine
incomplete-timestamp file rows. All 50 input hashes remained unchanged.
Detailed local review evidence is in
results/notebook_saved_output_review_2026-11-13.json.

The 4,969 source-minus-database difference decomposes as Benign 934, DoS
3,466 and Probe 569. Benign and Probe differences equal their respective
missing-timestamp counts; this suggests a filtering hypothesis, not verified
record lineage. DoS cannot be explained by simply counting timestamped
source objects: the database has 792 more DoS rows than that count. The
immediate next task remains diagnostic matching with explicit multiplicity
and unmatched records, not defining runs or starting model comparisons.

## Descriptive follow up on professor feedback

The [November 24 addendum](eda_cleaning_addendum.md) adds cohort-labelled
statistics, class/source BLER associations, raw-unit window-span interpretation
and an explicit cleaning ledger. Historical investigation gates above remain
dated context; use the current checklist and protocol for adopted decisions.
