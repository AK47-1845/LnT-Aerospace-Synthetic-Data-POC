"""
Genesis of Physical AI — Premium PPTX Builder
Uses matplotlib to render all LaTeX math as high-res PNG images,
then embeds them into fully custom-designed slides with:
  - Deep navy/black gradient theme
  - Gold accent color (#C9A84C)
  - Custom typography sizing via pptx
  - Proper layout zones: no text overflow
  - Speaker notes on every slide
"""

import io, os, sys
import collections
import collections.abc

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Inches, Pt
import copy
from lxml import etree

OUTPUT = r"c:\Users\k18ka\Downloads\Genuity IO all documents\LTTS\Genesis_of_Physical_AI_v2.pptx"
MATH_DIR = r"c:\Users\k18ka\Downloads\Genuity IO all documents\LTTS\math_imgs"
os.makedirs(MATH_DIR, exist_ok=True)

# ── Palette ──────────────────────────────────────────────────────────────────
BG_DARK      = RGBColor(0x07, 0x0D, 0x1A)   # deep navy
BG_CARD      = RGBColor(0x0E, 0x1A, 0x2E)   # card surface
GOLD         = RGBColor(0xC9, 0xA8, 0x4C)   # accent gold
WHITE        = RGBColor(0xFF, 0xFF, 0xFF)
LIGHT_GREY   = RGBColor(0xB0, 0xBC, 0xD4)
DIVIDER      = RGBColor(0xC9, 0xA8, 0x4C)
CYAN         = RGBColor(0x4D, 0xD0, 0xE1)

SLIDE_W = Inches(13.33)
SLIDE_H = Inches(7.5)

# ── Slide factory ─────────────────────────────────────────────────────────────
prs = Presentation()
prs.slide_width  = SLIDE_W
prs.slide_height = SLIDE_H

blank_layout = prs.slide_layouts[6]   # completely blank

def new_slide():
    return prs.slides.add_slide(blank_layout)

# ── Drawing helpers ───────────────────────────────────────────────────────────
def fill_bg(slide, color=BG_DARK):
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = color

def add_rect(slide, l, t, w, h, fill_color, alpha=None):
    shape = slide.shapes.add_shape(
        1,   # MSO_SHAPE_TYPE.RECTANGLE
        Inches(l), Inches(t), Inches(w), Inches(h)
    )
    shape.line.fill.background()
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    return shape

def add_textbox(slide, l, t, w, h, text, font_size, bold=False,
                color=WHITE, align=PP_ALIGN.LEFT, italic=False, wrap=True):
    txBox = slide.shapes.add_textbox(
        Inches(l), Inches(t), Inches(w), Inches(h)
    )
    tf = txBox.text_frame
    tf.word_wrap = wrap
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.size  = Pt(font_size)
    run.font.bold  = bold
    run.font.italic = italic
    run.font.color.rgb = color
    return txBox

def add_multiline_textbox(slide, l, t, w, h, lines, font_size,
                          color=LIGHT_GREY, line_spacing_pt=2, title_line=None):
    """lines = list of (text, bold, color, indent_level)"""
    txBox = slide.shapes.add_textbox(
        Inches(l), Inches(t), Inches(w), Inches(h)
    )
    tf = txBox.text_frame
    tf.word_wrap = True
    first = True
    for (text, bold, clr, lvl) in lines:
        if first:
            p = tf.paragraphs[0]
            first = False
        else:
            p = tf.add_paragraph()
        p.level = lvl
        p.space_before = Pt(line_spacing_pt)
        run = p.add_run()
        run.text = text
        run.font.size = Pt(font_size)
        run.font.bold = bold
        run.font.color.rgb = clr
    return txBox

def add_image_from_bytes(slide, img_bytes, l, t, w, h):
    img_stream = io.BytesIO(img_bytes)
    slide.shapes.add_picture(img_stream, Inches(l), Inches(t), Inches(w), Inches(h))

def set_notes(slide, text):
    notes_slide = slide.notes_slide
    tf = notes_slide.notes_text_frame
    tf.text = text

def gold_divider(slide, t, width=13.0, left=0.165):
    """Thin gold horizontal rule"""
    bar = slide.shapes.add_shape(1,
        Inches(left), Inches(t), Inches(width), Inches(0.04))
    bar.fill.solid()
    bar.fill.fore_color.rgb = GOLD
    bar.line.fill.background()

def module_badge(slide, text, l=0.2, t=0.2):
    badge = slide.shapes.add_shape(1,
        Inches(l), Inches(t), Inches(2.6), Inches(0.32))
    badge.fill.solid()
    badge.fill.fore_color.rgb = GOLD
    badge.line.fill.background()
    tf = badge.text_frame
    tf.word_wrap = False
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    run = p.add_run()
    run.text = text.upper()
    run.font.size = Pt(9)
    run.font.bold = True
    run.font.color.rgb = BG_DARK

# ── Math image renderer ───────────────────────────────────────────────────────
def render_latex(latex_str, filename, fontsize=18, dpi=220, bg='#070D1A', fg='white'):
    """Render a LaTeX string to a tight PNG, return bytes."""
    fig = plt.figure(figsize=(0.01, 0.01))
    fig.patch.set_facecolor(bg)
    text = fig.text(0, 0, f'${latex_str}$', fontsize=fontsize,
                    color=fg, usetex=False,
                    math_fontfamily='dejavusans')
    # measure and resize
    renderer = fig.canvas.get_renderer()
    bbox = text.get_window_extent(renderer=renderer)
    pad = 12
    w_in = (bbox.width  + pad*2) / dpi
    h_in = (bbox.height + pad*2) / dpi
    fig.set_size_inches(max(w_in, 0.5), max(h_in, 0.3))
    text.set_position((pad/fig.get_window_extent().width,
                       pad/fig.get_window_extent().height))

    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=dpi,
                facecolor=bg, bbox_inches='tight', pad_inches=pad/dpi)
    plt.close(fig)
    buf.seek(0)
    return buf.read()


# ═══════════════════════════════════════════════════════════════════════════════
#  SLIDE DEFINITIONS
# ═══════════════════════════════════════════════════════════════════════════════

# ── SLIDE 1: Title ─────────────────────────────────────────────────────────────
def slide_01():
    s = new_slide()
    fill_bg(s)

    # left accent bar
    bar = s.shapes.add_shape(1, Inches(0), Inches(0), Inches(0.12), Inches(7.5))
    bar.fill.solid(); bar.fill.fore_color.rgb = GOLD; bar.line.fill.background()

    # decorative right circle (subtle)
    circ = s.shapes.add_shape(9,   # oval
        Inches(9.5), Inches(-1.2), Inches(5.5), Inches(5.5))
    circ.fill.solid(); circ.fill.fore_color.rgb = RGBColor(0x0E,0x1A,0x2E)
    circ.line.color.rgb = GOLD; circ.line.width = Pt(1.5)

    # tag
    module_badge(s, "CONFIDENTIAL — BOARD BRIEFING", l=0.3, t=0.28)

    # main title
    add_textbox(s, 0.35, 1.15, 8.8, 1.5,
        "The Genesis of Physical", 14, bold=False, color=LIGHT_GREY)
    add_textbox(s, 0.35, 1.55, 9.5, 2.0,
        "Artificial Intelligence", 54, bold=True, color=WHITE)

    gold_divider(s, 3.75, width=9.0, left=0.35)

    add_textbox(s, 0.35, 3.95, 9.5, 0.55,
        "Strategic Briefing  ·  The $100M Deployment Architecture", 18,
        color=GOLD, bold=False)

    add_textbox(s, 0.35, 6.8, 6.0, 0.5,
        "August 2026  ·  Confidential & Proprietary", 11,
        color=LIGHT_GREY, bold=False)

    set_notes(s, "Good morning. We are at a structural inflection point in the global economy. For the past five years, AI has been confined to the screen. Today, we are bringing it into the physical world. This briefing outlines the exact mathematical and commercial architecture we will use to deploy physical AI at industrial scale.")
    return s

# ── SLIDE 2: Macro-Economic Surge ─────────────────────────────────────────────
def slide_02():
    s = new_slide(); fill_bg(s)
    module_badge(s, "Module 1 · The AI Paradigm")
    add_textbox(s, 0.3, 0.62, 12.5, 1.0,
        "The Macro-Economic Surge", 34, bold=True, color=WHITE)
    add_textbox(s, 0.3, 1.42, 12.5, 0.45,
        "A Half-Trillion Dollar Supercycle and the Fragile Trust Paradox", 16,
        color=GOLD, bold=False)
    gold_divider(s, 1.96)

    # 3 hero number cards
    cards = [
        (">$512B",  "Worldwide AI Spend 2027",   0.3),
        ("88%",     "Adopters with Revenue Gains",4.6),
        ("87%",     "Adopters with Cost Savings", 8.9),
    ]
    for val, label, lft in cards:
        add_rect(s, lft, 2.15, 4.0, 1.55, BG_CARD)
        add_textbox(s, lft+0.15, 2.25, 3.7, 0.9,
            val, 42, bold=True, color=GOLD, align=PP_ALIGN.CENTER)
        add_textbox(s, lft+0.1, 3.05, 3.8, 0.55,
            label, 13, bold=False, color=LIGHT_GREY, align=PP_ALIGN.CENTER)

    # Insight block
    add_rect(s, 0.3, 3.9, 12.7, 2.0, BG_CARD)
    lines = [
        ("⚠  The Fragile Trust Paradox", True, GOLD, 0),
        ("Massive capital deployment coexists with systems that still fail basic logical tasks in physical space.", False, LIGHT_GREY, 0),
        ("2/3 of enterprises report productivity gains — yet only 1/3 are reimagining business processes.", False, LIGHT_GREY, 0),
        ("Individual AI adoption is outpacing enterprise governance. Shadow IT is expanding unchecked.", False, LIGHT_GREY, 0),
    ]
    add_multiline_textbox(s, 0.5, 3.98, 12.3, 1.88, lines, 13.5, line_spacing_pt=3)

    set_notes(s, "The capital expenditure supercycle behind AI is unprecedented. But we are currently operating under 'fragile trust.' Enterprises are buying in, but these systems still unpredictably fail in physical space. The market will disproportionately reward whoever bridges this gap with verifiable capability.")
    return s

# ── SLIDE 3: Four Epochs ──────────────────────────────────────────────────────
def slide_03():
    s = new_slide(); fill_bg(s)
    module_badge(s, "Module 1 · The AI Paradigm")
    add_textbox(s, 0.3, 0.62, 12.5, 1.0,
        "The Four Epochs of Machine Intelligence", 32, bold=True, color=WHITE)
    add_textbox(s, 0.3, 1.42, 12.5, 0.4,
        "From Static Pattern Recognition to Embodied Physical AI", 16, color=GOLD)
    gold_divider(s, 1.92)

    epochs = [
        ("01", "pre-2018", "Supervised\nDiscriminative", "Human-annotated labels.\nBottleneck: labeling cost.", False),
        ("02", "2018–2023","Autoregressive\nPretraining",  "Raw internet text.\nBottleneck: data & compute.", False),
        ("03", "2023–2025","Test-Time\nReasoning",         "Monte Carlo Tree Search.\nBottleneck: inference cost.", False),
        ("04", "2025–Now", "Embodied\nPhysical AI",        "3D simulation & interaction.\nBottleneck: verified data.", True),
    ]
    connector_t = 4.05
    for i, (num, era, title, detail, highlight) in enumerate(epochs):
        lft = 0.3 + i * 3.25
        card_color = RGBColor(0x1A,0x2A,0x10) if highlight else BG_CARD
        add_rect(s, lft, 2.1, 3.0, 3.8, card_color)
        if highlight:
            # gold left border
            add_rect(s, lft, 2.1, 0.06, 3.8, GOLD)
        num_color = GOLD if highlight else LIGHT_GREY
        add_textbox(s, lft+0.12, 2.22, 2.8, 0.5,
            num, 28, bold=True, color=num_color)
        add_textbox(s, lft+0.12, 2.72, 2.8, 0.32,
            era, 10.5, bold=False, color=LIGHT_GREY)
        title_col = WHITE
        add_textbox(s, lft+0.12, 3.1, 2.78, 0.72,
            title, 14, bold=True, color=title_col)
        add_textbox(s, lft+0.12, 3.85, 2.78, 1.8,
            detail, 12, bold=False, color=LIGHT_GREY)
        # connector arrow (except last)
        if i < 3:
            arr = s.shapes.add_shape(1,
                Inches(lft+3.0), Inches(3.75), Inches(0.26), Inches(0.08))
            arr.fill.solid(); arr.fill.fore_color.rgb = GOLD
            arr.line.fill.background()

    add_textbox(s, 0.3, 6.1, 12.7, 0.5,
        "★  Epoch 4 is the absolute frontier — where the remaining marginal intelligence capability lives.",
        12.5, bold=True, color=GOLD)

    set_notes(s, "To understand where we are investing, we must trace how the learning signal has evolved. We have moved from human labels, to internet text, to inference-time reasoning. We are now entering the fourth epoch: Embodied Physical AI. Each epoch absorbed the previous one. Physical AI is the frontier.")
    return s

# ── SLIDE 4: Scaling Laws & Data Exhaustion ───────────────────────────────────
def slide_04():
    s = new_slide(); fill_bg(s)
    module_badge(s, "Module 1 · The AI Paradigm")
    add_textbox(s, 0.3, 0.62, 12.5, 0.9,
        "The Data Exhaustion Crisis & Compute Wall", 32, bold=True, color=WHITE)
    add_textbox(s, 0.3, 1.42, 12.5, 0.4,
        "The Structural Constraints of Autoregressive Pretraining", 16, color=GOLD)
    gold_divider(s, 1.92)

    # Left: equation block
    add_rect(s, 0.3, 2.1, 5.8, 1.85, BG_CARD)
    add_textbox(s, 0.45, 2.18, 5.5, 0.38,
        "KAPLAN / CHINCHILLA SCALING LAW", 9.5, bold=True, color=GOLD)
    eq = render_latex(r"L(N,D)=E+\frac{A}{N^{\alpha}}+\frac{B}{D^{\beta}}", "eq_scaling", fontsize=22)
    add_image_from_bytes(s, eq, 0.55, 2.65, 5.2, 1.05)
    add_textbox(s, 0.45, 3.62, 5.5, 0.38,
        "E = irreducible entropy floor  ·  N = parameters  ·  D = tokens", 10, color=LIGHT_GREY)

    # right: bullets
    lines = [
        ("Data Exhaustion", True, GOLD, 0),
        ("Public internet text (~10¹⁴ tokens) will be fully consumed between 2027–2028.", False, LIGHT_GREY, 0),
        ("", False, WHITE, 0),
        ("The Compute Wall", True, GOLD, 0),
        ("Gigawatt-scale grid constraints cap hardware acceleration.", False, LIGHT_GREY, 0),
        ("Growth decelerates: 10×/yr  →  3–4×/yr by 2028.", False, LIGHT_GREY, 0),
        ("", False, WHITE, 0),
        ("Strategic Implication", True, CYAN, 0),
        ("Progress migrates from compute-bound to data-bound & verification-bound.", False, LIGHT_GREY, 0),
        ("Proprietary, physics-verified data becomes the primary capability lever.", False, LIGHT_GREY, 0),
    ]
    add_multiline_textbox(s, 6.4, 2.1, 6.7, 5.2, lines, 13.5, line_spacing_pt=3)

    # bottom bar
    add_rect(s, 0.3, 6.05, 12.7, 0.85, BG_CARD)
    add_textbox(s, 0.5, 6.12, 12.3, 0.7,
        "The irreducible floor E does not move with scale. The only lever remaining is proprietary, physics-verified data.", 13,
        bold=True, color=WHITE)

    set_notes(s, "The assumption that sheer scale yields general intelligence is mathematically breaking down. The irreducible entropy floor E does not move. We are literally running out of internet text. The lever for future capability is no longer raw pretraining capital — it is proprietary, physics-verified data.")
    return s

# ── SLIDE 5: Train-to-Test Scaling ────────────────────────────────────────────
def slide_05():
    s = new_slide(); fill_bg(s)
    module_badge(s, "Module 1 · The AI Paradigm")
    add_textbox(s, 0.3, 0.62, 12.5, 0.9,
        "The Shift to Train-to-Test Scaling", 32, bold=True, color=WHITE)
    add_textbox(s, 0.3, 1.42, 12.5, 0.4,
        "Unifying the Compute Budget — System 1 vs. System 2 Reasoning", 16, color=GOLD)
    gold_divider(s, 1.92)

    # Equation
    add_rect(s, 0.3, 2.1, 12.7, 1.7, BG_CARD)
    add_textbox(s, 0.5, 2.18, 12.0, 0.35,
        "UNIFIED COMPUTE BUDGET", 9.5, bold=True, color=GOLD)
    eq = render_latex(
        r"C_{\mathrm{total}}=C_{\mathrm{train}}+C_{\mathrm{infer}}=6ND+2N_{\mathrm{active}}\sum_{q,k}T_{q,k}",
        "eq_compute", fontsize=20)
    add_image_from_bytes(s, eq, 1.5, 2.58, 10.0, 0.95)

    # Two columns
    for lft, title, points in [
        (0.3, "System 1 — Reflexive", [
            "Single forward pass",
            "Fast & cheap at inference time",
            "Brittle: fails outside training distribution",
            "Status: Commoditizing rapidly",
        ]),
        (6.85, "System 2 — Deliberative", [
            "Monte Carlo Tree Search",
            "Process Reward Models",
            "Backtracking & self-correction",
            "Status: The defensible frontier",
        ]),
    ]:
        add_rect(s, lft, 4.0, 6.2, 2.8, BG_CARD)
        title_col = LIGHT_GREY if "Reflexive" in title else GOLD
        add_textbox(s, lft+0.15, 4.08, 5.9, 0.45, title, 15, bold=True, color=title_col)
        for i, pt in enumerate(points):
            add_textbox(s, lft+0.25, 4.62+i*0.48, 5.8, 0.44,
                f"·  {pt}", 13, bold=False, color=LIGHT_GREY)

    add_textbox(s, 0.3, 6.95, 12.7, 0.45,
        "Raw intelligence cost is deflating >90% annually. The moat is not the largest model — it is proprietary verified data.",
        12.5, bold=True, color=CYAN)

    set_notes(s, "The industry has unified pretraining and test-time execution under a single compute budget. We are moving away from massive sluggish models to heavily overtrained systems that deliberate at inference time — System 2 reasoning. Raw intelligence is commoditizing. The defensible moat is proprietary, physically verified data.")
    return s

# ── SLIDE 6: Sector Impact ────────────────────────────────────────────────────
def slide_06():
    s = new_slide(); fill_bg(s)
    module_badge(s, "Module 1 · The AI Paradigm")
    add_textbox(s, 0.3, 0.62, 12.5, 0.9,
        "Cross-Industry Sector Impact", 32, bold=True, color=WHITE)
    add_textbox(s, 0.3, 1.42, 12.5, 0.4,
        "Quantifying the ROI of Task-Level Automation", 16, color=GOLD)
    gold_divider(s, 1.92)

    sectors = [
        ("55.8%",  "Task Acceleration",   "Software Engineering",
         "Closed-loop verifiability via compilers delivers instant reward signals.", CYAN),
        ("2.6×",   "Industry Avg Spend",  "Financial Services",
         "High-volume, structured transaction automation leads adoption.", GOLD),
        ("70%",    "Cycle Time Reduction","Healthcare & Drug Discovery",
         "AI cuts lead-optimization cycle time for early-stage drug candidates.", CYAN),
        ("80%",    "Setup Time Saved",    "Manufacturing & Physical AI",
         "Simulation collapses industrial pilot setup time. 80% penetration by 2027.", GOLD),
    ]
    for i, (metric, label, sector, detail, accent) in enumerate(sectors):
        col = i % 2; row = i // 2
        lft = 0.3 + col * 6.52
        top = 2.12 + row * 2.5
        add_rect(s, lft, top, 6.2, 2.32, BG_CARD)
        add_rect(s, lft, top, 0.08, 2.32, accent)
        add_textbox(s, lft+0.18, top+0.12, 5.9, 0.72,
            metric, 42, bold=True, color=accent)
        add_textbox(s, lft+0.18, top+0.82, 5.9, 0.35,
            label.upper(), 9, bold=True, color=LIGHT_GREY)
        add_textbox(s, lft+0.18, top+1.18, 5.9, 0.38,
            sector, 14, bold=True, color=WHITE)
        add_textbox(s, lft+0.18, top+1.58, 5.9, 0.65,
            detail, 12, bold=False, color=LIGHT_GREY)

    add_textbox(s, 0.3, 7.1, 12.7, 0.32,
        "Projected GDP uplift: $15.7 Trillion by 2030  (McKinsey Global Institute)",
        12, bold=False, color=LIGHT_GREY, align=PP_ALIGN.CENTER)

    set_notes(s, "The economic impact is staggering — $15.7 trillion GDP uplift by 2030. The impact is highest where closed-loop verifiability exists: Software Engineering and Manufacturing. If the code compiles or the robot picks up the part correctly, the model gets an unambiguous success signal. This verifiable feedback loop is what we are capitalizing on.")
    return s

# ── SLIDE 7: Causal Ladder ────────────────────────────────────────────────────
def slide_07():
    s = new_slide(); fill_bg(s)
    module_badge(s, "Module 2 · World Models")
    add_textbox(s, 0.3, 0.62, 12.5, 0.9,
        "Beyond the Autoregressive Bottleneck", 32, bold=True, color=WHITE)
    add_textbox(s, 0.3, 1.42, 12.5, 0.4,
        "Grounding AI in Physical Space via Causal Reasoning", 16, color=GOLD)
    gold_divider(s, 1.92)

    # Causal ladder: 3 rungs
    rungs = [
        ("Rung I",   "Association",       "Seeing & Correlating",
         "Language models: P(Y | X)",      "Predict tomorrow's weather from history.", LIGHT_GREY, False),
        ("Rung II",  "Intervention",      "Doing & Observing",
         "Robotics & Control: P(Y | do(X))", "What happens if I apply 15N of torque?", CYAN, True),
        ("Rung III", "Counterfactual",    "Imagining Alternatives",
         "Planning: P(Y_x | X', Y')",      "What would have happened had I acted differently?", GOLD, True),
    ]
    for i, (rung, name, sub, math_label, example, color, required) in enumerate(rungs):
        top = 2.12 + i * 1.6
        add_rect(s, 0.3, top, 7.6, 1.45, BG_CARD)
        if required:
            add_rect(s, 0.3, top, 0.08, 1.45, color)
        add_textbox(s, 0.5, top+0.08, 1.2, 0.38, rung, 10, bold=True, color=color)
        add_textbox(s, 0.5, top+0.45, 3.0, 0.42, name, 18, bold=True, color=WHITE)
        add_textbox(s, 0.5, top+0.90, 3.5, 0.42, sub,  12, bold=False, color=LIGHT_GREY)
        add_textbox(s, 3.8, top+0.45, 4.0, 0.38, math_label, 12, bold=False, color=color)
        add_textbox(s, 3.8, top+0.88, 4.0, 0.42, f"e.g. {example}", 11, bold=False, color=LIGHT_GREY)

    # Right panel: equation + key point
    add_rect(s, 8.2, 2.12, 4.9, 4.85, BG_CARD)
    add_textbox(s, 8.35, 2.22, 4.6, 0.38,
        "CONTINUOUS DYNAMICS FOUNDATION", 9, bold=True, color=GOLD)
    eq = render_latex(r"\frac{dx}{dt}=f(x,u,t)", "eq_dynamics", fontsize=22)
    add_image_from_bytes(s, eq, 8.5, 2.68, 4.4, 1.1)

    add_textbox(s, 8.35, 3.9, 4.6, 0.38,
        "THE CATEGORY ERROR", 10, bold=True, color=CYAN)
    add_textbox(s, 8.35, 4.35, 4.55, 2.5,
        "Deploying text-trained models into factory cells is a fundamental representational failure — not an engineering gap. Language models operate on Rung I. Physical deployment demands Rungs II and III.",
        12.5, bold=False, color=LIGHT_GREY)

    set_notes(s, "A language model can write a fluent paragraph about a wrench slipping off a bolt. But it cannot predict the specific trajectory, torque, and friction required to turn that bolt. Text models are stuck on Rung I. Physical deployment requires Intervention and Counterfactual reasoning based on continuous physical dynamics.")
    return s

# ── SLIDE 8: POMDP Formulation ────────────────────────────────────────────────
def slide_08():
    s = new_slide(); fill_bg(s)
    module_badge(s, "Module 2 · World Models")
    add_textbox(s, 0.3, 0.62, 12.5, 0.9,
        "POMDPs and Latent World Models", 32, bold=True, color=WHITE)
    add_textbox(s, 0.3, 1.42, 12.5, 0.4,
        "The Mathematical Formulation of a Differentiable Physical Surrogate", 16, color=GOLD)
    gold_divider(s, 1.92)

    # POMDP tuple
    add_rect(s, 0.3, 2.1, 12.7, 1.45, BG_CARD)
    add_textbox(s, 0.5, 2.18, 12.2, 0.35,
        "PARTIALLY OBSERVABLE MARKOV DECISION PROCESS", 9.5, bold=True, color=GOLD)
    eq_pomdp = render_latex(
        r"\mathcal{M}=\langle\mathcal{S},\mathcal{A},\mathcal{O},\mathcal{T},\mathcal{E},\mathcal{R},\gamma\rangle",
        "eq_pomdp", fontsize=22)
    add_image_from_bytes(s, eq_pomdp, 1.5, 2.58, 9.8, 0.82)

    # Encoder-Transition-Decoder pipeline
    add_rect(s, 0.3, 3.72, 12.7, 2.05, BG_CARD)
    add_textbox(s, 0.5, 3.80, 12.2, 0.35,
        "ENCODER → TRANSITION → DECODER  (LATENT WORLD MODEL PIPELINE)", 9.5, bold=True, color=CYAN)
    eq_etd = render_latex(
        r"z_t=E_\psi(o_{\leq t},a_{<t})\;\longrightarrow\;\hat{z}_{t+1}\sim\hat{\mathcal{T}}_\theta(\hat{z}_{t+1}|z_t,a_t)\;\longrightarrow\;\hat{o}_{t+1}=D_\phi(\hat{z}_{t+1})",
        "eq_etd", fontsize=16)
    add_image_from_bytes(s, eq_etd, 0.5, 4.22, 12.4, 1.2)

    # Variable legend
    legend = [
        ("z_t  — compressed latent state (reality compressed)", LIGHT_GREY),
        ("T̂_θ  — learned transition model (predicts next latent state given action)", LIGHT_GREY),
        ("D_ϕ  — decoder (reconstructs observable from latent)", LIGHT_GREY),
        ("Thousands of futures simulated per second — no pixel rendering required.", CYAN),
    ]
    for i, (text, color) in enumerate(legend):
        add_textbox(s, 0.5, 5.9+i*0.36, 12.5, 0.35,
            f"·  {text}", 12.5, bold=(color==CYAN), color=color)

    set_notes(s, "Formally, we model physical environments as POMDPs. To make this computationally tractable, world models operate in a compressed latent space. The model compresses a live video feed, predicts what the state will become if it takes an action, and reconstructs that prediction. This allows the system to roll forward thousands of scenarios per second without rendering every pixel.")
    return s

# ── SLIDE 9: Simulative Reasoning — Value Function ────────────────────────────
def slide_09():
    s = new_slide(); fill_bg(s)
    module_badge(s, "Module 2 · World Models")
    add_textbox(s, 0.3, 0.62, 12.5, 0.9,
        "Simulative Reasoning", 36, bold=True, color=WHITE)
    add_textbox(s, 0.3, 1.42, 12.5, 0.4,
        "The Value Function Over Imagined Latent Rollouts", 16, color=GOLD)
    gold_divider(s, 1.92)

    # Main equation — hero
    add_rect(s, 0.3, 2.1, 12.7, 2.1, BG_CARD)
    add_textbox(s, 0.5, 2.18, 12.2, 0.35,
        "VALUE FUNCTION OVER IMAGINED LATENT ROLLOUTS", 9.5, bold=True, color=GOLD)
    eq = render_latex(
        r"V^\pi(z_t)=\mathbb{E}_{\pi,\hat{\mathcal{T}}_\theta}\!\left[\sum_{k=0}^{H}\gamma^k\,\hat{r}_{t+k}+\gamma^{H+1}V^\omega(\hat{z}_{t+H+1})\right]",
        "eq_value", fontsize=22)
    add_image_from_bytes(s, eq, 1.0, 2.55, 11.2, 1.35)

    # Variable decoder grid
    vars = [
        ("V^π(z_t)", "Total expected future reward from latent state z_t"),
        ("γ",        "Discount factor — weights near-term rewards above distant ones"),
        ("ĥ_t+k",    "Predicted reward at step t+k, computed inside the latent simulator"),
        ("H",        "Planning horizon — number of simulated steps before real-world action"),
        ("V^ω",      "Bootstrap value estimator at the end of the imagined rollout"),
    ]
    for i, (var, meaning) in enumerate(vars):
        lft = 0.3 + (i%2)*6.52
        top = 4.35 + (i//2)*0.8
        add_rect(s, lft, top, 6.2, 0.65, BG_CARD)
        add_textbox(s, lft+0.12, top+0.06, 1.4, 0.52, var, 13, bold=True, color=GOLD)
        add_textbox(s, lft+1.55, top+0.06, 4.5, 0.52, meaning, 12.5, color=LIGHT_GREY)

    add_textbox(s, 0.3, 7.05, 12.7, 0.4,
        "Before a robotic arm moves a single millimeter, it has already imagined thousands of futures inside its own simulator.",
        13, bold=True, color=CYAN, align=PP_ALIGN.CENTER)

    set_notes(s, "This equation is the mathematical beating heart of Physical AI. Before a robotic arm moves, it imagines multiple futures. It calculates the expected value of every reward it can obtain across a given time horizon, strictly inside its own internal simulation. This is the definition of simulative reasoning.")
    return s

# ── SLIDE 10: Three Schools of Thought ───────────────────────────────────────
def slide_10():
    s = new_slide(); fill_bg(s)
    module_badge(s, "Module 2 · World Models")
    add_textbox(s, 0.3, 0.62, 12.5, 0.9,
        "The Three Schools of World Modeling", 32, bold=True, color=WHITE)
    add_textbox(s, 0.3, 1.42, 12.5, 0.4,
        "A Comparative Matrix of Dominant Technical Architectures", 16, color=GOLD)
    gold_divider(s, 1.92)

    schools = [
        {
            "num": "School I",
            "name": "Generative\nSimulators",
            "subtitle": "The Renderer School",
            "exemplars": "Sora · Genie · Oasis",
            "core": "Pixel diffusion / autoregressive video generation",
            "strength": "Photorealistic output; captures surface appearance",
            "flaw": "Physics learned only incidentally. High hallucination rate. Executability gap.",
            "verdict": "❌  NOT suitable for industrial deployment",
            "accent": LIGHT_GREY,
            "highlight": False,
        },
        {
            "num": "School II",
            "name": "Latent / JEPA\nModels",
            "subtitle": "The Efficiency School",
            "exemplars": "V-JEPA · DreamerV3",
            "core": "Energy-based latent prediction (no pixel reconstruction)",
            "strength": "High data efficiency. Sub-5ms control latency.",
            "flaw": "Semantic drift over long horizons. Limited 3D geometric awareness.",
            "verdict": "✓  Suitable for low-latency robotic control",
            "accent": CYAN,
            "highlight": False,
        },
        {
            "num": "School III",
            "name": "Spatial /\nEngineered",
            "subtitle": "The Industrial School",
            "exemplars": "Tesla Occ. Nets · NVIDIA Cosmos/Isaac",
            "core": "4D voxel occupancy grids + Physics-Informed Neural Networks",
            "strength": "Explicit physics constraints. Formally verifiable. Zero-shot transfer.",
            "flaw": "High compute overhead. Requires calibrated sensor rigs.",
            "verdict": "★  PRIMARY CHOICE for $100M deployment",
            "accent": GOLD,
            "highlight": True,
        },
    ]

    for i, sch in enumerate(schools):
        lft = 0.22 + i * 4.38
        add_rect(s, lft, 2.1, 4.2, 5.1, BG_CARD)
        if sch["highlight"]:
            add_rect(s, lft, 2.1, 0.08, 5.1, GOLD)
        add_textbox(s, lft+0.18, 2.18, 3.9, 0.32,
            sch["num"], 10, bold=True, color=sch["accent"])
        add_textbox(s, lft+0.18, 2.5, 3.9, 0.75,
            sch["name"], 18, bold=True, color=WHITE)
        add_textbox(s, lft+0.18, 3.22, 3.9, 0.32,
            sch["subtitle"], 11, bold=False, color=sch["accent"])
        add_textbox(s, lft+0.18, 3.58, 3.9, 0.3,
            sch["exemplars"], 11, bold=False, color=LIGHT_GREY)

        for row, (label, key, col) in enumerate([
            ("Core:", "core", LIGHT_GREY),
            ("Strength:", "strength", LIGHT_GREY),
            ("Flaw:", "flaw", LIGHT_GREY),
        ]):
            top = 4.0 + row * 0.72
            add_textbox(s, lft+0.18, top, 0.82, 0.38, label, 10, bold=True, color=sch["accent"])
            add_textbox(s, lft+1.02, top, 3.3, 0.65, sch[key], 11, bold=False, color=col)

        add_rect(s, lft+0.1, 6.62, 4.0, 0.42, BG_DARK)
        v_color = GOLD if sch["highlight"] else (CYAN if "✓" in sch["verdict"] else LIGHT_GREY)
        add_textbox(s, lft+0.15, 6.65, 3.9, 0.38,
            sch["verdict"], 11, bold=True, color=v_color)

    set_notes(s, "There are currently three schools of thought. The Renderer school generates beautiful video but fails at strict physics. The Latent school is highly efficient and built for low-latency robotic control. The Spatial school uses explicitly engineered physics grids. Conflating video generators with engineering-grade world models is a massive strategic error. For $100M industrial deployments, we rely on Schools II and III.")
    return s

# ── SLIDE 11: Failure Modes Part 1 ───────────────────────────────────────────
def slide_11():
    s = new_slide(); fill_bg(s)
    module_badge(s, "Module 2 · World Models")
    add_textbox(s, 0.3, 0.62, 12.5, 0.9,
        "Canonical Failure Modes (Part 1 / 2)", 30, bold=True, color=WHITE)
    add_textbox(s, 0.3, 1.42, 12.5, 0.4,
        "Compounding Drift · The Executability Gap", 16, color=GOLD)
    gold_divider(s, 1.92)

    # FM1
    add_rect(s, 0.3, 2.1, 12.7, 2.4, BG_CARD)
    add_rect(s, 0.3, 2.1, 0.08, 2.4, RGBColor(0xFF,0x4D,0x4D))
    add_textbox(s, 0.5, 2.18, 3.2, 0.38,
        "FAILURE MODE 1", 9.5, bold=True, color=RGBColor(0xFF,0x4D,0x4D))
    add_textbox(s, 0.5, 2.55, 5.0, 0.45,
        "Compounding Autoregressive Drift", 17, bold=True, color=WHITE)
    eq1 = render_latex(
        r"\mathbb{E}\!\left[\|\hat{z}_T - z_T\|\right]\;\leq\;\mathcal{O}(T\cdot\epsilon)",
        "eq_drift", fontsize=20)
    add_image_from_bytes(s, eq1, 0.5, 3.05, 5.5, 0.98)
    add_textbox(s, 6.2, 2.55, 6.6, 1.8,
        "Small single-step errors ε compound multiplicatively over time horizon T. Objects drift, vanish, or are hallucinated into existence. Long-horizon tasks become unreliable without explicit drift correction mechanisms.",
        13, bold=False, color=LIGHT_GREY)

    # FM2
    add_rect(s, 0.3, 4.7, 12.7, 2.4, BG_CARD)
    add_rect(s, 0.3, 4.7, 0.08, 2.4, RGBColor(0xFF,0x8C,0x00))
    add_textbox(s, 0.5, 4.78, 3.2, 0.38,
        "FAILURE MODE 2", 9.5, bold=True, color=RGBColor(0xFF,0x8C,0x00))
    add_textbox(s, 0.5, 5.15, 5.0, 0.45,
        "The Executability Gap", 17, bold=True, color=WHITE)
    eq2 = render_latex(r"F_{\mathrm{contact}}=\mu\,F_N", "eq_coulomb", fontsize=20)
    add_image_from_bytes(s, eq2, 0.5, 5.65, 4.0, 0.98)
    add_textbox(s, 4.8, 5.15, 8.0, 1.8,
        "Perceptual losses (LPIPS, SSIM) reward visual plausibility — not physical validity. Models violate Coulomb contact dynamics. A visually perfect rendered trajectory will shatter a physical component on execution.",
        13, bold=False, color=LIGHT_GREY)

    add_textbox(s, 0.3, 7.18, 12.7, 0.3,
        "Mitigation: Accumulate-and-Filter pipelines + PINN-augmented loss functions  (→ Module 3)",
        12, bold=True, color=CYAN)

    set_notes(s, "We must be brutally honest about where these models fail. Autoregressive drift means small per-step errors compound until the simulation breaks. The Executability Gap means a visually flawless video can still shatter a physical part because the model ignored Coulomb friction.")
    return s

# ── SLIDE 12: Failure Modes Part 2 ───────────────────────────────────────────
def slide_12():
    s = new_slide(); fill_bg(s)
    module_badge(s, "Module 2 · World Models")
    add_textbox(s, 0.3, 0.62, 12.5, 0.9,
        "Canonical Failure Modes (Part 2 / 2)", 30, bold=True, color=WHITE)
    add_textbox(s, 0.3, 1.42, 12.5, 0.4,
        "Perceptual Hallucination · Action Marginalization · Sim-to-Real Gap", 16, color=GOLD)
    gold_divider(s, 1.92)

    fms = [
        {
            "num": "FM 3", "title": "Perceptual Hallucination",
            "eq_str": r"z_q(x)=\arg\min_k\|E(x)-e_k\|_2",
            "eq_name": "eq_hall",
            "detail": "Unfamiliar objects are force-mapped onto the nearest codebook token. The model silently replaces what it cannot recognize, poisoning downstream decisions.",
            "color": RGBColor(0xFF,0x4D,0x4D),
        },
        {
            "num": "FM 4", "title": "Action Marginalization",
            "eq_str": r"\mathbb{E}\!\left[\|\hat{\mathcal{T}}(z,a)-\hat{\mathcal{T}}(z,\mathrm{shuffle}(a))\|^2\right]\to 0",
            "eq_name": "eq_margin",
            "detail": "The model's predictions become invariant to control input — it hallucinates an 'autopilot' sequence and effectively ignores operator commands entirely.",
            "color": RGBColor(0xFF,0x8C,0x00),
        },
        {
            "num": "FM 5", "title": "The Sim-to-Real Gap",
            "eq_str": r"\mathcal{D}_{\mathrm{real}}\neq\mathcal{D}_{\mathrm{sim}}",
            "eq_name": "eq_simreal",
            "detail": "Synthetic data cannot fully replace real data. Sensor noise, contact variability, and long-tail physical phenomena guarantee a distributional gap.",
            "color": RGBColor(0xAA,0x44,0xFF),
        },
    ]
    for i, fm in enumerate(fms):
        top = 2.1 + i * 1.72
        add_rect(s, 0.3, top, 12.7, 1.58, BG_CARD)
        add_rect(s, 0.3, top, 0.08, 1.58, fm["color"])
        add_textbox(s, 0.5, top+0.08, 1.5, 0.32,
            fm["num"], 9.5, bold=True, color=fm["color"])
        add_textbox(s, 0.5, top+0.42, 3.5, 0.42,
            fm["title"], 16, bold=True, color=WHITE)
        eq_img = render_latex(fm["eq_str"], fm["eq_name"], fontsize=16)
        add_image_from_bytes(s, eq_img, 0.5, top+0.9, 5.6, 0.55)
        add_textbox(s, 6.2, top+0.22, 6.6, 1.25,
            fm["detail"], 13, bold=False, color=LIGHT_GREY)

    add_textbox(s, 0.3, 7.22, 12.7, 0.28,
        "Every failure mode has a quantitative mitigation — no known deployment is beyond engineering control.",
        12, bold=True, color=CYAN)

    set_notes(s, "Furthermore, if an encoder sees an unknown tool, it halluccinates it silently. Action Marginalization means the model ignores human control inputs entirely. And the sim-to-real gap guarantees purely synthetic training is never enough. We must have a hybrid data strategy. Every failure mode has a known engineering mitigation.")
    return s

# ── SLIDE 13: Synthetic Data Taxonomy ────────────────────────────────────────
def slide_13():
    s = new_slide(); fill_bg(s)
    module_badge(s, "Module 3 · Synthetic Data Bridge")
    add_textbox(s, 0.3, 0.62, 12.5, 0.9,
        "Synthetic Data as the Connective Tissue", 32, bold=True, color=WHITE)
    add_textbox(s, 0.3, 1.42, 12.5, 0.4,
        "A Four-Tier Taxonomy: Matching Data Quality to Risk Profile", 16, color=GOLD)
    gold_divider(s, 1.92)

    tiers = [
        ("Tier 1", "Model-Generated Reasoning Traces",
         "Self-play · Tree search · MCTS rollouts",
         "Cost: Low  ·  Physics: None  ·  Use: Reasoning, Q&A, code",
         RGBColor(0x4D,0xD0,0xE1), 2.12),
        ("Tier 2", "Statistically Grounded Tabular Data",
         "Gaussian copulas · DP-GANs · VAE synthesis",
         "Cost: Medium  ·  Physics: Statistical  ·  Use: Finance, EHR, sensor logs",
         CYAN, 3.38),
        ("Tier 3", "Simulated Spatial Telemetry",
         "3D Gaussian Splats · NeRFs · USD Scene Graphs",
         "Cost: High  ·  Physics: Geometric  ·  Use: Autonomous driving, drone nav",
         GOLD, 4.64),
        ("Tier 4", "Formally Verified Data",
         "Lean 4 · SMT solvers · ASIC-grade verification",
         "Cost: Very High  ·  Physics: Certified  ·  Use: Safety-critical industrial AI",
         RGBColor(0xFF,0xD7,0x00), 5.9),
    ]
    for num, name, methods, meta, color, top in tiers:
        add_rect(s, 0.3, top, 12.7, 1.12, BG_CARD)
        add_rect(s, 0.3, top, 0.08, 1.12, color)
        add_textbox(s, 0.5, top+0.05, 1.1, 0.38, num, 12, bold=True, color=color)
        add_textbox(s, 1.65, top+0.05, 6.0, 0.42, name, 15, bold=True, color=WHITE)
        add_textbox(s, 1.65, top+0.52, 5.5, 0.35, methods, 11.5, bold=False, color=LIGHT_GREY)
        add_textbox(s, 8.0, top+0.28, 5.0, 0.55, meta, 11, bold=False, color=color, align=PP_ALIGN.RIGHT)

    add_textbox(s, 0.3, 7.15, 12.7, 0.35,
        "Core Governance: Match the tier to the cost of failure.  Safety-critical = Tier 4 only.",
        13, bold=True, color=CYAN)

    set_notes(s, "Because human data is running out, synthetic data is our connective tissue. But it is not a monolith. It exists on a spectrum from cheap self-play up to ASIC-grade formally verified data. A mature governance strategy does not treat all synthetic data equally — it mandates Tier 4 where failure has human consequences.")
    return s

# ── SLIDE 14: Model Collapse ──────────────────────────────────────────────────
def slide_14():
    s = new_slide(); fill_bg(s)
    module_badge(s, "Module 3 · Synthetic Data Bridge")
    add_textbox(s, 0.3, 0.62, 12.5, 0.9,
        "The Model Collapse Risk & The Accumulate Strategy", 30, bold=True, color=WHITE)
    add_textbox(s, 0.3, 1.42, 12.5, 0.4,
        "The Single Most Important Governance Constraint", 16, color=GOLD)
    gold_divider(s, 1.92)

    # Left — collapse
    add_rect(s, 0.3, 2.1, 6.1, 4.5, BG_CARD)
    add_rect(s, 0.3, 2.1, 0.08, 4.5, RGBColor(0xFF,0x4D,0x4D))
    add_textbox(s, 0.5, 2.18, 5.7, 0.38,
        "⚠  THE COLLAPSE RISK (Replace Strategy)", 11, bold=True, color=RGBColor(0xFF,0x4D,0x4D))
    add_textbox(s, 0.5, 2.65, 5.7, 0.42,
        "Variance Collapse Theorem", 15, bold=True, color=WHITE)
    eq_collapse = render_latex(
        r"\lim_{n\to\infty}\mathrm{Var}[X_n]=0", "eq_collapse", fontsize=22)
    add_image_from_bytes(s, eq_collapse, 0.7, 3.18, 5.2, 1.05)
    add_textbox(s, 0.5, 4.35, 5.7, 2.1,
        "Feeding a model its own unverified output causes its probability distribution to collapse onto its most likely modes.\n\nEdge cases, failure states, and rare but critical scenarios are permanently forgotten.\n\nResult: a confident, high-precision model that is catastrophically brittle.",
        13, bold=False, color=LIGHT_GREY)

    # Right — solution
    add_rect(s, 6.65, 2.1, 6.55, 4.5, BG_CARD)
    add_rect(s, 6.65, 2.1, 0.08, 4.5, GOLD)
    add_textbox(s, 6.85, 2.18, 6.1, 0.38,
        "✓  THE ACCUMULATE-AND-FILTER RESOLUTION", 11, bold=True, color=GOLD)
    add_textbox(s, 6.85, 2.65, 6.1, 0.42,
        "Governed Data Mixture Equation", 15, bold=True, color=WHITE)
    eq_accum = render_latex(
        r"\mathcal{D}_{n+1}=\alpha\mathcal{D}_{\mathrm{real}}+(1-\alpha)\{x\sim G\mid\mathrm{Ver}(x)=\mathsf{T}\}",
        "eq_accum", fontsize=17)
    add_image_from_bytes(s, eq_accum, 6.75, 3.18, 6.3, 1.05)
    add_textbox(s, 6.85, 4.35, 6.1, 2.1,
        "Maintain a strict ratio α between real data and verified synthetic data.\n\nOnly synthetic samples that pass the programmatic Verifier gate are admitted.\n\nα is a board-level governance parameter — not a hyperparameter.",
        13, bold=False, color=LIGHT_GREY)

    set_notes(s, "If you feed a model its own unchecked output, its variance collapses to zero. It forgets reality. To prevent this, we deploy an 'Accumulate-and-Filter' strategy. We maintain a strict mathematical ratio — alpha — between real data and synthetically verified data. This equation is the foundational governance constraint of our entire architecture.")
    return s

# ── SLIDE 15: GRPO ────────────────────────────────────────────────────────────
def slide_15():
    s = new_slide(); fill_bg(s)
    module_badge(s, "Module 3 · Synthetic Data Bridge")
    add_textbox(s, 0.3, 0.62, 12.5, 0.9,
        "Synthetic Reasoning via GRPO", 34, bold=True, color=WHITE)
    add_textbox(s, 0.3, 1.42, 12.5, 0.4,
        "Group Relative Policy Optimization — Scalable Reward Without Human Labels", 16, color=GOLD)
    gold_divider(s, 1.92)

    # Main equation
    add_rect(s, 0.3, 2.1, 12.7, 1.9, BG_CARD)
    add_textbox(s, 0.5, 2.18, 12.2, 0.35,
        "GROUP RELATIVE ADVANTAGE ESTIMATOR", 9.5, bold=True, color=GOLD)
    eq_grpo = render_latex(
        r"A_i=\frac{r_i - \mathrm{mean}(\{r_1,\dots,r_G\})}{\mathrm{std}(\{r_1,\dots,r_G\})}",
        "eq_grpo", fontsize=22)
    add_image_from_bytes(s, eq_grpo, 2.0, 2.58, 9.2, 1.18)

    # 3-step mechanism
    steps = [
        ("01", "Sample Group",
         "Generate G candidate trajectories from the current policy π.", CYAN),
        ("02", "Score via Verifier",
         "A deterministic physics engine / compiler assigns reward r_i to each trajectory — no human graders.", GOLD),
        ("03", "Compute Advantage",
         "Normalize r_i against group mean and std. Train only on relative quality signal. No critic network needed.", CYAN),
    ]
    for i, (num, title, detail, color) in enumerate(steps):
        lft = 0.3 + i * 4.3
        add_rect(s, lft, 4.18, 4.1, 2.6, BG_CARD)
        add_textbox(s, lft+0.15, 4.28, 0.7, 0.55, num, 26, bold=True, color=color)
        add_textbox(s, lft+0.15, 4.85, 3.8, 0.42, title, 15, bold=True, color=WHITE)
        add_textbox(s, lft+0.15, 5.32, 3.8, 1.35, detail, 12.5, bold=False, color=LIGHT_GREY)

    add_textbox(s, 0.3, 6.95, 12.7, 0.45,
        "The model teaches itself — verifiable tasks (robotics, code, physics) provide free, infinite, high-quality training signal.",
        13, bold=True, color=WHITE, align=PP_ALIGN.CENTER)

    set_notes(s, "How do we scale this without human labels? We use Group Relative Policy Optimization. The system generates multiple candidate trajectories. A strict physics engine acts as the verifier, grading them against the group average. The model teaches itself by recognizing which actions outperformed the mean. This is how we achieve massive scale efficiently.")
    return s

# ── SLIDE 16: PINNs ───────────────────────────────────────────────────────────
def slide_16():
    s = new_slide(); fill_bg(s)
    module_badge(s, "Module 3 · Synthetic Data Bridge")
    add_textbox(s, 0.3, 0.62, 12.5, 0.9,
        "Physics-Informed Neural Networks (PINNs)", 32, bold=True, color=WHITE)
    add_textbox(s, 0.3, 1.42, 12.5, 0.4,
        "Enforcing Physical Laws as Hard Constraints During Synthetic Generation", 16, color=GOLD)
    gold_divider(s, 1.92)

    # Main equation
    add_rect(s, 0.3, 2.1, 12.7, 2.1, BG_CARD)
    add_textbox(s, 0.5, 2.18, 12.2, 0.35,
        "PINN AUGMENTED LOSS FUNCTION", 9.5, bold=True, color=GOLD)
    eq_pinn = render_latex(
        r"\mathcal{L}_{\mathrm{total}}=\mathcal{L}_{\mathrm{data}}+\lambda_{\mathrm{pinn}}\left\|\frac{\partial u}{\partial t}+\mathcal{N}[u]-f\right\|^2",
        "eq_pinn", fontsize=22)
    add_image_from_bytes(s, eq_pinn, 1.2, 2.56, 10.8, 1.35)

    # What each term enforces
    terms = [
        ("ℒ_data", "Empirical fit to measured sensor telemetry", LIGHT_GREY),
        ("λ_pinn · ‖…‖²", "Physics residual penalty — forces the model to obey the governing PDE", GOLD),
        ("∂u/∂t", "Time derivative of the physical field (temperature, stress, velocity…)", LIGHT_GREY),
        ("𝒩[u]", "Differential operator encoding physical law (Navier-Stokes, elasticity, thermodynamics)", CYAN),
        ("f",    "Known external forcing term (loads, heat sources, boundary conditions)", LIGHT_GREY),
    ]
    for i, (term, meaning, color) in enumerate(terms):
        lft = 0.5 if i % 2 == 0 else 6.75
        top = 4.35 + (i // 2) * 0.78
        add_rect(s, lft, top, 6.0, 0.65, BG_CARD)
        add_textbox(s, lft+0.12, top+0.08, 2.0, 0.5, term, 13, bold=True, color=color)
        add_textbox(s, lft+2.15, top+0.08, 3.7, 0.52, meaning, 12, bold=False, color=LIGHT_GREY)

    add_textbox(s, 0.3, 7.15, 12.7, 0.35,
        "PINNs close the Executability Gap. Synthetic data generated under PINN constraints obeys the laws of physics — guaranteed.",
        13, bold=True, color=CYAN)

    set_notes(s, "To close the executability gap, we rely on Physics-Informed Neural Networks. By injecting a differential-operator penalty into the loss function, we force the AI's imagination to strictly obey thermodynamics, mass conservation, and momentum. We are not generating convincing video; we are generating verified physics.")
    return s

# ── SLIDE 17: Uncertainty Diagnostics ────────────────────────────────────────
def slide_17():
    s = new_slide(); fill_bg(s)
    module_badge(s, "Module 3 · Synthetic Data Bridge")
    add_textbox(s, 0.3, 0.62, 12.5, 0.9,
        "Real-Time Uncertainty Diagnostics", 32, bold=True, color=WHITE)
    add_textbox(s, 0.3, 1.42, 12.5, 0.4,
        "Production Safety: Managing Hallucination Through Statistical Confidence", 16, color=GOLD)
    gold_divider(s, 1.92)

    # Metric 1
    add_rect(s, 0.3, 2.1, 12.7, 2.4, BG_CARD)
    add_textbox(s, 0.5, 2.18, 7.0, 0.38,
        "METRIC 1 — RECONSTRUCTION RESIDUAL  (Aleatoric / Input Uncertainty)", 9.5, bold=True, color=CYAN)
    eq_recon = render_latex(
        r"\mathcal{E}_{\mathrm{recon}}(x)=\|x-D_\phi(E_\psi(x))\|_2",
        "eq_recon", fontsize=20)
    add_image_from_bytes(s, eq_recon, 0.5, 2.62, 7.0, 1.12)
    add_textbox(s, 7.8, 2.38, 5.0, 1.95,
        "Measures how faithfully the model can reconstruct its own input.\n\nA spike → the system has encountered an out-of-distribution physical configuration.\n\nAction: PAUSE and flag for human review.", 13, bold=False, color=LIGHT_GREY)

    # Metric 2
    add_rect(s, 0.3, 4.65, 12.7, 2.4, BG_CARD)
    add_textbox(s, 0.5, 4.73, 9.0, 0.38,
        "METRIC 2 — INTER-SEED DENOISING VARIANCE  (Epistemic Uncertainty)", 9.5, bold=True, color=GOLD)
    eq_var = render_latex(
        r"\sigma^2_{\mathrm{seed}}(\hat{z}_t)=\frac{1}{S-1}\sum_{s=1}^{S}\|\hat{z}_t^{(s)}-\bar{z}_t\|_2^2",
        "eq_var", fontsize=20)
    add_image_from_bytes(s, eq_var, 0.5, 5.18, 7.8, 1.15)
    add_textbox(s, 9.1, 4.93, 4.0, 1.95,
        "Measures disagreement across independently seeded denoising chains.\n\nA spike → the model is deeply uncertain about the future state.\n\nAction: HALT deployment in this region.", 13, bold=False, color=LIGHT_GREY)

    add_textbox(s, 0.3, 7.18, 12.7, 0.32,
        "These two metrics constitute a real-time safety monitor. The system fails safely — never silently.",
        13, bold=True, color=WHITE)

    set_notes(s, "In a production environment, safety is paramount. We monitor real-time uncertainty using two metrics: Reconstruction Residual and Inter-Seed Denoising Variance. If either spikes, the system pauses and flags the anomaly for review. It fails safely — never silently. This is our assurance framework for the board.")
    return s

# ── SLIDE 18: Closed-Loop Flywheel ────────────────────────────────────────────
def slide_18():
    s = new_slide(); fill_bg(s)
    module_badge(s, "Module 3 · Synthetic Data Bridge")
    add_textbox(s, 0.3, 0.62, 12.5, 0.9,
        "The Closed-Loop Flywheel Architecture", 32, bold=True, color=WHITE)
    add_textbox(s, 0.3, 1.42, 12.5, 0.4,
        "A Co-Development, Federated Data Ecosystem — The Ultimate Competitive Moat", 16, color=GOLD)
    gold_divider(s, 1.92)

    stages = [
        ("01\nTELEMETRY",   "Sparse, real-world\nindustrial sensor data\ningested & cleaned.",        CYAN),
        ("02\nCALIBRATION", "World model latent space\nanchored to real-world\nphysical telemetry.",   GOLD),
        ("03\nGENERATION",  "Large-scale synthetic\nedge cases generated\n& PINN-verified.",           CYAN),
        ("04\nDEPLOYMENT",  "Zero-shot policy\ndeployed to target\nphysical environment.",            GOLD),
        ("05\nFEEDBACK",    "Uncertainty-flagged\noutcomes logged &\nrouted to Stage 01.",            CYAN),
    ]
    for i, (num, detail, color) in enumerate(stages):
        lft = 0.22 + i * 2.6
        add_rect(s, lft, 2.12, 2.44, 3.5, BG_CARD)
        add_rect(s, lft, 2.12, 2.44, 0.08, color)
        add_textbox(s, lft+0.12, 2.22, 2.2, 0.7, num, 12, bold=True, color=color)
        add_textbox(s, lft+0.12, 2.98, 2.2, 1.55, detail, 12.5, bold=False, color=LIGHT_GREY)
        if i < 4:
            arr = s.shapes.add_shape(1,
                Inches(lft+2.44), Inches(3.5), Inches(0.16), Inches(0.08))
            arr.fill.solid(); arr.fill.fore_color.rgb = GOLD
            arr.line.fill.background()

    # Feedback loop arrow description
    add_rect(s, 0.3, 5.8, 12.7, 0.55, BG_CARD)
    add_textbox(s, 0.5, 5.87, 12.3, 0.42,
        "↺  Feedback loop is continuous — every real-world deployment enriches the next training cycle automatically.", 13, bold=True, color=GOLD)

    # Moat statement
    add_rect(s, 0.3, 6.5, 12.7, 0.9, RGBColor(0x10, 0x20, 0x08))
    add_rect(s, 0.3, 6.5, 0.08, 0.9, GOLD)
    add_textbox(s, 0.5, 6.58, 12.3, 0.75,
        "THE MOAT:  Compute is a commodity. This operational data flywheel — built on real industrial execution — is virtually impossible to replicate without years of deployment experience.",
        14, bold=True, color=WHITE)

    set_notes(s, "This is the operational architecture. We take real telemetry, calibrate the world model, generate millions of verified synthetic edge cases, deploy the zero-shot policy, and log the uncertainties to feed back into the loop. This closed-loop flywheel is our ultimate competitive moat. You can buy compute, but you cannot buy this operational data ecosystem.")
    return s

# ── SLIDE 19: Strategic Synthesis ────────────────────────────────────────────
def slide_19():
    s = new_slide(); fill_bg(s)
    # Gold left bar
    bar = s.shapes.add_shape(1, Inches(0), Inches(0), Inches(0.12), Inches(7.5))
    bar.fill.solid(); bar.fill.fore_color.rgb = GOLD; bar.line.fill.background()

    add_textbox(s, 0.35, 0.38, 12.5, 0.38,
        "STRATEGIC SYNTHESIS", 10, bold=True, color=GOLD)
    add_textbox(s, 0.35, 0.75, 12.5, 1.15,
        "Engineering World Models for Physical AI", 40, bold=True, color=WHITE)
    gold_divider(s, 2.0)

    imperatives = [
        ("Engineering over Entertainment",
         "Deploy physics-constrained world models (Schools II & III) — not consumer video generators. Verifiable physical laws are non-negotiable.",
         CYAN),
        ("Automated Verification Pipelines",
         "PINN-augmented synthetic generation automates the cleaning of industrial sensor telemetry and closes the Executability Gap at scale.",
         GOLD),
        ("Mandate the Accumulation Ratio",
         "Enforce α-governed data mixing at the board level. Model collapse is not a hyperparameter risk — it is a governance failure.",
         CYAN),
        ("The Ultimate ROI",
         "Shift CapEx from physical prototyping and manual annotation to scalable, OpEx-driven computational simulation via the closed-loop flywheel.",
         GOLD),
    ]
    for i, (title, detail, color) in enumerate(imperatives):
        top = 2.18 + i * 1.15
        add_rect(s, 0.35, top, 12.65, 1.05, BG_CARD)
        add_rect(s, 0.35, top, 0.08, 1.05, color)
        add_textbox(s, 0.55, top+0.06, 4.2, 0.42, title, 14.5, bold=True, color=WHITE)
        add_textbox(s, 4.85, top+0.06, 8.1, 0.88, detail, 13, bold=False, color=LIGHT_GREY)

    add_textbox(s, 0.35, 6.82, 12.65, 0.58,
        "The future of industry is physical AI. The question is not whether to deploy — it is who deploys it first, and who deploys it right.",
        16, bold=True, color=GOLD, align=PP_ALIGN.CENTER)

    set_notes(s, "To conclude: we are shifting away from physical prototyping to highly scalable, verified computational simulation. We are automating our data pipelines and mandating rigorous physics verification at every step. This architecture accelerates time-to-market and establishes a durable position of technical leadership. This is how we execute the future of physical AI. Thank you.")
    return s

# ═══════════════════════════════════════════════════════════════════════════════
#  BUILD
# ═══════════════════════════════════════════════════════════════════════════════
print("Building slides...")
slide_01()
print("  [1/19] Title")
slide_02()
print("  [2/19] Macro-Economic Surge")
slide_03()
print("  [3/19] Four Epochs")
slide_04()
print("  [4/19] Scaling Laws")
slide_05()
print("  [5/19] Train-to-Test")
slide_06()
print("  [6/19] Sector Impact")
slide_07()
print("  [7/19] Causal Ladder")
slide_08()
print("  [8/19] POMDP")
slide_09()
print("  [9/19] Value Function")
slide_10()
print(" [10/19] Three Schools")
slide_11()
print(" [11/19] Failure Modes 1")
slide_12()
print(" [12/19] Failure Modes 2")
slide_13()
print(" [13/19] Synthetic Taxonomy")
slide_14()
print(" [14/19] Model Collapse")
slide_15()
print(" [15/19] GRPO")
slide_16()
print(" [16/19] PINNs")
slide_17()
print(" [17/19] Uncertainty")
slide_18()
print(" [18/19] Flywheel")
slide_19()
print(" [19/19] Strategic Synthesis")

prs.save(OUTPUT)
print(f"\n✅  Presentation saved to:\n    {OUTPUT}")
