from __future__ import annotations

from deliverable_utils import (
    DATA_DIR,
    GRAPH_SUBDIRS,
    REPORTS_DIR,
    SCHEMA_COLUMNS,
    ensure_directories,
    export_html_to_pdf,
    html_escape,
    load_dataset,
    load_metrics,
    model_summary_from_runs,
    to_data_uri,
    top_runs,
)


HTML_SOURCE = REPORTS_DIR / "full_report_source.html"
PDF_OUTPUT = REPORTS_DIR / "full_report.pdf"


def build_pdf_report() -> None:
    ensure_directories()
    rows = load_metrics()
    summaries = model_summary_from_runs(rows)
    best = max(rows, key=lambda row: row["Composite Score"])
    top10 = top_runs(rows, 10)
    dataset_rows = load_dataset(DATA_DIR / "best_synthetic_empirical_seed11_n5000.csv")[:15]

    images = {
        "ranking": to_data_uri(GRAPH_SUBDIRS["A"] / "composite_score_ranking.png"),
        "heatmap": to_data_uri(GRAPH_SUBDIRS["A"] / "metrics_heatmap_models.png"),
        "size": to_data_uri(GRAPH_SUBDIRS["B"] / "composite_vs_size.png"),
        "scatter": to_data_uri(GRAPH_SUBDIRS["B"] / "physics_vs_statistical_scatter.png"),
        "corr": to_data_uri(GRAPH_SUBDIRS["C"] / "correlation_matrix_comparison.png"),
        "kde_emp": to_data_uri(GRAPH_SUBDIRS["C"] / "kde_overlay_empirical_s11_n5000.png"),
        "kde_kde": to_data_uri(GRAPH_SUBDIRS["C"] / "kde_overlay_kde_s11_n5000.png"),
        "leaderboard": to_data_uri(GRAPH_SUBDIRS["D"] / "top10_leaderboard.png"),
    }

    appendix_rows = "".join(
        f"<tr><td>{row['Model']}</td><td>{row['Seed']}</td><td>{row['Size']}</td><td>{row['Physics Consistency']:.4f}</td><td>{row['Statistical Similarity']:.4f}</td><td>{row['ML Utility (TSTR)']:.4f}</td><td>{row['Privacy / Detection AUC']:.4f}</td><td>{row['Composite Score']:.4f}</td></tr>"
        for row in rows
    )
    summary_rows = "".join(
        f"<tr><td>{row['Model']}</td><td>{row['Mean Composite']:.4f}</td><td>{row['Mean Physics']:.4f}</td><td>{row['Mean Statistical Similarity']:.4f}</td><td>{row['Mean TSTR']:.4f}</td><td>{row['Mean Privacy']:.4f}</td></tr>"
        for row in summaries
    )
    top10_rows = "".join(
        f"<tr><td>{idx+1}</td><td>{row['Model']}</td><td>{row['Seed']}</td><td>{row['Size']}</td><td>{row['Composite Score']:.4f}</td></tr>"
        for idx, row in enumerate(top10)
    )
    dataset_preview = "".join(
        "<tr>" + "".join(f"<td>{html_escape(value)}</td>" for value in row.values()) + "</tr>" for row in dataset_rows
    )

    html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Aerospace Structural Data Synthesis — Full Report</title>
  <style>
    @page {{ size: A4; margin: 18mm 14mm 18mm 14mm; }}
    body {{ font-family: Arial, sans-serif; color: #10213b; margin: 0; }}
    h1, h2, h3 {{ color: #1a2744; margin: 0 0 10px; }}
    h1 {{ font-size: 28px; }}
    h2 {{ font-size: 20px; margin-top: 12px; }}
    p, li, td, th {{ font-size: 11px; line-height: 1.45; }}
    .page {{ page-break-after: always; padding-top: 8px; }}
    .cover {{ display: flex; flex-direction: column; justify-content: center; min-height: 95vh; }}
    .small {{ color: #4b5b77; }}
    .toc li {{ margin-bottom: 4px; }}
    table {{ width: 100%; border-collapse: collapse; }}
    th, td {{ border: 1px solid #d7dce5; padding: 6px 8px; text-align: left; }}
    th {{ background: #1a2744; color: white; }}
    tr:nth-child(even) td {{ background: #f5f7fb; }}
    img {{ width: 100%; margin: 10px 0 14px; border: 1px solid #d7dce5; }}
    .two-up {{ display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }}
  </style>
</head>
<body>
  <section class="page cover">
    <h1>Aerospace Structural Data Synthesis — Full Report</h1>
    <p class="small">Confidential — Client Deliverable</p>
    <p class="small">Prepared from the recorded experiment artifacts on file.</p>
    <p><strong>Date:</strong> 2026-03-17</p>
    <p><strong>Champion:</strong> Empirical | Seed 11 | Size 5000 | Composite {best['Composite Score']:.4f}</p>
  </section>
  <section class="page">
    <h2>Table of Contents</h2>
    <ol class="toc">
      <li>Executive Summary</li>
      <li>Methodology</li>
      <li>Model Benchmarking</li>
      <li>Statistical Analysis</li>
      <li>Top 10 Leaderboard</li>
      <li>Best Synthetic Dataset Sample</li>
      <li>Conclusions & Recommendations</li>
      <li>Appendix A: Full 72-run Metrics</li>
    </ol>
    <h2>Executive Summary</h2>
    <p>This report summarizes 72 recorded synthesis experiments across six model families for aerospace structural design data. The best observed run was Empirical with seed 11 and size 5000, reaching a composite score of {best['Composite Score']:.4f}. KDE produced the strongest average score across all of its runs, but Empirical supplied the single best client-ready configuration. The recommended operational policy is to use Empirical or KDE at size 1000 or above.</p>
    <h2>Methodology</h2>
    <p>The pipeline profiled the original 300-row, 22-feature aerospace dataset, trained six model families over three seeds and four generation scales, evaluated four quality pillars, and then ranked every run using the composite score. This deliverable package was assembled strictly from those recorded artifacts without rerunning the experiment suite.</p>
    <table><thead><tr><th>Model</th><th>Mean Composite</th><th>Mean Physics</th><th>Mean Stats</th><th>Mean TSTR</th><th>Mean Privacy</th></tr></thead><tbody>{summary_rows}</tbody></table>
  </section>
  <section class="page">
    <h2>Model Benchmarking Results</h2>
    <img src="{images['ranking']}" alt="Composite ranking">
    <img src="{images['heatmap']}" alt="Metrics heatmap">
    <img src="{images['size']}" alt="Composite vs size">
  </section>
  <section class="page">
    <h2>Statistical Analysis</h2>
    <img src="{images['scatter']}" alt="Physics vs statistical scatter">
    <img src="{images['corr']}" alt="Correlation matrix comparison">
  </section>
  <section class="page">
    <h2>KDE Overlay Visuals</h2>
    <div class="two-up">
      <img src="{images['kde_emp']}" alt="Empirical KDE overlay">
      <img src="{images['kde_kde']}" alt="KDE KDE overlay">
    </div>
  </section>
  <section class="page">
    <h2>Top 10 Leaderboard</h2>
    <img src="{images['leaderboard']}" alt="Leaderboard">
    <table><thead><tr><th>Rank</th><th>Model</th><th>Seed</th><th>Size</th><th>Composite</th></tr></thead><tbody>{top10_rows}</tbody></table>
  </section>
  <section class="page">
    <h2>Best Synthetic Dataset Sample</h2>
    <table><thead><tr>{''.join(f'<th>{html_escape(col)}</th>' for col in SCHEMA_COLUMNS)}</tr></thead><tbody>{dataset_preview}</tbody></table>
  </section>
  <section class="page">
    <h2>Conclusions & Recommendations</h2>
    <ol>
      <li>Use Empirical or KDE at size ≥ 1000 for production synthesis tasks.</li>
      <li>Prefer Empirical as the default because it delivered the strongest single configuration with the lowest operational complexity.</li>
      <li>Keep GMM and Copula as explanatory baselines, not primary delivery models.</li>
      <li>Defer MaskedPredictor pending architecture overhaul.</li>
      <li>Explore conditional and ensemble synthesis as the next phase of work.</li>
    </ol>
  </section>
  <section class="page">
    <h2>Appendix A: Full 72-run Metrics</h2>
    <table><thead><tr><th>Model</th><th>Seed</th><th>Size</th><th>Physics</th><th>Stats</th><th>TSTR</th><th>Privacy</th><th>Composite</th></tr></thead><tbody>{appendix_rows}</tbody></table>
  </section>
</body>
</html>"""

    HTML_SOURCE.write_text(html, encoding="utf-8")
    export_html_to_pdf(HTML_SOURCE, PDF_OUTPUT)
    print(f"Saved {PDF_OUTPUT}")


if __name__ == "__main__":
    build_pdf_report()
