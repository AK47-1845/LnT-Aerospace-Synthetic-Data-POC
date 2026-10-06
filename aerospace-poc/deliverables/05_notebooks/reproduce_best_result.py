from __future__ import annotations

import pathlib
import random
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from deliverable_utils import (  # noqa: E402
    DATA_DIR,
    NUMERIC_COLUMNS,
    discover_real_dataset,
    discover_synthetic_dataset,
    ks_statistic,
    load_dataset,
    load_metrics,
    number,
    save_dataset,
    simple_kl_divergence,
    timestamp_slug,
    validate_dataset,
)


def empirical_resample(rows: list[dict], seed: int, size: int) -> list[dict]:
    rng = random.Random(seed)
    sampled = [dict(rng.choice(rows)) for _ in range(size)]
    for row in sampled:
        row["Operational Life (years)"] = int(round(float(row["Operational Life (years)"])))
        row["Number of Iterations"] = int(round(float(row["Number of Iterations"])))
    return sampled


def main() -> None:
    real_rows = load_dataset(discover_real_dataset())
    stored_path = discover_synthetic_dataset("Empirical", 11, 5000)
    synthetic_rows = load_dataset(stored_path) if stored_path else empirical_resample(real_rows, 11, 5000)

    errors = validate_dataset(synthetic_rows)
    if errors:
        raise AssertionError("Validation failed:\n" + "\n".join(errors[:20]))

    metrics_rows = load_metrics()
    recorded = next(
        row for row in metrics_rows if row["Model"] == "Empirical" and row["Seed"] == 11 and row["Size"] == 5000
    )

    ks_values = [ks_statistic([float(r[col]) for r in real_rows], [float(s[col]) for s in synthetic_rows]) for col in NUMERIC_COLUMNS]
    kl_values = [simple_kl_divergence([float(r[col]) for r in real_rows], [float(s[col]) for s in synthetic_rows]) for col in NUMERIC_COLUMNS]
    derived_stats = {
        "Mean KS distance": sum(ks_values) / len(ks_values),
        "Mean KL divergence": sum(kl_values) / len(kl_values),
    }

    out_path = DATA_DIR / f"best_synthetic_empirical_seed11_n5000_{timestamp_slug()}.csv"
    save_dataset(out_path, synthetic_rows)

    print("FINAL REPORT CARD")
    print("-" * 40)
    print(f"Physics Consistency: {number(recorded['Physics Consistency'])}")
    print(f"Statistical Similarity: {number(recorded['Statistical Similarity'])}")
    print(f"ML Utility (TSTR): {number(recorded['ML Utility (TSTR)'])}")
    print(f"Privacy / Detection AUC: {number(recorded['Privacy / Detection AUC'])}")
    print(f"Correlation Match: {number(recorded['Correlation Matrix Matching density'])}")
    print(f"Composite Score: {number(recorded['Composite Score'])}")
    print(f"Derived mean KS distance: {number(derived_stats['Mean KS distance'])}")
    print(f"Derived mean KL divergence: {number(derived_stats['Mean KL divergence'])}")
    print(f"Saved synthetic dataset: {out_path}")


if __name__ == "__main__":
    main()
