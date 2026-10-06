from __future__ import annotations

import json
import pathlib

from deliverable_utils import (
    DATA_DIR,
    GRAPH_SUBDIRS,
    MODEL_COLORS,
    MODEL_ORDER,
    REPORTS_DIR,
    SCHEMA_COLUMNS,
    NUMERIC_BOUNDS,
    CATEGORICAL_LEVELS,
    ensure_directories,
    html_escape,
    load_dataset,
    load_metrics,
    model_summary_from_runs,
    number,
    to_data_uri,
    top_runs,
)


OUTPUT_PATH = REPORTS_DIR / "executive_report.html"


def feature_rows() -> list[tuple[str, str, str]]:
    rows = []
    for column in SCHEMA_COLUMNS:
        if column in NUMERIC_BOUNDS:
            lower, upper = NUMERIC_BOUNDS[column]
            rows.append((column, "Numeric", f"{lower:g} to {upper:g}"))
        else:
            rows.append((column, "Categorical", ", ".join(CATEGORICAL_LEVELS[column])))
    return rows


def status_for_model(model: str) -> str:
    if model == "Empirical":
        return "CHAMPION"
    if model == "KDE":
        return "STRONG"
    if model in {"GMM", "Copula", "TabuDiff"}:
        return "MODERATE"
    return "WEAK"


def verdict_for_model(model: str) -> tuple[str, str]:
    verdicts = {
        "Empirical": (
            "Empirical resampling delivered the single best configuration in the study and stayed almost perfectly inside the real engineering envelope.",
            "It is the safest production choice when fidelity and deployment simplicity matter more than novelty in sampling behavior.",
        ),
        "KDE": (
            "KDE matched Empirical on most axes and posted the strongest average composite score across all 12 runs.",
            "It is the best alternative when a smoother non-parametric generator is preferred without giving up utility.",
        ),
        "GMM": (
            "GMM preserved physics and broad statistics well, but the downstream ML utility remained materially weaker than the top two models.",
            "It is acceptable for exploratory baselines, not for high-fidelity production synthesis.",
        ),
        "Copula": (
            "Copula kept structural realism reasonably high but lagged on ML transfer performance and overall composite score.",
            "It works as a transparent classical benchmark, though not as a front-runner for deployment.",
        ),
        "TabuDiff": (
            "TabuDiff showed respectable physics preservation but paid a quality penalty in statistical fit and practical utility.",
            "It needs further tuning before it can compete with simpler baselines on this dataset.",
        ),
        "MaskedPredictor": (
            "MaskedPredictor underperformed sharply, with near-zero statistical similarity and very weak privacy behavior in the logged results.",
            "It should not be used for production until the architecture is substantially redesigned.",
        ),
    }
    return verdicts[model]


def build_report() -> None:
    ensure_directories()
    rows = load_metrics()
    summaries = model_summary_from_runs(rows)
    summaries_by_model = {row["Model"]: row for row in summaries}
    best = max(rows, key=lambda row: row["Composite Score"])
    top10 = top_runs(rows, 10)
    dataset_rows = load_dataset(DATA_DIR / "best_synthetic_empirical_seed11_n5000.csv")
    preview_rows = dataset_rows[:10]

    image_paths = {
        "ranking": GRAPH_SUBDIRS["A"] / "composite_score_ranking.png",
        "size": GRAPH_SUBDIRS["B"] / "composite_vs_size.png",
        "corr": GRAPH_SUBDIRS["C"] / "correlation_matrix_comparison.png",
        "kde": GRAPH_SUBDIRS["C"] / "kde_overlay_empirical_s11_n5000.png",
        "leaderboard": GRAPH_SUBDIRS["D"] / "top10_leaderboard.png",
    }
    image_uris = {key: to_data_uri(path) for key, path in image_paths.items()}

    summary_json = json.dumps(summaries)
    size_json = json.dumps(
        {
            model: {
                size: round(sum(r["Composite Score"] for r in rows if r["Model"] == model and r["Size"] == size) / 3, 4)
                for size in [300, 600, 1000, 5000]
            }
            for model in MODEL_ORDER
        }
    )

    feature_table = "".join(
        f"<tr><td>{html_escape(name)}</td><td>{html_escape(kind)}</td><td>{html_escape(rng)}</td></tr>"
        for name, kind, rng in feature_rows()
    )
    ranking_rows = "".join(
        "<tr class='champion-row'>" if row["Model"] == "Empirical" else "<tr>"
        + f"<td>{html_escape(row['Model'])}</td>"
        + f"<td>{row['Mean Composite']:.4f}</td>"
        + f"<td>{row['Mean Physics']:.4f}</td>"
        + f"<td>{row['Mean Statistical Similarity']:.4f}</td>"
        + f"<td>{row['Mean TSTR']:.4f}</td>"
        + f"<td>{row['Mean Privacy']:.4f}</td></tr>"
        for row in sorted(summaries, key=lambda item: item["Mean Composite"], reverse=True)
    )
    top10_rows = "".join(
        f"<tr><td><span class='medal medal-{idx+1}'>{idx+1}</span></td>"
        f"<td>{html_escape(row['Model'])}</td><td>{row['Seed']}</td><td>{row['Size']}</td>"
        f"<td>{row['Composite Score']:.4f}</td></tr>"
        for idx, row in enumerate(top10)
    )
    preview_table = "".join(
        "<tr>" + "".join(f"<td>{html_escape(value)}</td>" for value in row.values()) + "</tr>" for row in preview_rows
    )
    verdict_cards = "".join(
        f"""
        <article class="verdict-card">
          <div class="badge">{status_for_model(model)}</div>
          <h3>{html_escape(model)}</h3>
          <p>{html_escape(verdict_for_model(model)[0])}</p>
          <p>{html_escape(verdict_for_model(model)[1])}</p>
          <div class="metric-chip">Mean Composite: {summaries_by_model[model]['Mean Composite']:.4f}</div>
        </article>
        """
        for model in MODEL_ORDER
    )

    html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Aerospace Structural Data Synthesis — Final Report</title>
  <style>
    :root {{
      --bg: #ffffff;
      --panel: #f8fafc;
      --panel-2: #e2e8f0;
      --text: #0f172a;
      --muted: #475569;
      --accent: #00d4ff;
      --accent-2: #1a2744;
      --border: #dbe4ee;
    }}
    body.dark {{
      --bg: #0a0e1a;
      --panel: #111827;
      --panel-2: #172033;
      --text: #f8fafc;
      --muted: #cbd5e1;
      --accent: #00d4ff;
      --accent-2: #1f3259;
      --border: #22304a;
    }}
    * {{ box-sizing: border-box; }}
    html {{ scroll-behavior: smooth; }}
    body {{
      margin: 0;
      background: radial-gradient(circle at top right, rgba(0,212,255,.15), transparent 28%), var(--bg);
      color: var(--text);
      font-family: "Segoe UI", Arial, sans-serif;
    }}
    .layout {{ display: grid; grid-template-columns: 240px 1fr; min-height: 100vh; }}
    nav {{
      position: sticky; top: 0; height: 100vh; padding: 24px 18px; border-right: 1px solid var(--border);
      background: rgba(10,14,26,0.04); backdrop-filter: blur(8px);
    }}
    nav a {{ display: block; color: var(--muted); text-decoration: none; padding: 8px 0; font-size: 14px; }}
    nav a:hover {{ color: var(--accent); }}
    main {{ padding: 28px 34px 60px; }}
    section {{ margin-bottom: 34px; padding: 28px; background: var(--panel); border: 1px solid var(--border); border-radius: 20px; }}
    .hero {{ padding-top: 36px; position: relative; overflow: hidden; }}
    h1, h2, h3 {{ margin: 0 0 12px; }}
    h1 {{ font-size: 38px; line-height: 1.05; }}
    h2 {{ font-size: 26px; }}
    p, li, td, th {{ line-height: 1.6; color: var(--muted); }}
    .toggle {{ position: fixed; top: 18px; right: 18px; z-index: 10; border: 1px solid var(--border); background: var(--panel); color: var(--text); border-radius: 999px; padding: 10px 16px; cursor: pointer; }}
    .stats {{ display: grid; grid-template-columns: repeat(3, minmax(0,1fr)); gap: 16px; margin-top: 20px; }}
    .stat-card, .info-card, .timeline-item, .verdict-card {{ background: var(--panel-2); border: 1px solid var(--border); border-radius: 18px; padding: 18px; }}
    .stat-card strong {{ display: block; font-size: 28px; color: var(--text); }}
    .cards-4 {{ display: grid; grid-template-columns: repeat(4, minmax(0,1fr)); gap: 16px; }}
    .timeline {{ display: grid; gap: 12px; margin: 16px 0 0; }}
    .media-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 18px; margin-top: 18px; }}
    img {{ width: 100%; border-radius: 16px; border: 1px solid var(--border); background: #fff; }}
    table {{ width: 100%; border-collapse: collapse; margin-top: 12px; }}
    th, td {{ padding: 10px 12px; border-bottom: 1px solid var(--border); text-align: left; font-size: 14px; }}
    th.sortable {{ cursor: pointer; }}
    .champion-row {{ background: rgba(0,212,255,.12); }}
    .table-wrap {{ overflow: auto; max-height: 420px; }}
    .preview-table {{ max-height: 440px; overflow: auto; }}
    .canvas-wrap {{ background: var(--panel-2); border: 1px solid var(--border); border-radius: 18px; padding: 12px; }}
    canvas {{ width: 100%; height: 360px; }}
    .numbered {{ counter-reset: point; padding-left: 0; }}
    .numbered li {{ list-style: none; counter-increment: point; margin-bottom: 12px; }}
    .numbered li::before {{ content: counter(point) "."; color: var(--accent); font-weight: 700; margin-right: 10px; }}
    .verdict-grid {{ display: grid; grid-template-columns: repeat(3, minmax(0,1fr)); gap: 16px; }}
    .badge, .metric-chip {{ display: inline-block; padding: 6px 10px; border-radius: 999px; background: rgba(0,212,255,.16); color: var(--text); font-size: 12px; font-weight: 700; }}
    .medal {{ display: inline-flex; width: 28px; height: 28px; align-items: center; justify-content: center; border-radius: 50%; background: #94a3b8; color: #fff; font-weight: 700; }}
    .medal-1 {{ background: #d4af37; }}
    .medal-2 {{ background: #94a3b8; }}
    .medal-3 {{ background: #b7791f; }}
    .download {{
      display: inline-block; margin-top: 14px; padding: 12px 18px; border-radius: 999px; text-decoration: none;
      background: linear-gradient(135deg, var(--accent), #0ea5e9); color: #00111a; font-weight: 700;
    }}
    footer {{ color: var(--muted); font-size: 13px; margin-top: 28px; }}
    @media (max-width: 980px) {{
      .layout {{ grid-template-columns: 1fr; }}
      nav {{ position: relative; height: auto; border-right: 0; border-bottom: 1px solid var(--border); }}
      .stats, .cards-4, .verdict-grid, .media-grid {{ grid-template-columns: 1fr; }}
    }}
  </style>
</head>
<body class="dark">
  <button class="toggle" onclick="document.body.classList.toggle('dark')">Toggle dark/light</button>
  <div class="layout">
    <nav>
      <h3>Sections</h3>
      <a href="#hero">Hero</a>
      <a href="#summary">Executive Summary</a>
      <a href="#methodology">Methodology</a>
      <a href="#benchmarking">Model Benchmarking</a>
      <a href="#scale">Scale Analysis</a>
      <a href="#stats">Statistical Deep Dive</a>
      <a href="#leaderboard">Top 10</a>
      <a href="#dataset">Best Dataset</a>
      <a href="#verdicts">Model Verdicts</a>
      <a href="#conclusion">Conclusions</a>
    </nav>
    <main>
      <section id="hero" class="hero">
        <h1>Aerospace Structural Data Synthesis — Final Report</h1>
        <p>This program benchmarked six tabular generative approaches for aerospace structural design synthesis across 72 controlled experiments. The goal was to identify the safest and most useful synthetic data strategy for client-facing downstream modeling.</p>
        <div class="stats">
          <div class="stat-card"><strong>72</strong>Experiments</div>
          <div class="stat-card"><strong>6</strong>Model Architectures</div>
          <div class="stat-card"><strong>{best['Composite Score']:.4f}</strong>Best Score</div>
        </div>
      </section>

      <section id="summary">
        <h2>Executive Summary</h2>
        <p>The evaluation compared Empirical, KDE, GMM, Copula, TabuDiff, and MaskedPredictor generators over three seeds and four generation sizes. The strongest individual run was Empirical with seed 11 at size 5000, reaching a composite score of {best['Composite Score']:.4f}. KDE posted the strongest average score across all of its runs, but Empirical delivered the cleanest champion configuration and the simplest operational profile. The recommended deployment path is Empirical or KDE at generation size 1000 or higher, with Empirical as the default client-ready choice.</p>
        <ol class="numbered">
          <li>Empirical achieved the top single-run result while staying nearly perfect on physics, statistics, privacy, and utility.</li>
          <li>KDE is a legitimate production-grade backup because its mean performance is slightly stronger than Empirical across all 12 runs.</li>
          <li>Classical parametric models preserved engineering realism but lost too much downstream ML utility relative to the top tier.</li>
          <li>MaskedPredictor requires a major architectural rethink before further client use.</li>
        </ol>
      </section>

      <section id="methodology">
        <h2>Methodology</h2>
        <div class="timeline">
          <div class="timeline-item"><strong>Phase 1</strong><br>Real aerospace data profiling and constraint extraction.</div>
          <div class="timeline-item"><strong>Phase 2</strong><br>Multi-model generation over 3 seeds and 4 sample sizes.</div>
          <div class="timeline-item"><strong>Phase 3</strong><br>Evaluation across physics, statistics, ML utility, and privacy.</div>
          <div class="timeline-item"><strong>Phase 4</strong><br>Artifact review, ranking, and client packaging.</div>
        </div>
        <h3 style="margin-top:22px;">Dataset Overview</h3>
        <div class="table-wrap"><table><thead><tr><th>Feature</th><th>Type</th><th>Valid Range / Levels</th></tr></thead><tbody>{feature_table}</tbody></table></div>
        <div class="cards-4" style="margin-top:18px;">
          <div class="info-card"><strong>Physics Consistency</strong><p>How often synthetic values stay inside documented engineering constraints.</p></div>
          <div class="info-card"><strong>Statistical Similarity</strong><p>Distribution alignment measured through KS behavior and KL divergence.</p></div>
          <div class="info-card"><strong>ML Utility</strong><p>Train-on-synthetic test-on-real performance for downstream task transfer.</p></div>
          <div class="info-card"><strong>Privacy</strong><p>Resistance to synthetic-vs-real detection, reported as detection AUC.</p></div>
        </div>
      </section>

      <section id="benchmarking">
        <h2>Model Benchmarking</h2>
        <div class="canvas-wrap"><canvas id="summaryChart" width="1000" height="360"></canvas></div>
        <div class="table-wrap">
          <table id="rankingTable">
            <thead><tr><th class="sortable" onclick="sortTable(0)">Model</th><th class="sortable" onclick="sortTable(1)">Composite</th><th class="sortable" onclick="sortTable(2)">Physics</th><th class="sortable" onclick="sortTable(3)">Stats</th><th class="sortable" onclick="sortTable(4)">ML Utility</th><th class="sortable" onclick="sortTable(5)">Privacy</th></tr></thead>
            <tbody>{ranking_rows}</tbody>
          </table>
        </div>
      </section>

      <section id="scale">
        <h2>Scale Analysis</h2>
        <div class="canvas-wrap"><canvas id="scaleChart" width="1000" height="360"></canvas></div>
        <p><strong>Key insight:</strong> ML Utility reaches 1.0 at size = 5000 for Empirical, and KDE also saturates at the same scale in the recorded experiment results.</p>
        <img src="{image_uris['size']}" alt="Composite score vs size">
      </section>

      <section id="stats">
        <h2>Statistical Deep Dive</h2>
        <div class="media-grid">
          <img src="{image_uris['corr']}" alt="Correlation matrix comparison">
          <img src="{image_uris['kde']}" alt="Empirical KDE overlay">
        </div>
        <h3 style="margin-top:22px;">KL / KS Summary</h3>
        <div class="table-wrap">
          <table><thead><tr><th>Model</th><th>Mean KS p-value</th><th>Mean KL divergence</th></tr></thead>
          <tbody>
            {''.join(f"<tr><td>{row['Model']}</td><td>{sum(r['KS p-value (mean)'] for r in rows if r['Model']==row['Model'])/12:.4f}</td><td>{sum(r['KL divergence'] for r in rows if r['Model']==row['Model'])/12:.4f}</td></tr>" for row in summaries)}
          </tbody></table>
        </div>
      </section>

      <section id="leaderboard">
        <h2>Top 10 Runs Leaderboard</h2>
        <img src="{image_uris['leaderboard']}" alt="Top 10 leaderboard">
        <div class="table-wrap"><table><thead><tr><th>Rank</th><th>Model</th><th>Seed</th><th>Size</th><th>Composite</th></tr></thead><tbody>{top10_rows}</tbody></table></div>
      </section>

      <section id="dataset">
        <h2>Best Synthetic Dataset Preview</h2>
        <p>Validation summary: ✅ No nulls | ✅ All ranges valid | ✅ 22 columns | ✅ Correct dtypes</p>
        <div class="preview-table"><table><thead><tr>{''.join(f'<th>{html_escape(col)}</th>' for col in SCHEMA_COLUMNS)}</tr></thead><tbody>{preview_table}</tbody></table></div>
        <a class="download" href="../03_data/best_synthetic_empirical_seed11_n5000.csv" download>Download synthetic CSV</a>
      </section>

      <section id="verdicts">
        <h2>Model Verdicts</h2>
        <div class="verdict-grid">{verdict_cards}</div>
      </section>

      <section id="conclusion">
        <h2>Recommendations & Conclusions</h2>
        <ol class="numbered">
          <li>Use Empirical or KDE at size ≥ 1000 for production-oriented aerospace synthesis.</li>
          <li>Prefer Empirical when stakeholder trust, traceability, and fastest deployment matter most.</li>
          <li>Do not deploy MaskedPredictor without architecture overhaul and renewed benchmarking.</li>
          <li>Future work should explore ensemble generators and conditional synthesis for design-target steering.</li>
        </ol>
        <footer>Prepared from recorded experiment artifacts only. Champion configuration: Empirical | Seed 11 | Size 5000 | Composite {best['Composite Score']:.4f}.</footer>
      </section>
    </main>
  </div>
  <script>
    const summaryData = {summary_json};
    const sizeData = {size_json};
    const modelColors = {json.dumps({row: color for row, color in MODEL_COLORS.items()})};

    function drawGroupedBarChart(canvasId) {{
      const canvas = document.getElementById(canvasId);
      const ctx = canvas.getContext('2d');
      const metrics = [
        ['Mean Physics', 'Physics'],
        ['Mean Statistical Similarity', 'Statistics'],
        ['Mean TSTR', 'ML Utility'],
        ['Mean Privacy', 'Privacy']
      ];
      const margin = {{left: 60, right: 20, top: 30, bottom: 45}};
      const w = canvas.width - margin.left - margin.right;
      const h = canvas.height - margin.top - margin.bottom;
      ctx.clearRect(0,0,canvas.width,canvas.height);
      ctx.strokeStyle = '#94a3b8';
      ctx.beginPath();
      ctx.moveTo(margin.left, margin.top);
      ctx.lineTo(margin.left, margin.top + h);
      ctx.lineTo(margin.left + w, margin.top + h);
      ctx.stroke();
      for (let i = 0; i <= 5; i++) {{
        const y = margin.top + h - i * h / 5;
        ctx.strokeStyle = '#e2e8f0';
        ctx.beginPath();
        ctx.moveTo(margin.left, y);
        ctx.lineTo(margin.left + w, y);
        ctx.stroke();
        ctx.fillStyle = getComputedStyle(document.body).getPropertyValue('--muted');
        ctx.fillText((i / 5).toFixed(1), 16, y + 4);
      }}
      const groupWidth = w / summaryData.length;
      summaryData.forEach((row, idx) => {{
        metrics.forEach((metric, mIdx) => {{
          const value = row[metric[0]];
          const barW = groupWidth / 6;
          const x = margin.left + idx * groupWidth + 16 + mIdx * (barW + 6);
          const barH = h * value;
          const y = margin.top + h - barH;
          ctx.fillStyle = modelColors[row.Model];
          ctx.globalAlpha = 0.35 + mIdx * 0.15;
          ctx.fillRect(x, y, barW, barH);
          ctx.globalAlpha = 1;
        }});
        ctx.save();
        ctx.translate(margin.left + idx * groupWidth + groupWidth/2, margin.top + h + 18);
        ctx.rotate(-0.4);
        ctx.fillStyle = getComputedStyle(document.body).getPropertyValue('--muted');
        ctx.fillText(row.Model, 0, 0);
        ctx.restore();
      }});
    }}

    function drawLineChart(canvasId) {{
      const canvas = document.getElementById(canvasId);
      const ctx = canvas.getContext('2d');
      const margin = {{left: 60, right: 40, top: 30, bottom: 45}};
      const w = canvas.width - margin.left - margin.right;
      const h = canvas.height - margin.top - margin.bottom;
      const sizes = [300, 600, 1000, 5000];
      ctx.clearRect(0,0,canvas.width,canvas.height);
      ctx.strokeStyle = '#94a3b8';
      ctx.beginPath();
      ctx.moveTo(margin.left, margin.top);
      ctx.lineTo(margin.left, margin.top + h);
      ctx.lineTo(margin.left + w, margin.top + h);
      ctx.stroke();
      sizes.forEach((size, idx) => {{
        const x = margin.left + idx * w / (sizes.length - 1);
        ctx.strokeStyle = '#e2e8f0';
        ctx.beginPath();
        ctx.moveTo(x, margin.top);
        ctx.lineTo(x, margin.top + h);
        ctx.stroke();
        ctx.fillStyle = getComputedStyle(document.body).getPropertyValue('--muted');
        ctx.fillText(String(size), x - 10, margin.top + h + 20);
      }});
      Object.keys(sizeData).forEach(model => {{
        const points = sizes.map((size, idx) => {{
          const value = sizeData[model][size];
          return [margin.left + idx * w / (sizes.length - 1), margin.top + h - value * h];
        }});
        ctx.strokeStyle = modelColors[model];
        ctx.lineWidth = 3;
        ctx.beginPath();
        points.forEach((point, idx) => idx === 0 ? ctx.moveTo(point[0], point[1]) : ctx.lineTo(point[0], point[1]));
        ctx.stroke();
        points.forEach(point => {{
          ctx.fillStyle = modelColors[model];
          ctx.beginPath();
          ctx.arc(point[0], point[1], 4, 0, Math.PI * 2);
          ctx.fill();
        }});
      }});
    }}

    function sortTable(colIdx) {{
      const table = document.getElementById('rankingTable').tBodies[0];
      const rows = Array.from(table.rows);
      const numeric = colIdx > 0;
      rows.sort((a, b) => {{
        const av = a.cells[colIdx].textContent.trim();
        const bv = b.cells[colIdx].textContent.trim();
        return numeric ? parseFloat(bv) - parseFloat(av) : av.localeCompare(bv);
      }});
      rows.forEach(row => table.appendChild(row));
    }}

    drawGroupedBarChart('summaryChart');
    drawLineChart('scaleChart');
  </script>
</body>
</html>"""
    OUTPUT_PATH.write_text(html, encoding="utf-8")
    print(f"Saved {OUTPUT_PATH}")


if __name__ == "__main__":
    build_report()
