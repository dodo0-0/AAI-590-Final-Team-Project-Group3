# Provenance sources inspected — 2026-11-15

## Local archive

Inspected only the central directory of `data/archive_2.zip`: 320 file entries.
Extensions are .csv (110), .pcap (83), .txt (49), .json (39), .pcapng (35)
and .db (4). No filenames/extensions met the documented script, notebook,
README, manifest, metadata, processing or label-document search criteria.
This does not establish that all JSON/CSV contents lack provenance fields.
No additional archive extraction or full integrity/hash check was performed.

## Authors' public repository

The [dataset descriptor](https://www.researchgate.net/publication/395909335_Descriptor_5G_Open_Radio_Access_Network_Multi-Modal_Intrusion_Detection_Dataset_NetsLab-5GORAN-IDD)
points to the authors' code repository. Read-only review via the GitHub
connector pinned the inspected revision to
`add5de9fe2a1491a8d0bf4ccf0239c553c286634`.

| Inspected source | Cells | Git blob SHA |
| --- | ---: | --- |
| [Radio analysis notebook](https://github.com/NetsLab-Demo/NetsLab-Demo-Netslab-5G-ORAN-IDD/blob/add5de9fe2a1491a8d0bf4ccf0239c553c286634/5G-NL-IDD_radio_telemetry_analysis.ipynb) | 82 | 20d0cafe08a571f3fa78cd1c75462a441e52e98a |
| [Higher-layer notebook](https://github.com/NetsLab-Demo/NetsLab-Demo-Netslab-5G-ORAN-IDD/blob/add5de9fe2a1491a8d0bf4ccf0239c553c286634/5G-NL-IDD-higher_layer_network_data.ipynb) | 91 | 43191181c37857b35abe361f14e34b0601fbdfbd |

The radio notebook's first cell is a commented importer for legacy attack CSV
paths into `Server_Data`; later cells use legacy database names and drop
timestamp/identifier fields for analysis. Neither inspected notebook source
mentions the current `Lower_Layer_Data.db`/`lower_layer_data` names. This
snapshot does not supply an explanation of the current DoS metadata
association. That is a limitation of the inspected material, not proof that
documentation does not exist elsewhere. No external code was executed or
adopted as this project's evaluation methodology.

The [author-hosted dataset description](https://zenodo.org/records/18923275)
documents the radio/network modalities. Its record version and the dataset
content version are not a verified Kaggle revision for the user's archive.
No release equivalence or byte equivalence was inferred from those names.

## Questions still requiring source evidence

1. Which exact Kaggle revision produced the downloaded archive?
2. Which export/merge script populated timestamps, UE ID, cell ID and sync
   state for database rows whose radio candidates lack those source fields?
3. Are radio timestamps event times or arrival times? What are their units,
   epoch/timezone semantics and clock-synchronization guarantees?
4. Which source files/segments belong to the same independent capture? Are
   there authoritative run IDs, attack start/stop events and pairing records?

No messages to authors or teammates were sent. The user was asked whether
team notes, exporter scripts or revision information are available.

## User clarification and evidence boundary — 2026-11-15

Gaurav reports that no revision identifier is displayed/available to him and
that he is the only teammate who has begun this work. No team exporter or
capture notes are available. This records supplied information, not a claim
that Kaggle has no platform versioning capability.

Record the platform revision as **unavailable** rather than inventing one or
waiting for assumed existing team artifacts. The 50 extracted files are
identified by relative paths, sizes and SHA-256 in the extraction manifest and
audit reports. This pins analyzed content; it does not recover the platform
revision, full archive hash, processing history or independent captures.

The available data support forensic assessment of consistency and limitations.
The original metadata assignment mechanism may be unidentifiable from final
files. Distinguish observed facts from candidate explanations; unresolved
origin is an acceptable scientific outcome.
