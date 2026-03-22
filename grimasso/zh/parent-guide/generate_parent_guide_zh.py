#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Grimasso ZH Parent Guide PDF — Professional Layout v3
All Chinese text written as UTF-8 literals (no \\u escapes) to avoid encoding errors.
Uses Arial Unicode for body text (full CJK coverage) and STHeiti Medium for bold.
"""

import io, os
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

SCRIPT_DIR  = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PATH = os.path.join(SCRIPT_DIR, "grimasso-english-guide-zh.pdf")
MASCOT_PATH = "/Users/lorenzmaierhofer/claude-projects/LogoApp/input/Grimasso_Images/Grimasso_Main.png"

# ── Palette ───────────────────────────────────────────────────────────────────
RED       = colors.HexColor("#E53935")
RED_DARK  = colors.HexColor("#B71C1C")
RED_MED   = colors.HexColor("#C62828")
GOLD      = colors.HexColor("#FFD700")
GOLD_DARK = colors.HexColor("#F9A825")
WHITE     = colors.white
OFF_WHITE = colors.HexColor("#FFF8F0")
BORDER    = colors.HexColor("#EDCFB0")
TEXT      = colors.HexColor("#1C1C1E")
TEXT_SUB  = colors.HexColor("#5A5A5A")
GREEN     = colors.HexColor("#34C759")
LIGHT_RED = colors.HexColor("#FFF0EF")
LIGHT_RED_BORDER = colors.HexColor("#F5C2BE")


# ── Fonts ─────────────────────────────────────────────────────────────────────
def load_fonts():
    # Arial Unicode: full CJK coverage (body text)
    pdfmetrics.registerFont(TTFont("AU",   "/Library/Fonts/Arial Unicode.ttf"))
    # STHeiti: for bold titles (common characters only)
    pdfmetrics.registerFont(TTFont("ZH-B", "/System/Library/Fonts/STHeiti Medium.ttc"))
    return {"r": "AU", "b": "ZH-B"}


# ── Drawing helpers ───────────────────────────────────────────────────────────
def rr(c, x, y, w, h, r, fill=None, stroke=None, sw=1):
    """Rounded rectangle. y = bottom-left."""
    p = c.beginPath()
    p.moveTo(x+r, y);           p.lineTo(x+w-r, y)
    p.arcTo(x+w-2*r, y,         x+w, y+2*r,      startAng=-90, extent=90)
    p.lineTo(x+w, y+h-r)
    p.arcTo(x+w-2*r, y+h-2*r,  x+w, y+h,         startAng=0,   extent=90)
    p.lineTo(x+r, y+h)
    p.arcTo(x, y+h-2*r,         x+2*r, y+h,       startAng=90,  extent=90)
    p.lineTo(x, y+r)
    p.arcTo(x, y,                x+2*r, y+2*r,     startAng=180, extent=90)
    p.close()
    c.saveState()
    if fill:   c.setFillColor(fill)
    if stroke: c.setStrokeColor(stroke); c.setLineWidth(sw)
    c.drawPath(p, fill=1 if fill else 0, stroke=1 if stroke else 0)
    c.restoreState()


def draw_check(c, cx, cy, size=5.5):
    c.saveState()
    c.setFillColor(GREEN)
    c.circle(cx, cy, size, fill=1, stroke=0)
    c.setStrokeColor(WHITE); c.setLineWidth(1.1); c.setLineCap(1); c.setLineJoin(1)
    p = c.beginPath()
    p.moveTo(cx - size*0.45, cy)
    p.lineTo(cx - size*0.05, cy - size*0.38)
    p.lineTo(cx + size*0.55, cy + size*0.42)
    c.drawPath(p, stroke=1, fill=0)
    c.restoreState()


def draw_cross(c, cx, cy, size=5.5):
    c.saveState()
    c.setFillColor(RED)
    c.circle(cx, cy, size, fill=1, stroke=0)
    c.setStrokeColor(WHITE); c.setLineWidth(1.2); c.setLineCap(1)
    d = size * 0.42
    for pts in [[(cx-d, cy-d),(cx+d, cy+d)], [(cx+d, cy-d),(cx-d, cy+d)]]:
        p = c.beginPath()
        p.moveTo(*pts[0]); p.lineTo(*pts[1])
        c.drawPath(p, stroke=1, fill=0)
    c.restoreState()


def draw_bullet(c, cx, cy, size=4, color=GOLD):
    """Small filled circle bullet for benefit cards."""
    c.saveState()
    c.setFillColor(color)
    c.circle(cx, cy, size, fill=1, stroke=0)
    c.restoreState()


def sec_title(c, f, x, y, text, size=11.5):
    """Section heading with gold left bar."""
    c.saveState()
    c.setFillColor(GOLD)
    c.rect(x, y - size + 2, 3.5, size + 4, fill=1, stroke=0)
    c.setFont(f["b"], size); c.setFillColor(RED_DARK)
    c.drawString(x + 9, y, text)
    c.restoreState()


def wrap_cjk(c, text, x, y, max_w, font, size, lh, color=TEXT_SUB):
    """Character-level wrap for CJK text. Returns y after last line."""
    c.saveState()
    c.setFont(font, size); c.setFillColor(color)
    line = ""
    for ch in text:
        test = line + ch
        if c.stringWidth(test, font, size) <= max_w:
            line = test
        else:
            c.drawString(x, y, line)
            y -= lh
            line = ch
    if line:
        c.drawString(x, y, line)
        y -= lh
    c.restoreState()
    return y


# ── Generator ─────────────────────────────────────────────────────────────────
def generate(f):
    W, H = A4        # 595.28 × 841.89 pt
    ML   = 34        # left / right margin
    CW   = W - 2*ML  # content width ≈ 527 pt

    c = canvas.Canvas(OUTPUT_PATH, pagesize=A4)
    c.setTitle("Grimasso — 帮孩子说一口地道英语")
    c.setAuthor("Lorenz Maierhofer")

    # ── QR code ───────────────────────────────────────────────────────────
    qr_img = None
    try:
        import qrcode
        from qrcode.constants import ERROR_CORRECT_H
        qr = qrcode.QRCode(version=None, error_correction=ERROR_CORRECT_H,
                           box_size=10, border=2)
        qr.add_data("https://apps.apple.com/us/app/grimasso/id6758241652")
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        buf = io.BytesIO(); img.save(buf, "PNG"); buf.seek(0)
        qr_img = ImageReader(buf)
        print("  QR code generated")
    except Exception as e:
        print(f"  QR error: {e}")

    # ═══════════════════════════════════════════════════════════════════════
    # 1. HEADER
    # ═══════════════════════════════════════════════════════════════════════
    HDR_H = 118
    HDR_Y = H - HDR_H   # = 723.89

    # Dark red base + slightly lighter left zone
    c.setFillColor(RED_DARK)
    c.rect(0, HDR_Y, W, HDR_H, fill=1, stroke=0)
    c.saveState()
    c.setFillColor(RED_MED)
    c.rect(0, HDR_Y, W * 0.60, HDR_H, fill=1, stroke=0)
    c.restoreState()

    # Mascot image — right side, slight overflow above header
    MASC_W = 132
    MASC_H = int(MASC_W * (1034 / 1142))
    if os.path.exists(MASCOT_PATH):
        c.drawImage(ImageReader(MASCOT_PATH),
                    W - ML - MASC_W + 10, HDR_Y - 6,
                    width=MASC_W, height=MASC_H, mask="auto")

    # Badge pill — top right corner
    badge = "★  App Store 免费下载"
    c.saveState()
    c.setFont(f["b"], 7)
    bw = c.stringWidth(badge, f["b"], 7) + 18
    rr(c, W - ML - bw, H - 22, bw, 16, 8, fill=GOLD)
    c.setFillColor(RED_DARK)
    tw = c.stringWidth(badge, f["b"], 7)
    c.drawString(W - ML - bw + (bw - tw) / 2, H - 17, badge)
    c.restoreState()

    # Logo
    c.saveState()
    c.setFont(f["b"], 30); c.setFillColor(GOLD)
    c.drawString(ML, H - 50, "Grimasso")
    c.restoreState()

    # Tagline
    c.saveState()
    c.setFont(f["b"], 14.5); c.setFillColor(WHITE)
    c.drawString(ML, H - 74, "帮孩子说一口地道英语")
    c.restoreState()

    # Thin divider
    c.saveState()
    c.setStrokeColor(colors.HexColor("#E8896A")); c.setLineWidth(0.8)
    c.line(ML, H - 84, ML + CW * 0.54, H - 84)
    c.restoreState()

    # Subtitle line
    c.saveState()
    c.setFont(f["r"], 7.5); c.setFillColor(colors.HexColor("#FFD4CC"))
    c.drawString(ML, H - 98, "口腔肌肉训练 × 游戏化学习 × 科学方法 —— 专为普通话家庭设计的英语发音解决方案")
    c.restoreState()

    y = HDR_Y - 20   # cursor just below header

    # ═══════════════════════════════════════════════════════════════════════
    # 2. SECTION 1 — Why is English pronunciation hard?
    # ═══════════════════════════════════════════════════════════════════════
    sec_title(c, f, ML, y, "为什么英语发音这么难？")
    y -= 17

    # Intro sentence
    c.saveState()
    c.setFont(f["r"], 8.5); c.setFillColor(TEXT_SUB)
    c.drawString(ML, y,
        '中文普通话中没有英语的几个核心音素。这些音不是\u201c听多了就会\u201d\u2014\u2014它们需要孩子的口腔肌肉学会新的动作模式。')
    c.restoreState()
    y -= 18

    # ── Phoneme table ──────────────────────────────────────────────────────
    COL   = [42, 118, 38, 50, CW - 42 - 118 - 38 - 50]
    ROW_H = 18
    hdrs  = ["英语音素", "例词", "英语中", "普通话中", "所需动作"]
    rows  = [
        ("/r/",  "rabbit, red, run",   "舌头中部隆起，不碰上颚"),
        ("/l/",  "light, love, blue",  "舌尖顶上齿龈，侧面出气"),
        ("/th/", "the, think, that",   "舌尖轻咬上齿，气流摩擦"),
        ("/v/",  "very, voice, live",  "上齿轻触下唇，振动发声"),
    ]

    # Header row (dark red bg, white text)
    c.saveState()
    c.setFillColor(RED_DARK)
    c.rect(ML, y - ROW_H, CW, ROW_H, fill=1, stroke=0)
    c.setFont(f["b"], 7.5); c.setFillColor(WHITE)
    cx = ML
    for i, h in enumerate(hdrs):
        c.drawString(cx + 5, y - ROW_H + 6, h)
        cx += COL[i]
    c.restoreState()
    y -= ROW_H

    # Data rows
    for ri, (ph, ex, action) in enumerate(rows):
        row_y = y - ROW_H
        bg = OFF_WHITE if ri % 2 == 0 else WHITE
        c.saveState()
        c.setFillColor(bg)
        c.rect(ML, row_y, CW, ROW_H, fill=1, stroke=0)
        c.setStrokeColor(BORDER); c.setLineWidth(0.4)
        c.line(ML, row_y, ML + CW, row_y)
        cx = ML
        # Phoneme symbol
        c.setFont(f["b"], 9.5); c.setFillColor(RED_DARK)
        c.drawString(cx + 5, row_y + 6, ph);  cx += COL[0]
        # Example words
        c.setFont(f["r"], 7.5); c.setFillColor(TEXT_SUB)
        c.drawString(cx + 5, row_y + 6, ex);  cx += COL[1]
        # Check / Cross drawn symbols
        sym_cy = row_y + ROW_H / 2
        draw_check(c, cx + COL[2] / 2, sym_cy); cx += COL[2]
        draw_cross(c, cx + COL[3] / 2, sym_cy); cx += COL[3]
        # Action description
        c.setFont(f["r"], 7.5); c.setFillColor(TEXT)
        c.drawString(cx + 5, row_y + 6, action)
        c.restoreState()
        y -= ROW_H

    y -= 10

    # ── Insight box ────────────────────────────────────────────────────────
    IB_H = 52
    rr(c, ML, y - IB_H, CW, IB_H, 6, fill=LIGHT_RED, stroke=LIGHT_RED_BORDER, sw=0.8)
    c.saveState()
    c.setFont(f["b"], 8); c.setFillColor(RED_DARK)
    c.drawString(ML + 10, y - 13, "关键洞察：")
    c.setFont(f["r"], 8); c.setFillColor(TEXT)
    c.drawString(ML + 10, y - 26,
        '这些音不是发音\u201c技巧\u201d问题，而是肌肉记忆问题。就像学钢琴需要手指练习，学英语发音同样需要口腔肌肉专项训练。')
    c.drawString(ML + 10, y - 39,
        "语言习得研究表明，越早开始训练，肌肉适应性越强，效果越持久。")
    c.restoreState()
    y -= IB_H + 18

    # ═══════════════════════════════════════════════════════════════════════
    # 3. SECTION 2 — Science
    # ═══════════════════════════════════════════════════════════════════════
    sec_title(c, f, ML, y, "科学发现：口腔肌肉训练是关键")
    y -= 14

    # Stat cards
    CARD_H  = 62
    CARD_W  = (CW - 16) / 3
    stats   = [
        ("100",  "个专业练习",      "5大训练类别"),
        ("4–6",  "周后家长和老师",   "开始注意到进步"),
        ("10",   "分钟 / 天",       "轻松坚持"),
    ]
    for i, (num, lbl1, lbl2) in enumerate(stats):
        cx = ML + i * (CARD_W + 8)
        cy = y - CARD_H
        rr(c, cx, cy, CARD_W, CARD_H, 8, fill=OFF_WHITE, stroke=BORDER, sw=1)
        # Gold top accent bar
        rr(c, cx, cy + CARD_H - 5, CARD_W, 5, 4, fill=GOLD)
        c.saveState()
        c.setFont(f["b"], 21); c.setFillColor(GOLD_DARK)
        nw = c.stringWidth(num, f["b"], 21)
        c.drawString(cx + (CARD_W - nw) / 2, cy + CARD_H - 28, num)
        c.setFont(f["b"], 7.5); c.setFillColor(RED_DARK)
        lw = c.stringWidth(lbl1, f["b"], 7.5)
        c.drawString(cx + (CARD_W - lw) / 2, cy + CARD_H - 43, lbl1)
        c.setFont(f["r"], 7); c.setFillColor(TEXT_SUB)
        lw = c.stringWidth(lbl2, f["r"], 7)
        c.drawString(cx + (CARD_W - lw) / 2, cy + CARD_H - 55, lbl2)
        c.restoreState()
    y -= CARD_H + 10

    # Science body — character-level wrap so it doesn't truncate
    sci = ("Grimasso基于口腔肌肉功能治疗（OMT）原理设计，这是言语语言病理学家广泛采用的循证治疗方案。"
           "通过专项训练舌尖位置、舌头力量、下颌协调和嘴唇控制，孩子的口腔肌肉逐步建立发英语音所需的新模式。"
           "游戏化设计确保孩子每天愿意坚持——而坚持性正是训练效果的最重要预测指标。")
    y = wrap_cjk(c, sci, ML, y, CW, f["r"], 8, 13.5, TEXT_SUB)
    y -= 16

    # ═══════════════════════════════════════════════════════════════════════
    # 4. SECTION 3 — 4 Benefits
    # ═══════════════════════════════════════════════════════════════════════
    sec_title(c, f, ML, y, "孩子的4大收获")
    y -= 14

    benefits = [
        ("英语发音更标准",
         "/r/、/l/、/th/、/v/ 等难发音逐步改善",
         "老师和同学都能听出进步"),
        ("自信开口说英语",
         "发音更准确，课堂发言不再羞于开口",
         "自信心显著提升"),
        ("在学校脱颖而出",
         "英语口语成绩提升，演讲或",
         "朗读比赛中表现更出色"),
        ("爸爸妈妈都放心",
         "无广告、无追踪、PIN码保护的",
         "家长控制台——安全可信赖"),
    ]

    B_W = (CW - 10) / 2
    B_H = 52
    for i, (title, d1, d2) in enumerate(benefits):
        col = i % 2;  row = i // 2
        bx = ML + col * (B_W + 10)
        by = y - row * (B_H + 8) - B_H
        rr(c, bx, by, B_W, B_H, 8, fill=OFF_WHITE, stroke=BORDER, sw=1)
        # Gold left accent stripe
        c.saveState()
        c.setFillColor(GOLD)
        c.rect(bx, by + 8, 4, B_H - 16, fill=1, stroke=0)
        # Title
        c.setFont(f["b"], 9); c.setFillColor(RED_DARK)
        c.drawString(bx + 14, by + B_H - 17, title)
        # Detail lines
        c.setFont(f["r"], 7.5); c.setFillColor(TEXT_SUB)
        c.drawString(bx + 14, by + B_H - 30, d1)
        c.drawString(bx + 14, by + B_H - 42, d2)
        c.restoreState()

    y -= 2 * (B_H + 8) + 10

    # ═══════════════════════════════════════════════════════════════════════
    # 5. CTA SECTION
    # ═══════════════════════════════════════════════════════════════════════
    CTA_H = 108
    CTA_Y = y - CTA_H
    rr(c, ML - 4, CTA_Y, CW + 8, CTA_H, 10, fill=RED_DARK)

    # QR code block — right side, vertically centred
    QR_SIZE  = 70
    QR_PAD   = 5
    qr_block = QR_SIZE + 2 * QR_PAD
    qr_x_box = ML - 4 + CW + 8 - 16 - qr_block   # box left edge
    qr_y_box = CTA_Y + (CTA_H - qr_block - 16) / 2 + 12
    rr(c, qr_x_box, qr_y_box, qr_block, qr_block, 6,
       fill=WHITE, stroke=GOLD, sw=2.5)
    if qr_img:
        c.drawImage(qr_img, qr_x_box + QR_PAD, qr_y_box + QR_PAD,
                    width=QR_SIZE, height=QR_SIZE)
    # Label below QR card
    c.saveState()
    c.setFont(f["r"], 6.5); c.setFillColor(GOLD)
    lbl = "扫码下载 · App Store · 免费"
    lw  = c.stringWidth(lbl, f["r"], 6.5)
    c.drawString(qr_x_box + (qr_block - lw) / 2, qr_y_box - 12, lbl)
    c.restoreState()

    # CTA text column — left of QR
    TX   = ML + 10
    TW   = qr_x_box - TX - 10
    # Title
    c.saveState()
    c.setFont(f["b"], 15); c.setFillColor(GOLD)
    c.drawString(TX, CTA_Y + CTA_H - 24, "立即免费下载 Grimasso")
    # Body lines
    c.setFont(f["r"], 8.5); c.setFillColor(WHITE)
    cta_body = [
        "每天 10 分钟，轻松开始训练。",
        "全部 100 个练习完全免费，无需订阅，无广告。",
        "适用于 iPhone 和 iPad。",
    ]
    for i, line in enumerate(cta_body):
        c.drawString(TX, CTA_Y + CTA_H - 42 - i * 14, line)
    c.restoreState()

    # App Store search pill — anchored just above CTA bottom
    pill = '在 App Store 搜索\u201cGrimasso\u201d'
    c.saveState()
    c.setFont(f["b"], 8)
    pw = c.stringWidth(pill, f["b"], 8) + 24; ph = 22
    px = TX; py = CTA_Y + 12
    rr(c, px, py, pw, ph, 11, fill=WHITE)
    c.setFillColor(RED_DARK)
    tw = c.stringWidth(pill, f["b"], 8)
    c.drawString(px + (pw - tw) / 2, py + 7, pill)
    c.restoreState()

    y -= CTA_H + 16

    # ═══════════════════════════════════════════════════════════════════════
    # 6. FOOTER
    # ═══════════════════════════════════════════════════════════════════════
    c.saveState()
    c.setStrokeColor(BORDER); c.setLineWidth(0.8)
    c.line(ML, y, ML + CW, y)
    y -= 13
    c.setFont(f["r"], 6.5); c.setFillColor(colors.HexColor("#999999"))
    left  = "Grimasso — 口腔肌肉训练应用"
    mid   = "grimasso.lorenzmaierhofer.com/zh/"
    right = "隐私政策 · 无广告 · 免费"
    c.drawString(ML, y, left)
    mw = c.stringWidth(mid, f["r"], 6.5)
    c.drawString((W - mw) / 2, y, mid)
    rw = c.stringWidth(right, f["r"], 6.5)
    c.drawString(ML + CW - rw, y, right)
    c.restoreState()

    c.save()
    print(f"  PDF saved → {OUTPUT_PATH}")


if __name__ == "__main__":
    print("Grimasso ZH Parent Guide Generator — v3")
    print("=========================================")
    f = load_fonts()
    generate(f)
    kb = os.path.getsize(OUTPUT_PATH) // 1024
    print(f"  File size: {kb} KB\nDone.")
