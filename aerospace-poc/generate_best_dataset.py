from __future__ import annotations

import random

from deliverable_utils import (
    DATA_DIR,
    NUMERIC_BOUNDS,
    SCHEMA_COLUMNS,
    discover_real_dataset,
    discover_synthetic_dataset,
    ensure_directories,
    load_dataset,
    save_dataset,
    validate_dataset,
)


BEST_MODEL = "Empirical"
BEST_SEED = 11
BEST_SIZE = 5000
OUTPUT_PATH = DATA_DIR / "best_synthetic_empirical_seed11_n5000.csv"


def empirical_resample(rows: list[dict], seed: int, size: int) -> list[dict]:
    rng = random.Random(seed)
    sampled = [dict(rng.choice(rows)) for _ in range(size)]
    # Preserve integer-like numeric fields.
    for row in sampled:
        row["Operational Life (years)"] = int(round(float(row["Operational Life (years)"])))
        row["Number of Iterations"] = int(round(float(row["Number of Iterations"])))
    return sampled


def build_best_dataset() -> list[dict]:
    real_dataset_path = discover_real_dataset()
    real_rows = load_dataset(real_dataset_path)

    existing_path = discover_synthetic_dataset(BEST_MODEL, BEST_SEED, BEST_SIZE)
    if existing_path:
        synthetic_rows = load_dataset(existing_path)
    else:
        synthetic_rows = empirical_resample(real_rows, seed=BEST_SEED, size=BEST_SIZE)

    # Ensure the exact expected schema order is carried through.
    normalized = []
    for row in synthetic_rows:
        clean = {column: row[column] for column in SCHEMA_COLUMNS}
        for column, (lower, upper) in NUMERIC_BOUNDS.items():
            value = float(clean[column])
            clean[column] = min(max(value, lower), upper)
        normalized.append(clean)
    errors = validate_dataset(normalized)
    if errors:
        raise AssertionError("Validation failed:\n" + "\n".join(errors[:25]))
    return normalized


def main() -> None:
    ensure_directories()
    rows = build_best_dataset()
    save_dataset(OUTPUT_PATH, rows)
    print("Validation summary: PASS")
    print("Checks: no nulls | ranges valid | 22 columns | categorical levels valid")
    print(f"Saved dataset: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
