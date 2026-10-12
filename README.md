# LTTS Aerospace Synthetic Data POC

Physics-constrained synthetic data for aerospace structural design — Genuity IO
proof of concept in the LTTS context (Mar 2026).

**Start here:** [`aerospace-poc/README.md`](./aerospace-poc/README.md) — the
POC pipeline, results, and run instructions.

## Headline results

- 300-row, 22-column seed → validated **5,000-row synthetic dataset**
- **92 experiments** across **9 model families** (3 seeds, Optuna HPO)
- **TSTR F1 1.000**, composite **0.9965**, MMD 0.0003
- **Zero physics violations** (yield/tensile, fatigue, ISA atmosphere)
- 30 edge-case scenarios, 294 visuals, 7 PDF reports

## Repo map

- `aerospace-poc/` — the POC: pipeline core, stages, `deliverables/` client
  pack, decks, seed data, full run log. Run: `pip install -r
  final/requirements.txt && python main.py` (see its README).
- `01-learn/` … `05-industrialize/`, `briefings/`, `docs/`, `examples/` —
  adjacent Physical-AI working material, shared with
  [physical-ai-atlas](https://github.com/AK47-1845/physical-ai-atlas).
- Root `.tex`/`.pptx`/`.pdf` files — executive briefing decks from the same
  workstream.

## Status

Working repo preserved as-archived. The POC deliverable is `aerospace-poc/`;
surrounding folders are research material, not part of the deliverable.

By Genuity IO (Adari Karthikeya).
