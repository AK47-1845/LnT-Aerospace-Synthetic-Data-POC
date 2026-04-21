"""
The Practice of Physical AI — Executive Presentation Specification & Layout Engine
==================================================================================
Defines global geometric constants, typography scale, color system, and shape builders
strictly adhering to the executive build specification.
"""

import os
import io
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# ── CANVAS SPECIFICATION ───────────────────────────────────────────────────────
CANVAS_WIDTH  = Inches(13.333)
CANVAS_HEIGHT = Inches(7.500)

# ── GEOMETRIC ZONES (Define once, reuse everywhere — ZERO ad-hoc positions) ────
MARGIN_LEFT   = Inches(0.6)
MARGIN_RIGHT  = Inches(0.6)
MARGIN_TOP    = Inches(0.6)
MARGIN_BOTTOM = Inches(0.6)

CONTENT_WIDTH  = Inches(12.133) # 13.333 - 1.2
CONTENT_TOP    = Inches(1.45)   # Content zone starts below header zone
CONTENT_HEIGHT = Inches(5.35)   # 1.45 to 6.80 (leaving room for takeaway & footer)
CONTENT_BOTTOM = Inches(6.80)

# Header Zone: top 0.6in - 1.35in
HEADER_TOP    = Inches(0.60)
HEADER_LEFT   = Inches(0.60)
HEADER_WIDTH  = CONTENT_WIDTH
HEADER_HEIGHT = Inches(0.80)

# Footer Zone: bottom 7.15in - 7.50in
FOOTER_TOP    = Inches(7.15)
FOOTER_LEFT   = Inches(0.60)
FOOTER_WIDTH  = CONTENT_WIDTH
FOOTER_HEIGHT = Inches(0.30)

# Takeaway Zone: 6.65in - 7.05in
TAKEAWAY_TOP    = Inches(6.55)
TAKEAWAY_LEFT   = Inches(0.60)
TAKEAWAY_WIDTH  = CONTENT_WIDTH
TAKEAWAY_HEIGHT = Inches(0.48)

# ── COLOR PALETTE (Strict, unified dark palette — NO theme leakage) ───────────
COLOR_BG          = RGBColor(0x0B, 0x12, 0x20) # Deep navy-charcoal background
COLOR_CARD_BG     = RGBColor(0x13, 0x1E, 0x32) # Surface dark card
COLOR_CARD_BORDER = RGBColor(0x26, 0x35, 0x4D) # Card border hairline
COLOR_TEXT_MAIN   = RGBColor(0xF5, 0xF6, 0xF8) # Primary crisp text
COLOR_TEXT_MUTED  = RGBColor(0x94, 0xA3, 0xB8) # Secondary muted text
COLOR_TEXT_DIM    = RGBColor(0x64, 0x74, 0x8B) # Footer / dimmed caption
COLOR_ACCENT      = RGBColor(0x3B, 0x82, 0xF6) # Electric Blue (SINGLE accent for entire deck)
COLOR_ACCENT_BG   = RGBColor(0x1D, 0x3A, 0x6E) # Deep accent container

# Verification Badge Colors (Mandatory standard)
COLOR_VERIFIED    = RGBColor(0x22, 0xC5, 0x5E) # [Verified] Green
COLOR_REPORTED    = RGBColor(0x94, 0xA3, 0xB8) # [Reported] Slate
COLOR_ESTIMATED   = RGBColor(0xEA, 0xB3, 0x08) # [Estimated] Amber
COLOR_SPECULATIVE = RGBColor(0xEF, 0x44, 0x44) # [Speculative] Red

# ── TYPOGRAPHIC SCALE ─────────────────────────────────────────────────────────
FONT_FAMILY = "Segoe UI" # Geometric, crisp sans-serif available across platforms

SIZE_SECTION_TITLE = Pt(44) # Section divider title
SIZE_SLIDE_TITLE   = Pt(32) # Standard slide title
SIZE_BODY_MIN      = Pt(18) # Body text MINIMUM (never smaller)
SIZE_STAT_NUM      = Pt(64) # Big stat numbers (60 - 96pt)
SIZE_STAT_CAPTION  = Pt(14) # Stat captions underneath
SIZE_LABEL_MIN     = Pt(14) # Table / chart labels minimum
SIZE_FOOTER        = Pt(10) # Footer text

# ── SHAPE BUILDERS & HELPERS ──────────────────────────────────────────────────
def init_presentation():
    prs = Presentation()
    prs.slide_width  = CANVAS_WIDTH
    prs.slide_height = CANVAS_HEIGHT
    return prs

def create_slide(prs):
    """Creates a blank slide with guaranteed solid COLOR_BG background."""
    blank_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank_layout)
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = COLOR_BG
    return slide

def add_header(slide, title_text, category_text=None):
    """Standardized header in the 0.6in - 1.35in zone."""
    tb = slide.shapes.add_textbox(HEADER_LEFT, HEADER_TOP, HEADER_WIDTH, HEADER_HEIGHT)
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    
    p = tf.paragraphs[0]
    p.space_after = Pt(0)
    
    if category_text:
        r_cat = p.add_run()
        r_cat.text = category_text.upper() + "  |  "
        r_cat.font.name = FONT_FAMILY
        r_cat.font.size = Pt(13)
        r_cat.font.bold = True
        r_cat.font.color.rgb = COLOR_ACCENT

    r_title = p.add_run()
    r_title.text = title_text
    r_title.font.name = FONT_FAMILY
    r_title.font.size = SIZE_SLIDE_TITLE
    r_title.font.bold = True
    r_title.font.color.rgb = COLOR_TEXT_MAIN

def add_footer(slide, slide_num, section_name):
    """Standardized footer at 7.15in - 7.50in."""
    tb = slide.shapes.add_textbox(FOOTER_LEFT, FOOTER_TOP, FOOTER_WIDTH, FOOTER_HEIGHT)
    tf = tb.text_frame
    tf.word_wrap = False
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    
    p = tf.paragraphs[0]
    r = p.add_run()
    r.text = f"{slide_num:02d} — {section_name.upper()}"
    r.font.name = FONT_FAMILY
    r.font.size = SIZE_FOOTER
    r.font.bold = True
    r.font.color.rgb = COLOR_TEXT_DIM

def add_takeaway(slide, bold_prefix, takeaway_text):
    """Standardized takeaway box at the bottom of the content zone."""
    shape = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        TAKEAWAY_LEFT, TAKEAWAY_TOP, TAKEAWAY_WIDTH, TAKEAWAY_HEIGHT
    )
    shape.adjustments[0] = 0.25
    shape.fill.solid()
    shape.fill.fore_color.rgb = COLOR_CARD_BG
    shape.line.color.rgb = COLOR_ACCENT
    shape.line.width = Pt(1)
    
    tf = shape.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.margin_left = Inches(0.2)
    tf.margin_right = Inches(0.2)
    tf.margin_top = tf.margin_bottom = 0
    
    p = tf.paragraphs[0]
    r1 = p.add_run()
    r1.text = "TAKEAWAY: " + bold_prefix + " "
    r1.font.name = FONT_FAMILY
    r1.font.size = Pt(14)
    r1.font.bold = True
    r1.font.color.rgb = COLOR_ACCENT
    
    r2 = p.add_run()
    r2.text = takeaway_text
    r2.font.name = FONT_FAMILY
    r2.font.size = Pt(14)
    r2.font.color.rgb = COLOR_TEXT_MAIN

def add_card(slide, left, top, width, height, bg=COLOR_CARD_BG, border=COLOR_CARD_BORDER, border_width=1.0):
    """Draws a standardized dark card container."""
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.adjustments[0] = 0.08
    shape.fill.solid()
    shape.fill.fore_color.rgb = bg
    if border:
        shape.line.color.rgb = border
        shape.line.width = Pt(border_width)
    else:
        shape.line.fill.background()
    return shape

def add_badge(slide, left, top, badge_type):
    """Draws a visible verification badge pill."""
    badges = {
        "Verified":    (COLOR_VERIFIED,    "[Verified]"),
        "Reported":    (COLOR_REPORTED,    "[Reported]"),
        "Estimated":   (COLOR_ESTIMATED,   "[Estimated]"),
        "Speculative": (COLOR_SPECULATIVE, "[Speculative]")
    }
    color, text = badges.get(badge_type, (COLOR_REPORTED, f"[{badge_type}]"))
    
    pill = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, Inches(1.35), Inches(0.28))
    pill.adjustments[0] = 0.5
    pill.fill.solid()
    pill.fill.fore_color.rgb = color
    pill.line.fill.background()
    
    tf = pill.text_frame
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = text
    r.font.name = FONT_FAMILY
    r.font.size = Pt(11)
    r.font.bold = True
    r.font.color.rgb = RGBColor(0x07, 0x09, 0x0E) # Dark text for high contrast pill
    return pill

def render_equation_image(latex_str, text_color='#F5F6F8', fontsize=26, dpi=300):
    """Renders a LaTeX equation into an in-memory PNG buffer with transparent background."""
    fig = plt.figure(figsize=(0.01, 0.01))
    fig.patch.set_alpha(0.0)
    text = fig.text(0, 0, f"${latex_str}$", fontsize=fontsize, color=text_color, math_fontfamily='cm')
    renderer = fig.canvas.get_renderer()
    bbox = text.get_window_extent(renderer=renderer)
    pad = 8
    w_in = (bbox.width + pad * 2) / dpi
    h_in = (bbox.height + pad * 2) / dpi
    fig.set_size_inches(max(w_in, 0.5), max(h_in, 0.3))
    text.set_position((pad / fig.get_window_extent().width, pad / fig.get_window_extent().height))
    
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=dpi, transparent=True, bbox_inches='tight', pad_inches=pad/dpi)
    plt.close(fig)
    buf.seek(0)
    return buf
