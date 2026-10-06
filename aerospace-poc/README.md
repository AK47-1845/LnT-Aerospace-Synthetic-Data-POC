# LTTS Aerospace Synthetic Data POC

Physics-constrained synthetic data for aerospace structural design, delivered to
L&T Technology Services (Mar 2026) by Genuity IO.

## What this is

From a **300-row, 22-column** seed dataset (`aerospace_structural_design_dataset.csv`),
this pipeline benchmarks generative models, enforces aerospace physics as hard
constraints, and ships a validated **5,000-row synthetic dataset** plus full evidence.

## Headline results

- **92 experiments** across **9 model families**, 3 seeds, 4 scales, Optuna HPO
- Best composite score **0.9965**; **TSTR F1 1.000** (train on synthetic, test on real)
- **MMD 0.0003**, discriminator AUC **0.478** (near chance = indistinguishable)
- **Zero physics violations** (yield ≤ tensile, fatigue ≤ tensile, ISA atmosphere consistency)
- **30 edge-case scenarios**, 91% mean LOF realism, 294 visuals, 7 PDF reports

## Map

- `main.py`, `config.py`, `physics.py`, `models_engine.py`, `evaluator.py` — pipeline core
- `data_prep.py`, `generator.py`, `edge_cases.py`, `eval_extended.py` — stages
- `generate_*.py`, `build_*.py`, `fix_*.py` — reporting and deck builders
- `DOCUMENTATION.md` — full technical documentation
- `deliverables/` — organized client deliverable (reports, graphs, data, benchmarks)
- `deliverables_LnT/` — LnT-formatted pack: docs, final reports, edge cases
- `final/` — experiment code, per-stage reports, validation reports, synthetic data
- `explainability/` — explainability graphs
- `aerospace_structural_design_dataset.csv` — the 300-row seed (input)
- `comprehensive_experiment_report.txt` — full text log of all runs
- `LnT_Aerospace_Synthetic_Data_POC_v4.pptx` — latest full deck
- `LnT_Aerospace_POC_Compact_v2.pptx` — executive compact deck

## Run

```bash
pip install -r final/requirements.txt
python main.py
```

See `final/README.md`, `final/PLAN.md`, and `DOCUMENTATION.md` for stage-by-stage
instructions. Graph/report builders regenerate excluded visual artifacts on demand.

## What is excluded from git (and why)

To keep this repo clonable, large regenerable/intermediate artifacts stay local:

- `*.zip` packs, `node_modules/`, `artifacts/` (raw run logs), `.env`
- `deliverables_LnT/anomaly_outlier|class_balanced|discriminator_similarity|feature_engineering|explainable_graphs|synthetic_data/`
  (intermediate scores and per-model variants; rebuild with `generate_all_graphs.py`)
- `final/per_model_datasets/` (intermediate), superseded deck versions (v1–v3, backups)

Final evidence (reports, validation PDFs, champion synthetic data, compact + v4 decks)
is all present above. Nothing excluded changes any reported number.
