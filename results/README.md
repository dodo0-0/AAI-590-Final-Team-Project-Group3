# Experiment artifacts

No model or abstention-policy experiments have been executed. Local audit,
cohort/window/split and validation JSON artifacts exist and are ignored by Git.
Share the snapshot described in [the handoff guide](../docs/handoff.md) through
the team Drive; restore it here without flattening paths. Historical preview
or approval records do not override the checklist or later decisions.

For the November 24 EDA supplement, upload eda_summary_2026-11-24.json and
eda_feedback_notebook_validation_2026-11-24.json to a new
EDA_Update_2026-11-24 subfolder in the existing team Drive folder. Keep the
original November 16 ZIP, inventory and checksums unchanged. Teammates extract
that ZIP into their checkout, then place both new JSON files here in results/.
The old checksum file does not cover the supplement. Current helper/code/docs
come from GitHub. See the handoff guide's November 24 EDA update instructions.

Future experiment outputs should include dataset and
code versions, split/run manifests, configuration, seeds, preprocessing fitted
on training data, selected validation thresholds, and metric limitations.
Large outputs are ignored by default. Deliberately select small, reviewed
summaries for version control when experiments exist.
