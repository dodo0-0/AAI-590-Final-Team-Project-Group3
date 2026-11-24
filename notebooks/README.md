# Dataset-understanding notebook

Open [01_dataset_understanding.ipynb](01_dataset_understanding.ipynb), select
the project `.venv/Scripts/python.exe` interpreter, restart the kernel and
Run All. Launch from the project root or `notebooks/`. The extracted radio
inputs must exist under `data/radio/`; prior result files are optional.

The notebook presents the structural audit, not source-to-database matching
or run reconstruction. It imports `reliability.data_audit` and does not copy
its parsing/validation implementation. No pandas, plotting package or model
library is required. Tables contain aggregate diagnostics, not raw data rows.

From the project root, install optional execution dependencies if needed:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-notebooks.txt
```

For execution without an interactive editor:

```powershell
.\.venv\Scripts\jupyter-execute.exe notebooks/01_dataset_understanding.ipynb --inplace --timeout=120
```

This saves fresh cell outputs into the notebook. Optional dependencies provide
a kernel and execution tools, not a browser notebook server. In an existing
notebook editor, select the project interpreter rather than a global kernel.

An existing Python 3.11+ notebook environment with IPython can also run the
audit. The provenance cell notes when it differs from the project `.venv`
and reports absent optional tools as not installed. `pytest` is needed to run
the tests, and nbclient/nbformat are needed for the headless execution setup;
they are not required for interactive execution of the audit cells. Do not
install packages into another environment just to populate the version table.

Every Run All recomputes the inventory, verifies extraction-manifest hashes
when supplied and checks input hashes afterward. The notebook reports its
interpreter, package versions, audit-code hash and canonical inventory hash.
The prior CLI artifact is compared as parsed JSON: Windows CRLF and LF file
encodings can have different byte hashes despite identical report content.

Read the explanations before interpreting the tables. Source counts are not
run counts; timestamp units and label/source lineage remain unverified.
The last section lists the next reconciliation investigation, explicitly
pending. Status lives in [the checklist](../planning/checklist.md).

The pre-existing root-level `AAI590_Data_Cleaning_EDA.ipynb` was inspected but
preserved unchanged. It is not a dependency of this notebook; its time/cleaning
assumptions have not been adopted as approved project methodology.

## Follow-up reconciliation notebook

[02_source_database_reconciliation.ipynb](02_source_database_reconciliation.ipynb)
is independent of notebook 01 and uses the same setup and Run All procedure.
It recomputes exact radio and radio-plus-metadata candidate groups, with all
source/database occurrences retained. It neither assigns run IDs nor changes
raw files. Its report can take longer to build than the initial inventory.
Use a new filename for the detailed CLI report on repeated executions.

[03_timing_and_metadata_provenance.ipynb](03_timing_and_metadata_provenance.ipynb)
is the next independent notebook, using the same kernel/path setup. It
recomputes timing and metadata-coincidence diagnostics without network access.
The full ZIP is optional for filename inventory; extracted radio files remain
required. All time quantities stay in raw units. Diagnostic identity groups
are not independently validated runs. Notebooks 01 and 02 are preserved.

Notebook 03 section 9 projects questionable database clocks onto candidate
source-line order and reports tuple reuse. These clocks were not observed in
those source records; projected reversals must not be confused with the
observed-source stream results in its earlier sections.

## Combined audit notebook

Open [00_combined_dataset_audit.ipynb](00_combined_dataset_audit.ipynb) to run
the dataset inventory, reconciliation and timing/provenance audits together.
Use Python 3.11+ (the existing rocm-jupyter kernel is supported), restart once,
then Run All from the top. Do not restart between parts. Launch from the
project root or notebooks directory, with the extracted data/radio files present.
Original code cells are unchanged; the three original notebooks are preserved.
Optional pytest metadata may be absent without blocking interactive execution.
No model training, degradation generation or abstention policy is run.

The November 24 follow-up adds Part 4 with cohort-labelled descriptive
statistics, full/class/source BLER associations and raw-unit timing summaries.
There are now 24 code cells: the original 23 unchanged cells plus one EDA
summary cell. It requires the restored cohort/window/split/timing artifacts
under results/. Read [the cleaning addendum](../docs/eda_cleaning_addendum.md).

Original narratives describe the investigation at each stage. Historical
pending decisions do not override later approved protocol/policy documents
or planning/checklist.md. Saving outputs changes only the combined notebook.

