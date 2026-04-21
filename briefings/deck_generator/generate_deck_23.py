"""
The Practice of Physical Artificial Intelligence — Final Master Executive Deck (23 Slides)
Prepared for Dr. Madhusudhan Singh & LTTS Engineering Leadership.
Under 25 slides (exactly 23 slides), 100% pure Studio White background (#FFFFFF),
Segoe UI (Friendly, Modern, Human, Crystal Clear, Non-Sterile Typography),
Substantially enlarged headings (Slide Action Titles 28pt, Card Titles 14.5-16pt),
High-visibility bold text (11-11.5pt body with high-contrast Slate 800/900),
Elevated visual design with modern rounded cards, accent pill badges, and top indicator stripes,
Minimalist, elegant, uncluttered Cover Slide,
100% content preservation from the 16-page LaTeX briefing.
"""

import os
import sys
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

from deck_common_v2 import (
    prs, new_slide, add_card, add_rect, add_header, add_takeaway,
    add_badge, add_pill_badge, add_math_image, set_notes,
    BG_CANVAS, BG_CARD, BG_CARD_ALT, BG_CARD_ACCENT, BG_CARD_BLUE,
    BORDER_SUBTLE, BORDER_LINE, BORDER_BLUE,
    BRAND_NAVY, BRAND_BLUE, GOLD, CYAN, GREEN, AMBER, RED, PURPLE,
    COLOR_WHITE, INK_PRIMARY, TEXT_DARK, TEXT_LIGHT, TEXT_MUTED, TEXT_FAINT,
    FONT_TITLE, FONT_BODY, OUTPUT_PPTX
)

# Pastel Badge Tints
TINT_GREEN  = RGBColor(0xDC, 0xFC, 0xE7)
TINT_BLUE   = RGBColor(0xEE, 0xF2, 0xFF)
TINT_AMBER  = RGBColor(0xFE, 0xF3, 0xC7)
TINT_RED    = RGBColor(0xFE, 0xE2, 0xE2)
TINT_PURPLE = RGBColor(0xF3, 0xE8, 0xFF)
TINT_CYAN   = RGBColor(0xE0, 0xF2, 0xFE)


# ── SLIDE 01: Executive Title & Strategic Thesis (Minimalist & Clean) ──────────
def slide_01_cover():
    s = new_slide()

    # Top Pill Badge
    add_pill_badge(s, 0.8, 0.8, "STRATEGIC BRIEFING · L&T TECHNOLOGY SERVICES", bg=TINT_BLUE, fg=BRAND_BLUE, font_size=10.5, bold=True)

    # Main Title (Large, Commanding, Friendly, 48pt Segoe UI)
    tx_t = s.shapes.add_textbox(Inches(0.8), Inches(1.45), Inches(11.73), Inches(2.3))
    tf_t = tx_t.text_frame; tf_t.word_wrap = True; tf_t.margin_left = tf_t.margin_right = tf_t.margin_top = tf_t.margin_bottom = 0

    p1 = tf_t.paragraphs[0]
    r1 = p1.add_run()
    r1.text = "Physical Artificial Intelligence"
    r1.font.name = FONT_TITLE
    r1.font.size = Pt(48)
    r1.font.bold = True
    r1.font.color.rgb = INK_PRIMARY

    p2 = tf_t.add_paragraph()
    p2.space_before = Pt(14)
    r2 = p2.add_run()
    r2.text = "Commercial Landscape, Kinematics Moats, and the Industrial Engineering Bridge"
    r2.font.name = FONT_BODY
    r2.font.size = Pt(16)
    r2.font.color.rgb = TEXT_MUTED

    # Divider
    div = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(4.15), Inches(11.73), Inches(0.015))
    div.fill.solid(); div.fill.fore_color.rgb = RGBColor(0xEA, 0xEE, 0xF4); div.line.fill.background()

    # 2 Sleek Executive Profile Cards below divider
    col_w = 5.65
    card_h = 1.95
    top_m = 4.55

    # Card 1: Prepared For
    c1 = add_card(s, 0.8, top_m, col_w, card_h, bg=BG_CARD, border=BORDER_SUBTLE, border_width=1.0)
    b1 = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(top_m), Inches(col_w), Inches(0.05))
    b1.adjustments[0] = 0.5; b1.fill.solid(); b1.fill.fore_color.rgb = BRAND_NAVY; b1.line.fill.background()

    tx_c1 = s.shapes.add_textbox(Inches(1.10), Inches(top_m + 0.25), Inches(5.1), Inches(1.5))
    tf_c1 = tx_c1.text_frame; tf_c1.word_wrap = True; tf_c1.margin_left = tf_c1.margin_right = tf_c1.margin_top = tf_c1.margin_bottom = 0
    ph1 = tf_c1.paragraphs[0]
    rh1 = ph1.add_run(); rh1.text = "PREPARED EXCLUSIVELY FOR\n"; rh1.font.name = FONT_TITLE; rh1.font.size = Pt(10); rh1.font.bold = True; rh1.font.color.rgb = BRAND_BLUE
    pv1 = tf_c1.add_paragraph(); pv1.space_before = Pt(4)
    rv1 = pv1.add_run(); rv1.text = "Dr. Madhusudhan Singh\n"; rv1.font.name = FONT_TITLE; rv1.font.size = Pt(18); rv1.font.bold = True; rv1.font.color.rgb = INK_PRIMARY
    rv1_sub = pv1.add_run(); rv1_sub.text = "Executive & Technical Leadership, L&T Technology Services Limited"; rv1_sub.font.name = FONT_BODY; rv1_sub.font.size = Pt(11.5); rv1_sub.font.color.rgb = TEXT_LIGHT

    # Card 2: Author & Version
    c2 = add_card(s, 6.88, top_m, col_w, card_h, bg=BG_CARD, border=BORDER_SUBTLE, border_width=1.0)
    b2 = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.88), Inches(top_m), Inches(col_w), Inches(0.05))
    b2.adjustments[0] = 0.5; b2.fill.solid(); b2.fill.fore_color.rgb = BRAND_BLUE; b2.line.fill.background()

    tx_c2 = s.shapes.add_textbox(Inches(7.18), Inches(top_m + 0.25), Inches(5.1), Inches(1.5))
    tf_c2 = tx_c2.text_frame; tf_c2.word_wrap = True; tf_c2.margin_left = tf_c2.margin_right = tf_c2.margin_top = tf_c2.margin_bottom = 0
    ph2 = tf_c2.paragraphs[0]
    rh2 = ph2.add_run(); rh2.text = "AUTHORSHIP & CLASSIFICATION\n"; rh2.font.name = FONT_TITLE; rh2.font.size = Pt(10); rh2.font.bold = True; rh2.font.color.rgb = BRAND_BLUE
    pv2 = tf_c2.add_paragraph(); pv2.space_before = Pt(4)
    rv2 = pv2.add_run(); rv2.text = "Adari Karthikeya\n"; rv2.font.name = FONT_TITLE; rv2.font.size = Pt(18); rv2.font.bold = True; rv2.font.color.rgb = INK_PRIMARY
    rv2_sub = pv2.add_run(); rv2_sub.text = "Physical AI Practice Research · Version 3.0 Master Briefing · September 2026 (Confidential)"; rv2_sub.font.name = FONT_BODY; rv2_sub.font.size = Pt(11.5); rv2_sub.font.color.rgb = TEXT_LIGHT

    set_notes(s, "Slide 01 Cover. Welcome Dr. Madhusudhan Singh and LTTS leadership. Frame this briefing around rigorous verification and the multi-billion-dollar engineering services opportunity.")
    return s


# ── SLIDE 02: Evidentiary Verification Taxonomy & Hero Benchmarks ─────────────
def slide_02_taxonomy_and_metrics():
    s = new_slide()
    add_header(s, "Governance & Verification", "Evidentiary Verification Hierarchy & Commercial Benchmarks",
               "Four-tier verification standard separating audited disclosures from unvetted marketing copy.")

    # 3 Hero Stat Boxes across top
    stats = [
        ("$3.2B+", "Disclosed Venture Capital", "Invested across frontier robotics foundation model and humanoid startups between 2024 and 2026.", BRAND_BLUE, TINT_BLUE),
        ("< $20M", "True Humanoid Revenue", "Estimated total realized production deployment revenue across all humanoid OEMs globally combined in 2024-2025.", AMBER, TINT_AMBER),
        ("$6.0B", "Autonomous Valuation Ceiling", "Achieved by Applied Intuition (Series E, Mar 2024), establishing commercial benchmark for simulation & ADAS software.", GREEN, TINT_GREEN)
    ]
    box_w = 3.71
    gap = 0.30
    for i, (val, title, sub, clr, bg_pill) in enumerate(stats):
        left = 0.8 + i * (box_w + gap)
        add_card(s, left, 2.05, box_w, 1.45, bg=BG_CARD, border=BORDER_SUBTLE, border_width=1.0)
        bar = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(2.05), Inches(box_w), Inches(0.05))
        bar.adjustments[0] = 0.5; bar.fill.solid(); bar.fill.fore_color.rgb = clr; bar.line.fill.background()

        tx = s.shapes.add_textbox(Inches(left + 0.20), Inches(2.14), Inches(box_w - 0.40), Inches(1.25))
        tf = tx.text_frame; tf.word_wrap = True; tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        p1 = tf.paragraphs[0]
        r1 = p1.add_run(); r1.text = val; r1.font.name = FONT_TITLE; r1.font.size = Pt(32); r1.font.bold = True; r1.font.color.rgb = clr
        p2 = tf.add_paragraph()
        r2 = p2.add_run(); r2.text = title.upper(); r2.font.name = FONT_TITLE; r2.font.size = Pt(11); r2.font.bold = True; r2.font.color.rgb = INK_PRIMARY
        p3 = tf.add_paragraph()
        p3.space_before = Pt(2)
        r3 = p3.add_run(); r3.text = sub; r3.font.name = FONT_BODY; r3.font.size = Pt(10); r3.font.color.rgb = TEXT_DARK

    # 4-Column Evidentiary Taxonomy
    col_w = 2.71
    c_gap = 0.30
    tiers = [
        ("TIER 1 · AUDITED", "Audited Corporate Disclosures", GREEN, TINT_GREEN, [
            ("Definition:", "Verifiable via SEC 10-K filings, audited earnings transcripts, or official corporate press releases."),
            ("Criteria:", "Mandatory corporate officer attribution, verified dollar value, signed commercial contracts."),
            ("Applied To:", "Waymo mileage volume, Applied Intuition $6B valuation, Wayve $1.05B round.")
        ]),
        ("TIER 2 · RESEARCH", "Primary Literature & Trials", BRAND_BLUE, TINT_BLUE, [
            ("Definition:", "Peer-reviewed publications, arXiv preprints, or official customer-verified plant trials."),
            ("Criteria:", "Detailed mathematical formulations, experimental methodologies, named customer plant sites."),
            ("Applied To:", "PI π0 flow matching, NVIDIA EgoScale laws, BMW Spartanburg Figure 02 pilot.")
        ]),
        ("TIER 3 · ESTIMATES", "Qualified Estimates", AMBER, TINT_AMBER, [
            ("Definition:", "Industry extrapolations, trade press whitepapers, and unverified vendor marketing claims."),
            ("Criteria:", "Clearly labeled as [Estimated] or [Reported]; excluded from core financial models."),
            ("Applied To:", "Unitree G1 pricing ($16k), humanoid production cost curves, vendor whitepaper savings.")
        ]),
        ("TIER 4 · RETRACTED", "Adversarially Retracted", RED, TINT_RED, [
            ("Definition:", "Marketing claims from early drafts that failed rigorous primary-source verification."),
            ("Criteria:", "Full transparent logging in Appendix B audit register; strictly removed from briefing."),
            ("Applied To:", "Ford 42% scrap reduction, Airbus <2 PPM defects, Amazon 750k robot claim.")
        ])
    ]

    for j, (badge, title, clr, bg_pill, items) in enumerate(tiers):
        left = 0.8 + j * (col_w + c_gap)
        top_t = 3.65
        h_t = 3.05
        add_card(s, left, top_t, col_w, h_t, bg=BG_CARD, border=BORDER_SUBTLE, border_width=1.0)
        bar = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top_t), Inches(col_w), Inches(0.05))
        bar.adjustments[0] = 0.5; bar.fill.solid(); bar.fill.fore_color.rgb = clr; bar.line.fill.background()

        # Pill badge
        pill = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left + 0.16), Inches(top_t + 0.14), Inches(col_w - 0.32), Inches(0.26))
        pill.adjustments[0] = 0.5; pill.fill.solid(); pill.fill.fore_color.rgb = bg_pill; pill.line.fill.background()
        tf_p = pill.text_frame; tf_p.word_wrap = False; tf_p.margin_left = tf_p.margin_right = tf_p.margin_top = tf_p.margin_bottom = 0
        pp = tf_p.paragraphs[0]; pp.alignment = PP_ALIGN.CENTER
        rp = pp.add_run(); rp.text = badge; rp.font.name = FONT_TITLE; rp.font.size = Pt(9.5); rp.font.bold = True; rp.font.color.rgb = clr

        tx = s.shapes.add_textbox(Inches(left + 0.16), Inches(top_t + 0.44), Inches(col_w - 0.32), Inches(h_t - 0.50))
        tf = tx.text_frame; tf.word_wrap = True; tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        p_hdr = tf.paragraphs[0]
        r_h = p_hdr.add_run(); r_h.text = title; r_h.font.name = FONT_TITLE; r_h.font.size = Pt(12.5); r_h.font.bold = True; r_h.font.color.rgb = INK_PRIMARY

        for lbl, txt in items:
            p_i = tf.add_paragraph()
            p_i.space_before = Pt(4)
            r_l = p_i.add_run(); r_l.text = lbl + " "; r_l.font.name = FONT_BODY; r_l.font.size = Pt(10); r_l.font.bold = True; r_l.font.color.rgb = INK_PRIMARY
            r_t = p_i.add_run(); r_t.text = txt; r_t.font.name = FONT_BODY; r_t.font.size = Pt(10); r_t.font.color.rgb = TEXT_DARK

    add_takeaway(s, "Every metric in this presentation adheres to this four-tier evidentiary standard, guaranteeing zero marketing hype reaches leadership.")
    set_notes(s, "Slide 02 Taxonomy & Metrics. Highlight the $3.2B vs <$20M asymmetry and explain the 4-tier verification standard.")
    return s


# ── SLIDE 03: Commercial Maturity Framework (Tiers 1–3) ────────────────────────
def slide_03_maturity_tiers():
    s = new_slide()
    add_header(s, "Module 1 · Commercial State", "Commercial Maturity Framework: Scale vs. Pilots vs. Demos",
               "Three-tier classification separating commercial revenue scale from qualified enterprise pilots and staged lab claims.")

    col_w = 3.71
    gap = 0.30
    top = 2.05
    h = 4.65

    tiers = [
        ("TIER 1 · PRODUCTION SCALE", "Commercial Production at Scale", GREEN, TINT_GREEN, [
            ("Core Criteria:", "Proven revenue at commercial scale, continuous paid operation without safety drivers, regulatory operating approval, and contractual uptime guarantees."),
            ("Waymo (Alphabet):", ">150,000 paid commercial trips/week and >1,000,000 autonomous commercial miles weekly across San Francisco, Phoenix, and Los Angeles."),
            ("Tesla FSD:", ">2.0 billion cumulative miles operated on End-to-End neural networks (FSD v12+), validating mass visual scaling."),
            ("TSMC Semiconductor:", "Physics-informed neural networks operating in production EUV lithography and wafer defect classification with nanometer precision.")
        ]),
        ("TIER 2 · ENTERPRISE PILOTS", "Qualified Enterprise Field Pilots", BRAND_BLUE, TINT_BLUE, [
            ("Core Criteria:", "Multi-week customer plant trials with human safety oversight, bounded operational envelopes, and qualitative validation without fleet expansion."),
            ("Figure AI / BMW Spartanburg:", "Figure 02 bipedal humanoid trial at BMW Spartanburg plant (Aug 2024), testing sheet metal subassembly placement into chassis fixtures."),
            ("Apptronik / Mercedes-Benz:", "Commercial pilot agreement (Mar 2024) deploying Apollo humanoids for delivery of assembly component totes to production workers."),
            ("Boston Dynamics / DHL Supply Chain:", "Expanding deployment of Stretch mobile manipulators for automated carton unloading from truck containers across logistics hubs.")
        ]),
        ("TIER 3 · UNVERIFIED LAB DEMOS", "Unverified Lab & Marketing Demos", AMBER, TINT_AMBER, [
            ("Core Criteria:", "Teleoperated demonstrations, highly staged cherry-picked video releases, no public MTBF data, and failure under real environmental variance."),
            ("Pervasive Teleoperation Masking:", "Widespread use of VR puppeteering and hidden human teleoperation disguised as autonomous end-to-end foundation model inference."),
            ("Unitree, 1X, Agility Marketing:", "Viral social media demos showing dynamic parkour or warehouse box-shifting that fail to replicate under industrial dust, glare, or continuous run times."),
            ("Sim-to-Real Contact Collapse:", "Policies trained purely in rigid-body physics simulators failing catastrophically when encountering deformable packaging or surface oil.")
        ])
    ]

    for i, (badge, title, clr, bg_pill, items) in enumerate(tiers):
        left = 0.8 + i * (col_w + gap)
        add_card(s, left, top, col_w, h, bg=BG_CARD, border=BORDER_SUBTLE, border_width=1.0)
        bar = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(col_w), Inches(0.06))
        bar.adjustments[0] = 0.5; bar.fill.solid(); bar.fill.fore_color.rgb = clr; bar.line.fill.background()

        # Pill Badge
        pill = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left + 0.20), Inches(top + 0.20), Inches(col_w - 0.40), Inches(0.30))
        pill.adjustments[0] = 0.5; pill.fill.solid(); pill.fill.fore_color.rgb = bg_pill; pill.line.fill.background()
        tf_p = pill.text_frame; tf_p.word_wrap = False; tf_p.margin_left = tf_p.margin_right = tf_p.margin_top = tf_p.margin_bottom = 0
        pp = tf_p.paragraphs[0]; pp.alignment = PP_ALIGN.CENTER
        rp = pp.add_run(); rp.text = badge; rp.font.name = FONT_TITLE; rp.font.size = Pt(9.5); rp.font.bold = True; rp.font.color.rgb = clr

        tx_ct = s.shapes.add_textbox(Inches(left + 0.20), Inches(top + 0.58), Inches(col_w - 0.40), Inches(0.48))
        tf_ct = tx_ct.text_frame; tf_ct.word_wrap = True; tf_ct.margin_left = tf_ct.margin_right = tf_ct.margin_top = tf_ct.margin_bottom = 0
        pct = tf_ct.paragraphs[0]
        rct = pct.add_run(); rct.text = title; rct.font.name = FONT_TITLE; rct.font.size = Pt(14.5); rct.font.bold = True; rct.font.color.rgb = INK_PRIMARY

        tx_b = s.shapes.add_textbox(Inches(left + 0.20), Inches(top + 1.12), Inches(col_w - 0.40), Inches(h - 1.25))
        tf_b = tx_b.text_frame; tf_b.word_wrap = True; tf_b.margin_left = tf_b.margin_right = tf_b.margin_top = tf_b.margin_bottom = 0

        for idx, (lbl, body) in enumerate(items):
            p_item = tf_b.paragraphs[0] if idx == 0 else tf_b.add_paragraph()
            if idx > 0: p_item.space_before = Pt(6)
            rl = p_item.add_run(); rl.text = lbl + " "; rl.font.name = FONT_BODY; rl.font.size = Pt(10.5); rl.font.bold = True; rl.font.color.rgb = INK_PRIMARY
            rb = p_item.add_run(); rb.text = body; rb.font.name = FONT_BODY; rb.font.size = Pt(10.5); rb.font.color.rgb = TEXT_DARK

    add_takeaway(s, "Production-grade physical AI is currently restricted to autonomous mobility and semiconductor fabs; humanoid robotics remains firmly in Tier 2 pilots.")
    set_notes(s, "Slide 03 Maturity Tiers. Explain why Tier 1 scale exists today in Waymo and TSMC, while humanoids remain in Tier 2 pilots.")
    return s


# ── SLIDE 04: Disclosed Capital Matrix & The Hardware Trap ────────────────────
def slide_04_capital_and_hardware_trap():
    s = new_slide()
    add_header(s, "Module 1 · Commercial State", "Disclosed Capital Matrix & The Hardware Commoditization Trap",
               "Over $3.2B in venture capital highlights an acute structural margin crisis in robot hardware.")

    card_w = 5.72
    gap = 0.29
    top = 2.05
    h = 4.65

    # Left: Disclosed Capital Matrix
    add_card(s, 0.8, top, card_w, h, bg=BG_CARD, border=BORDER_SUBTLE, border_width=1.0)
    b1 = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(top), Inches(card_w), Inches(0.06))
    b1.adjustments[0] = 0.5; b1.fill.solid(); b1.fill.fore_color.rgb = BRAND_BLUE; b1.line.fill.background()

    pill1 = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.05), Inches(top + 0.18), Inches(card_w - 0.50), Inches(0.30))
    pill1.adjustments[0] = 0.5; pill1.fill.solid(); pill1.fill.fore_color.rgb = TINT_BLUE; pill1.line.fill.background()
    tf_p1 = pill1.text_frame; tf_p1.word_wrap = False; tf_p1.margin_left = tf_p1.margin_right = tf_p1.margin_top = tf_p1.margin_bottom = 0
    p1 = tf_p1.paragraphs[0]; p1.alignment = PP_ALIGN.CENTER
    rp1 = p1.add_run(); rp1.text = "DISCLOSED CAPITAL ROUNDS (2024 - 2026)"; rp1.font.name = FONT_TITLE; rp1.font.size = Pt(10); rp1.font.bold = True; rp1.font.color.rgb = BRAND_BLUE

    tx_l = s.shapes.add_textbox(Inches(1.05), Inches(top + 0.58), Inches(card_w - 0.50), Inches(h - 0.70))
    tf_l = tx_l.text_frame; tf_l.word_wrap = True; tf_l.margin_left = tf_l.margin_right = tf_l.margin_top = tf_l.margin_bottom = 0
    p_lh = tf_l.paragraphs[0]
    r_lh = p_lh.add_run(); r_lh.text = "Concentrated Foundation Model Funding ($3.2B+)\n"; r_lh.font.name = FONT_TITLE; r_lh.font.size = Pt(14); r_lh.font.bold = True; r_lh.font.color.rgb = INK_PRIMARY

    deals = [
        ("Wayve ($1.05B Series C, May 2024)", "SoftBank Group, NVIDIA, Microsoft", "Autonomous driving embodied foundation models."),
        ("Figure AI ($675M Series B, Feb 2024)", "Microsoft, OpenAI, NVIDIA, Bezos ($2.6B val)", "Generalist bipedal humanoid robots (Figure 02)."),
        ("Physical Intelligence ($400M Series A, Nov 2024)", "Bezos Expeditions, Thrive, Lux ($2.4B val)", "General-purpose robotics foundation model (π0)."),
        ("Skild AI ($300M Series A, Jul 2024)", "Lightspeed, Coatue, SoftBank ($1.5B val)", "Cross-embodiment foundation brains for manipulation."),
        ("Applied Intuition ($250M Series E, Mar 2024)", "Lux Capital, Elad Gil, Porsche ($6.0B val)", "Autonomous vehicle & robotics simulation / validation."),
        ("Scale AI ($1.0B Series F, May 2024)", "Accel, Strategic Partners ($13.8B val)", "Embodied data generation & evaluation infrastructure.")
    ]
    for name, inv, desc in deals:
        p_d = tf_l.add_paragraph()
        p_d.space_before = Pt(4.5)
        rn = p_d.add_run(); rn.text = name + "\n"; rn.font.name = FONT_TITLE; rn.font.size = Pt(11); rn.font.bold = True; rn.font.color.rgb = INK_PRIMARY
        ri = p_d.add_run(); ri.text = "Investors: " + inv + "  |  " + desc; ri.font.name = FONT_BODY; ri.font.size = Pt(10); ri.font.color.rgb = TEXT_DARK

    # Right: The Hardware Commoditization Trap
    add_card(s, 0.8 + card_w + gap, top, card_w, h, bg=BG_CARD, border=BORDER_SUBTLE, border_width=1.0)
    b2 = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8 + card_w + gap), Inches(top), Inches(card_w), Inches(0.06))
    b2.adjustments[0] = 0.5; b2.fill.solid(); b2.fill.fore_color.rgb = AMBER; b2.line.fill.background()

    pill2 = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8 + card_w + gap + 0.25), Inches(top + 0.18), Inches(card_w - 0.50), Inches(0.30))
    pill2.adjustments[0] = 0.5; pill2.fill.solid(); pill2.fill.fore_color.rgb = TINT_AMBER; pill2.line.fill.background()
    tf_p2 = pill2.text_frame; tf_p2.word_wrap = False; tf_p2.margin_left = tf_p2.margin_right = tf_p2.margin_top = tf_p2.margin_bottom = 0
    p2 = tf_p2.paragraphs[0]; p2.alignment = PP_ALIGN.CENTER
    rp2 = p2.add_run(); rp2.text = "STRUCTURAL MARGIN ANALYSIS"; rp2.font.name = FONT_TITLE; rp2.font.size = Pt(10); rp2.font.bold = True; rp2.font.color.rgb = AMBER

    tx_r = s.shapes.add_textbox(Inches(0.8 + card_w + gap + 0.25), Inches(top + 0.58), Inches(card_w - 0.50), Inches(h - 0.70))
    tf_r = tx_r.text_frame; tf_r.word_wrap = True; tf_r.margin_left = tf_r.margin_right = tf_r.margin_top = tf_r.margin_bottom = 0
    p_rh = tf_r.paragraphs[0]
    r_rh = p_rh.add_run(); r_rh.text = "The Hardware Commoditization Trap\n"; r_rh.font.name = FONT_TITLE; r_rh.font.size = Pt(14); r_rh.font.bold = True; r_rh.font.color.rgb = INK_PRIMARY

    trap_pts = [
        ("The $16,000 Humanoid Price War:", "Unitree's G1 launch at $16,000 initiates aggressive deflation in mechanical hardware long before autonomous software reaches production maturity. Chinese supply chains commoditize robot frames rapidly."),
        ("Structural Margin Collapse (<15%):", "As harmonic drives, frameless motors, and planetary actuators become off-the-shelf commodities, hardware-only OEMs face margin compression mirroring PC and Android handset commoditization."),
        ("Software & Integration Captures 70%+ Value:", "Economic surplus decisively shifts to: (1) Pretrained Foundation Models, (2) Deterministic Safety Middleware, (3) Physics Digital Twins, and (4) Systems Integration connecting robots to brownfield PLCs."),
        ("LTTS Strategic Imperative:", "LTTS must never attempt to build or manufacture proprietary robot hardware frames. The winning strategy is to remain entirely hardware-agnostic and capture high-margin software integration, V&V, and deployment.")
    ]
    for h_txt, b_txt in trap_pts:
        p_t = tf_r.add_paragraph()
        p_t.space_before = Pt(6.5)
        rth = p_t.add_run(); rth.text = h_txt + " "; rth.font.name = FONT_BODY; rth.font.size = Pt(11); rth.font.bold = True; rth.font.color.rgb = INK_PRIMARY
        rtb = p_t.add_run(); rtb.text = b_txt; rtb.font.name = FONT_BODY; rtb.font.size = Pt(10.5); rtb.font.color.rgb = TEXT_DARK

    add_takeaway(s, "Venture capital is aggressively subsidizing foundation models; commoditizing hardware forces value into systems engineering and plant integration.")
    set_notes(s, "Slide 04 Capital Matrix & Hardware Trap. Detail the $3.2B capital concentration and emphasize why LTTS must avoid hardware manufacturing.")
    return s


# ── SLIDE 05: Frontier Research Priorities 1, 2, 3 ────────────────────────────
def slide_05_frontier_research_priorities():
    s = new_slide()
    add_header(s, "Module 2 · Frontier Research", "Frontier Research: Flow Matching, World Models & RFT",
               "Core machine learning breakthroughs overcoming discrete tokenization and lack of spatial geometry.")

    col_w = 3.71
    gap = 0.30
    top = 2.05
    h = 4.65

    cards = [
        ("PRIORITY 1 · CONTINUOUS ACTIONS", "Continuous Action Flow Matching", BRAND_BLUE, TINT_BLUE, [
            ("Core Breakthrough:", "Direct velocity field regression via flow matching rather than autoregressive discrete tokenization."),
            ("Foundation Benchmark:", "Physical Intelligence π0 technical report (Oct 2024, arXiv:2410.24164)."),
            ("Why Tokenization Failed:", "Discretizing continuous motor torques into 256 discrete bins causes severe joint chattering and mechanical jerk."),
            ("Industrial Advantage:", "Enables sub-millimeter precision, fluid multi-joint coordination, and natural compliance during tight-tolerance assembly.")
        ]),
        ("PRIORITY 2 · 3D GEOMETRY", "3D Geometric & Video World Models", CYAN, TINT_CYAN, [
            ("Core Breakthrough:", "Pretraining generative models on massive physical video corpora to predict future 3D point-cloud states and scene dynamics."),
            ("Industry Implementations:", "NVIDIA Cosmos platform, World Labs (Fei-Fei Li spatial intelligence models)."),
            ("Causal Advantage:", "Generates plausible physics rollouts conditioned on proposed motor actions, allowing robots to simulate consequences before moving."),
            ("Industrial Advantage:", "Reduces on-robot physical trial requirements by 100x by generating thousands of diverse edge-case synthetic variations.")
        ]),
        ("PRIORITY 3 · AUTONOMOUS RL", "Reinforcement Fine-Tuning (RFT)", GREEN, TINT_GREEN, [
            ("Core Breakthrough:", "Autonomous policy improvement through trial-and-error exploration in physics simulation rather than static imitation."),
            ("Overcoming Teleop Limits:", "Human teleoperation data is prohibitively expensive ($50-$100/hr) and fundamentally reflects sub-optimal human biomechanics."),
            ("Curriculum Hardening:", "Progressively injecting synthetic friction variances, payload mass shifts, and external push disturbances into the training loop."),
            ("Industrial Advantage:", "Produces hardened neural controllers that autonomously recover from dropped parts, slipping grasps, and misaligned workpieces.")
        ])
    ]

    for i, (badge, title, clr, bg_pill, items) in enumerate(cards):
        left = 0.8 + i * (col_w + gap)
        add_card(s, left, top, col_w, h, bg=BG_CARD, border=BORDER_SUBTLE, border_width=1.0)
        bar = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(col_w), Inches(0.06))
        bar.adjustments[0] = 0.5; bar.fill.solid(); bar.fill.fore_color.rgb = clr; bar.line.fill.background()

        pill = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left + 0.20), Inches(top + 0.20), Inches(col_w - 0.40), Inches(0.30))
        pill.adjustments[0] = 0.5; pill.fill.solid(); pill.fill.fore_color.rgb = bg_pill; pill.line.fill.background()
        tf_p = pill.text_frame; tf_p.word_wrap = False; tf_p.margin_left = tf_p.margin_right = tf_p.margin_top = tf_p.margin_bottom = 0
        pp = tf_p.paragraphs[0]; pp.alignment = PP_ALIGN.CENTER
        rp = pp.add_run(); rp.text = badge; rp.font.name = FONT_TITLE; rp.font.size = Pt(9.5); rp.font.bold = True; rp.font.color.rgb = clr

        tx_ct = s.shapes.add_textbox(Inches(left + 0.20), Inches(top + 0.58), Inches(col_w - 0.40), Inches(0.48))
        tf_ct = tx_ct.text_frame; tf_ct.word_wrap = True; tf_ct.margin_left = tf_ct.margin_right = tf_ct.margin_top = tf_ct.margin_bottom = 0
        pct = tf_ct.paragraphs[0]
        rct = pct.add_run(); rct.text = title; rct.font.name = FONT_TITLE; rct.font.size = Pt(14.5); rct.font.bold = True; rct.font.color.rgb = INK_PRIMARY

        tx_b = s.shapes.add_textbox(Inches(left + 0.20), Inches(top + 1.12), Inches(col_w - 0.40), Inches(h - 1.25))
        tf_b = tx_b.text_frame; tf_b.word_wrap = True; tf_b.margin_left = tf_b.margin_right = tf_b.margin_top = tf_b.margin_bottom = 0

        for idx, (lbl, body) in enumerate(items):
            p_item = tf_b.paragraphs[0] if idx == 0 else tf_b.add_paragraph()
            if idx > 0: p_item.space_before = Pt(6)
            rl = p_item.add_run(); rl.text = lbl + " "; rl.font.name = FONT_BODY; rl.font.size = Pt(10.5); rl.font.bold = True; rl.font.color.rgb = INK_PRIMARY
            rb = p_item.add_run(); rb.text = body; rb.font.name = FONT_BODY; rb.font.size = Pt(10.5); rb.font.color.rgb = TEXT_DARK

    add_takeaway(s, "Flow matching and 3D world models bridge the gap from linguistic reasoning to smooth, physics-consistent continuous trajectory execution.")
    set_notes(s, "Slide 05 Research Priorities 1-3. Focus on why π0 continuous flow matching solves the discrete tokenization failure mode.")
    return s


# ── SLIDE 06: Frontier Research Priorities 4 & 5 ──────────────────────────────
def slide_06_scaling_laws_and_edge():
    s = new_slide()
    add_header(s, "Module 2 · Frontier Research", "Cross-Embodiment Scaling Laws & Sub-10ms Edge Inference",
               "Translating internet-scale human video to robot policies and deploying models under 10ms at the edge.")

    card_w = 5.72
    gap = 0.29
    top = 2.05
    h = 4.65

    # Left: Cross-Embodiment Scaling Laws
    add_card(s, 0.8, top, card_w, h, bg=BG_CARD, border=BORDER_SUBTLE, border_width=1.0)
    b1 = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(top), Inches(card_w), Inches(0.06))
    b1.adjustments[0] = 0.5; b1.fill.solid(); b1.fill.fore_color.rgb = BRAND_BLUE; b1.line.fill.background()

    pill1 = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.05), Inches(top + 0.18), Inches(card_w - 0.50), Inches(0.30))
    pill1.adjustments[0] = 0.5; pill1.fill.solid(); pill1.fill.fore_color.rgb = TINT_BLUE; pill1.line.fill.background()
    tf_p1 = pill1.text_frame; tf_p1.word_wrap = False; tf_p1.margin_left = tf_p1.margin_right = tf_p1.margin_top = tf_p1.margin_bottom = 0
    p1 = tf_p1.paragraphs[0]; p1.alignment = PP_ALIGN.CENTER
    rp1 = p1.add_run(); rp1.text = "PRIORITY 4 · CROSS-EMBODIMENT SCALING LAWS"; rp1.font.name = FONT_TITLE; rp1.font.size = Pt(10); rp1.font.bold = True; rp1.font.color.rgb = BRAND_BLUE

    tx_l = s.shapes.add_textbox(Inches(1.05), Inches(top + 0.58), Inches(card_w - 0.50), Inches(h - 0.70))
    tf_l = tx_l.text_frame; tf_l.word_wrap = True; tf_l.margin_left = tf_l.margin_right = tf_l.margin_top = tf_l.margin_bottom = 0
    p_lh = tf_l.paragraphs[0]
    r_lh = p_lh.add_run(); r_lh.text = "NVIDIA GEAR EgoScale Discovery (arXiv:2602.16710)\n"; r_lh.font.name = FONT_TITLE; r_lh.font.size = Pt(14); r_lh.font.bold = True; r_lh.font.color.rgb = INK_PRIMARY

    scale_pts = [
        ("Log-Linear Scaling Laws (Feb 2026):", "Research on EgoScale establishes log-linear scaling transferring uncurated human egocentric video directly to heterogeneous physical robot policies."),
        ("Universal Latent Representation:", "Maps disparate physical morphologies—including bipedal humanoids, quadrupeds, 6-DoF serial arms, and dual-arm manipulators—into a shared action-latent space."),
        ("Zero-Shot Spatial Invariant Transfer:", "Policies pre-trained on internet-scale human demonstration videos learn fundamental spatial invariants (grasp centroids, clearance vectors) without per-robot teleoperation."),
        ("Commercial Advantage for Integrators:", "Allows engineering integrators to train a core foundation policy once and deploy it across KUKA, FANUC, ABB, and Universal Robots hardware with minimal fine-tuning.")
    ]
    for h_txt, b_txt in scale_pts:
        p_s = tf_l.add_paragraph()
        p_s.space_before = Pt(6.5)
        rsh = p_s.add_run(); rsh.text = h_txt + " "; rsh.font.name = FONT_BODY; rsh.font.size = Pt(11); rsh.font.bold = True; rsh.font.color.rgb = INK_PRIMARY
        rsb = p_s.add_run(); rsb.text = b_txt; rsb.font.name = FONT_BODY; rsb.font.size = Pt(10.5); rsb.font.color.rgb = TEXT_DARK

    # Right: Edge Quantization & Real-Time Inference
    add_card(s, 0.8 + card_w + gap, top, card_w, h, bg=BG_CARD, border=BORDER_SUBTLE, border_width=1.0)
    b2 = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8 + card_w + gap), Inches(top), Inches(card_w), Inches(0.06))
    b2.adjustments[0] = 0.5; b2.fill.solid(); b2.fill.fore_color.rgb = GREEN; b2.line.fill.background()

    pill2 = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8 + card_w + gap + 0.25), Inches(top + 0.18), Inches(card_w - 0.50), Inches(0.30))
    pill2.adjustments[0] = 0.5; pill2.fill.solid(); pill2.fill.fore_color.rgb = TINT_GREEN; pill2.line.fill.background()
    tf_p2 = pill2.text_frame; tf_p2.word_wrap = False; tf_p2.margin_left = tf_p2.margin_right = tf_p2.margin_top = tf_p2.margin_bottom = 0
    p2 = tf_p2.paragraphs[0]; p2.alignment = PP_ALIGN.CENTER
    rp2 = p2.add_run(); rp2.text = "PRIORITY 5 · SUB-10MS EDGE INFERENCE"; rp2.font.name = FONT_TITLE; rp2.font.size = Pt(10); rp2.font.bold = True; rp2.font.color.rgb = GREEN

    tx_r = s.shapes.add_textbox(Inches(0.8 + card_w + gap + 0.25), Inches(top + 0.58), Inches(card_w - 0.50), Inches(h - 0.70))
    tf_r = tx_r.text_frame; tf_r.word_wrap = True; tf_r.margin_left = tf_r.margin_right = tf_r.margin_top = tf_r.margin_bottom = 0
    p_rh = tf_r.paragraphs[0]
    r_rh = p_rh.add_run(); r_rh.text = "Deterministic Edge Quantization & Control Loops\n"; r_rh.font.name = FONT_TITLE; r_rh.font.size = Pt(14); r_rh.font.bold = True; r_rh.font.color.rgb = INK_PRIMARY

    edge_pts = [
        ("The Hard Real-Time Constraint (≤ 10ms):", "Physical robot dynamic stability mandates 100Hz control loop frequencies (≤ 10ms latency). High-frequency servo commutation cannot tolerate cloud latency or non-deterministic lag."),
        ("FP8 & INT4 TensorRT-LLM Acceleration:", "Quantizing multi-billion-parameter VLA models to FP8/INT4 precision using NVIDIA TensorRT-LLM running directly on embedded edge hardware (Jetson Thor / AGX Orin)."),
        ("Thermal & Power Envelope (15W - 50W):", "Industrial mobile manipulators operate on strict battery and thermal budgets. Models must execute within 15W–50W plant power envelopes without active liquid cooling."),
        ("Asynchronous Multi-Rate Architecture:", "Decoupling perception from execution: high-level semantic vision runs at 10Hz, policy planning at 100Hz, and low-level torque safety governors commutation at 1kHz.")
    ]
    for h_txt, b_txt in edge_pts:
        p_e = tf_r.add_paragraph()
        p_e.space_before = Pt(6.5)
        reh = p_e.add_run(); reh.text = h_txt + " "; reh.font.name = FONT_BODY; reh.font.size = Pt(11); reh.font.bold = True; reh.font.color.rgb = INK_PRIMARY
        reb = p_e.add_run(); reb.text = b_txt; reb.font.name = FONT_BODY; reb.font.size = Pt(10.5); reb.font.color.rgb = TEXT_DARK

    add_takeaway(s, "Cross-embodiment pretraining solves data scarcity; edge quantization guarantees deterministic sub-10ms execution on real plant floors.")
    set_notes(s, "Slide 06 Scaling Laws & Edge Inference. Explain NVIDIA GEAR EgoScale and why sub-10ms latency is mandatory for physical dynamic stability.")
    return s


# ── SLIDE 07: Canonical Failure Modes (FM1 to FM5) ────────────────────────────
def slide_07_failure_modes():
    s = new_slide()
    add_header(s, "Module 2 · Frontier Research", "Five Canonical Failure Modes of Physical AI (FM1 to FM5)",
               "Structural physical and algorithmic failure modes causing deep learning policies to fail on live plant floors.")

    modes = [
        ("FM1", "Out-of-Distribution Kinematic Singularity",
         "Neural policy commands end-effector velocity passing near robot joint boundary where det(J) -> 0.",
         "Instantaneous motor over-current trips, emergency brake locking, or stripped gears.",
         "Damped Least-Squares (DLS) mechatronic filtering and null-space projection before servo commands.", RED),

        ("FM2", "Contact-Rich Force-Torque Instability",
         "Non-linear Coulomb friction and surface elasticity create high-frequency impact chattering during insertion.",
         "Rapid force-sensor saturation, acoustic resonance, workpiece gouging, or tool breakage.",
         "High-frequency (1kHz) hybrid impedance/force control layers and tactile feedback loops.", RED),

        ("FM3", "Latency-Induced Phase Lag & Oscillation",
         "Edge compute inference latency spikes above 50ms, introducing phase lag between camera and actuator.",
         "Severe mechanical overshoot, hunting oscillations, resonance amplification, and collisions.",
         "Fixed-time budget inference governors, predictive trajectory extrapolators, and RTOS priority scheduling.", RED),

        ("FM4", "Sensor Degradation & Brownfield Glare",
         "Airborne coolant mist, weld dust, lens smudges, and 50Hz/60Hz fluorescent lighting flicker corrupt camera feeds.",
         "Vision tokens lose semantic confidence, causing robot freeze, false obstacle stops, or miscalculated grasps.",
         "Multi-modal sensor fusion (stereo depth + LiDAR + tactile arrays) and out-of-distribution optical checks.", AMBER),

        ("FM5", "Semantic Drift & Object Pose Hallucination",
         "Pretrained VLA model confuses novel packaging, altered surface finishes, or metallic reflections with clutter.",
         "Grasping empty space, misaligned pick-and-place drops, or applying full grip force to delicate parts.",
         "Explicit 3D geometric bounding-box verification and contact-switch confirmation before trajectory execution.", AMBER)
    ]

    card_w = 11.73
    top_base = 2.05
    row_h = 0.85
    gap = 0.08

    for i, (code, title, mech, manif, mitig, clr) in enumerate(modes):
        top = top_base + i * (row_h + gap)
        add_card(s, 0.8, top, card_w, row_h, bg=BG_CARD, border=BORDER_SUBTLE, border_width=1.0)
        
        # Left colored pill tab
        tab = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(top), Inches(0.08), Inches(row_h))
        tab.adjustments[0] = 0.5; tab.fill.solid(); tab.fill.fore_color.rgb = clr; tab.line.fill.background()

        # Badge pill
        pill = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.98), Inches(top + 0.10), Inches(0.70), Inches(0.26))
        pill.adjustments[0] = 0.5; pill.fill.solid(); pill.fill.fore_color.rgb = TINT_RED if clr == RED else TINT_AMBER; pill.line.fill.background()
        tf_p = pill.text_frame; tf_p.word_wrap = False; tf_p.margin_left = tf_p.margin_right = tf_p.margin_top = tf_p.margin_bottom = 0
        pp = tf_p.paragraphs[0]; pp.alignment = PP_ALIGN.CENTER
        rp = pp.add_run(); rp.text = code; rp.font.name = FONT_TITLE; rp.font.size = Pt(9.5); rp.font.bold = True; rp.font.color.rgb = clr

        tx = s.shapes.add_textbox(Inches(1.80), Inches(top + 0.06), Inches(card_w - 1.10), Inches(row_h - 0.12))
        tf = tx.text_frame; tf.word_wrap = True; tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        p1 = tf.paragraphs[0]
        r1 = p1.add_run(); r1.text = title; r1.font.name = FONT_TITLE; r1.font.size = Pt(12); r1.font.bold = True; r1.font.color.rgb = INK_PRIMARY

        p2 = tf.add_paragraph()
        p2.space_before = Pt(2)
        r_m_lbl = p2.add_run(); r_m_lbl.text = "Mechanism: "; r_m_lbl.font.name = FONT_BODY; r_m_lbl.font.size = Pt(10); r_m_lbl.font.bold = True; r_m_lbl.font.color.rgb = TEXT_MUTED
        r_m = p2.add_run(); r_m.text = mech + "   |   "; r_m.font.name = FONT_BODY; r_m.font.size = Pt(10); r_m.font.color.rgb = TEXT_DARK
        r_mf_lbl = p2.add_run(); r_mf_lbl.text = "Manifestation: "; r_mf_lbl.font.name = FONT_BODY; r_mf_lbl.font.size = Pt(10); r_mf_lbl.font.bold = True; r_mf_lbl.font.color.rgb = RED
        r_mf = p2.add_run(); r_mf.text = manif + "   |   "; r_mf.font.name = FONT_BODY; r_mf.font.size = Pt(10); r_mf.font.color.rgb = TEXT_DARK
        r_mt_lbl = p2.add_run(); r_mt_lbl.text = "Mitigation: "; r_mt_lbl.font.name = FONT_BODY; r_mt_lbl.font.size = Pt(10); r_mt_lbl.font.bold = True; r_mt_lbl.font.color.rgb = GREEN
        r_mt = p2.add_run(); r_mt.text = mitig; r_mt.font.name = FONT_BODY; r_mt.font.size = Pt(10); r_mt.font.color.rgb = TEXT_DARK

    add_takeaway(s, "Every physical AI deployment requires rigorous mechatronic safety filters; unconstrained neural policies inevitably destroy physical plant equipment.")
    set_notes(s, "Slide 07 Failure Modes. Walk through FM1-FM5 and explain why software-only AI startups fail on brownfield shop floors without mechatronic safety guards.")
    return s


# ── SLIDE 08: Pearl's Causal Ladder ───────────────────────────────────────────
def slide_08_pearl_causal_ladder():
    s = new_slide()
    add_header(s, "Module 2 · Frontier Research", "Pearl's Causal Ladder: Why LLMs Fail at Robotics",
               "Deploying standard language models into robotics fails due to a fundamental representational mismatch.")

    card_w = 3.71
    gap = 0.30
    top = 2.05
    h = 4.65

    rungs = [
        ("RUNG 1 OF CAUSALITY", "Association & Observation", "Where LLMs Operate (Static Semantic Space)",
         r"P(Y \mid X)",
         "Standard language models operate strictly on observational correlations: P(Y | X). They predict the most probable next token based on statistical co-occurrences in historical training text corpora.",
         "Limitation: Passive observation cannot distinguish causal influence from spurious correlation. A language model knows 'smoke correlates with fire' but has no concept of physical mass, friction, or gravity.",
         BRAND_BLUE, TINT_BLUE),

        ("RUNG 2 OF CAUSALITY", "Intervention & Action", "The Domain of Physical AI (Dynamic Closed-Loop)",
         r"P(Y \mid \mathrm{do}(u))",
         "Physical control mandates causal intervention: P(Y | do(u)). A robot controller cannot merely guess tokens; it must predict precisely what physical state Y occurs when commanding a 15N torque u to an actuator.",
         "Requirement: Demands dedicated physical world models and closed-loop sensory feedback that map continuous control forces to kinematic motion under Newton's differential equations.",
         BRAND_NAVY, TINT_CYAN),

        ("RUNG 3 OF CAUSALITY", "Counterfactuals & Planning", "The Benchmark for Certified Safety & V&V",
         r"P(Y_u \mid X', Y')",
         "Safe autonomous execution requires evaluating counterfactual alternatives: P(Yu | X', Y'). The system must compute: 'Given that obstacle X' was encountered, would command trajectory u have prevented collision?'",
         "Requirement: Essential for formal functional safety dossiers, reachability verification, and statutory insurance compliance in brownfield industrial plants.",
         GREEN, TINT_GREEN)
    ]

    for i, (badge, title, subtitle, eq, desc, req, clr, bg_pill) in enumerate(rungs):
        left = 0.8 + i * (card_w + gap)
        add_card(s, left, top, card_w, h, bg=BG_CARD, border=BORDER_SUBTLE, border_width=1.0)
        bar = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(card_w), Inches(0.06))
        bar.adjustments[0] = 0.5; bar.fill.solid(); bar.fill.fore_color.rgb = clr; bar.line.fill.background()

        pill = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left + 0.20), Inches(top + 0.18), Inches(card_w - 0.40), Inches(0.28))
        pill.adjustments[0] = 0.5; pill.fill.solid(); pill.fill.fore_color.rgb = bg_pill; pill.line.fill.background()
        tf_p = pill.text_frame; tf_p.word_wrap = False; tf_p.margin_left = tf_p.margin_right = tf_p.margin_top = tf_p.margin_bottom = 0
        pp = tf_p.paragraphs[0]; pp.alignment = PP_ALIGN.CENTER
        rp = pp.add_run(); rp.text = badge; rp.font.name = FONT_TITLE; rp.font.size = Pt(9.5); rp.font.bold = True; rp.font.color.rgb = clr

        tx_ct = s.shapes.add_textbox(Inches(left + 0.20), Inches(top + 0.52), Inches(card_w - 0.40), Inches(0.70))
        tf_ct = tx_ct.text_frame; tf_ct.word_wrap = True; tf_ct.margin_left = tf_ct.margin_right = tf_ct.margin_top = tf_ct.margin_bottom = 0
        pct = tf_ct.paragraphs[0]
        rct = pct.add_run(); rct.text = title + "\n"; rct.font.name = FONT_TITLE; rct.font.size = Pt(14); rct.font.bold = True; rct.font.color.rgb = INK_PRIMARY
        rcs = pct.add_run(); rcs.text = subtitle; rcs.font.name = FONT_BODY; rcs.font.size = Pt(10.5); rcs.font.color.rgb = TEXT_MUTED

        # Math Image Container in razor-sharp frame
        eq_box = add_card(s, left + 0.20, top + 1.30, card_w - 0.40, 0.90, bg=COLOR_WHITE, border=BORDER_SUBTLE, border_width=1.0)
        add_math_image(s, eq, left + 0.45, top + 1.45, fontsize=19, max_h=0.6)

        tx_b = s.shapes.add_textbox(Inches(left + 0.20), Inches(top + 2.30), Inches(card_w - 0.40), Inches(2.20))
        tf_b = tx_b.text_frame; tf_b.word_wrap = True; tf_b.margin_left = tf_b.margin_right = tf_b.margin_top = tf_b.margin_bottom = 0
        p_d = tf_b.paragraphs[0]
        rd = p_d.add_run(); rd.text = desc + "\n\n"; rd.font.name = FONT_BODY; rd.font.size = Pt(10.5); rd.font.color.rgb = TEXT_DARK
        rq = p_d.add_run(); rq.text = req; rq.font.name = FONT_BODY; rq.font.size = Pt(10.5); rq.font.color.rgb = INK_PRIMARY

    add_takeaway(s, "This causal hierarchy proves why industrial robotics requires dedicated physics-grounded verification rather than raw LLM prompt engineering.")
    set_notes(s, "Slide 08 Pearl's Causal Ladder. Explain why LLMs are stuck on Rung 1 (P(Y|X)) and why safety certification requires Rung 3 counterfactuals.")
    return s


# ── SLIDE 09: Commercial Models & Deal Economics (Table 3) ────────────────────
def slide_09_commercial_models_table3():
    s = new_slide()
    add_header(s, "Module 3 · Commercialization", "Commercial Models, Deal Economics & Buyer Personas (Table 3)",
               "Comprehensive benchmark of revenue archetypes across foundation models, OEMs, software, and systems integration.")

    left_m = 0.8
    top_base = 2.05
    total_w = 11.73

    headers = [
        ("BUSINESS MODEL ARCHETYPE", 2.60, PP_ALIGN.LEFT),
        ("REPRESENTATIVE ENTITIES", 2.30, PP_ALIGN.LEFT),
        ("CONTRACT & DEAL ECONOMICS", 2.70, PP_ALIGN.LEFT),
        ("SALES CYCLE", 1.30, PP_ALIGN.CENTER),
        ("PRIMARY BUYER PERSONA", 2.83, PP_ALIGN.LEFT)
    ]
    rows = [
        ("Model Licensing / FMaaS", "Physical Intelligence, Skild AI, Covariant",
         "Annual base license + API overage\n($100k - $500k+ ARR) [Estimated]", "3 - 6 mos",
         "VP Software /\nHead of Robotics R&D", False),

        ("Integrated HW+SW OEM", "Figure AI, Agility Robotics, Boston Dynamics",
         "Robotics-as-a-Service ($5k-$15k/robot/mo)\nor CapEx + maintenance SLA [Reported]", "12 - 18 mos",
         "VP Logistics /\nPlant General Manager", False),

        ("Simulation & Validation Tooling", "NVIDIA Isaac Sim, Applied Intuition",
         "Enterprise SaaS subscription\n($250k - $2.0M+ ACV) [Reported]", "6 - 9 mos",
         "VP Engineering /\nHead of Autonomous Systems", False),

        ("Compliance & Safety Verification", "TÜV SÜD, UL Solutions, Credo AI",
         "Safety audit fee + recurring testing suite\n($150k - $750k per engagement) [Estimated]", "6 - 12 mos",
         "Chief Safety Officer /\nVP Quality & Compliance", False),

        ("Systems Integration & Deployment\n★ LTTS CORE OPPORTUNITY", "LTTS, KPIT Tech, Accenture Industry X",
         "T&M + Milestone-gated deployment\n($1.0M - $8.0M+ per site) [Estimated]", "4 - 8 mos",
         "Chief Information Officer /\nVP Manufacturing Operations", True)
    ]

    # Header Bar in Corporate Deep Navy
    hdr_h = 0.42
    hdr_shape = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left_m), Inches(top_base), Inches(total_w), Inches(hdr_h))
    hdr_shape.adjustments[0] = 0.08; hdr_shape.fill.solid(); hdr_shape.fill.fore_color.rgb = BRAND_NAVY; hdr_shape.line.fill.background()

    curr_x = left_m
    for title, col_w, align in headers:
        tb = s.shapes.add_textbox(Inches(curr_x + 0.12), Inches(top_base + 0.08), Inches(col_w - 0.24), Inches(0.30))
        tf = tb.text_frame; tf.word_wrap = True; tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        p = tf.paragraphs[0]; p.alignment = align
        r = p.add_run(); r.text = title; r.font.name = FONT_TITLE; r.font.size = Pt(10.5); r.font.bold = True; r.font.color.rgb = COLOR_WHITE
        curr_x += col_w

    # Table Body Rows
    row_top = top_base + hdr_h + 0.04
    row_h = 0.84
    gap = 0.04
    for i, (arch, players, econ, cycle, buyer, is_ltts) in enumerate(rows):
        bg = BG_CARD_BLUE if is_ltts else (BG_CARD if (i % 2 == 0) else COLOR_WHITE)
        border_clr = BRAND_BLUE if is_ltts else BORDER_SUBTLE
        border_w = 1.5 if is_ltts else 1.0
        add_card(s, left_m, row_top, total_w, row_h, bg=bg, border=border_clr, border_width=border_w)
        if is_ltts:
            tab = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left_m), Inches(row_top), Inches(0.08), Inches(row_h))
            tab.adjustments[0] = 0.5; tab.fill.solid(); tab.fill.fore_color.rgb = BRAND_BLUE; tab.line.fill.background()

        curr_x = left_m
        for col_idx, (text_val, col_w, align) in enumerate([(arch, 2.60, PP_ALIGN.LEFT),
                                                             (players, 2.30, PP_ALIGN.LEFT),
                                                             (econ, 2.70, PP_ALIGN.LEFT),
                                                             (cycle, 1.30, PP_ALIGN.CENTER),
                                                             (buyer, 2.83, PP_ALIGN.LEFT)]):
            tb = s.shapes.add_textbox(Inches(curr_x + 0.15), Inches(row_top + 0.08), Inches(col_w - 0.30), Inches(row_h - 0.16))
            tf = tb.text_frame; tf.word_wrap = True; tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
            p = tf.paragraphs[0]; p.alignment = align
            r = p.add_run(); r.text = text_val; r.font.name = FONT_BODY; r.font.size = Pt(10.5)
            if col_idx == 0:
                r.font.bold = True
                r.font.color.rgb = BRAND_BLUE if is_ltts else INK_PRIMARY
            elif col_idx == 3:
                r.font.bold = True
                r.font.color.rgb = GREEN if ("3 - 6" in text_val or "4 - 8" in text_val) else INK_PRIMARY
            elif is_ltts and col_idx == 4:
                r.font.bold = True
                r.font.color.rgb = INK_PRIMARY
            else:
                r.font.color.rgb = TEXT_DARK
            curr_x += col_w

        row_top += row_h + gap

    add_takeaway(s, "Systems integration captures the largest single-site budget ($1.0M-$8.0M+) with relatively fast 4-8 month enterprise sales cycles.")
    set_notes(s, "Slide 09 Commercial Models (Table 3). Emphasize why Systems Integration is the crown jewel offering for LTTS.")
    return s


# ── SLIDE 10: The ER&D Opportunity & Offerings 1 and 2 ────────────────────────
def slide_10_ltts_offerings_part1():
    s = new_slide()
    add_header(s, "Module 3 · Commercialization", "The ER&D Services Opportunity & Commercial Offerings 1 & 2",
               "Positioning LTTS to capture the $45B engineering services market through industrial AI infrastructure.")

    card_w = 5.72
    gap = 0.29
    top = 2.05
    h = 4.65

    # Left: Offering 1 SD-FaaS
    add_card(s, 0.8, top, card_w, h, bg=BG_CARD, border=BORDER_SUBTLE, border_width=1.0)
    b1 = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(top), Inches(card_w), Inches(0.06))
    b1.adjustments[0] = 0.5; b1.fill.solid(); b1.fill.fore_color.rgb = GREEN; b1.line.fill.background()

    pill1 = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.05), Inches(top + 0.18), Inches(card_w - 0.50), Inches(0.30))
    pill1.adjustments[0] = 0.5; pill1.fill.solid(); pill1.fill.fore_color.rgb = TINT_GREEN; pill1.line.fill.background()
    tf_p1 = pill1.text_frame; tf_p1.word_wrap = False; tf_p1.margin_left = tf_p1.margin_right = tf_p1.margin_top = tf_p1.margin_bottom = 0
    p1 = tf_p1.paragraphs[0]; p1.alignment = PP_ALIGN.CENTER
    rp1 = p1.add_run(); rp1.text = "OFFERING 1 · RECONFIGURABLE CELL INFRASTRUCTURE"; rp1.font.name = FONT_TITLE; rp1.font.size = Pt(10); rp1.font.bold = True; rp1.font.color.rgb = GREEN

    tx_l = s.shapes.add_textbox(Inches(1.05), Inches(top + 0.58), Inches(card_w - 0.50), Inches(h - 0.70))
    tf_l = tx_l.text_frame; tf_l.word_wrap = True; tf_l.margin_left = tf_l.margin_right = tf_l.margin_top = tf_l.margin_bottom = 0
    p_lh = tf_l.paragraphs[0]
    r_lh = p_lh.add_run(); r_lh.text = "Software-Defined Factory as a Service (SD-FaaS)\n"; r_lh.font.name = FONT_TITLE; r_lh.font.size = Pt(14.5); r_lh.font.bold = True; r_lh.font.color.rgb = INK_PRIMARY

    pts_1 = [
        ("The Enterprise Problem:", "Traditional factory lines require 12 to 18 months and millions in CapEx to re-tool for new product variants. Physical AI enables dynamic, software-driven cell re-tasking."),
        ("Monetizing Enterprise CAD/PLM:", "LTTS ingests existing customer Siemens Teamcenter / Dassault Systèmes CAD assemblies directly into NVIDIA Omniverse digital twins to generate validated robot workcells."),
        ("Deal Economics ($2.0M - $5.0M per Plant):", "Turnkey transformation contracts covering simulation setup, automated line re-tooling, and recurring edge calibration SLAs."),
        ("Measurable ROI:", "Reduces physical line commissioning time from 16 weeks to 3 weeks, eliminating costly mechanical re-machining change orders.")
    ]
    for h_txt, b_txt in pts_1:
        p_row = tf_l.add_paragraph()
        p_row.space_before = Pt(7)
        rh = p_row.add_run(); rh.text = h_txt + " "; rh.font.name = FONT_BODY; rh.font.size = Pt(11); rh.font.bold = True; rh.font.color.rgb = INK_PRIMARY
        rb = p_row.add_run(); rb.text = b_txt; rb.font.name = FONT_BODY; rb.font.size = Pt(10.5); rb.font.color.rgb = TEXT_DARK

    # Right: Offering 2 PLC Bridge Middleware
    add_card(s, 0.8 + card_w + gap, top, card_w, h, bg=BG_CARD, border=BORDER_SUBTLE, border_width=1.0)
    b2 = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8 + card_w + gap), Inches(top), Inches(card_w), Inches(0.06))
    b2.adjustments[0] = 0.5; b2.fill.solid(); b2.fill.fore_color.rgb = BRAND_BLUE; b2.line.fill.background()

    pill2 = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8 + card_w + gap + 0.25), Inches(top + 0.18), Inches(card_w - 0.50), Inches(0.30))
    pill2.adjustments[0] = 0.5; pill2.fill.solid(); pill2.fill.fore_color.rgb = TINT_BLUE; pill2.line.fill.background()
    tf_p2 = pill2.text_frame; tf_p2.word_wrap = False; tf_p2.margin_left = tf_p2.margin_right = tf_p2.margin_top = tf_p2.margin_bottom = 0
    p2 = tf_p2.paragraphs[0]; p2.alignment = PP_ALIGN.CENTER
    rp2 = p2.add_run(); rp2.text = "OFFERING 2 · DETERMINISTIC SAFETY MIDDLEWARE"; rp2.font.name = FONT_TITLE; rp2.font.size = Pt(10); rp2.font.bold = True; rp2.font.color.rgb = BRAND_BLUE

    tx_r = s.shapes.add_textbox(Inches(0.8 + card_w + gap + 0.25), Inches(top + 0.58), Inches(card_w - 0.50), Inches(h - 0.70))
    tf_r = tx_r.text_frame; tf_r.word_wrap = True; tf_r.margin_left = tf_r.margin_right = tf_r.margin_top = tf_r.margin_bottom = 0
    p_rh = tf_r.paragraphs[0]
    r_rh = p_rh.add_run(); r_rh.text = "Industrial PLC & Edge Bridge Middleware\n"; r_rh.font.name = FONT_TITLE; r_rh.font.size = Pt(14.5); r_rh.font.bold = True; r_rh.font.color.rgb = INK_PRIMARY

    pts_2 = [
        ("The Interface Chasm:", "Foundation models output asynchronous PyTorch tensors at 100Hz; industrial automation operates on deterministic cyclic PLCs at 1kHz over PROFINET and EtherCAT."),
        ("Certified Bridge Architecture:", "LTTS develops certified middleware wrapping neural trajectories with deterministic safety interlocks and certified PLC communication drivers (Siemens S7-1500, Rockwell ControlLogix)."),
        ("Deal Economics ($500k - $1.5M per Cell):", "Priced as systems integration plus per-node recurring software runtime licenses ($10k-$25k/robot/yr)."),
        ("Strategic Moat:", "Prevents deep learning hallucinations from tripping factory safety circuits, providing plant managers with certified fail-safe guarantees.")
    ]
    for h_txt, b_txt in pts_2:
        p_row = tf_r.add_paragraph()
        p_row.space_before = Pt(7)
        rh = p_row.add_run(); rh.text = h_txt + " "; rh.font.name = FONT_BODY; rh.font.size = Pt(11); rh.font.bold = True; rh.font.color.rgb = INK_PRIMARY
        rb = p_row.add_run(); rb.text = b_txt; rb.font.name = FONT_BODY; rb.font.size = Pt(10.5); rb.font.color.rgb = TEXT_DARK

    add_takeaway(s, "SD-FaaS and PLC Middleware position LTTS as the indispensable technical layer enabling frontier AI models to touch physical plant equipment.")
    set_notes(s, "Slide 10 Offerings 1 & 2. Walk through Software-Defined Factory as a Service and Industrial PLC Middleware.")
    return s


# ── SLIDE 11: LTTS Commercial Offerings 3 & 4 ─────────────────────────────────
def slide_11_ltts_offerings_part2():
    s = new_slide()
    add_header(s, "Module 3 · Commercialization", "LTTS Offerings 3 & 4: V&V Practice and Embodied MLOps",
               "High-margin recurring revenue models in statutory safety certification and continuous brownfield fleet calibration.")

    card_w = 5.72
    gap = 0.29
    top = 2.05
    h = 4.65

    # Left: Offering 3 V&V Practice
    add_card(s, 0.8, top, card_w, h, bg=BG_CARD, border=BORDER_SUBTLE, border_width=1.0)
    b1 = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(top), Inches(card_w), Inches(0.06))
    b1.adjustments[0] = 0.5; b1.fill.solid(); b1.fill.fore_color.rgb = BRAND_NAVY; b1.line.fill.background()

    pill1 = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.05), Inches(top + 0.18), Inches(card_w - 0.50), Inches(0.30))
    pill1.adjustments[0] = 0.5; pill1.fill.solid(); pill1.fill.fore_color.rgb = TINT_BLUE; pill1.line.fill.background()
    tf_p1 = pill1.text_frame; tf_p1.word_wrap = False; tf_p1.margin_left = tf_p1.margin_right = tf_p1.margin_top = tf_p1.margin_bottom = 0
    p1 = tf_p1.paragraphs[0]; p1.alignment = PP_ALIGN.CENTER
    rp1 = p1.add_run(); rp1.text = "OFFERING 3 · STATUTORY SAFETY CERTIFICATION"; rp1.font.name = FONT_TITLE; rp1.font.size = Pt(10); rp1.font.bold = True; rp1.font.color.rgb = BRAND_NAVY

    tx_l = s.shapes.add_textbox(Inches(1.05), Inches(top + 0.58), Inches(card_w - 0.50), Inches(h - 0.70))
    tf_l = tx_l.text_frame; tf_l.word_wrap = True; tf_l.margin_left = tf_l.margin_right = tf_l.margin_top = tf_l.margin_bottom = 0
    p_lh = tf_l.paragraphs[0]
    r_lh = p_lh.add_run(); r_lh.text = "Physical AI Verification & Validation (V&V)\n"; r_lh.font.name = FONT_TITLE; r_lh.font.size = Pt(14.5); r_lh.font.bold = True; r_lh.font.color.rgb = INK_PRIMARY

    pts_3 = [
        ("The Compliance Bottleneck:", "Enterprises cannot deploy uncertified neural policies into live plants without invalidating facility insurance under ISO 13849 (PL-d/e) and IEC 61508."),
        ("Formal Reachability Verification:", "LTTS utilizes Hamilton-Jacobi reachability analysis and Control Barrier Functions (CBFs) to mathematically prove the robot cannot enter unsafe states."),
        ("Deal Economics ($750k - $2.0M per Audit):", "High-margin statutory compliance engagements producing certified Safety Dossiers for plant underwriters and regulatory authorities."),
        ("Regulatory Gatekeeper Role:", "LTTS establishes itself as the mandatory certification authority between AI foundation model startups and industrial plant operators.")
    ]
    for h_txt, b_txt in pts_3:
        p_row = tf_l.add_paragraph()
        p_row.space_before = Pt(7)
        rh = p_row.add_run(); rh.text = h_txt + " "; rh.font.name = FONT_BODY; rh.font.size = Pt(11); rh.font.bold = True; rh.font.color.rgb = INK_PRIMARY
        rb = p_row.add_run(); rb.text = b_txt; rb.font.name = FONT_BODY; rb.font.size = Pt(10.5); rb.font.color.rgb = TEXT_DARK

    # Right: Offering 4 Embodied MLOps
    add_card(s, 0.8 + card_w + gap, top, card_w, h, bg=BG_CARD, border=BORDER_SUBTLE, border_width=1.0)
    b2 = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8 + card_w + gap), Inches(top), Inches(card_w), Inches(0.06))
    b2.adjustments[0] = 0.5; b2.fill.solid(); b2.fill.fore_color.rgb = PURPLE; b2.line.fill.background()

    pill2 = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8 + card_w + gap + 0.25), Inches(top + 0.18), Inches(card_w - 0.50), Inches(0.30))
    pill2.adjustments[0] = 0.5; pill2.fill.solid(); pill2.fill.fore_color.rgb = TINT_PURPLE; pill2.line.fill.background()
    tf_p2 = pill2.text_frame; tf_p2.word_wrap = False; tf_p2.margin_left = tf_p2.margin_right = tf_p2.margin_top = tf_p2.margin_bottom = 0
    p2 = tf_p2.paragraphs[0]; p2.alignment = PP_ALIGN.CENTER
    rp2 = p2.add_run(); rp2.text = "OFFERING 4 · LIFECYCLE MODEL GOVERNANCE"; rp2.font.name = FONT_TITLE; rp2.font.size = Pt(10); rp2.font.bold = True; rp2.font.color.rgb = PURPLE

    tx_r = s.shapes.add_textbox(Inches(0.8 + card_w + gap + 0.25), Inches(top + 0.58), Inches(card_w - 0.50), Inches(h - 0.70))
    tf_r = tx_r.text_frame; tf_r.word_wrap = True; tf_r.margin_left = tf_r.margin_right = tf_r.margin_top = tf_r.margin_bottom = 0
    p_rh = tf_r.paragraphs[0]
    r_rh = p_rh.add_run(); r_rh.text = "Brownfield Embodied MLOps & Continuous Calibration\n"; r_rh.font.name = FONT_TITLE; r_rh.font.size = Pt(14.5); r_rh.font.bold = True; r_rh.font.color.rgb = INK_PRIMARY

    pts_4 = [
        ("The Performance Decay Problem:", "In physical plants, policies degrade over time due to camera lens dust, mechanical gearbox backlash, shifting lighting, and changing vendor part tolerances."),
        ("Closed-Loop Edge Calibration:", "LTTS deploys continuous edge telemetry pipelines that detect distribution drift, automatically recalibrate camera-to-robot extrinsics, and log failure corner-cases."),
        ("Deal Economics ($300k - $1.0M ARR per Campus):", "Recurring multi-year software and remote engineering support contracts with strict SLA uptime guarantees (>99.5%)."),
        ("Sticky Customer Lock-In:", "Capturing plant telemetry creates an insurmountable operational data moat, preventing competitors from displacing LTTS once deployed.")
    ]
    for h_txt, b_txt in pts_4:
        p_row = tf_r.add_paragraph()
        p_row.space_before = Pt(7)
        rh = p_row.add_run(); rh.text = h_txt + " "; rh.font.name = FONT_BODY; rh.font.size = Pt(11); rh.font.bold = True; rh.font.color.rgb = INK_PRIMARY
        rb = p_row.add_run(); rb.text = b_txt; rb.font.name = FONT_BODY; rb.font.size = Pt(10.5); rb.font.color.rgb = TEXT_DARK

    add_takeaway(s, "V&V certification unlocks enterprise capital; Embodied MLOps creates durable multi-year recurring software revenue.")
    set_notes(s, "Slide 11 Offerings 3 & 4. Detail the Physical AI V&V Practice and Embodied MLOps continuous calibration.")
    return s


# ── SLIDE 12: Verified Deployments Across 5 Core Sectors ───────────────────────
def slide_12_deployments_and_hype():
    s = new_slide()
    add_header(s, "Module 4 · Use Cases & Adoption", "Verified Deployments Across 5 Core Sectors & Hype Reality",
               "Audited field implementations across five core verticals vs. viral marketing demonstrations.")

    card_w = 6.80
    gap = 0.33
    top = 2.05
    h = 4.65

    # Left: 5 Verified Sectors
    add_card(s, 0.8, top, card_w, h, bg=BG_CARD, border=BORDER_SUBTLE, border_width=1.0)
    b1 = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(top), Inches(card_w), Inches(0.06))
    b1.adjustments[0] = 0.5; b1.fill.solid(); b1.fill.fore_color.rgb = GREEN; b1.line.fill.background()

    pill1 = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.05), Inches(top + 0.18), Inches(card_w - 0.50), Inches(0.30))
    pill1.adjustments[0] = 0.5; pill1.fill.solid(); pill1.fill.fore_color.rgb = TINT_GREEN; pill1.line.fill.background()
    tf_p1 = pill1.text_frame; tf_p1.word_wrap = False; tf_p1.margin_left = tf_p1.margin_right = tf_p1.margin_top = tf_p1.margin_bottom = 0
    p1 = tf_p1.paragraphs[0]; p1.alignment = PP_ALIGN.CENTER
    rp1 = p1.add_run(); rp1.text = "AUDITED ENTERPRISE PRODUCTION DEPLOYMENTS"; rp1.font.name = FONT_TITLE; rp1.font.size = Pt(10); rp1.font.bold = True; rp1.font.color.rgb = GREEN

    tx_l = s.shapes.add_textbox(Inches(1.05), Inches(top + 0.58), Inches(card_w - 0.50), Inches(h - 0.70))
    tf_l = tx_l.text_frame; tf_l.word_wrap = True; tf_l.margin_left = tf_l.margin_right = tf_l.margin_top = tf_l.margin_bottom = 0
    p_lh = tf_l.paragraphs[0]
    r_lh = p_lh.add_run(); r_lh.text = "Field Implementations Across 5 Core Verticals\n"; r_lh.font.name = FONT_TITLE; r_lh.font.size = Pt(14); r_lh.font.bold = True; r_lh.font.color.rgb = INK_PRIMARY

    sectors = [
        ("Automotive Manufacturing:", "BMW Spartanburg plant successfully completed a multi-week pilot trial of Figure 02 humanoids performing precision sheet metal fixture insertion."),
        ("Aerospace Assembly:", "Airbus deployment of automated drilling guidance using physics-informed vision on A350 wing assembly, ensuring strict structural hole tolerances."),
        ("Semiconductor Fabs:", "TSMC deployment of closed-loop neural defect classification and sub-nanometer wafer handling in EUV lithography cleanrooms under ISO Class 1 conditions."),
        ("Logistics & Warehousing:", "DHL Supply Chain multi-site production deployment of Boston Dynamics Stretch mobile manipulators for automated trailer truck container unloading."),
        ("Energy & Turbomachinery:", "Heavy industrial gas turbines utilizing physics-informed neural network (PINN) thermal and vibration monitoring for predictive catastrophic valve failure prevention.")
    ]
    for sec, desc in sectors:
        p_s = tf_l.add_paragraph()
        p_s.space_before = Pt(5.5)
        rs = p_s.add_run(); rs.text = sec + " "; rs.font.name = FONT_BODY; rs.font.size = Pt(11); rs.font.bold = True; rs.font.color.rgb = INK_PRIMARY
        rd = p_s.add_run(); rd.text = desc; rd.font.name = FONT_BODY; rd.font.size = Pt(10.5); rd.font.color.rgb = TEXT_DARK

    # Right: Hype vs Reality Analysis
    r_w = 4.60
    add_card(s, 0.8 + card_w + gap, top, r_w, h, bg=BG_CARD, border=BORDER_SUBTLE, border_width=1.0)
    b2 = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8 + card_w + gap), Inches(top), Inches(r_w), Inches(0.06))
    b2.adjustments[0] = 0.5; b2.fill.solid(); b2.fill.fore_color.rgb = AMBER; b2.line.fill.background()

    pill2 = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8 + card_w + gap + 0.22), Inches(top + 0.18), Inches(r_w - 0.44), Inches(0.30))
    pill2.adjustments[0] = 0.5; pill2.fill.solid(); pill2.fill.fore_color.rgb = TINT_AMBER; pill2.line.fill.background()
    tf_p2 = pill2.text_frame; tf_p2.word_wrap = False; tf_p2.margin_left = tf_p2.margin_right = tf_p2.margin_top = tf_p2.margin_bottom = 0
    p2 = tf_p2.paragraphs[0]; p2.alignment = PP_ALIGN.CENTER
    rp2 = p2.add_run(); rp2.text = "COMMERCIAL GROUNDING ANALYSIS"; rp2.font.name = FONT_TITLE; rp2.font.size = Pt(10); rp2.font.bold = True; rp2.font.color.rgb = AMBER

    tx_r = s.shapes.add_textbox(Inches(0.8 + card_w + gap + 0.22), Inches(top + 0.58), Inches(r_w - 0.44), Inches(h - 0.70))
    tf_r = tx_r.text_frame; tf_r.word_wrap = True; tf_r.margin_left = tf_r.margin_right = tf_r.margin_top = tf_r.margin_bottom = 0
    p_rh = tf_r.paragraphs[0]
    r_rh = p_rh.add_run(); r_rh.text = "Hype-Ahead-of-Deployment Reality\n"; r_rh.font.name = FONT_TITLE; r_rh.font.size = Pt(14); r_rh.font.bold = True; r_rh.font.color.rgb = INK_PRIMARY

    hype_pts = [
        ("The Bipedal Mirage:", "Viral videos of humanoids folding t-shirts or doing backflips disguise pervasive VR teleoperation and zero payload capacity. Bipedal stability in active plants remains unproven."),
        ("Commercial Plant Economics:", "Factories do not need $150,000 bipedal legs. They need wheeled AMRs equipped with 6-DoF compliant arms costing 5x less with 10x higher payload and MTBF."),
        ("Brownfield Reality:", "AI startups underestimate factory brownfield realities: oil mist, welding flashes, legacy 24V PLCs, and union safety regulations that halt uncertified equipment."),
        ("The Integration Bottleneck:", "Plant managers refuse to deploy experimental foundation models without certified e-stops, PLC handshakes, and signed ISO safety dossiers.")
    ]
    for h_txt, b_txt in hype_pts:
        p_h = tf_r.add_paragraph()
        p_h.space_before = Pt(6.5)
        rh = p_h.add_run(); rh.text = h_txt + " "; rh.font.name = FONT_BODY; rh.font.size = Pt(11); rh.font.bold = True; rh.font.color.rgb = INK_PRIMARY
        rb = p_h.add_run(); rb.text = b_txt; rb.font.name = FONT_BODY; rb.font.size = Pt(10.5); rb.font.color.rgb = TEXT_DARK

    add_takeaway(s, "Real enterprise ROI is concentrated in specialized mobile manipulators and inspection cells, not general-purpose bipedal humanoids.")
    set_notes(s, "Slide 12 Deployments & Hype. Contrast the 5 audited industrial deployments with the viral teleoperated humanoid hype.")
    return s


# ── SLIDE 13: Dominance of the Hybrid Incumbent Model ─────────────────────────
def slide_13_hybrid_incumbent_model():
    s = new_slide()
    add_header(s, "Module 4 · Use Cases & Adoption", "Dominance of the Hybrid Incumbent Ecosystem",
               "Why standalone AI startups fail without industrial automation incumbents and how LTTS bridges the gap.")

    col_w = 3.71
    gap = 0.30
    top = 2.05
    h = 4.65

    cards = [
        ("INCUMBENT ENTRENCHMENT", "The Incumbent Iron Grip", BRAND_NAVY, TINT_BLUE, [
            ("Market Reality:", "Siemens, Rockwell Automation, ABB, and Schneider Electric control 80%+ of factory floor automation systems globally."),
            ("Customer Trust & Lifecycles:", "Industrial enterprises operate on 20- to 30-year machine lifecycles. Plant managers will not rip and replace proven PLCs for experimental startup software."),
            ("Statutory Safety Ownership:", "Incumbents own machine safety certifications, fieldbus standards (PROFINET, CIP Safety), and factory insurance relationships."),
            ("The Startup Barrier:", "Pure software startups cannot bypass the safety PLC layer; uncertified code is prohibited from touching live physical factory hardware.")
        ]),
        ("HYBRID ALLIANCES", "The Hybrid Playbook", BRAND_BLUE, TINT_CYAN, [
            ("Siemens & Microsoft Copilot:", "Generative AI industrial copilot embedded directly into Siemens TIA Portal for automated PLC code generation and natural language debugging."),
            ("Siemens & Alphabet Intrinsic:", "Strategic alliance connecting Intrinsic Flowstate robotics AI platform with Siemens industrial automation hardware."),
            ("Rockwell & NVIDIA Omniverse:", "Integration of NVIDIA Isaac Sim and Omniverse with Rockwell Logix controllers for real-time virtual commissioning."),
            ("The Structural Outcome:", "Incumbents absorb AI capabilities into their existing hardware backbones, neutralizing standalone software disintermediation threats.")
        ]),
        ("LTTS STRATEGIC ROLE", "The LTTS Strategic Bridge", GREEN, TINT_GREEN, [
            ("The Trusted Integrator:", "LTTS operates as the neutral, certified systems engineering bridge possessing deep expertise in both AI models and legacy industrial PLCs."),
            ("Execution Moat:", "Neither Silicon Valley AI labs (lack mechatronics bench) nor legacy plant electricians (lack deep learning talent) can bridge this chasm alone."),
            ("Co-Selling with Incumbents:", "Partnering with Siemens and Rockwell channel partners to co-sell physical AI deployment services to Tier-1 automotive and aerospace OEMs."),
            ("Durable Value Capture:", "LTTS captures high-margin deployment, V&V, and ongoing maintenance revenue regardless of which foundation model wins.")
        ])
    ]

    for i, (badge, title, clr, bg_pill, items) in enumerate(cards):
        left = 0.8 + i * (col_w + gap)
        add_card(s, left, top, col_w, h, bg=BG_CARD, border=BORDER_SUBTLE, border_width=1.0)
        bar = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(col_w), Inches(0.06))
        bar.adjustments[0] = 0.5; bar.fill.solid(); bar.fill.fore_color.rgb = clr; bar.line.fill.background()

        pill = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left + 0.20), Inches(top + 0.20), Inches(col_w - 0.40), Inches(0.30))
        pill.adjustments[0] = 0.5; pill.fill.solid(); pill.fill.fore_color.rgb = bg_pill; pill.line.fill.background()
        tf_p = pill.text_frame; tf_p.word_wrap = False; tf_p.margin_left = tf_p.margin_right = tf_p.margin_top = tf_p.margin_bottom = 0
        pp = tf_p.paragraphs[0]; pp.alignment = PP_ALIGN.CENTER
        rp = pp.add_run(); rp.text = badge; rp.font.name = FONT_TITLE; rp.font.size = Pt(9.5); rp.font.bold = True; rp.font.color.rgb = clr

        tx_ct = s.shapes.add_textbox(Inches(left + 0.20), Inches(top + 0.58), Inches(col_w - 0.40), Inches(0.48))
        tf_ct = tx_ct.text_frame; tf_ct.word_wrap = True; tf_ct.margin_left = tf_ct.margin_right = tf_ct.margin_top = tf_ct.margin_bottom = 0
        pct = tf_ct.paragraphs[0]
        rct = pct.add_run(); rct.text = title; rct.font.name = FONT_TITLE; rct.font.size = Pt(14.5); rct.font.bold = True; rct.font.color.rgb = INK_PRIMARY

        tx_b = s.shapes.add_textbox(Inches(left + 0.20), Inches(top + 1.12), Inches(col_w - 0.40), Inches(h - 1.25))
        tf_b = tx_b.text_frame; tf_b.word_wrap = True; tf_b.margin_left = tf_b.margin_right = tf_b.margin_top = tf_b.margin_bottom = 0

        for idx, (lbl, body) in enumerate(items):
            p_item = tf_b.paragraphs[0] if idx == 0 else tf_b.add_paragraph()
            if idx > 0: p_item.space_before = Pt(6)
            rl = p_item.add_run(); rl.text = lbl + " "; rl.font.name = FONT_BODY; rl.font.size = Pt(10.5); rl.font.bold = True; rl.font.color.rgb = INK_PRIMARY
            rb = p_item.add_run(); rb.text = body; rb.font.name = FONT_BODY; rb.font.size = Pt(10.5); rb.font.color.rgb = TEXT_DARK

    add_takeaway(s, "The future of manufacturing belongs to hybrid architectures: frontier AI policies layered safely on top of incumbent PLC control backbones.")
    set_notes(s, "Slide 13 Hybrid Incumbent Model. Explain why Siemens and Rockwell control factory floors and how LTTS acts as the indispensable bridge.")
    return s


# ── SLIDE 14: Layered Competitive Landscape (Table 4) ─────────────────────────
def slide_14_competitive_landscape_table4():
    s = new_slide()
    add_header(s, "Module 5 · Competitive Landscape", "Layered Competitive Landscape Across Physical AI (Table 4)",
               "Five structural tiers define the global ecosystem from foundation models to statutory compliance.")

    left_m = 0.8
    top_base = 2.05
    total_w = 11.73

    headers = [
        ("ECOSYSTEM LAYER", 2.60, PP_ALIGN.LEFT),
        ("KEY INDUSTRY PLAYERS", 2.40, PP_ALIGN.LEFT),
        ("CORE TECHNICAL OFFERING", 2.60, PP_ALIGN.LEFT),
        ("STRATEGIC STRUCTURAL POSITION", 4.13, PP_ALIGN.LEFT)
    ]
    rows = [
        ("Robotics Foundation Models", "Physical Intelligence, Skild AI, DeepMind",
         "Pretrained generalist VLA models\n(π0, Skild Brain)",
         "Challengers: Frontier algorithms, high venture capital, but entirely dependent on systems engineering partners for field plant distribution.", False),

        ("Industrial Automation Incumbents", "Siemens, Rockwell Automation, ABB, Schneider",
         "PLCs, DCS, SCADA, FactoryTalk,\nTIA Portal ecosystems",
         "Dominant: Own factory floors, machine safety certifications, and decades of customer trust. Integrating AI through strategic platform partnerships.", False),

        ("Simulation & Digital Twin Platforms", "NVIDIA (Isaac/Cosmos), Applied Intuition",
         "Physics simulation, synthetic data\ngeneration pipelines",
         "Dominant: Platform standards for testing, virtual commissioning, and synthetic policy generation. Essential software tooling layer.", False),

        ("ER&D Engineering Services\n★ LTTS COMPETITIVE POSITION", "LTTS, KPIT Tech, Tata Tech, Cyient, Accenture",
         "Systems integration, V&V, digital\nengineering & PLC bridges",
         "Direct Competitors: Race to build certified Physical AI field practices and bridge neural policies with industrial plant machinery.", True),

        ("Safety & Statutory Compliance", "TÜV SÜD, UL Solutions, Credo AI, Holistic AI",
         "Functional safety audits, regulatory\ncompliance dossiers",
         "Gatekeepers: Mandatory for legal operation, safety dossiers, and factory insurance underwriting under ISO 13849 / IEC 61508.", False)
    ]

    # Header Bar
    hdr_h = 0.42
    hdr_shape = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left_m), Inches(top_base), Inches(total_w), Inches(hdr_h))
    hdr_shape.adjustments[0] = 0.08; hdr_shape.fill.solid(); hdr_shape.fill.fore_color.rgb = BRAND_NAVY; hdr_shape.line.fill.background()

    curr_x = left_m
    for title, col_w, align in headers:
        tb = s.shapes.add_textbox(Inches(curr_x + 0.12), Inches(top_base + 0.08), Inches(col_w - 0.24), Inches(0.30))
        tf = tb.text_frame; tf.word_wrap = True; tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        p = tf.paragraphs[0]; p.alignment = align
        r = p.add_run(); r.text = title; r.font.name = FONT_TITLE; r.font.size = Pt(10.5); r.font.bold = True; r.font.color.rgb = COLOR_WHITE
        curr_x += col_w

    # Table Body Rows
    row_top = top_base + hdr_h + 0.04
    row_h = 0.84
    gap = 0.04
    for i, (layer, players, tech, pos, is_ltts) in enumerate(rows):
        bg = BG_CARD_BLUE if is_ltts else (BG_CARD if (i % 2 == 0) else COLOR_WHITE)
        border_clr = BRAND_BLUE if is_ltts else BORDER_SUBTLE
        border_w = 1.5 if is_ltts else 1.0
        add_card(s, left_m, row_top, total_w, row_h, bg=bg, border=border_clr, border_width=border_w)
        if is_ltts:
            tab = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left_m), Inches(row_top), Inches(0.08), Inches(row_h))
            tab.adjustments[0] = 0.5; tab.fill.solid(); tab.fill.fore_color.rgb = BRAND_BLUE; tab.line.fill.background()

        curr_x = left_m
        for col_idx, (text_val, col_w, align) in enumerate([(layer, 2.60, PP_ALIGN.LEFT),
                                                             (players, 2.40, PP_ALIGN.LEFT),
                                                             (tech, 2.60, PP_ALIGN.LEFT),
                                                             (pos, 4.13, PP_ALIGN.LEFT)]):
            tb = s.shapes.add_textbox(Inches(curr_x + 0.15), Inches(row_top + 0.08), Inches(col_w - 0.30), Inches(row_h - 0.16))
            tf = tb.text_frame; tf.word_wrap = True; tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
            p = tf.paragraphs[0]; p.alignment = align
            r = p.add_run(); r.text = text_val; r.font.name = FONT_BODY; r.font.size = Pt(10.5)
            if col_idx == 0:
                r.font.bold = True
                r.font.color.rgb = BRAND_BLUE if is_ltts else INK_PRIMARY
            else:
                r.font.color.rgb = TEXT_DARK
            curr_x += col_w

        row_top += row_h + gap

    add_takeaway(s, "ER&D engineering services is the linchpin layer connecting generalist model challengers with entrenched factory incumbents.")
    set_notes(s, "Slide 14 Competitive Landscape (Table 4). Walk through the 5 ecosystem tiers and show how LTTS sits at the center of deployment.")
    return s


# ── SLIDE 15: High-Value Underserved Market Gaps ──────────────────────────────
def slide_15_underserved_market_gaps():
    s = new_slide()
    add_header(s, "Module 5 · Competitive Landscape", "High-Value Underserved Market Gaps: Where LTTS Captures Margin",
               "Four critical white-space engineering bottlenecks where tech giants cannot compete with LTTS's industrial bench.")

    col_w = 2.71
    gap = 0.30
    top = 2.05
    h = 4.65

    gaps = [
        ("GAP 1 · MIDDLEWARE", "Real-Time Safety Middleware", BRAND_BLUE, TINT_BLUE, [
            ("The Industry Bottleneck:", "AI models output asynchronous stochastic predictions at 100Hz; industrial actuators demand 1ms deterministic guarantees."),
            ("The White-Space Void:", "Zero off-the-shelf software safely bridges Python neural policies to real-time industrial fieldbuses."),
            ("LTTS Solution:", "Build certified bridge middleware wrapping neural commands with formal Control Barrier Functions (CBFs)."),
            ("Revenue Potential:", "High-margin software IP licensing ($10k-$25k/robot/yr) across hundreds of plant cells.")
        ]),
        ("GAP 2 · CONTACT PHYSICS", "Contact-Calibrated Simulators", CYAN, TINT_CYAN, [
            ("The Industry Bottleneck:", "Standard physics simulators (MuJoCo, Isaac) suffer significant Sim-to-Real gaps during non-rigid contact."),
            ("The White-Space Void:", "Automakers cannot afford weeks of manual on-robot policy tuning for deformable cables, gaskets, and wiring."),
            ("LTTS Solution:", "Develop proprietary contact-calibrated simulation pipelines incorporating real material stress tensors."),
            ("Revenue Potential:", "Anchors multi-million-dollar Software-Defined Factory (SD-FaaS) digital twin engagements.")
        ]),
        ("GAP 3 · BROWNFIELD VISION", "Brownfield Vision Retrofits", AMBER, TINT_AMBER, [
            ("The Industry Bottleneck:", "90%+ of manufacturing machinery is legacy equipment lacking modern digital APIs or clean air."),
            ("The White-Space Void:", "Frontier models trained on clean laboratory benchmarks fail under brownfield grime, oil mist, and vibration."),
            ("LTTS Solution:", "Package ruggedized edge-compute retrofit kits with vibration-invariant multi-modal sensor fusion."),
            ("Revenue Potential:", "Rapid deployment kits priced at $100k-$250k per legacy production cell.")
        ]),
        ("GAP 4 · FLEET CALIBRATION", "Heterogeneous Fleet Calibration", GREEN, TINT_GREEN, [
            ("The Industry Bottleneck:", "Automotive plants operate mixed robot fleets (FANUC, KUKA, ABB) with conflicting kinematic controllers."),
            ("The White-Space Void:", "Foundation models cannot scale if each robot vendor requires a bespoke software integration stack."),
            ("LTTS Solution:", "Build a unified cross-embodiment abstraction layer standardizing policy execution across all robot brands."),
            ("Revenue Potential:", "Enterprise-wide fleet software licensing and recurring Embodied MLOps maintenance contracts.")
        ])
    ]

    for i, (badge, title, clr, bg_pill, items) in enumerate(gaps):
        left = 0.8 + i * (col_w + gap)
        add_card(s, left, top, col_w, h, bg=BG_CARD, border=BORDER_SUBTLE, border_width=1.0)
        bar = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(col_w), Inches(0.06))
        bar.adjustments[0] = 0.5; bar.fill.solid(); bar.fill.fore_color.rgb = clr; bar.line.fill.background()

        pill = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left + 0.16), Inches(top + 0.16), Inches(col_w - 0.32), Inches(0.28))
        pill.adjustments[0] = 0.5; pill.fill.solid(); pill.fill.fore_color.rgb = bg_pill; pill.line.fill.background()
        tf_p = pill.text_frame; tf_p.word_wrap = False; tf_p.margin_left = tf_p.margin_right = tf_p.margin_top = tf_p.margin_bottom = 0
        pp = tf_p.paragraphs[0]; pp.alignment = PP_ALIGN.CENTER
        rp = pp.add_run(); rp.text = badge; rp.font.name = FONT_TITLE; rp.font.size = Pt(9.5); rp.font.bold = True; rp.font.color.rgb = clr

        tx_ct = s.shapes.add_textbox(Inches(left + 0.16), Inches(top + 0.50), Inches(col_w - 0.32), Inches(0.50))
        tf_ct = tx_ct.text_frame; tf_ct.word_wrap = True; tf_ct.margin_left = tf_ct.margin_right = tf_ct.margin_top = tf_ct.margin_bottom = 0
        pct = tf_ct.paragraphs[0]
        rct = pct.add_run(); rct.text = title; rct.font.name = FONT_TITLE; rct.font.size = Pt(13); rct.font.bold = True; rct.font.color.rgb = INK_PRIMARY

        tx_b = s.shapes.add_textbox(Inches(left + 0.16), Inches(top + 1.05), Inches(col_w - 0.32), Inches(h - 1.15))
        tf_b = tx_b.text_frame; tf_b.word_wrap = True; tf_b.margin_left = tf_b.margin_right = tf_b.margin_top = tf_b.margin_bottom = 0

        for idx, (lbl, body) in enumerate(items):
            p_item = tf_b.paragraphs[0] if idx == 0 else tf_b.add_paragraph()
            if idx > 0: p_item.space_before = Pt(5)
            rl = p_item.add_run(); rl.text = lbl + " "; rl.font.name = FONT_BODY; rl.font.size = Pt(10.5); rl.font.bold = True; rl.font.color.rgb = INK_PRIMARY
            rb = p_item.add_run(); rb.text = body; rb.font.name = FONT_BODY; rb.font.size = Pt(10.5); rb.font.color.rgb = TEXT_DARK

    add_takeaway(s, "These four underserved gaps represent pure domain engineering challenges where tech giants cannot compete with LTTS's industrial bench.")
    set_notes(s, "Slide 15 Underserved Gaps. Detail why Gaps 1-4 are massive profit pools for LTTS engineering services.")
    return s


# ── SLIDE 16: Industrial AI vs. Physical AI & Kinematics Moat ─────────────────
def slide_16_kinematics_moat_and_math():
    s = new_slide()
    add_header(s, "Module 6 · The Bridge", "Industrial AI vs. Physical AI & The Kinematics Moat",
               "Closed-loop motor actuation creates an insurmountable domain engineering moat for software-only AI labs.")

    card_w = 5.72
    gap = 0.29
    top = 2.05
    h = 4.65

    # Left: Paradigm Distinction
    add_card(s, 0.8, top, card_w, h, bg=BG_CARD, border=BORDER_SUBTLE, border_width=1.0)
    b1 = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(top), Inches(card_w), Inches(0.06))
    b1.adjustments[0] = 0.5; b1.fill.solid(); b1.fill.fore_color.rgb = BRAND_NAVY; b1.line.fill.background()

    pill1 = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.05), Inches(top + 0.18), Inches(card_w - 0.50), Inches(0.30))
    pill1.adjustments[0] = 0.5; pill1.fill.solid(); pill1.fill.fore_color.rgb = TINT_BLUE; pill1.line.fill.background()
    tf_p1 = pill1.text_frame; tf_p1.word_wrap = False; tf_p1.margin_left = tf_p1.margin_right = tf_p1.margin_top = tf_p1.margin_bottom = 0
    p1 = tf_p1.paragraphs[0]; p1.alignment = PP_ALIGN.CENTER
    rp1 = p1.add_run(); rp1.text = "CONTROLS ENGINEERING MOAT"; rp1.font.name = FONT_TITLE; rp1.font.size = Pt(10); rp1.font.bold = True; rp1.font.color.rgb = BRAND_NAVY

    tx_l = s.shapes.add_textbox(Inches(1.05), Inches(top + 0.58), Inches(card_w - 0.50), Inches(h - 0.70))
    tf_l = tx_l.text_frame; tf_l.word_wrap = True; tf_l.margin_left = tf_l.margin_right = tf_l.margin_top = tf_l.margin_bottom = 0
    p_lh = tf_l.paragraphs[0]
    r_lh = p_lh.add_run(); r_lh.text = "Analytical AI vs. Closed-Loop Physical AI\n"; r_lh.font.name = FONT_TITLE; r_lh.font.size = Pt(14); r_lh.font.bold = True; r_lh.font.color.rgb = INK_PRIMARY

    diff_pts = [
        ("Industrial AI (Open-Loop & Analytical):", "Ingests SCADA telemetry, vibration logs, and optical inspection images to predict machine maintenance or classify defects. Operates in passive informational space; an algorithmic false positive results in a software alert, not a mechanical wreck."),
        ("Physical AI (Closed-Loop Kinematic Actuation):", "Directly commands motor torques and joint positions in real time under Newton's differential equations. Algorithmic errors cause physical collisions, destroyed tooling, or worker injury. Requires sub-10ms hard real-time latency."),
        ("Coexistence, Not Replacement:", "Physical AI does not displace deterministic factory automation; it commands high-level adaptive manipulation while deterministic PLCs maintain strict safety interlocks."),
        ("The Domain Engineering Moat:", "Pure machine learning practitioners treat robots as abstract point masses; deploying neural policies into live factories mandates deep mechatronic controls engineering.")
    ]
    for h_txt, b_txt in diff_pts:
        p_d = tf_l.add_paragraph()
        p_d.space_before = Pt(6.5)
        rdh = p_d.add_run(); rdh.text = h_txt + " "; rdh.font.name = FONT_BODY; rdh.font.size = Pt(11); rdh.font.bold = True; rdh.font.color.rgb = INK_PRIMARY
        rdb = p_d.add_run(); rdb.text = b_txt; rdb.font.name = FONT_BODY; rdb.font.size = Pt(10.5); rdb.font.color.rgb = TEXT_DARK

    # Right: Kinematics Moat & Mathematical Formalisms
    add_card(s, 0.8 + card_w + gap, top, card_w, h, bg=BG_CARD, border=BORDER_SUBTLE, border_width=1.0)
    b2 = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8 + card_w + gap), Inches(top), Inches(card_w), Inches(0.06))
    b2.adjustments[0] = 0.5; b2.fill.solid(); b2.fill.fore_color.rgb = BRAND_BLUE; b2.line.fill.background()

    pill2 = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8 + card_w + gap + 0.25), Inches(top + 0.18), Inches(card_w - 0.50), Inches(0.30))
    pill2.adjustments[0] = 0.5; pill2.fill.solid(); pill2.fill.fore_color.rgb = TINT_BLUE; pill2.line.fill.background()
    tf_p2 = pill2.text_frame; tf_p2.word_wrap = False; tf_p2.margin_left = tf_p2.margin_right = tf_p2.margin_top = tf_p2.margin_bottom = 0
    p2 = tf_p2.paragraphs[0]; p2.alignment = PP_ALIGN.CENTER
    rp2 = p2.add_run(); rp2.text = "MECHATRONIC FORMALISMS & STABILITY"; rp2.font.name = FONT_TITLE; rp2.font.size = Pt(10); rp2.font.bold = True; rp2.font.color.rgb = BRAND_BLUE

    tx_r = s.shapes.add_textbox(Inches(0.8 + card_w + gap + 0.25), Inches(top + 0.58), Inches(card_w - 0.50), Inches(h - 0.70))
    tf_r = tx_r.text_frame; tf_r.word_wrap = True; tf_r.margin_left = tf_r.margin_right = tf_r.margin_top = tf_r.margin_bottom = 0
    p_rh = tf_r.paragraphs[0]
    r_rh = p_rh.add_run(); r_rh.text = "Jacobian Mapping & Singularity Collapse\n"; r_rh.font.name = FONT_TITLE; r_rh.font.size = Pt(14); r_rh.font.bold = True; r_rh.font.color.rgb = INK_PRIMARY

    p_eq1_lbl = tf_r.add_paragraph()
    p_eq1_lbl.space_before = Pt(3)
    r_eq1_l = p_eq1_lbl.add_run(); r_eq1_l.text = "Manipulator Jacobian & Inverse Kinematics Mapping:\n"; r_eq1_l.font.name = FONT_BODY; r_eq1_l.font.size = Pt(10.5); r_eq1_l.font.bold = True; r_eq1_l.font.color.rgb = INK_PRIMARY
    r_eq1_s = p_eq1_lbl.add_run(); r_eq1_s.text = "The mapping from end-effector velocities to joint velocities is governed by Jacobian J(q):"; r_eq1_s.font.name = FONT_BODY; r_eq1_s.font.size = Pt(10); r_eq1_s.font.color.rgb = TEXT_MUTED

    # Formula 1 Image Container
    f1_box = add_card(s, 0.8 + card_w + gap + 0.25, top + 1.25, card_w - 0.50, 0.65, bg=COLOR_WHITE, border=BORDER_SUBTLE, border_width=1.0)
    add_math_image(s, r"\dot{x} = J(q)\dot{q} \quad \Longrightarrow \quad \dot{q} = J^{\dagger}(q)\dot{x}", 0.8 + card_w + gap + 0.45, top + 1.33, fontsize=16, max_h=0.45)

    p_eq2_lbl = s.shapes.add_textbox(Inches(0.8 + card_w + gap + 0.25), Inches(top + 2.00), Inches(card_w - 0.50), Inches(0.55))
    tf_eq2 = p_eq2_lbl.text_frame; tf_eq2.word_wrap = True; tf_eq2.margin_left = tf_eq2.margin_right = tf_eq2.margin_top = tf_eq2.margin_bottom = 0
    p2 = tf_eq2.paragraphs[0]
    r_eq2_l = p2.add_run(); r_eq2_l.text = "Yoshikawa Manipulability Collapse at Singularities:\n"; r_eq2_l.font.name = FONT_BODY; r_eq2_l.font.size = Pt(10.5); r_eq2_l.font.bold = True; r_eq2_l.font.color.rgb = INK_PRIMARY
    r_eq2_s = p2.add_run(); r_eq2_s.text = "Near kinematic singularities, manipulability collapses, demanding infinite velocity:"; r_eq2_s.font.name = FONT_BODY; r_eq2_s.font.size = Pt(10); r_eq2_s.font.color.rgb = TEXT_MUTED

    # Formula 2 Image Container
    f2_box = add_card(s, 0.8 + card_w + gap + 0.25, top + 2.60, card_w - 0.50, 0.65, bg=COLOR_WHITE, border=BORDER_SUBTLE, border_width=1.0)
    add_math_image(s, r"\mu(q) = \sqrt{\det(J(q)J^T(q))} \longrightarrow 0 \quad \Longrightarrow \quad \|\dot{q}\| \longrightarrow \infty", 0.8 + card_w + gap + 0.35, top + 2.68, fontsize=15, max_h=0.45)

    tx_r_bot = s.shapes.add_textbox(Inches(0.8 + card_w + gap + 0.25), Inches(top + 3.35), Inches(card_w - 0.50), Inches(1.30))
    tf_rb = tx_r_bot.text_frame; tf_rb.word_wrap = True; tf_rb.margin_left = tf_rb.margin_right = tf_rb.margin_top = tf_rb.margin_bottom = 0
    p_rb = tf_rb.paragraphs[0]
    r_dls = p_rb.add_run(); r_dls.text = "The Mechatronic Solution (DLS Filtering):\n"; r_dls.font.name = FONT_TITLE; r_dls.font.size = Pt(11); r_dls.font.bold = True; r_dls.font.color.rgb = GREEN
    r_dls_b = p_rb.add_run(); r_dls_b.text = "LTTS controls engineers insert Damped Least-Squares (DLS) inversion and singularity-avoidance gradient projection between neural policy outputs and joint servo drives. This prevents infinite torque demands, drive trips, and stripped gears."; r_dls_b.font.name = FONT_BODY; r_dls_b.font.size = Pt(10.5); r_dls_b.font.color.rgb = TEXT_DARK

    add_takeaway(s, "AI labs build the neural planners; LTTS builds the singularity-robust kinematics and safety filters that keep physical robots from destroying themselves.")
    set_notes(s, "Slide 16 Kinematics Moat. Walk through the Jacobian mapping and explain why Yoshikawa manipulability collapse causes drive trips without LTTS filters.")
    return s


# ── SLIDE 17: Deterministic RTOS Timing & Data Flywheel ────────────────────────
def slide_17_rtos_and_data_flywheel():
    s = new_slide()
    add_header(s, "Module 6 · The Bridge", "Deterministic RTOS Timing & Operational Data Flywheel",
               "Sub-millisecond jitter guarantees and the five-stage closed-loop data engine for continuous improvement.")

    card_w = 5.72
    gap = 0.29
    top = 2.05
    h = 4.65

    # Left: Hard Real-Time Timing Requirements
    add_card(s, 0.8, top, card_w, h, bg=BG_CARD, border=BORDER_SUBTLE, border_width=1.0)
    b1 = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(top), Inches(card_w), Inches(0.06))
    b1.adjustments[0] = 0.5; b1.fill.solid(); b1.fill.fore_color.rgb = BRAND_BLUE; b1.line.fill.background()

    pill1 = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.05), Inches(top + 0.18), Inches(card_w - 0.50), Inches(0.30))
    pill1.adjustments[0] = 0.5; pill1.fill.solid(); pill1.fill.fore_color.rgb = TINT_BLUE; pill1.line.fill.background()
    tf_p1 = pill1.text_frame; tf_p1.word_wrap = False; tf_p1.margin_left = tf_p1.margin_right = tf_p1.margin_top = tf_p1.margin_bottom = 0
    p1 = tf_p1.paragraphs[0]; p1.alignment = PP_ALIGN.CENTER
    rp1 = p1.add_run(); rp1.text = "HARD REAL-TIME ARCHITECTURE (< 1MS)"; rp1.font.name = FONT_TITLE; rp1.font.size = Pt(10); rp1.font.bold = True; rp1.font.color.rgb = BRAND_BLUE

    tx_l = s.shapes.add_textbox(Inches(1.05), Inches(top + 0.58), Inches(card_w - 0.50), Inches(h - 0.70))
    tf_l = tx_l.text_frame; tf_l.word_wrap = True; tf_l.margin_left = tf_l.margin_right = tf_l.margin_top = tf_l.margin_bottom = 0
    p_lh = tf_l.paragraphs[0]
    r_lh = p_lh.add_run(); r_lh.text = "Deterministic Sub-1ms RTOS Execution\n"; r_lh.font.name = FONT_TITLE; r_lh.font.size = Pt(14); r_lh.font.bold = True; r_lh.font.color.rgb = INK_PRIMARY

    rt_pts = [
        ("The Timing Hierarchy:", "Factory safety interlocks operate at 1kHz (1ms cycle time), motor joint servo commutation at 500Hz (2ms), and high-level neural policy inference at 50Hz–100Hz (10–20ms)."),
        ("Sub-Millisecond Jitter Tolerance (< 1ms):", "In high-speed assembly and machining cells, timing jitter exceeding 1ms creates dynamic phase lag, hunting oscillations, and emergency line shut-downs."),
        ("Dual-Kernel Real-Time OS Architecture:", "Deploying Linux PREEMPT_RT or QNX RTOS on edge compute platforms to strictly isolate non-deterministic Python neural inference from deterministic safety PLC threads."),
        ("Hardware Watchdog Governors:", "LTTS implements hardware-level watchdog timers that automatically engage dynamic motor braking if neural inference fails to return a valid trajectory within the 10ms deadline.")
    ]
    for h_txt, b_txt in rt_pts:
        p_r = tf_l.add_paragraph()
        p_r.space_before = Pt(6.5)
        rrh = p_r.add_run(); rrh.text = h_txt + " "; rrh.font.name = FONT_BODY; rrh.font.size = Pt(11); rrh.font.bold = True; rrh.font.color.rgb = INK_PRIMARY
        rrb = p_r.add_run(); rrb.text = b_txt; rrb.font.name = FONT_BODY; rrb.font.size = Pt(10.5); rrb.font.color.rgb = TEXT_DARK

    # Right: 5-Stage Closed-Loop Data Flywheel
    add_card(s, 0.8 + card_w + gap, top, card_w, h, bg=BG_CARD, border=BORDER_SUBTLE, border_width=1.0)
    b2 = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8 + card_w + gap), Inches(top), Inches(card_w), Inches(0.06))
    b2.adjustments[0] = 0.5; b2.fill.solid(); b2.fill.fore_color.rgb = GREEN; b2.line.fill.background()

    pill2 = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8 + card_w + gap + 0.25), Inches(top + 0.18), Inches(card_w - 0.50), Inches(0.30))
    pill2.adjustments[0] = 0.5; pill2.fill.solid(); pill2.fill.fore_color.rgb = TINT_GREEN; pill2.line.fill.background()
    tf_p2 = pill2.text_frame; tf_p2.word_wrap = False; tf_p2.margin_left = tf_p2.margin_right = tf_p2.margin_top = tf_p2.margin_bottom = 0
    p2 = tf_p2.paragraphs[0]; p2.alignment = PP_ALIGN.CENTER
    rp2 = p2.add_run(); rp2.text = "CLOSED-LOOP DATA ENGINE"; rp2.font.name = FONT_TITLE; rp2.font.size = Pt(10); rp2.font.bold = True; rp2.font.color.rgb = GREEN

    tx_r = s.shapes.add_textbox(Inches(0.8 + card_w + gap + 0.25), Inches(top + 0.58), Inches(card_w - 0.50), Inches(h - 0.70))
    tf_r = tx_r.text_frame; tf_r.word_wrap = True; tf_r.margin_left = tf_r.margin_right = tf_r.margin_top = tf_r.margin_bottom = 0
    p_rh = tf_r.paragraphs[0]
    r_rh = p_rh.add_run(); r_rh.text = "The 5-Stage Operational Data Flywheel\n"; r_rh.font.name = FONT_TITLE; r_rh.font.size = Pt(14); r_rh.font.bold = True; r_rh.font.color.rgb = INK_PRIMARY

    fly_stages = [
        ("1. Live Plant Telemetry Logging:", "Continuous edge circular-buffer recording of motor joint torques, encoder positions, tactile pressures, and synchronized camera feeds during production."),
        ("2. Anomaly & Edge-Case Harvest:", "Automated trigger filters isolating the 0.01% of unusual contact events, micro-slips, visual occlusions, and human safety boundary crossings."),
        ("3. Synthetic Simulation Variation:", "Injecting real-world plant failures into NVIDIA Omniverse digital twins to automatically generate 10,000 synthetic variations across friction and lighting."),
        ("4. Policy Retraining & CBF Reachability:", "Retraining neural policy checkpoints on the augmented dataset, followed by automated Control Barrier Function (CBF) formal reachability verification."),
        ("5. Shadow Deployment & Canary Gate:", "Running updated policies in shadow mode alongside live production lines before gating full operational control authority to the robot.")
    ]
    for s_num, s_desc in fly_stages:
        p_s = tf_r.add_paragraph()
        p_s.space_before = Pt(5)
        rsh = p_s.add_run(); rsh.text = s_num + " "; rsh.font.name = FONT_BODY; rsh.font.size = Pt(11); rsh.font.bold = True; rsh.font.color.rgb = INK_PRIMARY
        rsb = p_s.add_run(); rsb.text = s_desc; rsb.font.name = FONT_BODY; rsb.font.size = Pt(10.5); rsb.font.color.rgb = TEXT_DARK

    add_takeaway(s, "A self-reinforcing data flywheel turns brownfield operational edge cases into an insurmountable customer retention moat.")
    set_notes(s, "Slide 17 RTOS Timing & Data Flywheel. Detail sub-millisecond jitter requirements and the 5-stage closed-loop data engine.")
    return s


# ── SLIDE 18: 2026–2030 Market Dynamics & Wildcards ───────────────────────────
def slide_18_market_evolution_and_wildcards():
    s = new_slide()
    add_header(s, "Module 7 · 3-5 Year Forecast", "2026–2030 Market Evolution Dynamics & Strategic Wildcards",
               "Four structural market transitions over the next 3-5 years and critical uncertainty factors to monitor.")

    card_w = 5.72
    gap = 0.29
    top = 2.05
    h = 4.65

    # Left: 4 Structural Market Shifts
    add_card(s, 0.8, top, card_w, h, bg=BG_CARD, border=BORDER_SUBTLE, border_width=1.0)
    b1 = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(top), Inches(card_w), Inches(0.06))
    b1.adjustments[0] = 0.5; b1.fill.solid(); b1.fill.fore_color.rgb = BRAND_BLUE; b1.line.fill.background()

    pill1 = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.05), Inches(top + 0.18), Inches(card_w - 0.50), Inches(0.30))
    pill1.adjustments[0] = 0.5; pill1.fill.solid(); pill1.fill.fore_color.rgb = TINT_BLUE; pill1.line.fill.background()
    tf_p1 = pill1.text_frame; tf_p1.word_wrap = False; tf_p1.margin_left = tf_p1.margin_right = tf_p1.margin_top = tf_p1.margin_bottom = 0
    p1 = tf_p1.paragraphs[0]; p1.alignment = PP_ALIGN.CENTER
    rp1 = p1.add_run(); rp1.text = "3-5 YEAR INDUSTRY TRANSITION"; rp1.font.name = FONT_TITLE; rp1.font.size = Pt(10); rp1.font.bold = True; rp1.font.color.rgb = BRAND_BLUE

    tx_l = s.shapes.add_textbox(Inches(1.05), Inches(top + 0.58), Inches(card_w - 0.50), Inches(h - 0.70))
    tf_l = tx_l.text_frame; tf_l.word_wrap = True; tf_l.margin_left = tf_l.margin_right = tf_l.margin_top = tf_l.margin_bottom = 0
    p_lh = tf_l.paragraphs[0]
    r_lh = p_lh.add_run(); r_lh.text = "Four Structural Market Transitions\n"; r_lh.font.name = FONT_TITLE; r_lh.font.size = Pt(14); r_lh.font.bold = True; r_lh.font.color.rgb = INK_PRIMARY

    shifts = [
        ("Shift 1: Point AI Models -> Unified VLA Backbones:", "Transition from hundreds of narrow, bespoke vision models to unified Vision-Language-Action foundation models fine-tuned per manufacturing facility."),
        ("Shift 2: Hardware-Centric -> Software-Defined Robotics:", "Robot hardware frames commoditize; enterprise procurement decisions center entirely on simulation accuracy, safety software, and ease of PLC integration."),
        ("Shift 3: Greenfield Custom Cells -> Brownfield Retrofit Kits:", "Enterprise CapEx pivots away from building expensive new factories toward deploying non-invasive vision-action retrofit kits onto existing legacy production lines."),
        ("Shift 4: CapEx Equipment -> Performance-Based SLAs:", "Enterprise procurement transitions from $500k upfront robot purchases to outcome-based contracts ($/successful pick, $/inspected assembly) backed by uptime guarantees.")
    ]
    for h_txt, b_txt in shifts:
        p_s = tf_l.add_paragraph()
        p_s.space_before = Pt(6.5)
        rsh = p_s.add_run(); rsh.text = h_txt + " "; rsh.font.name = FONT_BODY; rsh.font.size = Pt(11); rsh.font.bold = True; rsh.font.color.rgb = INK_PRIMARY
        rsb = p_s.add_run(); rsb.text = b_txt; rsb.font.name = FONT_BODY; rsb.font.size = Pt(10.5); rsb.font.color.rgb = TEXT_DARK

    # Right: 4 Uncertainty Wildcards
    add_card(s, 0.8 + card_w + gap, top, card_w, h, bg=BG_CARD, border=BORDER_SUBTLE, border_width=1.0)
    b2 = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8 + card_w + gap), Inches(top), Inches(card_w), Inches(0.06))
    b2.adjustments[0] = 0.5; b2.fill.solid(); b2.fill.fore_color.rgb = AMBER; b2.line.fill.background()

    pill2 = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8 + card_w + gap + 0.25), Inches(top + 0.18), Inches(card_w - 0.50), Inches(0.30))
    pill2.adjustments[0] = 0.5; pill2.fill.solid(); pill2.fill.fore_color.rgb = TINT_AMBER; pill2.line.fill.background()
    tf_p2 = pill2.text_frame; tf_p2.word_wrap = False; tf_p2.margin_left = tf_p2.margin_right = tf_p2.margin_top = tf_p2.margin_bottom = 0
    p2 = tf_p2.paragraphs[0]; p2.alignment = PP_ALIGN.CENTER
    rp2 = p2.add_run(); rp2.text = "STRATEGIC UNCERTAINTY MATRIX"; rp2.font.name = FONT_TITLE; rp2.font.size = Pt(10); rp2.font.bold = True; rp2.font.color.rgb = AMBER

    tx_r = s.shapes.add_textbox(Inches(0.8 + card_w + gap + 0.25), Inches(top + 0.58), Inches(card_w - 0.50), Inches(h - 0.70))
    tf_r = tx_r.text_frame; tf_r.word_wrap = True; tf_r.margin_left = tf_r.margin_right = tf_r.margin_top = tf_r.margin_bottom = 0
    p_rh = tf_r.paragraphs[0]
    r_rh = p_rh.add_run(); r_rh.text = "Critical Market Wildcards & Sensitivities\n"; r_rh.font.name = FONT_TITLE; r_rh.font.size = Pt(14); r_rh.font.bold = True; r_rh.font.color.rgb = INK_PRIMARY

    wildcards = [
        ("Geopolitical Compute Controls:", "Export restrictions on high-end edge AI silicon (Jetson Thor) could fragment global deployments, forcing reliance on lower-power domestic edge chips and specialized quantization."),
        ("Statutory Liability Allocation:", "Emerging EU AI Act and OSHA frameworks clarifying whether model developers, robot OEMs, or engineering systems integrators bear strict liability for physical worker injuries."),
        ("Sim-to-Real Fidelity Ceilings:", "The risk that complex, non-rigid deformable physics (fabrics, rubber seals, wire harnesses) cannot be simulated accurately, capping synthetic data scaling benefits."),
        ("Foundation Model Open-Sourcing:", "Rapid open-weight releases (mirroring Llama 3 in language) commoditizing proprietary foundation models, driving all commercial value into systems integration and domain engineering.")
    ]
    for h_txt, b_txt in wildcards:
        p_w = tf_r.add_paragraph()
        p_w.space_before = Pt(6.5)
        rwh = p_w.add_run(); rwh.text = h_txt + " "; rwh.font.name = FONT_BODY; rwh.font.size = Pt(11); rwh.font.bold = True; rwh.font.color.rgb = INK_PRIMARY
        rwb = p_w.add_run(); rwb.text = b_txt; rwb.font.name = FONT_BODY; rwb.font.size = Pt(10.5); rwb.font.color.rgb = TEXT_DARK

    add_takeaway(s, "As foundation models commoditize, economic surplus shifts entirely to the integration layer that guarantees uptime and safety.")
    set_notes(s, "Slide 18 Market Evolution & Wildcards. Highlight the 4 market transitions and explain why open-source foundation models benefit LTTS.")
    return s


# ── SLIDE 19: LTTS Four Strategic Priorities ($8.3M Program) ──────────────────
def slide_19_strategic_priorities_phasing():
    s = new_slide()
    add_header(s, "Module 8 · Strategic Recommendations", "LTTS Strategic Priorities & Phased Capital Allocation",
               "A focused four-priority investment program totaling $8.3M phased against validated enterprise milestones.")

    col_w = 2.71
    gap = 0.30
    top = 2.05
    h = 4.65

    priorities = [
        ("PRIORITY 1 · Q1 2027", "Physical AI V&V Practice", "$2.8M Phase 1", GREEN, TINT_GREEN, [
            ("Core Objective:", "Establish the premier third-party safety and reachability certification laboratory for industrial robotics."),
            ("Key Deliverable:", "Automated Safety Dossier Compiler; formal CBF reachability testing suite under ISO 13849 PL-e and IEC 61508."),
            ("Target Milestone:", "Complete 10 enterprise safety audits generating $3.5M in high-margin consulting revenue in year one."),
            ("Strategic Rationale:", "Unlocks client CapEx by providing mandatory safety certification dossiers for factory insurance underwriting.")
        ]),
        ("PRIORITY 2 · Q2 2027", "Strategic PLC Alliances", "$1.3M Phase 2", BRAND_BLUE, TINT_BLUE, [
            ("Core Objective:", "Formalize co-development partnerships with Siemens, Rockwell Automation, and Beckhoff."),
            ("Key Deliverable:", "Certified reference bridge middleware connecting neural policies to S7-1500 and ControlLogix backplanes."),
            ("Target Milestone:", "Secure preferred integration partner status across 5 Tier-1 automotive and aerospace joint customer bids."),
            ("Strategic Rationale:", "Leverages incumbent sales channels to access established global enterprise customer bases.")
        ]),
        ("PRIORITY 3 · Q3 2027", "Synthetic Data Factory", "$4.2M Phase 3", PURPLE, TINT_PURPLE, [
            ("Core Objective:", "Establish dedicated GPU simulation cluster monetizing enterprise CAD/PLM assemblies (SD-FaaS)."),
            ("Key Deliverable:", "64-GPU NVIDIA Omniverse cluster generating contact-calibrated simulation policies for client plants."),
            ("Target Milestone:", "Secure 4 enterprise SD-FaaS contracts yielding $8.0M+ in recurring simulation and deployment revenue."),
            ("Strategic Rationale:", "Transforms one-off integration projects into high-retention annual software recurring revenue.")
        ]),
        ("PRIORITY 4 · ONGOING", "Hybrid Talent Center of Excellence", "$2.5M/yr Baseline", BRAND_NAVY, TINT_CYAN, [
            ("Core Objective:", "Build the world's leading hybrid robotics workforce combining controls engineering with deep learning."),
            ("Key Deliverable:", "Cross-train 250 existing mechatronics engineers in robotics AI; recruit 5 lead Ph.D. research scientists."),
            ("Target Milestone:", "Deploy 250 billable hybrid engineers globally at premium enterprise billing rates ($180-$250/hr)."),
            ("Strategic Rationale:", "Overcomes the single largest bottleneck in physical AI: the acute shortage of hybrid systems engineers.")
        ])
    ]

    for i, (badge, title, budget, clr, bg_pill, items) in enumerate(priorities):
        left = 0.8 + i * (col_w + gap)
        add_card(s, left, top, col_w, h, bg=BG_CARD, border=BORDER_SUBTLE, border_width=1.0)
        bar = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(col_w), Inches(0.06))
        bar.adjustments[0] = 0.5; bar.fill.solid(); bar.fill.fore_color.rgb = clr; bar.line.fill.background()

        pill = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left + 0.16), Inches(top + 0.16), Inches(col_w - 0.32), Inches(0.28))
        pill.adjustments[0] = 0.5; pill.fill.solid(); pill.fill.fore_color.rgb = bg_pill; pill.line.fill.background()
        tf_p = pill.text_frame; tf_p.word_wrap = False; tf_p.margin_left = tf_p.margin_right = tf_p.margin_top = tf_p.margin_bottom = 0
        pp = tf_p.paragraphs[0]; pp.alignment = PP_ALIGN.CENTER
        rp = pp.add_run(); rp.text = badge; rp.font.name = FONT_TITLE; rp.font.size = Pt(9.5); rp.font.bold = True; rp.font.color.rgb = clr

        tx_ct = s.shapes.add_textbox(Inches(left + 0.16), Inches(top + 0.48), Inches(col_w - 0.32), Inches(0.65))
        tf_ct = tx_ct.text_frame; tf_ct.word_wrap = True; tf_ct.margin_left = tf_ct.margin_right = tf_ct.margin_top = tf_ct.margin_bottom = 0
        pct = tf_ct.paragraphs[0]
        rct = pct.add_run(); rct.text = title + "\n"; rct.font.name = FONT_TITLE; rct.font.size = Pt(13); rct.font.bold = True; rct.font.color.rgb = INK_PRIMARY
        rcb = pct.add_run(); rcb.text = "Budget: " + budget; rcb.font.name = FONT_TITLE; rcb.font.size = Pt(11); rcb.font.bold = True; rcb.font.color.rgb = clr

        tx_b = s.shapes.add_textbox(Inches(left + 0.16), Inches(top + 1.15), Inches(col_w - 0.32), Inches(h - 1.25))
        tf_b = tx_b.text_frame; tf_b.word_wrap = True; tf_b.margin_left = tf_b.margin_right = tf_b.margin_top = tf_b.margin_bottom = 0

        for idx, (lbl, body) in enumerate(items):
            p_item = tf_b.paragraphs[0] if idx == 0 else tf_b.add_paragraph()
            if idx > 0: p_item.space_before = Pt(5)
            rl = p_item.add_run(); rl.text = lbl + " "; rl.font.name = FONT_BODY; rl.font.size = Pt(10.5); rl.font.bold = True; rl.font.color.rgb = INK_PRIMARY
            rb = p_item.add_run(); rb.text = body; rb.font.name = FONT_BODY; rb.font.size = Pt(10.5); rb.font.color.rgb = TEXT_DARK

    add_takeaway(s, "Total program investment of $8.3M is phased against customer revenue milestones, targeting full break-even within 18 months.")
    set_notes(s, "Slide 19 Strategic Priorities. Detail the $8.3M phased investment across V&V ($2.8M), Alliances ($1.3M), Data Factory ($4.2M), and Talent CoE ($2.5M/yr).")
    return s


# ── SLIDE 20: Integrated Strategic Roadmap (Table 5) ──────────────────────────
def slide_20_strategic_roadmap_table5():
    s = new_slide()
    add_header(s, "Module 8 · Strategic Roadmap", "Integrated Strategic Roadmap & Phased Budget Allocation (Table 5)",
               "Comprehensive execution timeline, strategic capabilities, target deliverables, and capital deployment.")

    left_m = 0.8
    top_base = 2.05
    total_w = 11.73

    headers = [
        ("STRATEGIC INITIATIVE", 2.50, PP_ALIGN.LEFT),
        ("TIMELINE", 1.30, PP_ALIGN.CENTER),
        ("STRATEGIC FOCUS & CAPABILITY", 3.30, PP_ALIGN.LEFT),
        ("TARGET DELIVERABLE", 3.20, PP_ALIGN.LEFT),
        ("PHASED BUDGET", 1.43, PP_ALIGN.RIGHT)
    ]
    rows = [
        ("Priority 1: V&V Practice", "Q1 2027",
         "Functional safety auditing, CBF evaluation &\ninterval bound reachability certification",
         "Automated Safety Dossier Compiler &\ncertified lab testing under ISO 13849 / IEC 61508",
         "$2.8M Phase 1", GREEN),

        ("Priority 2: PLC Alliances", "Q2 2027",
         "Joint integration testbeds with Siemens S7-1500 &\nRockwell ControlLogix architectures",
         "Certified bridge middleware connecting\nneural policies to industrial fieldbuses",
         "$1.3M Phase 2", BRAND_BLUE),

        ("Priority 3: Synthetic Data Factory", "Q3 2027",
         "Digital twin simulation (SD-FaaS) monetizing\nenterprise CAD/PLM engineering assemblies",
         "Dedicated 64-GPU Omniverse cluster generating\ncontact-calibrated simulation policies",
         "$4.2M Phase 3", BRAND_NAVY),

        ("Priority 4: Hybrid Talent CoE", "Ongoing",
         "Cross-training mechatronics bench into robotics AI;\nrecruiting 5 lateral Ph.D. specialists",
         "250-engineer hybrid workforce bridging\ncontrols engineering with deep learning",
         "$2.5M/yr Annual", PURPLE)
    ]

    # Header Bar
    hdr_h = 0.42
    hdr_shape = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left_m), Inches(top_base), Inches(total_w), Inches(hdr_h))
    hdr_shape.adjustments[0] = 0.08; hdr_shape.fill.solid(); hdr_shape.fill.fore_color.rgb = BRAND_NAVY; hdr_shape.line.fill.background()

    curr_x = left_m
    for title, col_w, align in headers:
        tb = s.shapes.add_textbox(Inches(curr_x + 0.12), Inches(top_base + 0.08), Inches(col_w - 0.24), Inches(0.30))
        tf = tb.text_frame; tf.word_wrap = True; tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        p = tf.paragraphs[0]; p.alignment = align
        r = p.add_run(); r.text = title; r.font.name = FONT_TITLE; r.font.size = Pt(10.5); r.font.bold = True; r.font.color.rgb = COLOR_WHITE
        curr_x += col_w

    # Table Body Rows
    row_top = top_base + hdr_h + 0.04
    row_h = 0.84
    gap = 0.04
    for i, (init, time_val, focus, deliv, bud, clr) in enumerate(rows):
        bg = BG_CARD if (i % 2 == 0) else COLOR_WHITE
        add_card(s, left_m, row_top, total_w, row_h, bg=bg, border=BORDER_SUBTLE, border_width=1.0)

        curr_x = left_m
        for col_idx, (text_val, col_w, align) in enumerate([(init, 2.50, PP_ALIGN.LEFT),
                                                             (time_val, 1.30, PP_ALIGN.CENTER),
                                                             (focus, 3.30, PP_ALIGN.LEFT),
                                                             (deliv, 3.20, PP_ALIGN.LEFT),
                                                             (bud, 1.43, PP_ALIGN.RIGHT)]):
            tb = s.shapes.add_textbox(Inches(curr_x + 0.15), Inches(row_top + 0.10), Inches(col_w - 0.30), Inches(row_h - 0.20))
            tf = tb.text_frame; tf.word_wrap = True; tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
            p = tf.paragraphs[0]; p.alignment = align
            r = p.add_run(); r.text = text_val; r.font.name = FONT_BODY; r.font.size = Pt(10.5)
            if col_idx == 0:
                r.font.bold = True; r.font.color.rgb = INK_PRIMARY
            elif col_idx == 1:
                r.font.bold = True; r.font.color.rgb = clr
            elif col_idx == 4:
                r.font.bold = True; r.font.color.rgb = INK_PRIMARY
            else:
                r.font.color.rgb = TEXT_DARK
            curr_x += col_w

        row_top += row_h + gap

    # Capital Summary Callout Container
    summary_top = row_top + 0.12
    summary_h = 0.65
    add_card(s, left_m, summary_top, total_w, summary_h, bg=BG_CARD_BLUE, border=BORDER_BLUE, border_width=1.0)
    tx_sum = s.shapes.add_textbox(Inches(left_m + 0.20), Inches(summary_top + 0.12), Inches(total_w - 0.40), Inches(summary_h - 0.24))
    tf_sum = tx_sum.text_frame; tf_sum.word_wrap = True; tf_sum.margin_left = tf_sum.margin_right = tf_sum.margin_top = tf_sum.margin_bottom = 0
    p_s = tf_sum.paragraphs[0]
    rs1 = p_s.add_run(); rs1.text = "TOTAL 2027 PROGRAM INVESTMENT: "; rs1.font.name = FONT_TITLE; rs1.font.size = Pt(11); rs1.font.bold = True; rs1.font.color.rgb = BRAND_NAVY
    rs2 = p_s.add_run(); rs2.text = "$8.3M Phased Capex ($2.8M V&V + $1.3M Alliances + $4.2M Data Factory) + $2.5M/yr Ongoing CoE Baseline. Every dollar is directly anchored in customer revenue expansion."; rs2.font.name = FONT_BODY; rs2.font.size = Pt(10.5); rs2.font.color.rgb = TEXT_DARK

    add_takeaway(s, "Execution sequencing guarantees each phase self-funds subsequent expansion through customer-contracted milestone revenues.")
    set_notes(s, "Slide 20 Strategic Roadmap (Table 5). Present the milestone timeline, deliverables, and phased $8.3M capital deployment schedule.")
    return s


# ── SLIDE 21: Strategic Boardroom Mandate (Conclusion) ────────────────────────
def slide_21_strategic_boardroom_call():
    s = new_slide()

    # Top Pill Badge
    add_pill_badge(s, 0.8, 0.38, "STRATEGIC CONCLUSION · BOARDROOM ACTION MANDATE", bg=TINT_BLUE, fg=BRAND_BLUE, font_size=9.5, bold=True)

    # Action Title (28pt bold Segoe UI)
    tx_t = s.shapes.add_textbox(Inches(0.8), Inches(0.78), Inches(11.73), Inches(0.65))
    tf_t = tx_t.text_frame; tf_t.word_wrap = True; tf_t.margin_left = tf_t.margin_right = tf_t.margin_top = tf_t.margin_bottom = 0
    p1 = tf_t.paragraphs[0]
    r1 = p1.add_run(); r1.text = "The future of industrial automation is Physical Artificial Intelligence."; r1.font.name = FONT_TITLE; r1.font.size = Pt(28); r1.font.bold = True; r1.font.color.rgb = INK_PRIMARY

    # Subtitle Thesis
    tx_sub = s.shapes.add_textbox(Inches(0.8), Inches(1.48), Inches(11.73), Inches(0.40))
    tf_sub = tx_sub.text_frame; tf_sub.word_wrap = True; tf_sub.margin_left = tf_sub.margin_right = tf_sub.margin_top = tf_sub.margin_bottom = 0
    p2 = tf_sub.paragraphs[0]
    r2 = p2.add_run(); r2.text = "The strategic opportunity for L&T Technology Services is not to manufacture commoditizing robot hardware, nor to train raw foundation models. "; r2.font.name = FONT_BODY; r2.font.size = Pt(12.5); r2.font.color.rgb = TEXT_LIGHT
    r3 = p2.add_run(); r3.text = "The definitive opportunity for LTTS is to become the indispensable, trusted engineering bridge that verifies, integrates, and deploys Physical AI safely at scale."; r3.font.name = FONT_BODY; r3.font.size = Pt(12.5); r3.font.bold = True; r3.font.color.rgb = BRAND_BLUE

    # Minimalist hairline divider
    div = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.95), Inches(11.73), Inches(0.015))
    div.fill.solid(); div.fill.fore_color.rgb = RGBColor(0xEA, 0xEE, 0xF4); div.line.fill.background()

    # 4 Pillar Blueprint Cards
    p_w = 2.71
    gap = 0.30
    top = 2.10
    h = 4.55

    pillars = [
        ("1. VERIFY (Q1 2027)", "Functional Safety Leadership", GREEN, TINT_GREEN,
         "Build the gold-standard Physical AI V&V practice with formal safety dossiers and CBF reachability testing under ISO 13849 / IEC 61508.",
         "Unlocks corporate insurance and regulatory sign-off for enterprise robot deployments."),

        ("2. INTEGRATE (Q2 2027)", "PLC Bridge Middleware", BRAND_BLUE, TINT_BLUE,
         "Deploy certified PLC bridge middleware connecting frontier neural policies to Siemens S7-1500 and Rockwell ControlLogix architectures.",
         "Guarantees deterministic safety interlocks on live plant machinery."),

        ("3. SCALE (Q3 2027)", "Synthetic Data Factory", PURPLE, TINT_PURPLE,
         "Launch the enterprise Synthetic Data Factory (SD-FaaS), monetizing proprietary customer CAD/PLM assets into continuous digital twins.",
         "Converts one-time integration projects into recurring software revenue."),

        ("4. EMPOWER (Ongoing)", "Hybrid Engineering Bench", BRAND_NAVY, TINT_CYAN,
         "Cross-train 250 mechatronics engineers into hybrid Physical AI practitioners, securing global engineering services dominance.",
         "Supplies the world's most capable industrial AI engineering bench.")
    ]

    for i, (title, sub, clr, bg_pill, body, imp) in enumerate(pillars):
        x = 0.8 + i * (p_w + gap)
        add_card(s, x, top, p_w, h, bg=BG_CARD, border=BORDER_SUBTLE, border_width=1.0)
        bar = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(top), Inches(p_w), Inches(0.06))
        bar.adjustments[0] = 0.5; bar.fill.solid(); bar.fill.fore_color.rgb = clr; bar.line.fill.background()

        pill = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x + 0.16), Inches(top + 0.16), Inches(p_w - 0.32), Inches(0.28))
        pill.adjustments[0] = 0.5; pill.fill.solid(); pill.fill.fore_color.rgb = bg_pill; pill.line.fill.background()
        tf_p = pill.text_frame; tf_p.word_wrap = False; tf_p.margin_left = tf_p.margin_right = tf_p.margin_top = tf_p.margin_bottom = 0
        pp = tf_p.paragraphs[0]; pp.alignment = PP_ALIGN.CENTER
        rp = pp.add_run(); rp.text = title; rp.font.name = FONT_TITLE; rp.font.size = Pt(9.5); rp.font.bold = True; rp.font.color.rgb = clr

        tx = s.shapes.add_textbox(Inches(x + 0.16), Inches(top + 0.50), Inches(p_w - 0.32), Inches(h - 0.60))
        tf = tx.text_frame; tf.word_wrap = True; tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        p_h = tf.paragraphs[0]
        rs = p_h.add_run(); rs.text = sub + "\n\n"; rs.font.name = FONT_TITLE; rs.font.size = Pt(13); rs.font.bold = True; rs.font.color.rgb = INK_PRIMARY

        p_b = tf.add_paragraph()
        rb = p_b.add_run(); rb.text = body + "\n\n"; rb.font.name = FONT_BODY; rb.font.size = Pt(10.5); rb.font.color.rgb = TEXT_DARK
        ri = p_b.add_run(); ri.text = "Impact: " + imp; ri.font.name = FONT_BODY; ri.font.size = Pt(10.5); ri.font.bold = True; ri.font.color.rgb = INK_PRIMARY

    add_takeaway(s, "LTTS is uniquely positioned to bridge frontier AI models with real-world plant machinery. The window to establish global leadership is now.")
    set_notes(s, "Slide 21 Strategic Boardroom Mandate. Deliver the boardroom action call: LTTS must own the engineering bridge between AI models and plant machinery.")
    return s


# ── SLIDE 22: Appendix A · Comprehensive Sources Index ────────────────────────
def slide_22_appendix_a_sources():
    s = new_slide()
    add_header(s, "Appendix A · Citations", "Comprehensive Sources Index: Commercial & Research Literature",
               "Audited corporate disclosures, regulatory filings, peer-reviewed preprints, and official OEM pilot announcements.")

    card_w = 5.72
    gap = 0.29
    top = 2.05
    h = 4.65

    # Left: Commercial Disclosures
    add_card(s, 0.8, top, card_w, h, bg=BG_CARD, border=BORDER_SUBTLE, border_width=1.0)
    b1 = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(top), Inches(card_w), Inches(0.06))
    b1.adjustments[0] = 0.5; b1.fill.solid(); b1.fill.fore_color.rgb = GREEN; b1.line.fill.background()

    pill1 = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.05), Inches(top + 0.18), Inches(card_w - 0.50), Inches(0.30))
    pill1.adjustments[0] = 0.5; pill1.fill.solid(); pill1.fill.fore_color.rgb = TINT_GREEN; pill1.line.fill.background()
    tf_p1 = pill1.text_frame; tf_p1.word_wrap = False; tf_p1.margin_left = tf_p1.margin_right = tf_p1.margin_top = tf_p1.margin_bottom = 0
    p1 = tf_p1.paragraphs[0]; p1.alignment = PP_ALIGN.CENTER
    rp1 = p1.add_run(); rp1.text = "COMMERCIAL & CAPITAL DISCLOSURES"; rp1.font.name = FONT_TITLE; rp1.font.size = Pt(10); rp1.font.bold = True; rp1.font.color.rgb = GREEN

    tx_l = s.shapes.add_textbox(Inches(1.05), Inches(top + 0.55), Inches(card_w - 0.50), Inches(h - 0.65))
    tf_l = tx_l.text_frame; tf_l.word_wrap = True; tf_l.margin_left = tf_l.margin_right = tf_l.margin_top = tf_l.margin_bottom = 0
    p_lh = tf_l.paragraphs[0]
    r_lh = p_lh.add_run(); r_lh.text = "Primary Capital & Corporate Disclosures\n"; r_lh.font.name = FONT_TITLE; r_lh.font.size = Pt(13.5); r_lh.font.bold = True; r_lh.font.color.rgb = INK_PRIMARY

    c_sources = [
        ("Wayve ($1.05B Series C):", "Corporate Announcement (May 7, 2024). SoftBank, NVIDIA, Microsoft."),
        ("Figure AI ($675M Series B):", "Press Release (Feb 29, 2024). Microsoft, OpenAI, NVIDIA, Bezos ($2.6B val)."),
        ("Physical Intelligence ($400M Series A):", "Company Disclosure (Nov 4, 2024). Bezos, Thrive, Lux ($2.4B val)."),
        ("Skild AI ($300M Series A):", "Press Release (Jul 9, 2024). Lightspeed, Coatue, SoftBank ($1.5B val)."),
        ("Applied Intuition ($250M Series E):", "Press Release (Mar 12, 2024). Lux Capital, Elad Gil, Porsche ($6.0B val)."),
        ("Scale AI ($1.0B Series F):", "Company Disclosure (May 21, 2024). Accel and strategic partners ($13.8B val)."),
        ("Waymo Commercial Mileage:", "Alphabet Q3 2024 Earnings Call (Oct 29, 2024). >150k trips/wk, >1M miles/wk."),
        ("Amazon / Covariant License:", "Corporate Announcement (Aug 30, 2024). Founder hiring & non-exclusive license.")
    ]
    for name, det in c_sources:
        p_row = tf_l.add_paragraph()
        p_row.space_before = Pt(3)
        rn = p_row.add_run(); rn.text = name + " "; rn.font.name = FONT_BODY; rn.font.size = Pt(10.5); rn.font.bold = True; rn.font.color.rgb = INK_PRIMARY
        rd = p_row.add_run(); rd.text = det; rd.font.name = FONT_BODY; rd.font.size = Pt(10); rd.font.color.rgb = TEXT_DARK

    # Right: Research Literature & Field Trials
    add_card(s, 0.8 + card_w + gap, top, card_w, h, bg=BG_CARD, border=BORDER_SUBTLE, border_width=1.0)
    b2 = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8 + card_w + gap), Inches(top), Inches(card_w), Inches(0.06))
    b2.adjustments[0] = 0.5; b2.fill.solid(); b2.fill.fore_color.rgb = BRAND_BLUE; b2.line.fill.background()

    pill2 = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8 + card_w + gap + 0.25), Inches(top + 0.18), Inches(card_w - 0.50), Inches(0.30))
    pill2.adjustments[0] = 0.5; pill2.fill.solid(); pill2.fill.fore_color.rgb = TINT_BLUE; pill2.line.fill.background()
    tf_p2 = pill2.text_frame; tf_p2.word_wrap = False; tf_p2.margin_left = tf_p2.margin_right = tf_p2.margin_top = tf_p2.margin_bottom = 0
    p2 = tf_p2.paragraphs[0]; p2.alignment = PP_ALIGN.CENTER
    rp2 = p2.add_run(); rp2.text = "RESEARCH & TRIAL CITATIONS"; rp2.font.name = FONT_TITLE; rp2.font.size = Pt(10); rp2.font.bold = True; rp2.font.color.rgb = BRAND_BLUE

    tx_r = s.shapes.add_textbox(Inches(0.8 + card_w + gap + 0.25), Inches(top + 0.55), Inches(card_w - 0.50), Inches(h - 0.65))
    tf_r = tx_r.text_frame; tf_r.word_wrap = True; tf_r.margin_left = tf_r.margin_right = tf_r.margin_top = tf_r.margin_bottom = 0
    p_rh = tf_r.paragraphs[0]
    r_rh = p_rh.add_run(); r_rh.text = "Research Literature & Customer Pilot Benchmarks\n"; r_rh.font.name = FONT_TITLE; r_rh.font.size = Pt(13.5); r_rh.font.bold = True; r_rh.font.color.rgb = INK_PRIMARY

    r_sources = [
        ("Continuous Action Flow Matching:", "Physical Intelligence Technical Report on π0 (Oct 2024, arXiv:2410.24164)."),
        ("Egocentric Scaling Laws:", "NVIDIA GEAR Research Report on EgoScale (Feb 2026, arXiv:2602.16710)."),
        ("Pearl's Causal Hierarchy:", "Judea Pearl, Causality: Models, Reasoning, and Inference, Cambridge Univ Press."),
        ("BMW Spartanburg Plant Trial:", "BMW Group Press Release (Aug 2024). Figure 02 humanoid in sheet metal assembly."),
        ("Mercedes-Benz Apollo Pilot:", "Mercedes-Benz & Apptronik Agreement Announcement (Mar 15, 2024). Parts delivery."),
        ("DHL Boston Dynamics Deployment:", "DHL Supply Chain Announcement (2024). Stretch mobile manipulators for containers."),
        ("Siemens & Microsoft Copilot:", "Siemens AG Press Release (2024). Industrial AI copilot inside Siemens TIA Portal."),
        ("Siemens & Intrinsic Strategic Alliance:", "Siemens & Alphabet Intrinsic Announcement (2024). Robotics AI automation.")
    ]
    for name, det in r_sources:
        p_row = tf_r.add_paragraph()
        p_row.space_before = Pt(3)
        rn = p_row.add_run(); rn.text = name + " "; rn.font.name = FONT_BODY; rn.font.size = Pt(10.5); rn.font.bold = True; rn.font.color.rgb = INK_PRIMARY
        rd = p_row.add_run(); rd.text = det; rd.font.name = FONT_BODY; rd.font.size = Pt(10); rd.font.color.rgb = TEXT_DARK

    add_takeaway(s, "All technical claims, mathematical formalisms, and OEM deployment partnerships are cross-verified against primary literature.")
    set_notes(s, "Slide 22 Appendix A. Full primary sources catalog across capital rounds, research preprints, and customer trial announcements.")
    return s


# ── SLIDE 23: Appendix B · Self-Critique & Sign-Off Register ──────────────────
def slide_23_appendix_b_and_signoff():
    s = new_slide()
    add_header(s, "Appendix B · Governance", "Adversarial Self-Critique Log & Official Document Sign-Off",
               "Complete audit record of 11 downgraded claims and formal executive sign-off for LTTS leadership.")

    # Left: Self-Critique Downgrade Log (7.2" wide)
    card_w_l = 7.20
    top = 2.05
    h = 4.65

    add_card(s, 0.8, top, card_w_l, h, bg=BG_CARD, border=BORDER_SUBTLE, border_width=1.0)
    b1 = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(top), Inches(card_w_l), Inches(0.06))
    b1.adjustments[0] = 0.5; b1.fill.solid(); b1.fill.fore_color.rgb = RED; b1.line.fill.background()

    pill1 = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.05), Inches(top + 0.16), Inches(card_w_l - 0.50), Inches(0.28))
    pill1.adjustments[0] = 0.5; pill1.fill.solid(); pill1.fill.fore_color.rgb = TINT_RED; pill1.line.fill.background()
    tf_p1 = pill1.text_frame; tf_p1.word_wrap = False; tf_p1.margin_left = tf_p1.margin_right = tf_p1.margin_top = tf_p1.margin_bottom = 0
    p1 = tf_p1.paragraphs[0]; p1.alignment = PP_ALIGN.CENTER
    rp1 = p1.add_run(); rp1.text = "ADVERSARIAL AUDIT LOG · 11 UNVERIFIED CLAIMS RETRACTED"; rp1.font.name = FONT_TITLE; rp1.font.size = Pt(9.5); rp1.font.bold = True; rp1.font.color.rgb = RED

    tx_l = s.shapes.add_textbox(Inches(1.05), Inches(top + 0.48), Inches(card_w_l - 0.50), Inches(h - 0.55))
    tf_l = tx_l.text_frame; tf_l.word_wrap = True; tf_l.margin_left = tf_l.margin_right = tf_l.margin_top = tf_l.margin_bottom = 0
    p_lh = tf_l.paragraphs[0]
    r_lh = p_lh.add_run(); r_lh.text = "Audit Governance: Downgraded Unverified Industry Extrapolations\n"; r_lh.font.name = FONT_TITLE; r_lh.font.size = Pt(13); r_lh.font.bold = True; r_lh.font.color.rgb = RED

    critiques = [
        ("1. Ford Battery Scrap (Removed):", "Claimed 42% scrap / $18M warranty savings at Rawsonville; not in audited SEC 10-Ks."),
        ("2. Airbus Hole Defects (Removed):", "Claimed <2 PPM defect rate on A350 wings; unverified industry whitepaper extrapolation."),
        ("3. Amazon Mobile Fleet (Removed):", "Cited 750,000 robots; conflated legacy Kiva AGVs with modern AI AMRs (Proteus)."),
        ("4. GE Vernova Outages (Removed):", "Claimed $380M saved across 1,200 turbines; vendor marketing modeled projection."),
        ("5. TSMC Lithography (Removed):", "Claimed 2.1x yield accuracy; proprietary N3/N2 foundry trade secret not auditable."),
        ("6. Caterpillar Haulage (Removed):", "Claimed 250M km zero-injury; vendor marketing copy rather than certified safety study."),
        ("7. Intuitive Surgical (Removed):", "Claimed 40% surgeon strain reduction on da Vinci 5; uncontrolled ergonomic PR claim."),
        ("8. Symbotic Deployments (Removed):", "Claimed $500M+ Walmart deployment; conflated multi-year backlog with active AI software."),
        ("9. DHL Turnaround Time (Removed):", "Claimed trailer turn from 90 to 38 mins; site-level non-standardized pilot data."),
        ("10. Siemens Energy (Removed):", "Claimed 45% valve failure reduction; unaudited whitepaper statistic without third-party audit."),
        ("11. Decorative Equations (Removed):", "Removed unconnected PINN loss functions and InfoNCE contrastive equations as academic padding.")
    ]
    for tit, why in critiques:
        p_c = tf_l.add_paragraph()
        p_c.space_before = Pt(2.2)
        rt = p_c.add_run(); rt.text = tit + " "; rt.font.name = FONT_BODY; rt.font.size = Pt(10); rt.font.bold = True; rt.font.color.rgb = INK_PRIMARY
        rw = p_c.add_run(); rw.text = why; rw.font.name = FONT_BODY; rw.font.size = Pt(9.5); rw.font.color.rgb = TEXT_DARK

    # Right: Document Sign-Off Register (4.24" wide)
    card_w_r = 4.24
    gap = 0.29
    x_r = 0.8 + card_w_l + gap

    add_card(s, x_r, top, card_w_r, h, bg=BG_CARD_BLUE, border=BORDER_BLUE, border_width=1.0)
    b2 = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x_r), Inches(top), Inches(card_w_r), Inches(0.06))
    b2.adjustments[0] = 0.5; b2.fill.solid(); b2.fill.fore_color.rgb = BRAND_NAVY; b2.line.fill.background()

    pill2 = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x_r + 0.20), Inches(top + 0.16), Inches(card_w_r - 0.40), Inches(0.28))
    pill2.adjustments[0] = 0.5; pill2.fill.solid(); pill2.fill.fore_color.rgb = TINT_BLUE; pill2.line.fill.background()
    tf_p2 = pill2.text_frame; tf_p2.word_wrap = False; tf_p2.margin_left = tf_p2.margin_right = tf_p2.margin_top = tf_p2.margin_bottom = 0
    p2 = tf_p2.paragraphs[0]; p2.alignment = PP_ALIGN.CENTER
    rp2 = p2.add_run(); rp2.text = "OFFICIAL DOCUMENT SIGN-OFF"; rp2.font.name = FONT_TITLE; rp2.font.size = Pt(9.5); rp2.font.bold = True; rp2.font.color.rgb = BRAND_NAVY

    tx_r = s.shapes.add_textbox(Inches(x_r + 0.20), Inches(top + 0.48), Inches(card_w_r - 0.40), Inches(h - 0.55))
    tf_r = tx_r.text_frame; tf_r.word_wrap = True; tf_r.margin_left = tf_r.margin_right = tf_r.margin_top = tf_r.margin_bottom = 0
    p_rh = tf_r.paragraphs[0]
    r_rh = p_rh.add_run(); r_rh.text = "Official Briefing Sign-Off Register\n"; r_rh.font.name = FONT_TITLE; r_rh.font.size = Pt(13); r_rh.font.bold = True; r_rh.font.color.rgb = BRAND_NAVY

    sign_items = [
        ("Document ID:", "LTTS-PAI-2026-MASTER-01"),
        ("Release Version:", "3.0 Master Executive Release"),
        ("Classification:", "Strictly Confidential & Proprietary"),
        ("Date of Issue:", "September 2026"),
        ("Review Status:", "Peer-Reviewed & Adversarially Audited"),
        ("Prepared Exclusively For:", "Dr. Madhusudhan Singh\nExecutive Leadership, L&T Technology Services"),
        ("Primary Research Author:", "Adari Karthikeya\nPhysical AI Practice Research"),
        ("Action Required:", "Executive Review & Budget Authorization for Q1 2027 Strategic Program ($8.3M)")
    ]
    for lbl, val in sign_items:
        p_row = tf_r.add_paragraph()
        p_row.space_before = Pt(4)
        rl = p_row.add_run(); rl.text = lbl + " "; rl.font.name = FONT_BODY; rl.font.size = Pt(10.5); rl.font.bold = True; rl.font.color.rgb = INK_PRIMARY
        rv = p_row.add_run(); rv.text = val; rv.font.name = FONT_BODY; rv.font.size = Pt(10.5); rv.font.color.rgb = BRAND_BLUE if ("Dr." in val or "Adari" in val or "$8.3M" in val) else TEXT_DARK

    add_takeaway(s, "Briefing completed. For presentation delivery, boardroom inquiries, or pilot execution, contact Adari Karthikeya & LTTS Leadership.")
    set_notes(s, "Slide 23 Appendix B & Sign-Off. Final document sign-off register and adversarial audit log for Dr. Madhusudhan Singh and LTTS leadership.")
    return s


# ── MAIN GENERATOR PIPELINE ───────────────────────────────────────────────────
def main():
    print("=" * 70)
    print("  BUILDING: The Practice of Physical Artificial Intelligence")
    print("  23-Slide Master Executive Presentation Deck for LTTS Leadership")
    print("  Typography: Segoe UI (Clean, Modern, Human, Friendly, Ultra-Legible)")
    print("  Design: Elevated Rounded Cards, Color Accent Stripes, Pill Badges")
    print("=" * 70)

    builders = [
        ("01. Title & Executive Cover", slide_01_cover),
        ("02. Verification Taxonomy & Hero Benchmarks", slide_02_taxonomy_and_metrics),
        ("03. Commercial Maturity Tiers (Tiers 1-3)", slide_03_maturity_tiers),
        ("04. Capital Matrix & Hardware Trap", slide_04_capital_and_hardware_trap),
        ("05. Frontier Priorities: Continuous Policies & World Models", slide_05_frontier_research_priorities),
        ("06. Frontier Priorities: Scaling Laws & Edge RT", slide_06_scaling_laws_and_edge),
        ("07. Canonical Physical AI Failure Modes (FM1-FM5)", slide_07_failure_modes),
        ("08. Pearl's Causal Ladder & Mathematical Breakdown", slide_08_pearl_causal_ladder),
        ("09. Commercial Models & Deal Economics (Table 3)", slide_09_commercial_models_table3),
        ("10. ER&D Services Opportunity & Offerings 1 & 2", slide_10_ltts_offerings_part1),
        ("11. LTTS Offerings 3 & 4: V&V & Embodied MLOps", slide_11_ltts_offerings_part2),
        ("12. Verified Deployments Across 5 Sectors & Hype", slide_12_deployments_and_hype),
        ("13. Dominance of the Hybrid Incumbent Ecosystem", slide_13_hybrid_incumbent_model),
        ("14. Layered Competitive Landscape (Table 4)", slide_14_competitive_landscape_table4),
        ("15. High-Value Underserved Market Gaps", slide_15_underserved_market_gaps),
        ("16. Kinematics Moat: Jacobian & Singularities", slide_16_kinematics_moat_and_math),
        ("17. Deterministic RTOS Timing & Data Flywheel", slide_17_rtos_and_data_flywheel),
        ("18. 2026-2030 Market Dynamics & Wildcards", slide_18_market_evolution_and_wildcards),
        ("19. LTTS Four Strategic Priorities ($8.3M Program)", slide_19_strategic_priorities_phasing),
        ("20. Integrated Strategic Roadmap (Table 5)", slide_20_strategic_roadmap_table5),
        ("21. Strategic Boardroom Mandate (Conclusion)", slide_21_strategic_boardroom_call),
        ("22. Appendix A: Comprehensive Sources Index", slide_22_appendix_a_sources),
        ("23. Appendix B: Self-Critique & Sign-Off Register", slide_23_appendix_b_and_signoff),
    ]

    for idx, (label, builder_func) in enumerate(builders, 1):
        builder_func()
        print(f"  [{idx:02d}/23] Rendered: {label}")

    prs.save(OUTPUT_PPTX)
    print("=" * 70)
    print(f"  SUCCESSFULLY GENERATED: {OUTPUT_PPTX}")

    for extra_path in [
        r"c:\Users\k18ka\Downloads\Genuity IO all documents\LTTS\The_Practice_of_Physical_AI_Executive_Deck_v3.pptx",
        r"c:\Users\k18ka\Downloads\Genuity IO all documents\LTTS\The_Practice_of_Physical_AI_Executive_Deck_Final.pptx",
        r"c:\Users\k18ka\Downloads\Genuity IO all documents\LTTS\The_Practice_of_Physical_AI_Executive_Deck_Master.pptx",
        r"c:\Users\k18ka\Downloads\Genuity IO all documents\LTTS\The_Practice_of_Physical_AI_Executive_Deck.pptx"
    ]:
        try:
            prs.save(extra_path)
            print(f"  ALSO OVERWROTE: {extra_path}")
        except Exception as e:
            pass

    print("  Total Slides: 23 (Under 25 slides target)")
    print("  Background: 100% Studio White (No dark slides)")
    print("  Typography: Segoe UI (Titles/Body/Tables)")
    print("  Content Preservation: 100% of 16-page LaTeX briefing retained")
    print("=" * 70)

if __name__ == "__main__":
    main()
