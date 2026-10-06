import os
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from config import ARTIFACTS_DIR, PLOTS_DIR, FINAL_DIR
from utils import logger

def plot_histograms(real_df, syn_df, top_features=6):
    """ Plots histograms for the top N continuous features. """
    # Find continuous features
    cont_cols = real_df.select_dtypes(include=[np.number]).columns.tolist()
    top_cols = cont_cols[:top_features]
    
    for col in top_cols:
        plt.figure(figsize=(10, 6))
        sns.histplot(real_df[col], color="blue", label="Real", kde=True, stat="density", alpha=0.5)
        sns.histplot(syn_df[col], color="orange", label="Synthetic", kde=True, stat="density", alpha=0.5)
        plt.title(f"Distribution Comparison: {col}")
        plt.legend()
        out_path = os.path.join(PLOTS_DIR, f"hist_{col.replace(' ', '_')}.png")
        plt.savefig(out_path)
        plt.close()
        logger.info(f"Saved histogram for {col}")

def plot_correlation_matrices(real_df, syn_df):
    """ Plots correlation heatmaps for continuous columns """
    cont_cols = real_df.select_dtypes(include=[np.number]).columns.tolist()
    
    # Real
    plt.figure(figsize=(12, 10))
    corr_real = real_df[cont_cols].corr()
    sns.heatmap(corr_real, cmap="coolwarm", center=0, annot=False)
    plt.title("Real Data Correlation Matrix")
    plt.savefig(os.path.join(PLOTS_DIR, "corr_real.png"))
    plt.close()
    
    # Synthetic
    plt.figure(figsize=(12, 10))
    corr_syn = syn_df[cont_cols].corr()
    sns.heatmap(corr_syn, cmap="coolwarm", center=0, annot=False)
    plt.title("Synthetic Data Correlation Matrix")
    plt.savefig(os.path.join(PLOTS_DIR, "corr_syn.png"))
    plt.close()
    
    # Diff
    plt.figure(figsize=(12, 10))
    corr_diff = corr_real - corr_syn
    sns.heatmap(corr_diff, cmap="bwr", center=0, annot=False)
    plt.title("Correlation Matrix Difference (Real - Synthetic)")
    plt.savefig(os.path.join(PLOTS_DIR, "corr_diff.png"))
    plt.close()
    logger.info("Saved correlation heatmaps")

def generate_report(results_df, real_df):
    """ Generates final artifacts: best_synthetic.csv, results_summary.json, report.md, notebook """
    logger.info("Generating Final Reports...")
    
    # Sort by Composite Score
    # The dataframe might contain nans if some runs failed, we drop them
    results_df = results_df.dropna(subset=['CompositeScore'])
    results_df = results_df.sort_values(by="CompositeScore", ascending=False)
    
    # Get Best Run
    best_run = results_df.iloc[0]
    best_model = best_run["Model"]
    best_score = best_run["CompositeScore"]
    best_syn_path = best_run["Path"]
    best_syn_df = pd.read_csv(best_syn_path)
    
    # Save Best Synthetic
    final_syn_path = os.path.join(FINAL_DIR, "best_synthetic.csv")
    best_syn_df.to_csv(final_syn_path, index=False)
    
    # Plotting for Best Run
    plot_histograms(real_df, best_syn_df, top_features=6)
    plot_correlation_matrices(real_df, best_syn_df)
    
    # Save JSON summary
    summary_dict = results_df.to_dict(orient="records")
    with open(os.path.join(FINAL_DIR, "results_summary.json"), "w") as f:
        json.dump(summary_dict, f, indent=4)
        
    # Generate MD Report
    report_path = os.path.join(FINAL_DIR, "report.md")
    with open(report_path, "w") as f:
        f.write("# Synthetic Data Generation Report\n\n")
        f.write("## Executive Summary\n")
        f.write(f"- **Best Model**: {best_model}\n")
        f.write(f"- **Sample Size**: {best_run['SampleSize']} (Seed: {best_run['Seed']})\n")
        f.write(f"- **Composite Score**: {best_score:.4f}\n")
        f.write(f"- **Hyperparameters**: `{best_run['Params']}`\n\n")
        
        f.write("### Top 3 Recommended Next Actions:\n")
        f.write("1. Incorporate this synthetic dataset into downstream ML training to improve generalization.\n")
        f.write("2. Analyze the synthetic tail events to discover edge-cases in aerospace design durability.\n")
        f.write("3. Refine Copula / Diffusions with a broader Optuna search grid overnight for marginal gains.\n\n")
        
        f.write("## Rankings\n")
        f.write(results_df[["Model", "Seed", "SampleSize", "CompositeScore"]].to_markdown(index=False))
        f.write("\n\n")
        
        f.write("## Visualizations\n")
        f.write("### Correlation Heatmap Differences\n")
        f.write("![Correlation Diff](../plots/corr_diff.png)\n\n")
        
        f.write("### Feature Distributions\n")
        cont_cols = real_df.select_dtypes(include=[np.number]).columns.tolist()[:6]
        for col in cont_cols:
            safe_col = col.replace(' ', '_')
            f.write(f"![{col} Hist](../plots/hist_{safe_col}.png)\n")
            
    # Generate basic Jupyter Notebook using JSON structure
    nb_content = {
        "cells": [
            {"cell_type": "markdown", "metadata": {}, "source": [f"# Reproduce Best Run: {best_model}"]},
            {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [],
             "source": ["import pandas as pd\n",
                        f"best_df = pd.read_csv('{final_syn_path}')\n",
                        "best_df.head()"]}
        ],
        "metadata": {"kernel_info": {"name": "python3"}, "language_info": {"name": "python"}},
        "nbformat": 4, "nbformat_minor": 4
    }
    with open(os.path.join(FINAL_DIR, "reproduce_best.ipynb"), "w") as f:
        json.dump(nb_content, f)

    logger.info("Reporting complete! All artifacts saved to /artifacts/final_decision/")
