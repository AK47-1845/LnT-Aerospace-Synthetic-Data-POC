"""
Slides Part 5: Modules 4 & 5 — Use Cases, Adoption & Competitive Landscape (Slides 23 to 29)
Executive Editorial Light System: Crisp white canvas, 0.8" margins, deep ink typography.
"""

from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

from deck_common import (
    new_slide, add_card, add_rect, add_header, add_takeaway, add_stat_box,
    add_badge, set_notes, section_divider_slide, BG_CANVAS, BG_CARD, BG_CARD_ALT,
    BG_CARD_ACCENT, BORDER_SUBTLE, BORDER_GOLD, BORDER_CYAN, BORDER_GREEN,
    BORDER_AMBER, BORDER_RED, BORDER_PURPLE, GOLD, CYAN, GREEN, AMBER, RED, PURPLE, WHITE,
    COLOR_WHITE, BRAND_NAVY, BRAND_BLUE, INK_PRIMARY, TEXT_LIGHT, TEXT_MUTED, FONT_NAME
)

def slide_23_m4_divider():
    return section_divider_slide(
        4,
        "Use Cases & Adoption Patterns",
        "Production Reality vs. Hype & The Dominance of the Hybrid Model",
        [
            "Verified production deployments across 5 core industrial sectors",
            "Technical analysis of hype-ahead-of-deployment categories (humanoids, outdoor, surgical)",
            "The dominance of the hybrid incumbent-partner adoption model",
            "Why factory managers never bypass certified PLCs"
        ]
    )

def slide_24_verified_deployments():
    s = new_slide()
    add_header(s, "Module 4 · Use Cases & Adoption", "Verified Production Deployments Across 5 Core Sectors",
               "Documented enterprise deployments actively operating on global factory floors.")

    sectors = [
        ("Automotive Manufacturing", GREEN, [
            ("Optical & Acoustic Battery Inspection:", "Automated optical and acoustic vibration inspection for EV battery cells and body assembly modules deployed at BMW, Ford, and Mercedes facilities [Reported]."),
            ("Robotic Sheet Metal Handling:", "Robotic sheet metal positioning and parts handling in body shop cells operating under fixed mechanical fixture constraints [Verified].")
        ]),
        
        ("Aerospace & Defense", CYAN, [
            ("Composite Layup & Drilling:", "Automated composite layup inspection and precision robotic drilling guidance deployed across Airbus and Boeing commercial programs, cutting fuselage rework [Reported].")
        ]),

        ("Semiconductor Fabrication", BRAND_NAVY, [
            ("Physics-Informed Defect Classification:", "Physics-informed defect prediction and classification pipelines across wafer lithography stages (TSMC, Intel), optimizing tool uptime and yield [Reported].")
        ]),

        ("Logistics, Warehousing & Distribution", BRAND_BLUE, [
            ("Automated Container Unloading:", "Boston Dynamics Stretch mobile manipulators deployed at DHL Supply Chain for floor-loaded shipping container unloading [Verified]."),
            ("AMR Fleet Orchestration:", "Autonomous mobile robot fleets for tote transport and rack consolidation (Amazon Robotics, Symbotic at Walmart) [Verified].")
        ]),

        ("Energy & Utilities", PURPLE, [
            ("Turbine Health Monitoring:", "Predictive thermal and vibration monitoring on heavy gas turbines (GE Vernova SmartSignal, Siemens Energy Omnivise), mitigating unplanned trip events [Verified].")
        ])
    ]

    card_w = 11.73
    top_base = 1.85
    row_h = 0.88
    gap = 0.10

    for i, (sector, color, items) in enumerate(sectors):
        top = top_base + i * (row_h + gap)
        add_card(s, 0.8, top, card_w, row_h, bg=BG_CARD, border=BORDER_SUBTLE, border_width=0.75)

        tx = s.shapes.add_textbox(Inches(0.95), Inches(top + 0.10), Inches(card_w - 0.3), Inches(row_h - 0.20))
        tf = tx.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0

        p1 = tf.paragraphs[0]
        r1 = p1.add_run()
        r1.text = sector + "   "
        r1.font.name = FONT_NAME; r1.font.size = Pt(11); r1.font.bold = True; r1.font.color.rgb = INK_PRIMARY

        p2 = tf.add_paragraph()
        p2.space_before = Pt(2)
        for j, (hdr, desc) in enumerate(items):
            if j > 0:
                p2 = tf.add_paragraph()
                p2.space_before = Pt(2)
            rh = p2.add_run()
            rh.text = f"• {hdr} "
            rh.font.name = FONT_NAME; rh.font.size = Pt(9); rh.font.bold = True; rh.font.color.rgb = color
            rd = p2.add_run()
            rd.text = desc
            rd.font.name = FONT_NAME; rd.font.size = Pt(8.8); rd.font.color.rgb = TEXT_LIGHT

    add_takeaway(s, "Industrial Physical AI is already scaling in inspection, guided drilling, container unloading, and turbine monitoring.")
    set_notes(s, "Review verified deployments across 5 sectors. Highlight that these are documented deployments: DHL Stretch, TSMC lithography, GE Vernova.")
    return s


def slide_25_hype_analysis():
    s = new_slide()
    add_header(s, "Module 4 · Use Cases & Adoption", "Hype-Ahead-of-Deployment: Three Overstated Categories",
               "Rigorous engineering evaluation of three application categories facing severe physical barriers.")

    categories = [
        ("Unstructured Humanoid Assembly Workers", RED, BORDER_RED,
         "The Takt Time & Deformable Materials Wall",
         [
             ("Marketing Narrative:", "Claims that humanoid robots will broadly replace automotive final assembly line workers within the next 12 to 24 months are ungrounded [Speculative]."),
             ("Tactile & Dexterity Bottlenecks:", "Final assembly requires handling flexible electrical cables, seating deformable rubber grommets, and routing wire harnesses—tasks requiring dense tactile feedback that current humanoid hands lack."),
             ("The 60-Second Takt Barrier:", "Automotive assembly lines operate on rigid takt times (< 60 seconds per station). Current humanoids operate at 0.2x-0.4x human speed, creating instant line stoppage bottlenecks.")
         ]),

        ("Autonomous Outdoor Heavy Construction", AMBER, BORDER_AMBER,
         "The Environmental Dynamics Barrier",
         [
             ("Marketing Narrative:", "Autonomous excavators, graders, and multi-agent construction robots operating without human site supervisors [Reported]."),
             ("Soil & Weather Physics:", "Changing weather, heavy rain, thick mud, and shifting soil mechanics continuously disrupt visual odometry, traction control, and sim-to-real transfer."),
             ("Unstructured Boundaries:", "Unlike bounded indoor plants with fixed geometry, construction sites change topology dynamically each day, requiring human heavy-equipment operators for safety.")
         ]),

        ("Unsupervised Class III Surgical Robotics", PURPLE, BORDER_PURPLE,
         "The Statutory & Clinical Liability Barrier",
         [
             ("Marketing Narrative:", "Fully autonomous robotic tissue resection, suturing, and organ manipulation without surgeon guidance [Verified]."),
             ("FDA Class III Guardrails:", "Strict medical device regulatory frameworks (FDA Class III, CE Mark) mandate that systems remain strictly surgeon-in-the-loop with physical master-slave haptics."),
             ("Zero Legal Precedent:", "No hospital or insurer will indemnify autonomous neural networks for invasive soft-tissue surgical cuts without deterministic oversight.")
         ])
    ]

    card_w = 3.68
    gap = 0.34
    for i, (title, color, border, sub, items) in enumerate(categories):
        left = 0.8 + i * (card_w + gap)
        top = 1.85
        card_h = 4.75
        add_card(s, left, top, card_w, card_h, bg=BG_CARD, border=BORDER_SUBTLE, border_width=0.75)
        add_rect(s, left, top, card_w, 0.025, color)

        add_badge(s, left + 0.2, top + 0.22, f"HYPE ALERT {i+1}", bg=border, fg=color, font_size=8.5, bold=True)

        tx = s.shapes.add_textbox(Inches(left + 0.2), Inches(top + 0.60), Inches(card_w - 0.4), Inches(0.90))
        tf = tx.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        r1 = p.add_run()
        r1.text = title + "\n"
        r1.font.name = FONT_NAME; r1.font.size = Pt(11.5); r1.font.bold = True; r1.font.color.rgb = INK_PRIMARY
        r2 = p.add_run()
        r2.text = sub
        r2.font.name = FONT_NAME; r2.font.size = Pt(9); r2.font.bold = True; r2.font.color.rgb = color

        tx_body = s.shapes.add_textbox(Inches(left + 0.2), Inches(top + 1.55), Inches(card_w - 0.4), Inches(3.0))
        tf_b = tx_body.text_frame
        tf_b.word_wrap = True
        tf_b.margin_left = tf_b.margin_right = tf_b.margin_top = tf_b.margin_bottom = 0

        for j, (hdr, desc) in enumerate(items):
            pj = tf_b.paragraphs[0] if j == 0 else tf_b.add_paragraph()
            if j > 0: pj.space_before = Pt(6)
            rj1 = pj.add_run()
            rj1.text = f"• {hdr}\n"
            rj1.font.name = FONT_NAME; rj1.font.size = Pt(9.5); rj1.font.bold = True; rj1.font.color.rgb = INK_PRIMARY
            rj2 = pj.add_run()
            rj2.text = desc
            rj2.font.name = FONT_NAME; rj2.font.size = Pt(8.8); rj2.font.color.rgb = TEXT_LIGHT

    add_takeaway(s, "Do not build strategic business cases on unconstrained humanoids or autonomous surgery. Real growth is in bounded, structured industrial automation.")
    set_notes(s, "Hype vs Reality. Explain why humanoids cannot meet 60-second takt times or handle flexible wire harnesses in automotive assembly today.")
    return s


def slide_26_hybrid_adoption_model():
    s = new_slide()
    add_header(s, "Module 4 · Use Cases & Adoption", "Adoption Pattern: Dominance of the Hybrid Incumbent Model",
               "Industrial enterprise adoption follows a Hybrid Incumbent-Partner Pattern, not startup displacement.")

    pillars = [
        ("1. Incumbent Defense & Plant Trust", BRAND_NAVY, BORDER_SUBTLE,
         "Why Factory Managers Refuse Pure-Startup Stacks",
         "Industrial plant managers operate under immense operational pressure. Plant downtime costs upwards of $20,000 to $50,000 per minute in automotive assembly.",
         "Plant managers will never risk catastrophic production stops, equipment destruction, or voided corporate insurance policies by bypassing certified Siemens S7 or Rockwell ControlLogix safety PLCs to run experimental open-source AI stacks directly on machine drives."),

        ("2. AI Startup Distribution Limits", BRAND_BLUE, BORDER_CYAN,
         "The Severe Field Engineering Deficit",
         "Frontier AI startups possess world-class deep learning researchers, but completely lack the physical field engineering workforce required to execute hands-on deployments.",
         "Deploying into brownfield manufacturing requires wiring fieldbus drops, configuring safety relays, mounting ruggedized sensor brackets, and writing PLC ladder logic across thousands of non-standard plants. Startups cannot scale this workforce."),

        ("3. Strategic Alliances: The Winning Model", GREEN, BORDER_GREEN,
         "How Enterprise Incumbents Absorb Innovation",
         "Rather than being disrupted, industrial incumbents actively partner to absorb foundation model intelligence into their certified ecosystems.",
         "Key Example: Siemens partnering with Microsoft on the Industrial Copilot and with Intrinsic (Alphabet) on robotics motion software demonstrates how incumbents integrate AI while relying on certified systems integrators for customer delivery [Verified].")
    ]

    card_w = 3.68
    gap = 0.34
    for i, (title, color, border, sub, p1, p2) in enumerate(pillars):
        left = 0.8 + i * (card_w + gap)
        top = 1.85
        card_h = 4.75
        add_card(s, left, top, card_w, card_h, bg=BG_CARD, border=BORDER_SUBTLE, border_width=0.75)
        add_rect(s, left, top, card_w, 0.025, color)

        tx = s.shapes.add_textbox(Inches(left + 0.2), Inches(top + 0.22), Inches(card_w - 0.4), Inches(0.95))
        tf = tx.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        r1 = p.add_run()
        r1.text = title + "\n"
        r1.font.name = FONT_NAME; r1.font.size = Pt(12); r1.font.bold = True; r1.font.color.rgb = INK_PRIMARY
        r2 = p.add_run()
        r2.text = sub
        r2.font.name = FONT_NAME; r2.font.size = Pt(9); r2.font.bold = True; r2.font.color.rgb = color

        tx_body = s.shapes.add_textbox(Inches(left + 0.2), Inches(top + 1.25), Inches(card_w - 0.4), Inches(3.3))
        tf_b = tx_body.text_frame
        tf_b.word_wrap = True
        tf_b.margin_left = tf_b.margin_right = tf_b.margin_top = tf_b.margin_bottom = 0

        pb1 = tf_b.paragraphs[0]
        rb1 = pb1.add_run()
        rb1.text = p1 + "\n\n"
        rb1.font.name = FONT_NAME; rb1.font.size = Pt(9.2); rb1.font.color.rgb = TEXT_LIGHT

        pb2 = tf_b.add_paragraph()
        rb2 = pb2.add_run()
        rb2.text = p2
        rb2.font.name = FONT_NAME; rb2.font.size = Pt(8.8); rb2.font.color.rgb = TEXT_MUTED

    add_takeaway(s, "AI startups provide the brains; automation incumbents provide the trust; systems integrators like LTTS deliver the plant floor reality.")
    set_notes(s, "Explain the Hybrid Incumbent Model. Explain why Siemens + Microsoft + Intrinsic validates this: incumbents absorb software and rely on partners for deployment.")
    return s


def slide_27_m5_divider():
    return section_divider_slide(
        5,
        "Competitive Landscape",
        "Layered Industry Analysis & High-Value Underserved Gaps",
        [
            "Mapping the 5 structural competitive layers across Physical AI (Table 4)",
            "Challengers, dominant platform incumbents, and regulatory gatekeepers",
            "Direct competitors in ER&D engineering services (LTTS, KPIT, Cyient, Tata Tech)",
            "Identifying high-value underserved market gaps ripe for LTTS commercial entry"
        ]
    )


def slide_28_competitive_map_table():
    s = new_slide()
    add_header(s, "Module 5 · Competitive Landscape", "Layered Competitive Landscape Across Physical AI (Table 4)",
               "Five structural tiers define the global ecosystem from foundation models to statutory compliance.")

    left_m = 0.8
    top_base = 1.80
    total_w = 11.73

    # Column widths summing to 11.73"
    col_w = [2.70, 2.50, 2.80, 3.73]
    col_x = [left_m]
    for w in col_w[:-1]:
        col_x.append(col_x[-1] + w)

    # Header Row (Navy)
    hdr_h = 0.38
    add_rect(s, left_m, top_base, total_w, hdr_h, BRAND_NAVY)

    headers = [
        "ECOSYSTEM LAYER",
        "KEY INDUSTRY PLAYERS",
        "CORE TECHNICAL OFFERING",
        "STRATEGIC STRUCTURAL POSITION"
    ]

    for j, (h_text, x_pos, w) in enumerate(zip(headers, col_x, col_w)):
        tx = s.shapes.add_textbox(Inches(x_pos + 0.10), Inches(top_base + 0.05), Inches(w - 0.20), Inches(hdr_h - 0.10))
        tf = tx.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        r = p.add_run()
        r.text = h_text
        r.font.name = FONT_NAME; r.font.size = Pt(8.5); r.font.bold = True; r.font.color.rgb = COLOR_WHITE

    layers = [
        ("Robotics Foundation Models",
         "Physical Intelligence, Skild AI, DeepMind",
         "Pretrained generalist VLA models (π0, Skild Brain)",
         "Challengers: Frontier algorithms, high venture capital, but dependent on partners for field plant distribution.",
         CYAN, False),

        ("Industrial Automation Incumbents",
         "Siemens, Rockwell Automation, ABB, Schneider",
         "PLCs, DCS, SCADA, FactoryTalk, TIA Portal ecosystems",
         "Dominant: Own factory floors, machine safety certifications, and decades of customer trust.",
         GREEN, False),

        ("Simulation & Digital Twin Platforms",
         "NVIDIA (Isaac/Cosmos), Applied Intuition",
         "Physics simulation, synthetic data generation pipelines",
         "Dominant: Platform standards for testing, virtual commissioning, and synthetic policy generation.",
         BRAND_NAVY, False),

        ("ER&D Engineering Services",
         "LTTS, KPIT Tech, Tata Tech, Cyient, Accenture",
         "Systems integration, V&V, digital engineering & PLC bridges",
         "Direct Competitors: Race to build certified Physical AI field practices and bridge neural policies with industrial machinery.",
         BRAND_BLUE, True),  # Highlighted LTTS Category

        ("Safety & Statutory Compliance",
         "TÜV SÜD, UL Solutions, Credo AI, Holistic AI",
         "Functional safety audits, regulatory compliance dossiers",
         "Gatekeepers: Mandatory for legal operation, safety dossiers, and factory insurance underwriting.",
         PURPLE, False)
    ]

    row_h = 0.88
    for i, (layer, players, offering, position, color, is_erd) in enumerate(layers):
        row_top = top_base + hdr_h + i * row_h
        row_bg = RGBColor(0xEE, 0xF4, 0xFA) if is_erd else (BG_CARD if i % 2 == 0 else COLOR_WHITE)
        row_border = BRAND_BLUE if is_erd else BORDER_SUBTLE

        add_card(s, left_m, row_top, total_w, row_h, bg=row_bg, border=row_border, border_width=1.0 if is_erd else 0.5)

        if is_erd:
            add_rect(s, left_m, row_top, 0.04, row_h, BRAND_BLUE)

        # Col 0: Ecosystem Layer
        tx0 = s.shapes.add_textbox(Inches(col_x[0] + 0.12), Inches(row_top + 0.12), Inches(col_w[0] - 0.20), Inches(row_h - 0.24))
        tf0 = tx0.text_frame; tf0.word_wrap = True; tf0.margin_left = tf0.margin_right = tf0.margin_top = tf0.margin_bottom = 0
        p0 = tf0.paragraphs[0]
        r0 = p0.add_run(); r0.text = layer; r0.font.name = FONT_NAME; r0.font.size = Pt(10.5); r0.font.bold = True; r0.font.color.rgb = INK_PRIMARY
        if is_erd:
            p0_b = tf0.add_paragraph()
            p0_b.space_before = Pt(2)
            r0_b = p0_b.add_run(); r0_b.text = "★ LTTS COMPETITIVE POSITION"; r0_b.font.name = FONT_NAME; r0_b.font.size = Pt(8); r0_b.font.bold = True; r0_b.font.color.rgb = BRAND_BLUE

        # Col 1: Players
        tx1 = s.shapes.add_textbox(Inches(col_x[1] + 0.10), Inches(row_top + 0.14), Inches(col_w[1] - 0.20), Inches(row_h - 0.28))
        tf1 = tx1.text_frame; tf1.word_wrap = True; tf1.margin_left = tf1.margin_right = tf1.margin_top = tf1.margin_bottom = 0
        p1 = tf1.paragraphs[0]
        r1 = p1.add_run(); r1.text = players; r1.font.name = FONT_NAME; r1.font.size = Pt(9); r1.font.color.rgb = TEXT_LIGHT

        # Col 2: Offering
        tx2 = s.shapes.add_textbox(Inches(col_x[2] + 0.10), Inches(row_top + 0.12), Inches(col_w[2] - 0.20), Inches(row_h - 0.24))
        tf2 = tx2.text_frame; tf2.word_wrap = True; tf2.margin_left = tf2.margin_right = tf2.margin_top = tf2.margin_bottom = 0
        p2 = tf2.paragraphs[0]
        r2 = p2.add_run(); r2.text = offering; r2.font.name = FONT_NAME; r2.font.size = Pt(9); r2.font.color.rgb = TEXT_LIGHT

        # Col 3: Position
        tx3 = s.shapes.add_textbox(Inches(col_x[3] + 0.10), Inches(row_top + 0.12), Inches(col_w[3] - 0.20), Inches(row_h - 0.24))
        tf3 = tx3.text_frame; tf3.word_wrap = True; tf3.margin_left = tf3.margin_right = tf3.margin_top = tf3.margin_bottom = 0
        p3 = tf3.paragraphs[0]
        r3 = p3.add_run(); r3.text = position; r3.font.name = FONT_NAME; r3.font.size = Pt(8.8); r3.font.color.rgb = TEXT_LIGHT

    add_takeaway(s, "ER&D engineering services is the linchpin layer connecting generalist model challengers with entrenched factory incumbents.")
    set_notes(s, "Review Table 4. Point out the structural position of each layer: Incumbents own the floor, model labs own the algorithms, LTTS integrates them.")
    return s


def slide_29_underserved_gaps():
    s = new_slide()
    add_header(s, "Module 5 · Competitive Landscape", "High-Value Underserved Gaps in the Market",
               "Three critical white-space opportunities where enterprise demand far outstrips current tooling.")

    gaps = [
        ("GAP 1", "Formal Safety Verification Tooling for Neural Policies", RED, BORDER_RED,
         "The Certification Deficit for Probabilistic Controllers",
         [
             ("The Industry Stalemate:", "Foundation model startups generate neural policies, but industrial certifiers (TÜV, UL) and plant insurers demand deterministic mathematical safety proofs."),
             ("The Missing Toolchain:", "A major market vacuum exists for automated software toolchains that translate neural network weights into formal functional safety compliance dossiers (satisfying IEC 61508 and ISO 13849)."),
             ("LTTS Opportunity:", "Build the first automated Neural Safety Dossier Compiler, using Control Barrier Functions and interval bound propagation (Priority 1).")
         ]),

        ("GAP 2", "CAD/PLM to Differentiable Physics Pipelines", BRAND_NAVY, BORDER_SUBTLE,
         "The High-Friction Digital Twin Ingestion Bottleneck",
         [
             ("The Manual Engineering Drag:", "Converting complex enterprise CAD/PLM assemblies (Siemens NX, Teamcenter, CATIA) into simulation-ready digital twin environments currently requires weeks of manual engineering."),
             ("Friction & Contact Breakdown:", "Translating CAD geometry into mesh representations with accurate contact dynamics, mass matrices, and collision hulls is severely fragmented."),
             ("LTTS Opportunity:", "Offer automated ingestion pipelines converting mechanical CAD into calibrated Isaac Sim environments (Priority 3).")
         ]),

        ("GAP 3", "Deterministic Edge Deployment Middleware", BRAND_BLUE, BORDER_CYAN,
         "The Real-Time Jitter & Latency Barrier",
         [
             ("The Embedded Real-Time Gap:", "Managing the real-time execution of multi-billion parameter VLAs on industrial edge compute (NVIDIA Jetson AGX Orin) without timing jitter or safety watchdog violations."),
             ("Fieldbus Synchronization:", "Zero commercial middleware exists today that natively bridges PyTorch/TensorRT inference with 1ms EtherCAT cycles with formal RTOS guarantees."),
             ("LTTS Opportunity:", "Develop proprietary edge integration middleware connecting AI models to industrial fieldbuses (Priority 2).")
         ])
    ]

    card_w = 3.68
    gap = 0.34
    for i, (badge, title, color, border, sub, items) in enumerate(gaps):
        left = 0.8 + i * (card_w + gap)
        top = 1.85
        card_h = 4.75
        add_card(s, left, top, card_w, card_h, bg=BG_CARD, border=BORDER_SUBTLE, border_width=0.75)
        add_rect(s, left, top, card_w, 0.025, color)

        add_badge(s, left + 0.2, top + 0.22, badge, bg=border, fg=color, font_size=8.5, bold=True)

        tx = s.shapes.add_textbox(Inches(left + 0.2), Inches(top + 0.60), Inches(card_w - 0.4), Inches(0.95))
        tf = tx.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        r1 = p.add_run()
        r1.text = title + "\n"
        r1.font.name = FONT_NAME; r1.font.size = Pt(11.5); r1.font.bold = True; r1.font.color.rgb = INK_PRIMARY
        r2 = p.add_run()
        r2.text = sub
        r2.font.name = FONT_NAME; r2.font.size = Pt(9); r2.font.bold = True; r2.font.color.rgb = color

        tx_body = s.shapes.add_textbox(Inches(left + 0.2), Inches(top + 1.60), Inches(card_w - 0.4), Inches(3.0))
        tf_b = tx_body.text_frame
        tf_b.word_wrap = True
        tf_b.margin_left = tf_b.margin_right = tf_b.margin_top = tf_b.margin_bottom = 0

        for j, (hdr, desc) in enumerate(items):
            pj = tf_b.paragraphs[0] if j == 0 else tf_b.add_paragraph()
            if j > 0: pj.space_before = Pt(6)
            rj1 = pj.add_run()
            rj1.text = f"• {hdr}\n"
            rj1.font.name = FONT_NAME; rj1.font.size = Pt(9.5); rj1.font.bold = True; rj1.font.color.rgb = INK_PRIMARY
            rj2 = pj.add_run()
            rj2.text = desc
            rj2.font.name = FONT_NAME; rj2.font.size = Pt(8.8); rj2.font.color.rgb = TEXT_LIGHT

    add_takeaway(s, "These three gaps define LTTS's strategic roadmap: Formal Safety Dossiers (Q1 27), Edge Middleware (Q2 27), and CAD-to-Sim (Q3 27).")
    set_notes(s, "Explain the three underserved gaps. Emphasize that these gaps directly correspond to LTTS's 4 priority strategic recommendations.")
    return s
