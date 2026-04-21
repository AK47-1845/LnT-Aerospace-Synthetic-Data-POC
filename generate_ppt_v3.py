"""
The Practice of Physical AI — Premium PPTX Builder v3
Complete, exhaustive coverage of the practice briefing document.
Every section, every table, every citation, every formula.

Design: Deep navy/obsidian theme with gold accents, 
        clean typography, card-based layouts, math as PNGs.
Output: Genesis_of_Physical_AI_v3.pptx
"""

import io, os, sys
import collections
import collections.abc

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.oxml.ns import qn
from lxml import etree

OUTPUT = r"c:\Users\k18ka\Downloads\Genuity IO all documents\LTTS\Genesis_of_Physical_AI_v3.pptx"
MATH_DIR = r"c:\Users\k18ka\Downloads\Genuity IO all documents\LTTS\math_imgs"
os.makedirs(MATH_DIR, exist_ok=True)

# ── Palette ──────────────────────────────────────────────────────────────────
BG_DARK      = RGBColor(0x06, 0x0B, 0x18)   # near-black navy
BG_CARD      = RGBColor(0x0D, 0x17, 0x2A)   # card surface
BG_CARD_ALT  = RGBColor(0x10, 0x1E, 0x30)   # lighter card
GOLD         = RGBColor(0xC9, 0xA8, 0x4C)   # accent gold
WHITE        = RGBColor(0xFF, 0xFF, 0xFF)
LIGHT_GREY   = RGBColor(0xAA, 0xB8, 0xD0)
MID_GREY     = RGBColor(0x70, 0x80, 0x9A)
CYAN         = RGBColor(0x4D, 0xD0, 0xE1)
RED_SOFT     = RGBColor(0xFF, 0x5A, 0x5A)
ORANGE_SOFT  = RGBColor(0xFF, 0x99, 0x33)
GREEN_SOFT   = RGBColor(0x4D, 0xE1, 0x8A)
PURPLE_SOFT  = RGBColor(0xAA, 0x66, 0xFF)
BG_GREEN     = RGBColor(0x0A, 0x1A, 0x0A)   # verified highlight bg

SLIDE_W = Inches(13.33)
SLIDE_H = Inches(7.5)

# ── Slide factory ─────────────────────────────────────────────────────────────
prs = Presentation()
prs.slide_width  = SLIDE_W
prs.slide_height = SLIDE_H

blank_layout = prs.slide_layouts[6]

def new_slide():
    return prs.slides.add_slide(blank_layout)

# ── Drawing helpers ───────────────────────────────────────────────────────────
def fill_bg(slide, color=BG_DARK):
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = color

def add_rect(slide, l, t, w, h, fill_color):
    shape = slide.shapes.add_shape(
        1, Inches(l), Inches(t), Inches(w), Inches(h))
    shape.line.fill.background()
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    return shape

def add_textbox(slide, l, t, w, h, text, font_size, bold=False,
                color=WHITE, align=PP_ALIGN.LEFT, italic=False):
    txBox = slide.shapes.add_textbox(
        Inches(l), Inches(t), Inches(w), Inches(h))
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.size  = Pt(font_size)
    run.font.bold  = bold
    run.font.italic = italic
    run.font.color.rgb = color
    return txBox

def add_multiline(slide, l, t, w, h, lines, font_size, line_spacing_pt=2):
    """lines = list of (text, bold, color, indent_level)"""
    txBox = slide.shapes.add_textbox(
        Inches(l), Inches(t), Inches(w), Inches(h))
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

def gold_divider(slide, t, width=12.7, left=0.3):
    bar = slide.shapes.add_shape(1,
        Inches(left), Inches(t), Inches(width), Inches(0.035))
    bar.fill.solid()
    bar.fill.fore_color.rgb = GOLD
    bar.line.fill.background()

def module_badge(slide, text, l=0.25, t=0.22):
    badge = slide.shapes.add_shape(1,
        Inches(l), Inches(t), Inches(2.8), Inches(0.30))
    badge.fill.solid()
    badge.fill.fore_color.rgb = GOLD
    badge.line.fill.background()
    tf = badge.text_frame
    tf.word_wrap = False
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    run = p.add_run()
    run.text = text.upper()
    run.font.size = Pt(8.5)
    run.font.bold = True
    run.font.color.rgb = BG_DARK

def section_divider(slide, module_num, module_name, subtitle):
    """Full-bleed section divider slide"""
    fill_bg(slide)
    bar = slide.shapes.add_shape(1, Inches(0), Inches(0), Inches(0.10), Inches(7.5))
    bar.fill.solid(); bar.fill.fore_color.rgb = GOLD; bar.line.fill.background()
    add_textbox(slide, 0.4, 2.4, 12.0, 0.6,
        f"MODULE {module_num}", 14, bold=True, color=GOLD)
    add_textbox(slide, 0.4, 3.0, 12.0, 1.5,
        module_name, 44, bold=True, color=WHITE)
    gold_divider(slide, 4.6, width=6.0, left=0.4)
    add_textbox(slide, 0.4, 4.8, 12.0, 0.6,
        subtitle, 16, color=LIGHT_GREY)

# ── Math image renderer ───────────────────────────────────────────────────────
def render_latex(latex_str, filename, fontsize=18, dpi=220, bg='#060B18', fg='white'):
    fig = plt.figure(figsize=(0.01, 0.01))
    fig.patch.set_facecolor(bg)
    text = fig.text(0, 0, f'${latex_str}$', fontsize=fontsize,
                    color=fg, usetex=False,
                    math_fontfamily='dejavusans')
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
def slide_01_title():
    s = new_slide(); fill_bg(s)
    bar = s.shapes.add_shape(1, Inches(0), Inches(0), Inches(0.10), Inches(7.5))
    bar.fill.solid(); bar.fill.fore_color.rgb = GOLD; bar.line.fill.background()
    circ = s.shapes.add_shape(9,
        Inches(9.8), Inches(-1.5), Inches(5.5), Inches(5.5))
    circ.fill.solid(); circ.fill.fore_color.rgb = BG_CARD
    circ.line.color.rgb = RGBColor(0x1A,0x2A,0x40); circ.line.width = Pt(1)

    module_badge(s, "Confidential  \u00b7  Strategic Briefing", l=0.35, t=0.3)
    add_textbox(s, 0.4, 1.5, 9.0, 0.5,
        "The Practice of", 15, color=LIGHT_GREY)
    add_textbox(s, 0.4, 1.9, 10.0, 2.0,
        "Physical Artificial\nIntelligence", 50, bold=True, color=WHITE)
    gold_divider(s, 4.1, width=8.0, left=0.4)
    add_textbox(s, 0.4, 4.35, 10.0, 0.5,
        "Landscape, Commercialization, Competition, and the Industrial-AI Bridge", 15,
        color=GOLD)
    add_textbox(s, 0.4, 5.6, 6.0, 0.4,
        "Prepared by Adari Karthikeya", 13, color=LIGHT_GREY)
    add_textbox(s, 0.4, 5.95, 6.0, 0.4,
        "Prepared for Dr. Madhusudhan Singh and Team", 12, color=MID_GREY)
    add_textbox(s, 0.4, 6.28, 6.0, 0.4,
        "L&T Technology Services (LTTS)", 11, color=MID_GREY)
    add_textbox(s, 0.4, 7.0, 6.0, 0.35,
        "September 2026  \u00b7  Confidential & Proprietary", 10, color=MID_GREY)
    set_notes(s, "Opening slide. This briefing provides a comprehensive, rigorously sourced analysis of Physical AI for LTTS leadership.")
    return s

# ── SLIDE 2: Verification Taxonomy ────────────────────────────────────────────
def slide_02_taxonomy():
    s = new_slide(); fill_bg(s)
    module_badge(s, "Research Methodology")
    add_textbox(s, 0.3, 0.6, 12.5, 0.8,
        "Four-Tier Verification Taxonomy", 32, bold=True, color=WHITE)
    add_textbox(s, 0.3, 1.3, 12.5, 0.4,
        "Every Quantitative Claim Is Tagged With Its Evidentiary Basis", 15, color=GOLD)
    gold_divider(s, 1.82)
    tiers = [
        ("[Verified]", "Primary source, SEC/regulatory filing, peer-reviewed paper, or audited corporate disclosure.",
         GREEN_SOFT, BG_GREEN),
        ("[Reported]", "Trade press announcement or company self-reported claim (not independently audited).",
         CYAN, BG_CARD),
        ("[Estimated]", "Directional estimate derived from public comparable benchmarks with explicit methodology.",
         GOLD, BG_CARD),
        ("[Speculative]", "Forward-looking strategic judgment call flagged for executive evaluation.",
         ORANGE_SOFT, BG_CARD_ALT),
    ]
    for i, (tag, desc, color, bg) in enumerate(tiers):
        top = 2.05 + i * 1.28
        add_rect(s, 0.3, top, 12.7, 1.12, bg)
        add_rect(s, 0.3, top, 0.07, 1.12, color)
        add_textbox(s, 0.6, top + 0.12, 2.5, 0.4, tag, 18, bold=True, color=color)
        add_textbox(s, 3.3, top + 0.15, 9.5, 0.85, desc, 14, color=LIGHT_GREY)
    add_textbox(s, 0.3, 7.2, 12.7, 0.3,
        "This taxonomy is applied consistently throughout the briefing to maintain auditability.", 
        12, bold=True, color=GOLD, align=PP_ALIGN.CENTER)
    set_notes(s, "We establish our evidentiary framework upfront. Every number is tagged so Dr. Singh can assess its reliability.")
    return s

# ── SLIDE 3: Executive Summary ─────────────────────────────────────────────────
def slide_03_exec_summary():
    s = new_slide(); fill_bg(s)
    module_badge(s, "Executive Summary")
    add_textbox(s, 0.3, 0.6, 12.5, 0.8,
        "The Core Strategic Thesis", 32, bold=True, color=WHITE)
    add_textbox(s, 0.3, 1.3, 12.5, 0.4,
        "Why LTTS Wins as the Certified Bridge, Not the Foundation Model Player", 15, color=GOLD)
    gold_divider(s, 1.82)
    cards = [
        ("$3.2B+", "VC into humanoid/robotics\nfoundation models (18mo) [Verified]", GREEN_SOFT),
        ("<$20M", "Verified production revenue\nacross humanoid deployments [Estimated]", GOLD),
        ("$6B+", "LTTS market cap as pure-play\nER&D services firm [Verified]", GREEN_SOFT),
    ]
    for i, (val, desc, accent) in enumerate(cards):
        lft = 0.3 + i * 4.3
        add_rect(s, lft, 2.0, 4.1, 1.65, BG_CARD)
        add_rect(s, lft, 2.0, 0.06, 1.65, accent)
        add_textbox(s, lft+0.2, 2.08, 3.7, 0.7, val, 36, bold=True, color=accent, align=PP_ALIGN.CENTER)
        add_textbox(s, lft+0.2, 2.78, 3.7, 0.8, desc, 11.5, color=LIGHT_GREY, align=PP_ALIGN.CENTER)
    add_rect(s, 0.3, 3.85, 12.7, 2.8, BG_CARD)
    add_rect(s, 0.3, 3.85, 0.06, 2.8, GOLD)
    lines = [
        ("The Thesis", True, GOLD, 0),
        ("", False, WHITE, 0),
        ("Physical AI = transition from autoregressive token prediction in static semantic spaces to", False, LIGHT_GREY, 0),
        ("closed-loop causal interaction with continuous physical dynamics.", False, WHITE, 0),
        ("", False, WHITE, 0),
        ("LTTS should NOT manufacture robot hardware or train 50B-parameter foundation models.", False, LIGHT_GREY, 0),
        ("", False, WHITE, 0),
        ("LTTS's durable moat lies in becoming the Certified Systems Integration, V&V, and", False, WHITE, 0),
        ("Synthetic Data Engine that bridges foundation model builders with mission-critical", False, WHITE, 0),
        ("brownfield PLCs, safety interlocks, and regulated industrial plants.", False, GOLD, 0),
    ]
    add_multiline(s, 0.55, 3.95, 12.2, 2.6, lines, 13.5, line_spacing_pt=2)
    set_notes(s, "The central thesis: LTTS cannot win as a foundation model player. The high-conviction path is becoming the certified SI and V&V bridge.")
    return s

# ── SLIDE 4-7: Commercial State ──────────────────────────────────────────────
def slide_04_div():
    s = new_slide()
    section_divider(s, "01", "Commercial\nState Mapping", "Current State of Physical AI: Production Reality vs. Hype")
    set_notes(s, "Section 1: Commercial reality mapping.")
    return s

def slide_05_maturity():
    s = new_slide(); fill_bg(s)
    module_badge(s, "Module 1 \u00b7 Commercial State")
    add_textbox(s, 0.3, 0.6, 12.5, 0.8,
        "Commercial Maturity Tiers", 32, bold=True, color=WHITE)
    add_textbox(s, 0.3, 1.3, 12.5, 0.4,
        "Separating Production Reality from Vendor Marketing", 15, color=GOLD)
    gold_divider(s, 1.82)
    tiers_data = [
        ("Tier 1", "Commercial Production at Scale", GREEN_SOFT, [
            ("Autonomous Driving:", "Waymo 150k+ paid trips/week (Alphabet Q3 2024 Earnings) [Verified]"),
            ("Industrial Inspection:", "TSMC automated defect classification pipelines [Reported]"),
            ("Simulation & ADAS:", "Applied Intuition, NVIDIA Isaac Sim powering ISO 26262 validation [Verified]"),
        ]),
        ("Tier 2", "Active Customer Pilots (Pre-Production)", GOLD, [
            ("Humanoid Logistics:", "Figure 02 at BMW Spartanburg (Aug 2024) [Verified]"),
            ("Parts Delivery:", "Apptronik Apollo at Mercedes-Benz (Mar 2024) [Verified]"),
            ("Container Unloading:", "Boston Dynamics Stretch at DHL Supply Chain [Verified]"),
        ]),
        ("Tier 3", "Lab Demos & Research Claims", RED_SOFT, [
            ("Zero-Shot Assembly:", "Tight-tolerance insertion (<0.1mm) from sim only [Speculative]"),
            ("Domestic Tasks:", "Autonomous laundry folding, open-world tidying [Reported]"),
        ]),
    ]
    for i, (tier, label, color, items) in enumerate(tiers_data):
        top = 2.0 + i * 1.75
        add_rect(s, 0.3, top, 12.7, 1.6, BG_CARD)
        add_rect(s, 0.3, top, 0.06, 1.6, color)
        add_textbox(s, 0.55, top + 0.08, 1.2, 0.3, tier, 11, bold=True, color=color)
        add_textbox(s, 1.85, top + 0.08, 5.0, 0.3, label, 13, bold=True, color=WHITE)
        for j, (prefix, detail) in enumerate(items):
            y = top + 0.42 + j * 0.36
            add_textbox(s, 0.55, y, 2.2, 0.32, prefix, 11, bold=True, color=color)
            add_textbox(s, 2.85, y, 9.9, 0.32, detail, 11, color=LIGHT_GREY)
    set_notes(s, "Three tiers of commercial maturity. Tier 1 has real revenue, Tier 2 has pilots, Tier 3 is lab research.")
    return s

def slide_06_capital():
    s = new_slide(); fill_bg(s)
    module_badge(s, "Module 1 \u00b7 Commercial State")
    add_textbox(s, 0.3, 0.6, 12.5, 0.8,
        "Disclosed Capital Deployment Matrix", 30, bold=True, color=WHITE)
    add_textbox(s, 0.3, 1.3, 12.5, 0.4,
        "Verified Funding Rounds and Commercial Maturity (2024)", 15, color=GOLD)
    gold_divider(s, 1.82)
    add_rect(s, 0.3, 1.95, 12.7, 0.38, GOLD)
    headers = ["Sub-Segment", "Key Rounds", "Valuation", "Maturity", "Tag"]
    col_l = [0.35, 3.2, 6.9, 9.2, 11.5]
    col_w = [2.8, 3.6, 2.2, 2.2, 1.6]
    for i, h in enumerate(headers):
        add_textbox(s, col_l[i], 1.97, col_w[i], 0.35, h, 10, bold=True, color=BG_DARK)
    rows = [
        ("Robotics Foundation\nModels & Humanoids",
         "Wayve $1.05B (May '24)\nFigure AI $675M (Feb '24)\nPI $400M (Nov '24)",
         "$2.4B\u2013$2.6B", "Pilot / Early\nProduction", "[Verified]", GREEN_SOFT),
        ("Industrial AI\n(Fixed & Mobile)",
         "Skild AI $300M (Jul '24)\nBright Machines $126M",
         "$1.5B", "Pilot /\nProduction", "[Verified]", GREEN_SOFT),
        ("Simulation &\nDigital Twins",
         "Applied Intuition $250M\nScale AI $1.0B\nWorld Labs $230M",
         "$6B\u2013$13.8B", "Production", "[Verified]", GREEN_SOFT),
        ("Safety &\nCompliance Tooling",
         "Credo AI $25M\nHolistic AI $20M",
         "Early", "Pilot", "[Reported]", CYAN),
    ]
    for i, (seg, rounds, val, mat, tag, tag_color) in enumerate(rows):
        top = 2.4 + i * 1.25
        bg = BG_CARD if i % 2 == 0 else BG_CARD_ALT
        add_rect(s, 0.3, top, 12.7, 1.15, bg)
        add_textbox(s, col_l[0], top+0.05, col_w[0], 1.05, seg, 10.5, bold=True, color=WHITE)
        add_textbox(s, col_l[1], top+0.05, col_w[1], 1.05, rounds, 10, color=LIGHT_GREY)
        add_textbox(s, col_l[2], top+0.05, col_w[2], 1.05, val, 10.5, bold=True, color=GOLD)
        add_textbox(s, col_l[3], top+0.05, col_w[3], 1.05, mat, 10, color=LIGHT_GREY)
        add_textbox(s, col_l[4], top+0.05, col_w[4], 1.05, tag, 10, bold=True, color=tag_color)
    set_notes(s, "All funding figures cross-verified against primary corporate disclosures.")
    return s

def slide_07_asymmetry():
    s = new_slide(); fill_bg(s)
    module_badge(s, "Module 1 \u00b7 Commercial State")
    add_textbox(s, 0.3, 0.6, 12.5, 0.8,
        "The Capital vs. Maturity Asymmetry", 32, bold=True, color=WHITE)
    add_textbox(s, 0.3, 1.3, 12.5, 0.4,
        "Where Money Flows vs. Where Revenue Exists", 15, color=GOLD)
    gold_divider(s, 1.82)
    add_rect(s, 0.3, 2.0, 6.1, 4.0, BG_CARD)
    add_rect(s, 0.3, 2.0, 0.06, 4.0, RED_SOFT)
    lines_l = [
        ("The Humanoid Capital Trap", True, RED_SOFT, 0),
        ("", False, WHITE, 0),
        ("$2.2B+ into humanoid OEMs (18 months) [Verified]", False, WHITE, 0),
        ("", False, WHITE, 0),
        ("Customer revenue: <$20M industry-wide [Estimated]", False, LIGHT_GREY, 0),
        ("", False, WHITE, 0),
        ("MTBF: <50 hours continuous actuation [Estimated]", False, LIGHT_GREY, 0),
        ("Prototype BOM: $100k\u2013$250k/unit [Estimated]", False, LIGHT_GREY, 0),
    ]
    add_multiline(s, 0.55, 2.12, 5.6, 3.7, lines_l, 13, line_spacing_pt=2)
    add_rect(s, 6.65, 2.0, 6.35, 4.0, BG_CARD)
    add_rect(s, 6.65, 2.0, 0.06, 4.0, GREEN_SOFT)
    lines_r = [
        ("Cash-Flow-Positive Infrastructure", True, GREEN_SOFT, 0),
        ("", False, WHITE, 0),
        ("Simulation & validation: 70\u201380% gross margins", False, WHITE, 0),
        ("", False, WHITE, 0),
        ("Applied Intuition: $6B valuation with", False, LIGHT_GREY, 0),
        ("multi-million-dollar ARR contracts [Verified]", False, LIGHT_GREY, 0),
        ("", False, WHITE, 0),
        ("Enterprise SaaS that scales without hardware", False, LIGHT_GREY, 0),
    ]
    add_multiline(s, 6.9, 2.12, 5.9, 3.7, lines_r, 13, line_spacing_pt=2)
    add_rect(s, 0.3, 6.2, 12.7, 0.9, BG_CARD)
    add_rect(s, 0.3, 6.2, 12.7, 0.06, GOLD)
    add_textbox(s, 0.55, 6.35, 12.2, 0.65,
        "Implication: Capital is subsidizing hardware experimentation. LTTS should position upstream as the integration partner that captures revenue regardless of which hardware vendor wins.",
        13, bold=True, color=GOLD)
    set_notes(s, "The asymmetry is stark. LTTS should position upstream.")
    return s

# ── SLIDES 8-11: Research Frontiers ──────────────────────────────────────────
def slide_08_div():
    s = new_slide()
    section_divider(s, "02", "Research\nFrontiers", "What the Frontier Labs Are Actually Working On")
    set_notes(s, "Section 2: Five engineering bottlenecks and failure modes.")
    return s

def slide_09_tech():
    s = new_slide(); fill_bg(s)
    module_badge(s, "Module 2 \u00b7 Research Frontiers")
    add_textbox(s, 0.3, 0.6, 12.5, 0.8,
        "Five Active Engineering Bottlenecks", 30, bold=True, color=WHITE)
    add_textbox(s, 0.3, 1.3, 12.5, 0.4,
        "Technical Priorities Across Frontier Research Labs", 15, color=GOLD)
    gold_divider(s, 1.82)
    bottlenecks = [
        ("01", "Continuous Action Flow Matching", "RT-1/RT-2 quantized actions causing errors. Frontier: \u03c0\u2080 uses continuous flow matching at 50Hz.", CYAN),
        ("02", "Physics-Informed 3D World Models", "2D pixel prediction \u2192 3D voxel/point-flow (PointWorld, NVIDIA Cosmos).", GOLD),
        ("03", "Reinforced Fine-Tuning (RFT)", "Imitation learning drifts. RL fine-tuning with stage-aware rewards (STA-PPO).", CYAN),
        ("04", "Cross-Embodiment Scaling Laws", "NVIDIA EgoScale (2026): log-linear scaling from egocentric video to robot morphologies.", GOLD),
        ("05", "Edge Model Compression", "AutoQVLA: channel-aware quantization for VLAs on NVIDIA Jetson AGX Orin.", CYAN),
    ]
    for i, (num, title, detail, color) in enumerate(bottlenecks):
        top = 1.95 + i * 1.05
        add_rect(s, 0.3, top, 12.7, 0.92, BG_CARD)
        add_rect(s, 0.3, top, 0.06, 0.92, color)
        add_textbox(s, 0.55, top+0.08, 0.5, 0.35, num, 14, bold=True, color=color)
        add_textbox(s, 1.15, top+0.08, 3.5, 0.35, title, 13, bold=True, color=WHITE)
        add_textbox(s, 4.8, top+0.08, 8.0, 0.75, detail, 11.5, color=LIGHT_GREY)
    set_notes(s, "Five bottlenecks define the frontier.")
    return s

def slide_10_failures():
    s = new_slide(); fill_bg(s)
    module_badge(s, "Module 2 \u00b7 Research Frontiers")
    add_textbox(s, 0.3, 0.6, 12.5, 0.8,
        "Five Canonical Failure Modes", 30, bold=True, color=WHITE)
    add_textbox(s, 0.3, 1.3, 12.5, 0.4,
        "Every Failure Has a Quantitative Mitigation", 15, color=GOLD)
    gold_divider(s, 1.82)
    fms = [
        ("FM1", "Compounding Drift", "Per-step errors multiply exponentially.", "Hierarchical models, flow matching", RED_SOFT),
        ("FM2", "Executability Gap", "Visual plausibility \u2260 physical validity.", "PINN-augmented loss constraints", ORANGE_SOFT),
        ("FM3", "Perceptual Hallucination", "OOD inputs mapped to wrong tokens.", "Reconstruction residual gating", RED_SOFT),
        ("FM4", "Action Marginalization", "Predictions ignore control inputs.", "Action-conditioned contrastive losses", ORANGE_SOFT),
        ("FM5", "Sim-to-Real Gap", "Simulation \u2260 real contact/friction.", "Real2Sim2Real + hybrid data", PURPLE_SOFT),
    ]
    for i, (num, title, mechanism, mitigation, color) in enumerate(fms):
        top = 1.95 + i * 1.05
        add_rect(s, 0.3, top, 12.7, 0.92, BG_CARD)
        add_rect(s, 0.3, top, 0.06, 0.92, color)
        add_textbox(s, 0.55, top+0.06, 0.8, 0.3, num, 10, bold=True, color=color)
        add_textbox(s, 1.4, top+0.06, 3.0, 0.3, title, 12, bold=True, color=WHITE)
        add_textbox(s, 4.6, top+0.06, 4.2, 0.8, mechanism, 11, color=LIGHT_GREY)
        add_textbox(s, 9.0, top+0.06, 3.8, 0.8, mitigation, 11, bold=True, color=color)
    add_textbox(s, 0.3, 7.2, 12.7, 0.3,
        "No known deployment failure is beyond engineering control.", 12, bold=True, color=CYAN, align=PP_ALIGN.CENTER)
    set_notes(s, "Five canonical failure modes with engineering mitigations.")
    return s

def slide_11_causal():
    s = new_slide(); fill_bg(s)
    module_badge(s, "Module 2 \u00b7 Research Frontiers")
    add_textbox(s, 0.3, 0.6, 12.5, 0.8,
        "Pearl's Causal Ladder", 34, bold=True, color=WHITE)
    add_textbox(s, 0.3, 1.3, 12.5, 0.4,
        "Why LLMs Cannot Be Pointed at Robots", 15, color=GOLD)
    gold_divider(s, 1.82)
    rungs = [
        ("Rung I", "Association", "P(Y | X)", "Seeing & Correlating",
         "Language models: predict next token from data.", LIGHT_GREY, False),
        ("Rung II", "Intervention", "P(Y | do(u))", "Doing & Observing",
         "Robotics: what happens with 15N torque?", CYAN, True),
        ("Rung III", "Counterfactual", "P(Y\u2095 | X', Y')", "Imagining",
         "Planning: what if I acted differently?", GOLD, True),
    ]
    for i, (rung, name, math, sub, desc, color, req) in enumerate(rungs):
        top = 2.0 + i * 1.65
        add_rect(s, 0.3, top, 7.8, 1.5, BG_CARD)
        if req:
            add_rect(s, 0.3, top, 0.06, 1.5, color)
        add_textbox(s, 0.55, top+0.08, 1.2, 0.3, rung, 11, bold=True, color=color)
        add_textbox(s, 0.55, top+0.42, 3.0, 0.4, name, 20, bold=True, color=WHITE)
        add_textbox(s, 0.55, top+0.88, 3.0, 0.4, sub, 11, color=LIGHT_GREY)
        add_textbox(s, 3.8, top+0.42, 4.0, 0.35, math, 13, bold=True, color=color)
        add_textbox(s, 3.8, top+0.82, 4.0, 0.55, desc, 11.5, color=LIGHT_GREY)
    add_rect(s, 8.4, 2.0, 4.6, 4.95, BG_CARD)
    add_textbox(s, 8.6, 2.12, 4.2, 0.35, "THE CATEGORY ERROR", 10, bold=True, color=CYAN)
    eq = render_latex(r"\frac{dx}{dt}=f(x,u,t)", "eq_dynamics_v3", fontsize=22)
    add_image_from_bytes(s, eq, 8.6, 2.55, 4.0, 1.0)
    add_textbox(s, 8.6, 3.7, 4.2, 3.1,
        "Deploying text-trained models into factory cells is a fundamental representational failure.\n\n"
        "Language models operate on Rung I.\n\n"
        "Physical deployment demands Rungs II and III.\n\n"
        "This is not an engineering gap. It is a category error.",
        12, color=LIGHT_GREY)
    set_notes(s, "Pearl's Causal Hierarchy is the load-bearing formalism: LLMs are Rung I, robots need Rungs II and III.")
    return s

# ── SLIDES 12-14: Commercialization ──────────────────────────────────────────
def slide_12_div():
    s = new_slide()
    section_divider(s, "03", "Commercialization", "How Physical AI Generates Revenue")
    set_notes(s, "Section 3: Business models and LTTS's strategic playbook.")
    return s

def slide_13_commercial():
    s = new_slide(); fill_bg(s)
    module_badge(s, "Module 3 \u00b7 Commercialization")
    add_textbox(s, 0.3, 0.6, 12.5, 0.8,
        "Commercial Models and Deal Economics", 28, bold=True, color=WHITE)
    add_textbox(s, 0.3, 1.3, 12.5, 0.4,
        "Business Models, Contract Structures, Buyer Personas", 15, color=GOLD)
    gold_divider(s, 1.82)
    add_rect(s, 0.3, 1.95, 12.7, 0.35, GOLD)
    hdr = ["Business Model", "Key Players", "Contract Range", "Cycle", "Tag"]
    hdr_x = [0.4, 3.4, 6.6, 9.6, 11.3]
    hdr_w = [2.9, 3.1, 2.9, 1.6, 1.6]
    for i, h in enumerate(hdr):
        add_textbox(s, hdr_x[i], 1.96, hdr_w[i], 0.32, h, 9.5, bold=True, color=BG_DARK)
    models = [
        ("Model Licensing / FMaaS", "PI, Skild AI, Covariant", "$100k\u2013$500k+ ACV", "3\u20136 mo", "[Est]", GOLD),
        ("Integrated HW+SW (OEM)", "Figure, Agility, Boston Dyn.", "$5k\u2013$15k/robot/mo RaaS", "12\u201318 mo", "[Rep]", CYAN),
        ("Simulation & Validation", "NVIDIA Isaac, Applied Int.", "$250k\u2013$2M+ ACV", "6\u20139 mo", "[Rep]", GOLD),
        ("Safety & Compliance", "TUV SUD, UL, Credo AI", "$150k\u2013$750k per audit", "6\u201312 mo", "[Est]", CYAN),
        ("Systems Integration", "LTTS, KPIT, Accenture IX", "$1M\u2013$8M+ per site", "4\u20138 mo", "[Est]", GOLD),
    ]
    for i, (model, players, contract, cycle, tag, accent) in enumerate(models):
        top = 2.38 + i * 0.95
        bg = BG_CARD if i % 2 == 0 else BG_CARD_ALT
        add_rect(s, 0.3, top, 12.7, 0.85, bg)
        add_rect(s, 0.3, top, 0.05, 0.85, accent)
        add_textbox(s, hdr_x[0], top+0.08, hdr_w[0], 0.7, model, 11, bold=True, color=WHITE)
        add_textbox(s, hdr_x[1], top+0.08, hdr_w[1], 0.7, players, 10.5, color=LIGHT_GREY)
        add_textbox(s, hdr_x[2], top+0.08, hdr_w[2], 0.7, contract, 11, bold=True, color=accent)
        add_textbox(s, hdr_x[3], top+0.08, hdr_w[3], 0.7, cycle, 10.5, color=LIGHT_GREY)
        add_textbox(s, hdr_x[4], top+0.08, hdr_w[4], 0.7, tag, 10, bold=True, color=accent)
    add_rect(s, 0.3, 7.15, 12.7, 0.35, BG_GREEN)
    add_textbox(s, 0.5, 7.17, 12.3, 0.3,
        "LTTS's sweet spot: Systems Integration at $1M\u2013$8M+ per site with 4\u20138 month cycles",
        12, bold=True, color=GREEN_SOFT, align=PP_ALIGN.CENTER)
    set_notes(s, "Five business models. LTTS is positioned in the $1M-$8M+ SI layer.")
    return s

def slide_14_ltts():
    s = new_slide(); fill_bg(s)
    module_badge(s, "Module 3 \u00b7 Commercialization")
    add_textbox(s, 0.3, 0.6, 12.5, 0.8,
        "LTTS Strategic Playbook", 34, bold=True, color=WHITE)
    add_textbox(s, 0.3, 1.3, 12.5, 0.4,
        "Four Commercial Service Offerings for Physical AI", 15, color=GOLD)
    gold_divider(s, 1.82)
    offerings = [
        ("01", "Synthetic Data Factory as a Service (SD-FaaS)",
         "Ingest CAD/PLM assemblies (Siemens NX, Teamcenter, CATIA) to create calibrated digital twin environments in NVIDIA Isaac Sim.",
         "$1.0M\u2013$3.5M annual [Est]", CYAN),
        ("02", "Brownfield PLC-to-AI Integration",
         "Deterministic bridge middleware connecting neural outputs to Siemens S7-1500 / Rockwell ControlLogix via Profinet/EtherCAT with safety interlocks.",
         "$1.5M\u2013$5.0M per plant [Est]", GOLD),
        ("03", "Physical AI V&V",
         "Independent stress-testing of third-party neural controllers against ISO 13849 and IEC 61508 safety standards.",
         "$500k\u2013$1.5M/engagement [Est]", CYAN),
        ("04", "Managed Embodied MLOps",
         "Continuous telemetry monitoring, edge drift detection, and automated synthetic retraining pipelines.",
         "$500k\u2013$2.0M ARR [Est]", GOLD),
    ]
    for i, (num, title, desc, price, color) in enumerate(offerings):
        top = 1.95 + i * 1.35
        add_rect(s, 0.3, top, 12.7, 1.22, BG_CARD)
        add_rect(s, 0.3, top, 0.06, 1.22, color)
        add_textbox(s, 0.55, top+0.08, 0.5, 0.35, num, 18, bold=True, color=color)
        add_textbox(s, 1.2, top+0.08, 7.5, 0.35, title, 14, bold=True, color=WHITE)
        add_textbox(s, 1.2, top+0.45, 8.0, 0.7, desc, 11.5, color=LIGHT_GREY)
        add_textbox(s, 9.5, top+0.08, 3.3, 0.35, price, 12, bold=True, color=color, align=PP_ALIGN.RIGHT)
    set_notes(s, "Four concrete service offerings for LTTS.")
    return s

# ── SLIDES 15-17: Use Cases ──────────────────────────────────────────────────
def slide_15_div():
    s = new_slide()
    section_divider(s, "04", "Use Cases &\nAdoption", "Production Reality, Hype, and the Hybrid Model")
    set_notes(s, "Section 4: What's deployed vs. what's hype.")
    return s

def slide_16_deployments():
    s = new_slide(); fill_bg(s)
    module_badge(s, "Module 4 \u00b7 Use Cases")
    add_textbox(s, 0.3, 0.6, 12.5, 0.8,
        "Verified Deployments by Sector", 30, bold=True, color=WHITE)
    add_textbox(s, 0.3, 1.3, 12.5, 0.4,
        "Cross-Industry Mapping of Real Physical AI in Production", 15, color=GOLD)
    gold_divider(s, 1.82)
    sectors = [
        ("Automotive", "Optical/acoustic quality inspection at BMW, Ford, Mercedes. Robotic parts handling.", "[Rep/Ver]", GREEN_SOFT),
        ("Aerospace", "Composite layup inspection and precision robotic drilling (Airbus, Boeing).", "[Reported]", CYAN),
        ("Semiconductor", "Physics-informed defect prediction in wafer lithography (TSMC, Intel).", "[Reported]", CYAN),
        ("Logistics", "BD Stretch at DHL. AMR fleets at Amazon Robotics, Symbotic at Walmart.", "[Verified]", GREEN_SOFT),
        ("Energy", "Predictive monitoring on gas turbines (GE Vernova, Siemens Energy).", "[Verified]", GREEN_SOFT),
    ]
    for i, (sector, desc, tag, color) in enumerate(sectors):
        top = 1.95 + i * 1.05
        add_rect(s, 0.3, top, 12.7, 0.92, BG_CARD)
        add_rect(s, 0.3, top, 0.06, 0.92, color)
        add_textbox(s, 0.55, top+0.08, 2.2, 0.35, sector, 13, bold=True, color=WHITE)
        add_textbox(s, 2.9, top+0.08, 7.8, 0.78, desc, 11.5, color=LIGHT_GREY)
        add_textbox(s, 10.9, top+0.08, 2.0, 0.35, tag, 10, bold=True, color=color, align=PP_ALIGN.RIGHT)
    add_rect(s, 0.3, 7.2, 12.7, 0.3, BG_CARD_ALT)
    add_textbox(s, 0.5, 7.21, 12.3, 0.28,
        "Hype-Ahead: Humanoid assembly [Spec] \u00b7 Outdoor construction [Rep] \u00b7 Unsupervised surgery [FDA regulated]",
        10.5, color=ORANGE_SOFT, align=PP_ALIGN.CENTER)
    set_notes(s, "Five sectors with verified deployments. Three hype-ahead categories.")
    return s

def slide_17_hybrid():
    s = new_slide(); fill_bg(s)
    module_badge(s, "Module 4 \u00b7 Use Cases")
    add_textbox(s, 0.3, 0.6, 12.5, 0.8,
        "The Hybrid Adoption Pattern", 32, bold=True, color=WHITE)
    add_textbox(s, 0.3, 1.3, 12.5, 0.4,
        "Why the Incumbent-Partner Model Wins", 15, color=GOLD)
    gold_divider(s, 1.82)
    cards = [
        ("Incumbent Defense", "Factory managers won't risk downtime or void insurance by bypassing certified PLCs.", CYAN),
        ("AI Startup Limits", "Frontier startups lack field engineering for thousands of brownfield factories.", GOLD),
        ("Alliance Pattern", "Siemens + Microsoft (Copilot) and Siemens + Intrinsic (Alphabet) show incumbents absorbing AI while relying on SIs. [Verified]", GREEN_SOFT),
    ]
    for i, (title, desc, color) in enumerate(cards):
        top = 2.0 + i * 1.7
        add_rect(s, 0.3, top, 12.7, 1.55, BG_CARD)
        add_rect(s, 0.3, top, 0.06, 1.55, color)
        add_textbox(s, 0.6, top+0.12, 4.0, 0.4, title, 16, bold=True, color=WHITE)
        add_textbox(s, 0.6, top+0.55, 12.0, 0.9, desc, 13, color=LIGHT_GREY)
    add_rect(s, 0.3, 7.15, 12.7, 0.35, BG_CARD)
    add_rect(s, 0.3, 7.15, 12.7, 0.04, GOLD)
    add_textbox(s, 0.55, 7.18, 12.2, 0.3,
        "LTTS occupies the exact structural position these alliances require.",
        12, bold=True, color=GOLD, align=PP_ALIGN.CENTER)
    set_notes(s, "The hybrid model wins. LTTS is perfectly positioned as the SI bridge.")
    return s

# ── SLIDES 18-20: Competitive ────────────────────────────────────────────────
def slide_18_div():
    s = new_slide()
    section_divider(s, "05", "Competitive\nLandscape", "Layered Analysis and Underserved Gaps")
    set_notes(s, "Section 5: Five competitive layers and three gaps.")
    return s

def slide_19_competitive():
    s = new_slide(); fill_bg(s)
    module_badge(s, "Module 5 \u00b7 Competition")
    add_textbox(s, 0.3, 0.6, 12.5, 0.8,
        "Layered Competitive Map", 32, bold=True, color=WHITE)
    add_textbox(s, 0.3, 1.3, 12.5, 0.4,
        "Five Structural Layers Across Physical AI", 15, color=GOLD)
    gold_divider(s, 1.82)
    layers = [
        ("Robotics Foundation Models", "PI, Skild AI, DeepMind", "Challengers: depend on SIs", CYAN),
        ("Automation Incumbents", "Siemens, Rockwell, ABB", "Dominant: own floors and trust", GOLD),
        ("Simulation Platforms", "NVIDIA Isaac, Applied Int.", "Dominant: platform standards", CYAN),
        ("ER&D Engineering Services", "LTTS, KPIT, Tata Tech", "Race to build certified practices", GOLD),
        ("Safety & Compliance", "TUV SUD, UL, Credo AI", "Gatekeepers: mandatory for ops", CYAN),
    ]
    for i, (layer, players, position, color) in enumerate(layers):
        top = 1.95 + i * 1.0
        bg = BG_GREEN if i == 3 else BG_CARD
        add_rect(s, 0.3, top, 12.7, 0.88, bg)
        add_rect(s, 0.3, top, 0.06, 0.88, color if i != 3 else GOLD)
        add_textbox(s, 0.55, top+0.08, 3.5, 0.35, layer, 12, bold=True, color=WHITE)
        c = GOLD if i == 3 else LIGHT_GREY
        add_textbox(s, 4.2, top+0.08, 3.5, 0.72, players, 11.5, color=c)
        add_textbox(s, 7.8, top+0.08, 5.0, 0.72, position, 11.5, bold=True, color=color if i != 3 else GOLD)
    set_notes(s, "Five layers. LTTS competes in ER&D Services against KPIT, Tata Tech, and Cyient.")
    return s

def slide_20_gaps():
    s = new_slide(); fill_bg(s)
    module_badge(s, "Module 5 \u00b7 Competition")
    add_textbox(s, 0.3, 0.6, 12.5, 0.8,
        "High-Value Underserved Gaps", 32, bold=True, color=WHITE)
    add_textbox(s, 0.3, 1.3, 12.5, 0.4,
        "Three Immediate Opportunities for LTTS", 15, color=GOLD)
    gold_divider(s, 1.82)
    gaps = [
        ("Gap 1", "Formal Safety Verification for Neural Policies",
         "Foundation labs generate neural policies, but certifiers demand deterministic safety proofs. Major gap: automated toolchains translating neural outputs into IEC 61508 / ISO 13849 compliance dossiers.", GOLD),
        ("Gap 2", "CAD/PLM to Differentiable Physics Pipelines",
         "Converting CAD assemblies into simulation-ready digital twin environments requires heavy manual engineering. Automated ingestion is an immediate opportunity.", CYAN),
        ("Gap 3", "Deterministic Edge Deployment Middleware",
         "Managing real-time neural model execution on edge compute (NVIDIA Jetson) without jitter or safety watchdog violations. No turnkey solution exists.", GOLD),
    ]
    for i, (num, title, desc, color) in enumerate(gaps):
        top = 2.0 + i * 1.7
        add_rect(s, 0.3, top, 12.7, 1.55, BG_CARD)
        add_rect(s, 0.3, top, 0.06, 1.55, color)
        add_textbox(s, 0.55, top+0.12, 1.0, 0.35, num, 14, bold=True, color=color)
        add_textbox(s, 1.6, top+0.12, 10.5, 0.35, title, 15, bold=True, color=WHITE)
        add_textbox(s, 1.6, top+0.55, 11.0, 0.9, desc, 12.5, color=LIGHT_GREY)
    set_notes(s, "Three gaps. Gap 1 maps directly to Priority 1.")
    return s

# ── SLIDES 21-24: Bridge ─────────────────────────────────────────────────────
def slide_21_div():
    s = new_slide()
    section_divider(s, "06", "The Industrial AI\nto Physical AI Bridge", "Domain Engineering, Kinematics, and the Flywheel")
    set_notes(s, "Section 6: The technical bridge.")
    return s

def slide_22_bridge():
    s = new_slide(); fill_bg(s)
    module_badge(s, "Module 6 \u00b7 The Bridge")
    add_textbox(s, 0.3, 0.6, 12.5, 0.8,
        "Industrial AI vs. Physical AI", 32, bold=True, color=WHITE)
    add_textbox(s, 0.3, 1.3, 12.5, 0.4,
        "A Fundamental Technical Distinction", 15, color=GOLD)
    gold_divider(s, 1.82)
    add_rect(s, 0.3, 2.0, 6.1, 3.8, BG_CARD)
    add_rect(s, 0.3, 2.0, 6.1, 0.05, LIGHT_GREY)
    lines_l = [
        ("Industrial AI (Open-Loop)", True, LIGHT_GREY, 0),
        ("", False, WHITE, 0),
        ("1D scalar time-series", False, LIGHT_GREY, 0),
        ("Human notifications on minute/hour scale", False, LIGHT_GREY, 0),
        ("Predictive maintenance, anomaly detection", False, LIGHT_GREY, 0),
    ]
    add_multiline(s, 0.55, 2.15, 5.6, 3.5, lines_l, 13, line_spacing_pt=4)
    add_rect(s, 6.65, 2.0, 6.35, 3.8, BG_CARD)
    add_rect(s, 6.65, 2.0, 6.35, 0.05, GOLD)
    lines_r = [
        ("Physical AI (Closed-Loop)", True, GOLD, 0),
        ("", False, WHITE, 0),
        ("3D spatial + depth + force feedback", False, WHITE, 0),
        ("Actuator commands at \u226550Hz", False, WHITE, 0),
        ("Requires robotics + controls + mech DNA", False, WHITE, 0),
    ]
    add_multiline(s, 6.9, 2.15, 5.9, 3.5, lines_r, 13, line_spacing_pt=4)
    add_rect(s, 0.3, 6.0, 12.7, 1.2, BG_CARD)
    add_rect(s, 0.3, 6.0, 0.06, 1.2, GOLD)
    lines_b = [
        ("Key Consequence", True, GOLD, 0),
        ("PdM vendors cannot transition to robotics control. Physical AI needs engineering DNA.", False, LIGHT_GREY, 0),
        ("This is LTTS's structural advantage as a pure-play ER&D firm.", False, GOLD, 0),
    ]
    add_multiline(s, 0.55, 6.08, 12.2, 1.0, lines_b, 12.5, line_spacing_pt=2)
    set_notes(s, "Physical AI is fundamentally distinct from Industrial AI. LTTS's engineering DNA is the structural advantage.")
    return s

def slide_23_domain():
    s = new_slide(); fill_bg(s)
    module_badge(s, "Module 6 \u00b7 The Bridge")
    add_textbox(s, 0.3, 0.6, 12.5, 0.8,
        "The Domain Engineering Moat", 32, bold=True, color=WHITE)
    add_textbox(s, 0.3, 1.3, 12.5, 0.4,
        "Kinematic Invariants, Safety Architecture, Real-Time Control", 15, color=GOLD)
    gold_divider(s, 1.82)
    add_rect(s, 0.3, 2.0, 12.7, 2.5, BG_CARD)
    add_rect(s, 0.3, 2.0, 0.06, 2.5, GOLD)
    add_textbox(s, 0.55, 2.08, 12.0, 0.35,
        "KINEMATIC SINGULARITY MANAGEMENT", 10, bold=True, color=GOLD)
    eq1 = render_latex(r"\dot{x} = J(q)\dot{q}", "eq_jac_v3", fontsize=20)
    add_image_from_bytes(s, eq1, 0.55, 2.5, 4.5, 0.85)
    eq2 = render_latex(r"\mu(q) = \sqrt{\det(J(q)J^T(q))} \longrightarrow 0", "eq_manip_v3", fontsize=18)
    add_image_from_bytes(s, eq2, 5.5, 2.5, 6.5, 0.85)
    add_textbox(s, 0.55, 3.5, 12.2, 0.9,
        "Near singularities, small Cartesian commands demand unbounded joint velocities. Triggers drive faults, e-stops, or gearbox damage. Pure ML engineers cannot build singularity-robust IK layers.",
        12, color=LIGHT_GREY)
    items = [
        ("Deterministic Timing",
         "Synchronizing neural inference with <1ms jitter fieldbus cycles (EtherCAT/Profinet) via RTOS.", CYAN),
        ("Functional Safety",
         "Dual-channel safety circuits and hardware interlocks: ISO 13849 (Cat 4 / PLe).", GOLD),
    ]
    for i, (title, desc, color) in enumerate(items):
        top = 4.65 + i * 1.2
        add_rect(s, 0.3, top, 12.7, 1.05, BG_CARD)
        add_rect(s, 0.3, top, 0.06, 1.05, color)
        add_textbox(s, 0.55, top+0.08, 3.5, 0.35, title, 13, bold=True, color=WHITE)
        add_textbox(s, 4.2, top+0.08, 8.5, 0.85, desc, 12, color=LIGHT_GREY)
    set_notes(s, "The Jacobian singularity equation defines the domain moat. This is load-bearing math, not decoration.")
    return s

def slide_24_flywheel():
    s = new_slide(); fill_bg(s)
    module_badge(s, "Module 6 \u00b7 The Bridge")
    add_textbox(s, 0.3, 0.6, 12.5, 0.8,
        "The Operational Data Flywheel", 30, bold=True, color=WHITE)
    add_textbox(s, 0.3, 1.3, 12.5, 0.4,
        "Five-Stage Deployment Architecture", 15, color=GOLD)
    gold_divider(s, 1.82)
    stages = [
        ("01", "TELEMETRY", "Log motor torques,\ncurrents, visual streams\nfrom industrial buses.", CYAN),
        ("02", "CALIBRATION", "Refine simulation\nparams (friction, inertia)\nfrom real telemetry.", GOLD),
        ("03", "GENERATION", "Generate edge-case\nscenarios in Isaac Sim\nfor robust policies.", CYAN),
        ("04", "DEPLOYMENT", "Compressed models on\nJetson with deterministic\nsafety envelopes.", GOLD),
        ("05", "FEEDBACK", "Detect OOD states,\ntrigger re-simulation\nand policy refinement.", CYAN),
    ]
    for i, (num, title, detail, color) in enumerate(stages):
        lft = 0.22 + i * 2.6
        add_rect(s, lft, 2.0, 2.44, 3.8, BG_CARD)
        add_rect(s, lft, 2.0, 2.44, 0.06, color)
        add_textbox(s, lft+0.12, 2.12, 2.2, 0.4, num, 16, bold=True, color=color)
        add_textbox(s, lft+0.12, 2.55, 2.2, 0.5, title, 11, bold=True, color=WHITE)
        add_textbox(s, lft+0.12, 3.1, 2.2, 2.4, detail, 11, color=LIGHT_GREY)
        if i < 4:
            arr = s.shapes.add_shape(1,
                Inches(lft+2.44), Inches(3.6), Inches(0.16), Inches(0.06))
            arr.fill.solid(); arr.fill.fore_color.rgb = GOLD
            arr.line.fill.background()
    add_rect(s, 0.3, 6.0, 12.7, 0.5, BG_CARD)
    add_textbox(s, 0.5, 6.05, 12.3, 0.4,
        "\u21ba  Continuous feedback: every deployment enriches the next training cycle.",
        13, bold=True, color=GOLD, align=PP_ALIGN.CENTER)
    add_rect(s, 0.3, 6.65, 12.7, 0.75, BG_GREEN)
    add_rect(s, 0.3, 6.65, 0.06, 0.75, GOLD)
    add_textbox(s, 0.55, 6.72, 12.2, 0.6,
        "THE MOAT: Compute is a commodity. This operational data flywheel is virtually impossible to replicate without years of deployment.",
        13, bold=True, color=WHITE)
    set_notes(s, "The five-stage flywheel is the competitive moat. Compute is buyable. Operational data is not.")
    return s

# ── SLIDES 25-26: Future ─────────────────────────────────────────────────────
def slide_25_div():
    s = new_slide()
    section_divider(s, "07", "The Future:\n3\u20135 Year Forecast", "Market Evolution and Key Uncertainties")
    set_notes(s, "Section 7: Structural forecast.")
    return s

def slide_26_forecast():
    s = new_slide(); fill_bg(s)
    module_badge(s, "Module 7 \u00b7 The Future")
    add_textbox(s, 0.3, 0.6, 12.5, 0.8,
        "3\u20135 Year Structural Forecast", 32, bold=True, color=WHITE)
    add_textbox(s, 0.3, 1.3, 12.5, 0.4,
        "Market Evolution 2026\u20132030", 15, color=GOLD)
    gold_divider(s, 1.82)
    trends = [
        ("Hardware Commoditization", "Robotic arms commoditize. Value shifts to software and SI.", CYAN),
        ("Model Consolidation", "Foundation models \u2192 2\u20133 ecosystems. Proprietary training unviable for SIs.", GOLD),
        ("Integration Fragmentation", "Heterogeneous factories keep SI high-margin. LTTS's sweet spot.", GREEN_SOFT),
        ("Data Exhaustion Pivot", "Public text consumed. Proprietary physical data becomes the lever.", GOLD),
    ]
    for i, (title, desc, color) in enumerate(trends):
        top = 2.0 + i * 1.2
        add_rect(s, 0.3, top, 12.7, 1.08, BG_CARD)
        add_rect(s, 0.3, top, 0.06, 1.08, color)
        add_textbox(s, 0.55, top+0.08, 3.5, 0.35, title, 13, bold=True, color=WHITE)
        add_textbox(s, 4.2, top+0.08, 8.6, 0.9, desc, 12, color=LIGHT_GREY)
    add_rect(s, 0.3, 6.85, 12.7, 0.65, BG_CARD_ALT)
    add_rect(s, 0.3, 6.85, 12.7, 0.05, ORANGE_SOFT)
    add_textbox(s, 0.55, 6.95, 12.2, 0.5,
        "Key Uncertainties: Regulatory caging mandates  \u00b7  Geopolitical decoupling  \u00b7  Sim-to-real progress",
        12, bold=True, color=ORANGE_SOFT, align=PP_ALIGN.CENTER)
    set_notes(s, "Four trends, three uncertainties. Integration layer stays fragmented.")
    return s

# ── SLIDES 27-30: Recommendations ────────────────────────────────────────────
def slide_27_div():
    s = new_slide()
    section_divider(s, "08", "Strategic\nRecommendations", "The Four-Priority Roadmap for LTTS")
    set_notes(s, "Section 8: The four-priority roadmap.")
    return s

def slide_28_p1():
    s = new_slide(); fill_bg(s)
    module_badge(s, "Module 8 \u00b7 Recommendations")
    add_textbox(s, 0.3, 0.6, 12.5, 0.8,
        "Priority 1: Physical AI V&V Practice", 28, bold=True, color=WHITE)
    add_textbox(s, 0.3, 1.3, 12.5, 0.4,
        "Q1 2027 Launch  \u00b7  $2.0M\u2013$3.5M Investment [Estimated]", 15, color=GOLD)
    gold_divider(s, 1.82)
    add_rect(s, 0.3, 2.0, 6.1, 1.6, BG_CARD)
    add_rect(s, 0.3, 2.0, 0.06, 1.6, GOLD)
    lines = [
        ("Sequencing Rationale", True, GOLD, 0),
        ("Lowest capital barrier. Addresses immediate", False, LIGHT_GREY, 0),
        ("regulatory bottleneck for existing clients.", False, LIGHT_GREY, 0),
        ("Builds safety methodology before scaling.", False, LIGHT_GREY, 0),
    ]
    add_multiline(s, 0.55, 2.08, 5.6, 1.4, lines, 12.5, line_spacing_pt=2)
    add_rect(s, 6.65, 2.0, 6.35, 1.6, BG_CARD)
    add_rect(s, 6.65, 2.0, 0.06, 1.6, CYAN)
    add_textbox(s, 6.85, 2.08, 6.0, 0.3, "CONTROL BARRIER FUNCTION (CBF)", 9.5, bold=True, color=CYAN)
    eq_cbf = render_latex(
        r"\dot{h}(x,u) = \nabla h \cdot f(x, \pi_\theta(x)) \geq -\alpha(h(x))",
        "eq_cbf_v3", fontsize=16)
    add_image_from_bytes(s, eq_cbf, 6.85, 2.45, 6.0, 0.95)
    add_rect(s, 0.3, 3.8, 12.7, 3.2, BG_CARD)
    add_textbox(s, 0.55, 3.88, 12.0, 0.35, "BOTTOM-UP INVESTMENT BREAKDOWN", 10, bold=True, color=GOLD)
    budget = [
        ("HIL Testbenches", "$800k", "2 multi-axis robot cells + motion capture + torque dynamometers"),
        ("Verification Tooling", "$400k", "Formal methods, reachability toolchains"),
        ("Core Team (6 FTEs)", "$1.2M/yr", "2 TUV Safety + 2 Controls + 2 NN Verification"),
        ("Lab Accreditation", "$400k", "ISO/IEC 17025 + TUV SUD partnership"),
    ]
    for i, (item, cost, desc) in enumerate(budget):
        top = 4.3 + i * 0.65
        add_textbox(s, 0.55, top, 2.5, 0.3, item, 12, bold=True, color=WHITE)
        add_textbox(s, 3.2, top, 1.5, 0.3, cost, 12, bold=True, color=GOLD)
        add_textbox(s, 4.8, top, 8.0, 0.55, desc, 11, color=LIGHT_GREY)
    add_rect(s, 0.3, 6.95, 12.7, 0.05, GOLD)
    add_textbox(s, 0.55, 7.05, 12.0, 0.35,
        "Total Phase 1: $2.8M (within $2.0M\u2013$3.5M range) [Estimated]",
        13, bold=True, color=GOLD)
    set_notes(s, "Priority 1: V&V. CBF formalism defines the software deliverable. Budget: $2.8M.")
    return s

def slide_29_p234():
    s = new_slide(); fill_bg(s)
    module_badge(s, "Module 8 \u00b7 Recommendations")
    add_textbox(s, 0.3, 0.6, 12.5, 0.8,
        "Priorities 2, 3, and 4", 32, bold=True, color=WHITE)
    add_textbox(s, 0.3, 1.3, 12.5, 0.4,
        "Sequential Roadmap: Alliances, Synthetic Data, Talent", 15, color=GOLD)
    gold_divider(s, 1.82)
    priorities = [
        ("P2", "Strategic PLC Alliances", "Q2 2027", "$1.3M",
         "Siemens S7 / Rockwell ControlLogix integration lab + 3 FTE Solutions Architecture + co-marketing.",
         "Requires V&V credentials (P1) before incumbents certify LTTS.", GOLD),
        ("P3", "Synthetic Data Factory", "Q3 2027", "$4.2M",
         "GPU simulation cluster ($2.2M) + Omniverse licensing ($500k) + 8 FTE simulation team ($1.5M/yr).",
         "Leverages CAD/PLM access from P2 alliances and validation from P1.", CYAN),
        ("P4", "Hybrid Talent CoE", "Ongoing", "$2.5M/yr",
         "Upskill 250 engineers ($1.0M/yr) + 5 Principal Research Engineers ($1.2M/yr) + Academic ($300k/yr).",
         "Cross-trains mechatronics bench into robotics AI.", GOLD),
    ]
    for i, (pnum, title, timeline, budget, detail, rationale, color) in enumerate(priorities):
        top = 1.95 + i * 1.75
        add_rect(s, 0.3, top, 12.7, 1.6, BG_CARD)
        add_rect(s, 0.3, top, 0.06, 1.6, color)
        add_textbox(s, 0.55, top+0.08, 0.6, 0.3, pnum, 14, bold=True, color=color)
        add_textbox(s, 1.2, top+0.08, 4.0, 0.3, title, 14, bold=True, color=WHITE)
        add_textbox(s, 5.5, top+0.08, 1.8, 0.3, timeline, 11, bold=True, color=color)
        add_textbox(s, 7.5, top+0.08, 2.5, 0.3, budget, 11, bold=True, color=GOLD)
        add_textbox(s, 1.2, top+0.42, 6.0, 1.1, detail, 10.5, color=LIGHT_GREY)
        add_textbox(s, 7.5, top+0.42, 5.2, 1.1, rationale, 10.5, italic=True, color=MID_GREY)
    set_notes(s, "Priorities 2-4 follow sequentially. Each unlocks the next.")
    return s

def slide_30_roadmap():
    s = new_slide(); fill_bg(s)
    module_badge(s, "Module 8 \u00b7 Recommendations")
    add_textbox(s, 0.3, 0.6, 12.5, 0.8,
        "LTTS Physical AI Roadmap", 32, bold=True, color=WHITE)
    add_textbox(s, 0.3, 1.3, 12.5, 0.4,
        "Complete Phasing, Budget, and Outcomes", 15, color=GOLD)
    gold_divider(s, 1.82)
    add_rect(s, 0.3, 2.0, 12.7, 0.4, GOLD)
    hdr_items = ["Initiative", "Core Focus", "Timeline", "Budget", "Outcome"]
    hdr_x = [0.4, 2.8, 6.5, 8.2, 10.0]
    hdr_w = [2.3, 3.6, 1.6, 1.7, 3.0]
    for i, h in enumerate(hdr_items):
        add_textbox(s, hdr_x[i], 2.02, hdr_w[i], 0.35, h, 9.5, bold=True, color=BG_DARK)
    rows = [
        ("P1: V&V Practice", "Safety certification", "Q1 2027", "$2.8M", "Functional safety auditing", GREEN_SOFT),
        ("P2: PLC Alliances", "Siemens/Rockwell bridge", "Q2 2027", "$1.3M", "Preferred plant partner", GOLD),
        ("P3: SD Factory", "Digital twin SD-FaaS", "Q3 2027", "$4.2M", "Monetize CAD/PLM data", CYAN),
        ("P4: Talent CoE", "Mech + AI cross-training", "Ongoing", "$2.5M/yr", "Deep domain workforce", GOLD),
    ]
    for i, (init, focus, timeline, budget, outcome, color) in enumerate(rows):
        top = 2.5 + i * 1.15
        bg = BG_CARD if i % 2 == 0 else BG_CARD_ALT
        add_rect(s, 0.3, top, 12.7, 1.05, bg)
        add_rect(s, 0.3, top, 0.05, 1.05, color)
        add_textbox(s, hdr_x[0], top+0.05, hdr_w[0], 0.95, init, 10.5, bold=True, color=WHITE)
        add_textbox(s, hdr_x[1], top+0.05, hdr_w[1], 0.95, focus, 10, color=LIGHT_GREY)
        add_textbox(s, hdr_x[2], top+0.05, hdr_w[2], 0.95, timeline, 10.5, bold=True, color=color)
        add_textbox(s, hdr_x[3], top+0.05, hdr_w[3], 0.95, budget, 11, bold=True, color=GOLD)
        add_textbox(s, hdr_x[4], top+0.05, hdr_w[4], 0.95, outcome, 10, color=LIGHT_GREY)
    add_rect(s, 0.3, 7.15, 12.7, 0.35, BG_CARD)
    add_rect(s, 0.3, 7.15, 12.7, 0.04, GOLD)
    add_textbox(s, 0.55, 7.18, 12.2, 0.3,
        "Total 36-Month Investment: ~$10.8M  \u00b7  All figures [Estimated]",
        12, bold=True, color=GOLD, align=PP_ALIGN.CENTER)
    set_notes(s, "Complete roadmap. Total: ~$10.8M over 36 months.")
    return s

# ── SLIDES 31-33: Closing & Appendices ───────────────────────────────────────
def slide_31_closing():
    s = new_slide(); fill_bg(s)
    bar = s.shapes.add_shape(1, Inches(0), Inches(0), Inches(0.10), Inches(7.5))
    bar.fill.solid(); bar.fill.fore_color.rgb = GOLD; bar.line.fill.background()
    add_textbox(s, 0.4, 0.4, 12.0, 0.35,
        "STRATEGIC CONCLUSION", 11, bold=True, color=GOLD)
    add_textbox(s, 0.4, 1.2, 12.0, 1.5,
        "The Future of Industrial\nAutomation Is Physical AI", 42, bold=True, color=WHITE)
    gold_divider(s, 3.0, width=7.0, left=0.4)
    imperatives = [
        ("Position Upstream", "Capture revenue regardless of which hardware vendor wins.", CYAN),
        ("Build V&V First", "Safety certification is the prerequisite for everything else.", GOLD),
        ("Own the Flywheel", "Proprietary physical data from deployments is irreplicable.", CYAN),
        ("Execute Sequentially", "Each priority unlocks the next. No parallel build.", GOLD),
    ]
    for i, (title, desc, color) in enumerate(imperatives):
        top = 3.3 + i * 0.95
        add_rect(s, 0.4, top, 12.3, 0.82, BG_CARD)
        add_rect(s, 0.4, top, 0.06, 0.82, color)
        add_textbox(s, 0.65, top+0.08, 3.2, 0.3, title, 14, bold=True, color=WHITE)
        add_textbox(s, 4.0, top+0.08, 8.5, 0.65, desc, 13, color=LIGHT_GREY)
    add_textbox(s, 0.4, 7.0, 12.0, 0.4,
        "LTTS: the trusted engineering bridge that verifies, integrates, and deploys Physical AI at scale.",
        13, bold=True, color=GOLD, align=PP_ALIGN.CENTER)
    set_notes(s, "Closing: position upstream, V&V first, own the flywheel, execute sequentially.")
    return s

def slide_32_sources():
    s = new_slide(); fill_bg(s)
    module_badge(s, "Appendix A \u00b7 Sources")
    add_textbox(s, 0.3, 0.6, 12.5, 0.8,
        "Comprehensive Sources Index", 30, bold=True, color=WHITE)
    add_textbox(s, 0.3, 1.3, 12.5, 0.4,
        "Cross-Verified Primary Citations", 15, color=GOLD)
    gold_divider(s, 1.82)
    sources = [
        ("Wayve $1.05B Series C", "Corporate Announcement, May 7, 2024. SoftBank, NVIDIA, Microsoft.", GREEN_SOFT),
        ("Figure AI $675M Series B", "Press Release, Feb 29, 2024. $2.6B val. Parkway, Microsoft, OpenAI.", GREEN_SOFT),
        ("PI $400M Series A", "Disclosure, Nov 4, 2024. $2.4B val. Bezos, Thrive, Lux.", GREEN_SOFT),
        ("Skild AI $300M Series A", "Press Release, Jul 9, 2024. $1.5B val. Lightspeed, Coatue.", GREEN_SOFT),
        ("Applied Intuition $6B", "Press Release, Mar 12, 2024. Lux Capital, Elad Gil.", GREEN_SOFT),
        ("Scale AI $13.8B", "Disclosure, May 21, 2024. Led by Accel.", GREEN_SOFT),
        ("Waymo 150k trips/wk", "Alphabet Q3 2024 Earnings, Oct 29, 2024. CEO Sundar Pichai.", GREEN_SOFT),
        ("Pearl's Causal Hierarchy", "Judea Pearl, Causality, Cambridge University Press.", CYAN),
        ("BMW Figure 02 Pilot", "BMW Group Press Release, Aug 2024. Spartanburg.", GREEN_SOFT),
        ("DHL Stretch Deploy", "DHL Supply Chain Announcement, 2024. BD Stretch.", GREEN_SOFT),
    ]
    for i, (source, detail, color) in enumerate(sources):
        top = 1.95 + i * 0.5
        add_textbox(s, 0.55, top, 3.5, 0.32, source, 10.5, bold=True, color=color)
        add_textbox(s, 4.2, top, 8.6, 0.45, detail, 10, color=LIGHT_GREY)
    set_notes(s, "Appendix A: All verified citations with primary source references.")
    return s

def slide_33_critique():
    s = new_slide(); fill_bg(s)
    module_badge(s, "Appendix B \u00b7 Self-Critique")
    add_textbox(s, 0.3, 0.6, 12.5, 0.8,
        "Adversarial Self-Critique Log", 30, bold=True, color=WHITE)
    add_textbox(s, 0.3, 1.3, 12.5, 0.4,
        "Claims Removed or Downgraded Between Drafts", 15, color=GOLD)
    gold_divider(s, 1.82)
    removed = [
        ("Ford 42% Scrap Reduction", "Not in SEC 10-K filings", RED_SOFT),
        ("Airbus <2 PPM Defect Rate", "Unverified extrapolation", RED_SOFT),
        ("Amazon 750k Mobile Robots", "Aggregates legacy AGVs with AI AMRs", ORANGE_SOFT),
        ("GE Vernova $380M Savings", "Vendor projections, not verified", RED_SOFT),
        ("TSMC 2.1x Yield Gain", "Proprietary trade secret", RED_SOFT),
        ("Cat. 620 Trucks / 250M km", "Marketing, not certified data", ORANGE_SOFT),
        ("Intuitive 40% Strain Cut", "Uncontrolled ergonomic claim", ORANGE_SOFT),
        ("Decorative PINN/InfoNCE", "Academic padding, not load-bearing", LIGHT_GREY),
    ]
    for i, (claim, reason, color) in enumerate(removed):
        top = 1.95 + i * 0.62
        add_rect(s, 0.3, top, 12.7, 0.52, BG_CARD if i % 2 == 0 else BG_CARD_ALT)
        add_textbox(s, 0.55, top+0.06, 4.0, 0.35, claim, 11, bold=True, color=color)
        add_textbox(s, 4.8, top+0.06, 7.8, 0.4, reason, 11, color=LIGHT_GREY)
    add_rect(s, 0.3, 7.0, 12.7, 0.5, BG_CARD)
    add_rect(s, 0.3, 7.0, 12.7, 0.04, GOLD)
    add_textbox(s, 0.55, 7.08, 12.2, 0.35,
        "This self-critique is the single most important quality signal in the briefing.",
        12, bold=True, color=GOLD, align=PP_ALIGN.CENTER)
    set_notes(s, "Appendix B: Every removed claim with specific reasoning. Transparency is credibility.")
    return s


# ═══════════════════════════════════════════════════════════════════════════════
#  BUILD
# ═══════════════════════════════════════════════════════════════════════════════
print("Building The Practice of Physical AI v3...")
print("=" * 60)

slides = [
    (slide_01_title,       "Title"),
    (slide_02_taxonomy,    "Verification Taxonomy"),
    (slide_03_exec_summary,"Executive Summary"),
    (slide_04_div,         "Section 1 Divider"),
    (slide_05_maturity,    "Commercial Maturity Tiers"),
    (slide_06_capital,     "Capital Deployment Matrix"),
    (slide_07_asymmetry,   "Capital vs Maturity"),
    (slide_08_div,         "Section 2 Divider"),
    (slide_09_tech,        "Technical Bottlenecks"),
    (slide_10_failures,    "Failure Modes"),
    (slide_11_causal,      "Causal Ladder"),
    (slide_12_div,         "Section 3 Divider"),
    (slide_13_commercial,  "Commercial Models"),
    (slide_14_ltts,        "LTTS Service Offerings"),
    (slide_15_div,         "Section 4 Divider"),
    (slide_16_deployments, "Verified Deployments"),
    (slide_17_hybrid,      "Hybrid Adoption Pattern"),
    (slide_18_div,         "Section 5 Divider"),
    (slide_19_competitive, "Competitive Map"),
    (slide_20_gaps,        "Underserved Gaps"),
    (slide_21_div,         "Section 6 Divider"),
    (slide_22_bridge,      "Industrial vs Physical AI"),
    (slide_23_domain,      "Domain Engineering Moat"),
    (slide_24_flywheel,    "Operational Flywheel"),
    (slide_25_div,         "Section 7 Divider"),
    (slide_26_forecast,    "3-5 Year Forecast"),
    (slide_27_div,         "Section 8 Divider"),
    (slide_28_p1,          "Priority 1 V&V"),
    (slide_29_p234,        "Priorities 2-4"),
    (slide_30_roadmap,     "Roadmap Summary"),
    (slide_31_closing,     "Strategic Conclusion"),
    (slide_32_sources,     "Sources Index"),
    (slide_33_critique,    "Self-Critique Log"),
]

for i, (func, name) in enumerate(slides):
    func()
    print(f"  [{i+1:2d}/{len(slides)}] {name}")

prs.save(OUTPUT)
print(f"\n{'=' * 60}")
print(f"  Presentation saved: {OUTPUT}")
print(f"  Total slides: {len(slides)}")
print(f"{'=' * 60}")
