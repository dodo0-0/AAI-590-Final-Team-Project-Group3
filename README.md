# AAI-590: Radio intrusion detection reliability

Working title: **What Did the Detector Really Learn? Shortcut Audit and
Degraded-Telemetry Robustness of Radio-Based Intrusion Detection in 5G O-RAN.**

This workspace supports Gaurav's threat modeling, evaluation protocol, and
abstention policy responsibilities. Nitendra owns ML baselines, GRU/TCN models,
and calibration; Marco owns E2-based degradation models and playback.

Start each session with [the checklist](planning/checklist.md) and
[the progress log](docs/progress.md). The checklist is the task status authority.

## Current state

The workspace was empty at inspection on 2026-11-08. No dataset, source files,
meeting notes, reference paper, or experimental outputs were available here.
No empirical findings have been validated. This directory has not been
initialized as a Git repository.

- [Dataset inventory and evidence gaps](docs/dataset_inventory.md)
- [Threat-model skeleton](docs/threat_model.md)
- [Milestones](planning/milestones.md)
- [Team dependencies](planning/team_dependencies.md)
- [Methodological decisions](docs/decisions.md)

Evaluation and abstention specifications will follow dataset inspection and
review of the proposed definitions. `src/reliability/` is a package skeleton;
`tests/` documents the first test scope. No research utilities or test cases
are implemented yet. The six milestones are recorded in the checklist.

## Development setup (PowerShell, Python 3.11+)

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m pytest --collect-only -q
```

Pytest is pinned as a direct development dependency; this is not a complete
environment lock. Record resolved package versions with implementation and
experiment artifacts. Run tests from the project root: pytest adds `src/` to
its import path. No editable package installation is needed at this stage.
Collection currently has no tests (exit code 5), not a passing test suite.
Add useful tests with the first implemented utility.

## Data handling

Keep raw data outside version control. `data/` and `results/` contents are
ignored by default; keep only their committed README files. Supply the actual
dataset location during the next data session. Record version, source,
checksums, time semantics, and source-to-run provenance before experiments.
Never commit credentials or raw telemetry.
