"""
Slides Part 1: Cover, Taxonomy, Executive Summary, and Agenda (Slides 1-4)
"""

from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

from deck_common import (
    new_slide, add_card, add_rect, add_header, add_takeaway, add_stat_box,
    add_badge, set_notes, BG_CANVAS, BG_CARD, BG_CARD_ALT, BG_CARD_ACCENT,
    BORDER_SUBTLE, BORDER_GOLD, BORDER_CYAN, BORDER_GREEN, BORDER_AMBER,
    BORDER_RED, GOLD, CYAN, GREEN, AMBER, RED, PURPLE, WHITE, COLOR_WHITE,
    BRAND_NAVY, BRAND_BLUE, INK_PRIMARY, TEXT_LIGHT, TEXT_MUTED, FONT_NAME
)

def slide_01_cover():
    s = new_slide(bg_color=BRAND_NAVY)
    
    # Left accent gold bar
    bar = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(0.15), Inches(7.5))
    bar.fill.solid(); bar.fill.fore_color.rgb = GOLD; bar.line.fill.background()

    # Top metadata chip
    add_badge(s, 0.8, 0.8, "CONFIDENTIAL  ·  EXECUTIVE STRATEGIC BRIEFING", bg=RGBColor(0x00, 0x1E, 0x33), fg=GOLD, font_size=9, bold=True)

    # Main Title Box
    tx_title = s.shapes.add_textbox(Inches(0.8), Inches(1.5), Inches(10.5), Inches(2.2))
    tf_t = tx_title.text_frame
    tf_t.word_wrap = True
    tf_t.margin_left = tf_t.margin_right = tf_t.margin_top = tf_t.margin_bottom = 0
    
    p0 = tf_t.paragraphs[0]
    r0 = p0.add_run()
    r0.text = "The Practice of\n"
    r0.font.name = FONT_NAME
    r0.font.size = Pt(22)
    r0.font.color.rgb = RGBColor(0x93, 0xC5, 0xFD)

    r1 = p0.add_run()
    r1.text = "Physical Artificial Intelligence"
    r1.font.name = FONT_NAME
    r1.font.size = Pt(46)
    r1.font.bold = True
    r1.font.color.rgb = COLOR_WHITE

    # Gold horizontal separator
    div = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(3.85), Inches(7.5), Inches(0.02))
    div.fill.solid(); div.fill.fore_color.rgb = GOLD; div.line.fill.background()

    # Subtitle
    tx_sub = s.shapes.add_textbox(Inches(0.8), Inches(4.05), Inches(11.0), Inches(0.8))
    tf_sub = tx_sub.text_frame
    tf_sub.word_wrap = True
    tf_sub.margin_left = tf_sub.margin_right = tf_sub.margin_top = tf_sub.margin_bottom = 0
    p_sub = tf_sub.paragraphs[0]
    r_sub = p_sub.add_run()
    r_sub.text = "Landscape, Commercialization, Competition, and the Industrial-AI Bridge"
    r_sub.font.name = FONT_NAME
    r_sub.font.size = Pt(16)
    r_sub.font.color.rgb = GOLD

    # Attribution Cards at Bottom
    c1 = add_card(s, 0.8, 5.2, 5.6, 1.6, bg=RGBColor(0x04, 0x33, 0x54), border=RGBColor(0x0C, 0x4A, 0x73))
    tx_author = s.shapes.add_textbox(Inches(1.0), Inches(5.35), Inches(5.2), Inches(1.3))
    tf_a = tx_author.text_frame
    tf_a.word_wrap = True
    tf_a.margin_left = tf_a.margin_right = tf_a.margin_top = tf_a.margin_bottom = 0
    
    pa1 = tf_a.paragraphs[0]
    ra1 = pa1.add_run()
    ra1.text = "PRIMARY AUTHOR & RESEARCH\n"
    ra1.font.name = FONT_NAME; ra1.font.size = Pt(8.5); ra1.font.bold = True; ra1.font.color.rgb = GOLD
    
    ra2 = pa1.add_run()
    ra2.text = "Adari Karthikeya\n"
    ra2.font.name = FONT_NAME; ra2.font.size = Pt(14); ra2.font.bold = True; ra2.font.color.rgb = COLOR_WHITE
    
    ra3 = pa1.add_run()
    ra3.text = "Physical AI Practice Research & Strategy"
    ra3.font.name = FONT_NAME; ra3.font.size = Pt(10); ra3.font.color.rgb = RGBColor(0xBA, 0xE6, 0xFD)

    c2 = add_card(s, 6.7, 5.2, 5.8, 1.6, bg=RGBColor(0x04, 0x33, 0x54), border=RGBColor(0x0C, 0x4A, 0x73))
    tx_client = s.shapes.add_textbox(Inches(6.9), Inches(5.35), Inches(5.4), Inches(1.3))
    tf_c = tx_client.text_frame
    tf_c.word_wrap = True
    tf_c.margin_left = tf_c.margin_right = tf_c.margin_top = tf_c.margin_bottom = 0
    
    pc1 = tf_c.paragraphs[0]
    rc1 = pc1.add_run()
    rc1.text = "PREPARED EXCLUSIVELY FOR\n"
    rc1.font.name = FONT_NAME; rc1.font.size = Pt(8.5); rc1.font.bold = True; rc1.font.color.rgb = RGBColor(0x38, 0xBD, 0xF8)
    
    rc2 = pc1.add_run()
    rc2.text = "Dr. Madhusudhan Singh & Engineering Leadership\n"
    rc2.font.name = FONT_NAME; rc2.font.size = Pt(13); rc2.font.bold = True; rc2.font.color.rgb = COLOR_WHITE
    
    rc3 = pc1.add_run()
    rc3.text = "L&T Technology Services (LTTS)  ·  September 2026"
    rc3.font.name = FONT_NAME; rc3.font.size = Pt(10); rc3.font.color.rgb = RGBColor(0xBA, 0xE6, 0xFD)

    set_notes(s, "Title Slide. Executive briefing establishing the commercial, technical, and operational reality of Physical AI in 2026 for LTTS leadership.")
    return s


def slide_02_taxonomy():
    s = new_slide()
    add_header(s, "Evidentiary Governance", "Four-Tier Verification Taxonomy",
               "Every quantitative metric and assertion in this briefing is classified by its evidentiary basis.")
    
    # Top context card
    add_card(s, 0.8, 1.75, 11.73, 0.80, bg=BG_CARD, border=BORDER_SUBTLE)
    tx_ctx = s.shapes.add_textbox(Inches(1.0), Inches(1.85), Inches(11.33), Inches(0.60))
    tf_ctx = tx_ctx.text_frame
    tf_ctx.word_wrap = True
    tf_ctx.margin_left = tf_ctx.margin_right = tf_ctx.margin_top = tf_ctx.margin_bottom = 0
    p = tf_ctx.paragraphs[0]
    r1 = p.add_run()
    r1.text = "Research Governance Standard: "
    r1.font.name = FONT_NAME; r1.font.size = Pt(10.5); r1.font.bold = True; r1.font.color.rgb = BRAND_NAVY
    r2 = p.add_run()
    r2.text = "To eliminate vendor marketing distortions and speculative venture hype, every quantitative claim, customer case study, and market benchmark across this 51-slide deck adheres strictly to this four-tier audit framework. Unverified claims are explicitly downgraded or removed in Appendix B."
    r2.font.name = FONT_NAME; r2.font.size = Pt(9.5); r2.font.color.rgb = TEXT_LIGHT

    tiers = [
        ("[Verified]", GREEN, BORDER_GREEN, "Primary & Audited Corporate Disclosure",
         "Sourced directly from audited SEC regulatory filings, primary peer-reviewed scientific publications, official audited corporate earnings calls (e.g. Alphabet, Tesla), or legally binding contract disclosures. Maximum evidentiary confidence."),
        
        ("[Reported]", CYAN, BORDER_CYAN, "Trade Press & Company Self-Reported Claims",
         "Public announcements, trade press coverage, company press releases, and executive statements that are documented but have not undergone third-party audit or independent operational verification."),
        
        ("[Estimated]", AMBER, BORDER_AMBER, "Directional Analytical Benchmarks",
         "Analytical estimates and financial ranges derived from public comparable benchmarks, bottom-up engineering models, and disclosed industry unit economics with transparent methodology."),
        
        ("[Speculative]", RED, BORDER_RED, "Forward-Looking Executive Judgments",
         "Forward-looking strategic inferences, technology timeline assessments, and critical hypotheses flagged explicitly for executive evaluation and risk-weighted decision making.")
    ]

    card_w = 2.78
    gap = 0.20
    for i, (tag, color, border, title, desc) in enumerate(tiers):
        left = 0.8 + i * (card_w + gap)
        top = 2.75
        card_h = 3.85
        add_card(s, left, top, card_w, card_h, bg=BG_CARD, border=BORDER_SUBTLE)
        
        # Subtle top accent line
        add_rect(s, left, top, card_w, 0.03, color)
        
        # Tag badge
        add_badge(s, left + 0.2, top + 0.20, tag, bg=border, fg=color, font_size=9.5, bold=True)
        
        tx_t = s.shapes.add_textbox(Inches(left + 0.2), Inches(top + 0.55), Inches(card_w - 0.4), Inches(0.65))
        tf_t = tx_t.text_frame
        tf_t.word_wrap = True
        tf_t.margin_left = tf_t.margin_right = tf_t.margin_top = tf_t.margin_bottom = 0
        p_t = tf_t.paragraphs[0]
        r_t = p_t.add_run()
        r_t.text = title
        r_t.font.name = FONT_NAME; r_t.font.size = Pt(11); r_t.font.bold = True; r_t.font.color.rgb = INK_PRIMARY

        tx_d = s.shapes.add_textbox(Inches(left + 0.2), Inches(top + 1.30), Inches(card_w - 0.4), Inches(2.3))
        tf_d = tx_d.text_frame
        tf_d.word_wrap = True
        tf_d.margin_left = tf_d.margin_right = tf_d.margin_top = tf_d.margin_bottom = 0
        p_d = tf_d.paragraphs[0]
        r_d = p_d.add_run()
        r_d.text = desc
        r_d.font.name = FONT_NAME; r_d.font.size = Pt(9.5); r_d.font.color.rgb = TEXT_LIGHT

    add_takeaway(s, "Every single data point in this deck is tagged. Dr. Singh and leadership can instantly inspect the evidentiary grounding of any claim.")
    set_notes(s, "Methodology Slide. Explain the four tiers. This builds immediate credibility with engineering leaders by acknowledging that not all claims are equal.")
    return s


def slide_03_exec_summary():
    s = new_slide()
    add_header(s, "Executive Summary", "The Core Strategic Thesis: Where Real Value Resides",
               "Physical AI marks a paradigm shift from language models to continuous physical control.")

    # 3 Stat Cards on Top
    add_stat_box(s, 0.8, 1.75, 3.75, 1.25, "> $3.2B", "Venture Capital Inflow", "18-month investment into humanoids & VLAs [Verified]", BRAND_NAVY)
    add_stat_box(s, 4.8, 1.75, 3.75, 1.25, "< $20M", "Verified Humanoid Revenue", "Production revenue across unconstrained humanoids [Estimated]", RED)
    add_stat_box(s, 8.8, 1.75, 3.73, 1.25, "$6B+ Cap", "LTTS ER&D Opportunity", "Pure-play engineering leader positioned upstream [Verified]", GREEN)

    # Main Core Thesis Card (Left)
    add_card(s, 0.8, 3.25, 6.6, 3.35, bg=BG_CARD, border=BORDER_SUBTLE)
    tx_left = s.shapes.add_textbox(Inches(1.05), Inches(3.45), Inches(6.1), Inches(3.0))
    tf_l = tx_left.text_frame
    tf_l.word_wrap = True
    tf_l.margin_left = tf_l.margin_right = tf_l.margin_top = tf_l.margin_bottom = 0

    p1 = tf_l.paragraphs[0]
    r1 = p1.add_run()
    r1.text = "THE REVOLUTION: FROM TOKENS TO TORQUES\n"
    r1.font.name = FONT_NAME; r1.font.size = Pt(11); r1.font.bold = True; r1.font.color.rgb = BRAND_NAVY

    p2 = tf_l.add_paragraph()
    p2.space_before = Pt(4)
    r2 = p2.add_run()
    r2.text = "Physical AI represents the fundamental transition from autoregressive token prediction in static semantic spaces to closed-loop causal interaction with continuous physical dynamics.\n\n"
    r2.font.name = FONT_NAME; r2.font.size = Pt(10); r2.font.color.rgb = TEXT_LIGHT

    p3 = tf_l.add_paragraph()
    r3 = p3.add_run()
    r3.text = "While massive venture capital flows into humanoid robotics OEMs, customer deployments remain bounded pre-production pilots. Meanwhile, simulation software platforms, functional safety test suites, and brownfield systems integration are generating hundreds of millions in high-margin enterprise software licenses and recurring services [Verified]."
    r3.font.name = FONT_NAME; r3.font.size = Pt(10); r3.font.color.rgb = TEXT_LIGHT

    # Right Card: The LTTS Moat
    add_card(s, 7.6, 3.25, 4.93, 3.35, bg=BG_CARD_ALT, border=BORDER_SUBTLE)
    tx_right = s.shapes.add_textbox(Inches(7.85), Inches(3.45), Inches(4.43), Inches(3.0))
    tf_r = tx_right.text_frame
    tf_r.word_wrap = True
    tf_r.margin_left = tf_r.margin_right = tf_r.margin_top = tf_r.margin_bottom = 0

    pr1 = tf_r.paragraphs[0]
    rr1 = pr1.add_run()
    rr1.text = "LTTS'S STRATEGIC PLAYBOOK\n"
    rr1.font.name = FONT_NAME; rr1.font.size = Pt(11); rr1.font.bold = True; rr1.font.color.rgb = BRAND_NAVY

    points = [
        ("No Hardware Manufacturing Drag:", "Avoid high BOM and low MTBF commoditizing hardware."),
        ("No Foundation Model Training Drag:", "Avoid competing with NVIDIA or DeepMind on 50B models."),
        ("The High-Margin 'Arms Dealer' Role:", "Become the Certified Systems Integration, V&V, and Synthetic Data Engine bridging frontier AI with brownfield PLCs.")
    ]
    for title, desc in points:
        p_pt = tf_r.add_paragraph()
        p_pt.space_before = Pt(6)
        r_t = p_pt.add_run()
        r_t.text = f"•  {title} "
        r_t.font.name = FONT_NAME; r_t.font.size = Pt(10); r_t.font.bold = True; r_t.font.color.rgb = INK_PRIMARY
        r_d = p_pt.add_run()
        r_d.text = desc
        r_d.font.name = FONT_NAME; r_d.font.size = Pt(9.5); r_d.font.color.rgb = TEXT_LIGHT

    add_takeaway(s, "LTTS captures high-margin enterprise revenue upstream by acting as the certified bridge between AI models and physical factory floors.")
    set_notes(s, "Executive Summary. Anchor the core thesis: do not build humanoids; do not train base models; own the integration, verification, and digital twin layer.")
    return s


def slide_04_agenda():
    s = new_slide()
    add_header(s, "Briefing Structure", "Executive Agenda & Architecture",
               "A structured, 8-part strategic examination of Physical Artificial Intelligence.")

    modules = [
        ("01", "Commercial State Mapping", "Capital deployment, maturity tiers, and the hardware vs software asymmetry."),
        ("02", "Frontier Research & Bottlenecks", "Flow matching, 3D world models, failure modes, and Pearl's Causal Ladder."),
        ("03", "Commercialization & LTTS Playbook", "Deal economics, contract sizes, and LTTS's 4 core service offerings."),
        ("04", "Production Reality vs. Hype", "Verified multi-sector deployments vs ungrounded humanoid marketing claims."),
        ("05", "Layered Competitive Landscape", "5 industry layers, incumbent dynamics, and high-value underserved gaps."),
        ("06", "The Industrial AI -> Physical AI Bridge", "Evolution vs category split, formal kinematics Jacobian moat, and data flywheel."),
        ("07", "3-5 Year Structural Forecast", "Market commoditization, foundation consolidation, and regulatory wildcards."),
        ("08", "Integrated LTTS Recommendations", "Sequenced priorities (V&V, Alliances, Synthetic Data, CoE) with bottom-up budgets.")
    ]

    for i, (num, title, desc) in enumerate(modules):
        col = i % 2
        row = i // 2
        left = 0.8 + col * 6.0
        top = 1.85 + row * 1.18
        w = 5.73
        h = 1.05

        add_card(s, left, top, w, h, bg=BG_CARD, border=BORDER_SUBTLE)
        add_badge(s, left + 0.15, top + 0.20, num, bg=BG_CARD_ALT, fg=BRAND_NAVY, font_size=10.5, bold=True)
        
        tx = s.shapes.add_textbox(Inches(left + 0.85), Inches(top + 0.15), Inches(w - 1.0), Inches(0.8))
        tf = tx.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        
        p = tf.paragraphs[0]
        r1 = p.add_run()
        r1.text = title + "\n"
        r1.font.name = FONT_NAME; r1.font.size = Pt(11); r1.font.bold = True; r1.font.color.rgb = INK_PRIMARY
        
        r2 = p.add_run()
        r2.text = desc
        r2.font.name = FONT_NAME; r2.font.size = Pt(9); r2.font.color.rgb = TEXT_MUTED

    add_takeaway(s, "Plus Appendices: Comprehensive Sources & Citations Index and the Adversarial Self-Critique / Downgrade Log.")
    set_notes(s, "Agenda Slide. Walk Dr. Singh through the journey: from commercial reality, to deep research, to commercial models, up to actionable budgets.")
    return s
