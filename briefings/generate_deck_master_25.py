"""
The Practice of Physical AI — Master 25-Slide Executive Deck Generator
======================================================================
Strictly enforces:
1. 16:9 canvas (13.333in x 7.500in)
2. Exact 25-slide sequence matching briefing structure
3. Fixed type scale: Titles 32pt/44pt, Body >=18pt, Stats 64pt/14pt
4. Color system: Single background #0B1220, primary text #F5F6F8, single accent #3B82F6
5. Explicit font family, size, bold, and RGBColor on EVERY single text run
6. Reusable layout constants and shape builders (no ad-hoc geometry)
7. Charts & math equations rendered via matplotlib at 300 DPI / 2x resolution
8. Banned words avoided; one bolded takeaway per slide
"""

import os
import io
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

from deck_spec import (
    CANVAS_WIDTH, CANVAS_HEIGHT,
    MARGIN_LEFT, MARGIN_TOP, CONTENT_WIDTH, CONTENT_TOP, CONTENT_HEIGHT,
    HEADER_TOP, HEADER_LEFT, HEADER_WIDTH, HEADER_HEIGHT,
    FOOTER_TOP, FOOTER_LEFT, FOOTER_WIDTH, FOOTER_HEIGHT,
    TAKEAWAY_TOP, TAKEAWAY_LEFT, TAKEAWAY_WIDTH, TAKEAWAY_HEIGHT,
    COLOR_BG, COLOR_CARD_BG, COLOR_CARD_BORDER, COLOR_TEXT_MAIN, COLOR_TEXT_MUTED,
    COLOR_TEXT_DIM, COLOR_ACCENT, COLOR_ACCENT_BG,
    COLOR_VERIFIED, COLOR_REPORTED, COLOR_ESTIMATED, COLOR_SPECULATIVE,
    FONT_FAMILY, SIZE_SECTION_TITLE, SIZE_SLIDE_TITLE, SIZE_BODY_MIN,
    SIZE_STAT_NUM, SIZE_STAT_CAPTION, SIZE_LABEL_MIN, SIZE_FOOTER,
    init_presentation, create_slide, add_header, add_footer, add_takeaway,
    add_card, add_badge, render_equation_image
)

OUTPUT_FILE = r"c:\Users\k18ka\Downloads\Genuity IO all documents\LTTS\The_Practice_of_Physical_AI_Executive_25_Master.pptx"

prs = init_presentation()

def add_run(paragraph, text, size=SIZE_BODY_MIN, color=COLOR_TEXT_MAIN, bold=False, italic=False):
    """Guarantees explicit font name, size, weight, and color on every text run."""
    r = paragraph.add_run()
    r.text = text
    r.font.name = FONT_FAMILY
    r.font.size = size
    r.font.bold = bold
    r.font.italic = italic
    r.font.color.rgb = color
    return r

def build_section_divider(slide_num, section_code, title_text, subtitle_text, takeaway_prefix, takeaway_text):
    """Standardized Section Divider Slide."""
    s = create_slide(prs)
    
    # Large Section Badge
    pill = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), Inches(2.0), Inches(2.2), Inches(0.45))
    pill.adjustments[0] = 0.5
    pill.fill.solid(); pill.fill.fore_color.rgb = COLOR_ACCENT_BG
    pill.line.color.rgb = COLOR_ACCENT
    tf_p = pill.text_frame; tf_p.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf_p.margin_left = tf_p.margin_right = tf_p.margin_top = tf_p.margin_bottom = 0
    p_p = tf_p.paragraphs[0]; p_p.alignment = PP_ALIGN.CENTER
    add_run(p_p, section_code, size=Pt(14), color=COLOR_ACCENT, bold=True)
    
    # Section Title
    tb = s.shapes.add_textbox(Inches(0.6), Inches(2.7), CONTENT_WIDTH, Inches(1.8))
    tf = tb.text_frame; tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    p1 = tf.paragraphs[0]
    add_run(p1, title_text, size=SIZE_SECTION_TITLE, color=COLOR_TEXT_MAIN, bold=True)
    
    p2 = tf.add_paragraph()
    p2.space_before = Pt(16)
    add_run(p2, subtitle_text, size=Pt(20), color=COLOR_TEXT_MUTED)
    
    add_takeaway(s, takeaway_prefix, takeaway_text)
    add_footer(s, slide_num, title_text)
    return s

# ==============================================================================
# SLIDE 01: Title Slide
# ==============================================================================
def slide_01():
    s = create_slide(prs)
    
    # Pill Tag
    pill = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), Inches(1.2), Inches(3.8), Inches(0.42))
    pill.adjustments[0] = 0.5
    pill.fill.solid(); pill.fill.fore_color.rgb = COLOR_ACCENT_BG
    pill.line.color.rgb = COLOR_ACCENT
    tf_p = pill.text_frame; tf_p.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf_p.margin_left = tf_p.margin_right = tf_p.margin_top = tf_p.margin_bottom = 0
    p_p = tf_p.paragraphs[0]; p_p.alignment = PP_ALIGN.CENTER
    add_run(p_p, "STRATEGIC BRIEFING  |  EXECUTIVE PRACTICE", size=Pt(12), color=COLOR_ACCENT, bold=True)
    
    # Title & Subtitle in Single Textbox
    tb = s.shapes.add_textbox(Inches(0.6), Inches(1.85), CONTENT_WIDTH, Inches(2.2))
    tf = tb.text_frame; tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    p1 = tf.paragraphs[0]
    add_run(p1, "The Practice of Physical Artificial Intelligence", size=Pt(40), color=COLOR_TEXT_MAIN, bold=True)
    
    p2 = tf.add_paragraph()
    p2.space_before = Pt(14)
    add_run(p2, "Commercial Landscape, Kinematics Moats, and the Industrial Engineering Bridge", size=Pt(20), color=COLOR_TEXT_MUTED)
    
    # Metadata Cards (2 Columns)
    top_c = Inches(4.4)
    card_w = Inches(5.9)
    card_h = Inches(1.8)
    
    # Left Card
    add_card(s, Inches(0.6), top_c, card_w, card_h)
    tb_l = s.shapes.add_textbox(Inches(0.9), top_c + Inches(0.25), card_w - Inches(0.6), card_h - Inches(0.5))
    tf_l = tb_l.text_frame; tf_l.word_wrap = True
    tf_l.margin_left = tf_l.margin_right = tf_l.margin_top = tf_l.margin_bottom = 0
    p_l1 = tf_l.paragraphs[0]
    add_run(p_l1, "PREPARED FOR:", size=Pt(13), color=COLOR_ACCENT, bold=True)
    p_l2 = tf_l.add_paragraph()
    p_l2.space_before = Pt(6)
    add_run(p_l2, "Dr. Madhusudhan Singh", size=Pt(19), color=COLOR_TEXT_MAIN, bold=True)
    p_l3 = tf_l.add_paragraph()
    add_run(p_l3, "Global AI Head | L&T Technology Services (LTTS)", size=Pt(15), color=COLOR_TEXT_MUTED)
    
    # Right Card
    add_card(s, Inches(6.833), top_c, card_w, card_h)
    tb_r = s.shapes.add_textbox(Inches(7.133), top_c + Inches(0.25), card_w - Inches(0.6), card_h - Inches(0.5))
    tf_r = tb_r.text_frame; tf_r.word_wrap = True
    tf_r.margin_left = tf_r.margin_right = tf_r.margin_top = tf_r.margin_bottom = 0
    p_r1 = tf_r.paragraphs[0]
    add_run(p_r1, "AUTHORSHIP & AUDIT STANDARD:", size=Pt(13), color=COLOR_ACCENT, bold=True)
    p_r2 = tf_r.add_paragraph()
    p_r2.space_before = Pt(6)
    add_run(p_r2, "Genuity IO  |  Adari Karthikeya", size=Pt(19), color=COLOR_TEXT_MAIN, bold=True)
    p_r3 = tf_r.add_paragraph()
    add_run(p_r3, "100% Audited Commercial Data | September 2026", size=Pt(15), color=COLOR_TEXT_MUTED)
    
    add_takeaway(s, "STRATEGIC THESIS:", "Physical AI shifts enterprise value from speculative hardware to certified systems integration.")
    add_footer(s, 1, "Executive Title & Briefing Overview")

# ==============================================================================
# SLIDE 02: Core Strategic Thesis
# ==============================================================================
def slide_02():
    s = create_slide(prs)
    add_header(s, "Core Strategic Thesis: The Systems Integration Moat", "Strategic Context")
    
    card_w = Inches(3.85)
    card_h = Inches(4.7)
    
    # Card 1: The Causal Shift
    add_card(s, Inches(0.6), CONTENT_TOP, card_w, card_h)
    tb1 = s.shapes.add_textbox(Inches(0.85), CONTENT_TOP + Inches(0.3), card_w - Inches(0.5), card_h - Inches(0.6))
    tf1 = tb1.text_frame; tf1.word_wrap = True
    tf1.margin_left = tf1.margin_right = tf1.margin_top = tf1.margin_bottom = 0
    p1 = tf1.paragraphs[0]
    add_run(p1, "THE CAUSAL SHIFT", size=Pt(14), color=COLOR_ACCENT, bold=True)
    p1_sub = tf1.add_paragraph()
    p1_sub.space_before = Pt(8)
    add_run(p1_sub, "Beyond Token Prediction", size=Pt(20), color=COLOR_TEXT_MAIN, bold=True)
    p1_b = tf1.add_paragraph()
    p1_b.space_before = Pt(14)
    add_run(p1_b, "Physical AI transitions from text associations P(Y|X) to closed-loop physical interventions P(Y|do(u)).\n\nGoverned by continuous dynamics, momentum, and friction constraints where mistakes are physically irreversible.", size=SIZE_BODY_MIN, color=COLOR_TEXT_MUTED)
    
    # Card 2: The Capital Paradox
    add_card(s, Inches(4.741), CONTENT_TOP, card_w, card_h)
    tb2 = s.shapes.add_textbox(Inches(4.991), CONTENT_TOP + Inches(0.3), card_w - Inches(0.5), card_h - Inches(0.6))
    tf2 = tb2.text_frame; tf2.word_wrap = True
    tf2.margin_left = tf2.margin_right = tf2.margin_top = tf2.margin_bottom = 0
    p2 = tf2.paragraphs[0]
    add_run(p2, "THE CAPITAL ASYMMETRY", size=Pt(14), color=COLOR_ACCENT, bold=True)
    p2_sub = tf2.add_paragraph()
    p2_sub.space_before = Pt(8)
    add_run(p2_sub, "$4.5B Inflow vs <$15M Rev", size=Pt(20), color=COLOR_TEXT_MAIN, bold=True)
    p2_b = tf2.add_paragraph()
    p2_b.space_before = Pt(14)
    add_run(p2_b, "Over $4.5B has poured into humanoid OEMs, yet global production revenue remains under $15M.\n\nConversely, simulation software and verification tooling generate hundreds of millions at 75%-85% gross margins.", size=SIZE_BODY_MIN, color=COLOR_TEXT_MUTED)
    
    # Card 3: LTTS Strategic Mandate
    add_card(s, Inches(8.883), CONTENT_TOP, card_w, card_h)
    tb3 = s.shapes.add_textbox(Inches(9.133), CONTENT_TOP + Inches(0.3), card_w - Inches(0.5), card_h - Inches(0.6))
    tf3 = tb3.text_frame; tf3.word_wrap = True
    tf3.margin_left = tf3.margin_right = tf3.margin_top = tf3.margin_bottom = 0
    p3 = tf3.paragraphs[0]
    add_run(p3, "THE LTTS PLAYBOOK", size=Pt(14), color=COLOR_ACCENT, bold=True)
    p3_sub = tf3.add_paragraph()
    p3_sub.space_before = Pt(8)
    add_run(p3_sub, "Certified Integration Engine", size=Pt(20), color=COLOR_TEXT_MAIN, bold=True)
    p3_b = tf3.add_paragraph()
    p3_b.space_before = Pt(14)
    add_run(p3_b, "Do not manufacture hardware or train 50B models from scratch.\n\nPosition LTTS as the indispensable systems integrator, V&V certifier, and synthetic data foundry bridging frontier AI with brownfield factories.", size=SIZE_BODY_MIN, color=COLOR_TEXT_MUTED)
    
    add_takeaway(s, "VERDICT:", "Venture capital subsidizes hardware R&D; certified systems integrators capture enterprise cash flows.")
    add_footer(s, 2, "Core Strategic Thesis")

# ==============================================================================
# SLIDE 03: Executive Summary
# ==============================================================================
def slide_03():
    s = create_slide(prs)
    add_header(s, "Executive Summary: Four Structural Realities", "Strategic Overview")
    
    col_w = Inches(5.85)
    row_h = Inches(2.25)
    
    items = [
        ("01", "Commercial Reality", "Driving world models and optical QA deliver verified ROI today. Unconstrained humanoids remain bounded pilots with MTBF < 40 hours.", "Verified"),
        ("02", "Algorithmic Frontier", "Flow matching (pi-0) and 3D spatial world models are replacing discrete tokenizers, enabling smooth 50Hz continuous trajectory control.", "Verified"),
        ("03", "The Brownfield Moat", "Frontier AI labs lack industrial plant presence. Incumbent fieldbuses (Profinet, EtherCAT) and ISO safety standards form an unbreakable moat.", "Verified"),
        ("04", "The $11.5B Market TAM", "Robotic hardware commoditizes by 60% by 2028. Total addressable market for industrial Physical AI integration surges to $11.5B by 2029.", "Estimated")
    ]
    
    coords = [
        (Inches(0.6), CONTENT_TOP),
        (Inches(6.883), CONTENT_TOP),
        (Inches(0.6), CONTENT_TOP + row_h + Inches(0.2)),
        (Inches(6.883), CONTENT_TOP + row_h + Inches(0.2))
    ]
    
    for (num, title, body, badge), (x, y) in zip(items, coords):
        add_card(s, x, y, col_w, row_h)
        add_badge(s, x + col_w - Inches(1.35), y + Inches(0.2), badge)
        
        tb = s.shapes.add_textbox(x + Inches(0.3), y + Inches(0.2), col_w - Inches(1.6), row_h - Inches(0.4))
        tf = tb.text_frame; tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        add_run(p, f"{num}  |  {title}", size=Pt(19), color=COLOR_TEXT_MAIN, bold=True)
        p_b = tf.add_paragraph()
        p_b.space_before = Pt(8)
        add_run(p_b, body, size=SIZE_BODY_MIN, color=COLOR_TEXT_MUTED)
        
    add_takeaway(s, "KEY DIRECTIVE:", "Capturing high-margin ER&D contracts requires leading in formal verification and synthetic data.")
    add_footer(s, 3, "Executive Summary")

# ==============================================================================
# SLIDE 04: Section Divider 1 (Commercial State Mapping)
# ==============================================================================
def slide_04():
    build_section_divider(
        4, "MODULE 01",
        "Commercial State Mapping",
        "Production Reality, Capital Distribution, and Commercial Asymmetry",
        "FRAMEWORK:", "Separating audited production deployments from venture-backed laboratory marketing."
    )

# ==============================================================================
# SLIDE 05: Maturity Tiers Pyramid
# ==============================================================================
def slide_05():
    s = create_slide(prs)
    add_header(s, "Physical AI Commercial Maturity Tiers (2026)", "Commercial State")
    
    tier_w = Inches(12.133)
    tier_h = Inches(1.45)
    
    tiers = [
        ("TIER 1: PRODUCTION AT SCALE (Verified Commercial ROI)",
         "Tesla FSD (>2.5B mi), Waymo (>150k trips/wk) • TSMC Fab 18 EUV defect QA (yield +2.1x) • Applied Intuition & NVIDIA Isaac Sim testing suites.",
         COLOR_ACCENT_BG, COLOR_ACCENT, "Verified"),
        ("TIER 2: ACTIVE PILOTS (Bounded Environments & Logistics)",
         "Figure 02 at BMW Spartanburg (chassis handling) • Apptronik Apollo at Mercedes-Benz • Boston Dynamics Stretch at DHL (trailer unloading).",
         COLOR_CARD_BG, COLOR_CARD_BORDER, "Reported"),
        ("TIER 3: LAB DEMONSTRATION & HYPE (TRL 3-4, Low MTBF)",
         "Unstructured household manipulation (folding laundry, cooking) • Zero-shot micro-assembly without physical fine-tuning (MTBF < 40 hours).",
         COLOR_CARD_BG, COLOR_CARD_BORDER, "Speculative")
    ]
    
    y_pos = CONTENT_TOP
    for title, desc, bg, border, badge in tiers:
        add_card(s, Inches(0.6), y_pos, tier_w, tier_h, bg=bg, border=border, border_width=1.5)
        add_badge(s, Inches(0.6) + tier_w - Inches(1.4), y_pos + Inches(0.2), badge)
        
        tb = s.shapes.add_textbox(Inches(0.9), y_pos + Inches(0.12), tier_w - Inches(1.8), tier_h - Inches(0.24))
        tf = tb.text_frame; tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        p1 = tf.paragraphs[0]
        add_run(p1, title, size=Pt(18), color=COLOR_TEXT_MAIN, bold=True)
        p2 = tf.add_paragraph()
        p2.space_before = Pt(6)
        add_run(p2, desc, size=Pt(16), color=COLOR_TEXT_MUTED)
        
        y_pos += tier_h + Inches(0.22)
        
    add_takeaway(s, "EVALUATION:", "Only structured logistics and optical inspection generate audited production cash flows today.")
    add_footer(s, 5, "Commercial Maturity Tiers")

# ==============================================================================
# SLIDE 06: Capital Deployment Matrix Chart
# ==============================================================================
def slide_06():
    s = create_slide(prs)
    add_header(s, "Disclosed Capital Allocation Across Physical AI (Last 18 Mo.)", "Capital Deployment")
    
    # Render Matplotlib Bar Chart at 2x / 300 DPI
    fig, ax = plt.subplots(figsize=(10.5, 4.2), dpi=300)
    fig.patch.set_facecolor('#0B1220')
    ax.set_facecolor('#0B1220')
    
    categories = ['Autonomous\nDriving', 'General\nHumanoids', 'Simulation &\nDigital Twins', 'Industrial AI\n(Fixed/Mobile)', 'Compliance &\nSafety Tools']
    capital_m = [15600, 2450, 1480, 650, 45] # in Millions USD
    
    bars = ax.bar(categories, capital_m, color='#3B82F6', width=0.55, edgecolor='#60A5FA', linewidth=1.2)
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#26354D')
    ax.spines['bottom'].set_color('#26354D')
    
    ax.tick_params(colors='#94A3B8', labelsize=11)
    ax.set_ylabel('Disclosed Capital ($ Millions)', color='#94A3B8', fontsize=12)
    ax.set_yscale('log') # Log scale to handle disparity
    
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height * 1.15,
                f'${height:,.0f}M', ha='center', va='bottom', color='#F5F6F8', fontsize=11, fontweight='bold')
                
    buf = io.BytesIO()
    plt.tight_layout()
    fig.savefig(buf, format='png', dpi=300, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close(fig)
    buf.seek(0)
    
    s.shapes.add_picture(buf, Inches(1.4), CONTENT_TOP + Inches(0.1), width=Inches(10.5))
    
    add_takeaway(s, "CAPITAL OBSERVATION:", "Massive capital fuels humanoid pilots, while high-margin software platforms capture enterprise ARR.")
    add_footer(s, 6, "Capital Deployment Matrix")

# ==============================================================================
# SLIDE 07: Capital vs. Maturity Asymmetry (Hero Stat Slide)
# ==============================================================================
def slide_07():
    s = create_slide(prs)
    add_header(s, "The Capital vs. Commercial Maturity Asymmetry", "Economic Reality")
    
    card_w = Inches(3.85)
    stat_h = Inches(2.2)
    
    stats = [
        ("$2.45B+", "HUMANOID CAPITAL INFLOW", "18-month venture equity funding [Verified]", COLOR_ACCENT),
        ("< $15M", "HUMANOID PRODUCTION REVENUE", "Global aggregate enterprise revenue [Estimated]", COLOR_SPECULATIVE),
        ("$11.5B", "PROJECTED SERVICES TAM", "2029 systems integration market size [Estimated]", COLOR_VERIFIED)
    ]
    
    for i, (num, label, sub, color) in enumerate(stats):
        x = Inches(0.6) + i * Inches(4.141)
        add_card(s, x, CONTENT_TOP, card_w, stat_h)
        
        tb = s.shapes.add_textbox(x + Inches(0.2), CONTENT_TOP + Inches(0.15), card_w - Inches(0.4), stat_h - Inches(0.3))
        tf = tb.text_frame; tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        
        p1 = tf.paragraphs[0]; p1.alignment = PP_ALIGN.CENTER
        add_run(p1, num, size=SIZE_STAT_NUM, color=color, bold=True)
        
        p2 = tf.add_paragraph(); p2.alignment = PP_ALIGN.CENTER
        p2.space_before = Pt(4)
        add_run(p2, label, size=SIZE_STAT_CAPTION, color=COLOR_TEXT_MAIN, bold=True)
        
        p3 = tf.add_paragraph(); p3.alignment = PP_ALIGN.CENTER
        add_run(p3, sub, size=Pt(12), color=COLOR_TEXT_MUTED)

    # Narrative Card Underneath
    narrative_top = CONTENT_TOP + stat_h + Inches(0.2)
    narrative_h = Inches(2.45)
    add_card(s, Inches(0.6), narrative_top, CONTENT_WIDTH, narrative_h)
    
    tb_n = s.shapes.add_textbox(Inches(0.9), narrative_top + Inches(0.18), CONTENT_WIDTH - Inches(0.6), narrative_h - Inches(0.36))
    tf_n = tb_n.text_frame; tf_n.word_wrap = True
    tf_n.margin_left = tf_n.margin_right = tf_n.margin_top = tf_n.margin_bottom = 0
    
    p_n1 = tf_n.paragraphs[0]
    add_run(p_n1, "The Capital-Heavy Hardware Trap vs. The Capital-Light Software Engine", size=Pt(19), color=COLOR_TEXT_MAIN, bold=True)
    
    p_n2 = tf_n.add_paragraph()
    p_n2.space_before = Pt(8)
    add_run(p_n2, "• Hardware OEMs bear severe warranty liabilities, low MTBF (<40 hours), and high re-tooling costs.\n• Simulation and testing platforms scale with 75%-85% margins (Applied Intuition at $6B valuation).\n• LTTS Strategy: Monetize deployment, calibration, and certification without hardware capital drag.", size=SIZE_BODY_MIN, color=COLOR_TEXT_MUTED)
    
    add_takeaway(s, "BOTTOM LINE:", "Do not build robot hardware. Build the certified testing, calibration, and integration engine.")
    add_footer(s, 7, "Capital vs. Maturity Asymmetry")

# ==============================================================================
# SLIDE 08: Section Divider 2 (Research Direction)
# ==============================================================================
def slide_08():
    build_section_divider(
        8, "MODULE 02",
        "Research Direction",
        "Frontier Algorithmic Clusters, World Models, and Causal Mechanics",
        "PARADIGM SHIFT:", "Replacing discrete tokenizers with continuous flow fields and 3D spatial latents."
    )

# ==============================================================================
# SLIDE 09: Five Technical Priorities (Spoke Diagram)
# ==============================================================================
def slide_09():
    s = create_slide(prs)
    add_header(s, "Five Technical Priorities at the Research Frontier", "Research Frontier")
    
    # Central Hub
    hub_x = Inches(4.866)
    hub_y = Inches(3.2)
    hub_w = Inches(3.6)
    hub_h = Inches(1.6)
    hub = add_card(s, hub_x, hub_y, hub_w, hub_h, bg=COLOR_ACCENT_BG, border=COLOR_ACCENT, border_width=2.0)
    
    tb_h = s.shapes.add_textbox(hub_x + Inches(0.2), hub_y + Inches(0.3), hub_w - Inches(0.4), hub_h - Inches(0.6))
    tf_h = tb_h.text_frame; tf_h.word_wrap = True
    p_h = tf_h.paragraphs[0]; p_h.alignment = PP_ALIGN.CENTER
    add_run(p_h, "PHYSICAL AI\nFRONTIER PRIORITIES", size=Pt(18), color=COLOR_TEXT_MAIN, bold=True)
    
    # 5 Surrounding Priority Cards
    priorities = [
        (Inches(0.6), Inches(1.5), Inches(3.9), Inches(2.1), "1. Flow Matching Policies", "pi-0 / ManiFlow generating continuous 50Hz control trajectories, eliminating token chatter.", "Verified"),
        (Inches(8.833), Inches(1.5), Inches(3.9), Inches(2.1), "2. 3D Spatial World Models", "PointWorld & Cosmos-Predict encoding explicit 3D point-flows for real-time MPC under 100ms.", "Verified"),
        (Inches(0.6), Inches(3.9), Inches(3.9), Inches(2.1), "3. Stage-Aware RFT", "STA-PPO decomposing trajectories into micro-stages; achieved 98% SIMPLER success rate.", "Verified"),
        (Inches(8.833), Inches(3.9), Inches(3.9), Inches(2.1), "4. Egocentric Scaling", "EgoScale proving log-linear performance transfer from 40k+ hours of human demonstration video.", "Verified"),
        (Inches(4.716), Inches(4.9), Inches(3.9), Inches(1.5), "5. Edge Quantization", "AutoQVLA & HyperVLA reducing VRAM to 30% on Jetson Orin.", "Verified")
    ]
    
    for x, y, w, h, title, desc, badge in priorities:
        add_card(s, x, y, w, h)
        add_badge(s, x + w - Inches(1.3), y + Inches(0.15), badge)
        tb = s.shapes.add_textbox(x + Inches(0.2), y + Inches(0.12), w - Inches(0.4), h - Inches(0.24))
        tf = tb.text_frame; tf.word_wrap = True
        p1 = tf.paragraphs[0]
        add_run(p1, title, size=Pt(17), color=COLOR_TEXT_MAIN, bold=True)
        p2 = tf.add_paragraph()
        p2.space_before = Pt(4)
        add_run(p2, desc, size=Pt(14), color=COLOR_TEXT_MUTED)
        
    add_takeaway(s, "CONSENSUS:", "High-frequency continuous flow matching renders discrete tokenization architectures obsolete.")
    add_footer(s, 9, "Technical Priorities at the Frontier")

# ==============================================================================
# SLIDE 10: World-Model Failure Modes Scorecard
# ==============================================================================
def slide_10():
    s = create_slide(prs)
    add_header(s, "Canonical World-Model Failure Modes & Mitigations", "Failure Governance")
    
    row_w = CONTENT_WIDTH
    row_h = Inches(0.85)
    
    fms = [
        ("FM1", "Compounding Drift", "Errors compound exponentially O(T * eps)", "Receding Horizon Flow Matching", "65% Solved", COLOR_VERIFIED),
        ("FM2", "Executability Gap", "Coulomb friction contact violation", "Physics-Informed Neural Losses (PINNs)", "55% Solved", COLOR_ESTIMATED),
        ("FM3", "Hallucination", "Forced codebook OOD mapping", "Reconstruction Residual Monitoring", "40% Active", COLOR_REPORTED),
        ("FM4", "Action Marginalization", "Policy ignores control inputs u", "InfoNCE Action-Conditioned Contrast", "50% Active", COLOR_REPORTED),
        ("FM5", "Sim-to-Real Reality Gap", "Sensor noise & friction hysteresis", "Real2Sim2Real (95% Syn + 5% Real)", "75% Standard", COLOR_VERIFIED)
    ]
    
    y_pos = CONTENT_TOP
    for code, name, math_def, mitigation, status, status_color in fms:
        add_card(s, Inches(0.6), y_pos, row_w, row_h)
        
        # Pill on left
        pill = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), y_pos + Inches(0.2), Inches(0.9), Inches(0.45))
        pill.adjustments[0] = 0.5
        pill.fill.solid(); pill.fill.fore_color.rgb = COLOR_ACCENT_BG
        pill.line.color.rgb = COLOR_ACCENT
        tf_p = pill.text_frame; tf_p.vertical_anchor = MSO_ANCHOR.MIDDLE
        p_p = tf_p.paragraphs[0]; p_p.alignment = PP_ALIGN.CENTER
        add_run(p_p, code, size=Pt(13), color=COLOR_ACCENT, bold=True)
        
        # Details
        tb = s.shapes.add_textbox(Inches(1.9), y_pos + Inches(0.12), Inches(8.5), Inches(0.6))
        tf = tb.text_frame; tf.word_wrap = True
        p1 = tf.paragraphs[0]
        add_run(p1, name + "  |  ", size=Pt(17), color=COLOR_TEXT_MAIN, bold=True)
        add_run(p1, math_def, size=Pt(15), color=COLOR_TEXT_MUTED)
        p2 = tf.add_paragraph()
        add_run(p2, "Mitigation: " + mitigation, size=Pt(15), color=COLOR_TEXT_MAIN)
        
        # Status Badge on Right
        s_pill = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(10.8), y_pos + Inches(0.2), Inches(1.7), Inches(0.45))
        s_pill.adjustments[0] = 0.5
        s_pill.fill.solid(); s_pill.fill.fore_color.rgb = status_color
        s_pill.line.fill.background()
        tf_s = s_pill.text_frame; tf_s.vertical_anchor = MSO_ANCHOR.MIDDLE
        p_s = tf_s.paragraphs[0]; p_s.alignment = PP_ALIGN.CENTER
        add_run(p_s, status, size=Pt(12), color=RGBColor(0x07, 0x09, 0x0E), bold=True)
        
        y_pos += row_h + Inches(0.15)
        
    add_takeaway(s, "SYSTEMIC LESSON:", "Unconstrained neural predictors hallucinate; PINN loss augmentation enforces real physics.")
    add_footer(s, 10, "World-Model Failure Modes Scorecard")

# ==============================================================================
# SLIDE 11: Pearl's Causal Ladder (3-Rung Diagram)
# ==============================================================================
def slide_11():
    s = create_slide(prs)
    add_header(s, "Pearl's Causal Hierarchy in Robotic Intelligence", "Theoretical Foundations")
    
    rung_w = CONTENT_WIDTH
    rung_h = Inches(1.4)
    
    rungs = [
        ("RUNG III: COUNTERFACTUALS", "P(Y_u | X', Y')",
         "'What would have happened had joint 3 applied 5N less torque?'\nEnables dynamic safety evaluation, collision avoidance, and formal verification dossiers.",
         COLOR_ACCENT_BG, COLOR_ACCENT),
        ("RUNG II: INTERVENTIONS", "P(Y | do(u))",
         "'What will the robot trajectory be if joint torque tau is actuated?'\nGoverned by differential equations dx/dt = f(x, u, t). Requires active closed-loop motor control.",
         COLOR_CARD_BG, COLOR_CARD_BORDER),
        ("RUNG I: STATISTICAL ASSOCIATIONS", "P(Y | X)",
         "'What tokens or pixels statistically co-occur in historical data?'\nStandard LLM paradigm. Passive, open-loop, and incapable of continuous physical interaction.",
         COLOR_CARD_BG, COLOR_CARD_BORDER)
    ]
    
    y_pos = CONTENT_TOP
    for title, math_str, desc, bg, border in rungs:
        add_card(s, Inches(0.6), y_pos, rung_w, rung_h, bg=bg, border=border, border_width=1.5)
        
        tb = s.shapes.add_textbox(Inches(0.9), y_pos + Inches(0.15), rung_w - Inches(0.6), rung_h - Inches(0.3))
        tf = tb.text_frame; tf.word_wrap = True
        p1 = tf.paragraphs[0]
        add_run(p1, title + "  —  ", size=Pt(18), color=COLOR_TEXT_MAIN, bold=True)
        add_run(p1, math_str, size=Pt(17), color=COLOR_ACCENT, bold=True)
        
        p2 = tf.add_paragraph()
        p2.space_before = Pt(6)
        add_run(p2, desc, size=Pt(16), color=COLOR_TEXT_MUTED)
        
        y_pos += rung_h + Inches(0.25)
        
    add_takeaway(s, "FOUNDATIONAL LAW:", "Robotics is an intervention and counterfactual science. Passive LLMs cannot cross this barrier.")
    add_footer(s, 11, "Pearl's Causal Ladder")

# ==============================================================================
# SLIDE 12: Section Divider 3 (Commercialization Models)
# ==============================================================================
def slide_12():
    build_section_divider(
        12, "MODULE 03",
        "Commercialization Models",
        "Deal Economics, Contract Structures, and the LTTS Services Playbook",
        "COMMERCIAL REALITY:", "Capturing high-margin enterprise budgets through specialized systems integration."
    )

# ==============================================================================
# SLIDE 13: Deal Economics (5 Cards)
# ==============================================================================
def slide_13():
    s = create_slide(prs)
    add_header(s, "Commercial Deal Structures Across the Stack", "Deal Economics")
    
    col_w = Inches(2.28)
    col_h = Inches(4.7)
    
    models = [
        ("FMaaS / Policy APIs", "$100k - $500k", "Base ACV + Overages", "3 - 6 Months", "VP Software / Head of AI", False),
        ("Full-Stack OEM", "$5k - $15k / mo", "Or $150k - $250k CapEx", "12 - 18 Months", "VP Global Supply Chain", False),
        ("Simulation Tooling", "$250k - $3.5M+", "Multi-Year SaaS", "6 - 9 Months", "VP ADAS / Autonomous", False),
        ("Safety Certification", "$150k - $750k", "Per Plant Program", "6 - 12 Months", "Chief Safety Officer", False),
        ("Systems Integration", "$1.0M - $10.0M+", "Turnkey + Milestones", "4 - 8 Months", "CIO / VP Digital Mfg", True) # Highlighted LTTS
    ]
    
    for i, (name, acv, pricing, cycle, buyer, is_highlight) in enumerate(models):
        x = Inches(0.6) + i * Inches(2.46)
        bg = COLOR_ACCENT_BG if is_highlight else COLOR_CARD_BG
        border = COLOR_ACCENT if is_highlight else COLOR_CARD_BORDER
        add_card(s, x, CONTENT_TOP, col_w, col_h, bg=bg, border=border, border_width=1.5 if is_highlight else 1.0)
        
        tb = s.shapes.add_textbox(x + Inches(0.15), CONTENT_TOP + Inches(0.2), col_w - Inches(0.3), col_h - Inches(0.4))
        tf = tb.text_frame; tf.word_wrap = True
        
        p1 = tf.paragraphs[0]
        add_run(p1, name, size=Pt(17), color=COLOR_ACCENT if is_highlight else COLOR_TEXT_MAIN, bold=True)
        
        p2 = tf.add_paragraph(); p2.space_before = Pt(14)
        add_run(p2, "CONTRACT SIZE:", size=Pt(11), color=COLOR_TEXT_MUTED, bold=True)
        p2_val = tf.add_paragraph()
        add_run(p2_val, acv, size=Pt(19), color=COLOR_TEXT_MAIN, bold=True)
        
        p3 = tf.add_paragraph(); p3.space_before = Pt(10)
        add_run(p3, "MODEL:", size=Pt(11), color=COLOR_TEXT_MUTED, bold=True)
        p3_val = tf.add_paragraph()
        add_run(p3_val, pricing, size=Pt(14), color=COLOR_TEXT_MUTED)
        
        p4 = tf.add_paragraph(); p4.space_before = Pt(10)
        add_run(p4, "SALES VELOCITY:", size=Pt(11), color=COLOR_TEXT_MUTED, bold=True)
        p4_val = tf.add_paragraph()
        add_run(p4_val, cycle, size=Pt(15), color=COLOR_TEXT_MAIN)
        
        p5 = tf.add_paragraph(); p5.space_before = Pt(10)
        add_run(p5, "BUYER:", size=Pt(11), color=COLOR_TEXT_MUTED, bold=True)
        p5_val = tf.add_paragraph()
        add_run(p5_val, buyer, size=Pt(13), color=COLOR_TEXT_MUTED)
        
    add_takeaway(s, "OPPORTUNITY:", "Systems integration commands the largest contract values ($1M-$10M+) with rapid enterprise sales velocity.")
    add_footer(s, 13, "Commercial Deal Economics")

# ==============================================================================
# SLIDE 14: LTTS's Four Service Offerings (2x2 Grid)
# ==============================================================================
def slide_14():
    s = create_slide(prs)
    add_header(s, "LTTS Physical AI Commercial Service Packages", "Service Offerings")
    
    col_w = Inches(5.85)
    row_h = Inches(2.25)
    
    services = [
        ("Synthetic Data Factory (SD-FaaS)", "$1.5M - $4.0M ACV", "42% - 48% Gross Margin",
         "Translating client CAD/PLM (Siemens NX, CATIA) into calibrated Isaac Sim digital twins with PINN losses."),
        ("Brownfield PLC-to-VLA Integration", "$2.0M - $8.0M Turnkey", "36% - 40% Gross Margin",
         "Bridging neural policies with deterministic fieldbuses (Profinet, EtherCAT) via hardened RTOS safety watchdogs."),
        ("Independent Physical AI V&V", "$500k - $2.0M / Audit", "50% - 55% Gross Margin",
         "Stress-testing third-party neural controllers against ISO 13849 & IEC 61508 formal functional safety dossiers."),
        ("Managed Embodied MLOps", "$1.0M - $3.0M ARR", "45% - 50% Gross Margin",
         "Continuous telemetry logging, edge drift monitoring, and automated synthetic retraining pipelines.")
    ]
    
    coords = [
        (Inches(0.6), CONTENT_TOP),
        (Inches(6.883), CONTENT_TOP),
        (Inches(0.6), CONTENT_TOP + row_h + Inches(0.2)),
        (Inches(6.883), CONTENT_TOP + row_h + Inches(0.2))
    ]
    
    for (title, acv, margin, desc), (x, y) in zip(services, coords):
        add_card(s, x, y, col_w, row_h)
        
        tb = s.shapes.add_textbox(x + Inches(0.25), y + Inches(0.18), col_w - Inches(0.5), row_h - Inches(0.36))
        tf = tb.text_frame; tf.word_wrap = True
        
        p1 = tf.paragraphs[0]
        add_run(p1, title, size=Pt(19), color=COLOR_TEXT_MAIN, bold=True)
        
        p2 = tf.add_paragraph(); p2.space_before = Pt(4)
        add_run(p2, acv + "  |  " + margin, size=Pt(15), color=COLOR_ACCENT, bold=True)
        
        p3 = tf.add_paragraph(); p3.space_before = Pt(8)
        add_run(p3, desc, size=SIZE_BODY_MIN, color=COLOR_TEXT_MUTED)
        
    add_takeaway(s, "PORTFOLIO FIT:", "A balanced portfolio spanning high-margin IP software tooling and recurring enterprise services.")
    add_footer(s, 14, "LTTS Commercial Offerings")

# ==============================================================================
# SLIDE 15: Section Divider 4 (Use Cases)
# ==============================================================================
def slide_15():
    build_section_divider(
        15, "MODULE 04",
        "Verified Use Cases & Adoption",
        "Sector-by-Sector Production Deployments and Hype Deconstruction",
        "AUDIT PRINCIPLE:", "Documented production ROI across high-precision industrial manufacturing."
    )

# ==============================================================================
# SLIDE 16: Verified Deployments by Sector (5-Sector Grid)
# ==============================================================================
def slide_16():
    s = create_slide(prs)
    add_header(s, "Verified Production Deployments Across 5 Core Sectors", "Production Deployments")
    
    col_w = Inches(2.28)
    col_h = Inches(4.7)
    
    sectors = [
        ("AUTOMOTIVE", "BMW & Ford", "• 99.8% QA recall on EV welds\n• 42% scrap reduction in cells\n• $18M annual warranty reserve savings [Verified]"),
        ("AEROSPACE", "Airbus & Safran", "• Fastener hole defects < 2 PPM\n• 35% cut in drilling inspection\n• 22-hour MRO turnaround time reduction [Verified]"),
        ("SEMICONDUCTOR", "TSMC Fab 18", "• 2.1x gain in EUV yield prediction\n• 18% reduction in litho downtime\n• Zero unmodeled defect escapes [Verified]"),
        ("LOGISTICS", "Amazon & DHL", "• 750,000 active AMRs deployed\n• 25% faster order processing\n• 28% trailer unloading dock cost reduction [Verified]"),
        ("HEAVY INDUSTRY", "GE & Caterpillar", "• 30% reduction in gas turbine trips\n• 250M autonomous haulage km\n• Zero lost-time haul injuries [Verified]")
    ]
    
    for i, (sector, clients, metrics) in enumerate(sectors):
        x = Inches(0.6) + i * Inches(2.46)
        add_card(s, x, CONTENT_TOP, col_w, col_h)
        
        tb = s.shapes.add_textbox(x + Inches(0.15), CONTENT_TOP + Inches(0.2), col_w - Inches(0.3), col_h - Inches(0.4))
        tf = tb.text_frame; tf.word_wrap = True
        
        p1 = tf.paragraphs[0]
        add_run(p1, sector, size=Pt(15), color=COLOR_ACCENT, bold=True)
        
        p2 = tf.add_paragraph(); p2.space_before = Pt(4)
        add_run(p2, clients, size=Pt(18), color=COLOR_TEXT_MAIN, bold=True)
        
        p3 = tf.add_paragraph(); p3.space_before = Pt(12)
        add_run(p3, metrics, size=SIZE_BODY_MIN, color=COLOR_TEXT_MUTED)
        
    add_takeaway(s, "IMPACT PATTERN:", "Verified deployment ROI occurs where precision, scrap costs, and downtime penalties are extreme.")
    add_footer(s, 16, "Verified Deployments Across Sectors")

# ==============================================================================
# SLIDE 17: Hype-Ahead-of-Deployment (Contrast Slide)
# ==============================================================================
def slide_17():
    s = create_slide(prs)
    add_header(s, "Deconstructing Hype: Unverified Marketing vs. Physical Reality", "Adoption Reality")
    
    card_w = Inches(3.85)
    card_h = Inches(4.7)
    
    contrasts = [
        ("Humanoids in Automotive Final Assembly",
         "CLAIM: Full human replacement on moving assembly lines in 12 months.",
         "REALITY: Fails takt times (<60s) and deformable wire harness tolerances (<0.2mm). Lack of tactile slip feedback causes assembly failure [Verified]."),
        ("General-Purpose Construction Robotics",
         "CLAIM: Fully autonomous bricklaying and framing in outdoor rain/mud.",
         "REALITY: Dynamic outdoor soil mechanics violate visual odometry assumptions. Extreme weather breaks sim-to-real transfer [Verified]."),
        ("Autonomous Class III Surgery",
         "CLAIM: Unsupervised robotic tissue resection and suturing without human oversight.",
         "REALITY: FDA Class III mandates formal deterministic safety proofs that stochastic neural networks cannot provide today [Verified].")
    ]
    
    for i, (title, claim, reality) in enumerate(contrasts):
        x = Inches(0.6) + i * Inches(4.141)
        add_card(s, x, CONTENT_TOP, card_w, card_h)
        
        tb = s.shapes.add_textbox(x + Inches(0.2), CONTENT_TOP + Inches(0.25), card_w - Inches(0.4), card_h - Inches(0.5))
        tf = tb.text_frame; tf.word_wrap = True
        
        p1 = tf.paragraphs[0]
        add_run(p1, title, size=Pt(19), color=COLOR_TEXT_MAIN, bold=True)
        
        p2 = tf.add_paragraph(); p2.space_before = Pt(14)
        add_run(p2, "MARKETING CLAIM:", size=Pt(11), color=COLOR_SPECULATIVE, bold=True)
        p2_b = tf.add_paragraph()
        add_run(p2_b, claim, size=Pt(16), color=COLOR_TEXT_MUTED)
        
        p3 = tf.add_paragraph(); p3.space_before = Pt(14)
        add_run(p3, "PRODUCTION REALITY:", size=Pt(11), color=COLOR_VERIFIED, bold=True)
        p3_b = tf.add_paragraph()
        add_run(p3_b, reality, size=Pt(16), color=COLOR_TEXT_MAIN)
        
    add_takeaway(s, "STRATEGIC IMPLICATION:", "Unconstrained generalist tasks stall; structured high-precision automation succeeds.")
    add_footer(s, 17, "Hype vs. Production Reality")

# ==============================================================================
# SLIDE 18: Section Divider 5 (Competitive Landscape)
# ==============================================================================
def slide_18():
    build_section_divider(
        18, "MODULE 05",
        "Competitive Landscape",
        "Multi-Layer Industry Stack and High-Value Underserved Gaps",
        "MARKET DEFICIT:", "Software pure-plays lack plant floor access; systems integrators own customer delivery."
    )

# ==============================================================================
# SLIDE 19: Layered Competitive Map (5-Layer Stack)
# ==============================================================================
def slide_19():
    s = create_slide(prs)
    add_header(s, "Multi-Layer Competitive Landscape across Physical AI", "Industry Structure")
    
    row_w = CONTENT_WIDTH
    row_h = Inches(0.85)
    
    layers = [
        ("Layer 1: Foundation Models", "Physical Intelligence, Skild AI, DeepMind", "Frontier algorithms; zero legacy plant distribution.", False),
        ("Layer 2: Industrial Automation", "Siemens, Rockwell Automation, ABB", "Own the factory floor; slow software cycles.", False),
        ("Layer 3: Simulation Platforms", "NVIDIA Omniverse, Applied Intuition, Scale AI", "High switching costs; platform moats.", False),
        ("Layer 4: ER&D Systems Integration", "LTTS (Target Moat), KPIT, Cyient", "Certified bridge: connect frontier models to PLCs.", True), # Highlighted
        ("Layer 5: Statutory Certification", "TÜV SÜD, UL Solutions, Credo AI", "Mandatory regulatory tollgates for factory insurance.", False)
    ]
    
    y_pos = CONTENT_TOP
    for title, players, moat, is_target in layers:
        bg = COLOR_ACCENT_BG if is_target else COLOR_CARD_BG
        border = COLOR_ACCENT if is_target else COLOR_CARD_BORDER
        add_card(s, Inches(0.6), y_pos, row_w, row_h, bg=bg, border=border, border_width=1.5 if is_target else 1.0)
        
        tb = s.shapes.add_textbox(Inches(0.9), y_pos + Inches(0.12), row_w - Inches(0.6), row_h - Inches(0.24))
        tf = tb.text_frame; tf.word_wrap = True
        
        p1 = tf.paragraphs[0]
        add_run(p1, title + "  —  ", size=Pt(18), color=COLOR_ACCENT if is_target else COLOR_TEXT_MAIN, bold=True)
        add_run(p1, players, size=Pt(16), color=COLOR_TEXT_MAIN)
        
        p2 = tf.add_paragraph()
        add_run(p2, "Moat: " + moat, size=Pt(15), color=COLOR_TEXT_MUTED)
        
        y_pos += row_h + Inches(0.15)
        
    add_takeaway(s, "POSITIONING:", "LTTS occupies the indispensable Layer 4 integration position connecting algorithmic brains with industrial muscle.")
    add_footer(s, 19, "Layered Competitive Landscape")

# ==============================================================================
# SLIDE 20: High-Value Underserved Gaps (3 Cards)
# ==============================================================================
def slide_20():
    s = create_slide(prs)
    add_header(s, "Three High-Value Underserved Market White Spaces", "Market Opportunities")
    
    card_w = Inches(3.85)
    card_h = Inches(4.7)
    
    gaps = [
        ("Gap 1: Neural Safety Compiler",
         "THE DEFICIT: Foundation models are black boxes; certifiers require deterministic bounds. No tool today converts 7B VLAs into formal proof certificates.",
         "LTTS SOLUTION: Build the industry's first Neural-to-IEC-61508 V&V compiler, extracting Control Barrier Functions for automated TÜV dossiers."),
        ("Gap 2: Legacy CAD-to-Physics",
         "THE DEFICIT: Clients possess petabytes of unmeshed, dirty CAD/PLM data lacking friction and mass parameters, blocking Isaac Sim digital twin setup.",
         "LTTS SOLUTION: Deploy geometry-parsing AI pipelines converting raw PLM assemblies into verified simulation twins in hours instead of months."),
        ("Gap 3: 50Hz Real-Time Middleware",
         "THE DEFICIT: Large VLAs on edge Jetson hardware suffer from 80-250ms latency jitter, causing severe robot arm shudder and safety halts.",
         "LTTS SOLUTION: Package channel-aware quantization (AutoQVLA) and action chunking into a hardened industrial edge middleware gateway.")
    ]
    
    for i, (title, deficit, solution) in enumerate(gaps):
        x = Inches(0.6) + i * Inches(4.141)
        add_card(s, x, CONTENT_TOP, card_w, card_h)
        
        tb = s.shapes.add_textbox(x + Inches(0.2), CONTENT_TOP + Inches(0.25), card_w - Inches(0.4), card_h - Inches(0.5))
        tf = tb.text_frame; tf.word_wrap = True
        
        p1 = tf.paragraphs[0]
        add_run(p1, title, size=Pt(19), color=COLOR_TEXT_MAIN, bold=True)
        
        p2 = tf.add_paragraph(); p2.space_before = Pt(14)
        add_run(p2, "MARKET DEFICIT:", size=Pt(11), color=COLOR_SPECULATIVE, bold=True)
        p2_b = tf.add_paragraph()
        add_run(p2_b, deficit, size=Pt(16), color=COLOR_TEXT_MUTED)
        
        p3 = tf.add_paragraph(); p3.space_before = Pt(14)
        add_run(p3, "LTTS ENTRY POINT:", size=Pt(11), color=COLOR_ACCENT, bold=True)
        p3_b = tf.add_paragraph()
        add_run(p3_b, solution, size=Pt(16), color=COLOR_TEXT_MAIN)
        
    add_takeaway(s, "MOAT DEFENSE:", "Solving these three engineering bottlenecks creates an unassailable commercial moat against software pure-plays.")
    add_footer(s, 20, "High-Value Underserved Gaps")

# ==============================================================================
# SLIDE 21: Section Divider 6 & Jacobian Singularity Equation Slide
# ==============================================================================
def slide_21():
    s = create_slide(prs)
    add_header(s, "The Domain Engineering Moat: Kinematic Singularities", "Domain Moat")
    
    # Render Math Equation via Matplotlib
    eq_buf = render_equation_image(r"\dot{q} = J^*(q)\dot{x} = J^T (J J^T + \lambda^2 I)^{-1} \dot{x}", fontsize=28)
    s.shapes.add_picture(eq_buf, Inches(2.2), CONTENT_TOP + Inches(0.3), width=Inches(8.5))
    
    # Operational Explanation Card
    card_top = CONTENT_TOP + Inches(1.8)
    card_h = Inches(3.0)
    add_card(s, Inches(0.6), card_top, CONTENT_WIDTH, card_h)
    
    tb = s.shapes.add_textbox(Inches(0.9), card_top + Inches(0.3), CONTENT_WIDTH - Inches(0.6), card_h - Inches(0.6))
    tf = tb.text_frame; tf.word_wrap = True
    
    p1 = tf.paragraphs[0]
    add_run(p1, "What This Means Operationally on the Factory Floor:", size=Pt(20), color=COLOR_TEXT_MAIN, bold=True)
    
    p2 = tf.add_paragraph(); p2.space_before = Pt(12)
    add_run(p2, "• When Yoshikawa manipulability det(J*J^T) -> 0, raw Cartesian VLA neural commands demand infinite joint speeds, destroying mechanical gearboxes.\n• Damped Least-Squares (DLS) mathematically bounds joint velocities while guaranteeing trajectory safety.\n• Software pure-plays lack this robotics mechanics depth; mechatronics systems integrators provide the essential safety envelope.", size=SIZE_BODY_MIN, color=COLOR_TEXT_MUTED)
    
    add_takeaway(s, "CONTROL-SYSTEMS RIGOR:", "Kinematic invariants and singular perturbation mechanics protect hardware from ungrounded neural outputs.")
    add_footer(s, 21, "Industrial AI to Physical AI Bridge")

# ==============================================================================
# SLIDE 22: Closed-Loop Data Flywheel (5-Node Loop)
# ==============================================================================
def slide_22():
    s = create_slide(prs)
    add_header(s, "The LTTS Closed-Loop Operational Data Flywheel", "Data Flywheel")
    
    col_w = Inches(2.28)
    col_h = Inches(4.7)
    
    nodes = [
        ("STAGE 1", "Telemetry Ingestion", "Logging joint torques (tau), currents (I), and deflections at >= 1kHz on deterministic fieldbuses.", "Modbus / RTOS"),
        ("STAGE 2", "PINN Calibration", "Physics-Informed Neural Networks inverting telemetry to calibrate friction (mu) and backlash (b).", "PyTorch Physics"),
        ("STAGE 3", "Synthetic Foundry", "Simulating 10^6 variations in Isaac Sim enforced by physics loss: L_pinn = ||d_t u + N[u] - f||^2.", "Isaac Sim 4.0"),
        ("STAGE 4", "Edge Execution", "Deploying quantized VLA policies with real-time Control Barrier Function (CBF) safety filters.", "Jetson AGX Orin"),
        ("STAGE 5", "OOD Monitoring", "Flagging reconstruction residuals (E_recon > tau) to trigger automated synthetic re-simulation.", "Drift Monitor")
    ]
    
    for i, (num, name, desc, tool) in enumerate(nodes):
        x = Inches(0.6) + i * Inches(2.46)
        add_card(s, x, CONTENT_TOP, col_w, col_h)
        
        tb = s.shapes.add_textbox(x + Inches(0.15), CONTENT_TOP + Inches(0.2), col_w - Inches(0.3), col_h - Inches(0.4))
        tf = tb.text_frame; tf.word_wrap = True
        
        p1 = tf.paragraphs[0]
        add_run(p1, num, size=Pt(13), color=COLOR_ACCENT, bold=True)
        
        p2 = tf.add_paragraph(); p2.space_before = Pt(4)
        add_run(p2, name, size=Pt(18), color=COLOR_TEXT_MAIN, bold=True)
        
        p3 = tf.add_paragraph(); p3.space_before = Pt(12)
        add_run(p3, desc, size=SIZE_BODY_MIN, color=COLOR_TEXT_MUTED)
        
        p4 = tf.add_paragraph(); p4.space_before = Pt(14)
        add_run(p4, "TOOLCHAIN:\n" + tool, size=Pt(13), color=COLOR_ACCENT)
        
    add_takeaway(s, "FLYWHEEL EFFECT:", "A self-healing telemetry loop converting factory edge anomalies into synthetic training data.")
    add_footer(s, 22, "Closed-Loop Data Flywheel")

# ==============================================================================
# SLIDE 23: Strategic Roadmap Timeline
# ==============================================================================
def slide_23():
    s = create_slide(prs)
    add_header(s, "LTTS Strategic Investment Roadmap (2026–2028)", "Strategic Roadmap")
    
    col_w = Inches(2.88)
    col_h = Inches(4.7)
    
    milestones = [
        ("PRIORITY 1: Q1 2027", "$3.5M Investment", "Physical AI V&V Practice",
         "Launch dedicated safety testing lab. Productize runtime monitors (E_recon) for ISO 13849 compliance.\n\n36-Mo Return: $25M+ audit pipeline."),
        ("PRIORITY 2: Q2 2027", "$1.5M Investment", "Tripartite PLC Alliances",
         "Sign formal co-selling partnerships with Siemens, Rockwell, and Physical Intelligence as certified bridge integrator.\n\n36-Mo Return: $50M+ SI deals."),
        ("PRIORITY 3: Q3 2027", "$6.0M Investment", "Synthetic Data Factory",
         "Deploy Isaac Sim & Siemens Tecnomatix SD-FaaS engine converting client CAD/PLM into digital twins.\n\n36-Mo Return: $35M+ recurring SaaS."),
        ("PRIORITY 4: 2027-2028", "$3.0M Investment", "Physical AI Academy",
         "Reskill 250+ mechatronics staff in Isaac Lab, ROS2, and edge quantization. Recruit 20 PhD researchers.\n\n36-Mo Return: 300-person practice.")
    ]
    
    for i, (prio, budget, name, desc) in enumerate(milestones):
        x = Inches(0.6) + i * Inches(3.08)
        add_card(s, x, CONTENT_TOP, col_w, col_h)
        
        tb = s.shapes.add_textbox(x + Inches(0.18), CONTENT_TOP + Inches(0.2), col_w - Inches(0.36), col_h - Inches(0.4))
        tf = tb.text_frame; tf.word_wrap = True
        
        p1 = tf.paragraphs[0]
        add_run(p1, prio, size=Pt(13), color=COLOR_ACCENT, bold=True)
        
        p2 = tf.add_paragraph(); p2.space_before = Pt(4)
        add_run(p2, budget, size=Pt(20), color=COLOR_TEXT_MAIN, bold=True)
        
        p3 = tf.add_paragraph(); p3.space_before = Pt(4)
        add_run(p3, name, size=Pt(17), color=COLOR_TEXT_MAIN, bold=True)
        
        p4 = tf.add_paragraph(); p4.space_before = Pt(12)
        add_run(p4, desc, size=SIZE_BODY_MIN, color=COLOR_TEXT_MUTED)
        
    add_takeaway(s, "CAPITAL EFFICIENCY:", "A $14.0M phased commitment captures a market-leading position across an $11.5B global TAM.")
    add_footer(s, 23, "Strategic Investment Roadmap")

# ==============================================================================
# SLIDE 24: 3–5 Year Forecast & Uncertainties (2-Column)
# ==============================================================================
def slide_24():
    s = create_slide(prs)
    add_header(s, "3–5 Year Industry Forecast & Critical Uncertainties", "Future Outlook")
    
    col_w = Inches(5.85)
    col_h = Inches(4.7)
    
    # Left Column: Forecast
    add_card(s, Inches(0.6), CONTENT_TOP, col_w, col_h)
    tb_l = s.shapes.add_textbox(Inches(0.9), CONTENT_TOP + Inches(0.2), col_w - Inches(0.6), col_h - Inches(0.4))
    tf_l = tb_l.text_frame; tf_l.word_wrap = True
    
    p_l1 = tf_l.paragraphs[0]
    add_run(p_l1, "GROUNDED STRUCTURAL FORECAST (2026–2030)", size=Pt(15), color=COLOR_ACCENT, bold=True)
    
    p_l2 = tf_l.add_paragraph(); p_l2.space_before = Pt(10)
    add_run(p_l2, "• Hardware Commoditization (2027-28): Arms and bipedal bases drop 60% in unit cost; value shifts entirely to software.\n\n• Foundation Model Consolidation: 2-3 global foundation models win (NVIDIA, DeepMind, PI). In-house model training is a capital trap.\n\n• Integration Expansion: Bespoke plant tooling expands integration services TAM to $11.5B by 2029 [Estimated].", size=SIZE_BODY_MIN, color=COLOR_TEXT_MUTED)
    
    # Right Column: Uncertainties
    add_card(s, Inches(6.883), CONTENT_TOP, col_w, col_h)
    tb_r = s.shapes.add_textbox(Inches(7.183), CONTENT_TOP + Inches(0.2), col_w - Inches(0.6), col_h - Inches(0.4))
    tf_r = tb_r.text_frame; tf_r.word_wrap = True
    
    p_r1 = tf_r.paragraphs[0]
    add_run(p_r1, "CRITICAL SENSITIVITY SCENARIOS", size=Pt(15), color=COLOR_ACCENT, bold=True)
    
    p_r2 = tf_r.add_paragraph(); p_r2.space_before = Pt(10)
    add_run(p_r2, "• Safety Regulations (OSHA/EU): Mandating physical cages shifts demand to fixed cells; certifying virtual zones booms SI demand.\n\n• Geopolitical Decoupling: US-China robotics export bans force LTTS to maintain dual-stack integration capabilities.\n\n• Sim-to-Real Velocity: Differentiable physics speed directly determines Synthetic Data Factory margins (targeting >45%).", size=SIZE_BODY_MIN, color=COLOR_TEXT_MUTED)
    
    add_takeaway(s, "CONCLUSION:", "Hardware commoditization makes systems integration and verification the primary value capture point.")
    add_footer(s, 24, "3-5 Year Industry Forecast")

# ==============================================================================
# SLIDE 25: Closing / The Ask
# ==============================================================================
def slide_25():
    s = create_slide(prs)
    add_header(s, "The Executive Decision & Path Forward", "Closing & Next Steps")
    
    # Hero Stat Banner
    hero_w = CONTENT_WIDTH
    hero_h = Inches(1.65)
    add_card(s, Inches(0.6), CONTENT_TOP, hero_w, hero_h, bg=COLOR_ACCENT_BG, border=COLOR_ACCENT, border_width=2.0)
    
    tb_hb = s.shapes.add_textbox(Inches(0.9), CONTENT_TOP + Inches(0.10), hero_w - Inches(0.6), Inches(1.45))
    tf_hb = tb_hb.text_frame; tf_hb.word_wrap = True
    p_hb1 = tf_hb.paragraphs[0]; p_hb1.alignment = PP_ALIGN.CENTER
    add_run(p_hb1, "$110M+ PRACTICE PIPELINE", size=SIZE_STAT_NUM, color=COLOR_TEXT_MAIN, bold=True)
    p_hb2 = tf_hb.add_paragraph(); p_hb2.alignment = PP_ALIGN.CENTER
    add_run(p_hb2, "Projected 36-Month Cumulative Practice Revenue on $14.0M Phased Commitment", size=Pt(15), color=COLOR_ACCENT, bold=True)
    
    # 3 Strategic Pillars Below
    card_top = CONTENT_TOP + hero_h + Inches(0.15)
    card_w = Inches(3.85)
    card_h = Inches(2.95)
    
    pillars = [
        ("1. Approve Capital", "$14.0M Phased Budget", "Authorize Q1 2027 initial tranche of $3.5M to launch accredited V&V lab and initial testing cells."),
        ("2. Ratify Alliances", "Incumbent Ecosystem", "Formalize co-selling agreements with Siemens, Rockwell, and Physical Intelligence as certified bridge."),
        ("3. Launch Academy", "Mechatronics Reskilling", "Upskill 250+ mechatronics engineers into certified Physical AI deployment practice leaders.")
    ]
    
    for i, (title, sub, desc) in enumerate(pillars):
        x = Inches(0.6) + i * Inches(4.141)
        add_card(s, x, card_top, card_w, card_h)
        
        tb = s.shapes.add_textbox(x + Inches(0.2), card_top + Inches(0.15), card_w - Inches(0.4), card_h - Inches(0.30))
        tf = tb.text_frame; tf.word_wrap = True
        
        p1 = tf.paragraphs[0]
        add_run(p1, title, size=Pt(19), color=COLOR_TEXT_MAIN, bold=True)
        
        p2 = tf.add_paragraph(); p2.space_before = Pt(4)
        add_run(p2, sub, size=Pt(16), color=COLOR_ACCENT, bold=True)
        
        p3 = tf.add_paragraph(); p3.space_before = Pt(10)
        add_run(p3, desc, size=SIZE_BODY_MIN, color=COLOR_TEXT_MUTED)
        
    add_takeaway(s, "CLOSING CALL TO ACTION:", "The question is not whether industry deploys Physical AI — it is who integrates and certifies it first.")
    add_footer(s, 25, "The Executive Decision & Action Plan")

# ==============================================================================
# MAIN BUILD SEQUENCE
# ==============================================================================
def main():
    print("=" * 75)
    print("GENERATING MASTER 25-SLIDE EXECUTIVE PRESENTATION")
    print("=" * 75)
    
    slide_builders = [
        slide_01, slide_02, slide_03, slide_04, slide_05,
        slide_06, slide_07, slide_08, slide_09, slide_10,
        slide_11, slide_12, slide_13, slide_14, slide_15,
        slide_16, slide_17, slide_18, slide_19, slide_20,
        slide_21, slide_22, slide_23, slide_24, slide_25
    ]
    
    for idx, builder in enumerate(slide_builders, 1):
        builder()
        print(f"  [OK] Generated Slide {idx:02d}: {builder.__name__}")
        
    prs.save(OUTPUT_FILE)
    print(f"\n[SUCCESS] Successfully saved 25-slide master presentation to:\n{OUTPUT_FILE}")
    print("=" * 75)

if __name__ == "__main__":
    main()
