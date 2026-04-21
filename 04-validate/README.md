# Validation & Benchmarks

This directory contains reproducible benchmarks and validation scripts for the Physical AI Atlas.

## Benchmarks

### CBF QP Latency Benchmark

Measures actual Control Barrier Function QP solve times on your hardware to determine whether 1 kHz safety-loop operation is feasible.

```bash
python 04-validate/benchmarks/benchmark_cbf_latency.py
python 04-validate/benchmarks/benchmark_cbf_latency.py --iterations 50000 --save cbf_results.json
```

**Methodology:**
- 10,000 random (state, action) pairs, 40% biased toward workspace boundaries
- 30% of actions intentionally push toward nearest boundary (stress test)
- CBF-QP solved via `scipy.optimize.minimize` (SLSQP)
- Reports p50, p90, p95, p99, max latency in microseconds
- Separately reports latency for safe (pass-through) vs. override (QP solve) cases

**What "1 kHz Feasible" Means:**
The benchmark declares 1 kHz feasibility if the p99 solve time is under 1000 µs (1 ms). This means 99% of safety filter invocations complete within the 1 ms budget of a 1 kHz control loop. The remaining 1% can be handled by the deterministic watchdog fallback layer.

> **Note:** These benchmarks run on the SLSQP solver from SciPy. A production deployment would use a compiled QP solver (OSQP, qpOASES, or ECOS) which typically achieves 10-100x lower solve times. The benchmark establishes a *conservative lower bound* on feasibility.

## Reproducing Results

All benchmarks accept a `--seed` argument for reproducibility:

```bash
python 04-validate/benchmarks/benchmark_cbf_latency.py --seed 2026 --save results.json
```

Results are deterministic given the same seed, hardware, and software versions.
