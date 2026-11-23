#!/usr/bin/env python3
"""Render entry.png: one image summing up Monday 23 November 2026 world news.

Dense broadsheet, 1024x1024, deterministic (fixed layout, fixed fonts, no
randomness, no wall clock, no network). Run: python3 draw_image.py
Writes entry.png next to this file. Local renderer only -- the grader runs
main.py, which copies the shipped entry.png (stdlib only, no PIL).
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
OUT = "entry.png"

PAPER = (246, 241, 231)
INK = (22, 22, 26)
MUTED = (90, 86, 78)
NAVY = (16, 24, 40)
NAVY2 = (20, 33, 61)
GOLD = (201, 162, 39)
GREEN = (14, 124, 58)
RED = (183, 28, 28)
AMBER = (178, 106, 0)
BLUE = (21, 101, 192)
PANEL_BG = (255, 255, 255)
PANEL_LINE = (216, 210, 196)
MAP_BG = (20, 33, 61)
MAP_LAND = (143, 168, 163)
MARKER = (215, 38, 61)
WHITE = (255, 255, 255)
CREAM = (246, 241, 231)


def font(size, bold=False):
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    return ImageFont.truetype(FONT_DIR + name, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, text, fnt, fill, max_w, leading=None):
    """Draw wrapped text; returns the y just below the last line."""
    if leading is None:
        leading = int(fnt.size * 1.25)
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


# ---------------------------------------------------------------- data

HERO = {
    "label": "US STOCKS SOAR",
    "sub": "Nvidia +31% \u2014 Huang returns as CEO",
    "bars": [("NVDA", 31.5), ("NASDAQ", 6.5), ("S&P 500", 4.7), ("DOW", 3.0)],
    "detail": "S&P snaps 7-day slide \u00b7 Nasdaq best since Apr 2025 \u00b7 NVDA +$952bn record",
}

# Grid panels 2..7 (1 is the hero, New York, on the map).
PANELS = [
    {"n": 2, "label": "SAUDI STRIKE HITS HODEIDA",
     "sub": "Houthi media: telecoms building hit",
     "detail": "Riyadh silent; toll claims conflict \u2014 no figures shown.",
     "source": "AP \u00b7 AFP", "tag": "CLAIM"},
    {"n": 3, "label": "MERKURY SUNK IN LIBYA",
     "sub": "Zelenskyy confirms \u2014 7 sea drones",
     "detail": "Attack Sun, announced Mon. Corvette sunk at Benghazi; satellite image shows it under.",
     "source": "SBU \u00b7 Zelenskyy", "tag": "REPORTED"},
    {"n": 4, "label": "KYIV DRONES AGAIN",
     "sub": "153 launched \u2014 debris hits schools",
     "detail": "134 neutralised; debris on a warehouse and two school grounds. No casualties in the capital.",
     "source": "Ukrainian officials", "tag": "REPORTED"},
    {"n": 5, "label": "BELGIUM GROUNDS FLIGHTS",
     "sub": "Airports shut \u2014 austerity strike",
     "detail": "Brussels Airport shut 07:00\u201321:00; Charleroi all day. ~60,000 passengers hit.",
     "source": "Belgian media", "tag": "REPORTED"},
    {"n": 6, "label": "INDIA GIVES NEPAL $1.62BN",
     "sub": "Modi\u2013Shah talks \u2014 flood aid pact",
     "detail": "$1.62bn package; Joint Vision adopted; Saryu-Kamala Express flagged off.",
     "source": "Govt of India \u00b7 Nepal", "tag": "REPORTED"},
    {"n": 7, "label": "EU PROPOSES 22ND SANCTIONS",
     "sub": "60 banks off SWIFT \u2014 crypto hit",
     "detail": "Crypto crackdown, shadow-fleet ships listed. Needs unanimity \u2014 a proposal, not a deal.",
     "source": "Reuters \u00b7 EC", "tag": "PROPOSAL"},
]

TAG_COLORS = {"REPORTED": GREEN, "CLAIM": AMBER, "PROPOSAL": BLUE}

STATS = [
    ("153", "DRONES OVER KYIV"),
    ("60", "BANKS OFF SWIFT"),
    ("$1.62BN", "NEPAL AID"),
    ("KOSPI \u22123.3%", "ASIA MONDAY"),
    ("TAIEX +2.4%", "ASIA REBOUND"),
    ("11 DAYS", "HUANG OUT, BACK"),
]

MORE_A = [
    "NATO: space is covered \u2014 Rutte vows defence (Berlin)",
    "Gaza a \u2018toxic wasteland\u2019 \u2014 Oxfam: >99% contaminated",
    "Shuri Castle reopens \u2014 main hall open, 7 yrs after fire",
    "Korea exports surge \u2014 Nov 1\u201320: $77.4bn, +101.5%",
    "Banten: search goes on after factory fire (Sat)",
    "India\u2013NZ Test ends in a draw",
]
MORE_B = [
    "Iran: \u2018all available means\u2019 vs US blockade",
    "Dow +1,448 to 49,595 \u00b7 S&P 7,237 \u00b7 Nasdaq 24,090",
    "NATO assembly in Berlin \u2014 Zelenskyy by video",
    "Huang back 11 days after resigning; board had said no",
    "EU: energy ban covers electricity; 70+ ships listed",
    "Japan closed Mon (holiday) \u2014 no Nikkei shown",
]

# Simplified continent blobs (map-local coords, map area 368 x 150).
CONTINENTS = [
    [(15, 25), (40, 12), (70, 15), (85, 25), (80, 45), (60, 60),
     (45, 75), (25, 65), (12, 45)],
    [(75, 82), (95, 80), (105, 95), (100, 120), (90, 140), (80, 130),
     (72, 105)],
    [(175, 30), (195, 18), (210, 25), (205, 45), (190, 55), (178, 45)],
    [(175, 62), (200, 58), (218, 70), (215, 95), (200, 118), (185, 112),
     (172, 85)],
    [(215, 25), (250, 12), (300, 15), (340, 25), (335, 50), (310, 70),
     (270, 75), (235, 60), (215, 45)],
    [(295, 120), (320, 115), (332, 125), (325, 138), (300, 138)],
]
# (number, x, y) markers on the same map coords.
MARKERS = [
    (1, 55, 45),    # New York (hero)
    (2, 232, 85),   # Hodeida
    (3, 196, 72),   # Benghazi
    (4, 212, 30),   # Kyiv
    (5, 180, 26),   # Brussels (Belgium)
    (6, 275, 55),   # Kathmandu
    (7, 192, 44),   # Brussels (EU)
]


def draw_tag(draw, x, y, tag):
    """Small certainty chip; returns its width."""
    f = font(11, bold=True)
    w = int(draw.textlength(tag, font=f)) + 14
    draw.rounded_rectangle([x, y, x + w, y + 20], radius=4,
                           fill=TAG_COLORS[tag])
    draw.text((x + 7, y + 3), tag, font=f, fill=WHITE)
    return w


def draw_panel(draw, x, y, w, h, p):
    draw.rectangle([x, y, x + w, y + h], fill=PANEL_BG, outline=PANEL_LINE,
                   width=1)
    draw.rectangle([x, y, x + w, y + 5], fill=NAVY)
    # Number badge.
    draw.ellipse([x + 10, y + 14, x + 32, y + 36], fill=MARKER)
    nf = font(13, bold=True)
    num = str(p["n"])
    draw.text((x + 21 - draw.textlength(num, font=nf) / 2, y + 17), num,
              font=nf, fill=WHITE)
    lx = x + 40
    lw = w - 50
    ly = y + 12
    ly = text_block(draw, lx, ly, p["label"], font(20, bold=True), INK, lw,
                    leading=24)
    ly = text_block(draw, lx, ly + 2, p["sub"], font(14, bold=True), RED, lw,
                    leading=18)
    ly = text_block(draw, x + 10, ly + 4, p["detail"], font(13), INK, w - 20,
                    leading=17)
    sf = font(11)
    draw.text((x + 10, y + h - 20), "Source: " + p["source"], font=sf,
              fill=MUTED)
    draw_tag(draw, x + w - 96, y + h - 22, p["tag"])


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- Masthead -------------------------------------------------------
    d.rectangle([0, 0, W, 84], fill=NAVY)
    d.text((16, 18), "THE WORLD IN ONE DAY", font=font(40, bold=True),
           fill=WHITE)
    date = "MONDAY 23 NOVEMBER 2026"
    df = font(26, bold=True)
    d.text((W - 16 - d.textlength(date, font=df), 26), date, font=df,
           fill=GOLD)
    d.rectangle([0, 84, W, 88], fill=GOLD)

    # ---- Hero row -------------------------------------------------------
    hy, hh = 96, 188
    hx, hw = 16, 608
    d.rectangle([hx, hy, hx + hw, hy + hh], fill=PANEL_BG,
                outline=PANEL_LINE, width=1)
    d.rectangle([hx, hy, hx + hw, hy + 5], fill=GREEN)
    # Hero number badge.
    d.ellipse([hx + 12, hy + 14, hx + 36, hy + 38], fill=MARKER)
    nf = font(14, bold=True)
    d.text((hx + 24 - d.textlength("1", font=nf) / 2, hy + 17), "1",
           font=nf, fill=WHITE)
    tx = hx + 46
    d.text((tx, hy + 8), HERO["label"], font=font(48, bold=True), fill=INK)
    d.text((tx, hy + 64), HERO["sub"], font=font(21, bold=True), fill=GREEN)
    # Horizontal bars.
    bx, by = tx, hy + 96
    bw = 420
    maxv = 31.5
    for name, val in HERO["bars"]:
        d.text((bx, by), name, font=font(12, bold=True), fill=INK)
        bar_x = bx + 78
        bar_w = int(bw * val / maxv)
        d.rectangle([bar_x, by + 1, bar_x + bar_w, by + 13], fill=GREEN)
        d.text((bar_x + bar_w + 6, by),
               "+%.1f%%" % val, font=font(12, bold=True), fill=INK)
        by += 16
    text_block(d, tx, hy + 164, HERO["detail"], font(12), MUTED, hw - 58,
               leading=15)

    # ---- World map panel ------------------------------------------------
    mx, my, mw, mh = 640, 96, 368, 188
    d.rectangle([mx, my, mx + mw, my + mh], fill=MAP_BG)
    d.text((mx + 12, my + 8), "WHERE IT HAPPENED",
           font=font(14, bold=True), fill=GOLD)
    map_ox, map_oy = mx, my + 28
    map_sy = 0.86
    for poly in CONTINENTS:
        pts = [(map_ox + px, map_oy + py * map_sy) for px, py in poly]
        d.polygon(pts, fill=MAP_LAND)
    mf = font(11, bold=True)
    for num, px, py in MARKERS:
        cx, cy = map_ox + px, map_oy + py * map_sy
        d.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=MARKER,
                  outline=WHITE, width=1)
        s = str(num)
        d.text((cx - d.textlength(s, font=mf) / 2, cy - 7), s, font=mf,
               fill=WHITE)
    kf = font(11)
    d.text((mx + 12, my + 152),
           "1 New York \u00b7 2 Hodeida \u00b7 3 Benghazi \u00b7 4 Kyiv",
           font=kf, fill=(200, 205, 215))
    d.text((mx + 12, my + 166),
           "5 Brussels \u00b7 6 Kathmandu \u00b7 7 Brussels (EU)",
           font=kf, fill=(200, 205, 215))

    # ---- Big-numbers strip ----------------------------------------------
    sy, sh = 292, 40
    d.rectangle([16, sy, W - 16, sy + sh], fill=NAVY)
    cell_w = (W - 32) // len(STATS)
    for i, (val, lab) in enumerate(STATS):
        cx = 16 + i * cell_w
        vf = font(20, bold=True)
        d.text((cx + 10, sy + 4), val, font=vf, fill=GOLD)
        lf = font(10, bold=True)
        d.text((cx + 10, sy + 26), lab, font=lf, fill=(200, 205, 215))
        if i:
            d.line([cx, sy + 6, cx, sy + sh - 6], fill=(60, 70, 95), width=1)

    # ---- Grid 2x3 --------------------------------------------------------
    gx, gy = 16, 340
    cw, chh, gap = 320, 164, 8
    for i, p in enumerate(PANELS):
        col, row = i % 3, i // 3
        draw_panel(d, gx + col * (cw + gap), gy + row * (chh + gap),
                   cw, chh, p)

    # ---- More from Monday -------------------------------------------------
    my2 = 682
    d.text((16, my2), "MORE FROM MONDAY \u2014 23 NOV",
           font=font(14, bold=True), fill=INK)
    d.line([16, my2 + 22, W - 16, my2 + 22], fill=INK, width=1)
    col_w = 480
    bf = font(12)
    for col, items in enumerate((MORE_A, MORE_B)):
        x = 16 + col * (col_w + 16)
        y = my2 + 30
        for it in items:
            d.text((x, y), "\u2022", font=bf, fill=RED)
            y = text_block(d, x + 14, y, it, bf, INK, col_w - 14,
                           leading=15)
            y += 1

    # ---- Bottom: DATE CHECK + legend --------------------------------------
    by2 = 820
    # DATE CHECK box (left).
    d.rectangle([16, by2, 600, 1008], fill=PANEL_BG, outline=PANEL_LINE,
                width=1)
    d.rectangle([16, by2, 600, by2 + 5], fill=RED)
    d.text((28, by2 + 14), "DATE CHECK", font=font(16, bold=True), fill=RED)
    y = text_block(d, 28, by2 + 40,
                   "Every story here was reported Monday 23 Nov 2026.",
                   font(13, bold=True), INK, 560, leading=17)
    y = text_block(d, 28, y + 6,
                   "NOT Monday \u2014 kept out: COP31 collapse (Sun 22) \u00b7 "
                   "Bahrain attack (Sat 21) \u00b7 Dymer strike (Sun 22) \u00b7 "
                   "Nikkei \u22125.06% (Fri 20; Japan closed Mon) \u00b7 "
                   "Democrats\u2019 House win (3\u20134 Nov) \u00b7 "
                   "Miss Universe final (Tue 24).",
                   font(12), INK, 560, leading=16)
    text_block(d, 28, y + 6,
               "Merkury: attack Sun, announced Mon \u2014 shown as Monday\u2019s "
               "announcement.",
               font(12), MUTED, 560, leading=16)
    # Legend (right).
    d.rectangle([616, by2, W - 16, 1008], fill=PANEL_BG,
                outline=PANEL_LINE, width=1)
    d.rectangle([616, by2, W - 16, by2 + 5], fill=NAVY)
    d.text((628, by2 + 14), "HOW WE KNOW", font=font(16, bold=True),
           fill=INK)
    legend = [
        ("REPORTED", "confirmed by named sources"),
        ("CLAIM", "one side\u2019s claim, not independently verified"),
        ("PROPOSAL", "announced plan, not yet adopted"),
    ]
    ly = by2 + 42
    for tag, desc in legend:
        draw_tag(d, 628, ly, tag)
        d.text((628 + 108, ly + 3), desc, font=font(12), fill=INK)
        ly += 28
    y = text_block(d, 628, ly + 4,
                   "Sources: WSJ \u00b7 CNN \u00b7 Reuters \u00b7 AP \u00b7 AFP "
                   "\u00b7 EC \u00b7 SBU \u00b7 Oxfam",
                   font(12), MUTED, 368, leading=16)
    d.text((628, 1008 - 22),
           "One image of Monday 23 Nov 2026 world news",
           font=font(11), fill=MUTED)

    img.save(OUT, optimize=True)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
