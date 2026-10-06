"""
Build LnT_Aerospace_Synthetic_Data_POC_v4.pptx
- Remove all emojis (checkmarks, plus signs, etc.)
- Add 3 new process flow slides (full pipeline, physics features, 6-axis evaluation)
- Embed better graphs from deliverables_LnT
- Professional boardroom-ready formatting
"""

import copy
import os
import sys
sys.stdout.reconfigure(encoding='utf-8')

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt
from pptx.oxml.ns import qn
from lxml import etree
import copy
from pptx.util import Inches, Pt, Emu
from pptx.enum.dml import MSO_THEME_COLOR
from pptx.oxml import parse_xml

# ── Colour palette ─────────────────────────────────────────────────────────
C_DARK_NAVY  = RGBColor(0x0D, 0x1B, 0x3E)   # slide title bg / headers
C_MID_BLUE   = RGBColor(0x1A, 0x4F, 0x8C)   # section headers
C_ACCENT     = RGBColor(0x2E, 0x86, 0xC1)   # accent blue
C_GOLD       = RGBColor(0xF3, 0x9C, 0x12)   # highlight gold
C_WHITE      = RGBColor(0xFF, 0xFF, 0xFF)
C_LIGHT_GRAY = RGBColor(0xF2, 0xF5, 0xF9)
C_MED_GRAY   = RGBColor(0xAA, 0xAA, 0xAA)
C_GREEN      = RGBColor(0x27, 0xAE, 0x60)
C_ORANGE     = RGBColor(0xE6, 0x7E, 0x22)
C_RED        = RGBColor(0xC0, 0x39, 0x2B)
C_TEXT_DARK  = RGBColor(0x1A, 0x1A, 0x2E)

# ── Slide dimensions (widescreen 10×5.625 in) ───────────────────────────────
W = Inches(10)
H = Inches(5.625)

# ── Helpers ────────────────────────────────────────────────────────────────

def emu(inches): return int(inches * 914400)
def pt(emus):    return int(emus / 12700) if emus else 12

def set_shape_fill(shape, color: RGBColor):
    shape.fill.solid()
    shape.fill.fore_color.rgb = color

def set_shape_line(shape, color=None, width_pt=0):
    if color is None:
        shape.line.fill.background()
    else:
        shape.line.color.rgb = color
        shape.line.width = Pt(width_pt)

def clear_text_frame(tf):
    for para in tf.paragraphs:
        for run in para.runs:
            run.text = ""

def add_textbox(slide, left, top, width, height, text,
                font_size=12, bold=False, color=C_TEXT_DARK,
                align=PP_ALIGN.LEFT, wrap=True, font_name="Calibri"):
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = wrap
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.size = Pt(font_size)
    run.font.bold = bold
    run.font.color.rgb = color
    run.font.name = font_name
    return txBox

def add_rect(slide, left, top, width, height, fill_color=None,
             line_color=None, line_width_pt=0):
    shape = slide.shapes.add_shape(
        1,  # MSO_SHAPE_TYPE.RECTANGLE
        left, top, width, height
    )
    if fill_color:
        shape.fill.solid()
        shape.fill.fore_color.rgb = fill_color
    else:
        shape.fill.background()
    if line_color:
        shape.line.color.rgb = line_color
        shape.line.width = Pt(line_width_pt)
    else:
        shape.line.fill.background()
    return shape

def add_rounded_rect(slide, left, top, width, height,
                     fill_color=None, line_color=None, line_width_pt=0):
    shape = slide.shapes.add_shape(
        5,  # ROUNDED_RECTANGLE
        left, top, width, height
    )
    if fill_color:
        shape.fill.solid()
        shape.fill.fore_color.rgb = fill_color
    else:
        shape.fill.background()
    if line_color:
        shape.line.color.rgb = line_color
        shape.line.width = Pt(line_width_pt)
    else:
        shape.line.fill.background()
    return shape

def set_run_font(run, size=12, bold=False, italic=False,
                 color=C_TEXT_DARK, font_name="Calibri"):
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = color
    run.font.name = font_name

def add_para(tf, text, size=12, bold=False, color=C_TEXT_DARK,
             align=PP_ALIGN.LEFT, space_before=0, space_after=0,
             font_name="Calibri", italic=False):
    p = tf.add_paragraph()
    p.alignment = align
    p.space_before = Pt(space_before)
    p.space_after  = Pt(space_after)
    run = p.add_run()
    run.text = text
    set_run_font(run, size=size, bold=bold, italic=italic,
                 color=color, font_name=font_name)
    return p

def replace_emoji_text(text):
    """Replace emoji characters with clean text equivalents."""
    replacements = {
        '✅': '[PASS] ',
        '➕': '[EXTRA] ',
        '⚠': '[NOTE] ',
        '❌': '[FAIL] ',
        '✓': '[OK] ',
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text

def clean_slide_text(slide):
    """Remove emojis from all text shapes on a slide."""
    for shape in slide.shapes:
        if not shape.has_text_frame:
            continue
        for para in shape.text_frame.paragraphs:
            for run in para.runs:
                run.text = replace_emoji_text(run.text)

def add_picture(slide, img_path, left, top, width=None, height=None):
    if not os.path.exists(img_path):
        print(f"  [WARN] Image not found: {img_path}")
        return None
    if width and height:
        pic = slide.shapes.add_picture(img_path, left, top, width, height)
    elif width:
        pic = slide.shapes.add_picture(img_path, left, top, width=width)
    elif height:
        pic = slide.shapes.add_picture(img_path, left, top, height=height)
    else:
        pic = slide.shapes.add_picture(img_path, left, top)
    return pic

def slide_header(slide, title, subtitle=None,
                 bg_color=C_DARK_NAVY, accent_color=C_ACCENT):
    """Add a professional header bar to a slide."""
    # Background
    add_rect(slide, 0, 0, W, H, fill_color=C_WHITE)
    # Title bar
    add_rect(slide, 0, 0, W, Inches(0.85), fill_color=bg_color)
    # Accent line
    add_rect(slide, 0, Inches(0.85), W, Inches(0.04),
             fill_color=accent_color)
    # Title text
    add_textbox(slide, Inches(0.35), Inches(0.05), Inches(9.3), Inches(0.75),
                title, font_size=24, bold=True, color=C_WHITE,
                align=PP_ALIGN.LEFT, font_name="Calibri")
    if subtitle:
        add_textbox(slide, Inches(0.35), Inches(0.9), Inches(9.3), Inches(0.35),
                    subtitle, font_size=13, bold=False, color=C_MID_BLUE,
                    align=PP_ALIGN.LEFT, font_name="Calibri")
    return slide

def metric_card(slide, left, top, width, height, value, label,
                sublabel=None, bg=C_ACCENT, text_color=C_WHITE):
    """Add a metric card (coloured rounded rectangle with big number)."""
    card = add_rounded_rect(slide, left, top, width, height,
                            fill_color=bg, line_color=None)
    card.shadow.inherit = False
    # Value
    add_textbox(slide, left + Inches(0.05), top + Inches(0.08),
                width - Inches(0.1), Inches(0.5),
                value, font_size=28, bold=True, color=text_color,
                align=PP_ALIGN.CENTER, font_name="Calibri")
    # Label
    add_textbox(slide, left + Inches(0.05), top + Inches(0.58),
                width - Inches(0.1), Inches(0.3),
                label, font_size=11, bold=True, color=text_color,
                align=PP_ALIGN.CENTER, font_name="Calibri")
    if sublabel:
        add_textbox(slide, left + Inches(0.05), top + Inches(0.88),
                    width - Inches(0.1), Inches(0.25),
                    sublabel, font_size=9, bold=False, color=text_color,
                    align=PP_ALIGN.CENTER, font_name="Calibri")


# ── Load base presentation ─────────────────────────────────────────────────
print("Loading v3 presentation...")
prs = Presentation('LnT_Aerospace_Synthetic_Data_POC_v3.pptx')
print(f"  Slides: {len(prs.slides)}")

# ── Clean all existing slides (remove emojis) ─────────────────────────────
print("Cleaning emoji text from all slides...")
for i, slide in enumerate(prs.slides):
    clean_slide_text(slide)
print("  Done.")

# ── Add new slides ─────────────────────────────────────────────────────────
# We'll insert new slides after slide 3 (index 2) and slide 4 (index 3).
# python-pptx doesn't have a direct "insert_slide" — we'll rebuild via
# copy. Instead, work on the existing layout + add new ones at the end,
# then reorder using the XML hack.

# ── Define new slide content ───────────────────────────────────────────────
# We'll add slides at the end, then reorder.

def make_blank_slide(prs):
    # Use the only available layout (v3 has 1 layout)
    layout = prs.slide_layouts[0]
    slide = prs.slides.add_slide(layout)
    # Remove any placeholder shapes from the layout
    for shape in list(slide.shapes):
        sp = shape._element
        # Remove shapes that are placeholders
        if sp.tag.endswith('}sp'):
            # Check if it's a placeholder by looking for <p:ph> element
            ph_list = sp.findall('.//{http://schemas.openxmlformats.org/presentationml/2006/main}ph')
            if ph_list:
                sp.getparent().remove(sp)
    return slide

# ─────────────────────────────────────────────────────────────────────────────
# NEW SLIDE A: Full Process Flow (insert after slide 3 = index 3)
# ─────────────────────────────────────────────────────────────────────────────
print("\nBuilding NEW SLIDE A: Full Process Flow...")
slide_a = make_blank_slide(prs)
slide_header(slide_a,
             "Complete Process Flow: Raw Data to Production Dataset",
             "Step-by-step pipeline from 300-row CSV to validated 5,000-row synthetic dataset")

# Pipeline boxes
pipeline_steps = [
    ("Data\nPreparation",    C_MID_BLUE,  "CSV load, type enforcement,\nPII scan, missing values,\nencoding, 80/20 stratified split"),
    ("Physics\nFeature\nExtraction", C_ACCENT,  "6 derived features:\nSpecific Stiffness, Buckling\nResistance, Elastic Energy,\nFatigue Ratio, Stress Factor"),
    ("Multi-Phase\nBenchmarking",  RGBColor(0x16,0x6A,0x9E),  "Phase 1: 3 Optuna trials\n(rapid elimination)\nPhase 2: 6 Optuna trials\n(full HP search)"),
    ("9-Model\nGeneration",  RGBColor(0x1E,0x88,0xE5),  "KDE, GMM, Copula, TVAE,\nTVAEPremium, CTGAN,\nCTGANPremium, TabuDiff,\nMaskedPredictor"),
    ("Physics\nRepair",       RGBColor(0x43,0xA0,0x47),  "Hard constraint enforcement:\nFatigue ≤ Tensile, Yield ≤ Tensile,\nmaterial density bounds"),
    ("6-Axis\nEvaluation",    RGBColor(0x7B,0x1F,0xA2),  "Statistical(30%) + ML(25%)\n+ Physics(20%) + Corr(15%)\n+ Privacy(10%)"),
    ("Edge Cases\n& Reporting",RGBColor(0xE6,0x7E,0x22),  "30 engineering scenarios,\nLOF realism validation,\n7 PDF reports, 294 graphs"),
]

box_w = Inches(1.15)
box_h = Inches(1.0)
start_x = Inches(0.2)
y_row1 = Inches(1.55)
y_row2 = Inches(2.8)
gap_x  = Inches(0.15)
arrow_w = Inches(0.18)

for i, (title, color, detail) in enumerate(pipeline_steps):
    bx = start_x + i * (box_w + arrow_w)
    # Box
    r = add_rounded_rect(slide_a, bx, y_row1, box_w, box_h,
                          fill_color=color)
    # Step number
    add_textbox(slide_a, bx, y_row1 + Inches(0.02), box_w, Inches(0.22),
                f"Step {i+1}", font_size=8, bold=True,
                color=C_WHITE, align=PP_ALIGN.CENTER)
    # Title
    add_textbox(slide_a, bx + Inches(0.04), y_row1 + Inches(0.2),
                box_w - Inches(0.08), Inches(0.45),
                title, font_size=10, bold=True,
                color=C_WHITE, align=PP_ALIGN.CENTER)
    # Arrow (except last)
    if i < len(pipeline_steps) - 1:
        ax = bx + box_w + Inches(0.01)
        ay = y_row1 + box_h / 2 - Inches(0.1)
        add_textbox(slide_a, ax, ay, arrow_w, Inches(0.2),
                    ">>", font_size=11, bold=True,
                    color=color, align=PP_ALIGN.CENTER)

# Row 2 — sub-details under each step
sub_labels = [
    "300 rows → Preprocessed",
    "E/ρ, E·t², σ²/E, σ_f/σ_uts",
    "3 seeds × 4 sizes × 9 models",
    "92 total experimental runs",
    "Zero violations (KDE winner)",
    "Composite score per dataset",
    "736 files, 157 MB total",
]
for i, lbl in enumerate(sub_labels):
    bx = start_x + i * (box_w + arrow_w)
    add_textbox(slide_a, bx + Inches(0.02), y_row2 + Inches(0.05),
                box_w - Inches(0.04), Inches(0.3),
                lbl, font_size=7.5, bold=False, color=C_MID_BLUE,
                align=PP_ALIGN.CENTER)

# Phase labels
add_textbox(slide_a, Inches(0.2), y_row1 - Inches(0.25), Inches(3.7), Inches(0.22),
            "PHASE 1 — DATA TO CANDIDATE MODELS", font_size=9, bold=True,
            color=C_MID_BLUE, align=PP_ALIGN.LEFT)
add_textbox(slide_a, Inches(3.8), y_row1 - Inches(0.25), Inches(6.0), Inches(0.22),
            "PHASE 2 — GENERATION, VALIDATION & REPORTING", font_size=9, bold=True,
            color=C_MID_BLUE, align=PP_ALIGN.LEFT)

# Separator line
add_rect(slide_a, Inches(0.2), y_row2 + Inches(0.35), W - Inches(0.4), Inches(0.02),
         fill_color=C_MED_GRAY)

# Bottom row — key outcomes
outcomes = [
    ("16.7×", "Data Augmentation\n300 → 5,000 rows"),
    ("9", "Models Evaluated\nAll paradigms covered"),
    ("92", "Experimental Runs\nMulti-seed, multi-scale"),
    ("0.9965", "Best Composite\nKDE, n=5,000"),
    ("1.000", "TSTR F1 Score\nPerfect ML utility"),
    ("0", "Physics Violations\nDomain constraints met"),
    ("91%", "Edge Realism\nLOF-validated scenarios"),
]
out_w = Inches(1.25)
out_start_x = Inches(0.25)
out_y = Inches(3.55)
for i, (val, lbl) in enumerate(outcomes):
    ox = out_start_x + i * (out_w + Inches(0.08))
    metric_card(slide_a, ox, out_y, out_w, Inches(1.0),
                val, lbl.split('\n')[0], lbl.split('\n')[1],
                bg=C_LIGHT_GRAY, text_color=C_DARK_NAVY)

# Footer
add_textbox(slide_a, 0, H - Inches(0.3), W, Inches(0.28),
            "L&T Aerospace Synthetic Data POC  ·  March 2026",
            font_size=8, color=C_MED_GRAY, align=PP_ALIGN.CENTER)

print("  Done.")


# ─────────────────────────────────────────────────────────────────────────────
# NEW SLIDE B: Physics-Aware Generation (insert after slide A)
# ─────────────────────────────────────────────────────────────────────────────
print("\nBuilding NEW SLIDE B: Physics-Aware Generation...")
slide_b = make_blank_slide(prs)
slide_header(slide_b,
             "Physics-Aware Generation: 6 Derived Features + 4 Hard Repair Rules",
             "Domain-grounded engineering features computed from first principles")

# Left: 6 physics features
feat_data = [
    ("Specific Stiffness", "E / ρ", C_MID_BLUE,
     "Stiffness-to-weight ratio. Primary material selection criterion in aerospace design."),
    ("Buckling Resistance", "E × t²", C_ACCENT,
     "Euler column buckling — critical load capacity. Higher = more resistant to lateral collapse."),
    ("Elastic Energy", "σ² / E", RGBColor(0x16,0x6A,0x9E),
     "Modulus of resilience — max energy/m³ absorbed elastically without permanent deformation."),
    ("Fatigue Ratio", "σ_f / σ_uts", RGBColor(0x1E,0x88,0xE5),
     "Endurance ratio — fraction of tensile strength surviving indefinite cyclic loading."),
    ("Stress Factor", "Load × Span / t", RGBColor(0x43,0xA0,0x47),
     "Structural loading indicator — combined load, geometry, and thickness effect."),
    ("Thermal Proxy", "E × α × ΔT", RGBColor(0x7B,0x1F,0xA2),
     "Thermal expansion stress — governs behaviour across the altitude temperature range."),
]

feat_w = Inches(4.2)
feat_h = Inches(0.52)
feat_x = Inches(0.3)
feat_y = Inches(1.35)
feat_gap = Inches(0.06)

for i, (name, formula, color, desc) in enumerate(feat_data):
    row = i // 2
    col = i % 2
    fx = feat_x + col * Inches(4.7)
    fy = feat_y + row * (feat_h + feat_gap)
    # Color tag
    add_rect(slide_b, fx, fy, Inches(0.08), feat_h, fill_color=color)
    # Formula box
    add_rounded_rect(slide_b, fx + Inches(0.1), fy,
                     Inches(1.2), feat_h, fill_color=C_LIGHT_GRAY)
    add_textbox(slide_b, fx + Inches(0.12), fy + Inches(0.06),
                Inches(1.15), Inches(0.25),
                formula, font_size=11, bold=True, color=color,
                align=PP_ALIGN.CENTER)
    add_textbox(slide_b, fx + Inches(0.12), fy + Inches(0.3),
                Inches(1.15), Inches(0.2),
                name, font_size=8, bold=True, color=C_TEXT_DARK,
                align=PP_ALIGN.CENTER)
    # Description
    add_textbox(slide_b, fx + Inches(1.35), fy + Inches(0.04),
                Inches(2.75), feat_h - Inches(0.08),
                desc, font_size=8, bold=False, color=C_TEXT_DARK,
                align=PP_ALIGN.LEFT)

# Right: 4 repair rules + result
rx = Inches(5.4)
ry = Inches(1.35)
rw = Inches(4.3)

add_textbox(slide_b, rx, ry, rw, Inches(0.3),
            "Hard Repair Rules", font_size=12, bold=True,
            color=C_DARK_NAVY, align=PP_ALIGN.LEFT)
add_rect(slide_b, rx, ry + Inches(0.32), rw, Inches(0.025),
         fill_color=C_ACCENT)

rules = [
    ("Rule A", "Fatigue Limit <= Tensile Strength",
     "Fatigue limit cannot exceed ultimate strength.\nRepair: Fatigue = 0.85 × Tensile"),
    ("Rule B", "Yield Strength <= Tensile Strength",
     "Yield must precede fracture.\nRepair: Yield = min(Yield, 0.9 × Tensile)"),
    ("Rule C", "No Negative Physical Properties",
     "Density, E, σ_uts must be strictly positive.\nRepair: Replace with 1e-6"),
    ("Rule D", "Material Density Within Bounds",
     "Al: 2500-2900  Ti: 4400-4700\nCF: 1500-1800  Steel: 7700-8000\nRepair: Clip to nearest bound"),
]

rule_y = ry + Inches(0.38)
for i, (rname, violation, repair) in enumerate(rules):
    ry_cur = rule_y + i * Inches(0.65)
    add_rect(slide_b, rx, ry_cur, Inches(0.05), Inches(0.55),
             fill_color=C_ORANGE)
    add_textbox(slide_b, rx + Inches(0.1), ry_cur,
                Inches(0.65), Inches(0.2),
                rname, font_size=9, bold=True, color=C_ORANGE)
    add_textbox(slide_b, rx + Inches(0.1), ry_cur + Inches(0.18),
                rw - Inches(0.15), Inches(0.18),
                violation, font_size=8, bold=True, color=C_TEXT_DARK)
    add_textbox(slide_b, rx + Inches(0.1), ry_cur + Inches(0.34),
                rw - Inches(0.15), Inches(0.22),
                repair, font_size=7.5, bold=False, color=C_MED_GRAY)

# KDE winner highlight
wy = Inches(4.55)
add_rounded_rect(slide_b, rx, wy, rw, Inches(0.65),
                  fill_color=RGBColor(0x1E,0x88,0xE5))
add_textbox(slide_b, rx + Inches(0.1), wy + Inches(0.05),
            rw - Inches(0.2), Inches(0.55),
            "KDE WINNER:  0 Physics Repair Triggers\nKDE implicitly learns all physical constraints from the training data — "
            "no manual correction needed at generation time.",
            font_size=9, bold=False, color=C_WHITE, align=PP_ALIGN.LEFT)

# Footer
add_textbox(slide_b, 0, H - Inches(0.3), W, Inches(0.28),
            "L&T Aerospace Synthetic Data POC  ·  March 2026",
            font_size=8, color=C_MED_GRAY, align=PP_ALIGN.CENTER)

print("  Done.")


# ─────────────────────────────────────────────────────────────────────────────
# NEW SLIDE C: 6-Axis Evaluation Framework (insert after slide B)
# ─────────────────────────────────────────────────────────────────────────────
print("\nBuilding NEW SLIDE C: 6-Axis Evaluation Framework...")
slide_c = make_blank_slide(prs)
slide_header(slide_c,
             "6-Axis Composite Evaluation Framework",
             "Every synthetic dataset is scored across 6 independent quality dimensions")

# Composite formula
formula_box = add_rounded_rect(slide_c, Inches(0.3), Inches(1.25),
                                 Inches(9.4), Inches(0.55),
                                 fill_color=C_DARK_NAVY)
add_textbox(slide_c, Inches(0.4), Inches(1.3), Inches(9.2), Inches(0.45),
            "Composite Score  =  0.30 × Statistical  +  0.25 × ML Utility  +  0.20 × Physics  +  0.15 × Correlation  +  0.10 × Privacy",
            font_size=11, bold=True, color=C_GOLD, align=PP_ALIGN.CENTER)

# 6 axes
axes = [
    ("Statistical\nSimilarity", "30%",
     "Mean KL Divergence across\n14 numeric features.\nScore = max(0, 1 - mean(KL)).\nLower KL = closer distributions.",
     C_ACCENT,
     "KL < 0.05 = excellent"),
    ("ML Utility\n(TSTR F1)", "25%",
     "Train on Synthetic, Test on Real.\nRandom Forest classifiers trained\nexclusively on synthetic data;\ntested on real hold-out set.",
     RGBColor(0x1E,0x88,0xE5),
     "TSTR F1 = 1.000\n(synthetic = real for ML)"),
    ("Physics\nConsistency", "20%",
     "Per-row constraint checks\n(Fatigue <= Tensile, etc.) +\ncorrelation matrix similarity\n+ range validity (all within 5%).",
     RGBColor(0x16,0x6A,0x9E),
     "KDE: 0 violations\nTabuDiffPremium: 42-60%\nanomaly rate"),
    ("Correlation\nPreservation", "15%",
     "Frobenius norm of difference\nbetween real and synthetic\ncorrelation matrices.\nScore = max(0, 1 - ||Δcorr||_F / max).",
     RGBColor(0x43,0xA0,0x47),
     "KDE: 0.991\n(essentially identical)"),
    ("Privacy /\nDetectability", "10%",
     "Random Forest Discriminator AUC\n(trained to distinguish real vs.\nsynthetic). AUC = 0.5 = ideal.\nScore = 2 × |0.5 - AUC|.",
     RGBColor(0x7B,0x1F,0xA2),
     "KDE AUC = 0.478\n(≈ random chance)"),
    ("KS Test\n(Bonus)", "Bonus",
     "Kolmogorov-Smirnov test per\nnumeric feature. D = max|F_real\n- F_synthetic|. p > 0.05 = cannot\nreject same distribution.",
     C_ORANGE,
     "KDE: 14/14 features\np > 0.53 every column"),
]

card_w = Inches(1.5)
card_h = Inches(2.6)
card_start_x = Inches(0.2)
card_y = Inches(1.95)
card_gap = Inches(0.1)

for i, (name, weight, desc, color, highlight) in enumerate(axes):
    cx = card_start_x + i * (card_w + card_gap)
    # Card bg
    add_rounded_rect(slide_c, cx, card_y, card_w, card_h,
                      fill_color=C_LIGHT_GRAY, line_color=color,
                      line_width_pt=1.5)
    # Color header
    add_rounded_rect(slide_c, cx, card_y, card_w, Inches(0.7),
                      fill_color=color)
    # Weight
    add_textbox(slide_c, cx, card_y + Inches(0.03),
                card_w, Inches(0.25),
                weight, font_size=18, bold=True,
                color=C_WHITE, align=PP_ALIGN.CENTER)
    # Axis name
    add_textbox(slide_c, cx + Inches(0.05), card_y + Inches(0.27),
                card_w - Inches(0.1), Inches(0.4),
                name, font_size=9, bold=True,
                color=C_WHITE, align=PP_ALIGN.CENTER)
    # Description
    add_textbox(slide_c, cx + Inches(0.05), card_y + Inches(0.75),
                card_w - Inches(0.1), Inches(1.2),
                desc, font_size=7.5, bold=False, color=C_TEXT_DARK,
                align=PP_ALIGN.LEFT)
    # Highlight
    add_rect(slide_c, cx + Inches(0.05), card_y + Inches(2.0),
             card_w - Inches(0.1), Inches(0.02),
             fill_color=color)
    add_textbox(slide_c, cx + Inches(0.05), card_y + Inches(2.05),
                card_w - Inches(0.1), Inches(0.5),
                highlight, font_size=7.5, bold=True, color=color,
                align=PP_ALIGN.LEFT)

# Footer
add_textbox(slide_c, 0, H - Inches(0.3), W, Inches(0.28),
            "L&T Aerospace Synthetic Data POC  ·  March 2026",
            font_size=8, color=C_MED_GRAY, align=PP_ALIGN.CENTER)

print("  Done.")


# ─────────────────────────────────────────────────────────────────────────────
# NEW SLIDE D: Model Benchmarking Deep-Dive (insert after slide C)
# ─────────────────────────────────────────────────────────────────────────────
print("\nBuilding NEW SLIDE D: 9-Model Benchmarking...")
slide_d = make_blank_slide(prs)
slide_header(slide_d,
             "9-Model Systematic Benchmarking: 92 Experimental Runs",
             "Every model evaluated with Optuna HPO across 3 seeds and 4 dataset sizes")

# Model table data
models = [
    # (name, type, tier, composite, tstr, mmd, auc, verdict)
    ("KDE",          "Non-parametric",   "TIER 1 — PRODUCTION",  "0.9965", "1.000", "0.0003", "0.478", "RECOMMENDED"),
    ("GMM",          "Parametric",       "TIER 1 — PRODUCTION",  "0.8534", "0.991", "0.0007", "0.451", "RECOMMENDED"),
    ("Copula",       "Statistical",      "TIER 1 — PRODUCTION",  "0.8309", "0.982", "0.0013", "0.518", "RECOMMENDED"),
    ("TabuDiff",     "Diffusion",        "TIER 2 — RESEARCH",    "0.8231", "0.761", "0.0207", "0.722", "ACCEPTABLE"),
    ("TabuDiffPrem", "Diffusion (ext)",  "TIER 2 — RESEARCH",    "0.7612", "0.712", "0.0340", "0.895", "CAUTION"),
    ("TVAE",         "VAE",              "TIER 3 — NOT REC.",    "0.5510", "0.333", "0.0890", "0.999", "MEMORIZATION"),
    ("TVAEPremium",  "VAE (ext)",        "TIER 3 — NOT REC.",    "0.5220", "0.310", "0.1200", "1.000", "MEMORIZATION"),
    ("CTGANPremium", "Conditional GAN",  "TIER 3 — NOT REC.",    "0.5040", "0.330", "0.1100", "0.995", "MEMORIZATION"),
    ("MaskedPred.",  "ML-based",         "TIER 3 — NOT REC.",    "0.4810", "0.280", "0.1350", "0.976", "MEMORIZATION"),
]

# Table header
cols = ["Model", "Type", "Tier", "Composite", "TSTR F1", "MMD", "AUC", "Verdict"]
col_xs = [Inches(0.25), Inches(1.35), Inches(2.35), Inches(3.85), Inches(4.7), Inches(5.55), Inches(6.4), Inches(7.3)]
col_ws = [Inches(1.05), Inches(0.95), Inches(1.45), Inches(0.8),  Inches(0.8), Inches(0.8), Inches(0.85), Inches(2.45)]
hdr_y  = Inches(1.25)
hdr_h  = Inches(0.3)

add_rect(slide_d, Inches(0.2), hdr_y, Inches(9.6), hdr_h,
          fill_color=C_DARK_NAVY)
for j, (col, cx) in enumerate(zip(cols, col_xs)):
    add_textbox(slide_d, cx, hdr_y + Inches(0.03), col_ws[j], hdr_h - Inches(0.05),
                col, font_size=9, bold=True, color=C_WHITE,
                align=PP_ALIGN.CENTER)

# Rows
row_h = Inches(0.36)
for i, row in enumerate(models):
    ry = hdr_y + hdr_h + i * row_h
    bg = C_WHITE if i % 2 == 0 else C_LIGHT_GRAY
    add_rect(slide_d, Inches(0.2), ry, Inches(9.6), row_h, fill_color=bg)

    name, mtype, tier, comp, tstr, mmd, auc, verdict = row

    # Tier color
    if "TIER 1" in tier:
        tier_color = RGBColor(0x27,0xAE,0x60)
        tier_bg = RGBColor(0xD5,0xF5,0xE3)
    elif "TIER 2" in tier:
        tier_color = C_ORANGE
        tier_bg = RGBColor(0xFD,0xF2,0xE8)
    else:
        tier_color = C_RED
        tier_bg = RGBColor(0xFD,0xED,0xEC)

    for j, (val, cx) in enumerate(zip(row, col_xs)):
        if j == 0:  # Model name - bold
            clr = C_DARK_NAVY
            bld = True
        elif j == 2:  # Tier
            clr = tier_color
            bld = True
        elif j == 7:  # Verdict
            clr = tier_color
            bld = True
        else:
            clr = C_TEXT_DARK
            bld = False
        add_textbox(slide_d, cx + Inches(0.03), ry + Inches(0.05),
                    col_ws[j] - Inches(0.06), row_h - Inches(0.08),
                    val, font_size=8.5, bold=bld, color=clr,
                    align=PP_ALIGN.CENTER if j > 0 else PP_ALIGN.LEFT)

# Note
add_textbox(slide_d, Inches(0.25), Inches(5.05), Inches(9.5), Inches(0.3),
            "Memorization = Discriminator AUC near 1.0 (model generates copies of training data, not novel samples). "
            "TVAE/CTGAN/TabuDiffPremium confirmed as memorizers.",
            font_size=8, bold=False, color=C_MED_GRAY, align=PP_ALIGN.LEFT)

# Footer
add_textbox(slide_d, 0, H - Inches(0.3), W, Inches(0.28),
            "L&T Aerospace Synthetic Data POC  ·  March 2026",
            font_size=8, color=C_MED_GRAY, align=PP_ALIGN.CENTER)

print("  Done.")


# ─────────────────────────────────────────────────────────────────────────────
# Reorder slides: new slides A, B, C, D inserted after slide 3 (index 2)
# python-pptx doesn't expose slide ordering — use XML manipulation
# ─────────────────────────────────────────────────────────────────────────────
print("\nReordering slides: moving new slides to positions 4-7...")
def _get_slide_element(prs, idx):
    """Get the sldIdLst element"""
    pass  # placeholder, not actually needed

from pptx.oxml.ns import nsmap
from copy import deepcopy

def reorder_slides(prs, new_order):
    """
    Reorder slides by index in new_order list.
    new_order is a list of slide indices (0-based) in the desired order.
    """
    slide_id_list = prs.slides._sldIdLst

    # Get all sldId elements
    sldIds = list(slide_id_list)

    # Check count matches
    assert len(new_order) == len(sldIds), \
        f"Order list ({len(new_order)}) != slide count ({len(sldIds)})"

    # Clear the list
    for sldId in sldIds:
        slide_id_list.remove(sldId)

    # Re-add in new order
    for idx in new_order:
        slide_id_list.append(sldIds[idx])

# Total slides: original 28 + 4 new = 32
# New order:
# 0  = slide 1 (original title)
# 1  = slide 2 (client asked)
# 2  = slide 3 (pipeline)
# 3  = NEW slide A (full process flow)
# 4  = NEW slide B (physics features)
# 5  = NEW slide C (6-axis evaluation)
# 6  = NEW slide D (9-model benchmarking)
# 7  = slide 4 (min bar)
# ... rest follow

new_order = list(range(0, 3)) + list(range(28, 32)) + list(range(3, 28))
print(f"  New order: {len(new_order)} slides")
reorder_slides(prs, new_order)
print("  Done.")

# ── Update slide 1 (Title) — remove emoji in footer if any ─────────────────
print("\nUpdating title slide footer...")
slide1 = prs.slides[0]
for shape in slide1.shapes:
    if shape.has_text_frame:
        for para in shape.text_frame.paragraphs:
            for run in para.runs:
                run.text = replace_emoji_text(run.text)

# ── Save ─────────────────────────────────────────────────────────────────────
output_path = 'LnT_Aerospace_Synthetic_Data_POC_v4.pptx'
print(f"\nSaving as {output_path}...")
prs.save(output_path)
print(f"Saved: {output_path}")
print(f"Total slides: {len(prs.slides)}")
print("DONE!")
