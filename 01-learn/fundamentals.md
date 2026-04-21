# Fundamentals of Physical AI

> **From statistical association to causal interaction with continuous physical dynamics.**

---

## The Paradigm Shift

**Physical Artificial Intelligence (Physical AI)** is the engineering discipline of deploying learned models into closed-loop interaction with continuous, irreversible physical systems — robots, autonomous vehicles, industrial actuators, and surgical instruments.

While Large Language Models (LLMs) operate on statistical association ($P(Y \mid X)$), robots must operate on **causal interventions** ($P(Y \mid \text{do}(u))$) governed by differential equations of motion:

$$\tau = M(q)\ddot{q} + C(q, \dot{q})\dot{q} + g(q) - J^T(q)F_{\text{contact}}$$

In language, hallucinating a wrong token can be regenerated. In physical systems, hallucinating an unsafe torque breaks tooling or injures operators.

---

## Pearl's Causal Ladder in Robotics

Under **Judea Pearl's Causal Hierarchy**, intelligence operates across three distinct rungs:

```
                      ▲
     RUNG III         │   Counterfactuals: P(Y_u | X', Y')
   (Imagining)        │   "What would have happened had the robot gripped
                      │    with 5N less force?"
                      │
     RUNG II          │   Interventions: P(Y | do(u))
     (Doing)          │   "What is the system trajectory if actuator 3
                      │    applies torque tau?"
                      │
     RUNG I           │   Associations: P(Y | X)
    (Seeing)          │   "What text tokens/pixels statistically co-occur
                      │    in historical data?"
                      └────────────────────────────────────────────────►
```

Standard autoregressive LLMs operate at Rung I. Physical AI requires Rung II (active intervention via torque/force commands) and Rung III (counterfactual planning for safe multi-step manipulation).

---

## The 5 Canonical Failure Modes

| # | Failure Mode | Physical Mechanism | Mitigation |
|:-:|:---|:---|:---|
| **1** | **Visual Distractor Fragility** | Background shifts cause spurious cross-attention activations | Invariant feature pretraining (DINOv2 / SigLIP) + visual domain randomization |
| **2** | **Multi-Contact Discontinuity** | Non-smooth Coulomb friction boundaries ($F_f \le \mu F_N$) | Hybrid continuous dynamics + elastomeric tactile feedback (GelSight) |
| **3** | **Kinematic Singularity** | Yoshikawa manipulability $\mu(q) \to 0$ demands infinite joint rates | Damped Least-Squares (DLS): $J^* = J^T(J J^T + \lambda^2 I)^{-1}$ |
| **4** | **Compounding Covariate Shift** | $O(\epsilon T^2)$ drift off expert demonstration manifold | Action Chunking (ACT) + Flow Matching ($\pi_0$) with temporal ensembling |
| **5** | **Edge Latency Jitter** | Dropped frames violate control loop stability deadlines | Deterministic RTOS Watchdog + CBF QP override |

---

## The Three Schools of World Modeling

A **World Model** allows an agent to simulate and evaluate actions before executing them in the irreversible physical world.

| Dimension | School I: Generative Video | School II: Latent JEPA | School III: Spatial Occupancy |
|:---|:---|:---|:---|
| **Representatives** | Sora, Genie 2, Cosmos | LeCun JEPA, V-JEPA 2 | PointWorld, 3DGS-Dynamics |
| **Prediction Space** | Pixel RGB ($\mathbb{R}^{H \times W \times 3 \times T}$) | Latent features ($\mathbb{R}^d$) | 3D point clouds ($\mathbb{R}^{N \times 3}$) |
| **Inference Latency** | High (150ms – 2,000ms) | Ultra-low (2ms – 10ms) | Medium (15ms – 40ms) |
| **Hallucination Risk** | Severe (objects dissolve/warp) | Low (invariant state focus) | Minimal (enforces rigid volume) |
| **Industrial Role** | Synthetic data & scenario gen | Real-time on-robot planning | Collision avoidance & metrology |

---

*See also: [System Architecture](../02-architect/ARCHITECTURE.md) for implementation blueprints and [Research Index](./research-index.md) for curated paper references.*
