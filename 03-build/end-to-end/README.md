# End-to-End Physical AI Pipeline Demo

This demo chains the complete Physical AI Atlas stack in a single script:

```
Language Instruction → VLA Reasoning → Flow Matching Policy → CBF Safety Filter → Physics Simulation → Evaluation
```

## Quick Start

```bash
# From repository root
pip install -r requirements.txt
python 03-build/end-to-end/run_atlas_demo.py
```

## What It Does

1. **VLA Reasoning** (simulated): Parses a language instruction ("Pick red cube and place on tray") into structured waypoints and grasp parameters. In production, this would be OpenVLA / SmolVLA / PaLM-E running at 1-5 Hz.

2. **Flow Matching Policy**: Generates smooth continuous action chunks via Conditional Flow Matching with 3-step Euler ODE integration. Implements the actual optimal-transport vector field from noise prior to target action.

3. **CBF Safety Filter**: Control Barrier Function QP (via SLSQP) that constrains every action to maintain workspace safety invariants. Reports per-action solve times for 1 kHz feasibility assessment.

4. **Physics Simulation**: Rigid-body pick-and-place with contact modeling, grasp probability, and actuation noise. Uses MuJoCo if installed, otherwise analytical kinematics.

5. **Quantitative Evaluation**: Reports success rate, collision count, safety override frequency, per-stage latency, and CBF QP solve-time percentiles.

## Output

```
═══════════════════════════════════════════════════════════════
  Physical AI Atlas — End-to-End Pipeline Demo
═══════════════════════════════════════════════════════════════
  Task:            Pick red cube and place on tray
  Policy:          Flow Matching (3-step Euler ODE)
  Safety Filter:   CBF-QP (h(x) >= 0 enforced)
  Simulator:       Analytical Kinematics
  Episodes:        50
  Seed:            2026
  ─────────────────────────────────────────────────────────────
  Success Rate:    XX/50 (XX.X%)
  Mean Steps:      XX.X
  Safety Overrides: XX total across 50 episodes
  Collisions:      0
  Policy Latency:  X.XX ms (mean)
  CBF Solve Time:  p50=XXX µs  p95=XXX µs  p99=XXX µs
  1 kHz Feasible:  Yes/No (p99 </>=  1000 µs)
═══════════════════════════════════════════════════════════════
```

## CLI Options

```bash
python run_atlas_demo.py --episodes 200      # More episodes
python run_atlas_demo.py --seed 42           # Reproducible seed
python run_atlas_demo.py --save results.json # Save detailed results
```

## Dependencies

- `numpy` >= 1.24
- `scipy` >= 1.10
- `mujoco` >= 3.0 (optional, for full rigid-body physics)
