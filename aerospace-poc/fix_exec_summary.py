"""Step 3: Generate a polished 1-page Executive Summary PDF."""
from fpdf import FPDF
import os

OUT = "D:/aero/final_LnT/reports/executive_summary.pdf"

class ExecPDF(FPDF):
    def header(self):
        pass
    def footer(self):
        self.set_y(-12)
        self.set_font("Helvetica", "I", 7)
        self.set_text_color(120, 120, 120)
        self.cell(0, 10, "Aerospace Synthetic Data Generation | Confidential", align="C")


pdf = ExecPDF("P", "mm", "A4")
pdf.set_auto_page_break(auto=False)
pdf.add_page()

# ── HEADER BAR ──
pdf.set_fill_color(27, 42, 74)  # navy #1B2A4A
pdf.rect(0, 0, 210, 38, "F")
pdf.set_xy(12, 8)
pdf.set_font("Helvetica", "B", 20)
pdf.set_text_color(255, 255, 255)
pdf.cell(0, 10, "Executive Summary")
pdf.ln()
pdf.set_xy(12, 20)
pdf.set_font("Helvetica", "", 11)
pdf.set_text_color(200, 220, 255)
pdf.cell(0, 8, "Aerospace Structural Design Dataset  |  Synthetic Data Generation & Validation")

# ── OBJECTIVE ──
y = 44
pdf.set_xy(12, y)
pdf.set_font("Helvetica", "B", 11)
pdf.set_text_color(27, 42, 74)
pdf.cell(0, 7, "OBJECTIVE")
pdf.set_xy(12, y + 8)
pdf.set_font("Helvetica", "", 9)
pdf.set_text_color(50, 50, 50)
pdf.multi_cell(186, 4.5,
    "Generate high-fidelity synthetic data from a 300-row aerospace structural design dataset, "
    "preserving statistical distributions, feature interdependencies, input-to-output coherence, "
    "and class balance across 4 categorical target variables.")

# ── BEST MODEL BOX ──
y = 68
pdf.set_fill_color(240, 245, 250)
pdf.rect(12, y, 186, 42, "F")
pdf.set_draw_color(27, 42, 74)
pdf.rect(12, y, 186, 42, "D")

pdf.set_xy(16, y + 3)
pdf.set_font("Helvetica", "B", 11)
pdf.set_text_color(27, 42, 74)
pdf.cell(60, 6, "RECOMMENDED MODEL:  KDE")
pdf.set_font("Helvetica", "", 8)
pdf.set_text_color(100, 100, 100)
pdf.cell(0, 6, "(Kernel Density Estimation)")

metrics = [
    ("Composite Score", "0.9965 / 1.0", "Weighted aggregate of all quality dimensions"),
    ("MMD", "0.00027", "Near-zero = distributions statistically indistinguishable"),
    ("Discriminator AUC", "0.478", "Near-random (0.50) = classifier cannot tell real from synthetic"),
    ("TSTR Accuracy", "1.000", "Model trained on synthetic achieves perfect accuracy on real data"),
    ("Schema Compliance", "22/22 cols, 0 nulls, 0 OOR", "Full schema match, zero out-of-range values"),
    ("Output Size", "5,000 rows", "16.7x the original dataset"),
]
pdf.set_font("Helvetica", "", 8)
row_y = y + 12
for label, value, note in metrics:
    pdf.set_xy(18, row_y)
    pdf.set_font("Helvetica", "B", 8)
    pdf.set_text_color(27, 42, 74)
    pdf.cell(32, 4.5, label)
    pdf.set_font("Helvetica", "B", 8)
    pdf.set_text_color(220, 60, 60)
    pdf.cell(38, 4.5, value)
    pdf.set_font("Helvetica", "", 7.5)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 4.5, note)
    row_y += 4.8

# ── CLIENT CRITERIA CHECKLIST ──
y = 116
pdf.set_xy(12, y)
pdf.set_font("Helvetica", "B", 11)
pdf.set_text_color(27, 42, 74)
pdf.cell(0, 7, "CLIENT CRITERIA CHECKLIST")

criteria = [
    ("Statistical Fidelity", "KS test 100% pass rate, KL divergence 0.004, all distributions shape-matched"),
    ("Feature Interdependencies", "Correlation Frobenius norm 0.20 (convergent at n=5000), structure preserved"),
    ("Input-to-Output Coherence", "SHAP top-5 feature overlap 3/5, 12 domain physics rules tested, TSTR=1.0"),
    ("Class Balance & Edge Cases", "Chi-square p > 0.83 all targets, 27 edge scenarios at 95.9% Tier-1 pass"),
    ("Rare Case Realism", "Isolation Forest + LOF + NN-distance validated; mean realism score 90.1%"),
    ("Overall Similarity", "MMD, TSTR/TRTS, Discriminator AUC all validated with 30-seed bootstrap CIs"),
]
row_y = y + 9
for label, detail in criteria:
    pdf.set_xy(14, row_y)
    pdf.set_font("Helvetica", "B", 8.5)
    pdf.set_text_color(34, 139, 34)
    pdf.cell(4, 4.5, "[OK]")
    pdf.set_text_color(27, 42, 74)
    pdf.cell(42, 4.5, "  " + label)
    pdf.set_font("Helvetica", "", 7.5)
    pdf.set_text_color(60, 60, 60)
    pdf.cell(0, 4.5, detail)
    row_y += 6.5

# ── VALIDATION DEEPER DIVE ──
y = 162
pdf.set_xy(12, y)
pdf.set_font("Helvetica", "B", 11)
pdf.set_text_color(27, 42, 74)
pdf.cell(0, 7, "DEEPER VALIDATIONS PERFORMED")

validations = [
    ("I/P to O/P Correlations", "Correlation matrix, grouped stats by target class, conditional distributions"),
    ("Feature Structure", "Per-column histograms vs reference, KS test, KL divergence, joint pair plots"),
    ("Class Balance Tests", "Class frequency counts, chi-square tests, joint 4-way target distribution"),
    ("Rare Case Realism", "Isolation Forest, LOF, nearest-neighbour distance to reference rows"),
    ("Overall Similarity", "Train-on-synthetic/test-on-real (TSTR), MMD, discriminator AUC with bootstrap CIs"),
]
row_y = y + 9
for label, detail in validations:
    pdf.set_xy(14, row_y)
    pdf.set_font("Helvetica", "B", 8)
    pdf.set_text_color(27, 42, 74)
    pdf.cell(38, 4.5, label)
    pdf.set_font("Helvetica", "", 7.5)
    pdf.set_text_color(60, 60, 60)
    pdf.cell(0, 4.5, detail)
    row_y += 5.5

# ── MODEL BENCHMARKING SUMMARY ──
y = 200
pdf.set_xy(12, y)
pdf.set_font("Helvetica", "B", 11)
pdf.set_text_color(27, 42, 74)
pdf.cell(0, 7, "MODEL BENCHMARKING (9 Models, 92 Configurations)")

# Table header
row_y = y + 10
pdf.set_fill_color(27, 42, 74)
pdf.set_xy(14, row_y)
pdf.set_font("Helvetica", "B", 7.5)
pdf.set_text_color(255, 255, 255)
headers = [("Model", 28), ("Tier", 18), ("Composite", 20), ("MMD", 20), ("Disc. AUC", 18), ("TSTR", 14), ("Verdict", 68)]
for h, w in headers:
    pdf.cell(w, 5, h, border=1, fill=True, align="C")
pdf.ln()

models = [
    ("KDE", "Production", "0.9965", "0.00027", "0.478", "1.000", "Best overall - recommended"),
    ("GMM", "Production", "0.8535", "0.0007", "0.451", "0.460", "Excellent discriminator score"),
    ("Copula", "Production", "0.8309", "0.0013", "0.518", "0.347", "Best indistinguishability (96.5%)"),
    ("TabuDiff", "Research", "0.7890", "0.0207", "0.722", "0.313", "Best deep-learning model"),
    ("MaskedPredictor", "Research", "0.5250", "0.0276", "0.976", "0.303", "High variance, conditional learning"),
    ("TVAE/CTGAN", "Evaluated", "0.610", "> 0.4", "~1.0", "0.300", "Class collapse - not recommended"),
]
row_y += 5
for m in models:
    pdf.set_xy(14, row_y)
    pdf.set_font("Helvetica", "", 7)
    pdf.set_text_color(50, 50, 50)
    vals = list(zip(m, [h[1] for h in headers]))
    for val, w in vals:
        pdf.cell(w, 4.5, val, border=1, align="C")
    pdf.ln()
    row_y += 4.5

# ── DELIVERABLE CONTENTS ──
y = 250
pdf.set_xy(12, y)
pdf.set_font("Helvetica", "B", 11)
pdf.set_text_color(27, 42, 74)
pdf.cell(0, 7, "DELIVERABLE CONTENTS")

pdf.set_xy(14, y + 9)
pdf.set_font("Helvetica", "", 8.5)
pdf.set_text_color(50, 50, 50)

items = [
    "7 PDF Reports (EDA, Model Comparison, Feature Interdependency, I/O Coherence, Class Balance, Similarity, Business Narrative)",
    "294 Catalogued Visualizations across 11 categories with searchable graph_catalog.csv",
    "9 Best-per-model synthetic datasets + Top 10 leaderboard + 92 experimental archives",
    "Full validation pipeline: Anomaly detection, class balancing, edge cases, discriminator tests, MMD, PCA/t-SNE",
]
row_y = y + 9
for item in items:
    pdf.set_xy(14, row_y)
    pdf.set_font("Helvetica", "B", 8)
    pdf.cell(3, 4.5, "-")
    pdf.set_font("Helvetica", "", 8)
    pdf.cell(0, 4.5, "  " + item)
    row_y += 5.5

# ── RECOMMENDED READING ORDER ──
row_y += 2
pdf.set_xy(12, row_y)
pdf.set_font("Helvetica", "B", 9)
pdf.set_text_color(27, 42, 74)
pdf.cell(0, 5, "RECOMMENDED READING ORDER")
row_y += 6
pdf.set_font("Helvetica", "", 7.5)
pdf.set_text_color(60, 60, 60)
steps = [
    "1. This Summary",
    "2. Model Comparison Report",
    "3. Similarity & Innovation Report",
    "4. Deep Data Analysis Report",
    "5. Remaining reports as needed"
]
pdf.set_xy(14, row_y)
pdf.cell(0, 4, "    ".join(steps))

# Save
pdf.output(OUT)
print(f"Executive summary saved to: {OUT}")
print(f"File size: {os.path.getsize(OUT):,} bytes")
