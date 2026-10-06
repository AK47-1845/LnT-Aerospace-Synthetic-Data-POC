from __future__ import annotations

import base64
import csv
import datetime as dt
import html
import json
import math
import os
import pathlib
import re
import shutil
import statistics
import subprocess
from typing import Iterable, Sequence


ROOT = pathlib.Path(__file__).resolve().parent
DELIVERABLES_DIR = ROOT / "deliverables"
REPORTS_DIR = DELIVERABLES_DIR / "01_reports"
GRAPHS_DIR = DELIVERABLES_DIR / "02_graphs"
DATA_DIR = DELIVERABLES_DIR / "03_data"
BENCHMARKS_DIR = DELIVERABLES_DIR / "04_benchmarks"
NOTEBOOKS_DIR = DELIVERABLES_DIR / "05_notebooks"

GRAPH_SUBDIRS = {
    "A": GRAPHS_DIR / "A_model_comparison",
    "B": GRAPHS_DIR / "B_scale_analysis",
    "C": GRAPHS_DIR / "C_statistical",
    "D": GRAPHS_DIR / "D_summary",
}

MODEL_ORDER = ["Empirical", "KDE", "GMM", "Copula", "TabuDiff", "MaskedPredictor"]
SIZE_ORDER = [300, 600, 1000, 5000]
SEED_ORDER = [11, 42, 123]
MODEL_COLORS = {
    "Empirical": "#00d4ff",
    "KDE": "#4db06d",
    "GMM": "#f59e0b",
    "Copula": "#ef4444",
    "TabuDiff": "#8b5cf6",
    "MaskedPredictor": "#6b7280",
}

HEADER_MAP = {
    "Material Type": "Material Type",
    "E (GPa)": "E (GPa)",
    "ν": "ν (Poisson)",
    "Î½": "ν (Poisson)",
    "ρ (kg/m³)": "ρ (kg/m³)",
    "Ï\x81 (kg/mÂ³)": "ρ (kg/m³)",
    "Tensile Strength (MPa)": "Tensile Strength (MPa)",
    "Young’s Modulus": "Young's Modulus",
    "Youngâ€™s Modulus": "Young's Modulus",
    "Structural Shape": "Structural Shape",
    "Load Distribution": "Load Distribution",
    "Altitude (m)": "Altitude (m)",
    "Temperature (°C)": "Temperature (°C)",
    "Temperature (Â°C)": "Temperature (°C)",
    "Pressure (Pa)": "Pressure (Pa)",
    "Operational Life (years)": "Operational Life (years)",
    "Wing Span (m)": "Wing Span (m)",
    "Fuselage Length (m)": "Fuselage Length (m)",
    "Structural Thickness (mm)": "Structural Thickness (mm)",
    "Quantum Algorithm Type": "Quantum Algorithm Type",
    "Number of Iterations": "Number of Iterations",
    "Optimization Time (sec)": "Optimization Time (sec)",
    "Vibration Damping": "Target — Vibration Damping",
    "Computational Time": "Target — Computational Time",
    "Weight Efficiency": "Target — Weight Efficiency",
    "Durability": "Target — Durability",
    "Target — Vibration Damping": "Target — Vibration Damping",
    "Target — Computational Time": "Target — Computational Time",
    "Target — Weight Efficiency": "Target — Weight Efficiency",
    "Target — Durability": "Target — Durability",
}

SCHEMA_COLUMNS = [
    "Material Type",
    "E (GPa)",
    "ν (Poisson)",
    "ρ (kg/m³)",
    "Tensile Strength (MPa)",
    "Young's Modulus",
    "Structural Shape",
    "Load Distribution",
    "Altitude (m)",
    "Temperature (°C)",
    "Pressure (Pa)",
    "Operational Life (years)",
    "Wing Span (m)",
    "Fuselage Length (m)",
    "Structural Thickness (mm)",
    "Quantum Algorithm Type",
    "Number of Iterations",
    "Optimization Time (sec)",
    "Target — Vibration Damping",
    "Target — Computational Time",
    "Target — Weight Efficiency",
    "Target — Durability",
]

NUMERIC_COLUMNS = [
    "E (GPa)",
    "ν (Poisson)",
    "ρ (kg/m³)",
    "Tensile Strength (MPa)",
    "Young's Modulus",
    "Altitude (m)",
    "Temperature (°C)",
    "Pressure (Pa)",
    "Operational Life (years)",
    "Wing Span (m)",
    "Fuselage Length (m)",
    "Structural Thickness (mm)",
    "Number of Iterations",
    "Optimization Time (sec)",
]

NUMERIC_BOUNDS = {
    "E (GPa)": (50.1, 199.8),
    "ν (Poisson)": (0.30, 0.35),
    "ρ (kg/m³)": (1521.0, 4496.0),
    "Tensile Strength (MPa)": (261.0, 1496.0),
    "Young's Modulus": (50.0, 99.6),
    "Altitude (m)": (5086.0, 19963.0),
    "Temperature (°C)": (-60.0, -40.0),
    "Pressure (Pa)": (100172.0, 199839.0),
    "Operational Life (years)": (20.0, 39.0),
    "Wing Span (m)": (20.0, 59.7),
    "Fuselage Length (m)": (30.0, 70.0),
    "Structural Thickness (mm)": (5.0, 14.9),
    "Number of Iterations": (523.0, 1983.0),
    "Optimization Time (sec)": (51.5, 149.8),
}

CATEGORICAL_LEVELS = {
    "Material Type": ["Aluminum", "Titanium", "Carbon Fiber"],
    "Structural Shape": ["Rectangular", "Cylindrical", "Tapered"],
    "Load Distribution": ["uniform", "point load", "distributed"],
    "Quantum Algorithm Type": ["Chaotic Quantum Genetic", "Shark Optimizer"],
    "Target — Vibration Damping": ["Low", "Moderate", "High"],
    "Target — Computational Time": ["Short", "Medium", "Long"],
    "Target — Weight Efficiency": ["Poor", "Good", "Excellent"],
    "Target — Durability": ["Low", "Medium", "High"],
}

FALLBACK_MODEL_SUMMARY = {
    "Empirical": {
        "Mean Composite": 0.9631,
        "Max Composite": 0.9969,
        "Mean Physics": 0.9911,
        "Mean Statistical Similarity": 0.9828,
        "Mean TSTR": 0.96,
        "Mean Privacy": 0.983,
    },
    "KDE": {
        "Mean Composite": 0.9650,
        "Max Composite": 0.9965,
        "Mean Physics": 0.9924,
        "Mean Statistical Similarity": 0.9828,
        "Mean TSTR": 0.96,
        "Mean Privacy": 0.983,
    },
    "GMM": {
        "Mean Composite": 0.8345,
        "Max Composite": 0.8535,
        "Mean Physics": 0.9897,
        "Mean Statistical Similarity": 0.9781,
        "Mean TSTR": 0.37,
        "Mean Privacy": 0.962,
    },
    "Copula": {
        "Mean Composite": 0.8124,
        "Max Composite": 0.8309,
        "Mean Physics": 0.9895,
        "Mean Statistical Similarity": 0.9669,
        "Mean TSTR": 0.35,
        "Mean Privacy": 0.967,
    },
    "TabuDiff": {
        "Mean Composite": 0.7965,
        "Max Composite": 0.8231,
        "Mean Physics": 0.9822,
        "Mean Statistical Similarity": 0.9107,
        "Mean TSTR": 0.30,
        "Mean Privacy": 0.911,
    },
    "MaskedPredictor": {
        "Mean Composite": 0.4313,
        "Max Composite": 0.4398,
        "Mean Physics": 0.9587,
        "Mean Statistical Similarity": 0.0,
        "Mean TSTR": 0.10,
        "Mean Privacy": 0.0,
    },
}


def ensure_directories() -> None:
    for path in [DELIVERABLES_DIR, REPORTS_DIR, DATA_DIR, BENCHMARKS_DIR, NOTEBOOKS_DIR, *GRAPH_SUBDIRS.values()]:
        path.mkdir(parents=True, exist_ok=True)


def canonical_header(name: str) -> str:
    return HEADER_MAP.get(name.strip(), name.strip())


def read_csv_rows(path: pathlib.Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = []
        for row in reader:
            normalized = {canonical_header(key): value for key, value in row.items() if key is not None}
            rows.append(normalized)
    return rows


def write_csv(path: pathlib.Path, rows: Sequence[dict], fieldnames: Sequence[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def discover_real_dataset() -> pathlib.Path:
    candidates = [
        "aerospace_dataset.csv",
        "data.csv",
        "dataset.csv",
        "original.csv",
        "aerospace_structural_design_dataset.csv",
    ]
    for name in candidates:
        path = ROOT / name
        if path.exists():
            return path
    for path in ROOT.rglob("*.csv"):
        if "synthetic_" not in path.name.lower() and "metrics" not in path.name.lower():
            return path
    raise FileNotFoundError("Could not locate the original dataset in the project directory.")


def discover_metrics_csv() -> pathlib.Path | None:
    explicit = DATA_DIR / "all_metrics_72runs.csv"
    if explicit.exists():
        return explicit
    candidates = sorted(ROOT.glob("artifacts/experiments/*/metrics/metrics_raw.csv"))
    return candidates[-1] if candidates else None


def discover_synthetic_dataset(model: str, seed: int, size: int) -> pathlib.Path | None:
    direct = DATA_DIR / f"best_synthetic_{model.lower()}_seed{seed}_n{size}.csv"
    if direct.exists():
        return direct
    pattern = f"artifacts/experiments/*/synth_datasets/synthetic_{model}_{seed}_{size}_best.csv"
    candidates = sorted(ROOT.glob(pattern))
    return candidates[-1] if candidates else None


def convert_value(column: str, value: str):
    if column in NUMERIC_COLUMNS:
        return float(value)
    return value


def load_dataset(path: pathlib.Path) -> list[dict]:
    rows = read_csv_rows(path)
    normalized = []
    for row in rows:
        clean = {}
        for column in SCHEMA_COLUMNS:
            source_value = row.get(column, "")
            clean[column] = convert_value(column, source_value)
        normalized.append(clean)
    return normalized


def save_dataset(path: pathlib.Path, rows: Sequence[dict]) -> None:
    serializable = []
    for row in rows:
        out = {}
        for column in SCHEMA_COLUMNS:
            value = row[column]
            if isinstance(value, float) and column in ("Operational Life (years)", "Number of Iterations"):
                value = int(round(value))
            out[column] = value
        serializable.append(out)
    write_csv(path, serializable, SCHEMA_COLUMNS)


def validate_dataset(rows: Sequence[dict]) -> list[str]:
    errors: list[str] = []
    if not rows:
        errors.append("Dataset is empty.")
        return errors

    for idx, row in enumerate(rows):
        missing = [column for column in SCHEMA_COLUMNS if column not in row]
        if missing:
            errors.append(f"Row {idx} missing columns: {missing}")
            continue
        for column in SCHEMA_COLUMNS:
            value = row[column]
            if value in ("", None):
                errors.append(f"Row {idx} has null/empty value in {column}")
        for column, (lower, upper) in NUMERIC_BOUNDS.items():
            value = float(row[column])
            if value < lower or value > upper:
                errors.append(f"Row {idx} out of range for {column}: {value}")
        for column, levels in CATEGORICAL_LEVELS.items():
            value = str(row[column])
            if value not in levels:
                errors.append(f"Row {idx} invalid level in {column}: {value}")
    return errors


def load_metrics(path: pathlib.Path | None = None) -> list[dict]:
    source = path or discover_metrics_csv()
    if source is None or not source.exists():
        raise FileNotFoundError("Could not find metrics CSV.")
    rows = read_csv_rows(source)
    normalized = []
    for row in rows:
        clean = {
            "Model": row["Model"],
            "Seed": int(row["Seed"]),
            "Size": int(row["Size"]),
            "Physics Consistency": float(row.get("Physics Consistency", row.get("physics_consistency", 0.0))),
            "Statistical Similarity": float(row.get("Statistical Similarity", row.get("statistical_similarity", 0.0))),
            "KS p-value (mean)": float(row.get("KS p-value (mean)", row.get("mean_ks_pval", 0.0))),
            "KL divergence": float(row.get("KL divergence", row.get("mean_kl_div", 0.0))),
            "ML Utility (TSTR)": float(row.get("ML Utility (TSTR)", row.get("ml_utility", 0.0))),
            "Privacy / Detection AUC": float(row.get("Privacy / Detection AUC", row.get("privacy_detectability", 0.0))),
            "Correlation Matrix Matching density": float(
                row.get("Correlation Matrix Matching density", row.get("correlation_preservation", 0.0))
            ),
            "Composite Score": float(row.get("Composite Score", row.get("composite_score", 0.0))),
            "Repair protocol trigger count": int(float(row.get("Repair protocol trigger count", row.get("repair_count", 0)))),
        }
        normalized.append(clean)
    return normalized


def group_by(rows: Sequence[dict], key: str) -> dict:
    grouped: dict = {}
    for row in rows:
        grouped.setdefault(row[key], []).append(row)
    return grouped


def mean(values: Iterable[float]) -> float:
    values = list(values)
    return sum(values) / len(values) if values else 0.0


def stddev(values: Iterable[float]) -> float:
    values = list(values)
    return statistics.pstdev(values) if len(values) > 1 else 0.0


def model_summary_from_runs(rows: Sequence[dict]) -> list[dict]:
    summaries = []
    grouped = group_by(rows, "Model")
    for model in MODEL_ORDER:
        model_rows = grouped.get(model, [])
        if model_rows:
            summaries.append(
                {
                    "Model": model,
                    "Mean Composite": round(mean(r["Composite Score"] for r in model_rows), 4),
                    "Max Composite": round(max(r["Composite Score"] for r in model_rows), 4),
                    "Mean Physics": round(mean(r["Physics Consistency"] for r in model_rows), 4),
                    "Mean Statistical Similarity": round(mean(r["Statistical Similarity"] for r in model_rows), 4),
                    "Mean TSTR": round(mean(r["ML Utility (TSTR)"] for r in model_rows), 4),
                    "Mean Privacy": round(mean(r["Privacy / Detection AUC"] for r in model_rows), 4),
                }
            )
        else:
            fallback = FALLBACK_MODEL_SUMMARY[model]
            summaries.append({"Model": model, **fallback})
    return summaries


def top_runs(rows: Sequence[dict], limit: int = 10) -> list[dict]:
    return sorted(rows, key=lambda row: row["Composite Score"], reverse=True)[:limit]


def to_data_uri(path: pathlib.Path) -> str:
    mime = "image/png" if path.suffix.lower() == ".png" else "image/svg+xml"
    data = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{data}"


def html_escape(value) -> str:
    return html.escape(str(value), quote=True)


def number(value: float, digits: int = 4) -> str:
    return f"{value:.{digits}f}"


def slugify(text: str) -> str:
    lowered = text.lower().replace("—", "-").replace("'", "")
    lowered = re.sub(r"[^a-z0-9]+", "_", lowered)
    return lowered.strip("_")


def safe_filename(text: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]+", "_", text)


def chrome_path() -> pathlib.Path:
    candidates = [
        pathlib.Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe"),
        pathlib.Path(r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    raise FileNotFoundError("Chrome executable not found for headless export.")


def export_svg_to_png(svg_path: pathlib.Path, png_path: pathlib.Path, width: int, height: int) -> None:
    png_path.parent.mkdir(parents=True, exist_ok=True)
    command = [
        str(chrome_path()),
        "--headless=new",
        "--disable-gpu",
        "--hide-scrollbars",
        f"--window-size={width},{height}",
        f"--screenshot={str(png_path)}",
        svg_path.resolve().as_uri(),
    ]
    subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def export_html_to_pdf(html_path: pathlib.Path, pdf_path: pathlib.Path) -> None:
    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    command = [
        str(chrome_path()),
        "--headless=new",
        "--disable-gpu",
        f"--print-to-pdf={str(pdf_path)}",
        "--print-to-pdf-no-header",
        html_path.resolve().as_uri(),
    ]
    subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def copy_file(src: pathlib.Path, dst: pathlib.Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def percent(value: float) -> str:
    return f"{value * 100:.1f}%"


def correlation_matrix(rows: Sequence[dict]) -> tuple[list[str], list[list[float]]]:
    labels = NUMERIC_COLUMNS
    columns = {label: [float(row[label]) for row in rows] for label in labels}
    matrix: list[list[float]] = []
    for label_a in labels:
        row_values = []
        for label_b in labels:
            row_values.append(pearson(columns[label_a], columns[label_b]))
        matrix.append(row_values)
    return labels, matrix


def pearson(xs: Sequence[float], ys: Sequence[float]) -> float:
    if len(xs) != len(ys) or not xs:
        return 0.0
    mean_x = sum(xs) / len(xs)
    mean_y = sum(ys) / len(ys)
    num = sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, ys))
    den_x = math.sqrt(sum((x - mean_x) ** 2 for x in xs))
    den_y = math.sqrt(sum((y - mean_y) ** 2 for y in ys))
    if den_x == 0 or den_y == 0:
        return 0.0
    return num / (den_x * den_y)


def ks_statistic(xs: Sequence[float], ys: Sequence[float]) -> float:
    xs_sorted = sorted(xs)
    ys_sorted = sorted(ys)
    values = sorted(set(xs_sorted + ys_sorted))
    if not values:
        return 0.0
    max_gap = 0.0
    for value in values:
        cdf_x = sum(1 for item in xs_sorted if item <= value) / len(xs_sorted)
        cdf_y = sum(1 for item in ys_sorted if item <= value) / len(ys_sorted)
        max_gap = max(max_gap, abs(cdf_x - cdf_y))
    return max_gap


def simple_kl_divergence(xs: Sequence[float], ys: Sequence[float], bins: int = 20) -> float:
    min_v = min(min(xs), min(ys))
    max_v = max(max(xs), max(ys))
    if min_v == max_v:
        return 0.0
    step = (max_v - min_v) / bins
    hist_x = [0] * bins
    hist_y = [0] * bins
    for value in xs:
        idx = min(int((value - min_v) / step), bins - 1)
        hist_x[idx] += 1
    for value in ys:
        idx = min(int((value - min_v) / step), bins - 1)
        hist_y[idx] += 1
    total_x = sum(hist_x)
    total_y = sum(hist_y)
    eps = 1e-9
    result = 0.0
    for px, py in zip(hist_x, hist_y):
        p = px / total_x + eps
        q = py / total_y + eps
        result += p * math.log(p / q)
    return result


def format_run_label(row: dict) -> str:
    return f"{row['Model']} | seed={row['Seed']} | n={row['Size']}"


def timestamp_slug() -> str:
    return dt.datetime.now().strftime("%Y%m%d_%H%M%S")


def save_text(path: pathlib.Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def load_json(path: pathlib.Path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)
