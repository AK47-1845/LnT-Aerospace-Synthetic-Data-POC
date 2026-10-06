from __future__ import annotations

import math
from typing import Sequence

from deliverable_utils import (
    GRAPH_SUBDIRS,
    MODEL_COLORS,
    MODEL_ORDER,
    SIZE_ORDER,
    correlation_matrix,
    discover_real_dataset,
    discover_synthetic_dataset,
    ensure_directories,
    export_svg_to_png,
    group_by,
    html_escape,
    load_dataset,
    load_metrics,
    mean,
    number,
    stddev,
)


WIDTH = 1200
HEIGHT = 700
MARGIN = {"left": 90, "right": 40, "top": 70, "bottom": 70}


def short_label(label: str) -> str:
    replacements = {
        "Physics Consistency": "Physics",
        "Statistical Similarity": "Statistical",
        "ML Utility (TSTR)": "ML Utility",
        "Privacy / Detection AUC": "Privacy",
        "Correlation Matrix Matching density": "Correlation",
        "Target — ": "",
        " (years)": "",
        " (sec)": "",
        " (m)": "",
        " (mm)": "",
        " (Pa)": "",
        " (MPa)": "",
        " (GPa)": "",
        " (Poisson)": "",
        " (°C)": "",
        " (kg/m³)": "",
    }
    for old, new in replacements.items():
        label = label.replace(old, new)
    return label


def svg_document(width: int, height: int, body: str) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}">'
        f'<rect width="100%" height="100%" fill="#ffffff"/>'
        f"{body}</svg>"
    )


def save_chart(subdir_key: str, filename: str, svg: str, width: int = WIDTH, height: int = HEIGHT) -> None:
    subdir = GRAPH_SUBDIRS[subdir_key]
    svg_path = subdir / f"{filename}.svg"
    png_path = subdir / f"{filename}.png"
    svg_path.write_text(svg, encoding="utf-8")
    export_svg_to_png(svg_path, png_path, width, height)


def chart_scaffold(title: str, width: int = WIDTH, height: int = HEIGHT):
    left = MARGIN["left"]
    top = MARGIN["top"]
    right = width - MARGIN["right"]
    bottom = height - MARGIN["bottom"]
    body = [
        f'<text x="{width/2}" y="34" text-anchor="middle" font-size="24" font-weight="700" '
        f'font-family="Segoe UI, Arial, sans-serif" fill="#0f172a">{html_escape(title)}</text>',
        f'<line x1="{left}" y1="{bottom}" x2="{right}" y2="{bottom}" stroke="#94a3b8" stroke-width="1"/>',
        f'<line x1="{left}" y1="{top}" x2="{left}" y2="{bottom}" stroke="#94a3b8" stroke-width="1"/>',
    ]
    return left, top, right, bottom, body


def color_mix(low: str, high: str, t: float) -> str:
    t = max(0.0, min(1.0, t))
    low_rgb = tuple(int(low[i : i + 2], 16) for i in (1, 3, 5))
    high_rgb = tuple(int(high[i : i + 2], 16) for i in (1, 3, 5))
    mixed = tuple(round(a + (b - a) * t) for a, b in zip(low_rgb, high_rgb))
    return "#" + "".join(f"{c:02x}" for c in mixed)


def add_y_grid(body: list[str], left: int, top: int, right: int, bottom: int, ticks: int = 5) -> None:
    for idx in range(ticks + 1):
        y = bottom - (bottom - top) * idx / ticks
        value = idx / ticks
        body.append(f'<line x1="{left}" y1="{y}" x2="{right}" y2="{y}" stroke="#e2e8f0" stroke-width="1"/>')
        body.append(
            f'<text x="{left-14}" y="{y+4}" text-anchor="end" font-size="12" fill="#475569" '
            f'font-family="Segoe UI, Arial, sans-serif">{value:.1f}</text>'
        )


def model_means(rows: list[dict]) -> list[dict]:
    grouped = group_by(rows, "Model")
    items = []
    for model in MODEL_ORDER:
        model_rows = grouped[model]
        items.append(
            {
                "Model": model,
                "Physics Consistency": mean(row["Physics Consistency"] for row in model_rows),
                "Statistical Similarity": mean(row["Statistical Similarity"] for row in model_rows),
                "ML Utility (TSTR)": mean(row["ML Utility (TSTR)"] for row in model_rows),
                "Privacy / Detection AUC": mean(row["Privacy / Detection AUC"] for row in model_rows),
                "Composite Score": mean(row["Composite Score"] for row in model_rows),
            }
        )
    return items


def grouped_horizontal_bars(model_means_rows: list[dict]) -> str:
    metrics = [
        "Physics Consistency",
        "Statistical Similarity",
        "ML Utility (TSTR)",
        "Privacy / Detection AUC",
    ]
    width = 1200
    height = 760
    left, top, right, bottom, body = chart_scaffold("Model Performance Across All Evaluation Pillars", width, height)
    add_y_grid(body, left, top, right, bottom)
    row_h = (bottom - top) / len(MODEL_ORDER)
    group_h = row_h * 0.72
    bar_h = group_h / len(metrics)
    for idx, model in enumerate(MODEL_ORDER):
        row = next(item for item in model_means_rows if item["Model"] == model)
        y0 = top + idx * row_h + (row_h - group_h) / 2
        body.append(
            f'<text x="{left-14}" y="{y0 + group_h/2 + 4}" text-anchor="end" font-size="13" '
            f'fill="#0f172a" font-family="Segoe UI, Arial, sans-serif">{model}</text>'
        )
        for metric_idx, metric in enumerate(metrics):
            value = row[metric]
            x = left
            y = y0 + metric_idx * bar_h
            bar_w = (right - left) * value
            color = color_mix("#cbd5e1", MODEL_COLORS[model], 0.75 - metric_idx * 0.12)
            body.append(
                f'<rect x="{x}" y="{y}" width="{bar_w}" height="{bar_h-3}" rx="3" fill="{color}" opacity="0.95"/>'
            )
            body.append(
                f'<text x="{x + bar_w + 8}" y="{y + bar_h/2 + 4}" font-size="11" fill="#334155" '
                f'font-family="Segoe UI, Arial, sans-serif">{short_label(metric)} {number(value,3)}</text>'
            )
    body.append(
        f'<text x="{(left+right)/2}" y="{height-18}" text-anchor="middle" font-size="14" fill="#334155" '
        f'font-family="Segoe UI, Arial, sans-serif">Mean pillar score</text>'
    )
    return svg_document(width, height, "".join(body))


def composite_ranking_chart(runs: list[dict]) -> str:
    means = []
    for model, model_rows in group_by(runs, "Model").items():
        values = [row["Composite Score"] for row in model_rows]
        means.append({"Model": model, "mean": mean(values), "std": stddev(values)})
    means.sort(key=lambda item: item["mean"], reverse=True)
    left, top, right, bottom, body = chart_scaffold("Composite Score Ranking With Run-to-Run Variability")
    add_y_grid(body, left, top, right, bottom)
    slot = (right - left) / len(means)
    bar_w = slot * 0.54
    for idx, item in enumerate(means):
        x = left + idx * slot + (slot - bar_w) / 2
        bar_h = (bottom - top) * item["mean"]
        y = bottom - bar_h
        cx = x + bar_w / 2
        err = (bottom - top) * item["std"]
        body.append(f'<rect x="{x}" y="{y}" width="{bar_w}" height="{bar_h}" rx="5" fill="{MODEL_COLORS[item["Model"]]}"/>')
        body.append(f'<line x1="{cx}" y1="{y-err}" x2="{cx}" y2="{y+err}" stroke="#0f172a" stroke-width="2"/>')
        body.append(f'<line x1="{cx-7}" y1="{y-err}" x2="{cx+7}" y2="{y-err}" stroke="#0f172a" stroke-width="2"/>')
        body.append(f'<line x1="{cx-7}" y1="{y+err}" x2="{cx+7}" y2="{y+err}" stroke="#0f172a" stroke-width="2"/>')
        body.append(
            f'<text x="{cx}" y="{y-10}" text-anchor="middle" font-size="12" fill="#0f172a" '
            f'font-family="Segoe UI, Arial, sans-serif">{number(item["mean"])}</text>'
        )
        body.append(
            f'<text x="{cx}" y="{bottom+24}" text-anchor="middle" font-size="12" fill="#334155" '
            f'font-family="Segoe UI, Arial, sans-serif">{item["Model"]}</text>'
        )
    return svg_document(WIDTH, HEIGHT, "".join(body))


def radar_chart(model_means_rows: list[dict]) -> str:
    axes = ["Physics Consistency", "Statistical Similarity", "ML Utility (TSTR)", "Privacy / Detection AUC"]
    width, height = 1000, 820
    cx, cy, radius = width / 2, height / 2 + 20, 270
    body = [
        f'<text x="{width/2}" y="34" text-anchor="middle" font-size="24" font-weight="700" '
        f'font-family="Segoe UI, Arial, sans-serif" fill="#0f172a">Model Radar Comparison</text>'
    ]
    for ring in range(1, 6):
        ring_r = radius * ring / 5
        points = []
        for idx in range(len(axes)):
            angle = -math.pi / 2 + idx * 2 * math.pi / len(axes)
            points.append(f"{cx + ring_r * math.cos(angle)},{cy + ring_r * math.sin(angle)}")
        body.append(f'<polygon points="{" ".join(points)}" fill="none" stroke="#e2e8f0" stroke-width="1"/>')
    for idx, axis in enumerate(axes):
        angle = -math.pi / 2 + idx * 2 * math.pi / len(axes)
        x = cx + radius * math.cos(angle)
        y = cy + radius * math.sin(angle)
        lx = cx + (radius + 32) * math.cos(angle)
        ly = cy + (radius + 32) * math.sin(angle)
        body.append(f'<line x1="{cx}" y1="{cy}" x2="{x}" y2="{y}" stroke="#94a3b8" stroke-width="1"/>')
        body.append(
            f'<text x="{lx}" y="{ly}" text-anchor="middle" font-size="13" fill="#334155" '
            f'font-family="Segoe UI, Arial, sans-serif">{html_escape(short_label(axis))}</text>'
        )
    for row in model_means_rows:
        points = []
        for idx, axis in enumerate(axes):
            value = row[axis]
            angle = -math.pi / 2 + idx * 2 * math.pi / len(axes)
            points.append(f"{cx + radius * value * math.cos(angle)},{cy + radius * value * math.sin(angle)}")
        color = MODEL_COLORS[row["Model"]]
        body.append(f'<polygon points="{" ".join(points)}" fill="{color}" fill-opacity="0.12" stroke="{color}" stroke-width="3"/>')
    legend_y = height - 42
    legend_x = 110
    for model in MODEL_ORDER:
        body.append(f'<rect x="{legend_x}" y="{legend_y-12}" width="16" height="16" rx="3" fill="{MODEL_COLORS[model]}"/>')
        body.append(
            f'<text x="{legend_x+24}" y="{legend_y}" font-size="13" fill="#334155" '
            f'font-family="Segoe UI, Arial, sans-serif">{model}</text>'
        )
        legend_x += 135
    return svg_document(width, height, "".join(body))


def metrics_heatmap(model_means_rows: list[dict]) -> str:
    metrics = [
        "Physics Consistency",
        "Statistical Similarity",
        "ML Utility (TSTR)",
        "Privacy / Detection AUC",
        "Composite Score",
    ]
    width, height = 1000, 640
    left, top, right, bottom, body = chart_scaffold("Mean Metrics Heatmap By Model", width, height)
    cell_w = (right - left) / len(metrics)
    cell_h = (bottom - top) / len(MODEL_ORDER)
    values = [row[metric] for row in model_means_rows for metric in metrics]
    vmin, vmax = min(values), max(values)
    for c_idx, metric in enumerate(metrics):
        body.append(
            f'<text x="{left + c_idx*cell_w + cell_w/2}" y="{top-16}" text-anchor="middle" font-size="12" '
            f'fill="#334155" font-family="Segoe UI, Arial, sans-serif">{html_escape(short_label(metric))}</text>'
        )
    for r_idx, row in enumerate(model_means_rows):
        body.append(
            f'<text x="{left-14}" y="{top + r_idx*cell_h + cell_h/2 + 4}" text-anchor="end" font-size="13" '
            f'fill="#0f172a" font-family="Segoe UI, Arial, sans-serif">{row["Model"]}</text>'
        )
        for c_idx, metric in enumerate(metrics):
            value = row[metric]
            t = 0.0 if vmax == vmin else (value - vmin) / (vmax - vmin)
            color = color_mix("#ffffff", "#166534", t)
            text_fill = "#ffffff" if t > 0.55 else "#0f172a"
            x = left + c_idx * cell_w
            y = top + r_idx * cell_h
            body.append(f'<rect x="{x}" y="{y}" width="{cell_w}" height="{cell_h}" fill="{color}" stroke="#e2e8f0"/>')
            body.append(
                f'<text x="{x + cell_w/2}" y="{y + cell_h/2 + 4}" text-anchor="middle" font-size="12" '
                f'fill="{text_fill}" font-family="Segoe UI, Arial, sans-serif">{number(value,3)}</text>'
            )
    return svg_document(width, height, "".join(body))


def line_chart_by_size(rows: list[dict], metric: str, title: str, y_label: str) -> str:
    left, top, right, bottom, body = chart_scaffold(title)
    add_y_grid(body, left, top, right, bottom)
    step_x = (right - left) / (len(SIZE_ORDER) - 1)
    grouped_model = group_by(rows, "Model")
    for idx, size in enumerate(SIZE_ORDER):
        x = left + idx * step_x
        body.append(f'<line x1="{x}" y1="{top}" x2="{x}" y2="{bottom}" stroke="#f1f5f9" stroke-width="1"/>')
        body.append(
            f'<text x="{x}" y="{bottom+24}" text-anchor="middle" font-size="12" fill="#475569" '
            f'font-family="Segoe UI, Arial, sans-serif">{size}</text>'
        )
    for model in MODEL_ORDER:
        model_rows = grouped_model[model]
        points = []
        for idx, size in enumerate(SIZE_ORDER):
            value = mean(row[metric] for row in model_rows if row["Size"] == size)
            x = left + idx * step_x
            y = bottom - (bottom - top) * value
            points.append((x, y, value))
        body.append(
            f'<polyline points="{" ".join(f"{x},{y}" for x, y, _ in points)}" fill="none" '
            f'stroke="{MODEL_COLORS[model]}" stroke-width="3"/>'
        )
        for x, y, _ in points:
            body.append(f'<circle cx="{x}" cy="{y}" r="5" fill="{MODEL_COLORS[model]}"/>')
        last_x, last_y, last_value = points[-1]
        body.append(
            f'<text x="{last_x+8}" y="{last_y-8}" font-size="11" fill="{MODEL_COLORS[model]}" '
            f'font-family="Segoe UI, Arial, sans-serif">{model} {number(last_value,3)}</text>'
        )
    body.append(
        f'<text x="{(left+right)/2}" y="{HEIGHT-16}" text-anchor="middle" font-size="14" fill="#334155" '
        f'font-family="Segoe UI, Arial, sans-serif">Generation size</text>'
    )
    body.append(
        f'<text transform="translate(26,{(top+bottom)/2}) rotate(-90)" text-anchor="middle" font-size="14" '
        f'fill="#334155" font-family="Segoe UI, Arial, sans-serif">{html_escape(y_label)}</text>'
    )
    return svg_document(WIDTH, HEIGHT, "".join(body))


def box_plot(rows: list[dict]) -> str:
    left, top, right, bottom, body = chart_scaffold("Composite Score Distribution Across Seeds")
    add_y_grid(body, left, top, right, bottom)
    grouped = group_by(rows, "Model")
    slot = (right - left) / len(MODEL_ORDER)
    for idx, model in enumerate(MODEL_ORDER):
        values = sorted(row["Composite Score"] for row in grouped[model])
        q1 = values[len(values) // 4]
        med = values[len(values) // 2]
        q3 = values[(len(values) * 3) // 4]
        lo, hi = min(values), max(values)
        cx = left + idx * slot + slot / 2
        box_w = slot * 0.4
        y_q1 = bottom - (bottom - top) * q1
        y_q3 = bottom - (bottom - top) * q3
        y_med = bottom - (bottom - top) * med
        y_lo = bottom - (bottom - top) * lo
        y_hi = bottom - (bottom - top) * hi
        body.append(f'<line x1="{cx}" y1="{y_lo}" x2="{cx}" y2="{y_hi}" stroke="#334155" stroke-width="2"/>')
        body.append(
            f'<rect x="{cx-box_w/2}" y="{y_q3}" width="{box_w}" height="{y_q1-y_q3}" fill="{MODEL_COLORS[model]}" '
            f'fill-opacity="0.25" stroke="{MODEL_COLORS[model]}" stroke-width="2"/>'
        )
        body.append(f'<line x1="{cx-box_w/2}" y1="{y_med}" x2="{cx+box_w/2}" y2="{y_med}" stroke="#0f172a" stroke-width="2"/>')
        body.append(
            f'<text x="{cx}" y="{bottom+24}" text-anchor="middle" font-size="12" fill="#334155" '
            f'font-family="Segoe UI, Arial, sans-serif">{model}</text>'
        )
    return svg_document(WIDTH, HEIGHT, "".join(body))


def scatter_plot(rows: list[dict], x_metric: str, y_metric: str, title: str) -> str:
    left, top, right, bottom, body = chart_scaffold(title)
    add_y_grid(body, left, top, right, bottom)
    for idx in range(6):
        x = left + (right - left) * idx / 5
        body.append(f'<line x1="{x}" y1="{top}" x2="{x}" y2="{bottom}" stroke="#f1f5f9" stroke-width="1"/>')
        body.append(
            f'<text x="{x}" y="{bottom+24}" text-anchor="middle" font-size="12" fill="#475569" '
            f'font-family="Segoe UI, Arial, sans-serif">{idx/5:.1f}</text>'
        )
    for row in rows:
        x = left + (right - left) * row[x_metric]
        y = bottom - (bottom - top) * row[y_metric]
        radius = 4 + row["Size"] / 1200
        body.append(
            f'<circle cx="{x}" cy="{y}" r="{radius}" fill="{MODEL_COLORS[row["Model"]]}" fill-opacity="0.72" '
            f'stroke="#ffffff" stroke-width="1"/>'
        )
    legend_x = right - 130
    legend_y = top + 10
    for model in MODEL_ORDER:
        body.append(f'<circle cx="{legend_x}" cy="{legend_y}" r="6" fill="{MODEL_COLORS[model]}"/>')
        body.append(
            f'<text x="{legend_x+14}" y="{legend_y+4}" font-size="12" fill="#334155" '
            f'font-family="Segoe UI, Arial, sans-serif">{model}</text>'
        )
        legend_y += 22
    return svg_document(WIDTH, HEIGHT, "".join(body))


def density_curve(values: Sequence[float], lower: float, upper: float, samples: int = 80) -> tuple[list[float], list[float]]:
    if not values:
        return [0.0], [0.0]
    spread = max(0.02, stddev(values) or 0.05)
    ys = [lower + (upper - lower) * idx / (samples - 1) for idx in range(samples)]
    xs = []
    coeff = 1 / (spread * math.sqrt(2 * math.pi))
    for y in ys:
        density = 0.0
        for value in values:
            z = (y - value) / spread
            density += coeff * math.exp(-0.5 * z * z)
        xs.append(density / len(values))
    return xs, ys


def violin_plot(rows: list[dict]) -> str:
    left, top, right, bottom, body = chart_scaffold("KS p-value Distribution By Model")
    add_y_grid(body, left, top, right, bottom)
    grouped = group_by(rows, "Model")
    slot = (right - left) / len(MODEL_ORDER)
    for idx, model in enumerate(MODEL_ORDER):
        values = [row["KS p-value (mean)"] for row in grouped[model]]
        xs, ys = density_curve(values, 0.0, 1.0, samples=50)
        scale = slot * 0.7 / max(xs or [1.0])
        cx = left + idx * slot + slot / 2
        points_left = []
        points_right = []
        for density, value in zip(xs, ys):
            y = bottom - (bottom - top) * value
            points_left.append(f"{cx - density * scale},{y}")
            points_right.append(f"{cx + density * scale},{y}")
        points = points_left + list(reversed(points_right))
        body.append(
            f'<polygon points="{" ".join(points)}" fill="{MODEL_COLORS[model]}" fill-opacity="0.28" '
            f'stroke="{MODEL_COLORS[model]}" stroke-width="2"/>'
        )
        body.append(
            f'<text x="{cx}" y="{bottom+24}" text-anchor="middle" font-size="12" fill="#334155" '
            f'font-family="Segoe UI, Arial, sans-serif">{model}</text>'
        )
    return svg_document(WIDTH, HEIGHT, "".join(body))


def kl_bar_chart(rows: list[dict]) -> str:
    grouped = group_by(rows, "Model")
    means = [{"Model": model, "value": mean(r["KL divergence"] for r in grouped[model])} for model in MODEL_ORDER]
    max_value = max(item["value"] for item in means) or 1.0
    left, top, right, bottom, body = chart_scaffold("Mean KL Divergence By Model (Lower Is Better)")
    slot = (right - left) / len(means)
    for idx, item in enumerate(means):
        bar_w = slot * 0.56
        x = left + idx * slot + (slot - bar_w) / 2
        height_ratio = item["value"] / max_value
        bar_h = (bottom - top) * height_ratio
        y = bottom - bar_h
        color = color_mix("#16a34a", "#dc2626", height_ratio)
        body.append(f'<rect x="{x}" y="{y}" width="{bar_w}" height="{bar_h}" rx="4" fill="{color}"/>')
        body.append(
            f'<text x="{x+bar_w/2}" y="{y-8}" text-anchor="middle" font-size="12" fill="#334155" '
            f'font-family="Segoe UI, Arial, sans-serif">{item["value"]:.4f}</text>'
        )
        body.append(
            f'<text x="{x+bar_w/2}" y="{bottom+24}" text-anchor="middle" font-size="12" fill="#334155" '
            f'font-family="Segoe UI, Arial, sans-serif">{item["Model"]}</text>'
        )
    return svg_document(WIDTH, HEIGHT, "".join(body))


def kde_overlay_chart(real_rows: list[dict], synthetic_rows: list[dict], title: str, model: str) -> str:
    features = ["E (GPa)", "Tensile Strength (MPa)", "ρ (kg/m³)", "Altitude (m)"]
    width, height = 1200, 900
    plot_w, plot_h = 470, 300
    gap_x, gap_y = 80, 90
    start_x, start_y = 90, 90
    body = [
        f'<text x="{width/2}" y="34" text-anchor="middle" font-size="24" font-weight="700" '
        f'font-family="Segoe UI, Arial, sans-serif" fill="#0f172a">{html_escape(title)}</text>'
    ]
    for idx, feature in enumerate(features):
        col = idx % 2
        row = idx // 2
        x0 = start_x + col * (plot_w + gap_x)
        y0 = start_y + row * (plot_h + gap_y)
        x1 = x0 + plot_w
        y1 = y0 + plot_h
        body.append(f'<rect x="{x0}" y="{y0}" width="{plot_w}" height="{plot_h}" fill="none" stroke="#cbd5e1"/>')
        body.append(
            f'<text x="{x0 + plot_w/2}" y="{y0-12}" text-anchor="middle" font-size="14" fill="#334155" '
            f'font-family="Segoe UI, Arial, sans-serif">{html_escape(short_label(feature))}</text>'
        )
        real_values = [float(item[feature]) for item in real_rows]
        synthetic_values = [float(item[feature]) for item in synthetic_rows]
        lower = min(real_values + synthetic_values)
        upper = max(real_values + synthetic_values)
        real_density_x, sample_values = density_curve(real_values, lower, upper, samples=80)
        synth_density_x, _ = density_curve(synthetic_values, lower, upper, samples=80)
        max_density = max(max(real_density_x), max(synth_density_x), 1e-9)
        real_points = []
        synth_points = []
        for density, value in zip(real_density_x, sample_values):
            px = x0 + (plot_w - 10) * (value - lower) / (upper - lower + 1e-9) + 5
            py = y1 - (plot_h - 20) * density / max_density - 10
            real_points.append(f"{px},{py}")
        for density, value in zip(synth_density_x, sample_values):
            px = x0 + (plot_w - 10) * (value - lower) / (upper - lower + 1e-9) + 5
            py = y1 - (plot_h - 20) * density / max_density - 10
            synth_points.append(f"{px},{py}")
        body.append(
            f'<polyline points="{" ".join(real_points)}" fill="none" stroke="#111827" stroke-width="3" '
            f'stroke-dasharray="7 6"/>'
        )
        body.append(
            f'<polyline points="{" ".join(synth_points)}" fill="none" stroke="{MODEL_COLORS[model]}" stroke-width="3"/>'
        )
    body.append(f'<line x1="420" y1="{height-36}" x2="470" y2="{height-36}" stroke="#111827" stroke-width="3" stroke-dasharray="7 6"/>')
    body.append(f'<text x="478" y="{height-31}" font-size="13" fill="#334155" font-family="Segoe UI, Arial, sans-serif">Real data</text>')
    body.append(f'<line x1="630" y1="{height-36}" x2="680" y2="{height-36}" stroke="{MODEL_COLORS[model]}" stroke-width="3"/>')
    body.append(f'<text x="688" y="{height-31}" font-size="13" fill="#334155" font-family="Segoe UI, Arial, sans-serif">Synthetic data</text>')
    return svg_document(width, height, "".join(body))


def correlation_comparison(real_rows: list[dict], synthetic_rows: list[dict]) -> str:
    labels, real_corr = correlation_matrix(real_rows)
    _, synth_corr = correlation_matrix(synthetic_rows)
    width, height = 1500, 820
    body = [
        f'<text x="{width/2}" y="34" text-anchor="middle" font-size="24" font-weight="700" '
        f'font-family="Segoe UI, Arial, sans-serif" fill="#0f172a">Correlation Matrix Comparison</text>'
    ]
    for panel_idx, (title, matrix) in enumerate((("Real dataset", real_corr), ("Best synthetic dataset", synth_corr))):
        x0 = 80 + panel_idx * 700
        y0 = 90
        cell = 36
        body.append(
            f'<text x="{x0 + len(labels)*cell/2}" y="72" text-anchor="middle" font-size="16" fill="#334155" '
            f'font-family="Segoe UI, Arial, sans-serif">{title}</text>'
        )
        for idx, label in enumerate(labels):
            lab = short_label(label)[:10]
            body.append(
                f'<text x="{x0 + idx*cell + cell/2}" y="{y0-10}" text-anchor="middle" font-size="9" fill="#475569" '
                f'font-family="Segoe UI, Arial, sans-serif">{html_escape(lab)}</text>'
            )
            body.append(
                f'<text x="{x0-8}" y="{y0 + idx*cell + cell/2 + 3}" text-anchor="end" font-size="9" fill="#475569" '
                f'font-family="Segoe UI, Arial, sans-serif">{html_escape(lab)}</text>'
            )
        for r_idx, row in enumerate(matrix):
            for c_idx, value in enumerate(row):
                color = color_mix("#b91c1c", "#16a34a", (value + 1) / 2)
                body.append(
                    f'<rect x="{x0 + c_idx*cell}" y="{y0 + r_idx*cell}" width="{cell}" height="{cell}" '
                    f'fill="{color}" stroke="#ffffff" stroke-width="1"/>'
                )
    return svg_document(width, height, "".join(body))


def leaderboard_chart(rows: list[dict]) -> str:
    top10 = sorted(rows, key=lambda row: row["Composite Score"], reverse=True)[:10]
    left, top, right, bottom, body = chart_scaffold("Top 10 Run Leaderboard")
    add_y_grid(body, left, top, right, bottom)
    slot = (right - left) / len(top10)
    for idx, row in enumerate(top10):
        bar_w = slot * 0.6
        x = left + idx * slot + (slot - bar_w) / 2
        bar_h = (bottom - top) * row["Composite Score"]
        y = bottom - bar_h
        fill = "#d4af37" if idx == 0 else MODEL_COLORS[row["Model"]]
        body.append(f'<rect x="{x}" y="{y}" width="{bar_w}" height="{bar_h}" rx="4" fill="{fill}"/>')
        body.append(
            f'<text x="{x+bar_w/2}" y="{y-8}" text-anchor="middle" font-size="11" fill="#0f172a" '
            f'font-family="Segoe UI, Arial, sans-serif">{number(row["Composite Score"])}</text>'
        )
        body.append(
            f'<text x="{x+bar_w/2}" y="{bottom+18}" text-anchor="middle" font-size="9" fill="#334155" '
            f'font-family="Segoe UI, Arial, sans-serif">#{idx+1}</text>'
        )
        body.append(
            f'<text x="{x+bar_w/2}" y="{bottom+34}" text-anchor="middle" font-size="9" fill="#334155" '
            f'font-family="Segoe UI, Arial, sans-serif">{html_escape(row["Model"])}</text>'
        )
    return svg_document(WIDTH, HEIGHT, "".join(body))


def improvement_chart(rows: list[dict]) -> str:
    left, top, right, bottom, body = chart_scaffold("Improvement By Scale (300 to 5000 Rows)")
    add_y_grid(body, left, top, right, bottom)
    slot = (right - left) / len(MODEL_ORDER)
    grouped = group_by(rows, "Model")
    for idx, model in enumerate(MODEL_ORDER):
        base = mean(row["Composite Score"] for row in grouped[model] if row["Size"] == 300)
        final = mean(row["Composite Score"] for row in grouped[model] if row["Size"] == 5000)
        gain = final - base
        bar_w = slot * 0.58
        x = left + idx * slot + (slot - bar_w) / 2
        bar_h = (bottom - top) * gain / 0.2
        y = bottom - bar_h
        body.append(f'<rect x="{x}" y="{y}" width="{bar_w}" height="{bar_h}" rx="4" fill="{MODEL_COLORS[model]}"/>')
        body.append(
            f'<text x="{x+bar_w/2}" y="{y-8}" text-anchor="middle" font-size="12" fill="#334155" '
            f'font-family="Segoe UI, Arial, sans-serif">{gain:.3f}</text>'
        )
        body.append(
            f'<text x="{x+bar_w/2}" y="{bottom+24}" text-anchor="middle" font-size="12" fill="#334155" '
            f'font-family="Segoe UI, Arial, sans-serif">{model}</text>'
        )
    return svg_document(WIDTH, HEIGHT, "".join(body))


def repair_bar(rows: list[dict]) -> str:
    grouped = group_by(rows, "Model")
    totals = [{"Model": model, "total": sum(row["Repair protocol trigger count"] for row in grouped[model])} for model in MODEL_ORDER]
    max_total = max(item["total"] for item in totals) or 1
    left, top, right, bottom, body = chart_scaffold("Repair Protocol Activity By Model")
    slot = (right - left) / len(totals)
    for idx, item in enumerate(totals):
        bar_w = slot * 0.56
        x = left + idx * slot + (slot - bar_w) / 2
        bar_h = (bottom - top) * item["total"] / max_total
        y = bottom - bar_h
        body.append(f'<rect x="{x}" y="{y}" width="{bar_w}" height="{bar_h}" rx="4" fill="{MODEL_COLORS[item["Model"]]}"/>')
        body.append(
            f'<text x="{x+bar_w/2}" y="{y-8}" text-anchor="middle" font-size="12" fill="#334155" '
            f'font-family="Segoe UI, Arial, sans-serif">{item["total"]}</text>'
        )
        body.append(
            f'<text x="{x+bar_w/2}" y="{bottom+24}" text-anchor="middle" font-size="12" fill="#334155" '
            f'font-family="Segoe UI, Arial, sans-serif">{item["Model"]}</text>'
        )
    return svg_document(WIDTH, HEIGHT, "".join(body))


def build_all_graphs() -> None:
    ensure_directories()
    rows = load_metrics()
    means_rows = model_means(rows)

    save_chart("A", "composite_vs_models", grouped_horizontal_bars(means_rows), 1200, 760)
    save_chart("A", "composite_score_ranking", composite_ranking_chart(rows))
    save_chart("A", "radar_model_comparison", radar_chart(means_rows), 1000, 820)
    save_chart("A", "metrics_heatmap_models", metrics_heatmap(means_rows), 1000, 640)

    save_chart("B", "composite_vs_size", line_chart_by_size(rows, "Composite Score", "Composite Score vs Generation Size", "Composite score"))
    save_chart("B", "tstr_vs_size", line_chart_by_size(rows, "ML Utility (TSTR)", "ML Utility (TSTR) vs Generation Size", "TSTR accuracy"))
    save_chart("B", "seed_variance_boxplot", box_plot(rows))
    save_chart(
        "B",
        "physics_vs_statistical_scatter",
        scatter_plot(rows, "Physics Consistency", "Statistical Similarity", "Physics Consistency vs Statistical Similarity"),
    )

    save_chart("C", "ks_pvalue_violin", violin_plot(rows))
    save_chart("C", "kl_divergence_bars", kl_bar_chart(rows))

    real_rows = load_dataset(discover_real_dataset())
    kde_specs = [
        ("Empirical", 11, 5000, "kde_overlay_empirical_s11_n5000"),
        ("KDE", 11, 5000, "kde_overlay_kde_s11_n5000"),
        ("GMM", 11, 5000, "kde_overlay_gmm_s11_n5000"),
        ("MaskedPredictor", 11, 5000, "kde_overlay_masked_s11_n5000"),
    ]
    for model, seed, size, filename in kde_specs:
        synthetic_path = discover_synthetic_dataset(model, seed, size)
        if synthetic_path is None:
            raise FileNotFoundError(f"Missing synthetic dataset for {model} seed={seed} size={size}")
        synthetic_rows = load_dataset(synthetic_path)
        svg = kde_overlay_chart(real_rows, synthetic_rows, f"KDE Overlay: {model} | seed={seed} | n={size}", model)
        save_chart("C", filename, svg, 1200, 900)

    best_path = discover_synthetic_dataset("Empirical", 11, 5000)
    if best_path is None:
        raise FileNotFoundError("Missing best synthetic dataset source for correlation comparison.")
    best_rows = load_dataset(best_path)
    save_chart("C", "correlation_matrix_comparison", correlation_comparison(real_rows, best_rows), 1500, 820)

    save_chart("D", "tstr_by_size_grouped", line_chart_by_size(rows, "ML Utility (TSTR)", "TSTR Accuracy By Model and Size", "TSTR accuracy"))
    save_chart(
        "D",
        "privacy_utility_tradeoff",
        scatter_plot(rows, "ML Utility (TSTR)", "Privacy / Detection AUC", "Privacy vs Utility Tradeoff"),
    )
    save_chart("D", "top10_leaderboard", leaderboard_chart(rows))
    save_chart("D", "improvement_by_scale", improvement_chart(rows))
    save_chart("D", "repair_triggers_bar", repair_bar(rows))

    print("Graph generation complete.")


if __name__ == "__main__":
    build_all_graphs()
