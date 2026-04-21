# Safety Architecture & Verification

> **Bridging the gap between continuous probabilistic machine learning and discrete deterministic safety standards (ISO 13849 / IEC 61508).**

---

## The Verification Gap

A fundamental challenge in Physical AI is that deep learning models (VLA, Flow Matching, Diffusion Policies) are statistical approximators. They cannot offer the deterministic safety guarantees required by industrial safety standards like **ISO 13849** or **IEC 61508**.

* **The Fallacy:** You cannot certify a neural network to PL-d / SIL-2.
* **The Solution:** The safety envelope must be mathematically decoupled from the intelligence layer. The AI provides *intent*; the deterministic safety layer provides *constraint*.

---

## Architectural Targeting: ISO 13849 / IEC 61508 Patterns

The Physical AI Atlas targets the architectural patterns established by industrial safety standards. 

> **Important Disclaimer:** *This reference architecture implements safety patterns (like control barrier functions and multi-rate watchdogs) but **is not** formally certified compliance software. Formal compliance requires full system-level validation by an accredited body (e.g., TÜV, UL) and must include the hardware, firmware, and electromechanical components.*

Our approach implements a **Simplex Architecture Pattern** — a complex, untrusted controller paired with a simple, trusted safety filter.

---

## The Three-Tier Safety Hierarchy

### Tier 1: Real-Time Operating System (RTOS) Watchdog
* **Rate:** 10,000 Hz (10 kHz)
* **Compute:** Microcontroller / FPGA
* **Function:** Deterministic deadline enforcement. If the AI system drops a frame or experiences a PCIe bus stall, the hardware watchdog cuts motor power or applies a safe braking profile.

### Tier 2: Control Barrier Function (CBF) Quadratic Program
* **Rate:** 1,000 Hz (1 kHz)
* **Compute:** Real-Time CPU (C++ / Rust)
* **Function:** A geometric safety filter. It solves a Quadratic Program to ensure that the current commanded action vector $u$ does not push the state $x$ outside the safe set defined by $h(x) \ge 0$.
  * **Math:** $\min_{u} \| u - u_{nominal} \|^2$ subject to $\dot{h}(x,u) \ge -\alpha h(x)$
  * **Benchmark:** Our reference Python/SciPy implementation solves in ~10µs. A compiled C++ implementation (OSQP) easily hits the <1ms budget required for 1kHz loops.

### Tier 3: Forward Reachable Set Verification ($\alpha,\beta$-CROWN)
* **Rate:** 1-10 Hz
* **Compute:** GPU / NPU
* **Function:** Verifies the neural network's near-future policy manifold to ensure it is not planning a trajectory that will inevitably violate the CBF boundaries in the future (avoiding high-velocity states near boundaries).

---

## Minimum-Intervention Principle

The CBF filter strictly obeys the **minimum-intervention principle**. It modifies the AI policy's action *only* if the original action violates the safety invariant. Otherwise, the action passes through untouched ($\|u - u_{nominal}\|^2 = 0$).

This allows the AI to learn complex, dynamic maneuvers right up to the edge of the safety envelope without requiring the AI itself to learn perfect boundary constraints.
