#!/usr/bin/env python3
"""
Grimasso Referral Kit PDF Generator
Generates a print-ready A4 referral card for SLPs/orthodontists to hand to parents.
"""

import io
import os
import sys

from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ── Paths ────────────────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PATH = os.path.join(SCRIPT_DIR, "grimasso-referral-kit-en.pdf")
MASCOT_PATH = "/Users/lorenzmaierhofer/claude-projects/LogoApp/input/Grimasso_Images/Grimasso_Main.png"
# ── Colors ────────────────────────────────────────────────────────────────────
GREEN      = colors.HexColor("#33C759")
GREEN_DARK = colors.HexColor("#26A647")
GREEN_PILL = colors.HexColor("#E8F9ED")
GREEN_STEP = colors.HexColor("#F0FAF3")
BODY_TEXT  = colors.HexColor("#2A2A35")
LABEL_CLR  = colors.HexColor("#26A647")
WHITE      = colors.white
LIGHT_GRAY = colors.HexColor("#F5F5F7")
MID_GRAY   = colors.HexColor("#8E8E9A")

# ── Font setup ────────────────────────────────────────────────────────────────
# Avenir Next from macOS system fonts (TTC subfont indices)
AVENIR_TTC  = "/System/Library/Fonts/Avenir Next.ttc"
AVENIR_MAP  = {
    "AvenirNext-Regular":   7,   # Avenir Next Regular
    "AvenirNext-Medium":    5,   # Avenir Next Medium
    "AvenirNext-DemiBold":  2,   # Avenir Next Demi Bold
    "AvenirNext-Bold":      0,   # Avenir Next Bold
    "AvenirNext-Heavy":     8,   # Avenir Next Heavy
}

def load_fonts():
    """Register Avenir Next from macOS system fonts; fall back to Helvetica."""
    loaded = {}
    for name, idx in AVENIR_MAP.items():
        try:
            pdfmetrics.registerFont(TTFont(name, AVENIR_TTC, subfontIndex=idx))
            loaded[name] = name
            print(f"  Registered: {name}")
        except Exception as e:
            print(f"  WARNING: could not register {name}: {e}")
            loaded[name] = None

    return {
        "regular":   loaded.get("AvenirNext-Regular")   or "Helvetica",
        "semibold":  loaded.get("AvenirNext-Medium")    or "Helvetica",
        "bold":      loaded.get("AvenirNext-DemiBold")  or "Helvetica-Bold",
        "extrabold": loaded.get("AvenirNext-Bold")      or "Helvetica-Bold",
    }


def make_qr() -> ImageReader:
    """Generate QR code pointing to the Grimasso App Store page."""
    import qrcode
    from qrcode.constants import ERROR_CORRECT_H

    qr = qrcode.QRCode(
        version=None,
        error_correction=ERROR_CORRECT_H,
        box_size=10,
        border=2,
    )
    qr.add_data("https://apps.apple.com/us/app/grimasso/id6758241652")
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return ImageReader(buf)


def rounded_rect(c: canvas.Canvas, x, y, w, h, r, fill_color=None, stroke_color=None, stroke_width=1):
    """Draw a rounded rectangle. y is bottom-left (ReportLab convention)."""
    p = c.beginPath()
    p.moveTo(x + r, y)
    p.lineTo(x + w - r, y)
    p.arcTo(x + w - 2*r, y, x + w, y + 2*r, startAng=-90, extent=90)
    p.lineTo(x + w, y + h - r)
    p.arcTo(x + w - 2*r, y + h - 2*r, x + w, y + h, startAng=0, extent=90)
    p.lineTo(x + r, y + h)
    p.arcTo(x, y + h - 2*r, x + 2*r, y + h, startAng=90, extent=90)
    p.lineTo(x, y + r)
    p.arcTo(x, y, x + 2*r, y + 2*r, startAng=180, extent=90)
    p.close()

    c.saveState()
    if fill_color:
        c.setFillColor(fill_color)
    if stroke_color:
        c.setStrokeColor(stroke_color)
        c.setLineWidth(stroke_width)
        c.drawPath(p, fill=1 if fill_color else 0, stroke=1 if stroke_color else 0)
    else:
        c.drawPath(p, fill=1 if fill_color else 0, stroke=0)
    c.restoreState()


def text_centered(c: canvas.Canvas, text, cx, y, font, size, color=BODY_TEXT):
    c.saveState()
    c.setFont(font, size)
    c.setFillColor(color)
    w = c.stringWidth(text, font, size)
    c.drawString(cx - w/2, y, text)
    c.restoreState()


def draw_spaced(c: canvas.Canvas, text, x, y, font, size, spacing=1.6, color=BODY_TEXT):
    """Draw text with manual letter spacing."""
    c.saveState()
    c.setFont(font, size)
    c.setFillColor(color)
    cx = x
    for ch in text:
        c.drawString(cx, y, ch)
        cx += c.stringWidth(ch, font, size) + spacing
    c.restoreState()


def wrap_text(c: canvas.Canvas, text, x, y, max_width, font, size, line_height, color=BODY_TEXT):
    """Simple word-wrap for canvas text. Returns final y position."""
    c.saveState()
    c.setFont(font, size)
    c.setFillColor(color)
    words = text.split()
    line = ""
    for word in words:
        test = (line + " " + word).strip()
        if c.stringWidth(test, font, size) <= max_width:
            line = test
        else:
            c.drawString(x, y, line)
            y -= line_height
            line = word
    if line:
        c.drawString(x, y, line)
        y -= line_height
    c.restoreState()
    return y


def generate(fonts):
    W, H = A4   # 595.28 × 841.89 pt
    MARGIN = 30

    c = canvas.Canvas(OUTPUT_PATH, pagesize=A4)
    c.setTitle("Grimasso – Referral Card for Clinicians")
    c.setAuthor("Lorenz Maierhofer")
    c.setSubject("Recommend Grimasso to your patients")

    qr_img   = make_qr()
    mascot   = ImageReader(MASCOT_PATH)

    # ── SECTION BOUNDARIES ─────────────────────────────────────────────────
    # Equal GAP=16 between every section pair; separators at midpoints.
    #
    # Header:     y 678 → 842  (h=164, full-bleed)
    # WHAT:       y 618 → 678  (h=60)   sep at y=610
    # CAT:        y 554 → 602  (h=48)   sep at y=546
    # CLP:        y 288 → 538  (h=250)  sep at y=280
    # HOW:        y 172 → 272  (h=100)  sep at y=164
    # QR+CTA:     y  52 → 156  (h=104)  centered block
    # Contact:    text at y=36
    # Footer:     y   0 →  28  (h=28)
    GAP  = 16   # equal inter-section breathing room
    LPAD = 12   # section label: distance from section TOP to label baseline

    # ── Explicit section coordinates ─────────────────────────────────────────
    HDR_TOP  = H;        HDR_BOT  = H - 164       # 842 → 678
    WHAT_TOP = HDR_BOT;  WHAT_BOT = WHAT_TOP - 60 # 678 → 618
    CAT_TOP  = WHAT_BOT - GAP;  CAT_BOT = CAT_TOP - 48   # 602 → 554
    CLP_TOP  = CAT_BOT  - GAP;  CLP_BOT = 298             # 538 → 298
    HOW_TOP  = CLP_BOT  - GAP;  HOW_BOT = HOW_TOP - 100   # 272 → 172
    QR_TOP   = HOW_BOT  - GAP;  QR_BOT  = 52              # 156 → 52

    def draw_sep(y):
        """Draw a consistent separator line."""
        c.saveState()
        c.setStrokeColor(colors.HexColor("#D8D8E0"))
        c.setLineWidth(0.5)
        c.line(MARGIN, y, W - MARGIN, y)
        c.restoreState()

    # ────────────────────────────────────────────────────────────────────────
    # HEADER BAND
    # ────────────────────────────────────────────────────────────────────────
    HDR_H = HDR_TOP - HDR_BOT

    c.setFillColor(GREEN)
    c.rect(0, HDR_BOT, W, HDR_H, fill=1, stroke=0)

    # Subtle diagonal stripe texture in header
    c.saveState()
    c.setStrokeColor(colors.HexColor("#2DB34E"))
    c.setLineWidth(0.4)
    for i in range(-20, int(W)+50, 18):
        c.line(i, HDR_BOT, i + HDR_H, HDR_BOT + HDR_H)
    c.restoreState()

    # Mascot — right side, slightly overflowing header top
    MASCOT_W = 148
    MASCOT_H = int(MASCOT_W * (1034 / 1142))
    mascot_x = W - MARGIN - MASCOT_W - 2
    mascot_y = HDR_BOT - 2
    c.drawImage(mascot, mascot_x, mascot_y, width=MASCOT_W, height=MASCOT_H, mask='auto')

    # Header text (left of mascot)
    text_right_edge = mascot_x - 12
    text_width = text_right_edge - MARGIN

    # "FOR SPEECH THERAPISTS & ORTHODONTISTS" — small caps label
    label_y = HDR_TOP - 26
    draw_spaced(c, "FROM YOUR SPEECH THERAPIST",
                MARGIN, label_y, fonts["bold"], 7.5,
                spacing=1.8, color=colors.HexColor("#B8F5C8"))

    # Main headline — two lines
    c.saveState()
    c.setFont(fonts["extrabold"], 23)
    c.setFillColor(WHITE)
    c.drawString(MARGIN, label_y - 32, "Your Child's Therapy")
    c.drawString(MARGIN, label_y - 58, "Homework — Made Fun")
    c.restoreState()

    # Divider line
    div_y = label_y - 68
    c.saveState()
    c.setStrokeColor(colors.HexColor("#5BD97A"))
    c.setLineWidth(1.5)
    c.line(MARGIN, div_y, MARGIN + text_width * 0.55, div_y)
    c.restoreState()

    # Subheadline
    c.saveState()
    c.setFont(fonts["semibold"], 10.5)
    c.setFillColor(colors.HexColor("#D4F7DF"))
    sub_y = div_y - 16
    c.drawString(MARGIN, sub_y, "Free · Ages 7–12 · iOS")
    c.drawString(MARGIN, sub_y - 15, "Recommended by your therapist")
    c.restoreState()

    # ────────────────────────────────────────────────────────────────────────
    # WHAT IS GRIMASSO
    # ────────────────────────────────────────────────────────────────────────
    sec_y = WHAT_TOP - LPAD - 5
    draw_spaced(c, "WHAT IS GRIMASSO?", MARGIN, sec_y, fonts["extrabold"], 7, color=LABEL_CLR)
    body = ("Grimasso turns the tongue, lip, and jaw exercises your therapist prescribed into a game "
            "your child will ask to play. 100 guided exercises across 20 levels — with a lovable frog "
            "mascot, streaks, and badges that make daily practice feel like an achievement.")
    wrap_text(c, body, MARGIN, sec_y - 14, W - 2*MARGIN, fonts["regular"], 9, 13.5, BODY_TEXT)
    draw_sep(WHAT_BOT - GAP // 2)   # separator at midpoint of gap

    # ────────────────────────────────────────────────────────────────────────
    # WHAT YOUR CHILD WILL PRACTICE
    # ────────────────────────────────────────────────────────────────────────
    sec_y = CAT_TOP - LPAD
    draw_spaced(c, "WHAT YOUR CHILD WILL PRACTICE", MARGIN, sec_y, fonts["extrabold"], 7, color=LABEL_CLR)

    categories = ["Tongue Tip", "Tongue Strength", "Tongue Control", "Swallowing", "Jaw Muscles"]
    pill_y_center = sec_y - 20
    pill_h = 18
    pill_r = 9
    pill_gap = 7
    c.saveState()
    c.setFont(fonts["bold"], 8)
    total_w = sum(c.stringWidth(cat, fonts["bold"], 8) + 20 for cat in categories) + pill_gap * (len(categories) - 1)
    pill_x = (W - total_w) / 2
    c.restoreState()
    for cat in categories:
        c.saveState()
        c.setFont(fonts["bold"], 8)
        pw = c.stringWidth(cat, fonts["bold"], 8) + 20
        rounded_rect(c, pill_x, pill_y_center - pill_h/2, pw, pill_h, pill_r,
                     fill_color=GREEN_PILL, stroke_color=GREEN_DARK, stroke_width=0.8)
        c.setFillColor(GREEN_DARK)
        tw = c.stringWidth(cat, fonts["bold"], 8)
        c.drawString(pill_x + (pw - tw)/2, pill_y_center - 3, cat)
        c.restoreState()
        pill_x += pw + pill_gap
    draw_sep(CAT_BOT - GAP // 2)   # separator at midpoint of gap

    # ────────────────────────────────────────────────────────────────────────
    # WHAT YOU GET AS A PARENT  (2-column checkmark grid + social proof strip)
    # ────────────────────────────────────────────────────────────────────────
    sec_y = CLP_TOP - LPAD
    draw_spaced(c, "WHAT YOU GET AS A PARENT", MARGIN, sec_y, fonts["extrabold"], 7, color=LABEL_CLR)

    points = [
        ("Free forever",         "Full access, no subscription, no hidden costs"),
        ("Parent dashboard",     "See what your child practiced each day"),
        ("No ads, no data",      "Safe for kids — COPPA & GDPR compliant"),
        ("Mirror camera",        "Child sees themselves doing each exercise"),
        ("Daily reminders",      "App nudges practice — without you nagging"),
        ("Multi-child profiles", "Works for all your children in one app"),
        ("Voice instructions",   "Clear audio guides every exercise"),
        ("20 progressive levels","Keeps motivation high week after week"),
        ("Works offline",        "No wifi needed once installed"),
    ]

    col_w = (W - 2*MARGIN - 12) / 2
    row_h = 23
    start_y = sec_y - 16

    for i, (title, detail) in enumerate(points):
        col = i % 2
        row = i // 2
        px = MARGIN + col * (col_w + 12)
        py = start_y - row * row_h

        # Checkmark circle (drawn path)
        c.saveState()
        c.setFillColor(GREEN)
        c.circle(px + 6, py + 1, 6, fill=1, stroke=0)
        c.setStrokeColor(WHITE)
        c.setLineWidth(1.3)
        c.setLineCap(1)
        c.setLineJoin(1)
        p = c.beginPath()
        p.moveTo(px + 2.8, py + 1.2)
        p.lineTo(px + 5.2, py + 3.6)
        p.lineTo(px + 9.5, py - 1.5)
        c.drawPath(p, stroke=1, fill=0)
        c.restoreState()

        c.saveState()
        c.setFont(fonts["bold"], 8.5)
        c.setFillColor(BODY_TEXT)
        c.drawString(px + 16, py + 2, title)
        c.setFont(fonts["regular"], 7.5)
        c.setFillColor(MID_GRAY)
        c.drawString(px + 16, py - 7, detail)
        c.restoreState()

    # ── Social proof strip ───────────────────────────────────────────────────
    # Sits below the 9 items, fills remaining benefits space
    # Last item bottom ≈ start_y - 4*row_h - 10 = 524 - 70 - 10 = 444
    SP_TOP = int(start_y - 4 * row_h - 18)   # a little below last row
    SP_BOT = CLP_BOT + 6
    SP_H   = SP_TOP - SP_BOT

    rounded_rect(c, MARGIN, SP_BOT, W - 2*MARGIN, SP_H, 10,
                 fill_color=GREEN_PILL, stroke_color=GREEN_DARK, stroke_width=0.8)

    # Strip title
    strip_title_y = SP_BOT + SP_H - 17
    c.saveState()
    c.setFont(fonts["bold"], 9.5)
    c.setFillColor(GREEN_DARK)
    c.drawString(MARGIN + 14, strip_title_y, "Children stay motivated — because it feels like a game")
    c.restoreState()

    # Strip body
    strip_body = ("Grimasso uses the same motivation loop as children's favourite games: levels to beat, "
                  "badges to earn, and a character that celebrates every win. Kids who use Grimasso practise "
                  "more consistently and independently — making your home routine easier.")
    wrap_text(c, strip_body, MARGIN + 14, strip_title_y - 14,
              W - 2*MARGIN - 28, fonts["regular"], 8.5, 13, BODY_TEXT)

    # Three stat chips at the bottom of the strip
    stats = [("10", "game levels"), ("25+", "achievement badges"), ("100", "guided exercises")]
    chip_h = 22
    chip_y = SP_BOT + 10
    chip_gap = 10
    c.saveState()
    c.setFont(fonts["bold"], 8)
    total_chip_w = sum(c.stringWidth(f"{n}  {lbl}", fonts["bold"], 8) + 22 for n, lbl in stats) + chip_gap * (len(stats) - 1)
    chip_x = (W - total_chip_w) / 2
    c.restoreState()
    for num, lbl in stats:
        chip_label = f"{num}  {lbl}"
        c.saveState()
        c.setFont(fonts["bold"], 8)
        cw2 = c.stringWidth(chip_label, fonts["bold"], 8) + 22
        rounded_rect(c, chip_x, chip_y, cw2, chip_h, 11,
                     fill_color=GREEN_DARK)
        c.setFont(fonts["bold"], 8)
        c.setFillColor(WHITE)
        tw2 = c.stringWidth(chip_label, fonts["bold"], 8)
        c.drawString(chip_x + (cw2 - tw2) / 2, chip_y + 7, chip_label)
        c.restoreState()
        chip_x += cw2 + chip_gap

    draw_sep(CLP_BOT - GAP // 2)

    # ────────────────────────────────────────────────────────────────────────
    # GET STARTED IN 3 STEPS
    # ────────────────────────────────────────────────────────────────────────
    sec_y = HOW_TOP - LPAD
    draw_spaced(c, "GET STARTED IN 3 STEPS", MARGIN, sec_y, fonts["extrabold"], 7, color=LABEL_CLR)

    steps = [
        ("1", "Download Free",     "Search \"Grimasso\" on the\nApp Store — it takes\njust 30 seconds."),
        ("2", "Set Up Your Child", "Create a profile and\npick their exercise\nprogram in 2 minutes."),
        ("3", "Play Today",         "Do the first level\ntogether — it only\ntakes 5 minutes."),
    ]

    step_gap   = 10
    step_w     = (W - 2*MARGIN - step_gap * (len(steps) - 1)) / len(steps)
    step_h     = HOW_TOP - HOW_BOT - 28   # 8pt gap below label + 8pt bottom pad + LPAD(12)
    step_y_bot = HOW_BOT + 8

    BADGE_R = 10
    BODY_LH = 13
    BLOCK_H = BADGE_R * 2 + 8 + 3 * BODY_LH   # badge row + gap + 3 body lines = 67pt

    for i, (num, title, step_body) in enumerate(steps):
        sx      = MARGIN + i * (step_w + step_gap)
        card_cx = sx + step_w / 2
        card_cy = step_y_bot + step_h / 2

        rounded_rect(c, sx, step_y_bot, step_w, step_h, 8,
                     fill_color=GREEN_STEP, stroke_color=GREEN, stroke_width=1.0)

        # Content block — vertically centered in card, shifted 8pt down
        blk_top = card_cy + BLOCK_H / 2 - 6

        # Badge + title row — horizontally centered as a unit
        c.saveState()
        c.setFont(fonts["bold"], 9)
        title_w  = c.stringWidth(title, fonts["bold"], 9)
        row_w    = BADGE_R * 2 + 6 + title_w
        badge_cx = card_cx - row_w / 2 + BADGE_R
        title_x  = card_cx - row_w / 2 + BADGE_R * 2 + 6
        badge_cy = blk_top - BADGE_R

        c.setFillColor(GREEN)
        c.circle(badge_cx, badge_cy, BADGE_R, fill=1, stroke=0)
        c.setFont(fonts["extrabold"], 11)
        c.setFillColor(WHITE)
        nw = c.stringWidth(num, fonts["extrabold"], 11)
        c.drawString(badge_cx - nw / 2, badge_cy - 4, num)

        c.setFont(fonts["bold"], 9)
        c.setFillColor(BODY_TEXT)
        c.drawString(title_x, badge_cy - 3, title)
        c.restoreState()

        # Body lines — each line centered horizontally
        body_top = blk_top - BADGE_R * 2 - 8
        c.saveState()
        c.setFont(fonts["regular"], 8)
        c.setFillColor(MID_GRAY)
        for j, line in enumerate(step_body.split("\n")):
            lw = c.stringWidth(line, fonts["regular"], 8)
            c.drawString(card_cx - lw / 2, body_top - j * BODY_LH, line)
        c.restoreState()

    draw_sep(HOW_BOT - GAP // 2)

    # ────────────────────────────────────────────────────────────────────────
    # QR + CTA  — left-aligned; frog image fills right side
    # ────────────────────────────────────────────────────────────────────────
    APPSTORE_URL = "https://apps.apple.com/us/app/grimasso/id6758241652"
    QR_SIZE  = 82
    QR_SEC_H = QR_TOP - QR_BOT   # = 104pt

    # Frog image: full section height, right-aligned
    FROG_PATH = "/Users/lorenzmaierhofer/claude-projects/LogoApp/input/originals/FrogLevel_16.imageset/FrogLevel_16.png"
    frog_h    = QR_SEC_H * 1.10
    frog_w    = int(frog_h * (1076 / 976))
    frog_x    = W - MARGIN - frog_w
    frog_y    = QR_BOT
    c.drawImage(ImageReader(FROG_PATH), frog_x, frog_y,
                width=frog_w, height=frog_h, mask='auto')

    # QR + text left-aligned from MARGIN
    qr_card_x = MARGIN
    qr_x      = MARGIN + 4
    qr_y      = QR_BOT + (QR_SEC_H - QR_SIZE) / 2   # vertically centered

    # QR border card
    rounded_rect(c, qr_card_x, qr_y - 4, QR_SIZE + 8, QR_SIZE + 8, 6,
                 fill_color=WHITE, stroke_color=GREEN, stroke_width=1.2)
    c.drawImage(qr_img, qr_x, qr_y, width=QR_SIZE, height=QR_SIZE)

    # Text column — immediately right of QR card
    btn_w     = 180
    cta_x     = MARGIN + (QR_SIZE + 8) + 18
    cta_top_y = qr_y + QR_SIZE + 4

    c.saveState()
    c.setFont(fonts["extrabold"], 15)
    c.setFillColor(GREEN_DARK)
    c.drawString(cta_x, cta_top_y - 15, "Download Free Today")
    c.restoreState()

    c.saveState()
    c.setFont(fonts["regular"], 8.5)
    c.setFillColor(MID_GRAY)
    wrap_text(c, "Search \"Grimasso\" or scan the QR code with your iPhone camera.",
              cta_x, cta_top_y - 31, btn_w, fonts["regular"], 8.5, 13, MID_GRAY)
    c.restoreState()

    # App Store button — pinned to QR card bottom
    btn_h = 27
    btn_x = cta_x
    btn_y = qr_y + 4
    rounded_rect(c, btn_x, btn_y, btn_w, btn_h, 13, fill_color=GREEN_DARK)
    c.saveState()
    c.setFont(fonts["bold"], 9.5)
    c.setFillColor(WHITE)
    lbl = "Download on the App Store"
    lw  = c.stringWidth(lbl, fonts["bold"], 9.5)
    c.drawString(btn_x + (btn_w - lw) / 2, btn_y + 9, lbl)
    c.restoreState()
    c.linkURL(APPSTORE_URL, (btn_x, btn_y, btn_x + btn_w, btn_y + btn_h))

    # ────────────────────────────────────────────────────────────────────────
    # CONTACT NOTE  (y ≈ 36)
    # ────────────────────────────────────────────────────────────────────────
    c.saveState()
    c.setFont(fonts["regular"], 7.5)
    c.setFillColor(MID_GRAY)
    contact_text = "Questions? grimasso@lorenzmaierhofer.com"
    cw = c.stringWidth(contact_text, fonts["regular"], 7.5)
    c.drawString((W - cw) / 2, 36, contact_text)
    c.restoreState()

    # ────────────────────────────────────────────────────────────────────────
    # FOOTER BAND  (anchored to y=0)
    # ────────────────────────────────────────────────────────────────────────
    FOOTER_H = 28
    FOOTER_Y = 0

    c.setFillColor(GREEN_DARK)
    c.rect(0, FOOTER_Y, W, FOOTER_H, fill=1, stroke=0)

    c.saveState()
    c.setFont(fonts["bold"], 8.5)
    c.setFillColor(WHITE)
    footer_text = "lorenzmaierhofer.com/grimasso  ·  Learn more about the app"
    ftw = c.stringWidth(footer_text, fonts["bold"], 8.5)
    c.drawString((W - ftw) / 2, FOOTER_Y + 9, footer_text)
    c.restoreState()

    # ────────────────────────────────────────────────────────────────────────

    # ────────────────────────────────────────────────────────────────────────
    c.save()
    print(f"\n  PDF saved → {OUTPUT_PATH}")


if __name__ == "__main__":
    print("Grimasso Referral Kit Generator")
    print("================================")
    print("Loading fonts…")
    fonts = load_fonts()
    print("Generating PDF…")
    generate(fonts)
    size = os.path.getsize(OUTPUT_PATH) // 1024
    print(f"  File size: {size} KB")
    print("Done.")
