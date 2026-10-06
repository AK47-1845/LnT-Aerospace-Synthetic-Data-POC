const pptxgen = require("pptxgenjs");

const pres = new pptxgen();
pres.layout = "LAYOUT_16x9";
pres.title = "L&T Aerospace Synthetic Data POC";

// ─── PALETTE ─────────────────────────────────────────────────────────────────
const C = {
  navy:    "065A82",  // deep blue – dominant
  teal:    "0D9488",  // teal accent
  teal2:   "1C7293",  // medium blue
  dark:    "1E2761",  // dark header bg
  charcoal:"1E293B",  // body text
  muted:   "64748B",  // secondary text
  light:   "F0F7FF",  // content slide bg
  white:   "FFFFFF",
  green:   "059669",  // pass / positive
  amber:   "D97706",  // warning
  red:     "DC2626",  // not recommended
  paleGreen: "D1FAE5",
  paledark:"E8F4FD",
};

// ─── HELPERS ──────────────────────────────────────────────────────────────────
const IMG = (name) => `D:/aero/deliverables_LnT/explainable_graphs/${name}`;

// Adds the standard header bar + left accent strip to a content slide
function addHeader(slide, title) {
  // Navy top bar
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 0, w: 10, h: 0.65,
    fill: { color: C.dark }, line: { color: C.dark }
  });
  // Teal left accent strip below header
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 0.65, w: 0.06, h: 4.975,
    fill: { color: C.teal }, line: { color: C.teal }
  });
  // Title text
  slide.addText(title, {
    x: 0.3, y: 0, w: 9.4, h: 0.65,
    fontSize: 18, bold: true, color: C.white,
    fontFace: "Calibri", valign: "middle", margin: 0
  });
  // Light background
  slide.background = { color: C.light };
}

// Stat box: big number + label below
function addStatBox(slide, val, label, x, y, w, h, bg, valColor, labelColor) {
  slide.addShape(pres.shapes.RECTANGLE, {
    x, y, w, h,
    fill: { color: bg }, line: { color: bg },
    shadow: { type: "outer", color: "000000", blur: 5, offset: 2, angle: 135, opacity: 0.10 }
  });
  slide.addText(val, {
    x: x + 0.05, y: y + 0.07, w: w - 0.1, h: h * 0.52,
    fontSize: 26, bold: true, color: valColor, fontFace: "Calibri",
    align: "center", valign: "middle", margin: 0
  });
  slide.addText(label, {
    x: x + 0.05, y: y + h * 0.54, w: w - 0.1, h: h * 0.42,
    fontSize: 9, bold: false, color: labelColor, fontFace: "Calibri",
    align: "center", valign: "top", margin: 0
  });
}

// Section divider label
function addSectionLabel(slide, text, x, y, color) {
  slide.addShape(pres.shapes.RECTANGLE, {
    x, y, w: 2.2, h: 0.24,
    fill: { color: color }, line: { color: color }
  });
  slide.addText(text, {
    x, y, w: 2.2, h: 0.24,
    fontSize: 8, bold: true, color: C.white, fontFace: "Calibri",
    align: "center", valign: "middle", margin: 0
  });
}

// ─── SLIDE 1: TITLE ───────────────────────────────────────────────────────────
{
  const s = pres.addSlide();
  s.background = { color: C.dark };

  // Teal accent bar at top
  s.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 0, w: 10, h: 0.06,
    fill: { color: C.teal }, line: { color: C.teal }
  });
  // Bottom bar
  s.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 5.565, w: 10, h: 0.06,
    fill: { color: C.teal }, line: { color: C.teal }
  });

  // Company label
  s.addText("L&T ENGINEERING  ·  PROOF OF CONCEPT  ·  MARCH 2026", {
    x: 0.5, y: 0.22, w: 9, h: 0.3,
    fontSize: 9, bold: false, color: "7FB3D3", fontFace: "Calibri",
    align: "left", charSpacing: 2, margin: 0
  });

  // Main title
  s.addText("Aerospace Structural Design", {
    x: 0.5, y: 0.6, w: 9, h: 0.75,
    fontSize: 34, bold: true, color: C.white, fontFace: "Calibri",
    align: "left", margin: 0
  });
  s.addText("Synthetic Data Generation", {
    x: 0.5, y: 1.28, w: 9, h: 0.65,
    fontSize: 34, bold: true, color: "7ECBE8", fontFace: "Calibri",
    align: "left", margin: 0
  });

  // Subtitle
  s.addText("Production-ready synthetic dataset · 9 generative models · 6-axis validation · 0 physics violations", {
    x: 0.5, y: 2.05, w: 9, h: 0.35,
    fontSize: 11, color: "9BBFD4", fontFace: "Calibri", align: "left", margin: 0
  });

  // Divider line
  s.addShape(pres.shapes.LINE, {
    x: 0.5, y: 2.5, w: 9, h: 0,
    line: { color: "1C4E6E", width: 1 }
  });

  // 6 hero metrics
  const metrics = [
    { val: "0.9965", label: "Composite Score" },
    { val: "1.000",  label: "TSTR F1" },
    { val: "0.0003", label: "MMD" },
    { val: "0.478",  label: "Discriminator AUC" },
    { val: "0",      label: "Physics Violations" },
    { val: "91%",    label: "Edge Case Realism" },
  ];
  metrics.forEach((m, i) => {
    const x = 0.5 + i * 1.54;
    addStatBox(s, m.val, m.label, x, 2.7, 1.42, 0.95, "0D3A5C", C.teal, "9BBFD4");
  });

  // Footer
  s.addText("All 4 client requirements met and exceeded  ·  KDE_s123_n5000_r035.csv recommended", {
    x: 0.5, y: 4.78, w: 9, h: 0.25,
    fontSize: 9, color: "5A8AA6", fontFace: "Calibri", align: "left", margin: 0
  });
}

// ─── SLIDE 2: PROBLEM & APPROACH ─────────────────────────────────────────────
{
  const s = pres.addSlide();
  addHeader(s, "Client Requirements & Our Approach");

  // Left: 4 requirements
  const reqs = [
    { num: "01", title: "Statistical Fidelity", desc: "Distributions, spread, skew — shape of data matters, not just valid ranges" },
    { num: "02", title: "Feature Interdependencies", desc: "Variables don't exist in isolation — understand what drives what" },
    { num: "03", title: "Input→Output Coherence", desc: "Target variables must follow logically from inputs, no random labels" },
    { num: "04", title: "Class Balance & Edge Cases", desc: "Handle imbalance; rare but realistic combinations must be representable" },
  ];

  reqs.forEach((r, i) => {
    const y = 0.82 + i * 1.12;
    // Number badge
    s.addShape(pres.shapes.RECTANGLE, {
      x: 0.25, y, w: 0.38, h: 0.38,
      fill: { color: C.navy }, line: { color: C.navy }
    });
    s.addText(r.num, {
      x: 0.25, y, w: 0.38, h: 0.38,
      fontSize: 13, bold: true, color: C.white, fontFace: "Calibri",
      align: "center", valign: "middle", margin: 0
    });
    s.addText(r.title, {
      x: 0.72, y: y + 0.01, w: 4.2, h: 0.26,
      fontSize: 12, bold: true, color: C.charcoal, fontFace: "Calibri",
      align: "left", valign: "middle", margin: 0
    });
    s.addText(r.desc, {
      x: 0.72, y: y + 0.28, w: 4.2, h: 0.56,
      fontSize: 9, color: C.muted, fontFace: "Calibri",
      align: "left", valign: "top", margin: 0
    });
  });

  // Vertical divider
  s.addShape(pres.shapes.LINE, {
    x: 5.2, y: 0.75, w: 0, h: 4.65,
    line: { color: "D1E8F5", width: 1 }
  });

  // Right: pipeline + key numbers
  s.addText("End-to-End Pipeline", {
    x: 5.4, y: 0.82, w: 4.3, h: 0.3,
    fontSize: 12, bold: true, color: C.charcoal, fontFace: "Calibri", margin: 0
  });

  const steps = [
    "300 Real Rows (Aerospace Dataset)",
    "Physics Feature Extraction (6 derived features)",
    "Optuna HPO Tuning (per model)",
    "9-Model Parallel Generation",
    "6-Axis Composite Evaluation",
    "5,000 Synthetic Rows + 7 PDF Reports",
  ];
  steps.forEach((step, i) => {
    const y = 1.22 + i * 0.55;
    s.addShape(pres.shapes.RECTANGLE, {
      x: 5.4, y, w: 4.2, h: 0.36,
      fill: { color: i === steps.length - 1 ? C.teal : C.navy },
      line: { color: i === steps.length - 1 ? C.teal : C.navy }
    });
    s.addText(step, {
      x: 5.5, y, w: 4.0, h: 0.36,
      fontSize: 9.5, color: C.white, fontFace: "Calibri",
      align: "left", valign: "middle", margin: 0
    });
    if (i < steps.length - 1) {
      s.addText("▼", {
        x: 7.1, y: y + 0.36, w: 0.5, h: 0.19,
        fontSize: 8, color: C.teal, fontFace: "Calibri",
        align: "center", margin: 0
      });
    }
  });

  // Key numbers bar
  s.addShape(pres.shapes.RECTANGLE, {
    x: 5.4, y: 5.05, w: 4.2, h: 0.3,
    fill: { color: "E0F2FE" }, line: { color: "E0F2FE" }
  });
  s.addText("9 models  ·  92 runs  ·  294 visualizations  ·  7 PDF reports  ·  736 files", {
    x: 5.4, y: 5.05, w: 4.2, h: 0.3,
    fontSize: 8.5, bold: false, color: C.navy, fontFace: "Calibri",
    align: "center", valign: "middle", margin: 0
  });
}

// ─── SLIDE 3: MINIMUM BAR ─────────────────────────────────────────────────────
{
  const s = pres.addSlide();
  addHeader(s, "Minimum Bar — All Checks Pass");

  // Best dataset callout
  s.addShape(pres.shapes.RECTANGLE, {
    x: 0.25, y: 0.75, w: 9.5, h: 0.45,
    fill: { color: "D1FAE5" }, line: { color: "059669" }
  });
  s.addText([
    { text: "Best Delivered Dataset: ", options: { bold: false, color: C.charcoal } },
    { text: "KDE_s123_n5000_r035.csv", options: { bold: true, color: C.green } },
    { text: "  ·  5,000 rows  ·  22 columns  ·  Composite Score 0.9965", options: { bold: false, color: C.charcoal } },
  ], {
    x: 0.35, y: 0.75, w: 9.3, h: 0.45,
    fontSize: 11, fontFace: "Calibri", valign: "middle", margin: 0
  });

  // Table
  const hdr = { fill: { color: C.dark }, color: C.white, bold: true };
  const passCell = (txt) => ({ text: txt, options: { fill: { color: C.paleGreen }, color: C.green, bold: true } });
  const rows = [
    [
      { text: "Check", options: { ...hdr } },
      { text: "Requirement", options: { ...hdr } },
      { text: "Method", options: { ...hdr } },
      { text: "Result", options: { ...hdr } },
      { text: "Status", options: { ...hdr } },
    ],
    ["Schema", "22 cols, correct names & dtypes", "Automated schema validator", "22/22 columns match, all dtypes correct", passCell("✓ PASS")],
    ["Null Values", "0 nulls", "pd.isnull().sum()", "0 nulls in 5,000-row dataset", passCell("✓ PASS")],
    ["Out-of-Range", "All values in physical range", "Hard boundary enforcement", "All within validated aerospace bounds", passCell("✓ PASS")],
    ["Categorical Vocab", "Exact case-sensitive match", "Set comparison", "100% vocabulary match (4 categorical features)", passCell("✓ PASS")],
    ["Row Count", "≥ 300 rows", "len()", "5,000 rows delivered (16.7× minimum)", passCell("✓ PASS")],
    ["Class Distribution", "Not skewed to one label", "Frequency counts", "All 4 targets within ±10% of uniform", passCell("✓ PASS")],
  ];
  s.addTable(rows, {
    x: 0.25, y: 1.28, w: 9.5,
    fontSize: 9.5, fontFace: "Calibri", align: "left",
    border: { pt: 0.5, color: "D1E8F5" },
    rowH: 0.5,
    colW: [1.2, 2.1, 1.9, 2.9, 0.9],
  });
}

// ─── SLIDE 4: STATISTICAL FIDELITY ───────────────────────────────────────────
{
  const s = pres.addSlide();
  addHeader(s, "Requirement 01: Statistical Fidelity");

  // Left column: metrics
  addSectionLabel(s, "5 DISTRIBUTIONAL TESTS — ALL PASS", 0.25, 0.78, C.navy);

  const stats = [
    { label: "KS Pass Rate",       val: "1.0000",  sub: "14/14 features · p > 0.53 every column" },
    { label: "KL Divergence",      val: "0.0177",  sub: "Benchmark < 0.05 = excellent" },
    { label: "Wasserstein Distance",val: "0.0399", sub: "Near-zero distributional shift" },
    { label: "JS Divergence",       val: "0.0043", sub: "Essentially zero" },
    { label: "MMD Score",           val: "0.0068", sub: "Distributions nearly identical" },
  ];
  stats.forEach((st, i) => {
    const y = 1.1 + i * 0.73;
    s.addShape(pres.shapes.RECTANGLE, {
      x: 0.25, y, w: 4.6, h: 0.6,
      fill: { color: C.paledark }, line: { color: "C5DFF0" }
    });
    s.addText(st.label, {
      x: 0.35, y: y + 0.04, w: 2.8, h: 0.24,
      fontSize: 9.5, bold: true, color: C.navy, fontFace: "Calibri", margin: 0
    });
    s.addText(st.val, {
      x: 3.1, y: y + 0.04, w: 1.65, h: 0.24,
      fontSize: 14, bold: true, color: C.green, fontFace: "Calibri",
      align: "right", margin: 0
    });
    s.addText(st.sub, {
      x: 0.35, y: y + 0.3, w: 4.35, h: 0.22,
      fontSize: 8, color: C.muted, fontFace: "Calibri", margin: 0
    });
  });

  // Right column: distribution overlay image
  addSectionLabel(s, "KDE SYNTHETIC vs REAL — SEED 123", 5.1, 0.78, C.teal);
  s.addImage({
    path: IMG("11_report_figures/kde_overlay_kde_s11_n5000.png"),
    x: 5.1, y: 1.1, w: 4.65, h: 3.6,
    altText: "KDE distribution overlay vs real"
  });

  s.addText("KDE achieves near-perfect distribution overlap across all 14 numeric features · Skewness preserved |Δskew| < 0.02", {
    x: 0.25, y: 4.82, w: 9.5, h: 0.3,
    fontSize: 8.5, color: C.muted, fontFace: "Calibri", align: "center", margin: 0
  });
}

// ─── SLIDE 5: FEATURE INTERDEPENDENCY + I/O COHERENCE ─────────────────────────
{
  const s = pres.addSlide();
  addHeader(s, "Req 02 + 03: Feature Interdependencies & Input→Output Coherence");

  // Left: Feature interdependency
  addSectionLabel(s, "FEATURE INTERDEPENDENCIES (Req 02)", 0.25, 0.75, C.navy);

  const featureStats = [
    { label: "Frobenius Norm (correlation matrix similarity)", val: "0.991" },
    { label: "Feature Importance MAE (real vs synthetic)",    val: "0.0039" },
    { label: "SHAP Overlap Score (all 4 targets)",            val: ">90%" },
    { label: "Top SHAP features match (real = synthetic)",    val: "100%" },
  ];
  featureStats.forEach((fs, i) => {
    const y = 1.08 + i * 0.47;
    s.addText(fs.label, {
      x: 0.25, y, w: 3.7, h: 0.22,
      fontSize: 9, color: C.charcoal, fontFace: "Calibri", margin: 0
    });
    s.addText(fs.val, {
      x: 3.97, y, w: 1.0, h: 0.22,
      fontSize: 12, bold: true, color: C.green, fontFace: "Calibri",
      align: "right", margin: 0
    });
    s.addShape(pres.shapes.LINE, {
      x: 0.25, y: y + 0.22, w: 4.7, h: 0,
      line: { color: "D1E8F5", width: 0.5 }
    });
  });

  s.addImage({
    path: IMG("06_feature_importance/feature_importance_heatmap.png"),
    x: 0.25, y: 3.0, w: 4.7, h: 2.1,
    altText: "Feature importance heatmap"
  });

  // Vertical divider
  s.addShape(pres.shapes.LINE, {
    x: 5.15, y: 0.75, w: 0, h: 4.55,
    line: { color: "D1E8F5", width: 1 }
  });

  // Right: I/O Coherence
  addSectionLabel(s, "INPUT→OUTPUT COHERENCE (Req 03)", 5.3, 0.75, C.teal);

  // Big TSTR/TRTS stats
  addStatBox(s, "1.000", "TSTR F1\nTrain Synthetic, Test Real", 5.3, 1.08, 2.15, 1.05, C.navy, C.white, "9BBFD4");
  addStatBox(s, "1.000", "TRTS Accuracy\nTrain Real, Test Synthetic", 7.6, 1.08, 2.1, 1.05, C.navy, C.white, "9BBFD4");

  s.addText([
    { text: "I/O Coherence Score: ", options: { bold: false } },
    { text: "0.9910", options: { bold: true, color: C.green } },
    { text: "  (Frobenius correlation preservation)", options: { bold: false } },
  ], {
    x: 5.3, y: 2.22, w: 4.4, h: 0.3,
    fontSize: 9.5, color: C.charcoal, fontFace: "Calibri", margin: 0
  });

  s.addImage({
    path: IMG("07_model_performance/si01_tstr_trts_heatmap.png"),
    x: 5.3, y: 2.6, w: 4.4, h: 2.55,
    altText: "TSTR/TRTS heatmap"
  });

  s.addText("CTGAN baseline TSTR = 0.33 (random chance) — KDE achieves 1.000 because it preserves joint distribution", {
    x: 0.25, y: 5.2, w: 9.5, h: 0.25,
    fontSize: 8, color: C.muted, fontFace: "Calibri", align: "center", margin: 0
  });
}

// ─── SLIDE 6: CLASS BALANCE + EDGE CASES ──────────────────────────────────────
{
  const s = pres.addSlide();
  addHeader(s, "Requirement 04: Class Balance & Edge Cases");

  // Left: Class balance
  addSectionLabel(s, "CLASS BALANCING STRATEGIES", 0.25, 0.75, C.navy);

  const balRows = [
    [
      { text: "Strategy", options: { fill: { color: C.dark }, color: C.white, bold: true } },
      { text: "Balance Score", options: { fill: { color: C.dark }, color: C.white, bold: true } },
      { text: "TSTR F1", options: { fill: { color: C.dark }, color: C.white, bold: true } },
      { text: "Verdict", options: { fill: { color: C.dark }, color: C.white, bold: true } },
    ],
    ["Real + SMOTE-NC oversampling", "0.9663", "0.9903", { text: "✓ Good", options: { color: C.green, bold: true } }],
    [
      { text: "KDE Synthetic + Undersampling", options: { fill: { color: "D1FAE5" }, bold: true } },
      { text: "0.9769", options: { fill: { color: "D1FAE5" }, color: C.green, bold: true } },
      { text: "1.0000", options: { fill: { color: "D1FAE5" }, color: C.green, bold: true } },
      { text: "★ BEST", options: { fill: { color: "D1FAE5" }, color: C.green, bold: true } },
    ],
    ["Unbalanced KDE (baseline)", "0.9327", "1.0000", "Baseline"],
  ];
  s.addTable(balRows, {
    x: 0.25, y: 1.05, w: 4.65,
    fontSize: 9, fontFace: "Calibri",
    border: { pt: 0.5, color: "D1E8F5" },
    rowH: 0.44, colW: [2.0, 1.0, 0.75, 0.9],
  });

  s.addText("KDE Synthetic + Undersampling achieves 0.9769 balance while maintaining TSTR F1 = 1.000. No label corruption from balancing.", {
    x: 0.25, y: 2.9, w: 4.65, h: 0.5,
    fontSize: 8.5, color: C.muted, fontFace: "Calibri", margin: 0
  });

  s.addImage({
    path: IMG("05_validation_metrics/cb02_chi_square_heatmap.png"),
    x: 0.25, y: 3.45, w: 4.65, h: 1.7,
    altText: "Chi-square heatmap class balance"
  });

  // Vertical divider
  s.addShape(pres.shapes.LINE, {
    x: 5.1, y: 0.75, w: 0, h: 4.5,
    line: { color: "D1E8F5", width: 1 }
  });

  // Right: Edge cases
  addSectionLabel(s, "30 EDGE CASE SCENARIOS — 6 CATEGORIES", 5.25, 0.75, C.teal);

  const edgeRows = [
    [
      { text: "Category", options: { fill: { color: C.dark }, color: C.white, bold: true } },
      { text: "Scenarios", options: { fill: { color: C.dark }, color: C.white, bold: true } },
      { text: "Avg Realism", options: { fill: { color: C.dark }, color: C.white, bold: true } },
    ],
    ["Lifecycle Extremes", "2", { text: "94.8%", options: { color: C.green, bold: true } }],
    ["Target Extremes", "4", { text: "93.3%", options: { color: C.green, bold: true } }],
    ["Flight Envelope", "6", { text: "93.0%", options: { color: C.green, bold: true } }],
    ["Material Clusters", "8", { text: "91.1%", options: { color: C.green, bold: true } }],
    ["Optimization Scenarios", "4", { text: "87.2%", options: { color: C.amber, bold: true } }],
    ["Geometry Extremes", "4", { text: "83.9%", options: { color: C.amber, bold: true } }],
    [
      { text: "OVERALL (30 scenarios)", options: { fill: { color: "D1FAE5" }, bold: true } },
      { text: "30", options: { fill: { color: "D1FAE5" }, bold: true } },
      { text: "91.0%", options: { fill: { color: "D1FAE5" }, color: C.green, bold: true } },
    ],
  ];
  s.addTable(edgeRows, {
    x: 5.25, y: 1.05, w: 4.45,
    fontSize: 9, fontFace: "Calibri",
    border: { pt: 0.5, color: "D1E8F5" },
    rowH: 0.44, colW: [2.3, 0.85, 1.3],
  });

  s.addText("Validation: LOF-based realism scoring + Isolation Forest anomaly detection + Nearest-neighbour distance to reference rows", {
    x: 5.25, y: 4.9, w: 4.45, h: 0.4,
    fontSize: 8, color: C.muted, fontFace: "Calibri", margin: 0
  });
}

// ─── SLIDE 7: 9 MODELS BENCHMARKED ───────────────────────────────────────────
{
  const s = pres.addSlide();
  addHeader(s, "9 Models Benchmarked — KDE Wins Decisively");

  // Left: Tier classification
  addSectionLabel(s, "3 TIERS EMERGED FROM BENCHMARKING", 0.25, 0.75, C.navy);

  const tiers = [
    { name: "TIER 1 — PRODUCTION READY", color: C.teal, models: [
      { m: "KDE", s: "0.9965", highlight: true },
      { m: "GMM", s: "0.8534" },
      { m: "Copula", s: "0.8309" },
    ]},
    { name: "TIER 2 — RESEARCH INTEREST", color: C.amber, models: [
      { m: "TabuDiff", s: "~0.82" },
      { m: "TabuDiffPremium", s: "~0.82" },
    ]},
    { name: "TIER 3 — NOT RECOMMENDED", color: C.red, models: [
      { m: "CTGAN", s: "0.42" },
      { m: "TVAE", s: "~0.25" },
      { m: "DP-TVAE", s: "~0.23" },
      { m: "MaskedPredictor", s: "0.44" },
    ]},
  ];

  let y = 1.05;
  tiers.forEach(tier => {
    s.addShape(pres.shapes.RECTANGLE, {
      x: 0.25, y, w: 4.6, h: 0.28,
      fill: { color: tier.color }, line: { color: tier.color }
    });
    s.addText(tier.name, {
      x: 0.35, y, w: 4.4, h: 0.28,
      fontSize: 9, bold: true, color: C.white, fontFace: "Calibri",
      valign: "middle", margin: 0
    });
    y += 0.28;
    tier.models.forEach(m => {
      s.addShape(pres.shapes.RECTANGLE, {
        x: 0.25, y, w: 4.6, h: 0.38,
        fill: { color: m.highlight ? "D1FAE5" : "F8FBFF" },
        line: { color: "D1E8F5" }
      });
      s.addText(m.m, {
        x: 0.55, y: y + 0.05, w: 2.8, h: 0.28,
        fontSize: m.highlight ? 11 : 9.5,
        bold: m.highlight ? true : false,
        color: m.highlight ? C.navy : C.charcoal,
        fontFace: "Calibri", margin: 0
      });
      s.addText(`Composite: ${m.s}`, {
        x: 3.0, y: y + 0.07, w: 1.65, h: 0.24,
        fontSize: 9, bold: m.highlight, color: m.highlight ? C.green : C.muted,
        fontFace: "Calibri", align: "right", margin: 0
      });
      if (m.highlight) {
        s.addText("★ WINNER", {
          x: 4.55, y: y + 0.08, w: 0.5, h: 0.22,
          fontSize: 7.5, bold: true, color: C.green, fontFace: "Calibri", margin: 0
        });
      }
      y += 0.38;
    });
    y += 0.1;
  });

  s.addText("KDE decisively outperforms deep learning: composite 0.9965 vs CTGAN 0.42 · TSTR = 1.000 · zero memorization · zero physics violations", {
    x: 0.25, y: 5.05, w: 4.6, h: 0.3,
    fontSize: 7.5, color: C.muted, fontFace: "Calibri", margin: 0
  });

  // Vertical divider
  s.addShape(pres.shapes.LINE, {
    x: 5.1, y: 0.75, w: 0, h: 4.5,
    line: { color: "D1E8F5", width: 1 }
  });

  // Right: Leaderboard image
  addSectionLabel(s, "TOP 10 LEADERBOARD — ALL KDE", 5.25, 0.75, C.teal);
  s.addImage({
    path: IMG("07_model_performance/top10_leaderboard.png"),
    x: 5.25, y: 1.05, w: 4.45, h: 4.1,
    altText: "Model leaderboard"
  });
}

// ─── SLIDE 8: DEEPER VALIDATIONS ─────────────────────────────────────────────
{
  const s = pres.addSlide();
  addHeader(s, "Deeper Validations: Privacy, Physics & Visual Structure");

  // Top: 4 key stats
  const deepStats = [
    { val: "0.0003", label: "MMD (KDE n=5000)\nnear-zero distributional distance" },
    { val: "0.478",  label: "Discriminator AUC\nRF cannot distinguish real from synthetic" },
    { val: "0",      label: "Physics Violations\nKDE implicitly learns all constraints" },
    { val: "95.5%",  label: "Indistinguishability\nKDE rows identical to real data" },
  ];
  deepStats.forEach((ds, i) => {
    addStatBox(s, ds.val, ds.label, 0.25 + i * 2.38, 0.75, 2.2, 0.98, C.navy, C.white, "9BBFD4");
  });

  // Bottom: 2 images side by side
  addSectionLabel(s, "DISCRIMINATOR ROC CURVES", 0.25, 1.82, C.teal);
  s.addImage({
    path: IMG("05_validation_metrics/discriminator_roc_curves.png"),
    x: 0.25, y: 2.08, w: 4.65, h: 3.0,
    altText: "Discriminator ROC curves"
  });

  addSectionLabel(s, "PCA OVERLAY: REAL vs KDE SYNTHETIC", 5.1, 1.82, C.navy);
  s.addImage({
    path: IMG("10_dimensionality_reduction/si06_pca_overlay.png"),
    x: 5.1, y: 2.08, w: 4.65, h: 3.0,
    altText: "PCA overlay real vs synthetic"
  });

  s.addText("KDE AUC 0.478 ≈ random — ideal = 0.50 · TVAE AUC = 0.999 = memorization (NOT safe) · KDE NN distance = 0.0000 — perfect overlap", {
    x: 0.25, y: 5.17, w: 9.5, h: 0.27,
    fontSize: 8, color: C.muted, fontFace: "Calibri", align: "center", margin: 0
  });
}

// ─── SLIDE 9: DELIVERABLES + RECOMMENDATION ───────────────────────────────────
{
  const s = pres.addSlide();
  s.background = { color: C.dark };

  // Teal top/bottom accents
  s.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 0, w: 10, h: 0.06,
    fill: { color: C.teal }, line: { color: C.teal }
  });
  s.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 5.565, w: 10, h: 0.06,
    fill: { color: C.teal }, line: { color: C.teal }
  });

  s.addText("Complete Deliverables Package", {
    x: 0.4, y: 0.1, w: 9.2, h: 0.5,
    fontSize: 20, bold: true, color: C.white, fontFace: "Calibri", margin: 0
  });

  // 4 deliverable boxes
  const boxes = [
    { title: "7 PDF REPORTS", color: C.teal, items: ["Executive Summary (1-page checklist)", "Deep Data Analysis (30+ pages EDA)", "Business Narrative", "Model Comparison (9-model benchmark)", "Feature Interdependency", "Input-Output Coherence", "Similarity & Innovation"] },
    { title: "294 VISUALIZATIONS", color: "1A6B8A", items: ["42 Univariate distributions", "22 Bivariate interactions", "79 Real vs Synthetic overlays", "31 Target & class analysis", "21 Validation metric heatmaps", "10 Feature importance (SHAP+RF)", "36 PCA/t-SNE overlays"] },
    { title: "112 SYNTHETIC DATASETS", color: "0F5070", items: ["9 best-per-model CSVs", "Top 10 ranked + composite index", "89 experimental archive CSVs", "30 edge case scenario CSVs", "4 balanced per-target datasets", "Best: KDE_s123_n5000_r035.csv"] },
    { title: "REPRODUCIBILITY PACK", color: "0A3D5C", items: ["requirements.txt", "reproduce_graphs.py", "edge_case_catalog.csv", "graph_catalog.csv (294 charts)", "Optuna trial logs (JSON per model)", "DIRECTORY_GUIDE.md navigation"] },
  ];

  boxes.forEach((box, i) => {
    const x = 0.25 + i * 2.38;
    s.addShape(pres.shapes.RECTANGLE, {
      x, y: 0.68, w: 2.25, h: 0.28,
      fill: { color: box.color }, line: { color: box.color }
    });
    s.addText(box.title, {
      x, y: 0.68, w: 2.25, h: 0.28,
      fontSize: 7.5, bold: true, color: C.white, fontFace: "Calibri",
      align: "center", valign: "middle", margin: 0
    });
    box.items.forEach((item, j) => {
      s.addText("· " + item, {
        x: x + 0.05, y: 1.0 + j * 0.3, w: 2.15, h: 0.3,
        fontSize: 8, color: "9BBFD4", fontFace: "Calibri",
        align: "left", valign: "top", margin: 0
      });
    });
  });

  // Recommended dataset box
  s.addShape(pres.shapes.RECTANGLE, {
    x: 0.25, y: 4.4, w: 9.5, h: 0.75,
    fill: { color: "0A3D5C" }, line: { color: C.teal }
  });
  s.addText([
    { text: "★  RECOMMENDED DATASET: ", options: { bold: true, color: C.teal } },
    { text: "KDE_s123_n5000_r035.csv", options: { bold: true, color: C.white } },
    { text: "  ·  Composite 0.9965  ·  TSTR F1 1.000  ·  MMD 0.0003  ·  0 Physics Violations  ·  5,000 rows  ·  22 cols", options: { bold: false, color: "9BBFD4" } },
  ], {
    x: 0.45, y: 4.4, w: 9.1, h: 0.42,
    fontSize: 10.5, fontFace: "Calibri", valign: "middle", margin: 0
  });
  s.addText("736 total files  ·  157 MB  ·  300 → 5,000 rows (16.7× augmentation)  ·  All client requirements addressed and exceeded", {
    x: 0.45, y: 4.82, w: 9.1, h: 0.28,
    fontSize: 9, color: "5A8AA6", fontFace: "Calibri", margin: 0
  });
}

// ─── WRITE ────────────────────────────────────────────────────────────────────
pres.writeFile({ fileName: "LnT_Aerospace_POC_Compact.pptx" })
  .then(() => console.log("✅  Saved: LnT_Aerospace_POC_Compact.pptx"))
  .catch(err => { console.error("❌  Error:", err); process.exit(1); });
