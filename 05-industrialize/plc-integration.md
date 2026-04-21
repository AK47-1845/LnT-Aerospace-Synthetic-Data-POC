# PLC & Fieldbus Integration Guide

> **Deploying continuous AI models into deterministic brownfield industrial environments.**

---

## The Industrial Reality

Most factory floors are run by **Programmable Logic Controllers (PLCs)** (Siemens, Allen-Bradley, Beckhoff) using legacy fieldbuses (EtherCAT, PROFINET, Modbus TCP). These systems are highly deterministic, rigidly cyclical, and operate on discrete ladder logic.

Physical AI models (running on Linux with GPUs) are continuous, asynchronous, and non-deterministic in execution time.

Bridging these two worlds is the primary deployment challenge in industrial Physical AI.

---

## The Bridge Architecture

To deploy a Python-based PyTorch/JAX model to a real factory floor, you must implement a strict **Producer-Consumer Bridge** across the IT/OT boundary.

### The OT Side (Operational Technology)
The PLC acts as the master clock. It runs a deterministic loop (e.g., exactly 2ms cycle time).
1. **Reads** sensors.
2. **Writes** the current state buffer to shared memory or a fast IPC bridge (e.g., ADS for Beckhoff).
3. **Reads** the latest commanded action from the command buffer.
4. **Executes** the action via EtherCAT to the motor drives.

### The IT Side (Information Technology)
The AI system (e.g., Jetson Orin or IPC with RTX GPU) runs asynchronously.
1. **Polls** the state buffer.
2. **Runs** policy inference (takes 10-40ms).
3. **Writes** a continuous action trajectory (an "action chunk") to the command buffer.

---

## Handling Non-Determinism (The "Action Chunk")

Because the AI inference time varies (e.g., garbage collection, GPU scheduling), it cannot reliably provide a new action every 2ms.

**The Solution: Action Chunking.**
The policy does not predict a single action $a_t$. It predicts a trajectory of future actions $A_t = [a_t, a_{t+1}, \dots, a_{t+H}]$.

The PLC buffer holds this trajectory and consumes one step every 2ms. As long as the AI system computes the next chunk before the PLC exhausts the current buffer, the robot moves smoothly without jitter.

---

## Security & Network Isolation

Never expose the PLC directly to the AI compute node's network interface.
1. **Dual-NIC:** The AI node should have two Network Interface Cards.
2. **IT NIC:** Connected to the corporate network (for telemetry, weight updates, remote monitoring).
3. **OT NIC:** Point-to-point connection to the PLC (static IP, no gateway, no routing).

---

## Reference Implementation

See `03-build/starters/05_brownfield_plc_bridge.py` for a complete reference architecture using Python `pyads` to interface with a Beckhoff TwinCAT 3 PLC.
