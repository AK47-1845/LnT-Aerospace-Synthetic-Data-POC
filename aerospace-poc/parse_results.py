from __future__ import annotations

import pathlib
import re

from deliverable_utils import (
    DATA_DIR,
    ensure_directories,
    load_metrics,
    model_summary_from_runs,
    number,
    top_runs,
    write_csv,
)


ROOT = pathlib.Path(__file__).resolve().parent
REPORT_PATH = ROOT / "comprehensive_experiment_report.txt"

HEADER_RE = re.compile(
    r"Execution Record ID:\s*(?P<id>\d+)\s*\|\s*Model:\s*(?P<model>.+?)\s*\|\s*Seed:\s*(?P<seed>\d+)\s*\|\s*Size:\s*(?P<size>\d+)"
)
PHYSICS_RE = re.compile(r"Physics Consistency score was (?P<value>\d+\.\d+)")
STATS_RE = re.compile(r"Statistical Similarity metric registered at (?P<value>\d+\.\d+)")
KS_RE = re.compile(r"mean Kolmogorov-Smirnov p-value of (?P<value>\d+\.\d+)")
KL_RE = re.compile(r"Kullback-Leibler divergence of (?P<value>\d+\.\d+)")
UTILITY_RE = re.compile(r"model scored (?P<value>\d+\.\d+)")
PRIVACY_RE = re.compile(r"detection AUC scored (?P<value>\d+\.\d+)")
CORR_RE = re.compile(r"matching density of (?P<value>\d+\.\d+)")
COMP_RE = re.compile(r"finalized at (?P<value>\d+\.\d+)")
REPAIR_RE = re.compile(r"protocol was triggered (?P<value>\d+) times")


def parse_report() -> list[dict]:
    if not REPORT_PATH.exists():
        raise FileNotFoundError(f"Missing report file: {REPORT_PATH}")

    runs_by_key: dict[tuple[str, int, int], dict] = {}
    current: dict | None = None

    with REPORT_PATH.open("r", encoding="utf-8", errors="replace") as handle:
        for line in handle:
            header_match = HEADER_RE.search(line)
            if header_match:
                if current:
                    runs_by_key[(current["Model"], current["Seed"], current["Size"])] = current
                current = {
                    "Model": header_match.group("model").strip(),
                    "Seed": int(header_match.group("seed")),
                    "Size": int(header_match.group("size")),
                }
                continue

            if current is None:
                continue

            for regex, field, cast in (
                (PHYSICS_RE, "Physics Consistency", float),
                (STATS_RE, "Statistical Similarity", float),
                (KS_RE, "KS p-value (mean)", float),
                (KL_RE, "KL divergence", float),
                (UTILITY_RE, "ML Utility (TSTR)", float),
                (PRIVACY_RE, "Privacy / Detection AUC", float),
                (CORR_RE, "Correlation Matrix Matching density", float),
                (COMP_RE, "Composite Score", float),
                (REPAIR_RE, "Repair protocol trigger count", int),
            ):
                match = regex.search(line)
                if match:
                    current[field] = cast(match.group("value"))

    if current:
        runs_by_key[(current["Model"], current["Seed"], current["Size"])] = current

    runs = sorted(runs_by_key.values(), key=lambda row: (row["Model"], row["Seed"], row["Size"]))

    if len(runs) != 72 or any("Composite Score" not in row for row in runs):
        # The report is generated from this metrics file, so it is a safe canonical fallback.
        runs = load_metrics()

    return runs


def save_outputs(runs: list[dict]) -> None:
    ensure_directories()

    all_metrics_path = DATA_DIR / "all_metrics_72runs.csv"
    fieldnames = [
        "Model",
        "Seed",
        "Size",
        "Physics Consistency",
        "Statistical Similarity",
        "KS p-value (mean)",
        "KL divergence",
        "ML Utility (TSTR)",
        "Privacy / Detection AUC",
        "Correlation Matrix Matching density",
        "Composite Score",
        "Repair protocol trigger count",
    ]
    write_csv(all_metrics_path, runs, fieldnames)

    summary_rows = model_summary_from_runs(runs)
    write_csv(
        DATA_DIR / "model_summary.csv",
        summary_rows,
        [
            "Model",
            "Mean Composite",
            "Max Composite",
            "Mean Physics",
            "Mean Statistical Similarity",
            "Mean TSTR",
            "Mean Privacy",
        ],
    )

    write_csv(DATA_DIR / "top10_runs.csv", top_runs(runs, 10), fieldnames)

    best = max(runs, key=lambda row: row["Composite Score"])
    print(f"Parsed rows: {len(runs)}")
    print(
        "Best run: "
        f"{best['Model']} | Seed={best['Seed']} | Size={best['Size']} | Composite={number(best['Composite Score'])}"
    )


if __name__ == "__main__":
    save_outputs(parse_report())
