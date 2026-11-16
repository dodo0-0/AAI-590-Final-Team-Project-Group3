# Dataset inventory and evidence register

Status: initial inventory, 2026-11-08. Workspace inspection found no files or
dataset before this scaffold was created. The user's project brief is the
only supplied research context; the paper, notes and prior code are absent.

## Evidence needed before analysis

Record the local source path, release/version, acquisition source/date,
license/access restrictions, file sizes and checksums. Inventory file formats,
radio versus network sources, field names/types/units, label vocabulary,
timestamp representation/timezone, duplicates and missingness. Inspect data
without modifying originals. Dataset-wide inspection is for integrity and
feasibility; do not use held-out distributions to choose predictors or tune.

## Preliminary claims: all unverified

| Claim from user's summary of October 29 notes | Required validation |
| --- | --- |
| Six classes: Benign, Probe, DDoS, DoS, Web, BruteForce | Count actual label values, aliases and inconsistent source labels |
| Approximately one-second sampling | Within-source/run timestamp deltas, duplicates, gaps and clock semantics |
| 52 reconstructed runs versus 42 paired runs in reference paper | Compare gap segmentation to source capture manifests and paper pairing definition |
| Strong potential recording-day confounding | Run-level class-by-date support table, including absent combinations |
| About 13 informative radio metrics out of 22 | Schema and units first; training-only variability/eligibility analysis later |
| Constant or identifier columns exist | Semantic identifier review and training-only constant checks |
| Cumulative bytes require rates where appropriate | Counter semantics, units, resets/wraps and positive elapsed times |
| Too few independent benign runs for very low-FPR claims | Verified independent benign run count and duration; dependence-aware uncertainty |

## Run provenance gate

Timestamp gaps are candidate boundaries, not verified independent runs.
Preserve source file identity and original row ordering. Recover authoritative
capture/run IDs where possible and check overlaps, timestamp resets, label
transitions and capture pairing. Multiple files, windows or UEs from one
capture may remain dependent. Do not treat the preliminary 52 or the reported
42 as the validated grouping unit. If authoritative IDs cannot be recovered,
document uncertainty and seek Gaurav's decision before choosing a fallback.

## First data-backed deliverable

A reproducible read-only inventory with schema summary, source manifest,
timestamp diagnostics, label counts and a candidate-run validation report.
Implement its smallest useful portion after actual file formats are known.
Tests should use explicit synthetic fixtures to exercise logic, clearly
separated from empirical dataset evidence.

Pending investigations remain open: recover true source run IDs; compare
downlink channel features separately from uplink power/SNR; search the supplied
capture inventory for additional same-day benign recordings. No investigation
has been completed in this session.

## Initialization reinspection — 2026-11-08

The workspace still contains only documentation and the new development
skeleton; `data/` contains its README only. No external data directory has
been specified or searched. Absence here does not establish that the team
lacks these artifacts elsewhere.

Missing inputs, in priority order:

1. Accessible NetsLab-5GORAN-IDD v2 radio files, release/version and source
   location; identify whether they are raw captures, exports or merged tables.
2. Source file/run/date manifest, radio/network pairing if available, timezone
   and timestamp semantics. These are needed before claiming run independence.
3. Schema/data dictionary with units, counter semantics, labels and attack
   generation documentation; reference paper and October 29 audit code/notes.
4. Nitendra's window/label/score and preprocessing conventions; Marco's
   observation/quality fields, clean/degraded alignment and scenario rationale.

First actionable task is DATA-00: record a real accessible data path/source
and provenance, explicitly listing any absent manifests. Then DATA-01 can
produce the smallest reproducible file/schema inventory. DATA-00 does not
require waiting for every later teammate interface.

## Remote source inspection and staged acquisition — 2026-11-08

The user supplied a Kaggle Data Explorer screenshot showing 145.96 GB,
six current class folders, Attack (Legacy) Version 1, and three summary files.
The authors' [NetsLab page](https://netslab.ucd-cs.ie/netslab-datasets/netslab-5goran-idd/)
links [this Kaggle dataset](https://www.kaggle.com/datasets/netslabdemo/netslab-5g-oran-idd).
Kaggle's dynamic file tree was not readable through the web tool; the exact
current version, individual paths/sizes and match to the screenshot remain
unconfirmed. Dataset content version 2 and a platform release number are
distinct provenance fields; record both when available.

The authors' [Zenodo record](https://zenodo.org/records/18923275) documents
per-class lower_layer/ text radio files and network_layer/ packet captures,
and identifies Lower_Layer_Data.db as the combined radio summary. That record
lists the database at 5.4 MB; this is not a verified Kaggle file size or proof
that the two distributions contain identical data. No file has been downloaded
or queried. Source documentation is evidence of intended organization, not
validation of actual labels, completeness, timestamps or independent runs.

Recommended acquisition order (no change to research population or splits):

1. Download Lower_Layer_Data.db from the user's selected Kaggle version.
   Record version, source path, size and checksum; inspect tables/schema and
   retained provenance before deciding what it supports.
2. Obtain all available source lower_layer/ radio files for Benign,
   BruteForce, DDOS, DoS, Probe and Web, preserving relative paths and names.
   These are needed to investigate source-run identity and benign capture
   availability. Total size is not yet established. A database-only inspection
   does not complete run validation.
3. Defer network_layer/ captures, Network_Dataset.csv/.db and legacy attacks.
   Reconsider specific files if radio provenance cannot be resolved without
   cross-layer metadata; do not promise they will never be needed.

This is selection by modality/version, not class subsampling or random row
sampling. Retain every current class, especially all available benign captures.
The [official Kaggle CLI documentation](https://github.com/Kaggle/kaggle-cli/blob/main/docs/datasets.md)
supports file listing and individual-file downloads with `-f`; use actual
listed paths. No Kaggle CLI was installed or executed in this session.

## Actual archive and selective extraction — 2026-11-13

The user downloaded `data/archive_2.zip`. Inspected its central directory
using Python's standard-library zipfile module; the archive has 320 file
entries, 25,101,375,790 compressed archive bytes (25.10 GB), and
145,957,931,888 bytes of listed uncompressed file content (145.96 GB).
No full decompression is necessary for the selected radio workstream.

Extracted to `data/radio/`, preserving exact member paths:

| Selection | Files |
| --- | ---: |
| Lower_Layer_Data.db | 1 |
| Benign/Benign/Lower_Layer/ | 12 |
| BruteForce/BruteForce/Lower_Layer/ | 4 |
| DDOS/DDOS/Lower_Layer/ | 9 |
| DoS/DoS/Lower_Layer/ | 10 |
| Probe/Probe/Lower_Layer/ | 7 |
| Web/Web/Lower_Layer/ | 7 |
| Total | 50 |

Selected content totals **22,786,276 bytes (22.79 MB)**, including the
5,402,624-byte database and 49 source text files. Retained all files in the
selected directories, including names containing `test`; eligibility and
capture independence have not been inferred from names. In particular, the
12 Benign files are not evidence of 12 independent benign runs.

`data/radio/extraction_manifest.json` records the selection rule, archive
filename/size, exact selected member paths, original sizes, ZIP CRC32 and
SHA-256 of every extracted file. Reading selected ZIP members checked their
CRC; re-reading extracted files confirmed sizes and SHA-256. No existing
files were overwritten. Paths were checked to remain under the extraction
directory. The original archive was unchanged. It has not been fully hashed
or integrity-tested; checks cover selected members only.

Network captures, network summary files and legacy content remain inside the
ZIP. The data directory and manifest remain excluded from Git by existing
ignore rules. Kaggle platform release is still unknown; schema, labels,
timestamps and source-to-summary/run lineage remain to be inspected. The
next task is read-only schema/source-format inspection, not model training.

## Structural audit performed — 2026-11-13

See [the actual-data findings](data_audit_findings.md) and
`results/radio_inventory_2026-11-13.json`. The read-only audit confirms six
literal database category values and a 45,244-row, 25-column table. The 49
source files contain 50,213 JSON objects, with varying timestamp availability.
Source-to-summary correspondence remains unresolved. Earlier notes above
describe the state before this inspection, not current absence of data.
No run count, cadence, counter semantics or class/date confounding claim has
been validated by this structural step.

## Source/database comparison performed — 2026-11-13

[Reconciliation findings](reconciliation_findings.md) now account for the
count difference using exact candidate groups without assigning runs or
dropping any occurrence. All 45,244 database rows have exact radio candidates;
43,704 have unique candidates including all compared metadata. The remaining
1,540 DoS database rows agree on radio values with source records lacking
timestamp/UE metadata. Their populated database metadata remains unverified.
Candidate grouping resolves the descriptive mismatch, not the author's
processing provenance or independent-run boundaries. Prior sections record
earlier evidence states; the clock/run gates remain open.

## Raw timing/provenance diagnostic — 2026-11-15

[Timing findings](timing_findings.md) record 88 descriptive source/identity
groups, all with a median positive step of 1,000 raw timestamp units. No
backward/repeated times occurred within those groups; no interval overlaps
were found in 102 same-identity cross-file pairs. These are not run IDs or
proof of independence. All 1,540 questionable DoS metadata tuples coincide
with other source observations while their radio values differ. Clock
provenance remains unresolved. The archive filename search and pinned author
repository review are scoped in [provenance sources](provenance_sources.md).

2026-11-15 clarification: Gaurav reports no available Kaggle revision and no
team exporter/capture notes. Record the platform revision as unavailable and
identify this analyzed snapshot by its existing per-file hashes. Do not
conflate those hashes with recovered processing or capture provenance.
Further diagnostics in notebook 03 section 9 quantify metadata reuse/order;
they do not authenticate the questionable clocks or recover the generating
procedure. These unknowns remain explicit while draft research work proceeds.
