<div align="center">
  <h1>The Physical AI Atlas</h1>
  <p><b>An open engineering reference architecture, roadmap, and implementation guide for Physical AI.</b></p>

  <p>
    <a href="https://github.com/AK47-1845/physical-ai-atlas/actions"><img src="https://img.shields.io/badge/Build-Passing-brightgreen" alt="Build Status"></a>
    <a href="#"><img src="https://img.shields.io/badge/Status-Active%20Development-blue" alt="Status"></a>
    <a href="#"><img src="https://img.shields.io/badge/Domain-Physical%20AI-orange" alt="Domain"></a>
    <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-purple.svg" alt="License"></a>
  </p>
</div>

---

> **Also in this repo:** [`aerospace-poc/`](./aerospace-poc/) — the LTTS Aerospace Synthetic Data POC: 300 seed rows → 5,000 physics-valid rows, 92 experiments, TSTR F1 1.000, zero physics violations. Start at its README.

**Physical AI** is the discipline of deploying generative machine learning into closed-loop interaction with continuous, irreversible physical systems (robots, industrial actuators).

This repository is an open engineering reference that bridges the gap between **continuous probabilistic AI** and **discrete deterministic industrial systems**. It provides runnable examples of modern visuomotor policies (Flow Matching, Diffusion) interacting safely with physical environments via geometric safety filters (Control Barrier Functions).

## 🗺️ The Atlas

The repository is structured into five sequential tiers:

| Tier | Directory | Description | Key Artifacts |
|:---:|:---|:---|:---|
| **1** | [`01-learn/`](./01-learn/) | **Theory & Foundations** | Pearl's Causal Ladder, Research Index, Practitioner Roadmap |
| **2** | [`02-architect/`](./02-architect/) | **System Design** | Hardware BOM ($250 to $100k+), Blueprint, Safety Architecture |
| **3** | [`03-build/`](./03-build/) | **Code & Implementations** | End-to-End Demo, Flow Matching, CBF, VLA inference |
| **4** | [`04-validate/`](./04-validate/) | **Benchmarks** | Reproducible Control Barrier Function latency benchmarking |
| **5** | [`05-industrialize/`](./05-industrialize/) | **Deployment** | IT/OT Bridging, PLC & EtherCAT integration |

> 🚨 **MUST READ FOR NEWCOMERS:** Before diving into the codebase, absolutely everyone starting with foundational models and Physical AI must read the [**Complete Evolution of Frontier LLMs & Benchmarks (2019–2026)**](./briefings/LLM_Evolution_and_Benchmarks.md) briefing. It provides the critical architectural context, benchmark realities, and unit economics that drive this entire repository.

*Executive briefings and presentation generators are available in the [`briefings/`](./briefings/) folder.*

---

## 🚀 Quick Start (End-to-End Canonical Demo)

The easiest way to understand the stack is to run the end-to-end canonical demo. It simulates a complete pipeline: **Language Instruction → VLA Reasoning → Flow Matching Policy → CBF Safety Filter → Physics Simulation**.

```bash
git clone https://github.com/AK47-1845/physical-ai-atlas.git
cd physical-ai-atlas
pip install -r requirements.txt

# Run the 100-episode canonical demo
python 03-build/end-to-end/run_atlas_demo.py --episodes 100
```

> **What you'll see:** The demo outputs quantitative metrics showing success rates and CBF intervention latency, demonstrating how the safety filter operates strictly on a "minimum intervention" basis.

---

## 🔍 What This Is (And What It Is Not)

**This Is:**
- A pedagogical reference architecture explaining *how* modern Physical AI components fit together.
- A collection of minimal, standalone Python implementations (Flow Matching, Diffusion, CBF QPs) that prioritize mathematical clarity over optimization.
- A roadmap for practitioners moving from traditional robotics or software engineering into Physical AI.

**This Is NOT:**
- A production-ready robot control framework (use ROS2 or Mujoco MPC for that).
- A pre-trained foundation model library (use Hugging Face `lerobot` or OpenVLA).
- Formally certified safety software. While the architecture targets ISO 13849 / IEC 61508 patterns, true compliance requires full system-level certification by an accredited body.

---

## 🏗️ The Reference Architecture

A robust Physical AI system cannot be a single end-to-end neural network. It must be a multi-rate pipeline bridging cloud compute to hard real-time motor controllers.

```ascii
     [CLOUD / EDGE GPU]                  [IPC / REAL-TIME CPU]              [MCU / PLC]
     Latency: ~100-500ms                 Latency: ~1-5ms                    Latency: <1ms

┌───────────────────────────┐      ┌───────────────────────────┐      ┌─────────────────────┐
│ 1. SEMANTIC REASONING     │      │ 3. DETERMINISTIC SAFETY   │      │ 4. HARD ACTUATION   │
│ (VLA / LLM / PaLM-E)      │      │ (Control Barrier Filters) │      │ (Torque / Position) │
│ Output: Spatial Waypoints ├─────►│ Output: Safe Vector Field ├─────►│ Output: PWM / Ether │
└───────────────────────────┘      └───────────────────────────┘      └─────────────────────┘
             ▲                                   ▲                               ▲
             │                                   │                               │
┌────────────┴──────────────┐      ┌─────────────┴─────────────┐      ┌──────────┴──────────┐
│ 2. VISUOMOTOR POLICY      │      │ GEOMETRIC WORLD MODEL     │      │ KINEMATICS & DYNAMICS│
│ (Flow Matching / Pi0)     │      │ (Occupancy / Collisions)  │      │ (Forward/Inverse)   │
│ Output: Action Chunk      │      │ State: Joint + Vision     │      │ State: Encoders     │
└───────────────────────────┘      └───────────────────────────┘      └─────────────────────┘
```

See the [Architecture Documentation](./02-architect/ARCHITECTURE.md) for deep dives into specific layers.

---

## ⏱️ Validation & Benchmarks

The gap between research and reality is latency. We provide reproducible benchmarks to validate architectural claims.

### CBF Safety Filter Latency
The architecture targets a **1,000 Hz (1 ms)** safety loop. To verify this is achievable in Python before dropping down to C++/Rust, we benchmark the SciPy SLSQP solver on 50,000 randomized state-action vectors:

| Metric | All Actions (µs) | Safe Pass-Through (µs) | QP Override (µs) |
|:---|---:|---:|---:|
| **p50 (median)** | 1,229 | 18 | 1,638 |
| **p95** | 3,336 | - | - |
| **p99** | 11,158 | 58 | 15,630 |

*Hardware: AMD Ryzen (Standard Desktop CPU).*

**Conclusion:** A pure Python/SciPy implementation achieves ~12-15ms p99 latency. To hit the 1ms budget required for 1kHz operation, the CBF solver **must** be implemented in compiled C/C++ using a specialized solver like OSQP or qpOASES. See the `04-validate/` directory to run this benchmark on your own hardware.

---

## 🤝 Contributing

This is an open reference. We welcome implementations of new policy algorithms (e.g., ACT, Diffusion), better safety filters, or bindings to real industrial hardware.

Please read [`CONTRIBUTING.md`](./CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## 📄 License

This project is licensed under the MIT License - see the [`LICENSE`](./LICENSE) file for details.
