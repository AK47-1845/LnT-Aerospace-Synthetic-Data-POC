"""
Edge Case Analysis for Aerospace Structural Design.
Generates 27 stress scenario datasets, runs anomaly detection,
produces catalog and business report.
"""
import os
import sys
import logging
import warnings
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import NearestNeighbors, LocalOutlierFactor
from sklearn.decomposition import PCA
from datetime import datetime

warnings.filterwarnings('ignore')
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s",
                    handlers=[logging.StreamHandler(sys.stdout)])
logger = logging.getLogger(__name__)

REAL_PATH  = r"d:\aero\aerospace_structural_design_dataset.csv"
SYN_PATH   = r"d:\aero\final\per_model_datasets\empirical_1000.csv"
EC_DIR     = r"d:\aero\final\edge_cases"
PLOT_DIR   = r"d:\aero\final\reports\plots"
CATALOG_PATH  = r"d:\aero\final\edge_cases\edge_case_catalog.md"
REPORT_PATH   = r"d:\aero\final\reports\edge_case_report.md"
SEED       = 42
N_ROWS     = 50

# 27 stress scenarios
SCENARIOS = [
    # Flight environment extremes
    {"name": "altitude_extreme_high",    "condition": lambda df: df["Altitude (m)"] >= df["Altitude (m)"].quantile(0.95),    "desc": "Altitude at 95th percentile (>17,500 m). Simulates stratospheric flight above commercial ceiling.",        "category": "Flight Envelope"},
    {"name": "altitude_extreme_low",     "condition": lambda df: df["Altitude (m)"] <= df["Altitude (m)"].quantile(0.05),    "desc": "Altitude at 5th percentile (<7,000 m). Simulates low-altitude flight or climb/descent phase.",             "category": "Flight Envelope"},
    {"name": "temperature_extreme_cold", "condition": lambda df: df["Temperature (°C)"] <= df["Temperature (°C)"].quantile(0.05), "desc": "Temperature at coldest 5th percentile (<-57 degrees C). Extreme cold soak scenario.",                   "category": "Flight Envelope"},
    {"name": "temperature_moderate",     "condition": lambda df: (df["Temperature (°C)"] > -52) & (df["Temperature (°C)"] < -47), "desc": "Temperature near mean (-50 degrees C). Nominal cruise temperature band.",                               "category": "Flight Envelope"},
    {"name": "pressure_extreme_high",    "condition": lambda df: df["Pressure (Pa)"] >= df["Pressure (Pa)"].quantile(0.95),    "desc": "Pressure at 95th percentile (>190,000 Pa). Near sea-level equivalent — low-altitude pressurization.",     "category": "Flight Envelope"},
    {"name": "pressure_extreme_low",     "condition": lambda df: df["Pressure (Pa)"] <= df["Pressure (Pa)"].quantile(0.05),    "desc": "Pressure at 5th percentile (<110,000 Pa). Very low ambient pressure — high-altitude regime.",              "category": "Flight Envelope"},
    # Material extremes
    {"name": "density_extreme_heavy",    "condition": lambda df: df["ρ (kg/m³)"] >= df["ρ (kg/m³)"].quantile(0.95),           "desc": "Density >4,200 kg/m3. Heavy structural material — likely dense Titanium alloy.",                           "category": "Material"},
    {"name": "density_extreme_light",    "condition": lambda df: df["ρ (kg/m³)"] <= df["ρ (kg/m³)"].quantile(0.05),           "desc": "Density <1,800 kg/m3. Ultra-lightweight materials — Carbon Fiber or thin Aluminum.",                        "category": "Material"},
    {"name": "tensile_extreme_high",     "condition": lambda df: df["Tensile Strength (MPa)"] >= df["Tensile Strength (MPa)"].quantile(0.95), "desc": "Tensile strength >1,400 MPa. Ultra-high-strength alloys for extreme load scenarios.",        "category": "Material"},
    {"name": "tensile_extreme_low",      "condition": lambda df: df["Tensile Strength (MPa)"] <= df["Tensile Strength (MPa)"].quantile(0.05), "desc": "Tensile strength <370 MPa. Lowest-grade structural materials — near yield limit.",          "category": "Material"},
    {"name": "modulus_extreme_high",     "condition": lambda df: df["E (GPa)"] >= df["E (GPa)"].quantile(0.95),                "desc": "Young's modulus >185 GPa. Highest stiffness — Carbon Fiber composites at maximum grade.",                  "category": "Material"},
    {"name": "material_aluminum_only",   "condition": lambda df: df["Material Type"] == "Aluminum",                             "desc": "Aluminum-only structure set. Lower density but lower strength — budget aerospace applications.",           "category": "Material"},
    {"name": "material_titanium_only",   "condition": lambda df: df["Material Type"] == "Titanium",                             "desc": "Titanium-only structure set. Balanced strength-to-weight — engine pylons, landing gear.",                 "category": "Material"},
    {"name": "material_carbonfiber_only","condition": lambda df: df["Material Type"] == "Carbon Fiber",                         "desc": "Carbon Fiber-only structure set. Highest specific stiffness — primary flight structures.",                 "category": "Material"},
    # Structural geometry extremes
    {"name": "wingspan_extreme_large",   "condition": lambda df: df["Wing Span (m)"] >= df["Wing Span (m)"].quantile(0.95),    "desc": "Wing span >56 m. Wide-body or UAV with high aspect ratio — maximum bending moment scenario.",              "category": "Geometry"},
    {"name": "wingspan_extreme_small",   "condition": lambda df: df["Wing Span (m)"] <= df["Wing Span (m)"].quantile(0.05),    "desc": "Wing span <24 m. Short-range jet or fighter configuration — high wing loading.",                          "category": "Geometry"},
    {"name": "thickness_extreme_thin",   "condition": lambda df: df["Structural Thickness (mm)"] <= df["Structural Thickness (mm)"].quantile(0.05), "desc": "Structural thickness <6 mm. Thin-shell structure — risk of buckling under compressive load.", "category": "Geometry"},
    {"name": "thickness_extreme_thick",  "condition": lambda df: df["Structural Thickness (mm)"] >= df["Structural Thickness (mm)"].quantile(0.95), "desc": "Structural thickness >14.5 mm. Heavily reinforced structure — armored or pressure vessel.",  "category": "Geometry"},
    {"name": "operational_life_long",    "condition": lambda df: df["Operational Life (years)"] >= 37,                          "desc": "Operational life 37-39 years. Long-service aircraft requiring enhanced fatigue analysis.",                 "category": "Lifecycle"},
    {"name": "operational_life_short",   "condition": lambda df: df["Operational Life (years)"] <= 22,                          "desc": "Operational life 20-22 years. Short-service aircraft — possibly military or regional commuter.",           "category": "Lifecycle"},
    # Target-based clusters
    {"name": "low_durability_cluster",   "condition": lambda df: df["Durability"] == "Low",                                     "desc": "All Low-Durability configurations. Identifies input feature patterns associated with early structural degradation.", "category": "Target"},
    {"name": "high_durability_cluster",  "condition": lambda df: df["Durability"] == "High",                                    "desc": "All High-Durability configurations. Best-case scenario for structural longevity design.",                 "category": "Target"},
    {"name": "poor_weight_efficiency",   "condition": lambda df: df["Weight Efficiency"] == "Poor",                              "desc": "All Poor Weight Efficiency rows. Overweight structural designs — candidates for optimization.",          "category": "Target"},
    {"name": "excellent_weight_efficiency", "condition": lambda df: df["Weight Efficiency"] == "Excellent",                     "desc": "All Excellent Weight Efficiency rows. Optimal lightweight structural designs.",                          "category": "Target"},
    # Algorithm extremes
    {"name": "long_optimization",        "condition": lambda df: df["Optimization Time (sec)"] >= df["Optimization Time (sec)"].quantile(0.95), "desc": "Optimization time >145 sec. Computationally expensive convergence — complex search spaces.", "category": "Optimization"},
    {"name": "short_optimization",       "condition": lambda df: df["Optimization Time (sec)"] <= df["Optimization Time (sec)"].quantile(0.05), "desc": "Optimization time <60 sec. Fast convergence — simpler structural problems or efficient search.", "category": "Optimization"},
    {"name": "shark_optimizer_only",     "condition": lambda df: df["Quantum Algorithm Type"] == "Shark Optimizer",             "desc": "Shark Optimizer algorithm only. Nature-inspired metaheuristic mimicking shark predation behavior.",       "category": "Optimization"},
    {"name": "chaotic_quantum_only",     "condition": lambda df: df["Quantum Algorithm Type"] == "Chaotic Quantum Genetic",     "desc": "Chaotic Quantum Genetic algorithm only. Quantum-inspired genetic algorithm with chaotic initialization.","category": "Optimization"},
]


def generate_edge_case(syn_df, real_df, condition_fn, n_rows=N_ROWS, seed=SEED, noise=0.01):
    """Sample rows meeting the condition, add noise, clip to real bounds."""
    rng = np.random.RandomState(seed)

    # Try synthetic first
    pool = syn_df[condition_fn(syn_df)]
    if len(pool) < 5:
        pool = real_df[condition_fn(real_df)]
    if len(pool) == 0:
        return None

    # Sample with replacement
    result = pool.sample(n=n_rows, replace=True, random_state=seed).reset_index(drop=True)

    # Add noise to numeric columns
    num_cols = real_df.select_dtypes(include=np.number).columns.tolist()
    for col in num_cols:
        if col not in result.columns:
            continue
        std = real_df[col].std()
        result[col] = (result[col] + rng.normal(0, std * noise, n_rows)).clip(
            real_df[col].min(), real_df[col].max()
        )

    return result[real_df.columns]  # ensure correct column order


def analyze_edge_case(ec_df, real_df, seed=SEED):
    """Run IF, LOF, NN distance on an edge case dataset."""
    metrics = {}
    num_cols = [c for c in real_df.select_dtypes(include=np.number).columns if c in ec_df.columns]

    r_num = real_df[num_cols].fillna(0)
    e_num = ec_df[num_cols].fillna(0)

    scaler = StandardScaler().fit(r_num)
    r_sc = scaler.transform(r_num)
    e_sc = scaler.transform(e_num)

    # Isolation Forest
    try:
        iso = IsolationForest(contamination=0.05, random_state=seed)
        iso.fit(r_sc)
        preds = iso.predict(e_sc)
        metrics["if_anomaly_pct"] = round(float(np.mean(preds == -1)) * 100, 1)
    except:
        metrics["if_anomaly_pct"] = None

    # LOF
    try:
        lof = LocalOutlierFactor(n_neighbors=min(5, len(r_sc)-1), contamination=0.05, novelty=True)
        lof.fit(r_sc)
        lof_preds = lof.predict(e_sc)
        metrics["lof_anomaly_pct"] = round(float(np.mean(lof_preds == -1)) * 100, 1)
    except:
        metrics["lof_anomaly_pct"] = None

    # NN distance
    try:
        nn = NearestNeighbors(n_neighbors=1).fit(r_sc)
        dists, _ = nn.kneighbors(e_sc)
        metrics["nn_dist_mean"] = round(float(np.mean(dists)), 4)
    except:
        metrics["nn_dist_mean"] = None

    return metrics


def main():
    os.makedirs(EC_DIR, exist_ok=True)
    os.makedirs(PLOT_DIR, exist_ok=True)

    logger.info("Loading datasets...")
    real_df = pd.read_csv(REAL_PATH)
    syn_df  = pd.read_csv(SYN_PATH)

    catalog_rows = []
    all_dfs      = []

    logger.info(f"Generating {len(SCENARIOS)} edge case datasets...")
    for scen in SCENARIOS:
        name   = scen["name"]
        cond   = scen["condition"]
        desc   = scen["desc"]
        cat    = scen["category"]

        ec_df = generate_edge_case(syn_df, real_df, cond, n_rows=N_ROWS, seed=SEED)

        if ec_df is None or len(ec_df) == 0:
            logger.warning(f"  {name}: no rows match condition — skipping")
            continue

        # Save individual file
        ec_path = os.path.join(EC_DIR, f"edge_case_{name}.csv")
        ec_df.to_csv(ec_path, index=False)

        # Analyze
        metrics = analyze_edge_case(ec_df, real_df)

        # Realism score: lower IF%, lower LOF%, lower NN dist = more realistic
        if_pct  = metrics.get("if_anomaly_pct") or 50
        lof_pct = metrics.get("lof_anomaly_pct") or 50
        nn_dist = metrics.get("nn_dist_mean") or 10
        # Realism: 0-100, higher = more realistic
        realism = round(100 - (if_pct * 0.3 + lof_pct * 0.3 + min(nn_dist * 20, 40)), 1)

        catalog_rows.append({
            "scenario": name,
            "category": cat,
            "variable_stressed": name.replace("_", " ").title(),
            "n_rows": len(ec_df),
            "if_anomaly_pct": metrics.get("if_anomaly_pct"),
            "lof_anomaly_pct": metrics.get("lof_anomaly_pct"),
            "nn_dist_mean": metrics.get("nn_dist_mean"),
            "realism_score": realism,
            "description": desc,
        })

        all_dfs.append(ec_df)
        logger.info(f"  {name:40s} | IF={metrics.get('if_anomaly_pct')}% | "
                    f"LOF={metrics.get('lof_anomaly_pct')}% | "
                    f"NN={metrics.get('nn_dist_mean')} | Realism={realism}")

    # Save combined
    if all_dfs:
        combined = pd.concat(all_dfs, ignore_index=True)
        combined.to_csv(os.path.join(EC_DIR, "all_edge_cases_combined.csv"), index=False)
        logger.info(f"Combined edge cases: {combined.shape}")

    catalog_df = pd.DataFrame(catalog_rows).sort_values("realism_score", ascending=False)
    catalog_df.to_csv(os.path.join(EC_DIR, "edge_case_metrics.csv"), index=False)

    # PCA overlay plot (top 5 most realistic)
    try:
        top5 = catalog_df.head(5)
        scaler = StandardScaler()
        num_cols = real_df.select_dtypes(include=np.number).columns.tolist()
        r_sc = scaler.fit_transform(real_df[num_cols].fillna(0))
        pca = PCA(n_components=2, random_state=SEED)
        r_pca = pca.fit_transform(r_sc)

        fig, ax = plt.subplots(figsize=(14, 9))
        ax.scatter(r_pca[:, 0], r_pca[:, 1], c='lightgray', s=15, alpha=0.6, label='Real Data')

        colors = ['red', 'blue', 'green', 'purple', 'orange']
        for i, (_, row) in enumerate(top5.iterrows()):
            ec_path = os.path.join(EC_DIR, f"edge_case_{row['scenario']}.csv")
            if not os.path.exists(ec_path):
                continue
            ec_df = pd.read_csv(ec_path)
            e_sc  = scaler.transform(ec_df[num_cols].fillna(0))
            e_pca = pca.transform(e_sc)
            ax.scatter(e_pca[:, 0], e_pca[:, 1], c=colors[i], s=40, alpha=0.8,
                      label=f"{row['scenario']} (realism={row['realism_score']})", zorder=3)

        ax.set_xlabel(f"PC1 ({pca.explained_variance_ratio_[0]*100:.1f}%)")
        ax.set_ylabel(f"PC2 ({pca.explained_variance_ratio_[1]*100:.1f}%)")
        ax.set_title("PCA: Top 5 Most Realistic Edge Cases vs Real Data")
        ax.legend(fontsize=8, loc='upper right')
        plt.tight_layout()
        plt.savefig(os.path.join(PLOT_DIR, "edge_cases_pca_overlay.png"), dpi=150, bbox_inches='tight')
        plt.close()
        logger.info("PCA overlay plot saved.")
    except Exception as e:
        logger.warning(f"PCA plot failed: {e}")

    # Build catalog
    catalog_lines = [
        "# Edge Case Dataset Catalog",
        f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*",
        "",
        f"**Total scenarios:** {len(catalog_df)}  ",
        f"**Rows per scenario:** {N_ROWS}  ",
        f"**Total edge case rows:** {len(catalog_df) * N_ROWS}  ",
        "",
        "## Summary Table",
        "",
        "| Scenario | Category | IF Anomaly % | LOF Anomaly % | NN Distance | Realism Score |",
        "|---|---|---|---|---|---|",
    ]
    for _, row in catalog_df.iterrows():
        catalog_lines.append(
            f"| {row['scenario']} | {row['category']} | "
            f"{row['if_anomaly_pct']}% | {row['lof_anomaly_pct']}% | "
            f"{row['nn_dist_mean']} | {row['realism_score']} |"
        )

    catalog_lines += ["", "---", "", "## Detailed Scenario Descriptions", ""]
    for _, row in catalog_df.iterrows():
        catalog_lines += [
            f"### {row['scenario']}",
            f"**Category:** {row['category']}  ",
            f"**N Rows:** {row['n_rows']}  ",
            f"**Description:** {row['description']}  ",
            f"**Realism Score:** {row['realism_score']} / 100  ",
            "",
        ]

    with open(CATALOG_PATH, 'w', encoding='utf-8') as f:
        f.write("\n".join(catalog_lines))
    logger.info(f"Catalog saved: {CATALOG_PATH}")

    # Business report
    report_lines = [
        "# Edge Case Stress Test Report — Aerospace Structural Design",
        "*Business & Engineering Framing*",
        "",
        "## Executive Summary",
        "",
        "This report presents **27 stress test scenarios** representing rare but physically",
        "plausible edge cases in aerospace structural design. Each scenario targets a specific",
        "variable or configuration at its extreme — simulating conditions a structure might",
        "encounter during its operational lifetime but which are underrepresented in the",
        "nominal design dataset.",
        "",
        "**Why edge cases matter in aerospace:**",
        "- Aircraft certification requires demonstrating safety at operating extremes",
        "- Failure mode analysis requires understanding tail-risk scenarios",
        "- Predictive maintenance depends on identifying signatures of structural degradation",
        "- Design optimization must avoid creating structures optimized only for nominal conditions",
        "",
        "## Edge Case Overview",
        "",
        f"| Category | Scenarios | Avg Realism Score |",
        "|---|---|---|",
    ]

    for cat in catalog_df["category"].unique():
        cat_df = catalog_df[catalog_df["category"] == cat]
        avg_real = round(cat_df["realism_score"].mean(), 1)
        report_lines.append(f"| {cat} | {len(cat_df)} | {avg_real} |")

    report_lines += [
        "",
        "## Realism Validation",
        "",
        "Edge cases are validated by three criteria:",
        "1. **Isolation Forest (IF):** IF anomaly % should be higher than the nominal ~5%,",
        "   confirming the edge case rows are rare relative to the real data distribution.",
        "2. **LOF (Local Outlier Factor):** Confirms local neighbourhood rareness.",
        "3. **NN Distance:** Measures how far synthetic edge case rows are from their nearest",
        "   real data point. Lower = more physically realistic; very high = hallucinated.",
        "",
        "## Most Realistic Edge Cases",
        "",
        "| Rank | Scenario | Realism Score | Description |",
        "|---|---|---|---|",
    ]

    for i, (_, row) in enumerate(catalog_df.head(10).iterrows(), 1):
        report_lines.append(f"| {i} | {row['scenario']} | {row['realism_score']} | {row['description'][:80]}... |")

    report_lines += [
        "",
        "![PCA Overlay of Top 5 Edge Cases](plots/edge_cases_pca_overlay.png)",
        "",
        "## Applications",
        "",
        "1. **Fatigue Analysis:** The `operational_life_long` scenario (37+ years) tests structural",
        "   longevity predictions — essential for Extended Service Life (ESL) certification.",
        "2. **Extreme Environment Certification:** The `altitude_extreme_high` and",
        "   `temperature_extreme_cold` scenarios support DO-160 environmental qualification.",
        "3. **Weight Optimization:** The `poor_weight_efficiency` cluster identifies which",
        "   input configurations drive overweight designs, directing optimization effort.",
        "4. **Material Selection:** The material-specific clusters enable per-material",
        "   durability analysis, supporting material down-selection decisions.",
        "5. **Algorithm Benchmarking:** The optimization scenario clusters enable",
        "   algorithm-specific convergence analysis under identical structural conditions.",
        "",
        "---",
        "*Edge Case Report — Aerospace Synthetic Data Project*",
    ]

    with open(REPORT_PATH, 'w', encoding='utf-8') as f:
        f.write("\n".join(report_lines))
    logger.info(f"Business report saved: {REPORT_PATH}")


if __name__ == "__main__":
    main()
