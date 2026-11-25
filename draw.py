#!/usr/bin/env python3
"""Koran 25 — Wednesday 25 November 2026.
Draws 'THE WORLD IN ONE PAGE' at 4x supersampling with PIL, then
downsamples to 1024x1024. Deterministic: fixed seed, no time, no network.
Layout: full-width hero banner (rocket launch) + 3 secondary stories +
number strip + navy region bar + 10-story icon grid + where-it-happened
list + also-on-Wednesday list + date-check box. 35 stories total.
"""
import random
from PIL import Image, ImageDraw, ImageFont

SS = 4                      # supersampling factor
W, H = 1024, 1024           # final size
CW, CH = W * SS, H * SS

PAPER = (246, 239, 221)
CARD = (252, 249, 240)
INK = (26, 22, 18)
RED = (178, 34, 28)
NAVY = (28, 47, 74)
GRAY = (96, 89, 75)
FAINT = (200, 190, 168)
SKY_TOP = (13, 27, 51)
SKY_BOT = (39, 75, 115)

SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def F(path, size):
    return ImageFont.truetype(path, int(size * SS))


def wrap(draw, text, font, max_w):
    """Greedy word wrap to max_w (final px). Returns list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=font) <= max_w * SS:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, lines, font, fill=INK, leading=1.25):
    """Draw lines (final px coords). Returns y after last line."""
    lh = int(font.size / SS * leading)
    for ln in lines:
        draw.text((x * SS, y * SS), ln, font=font, fill=fill)
        y += lh
    return y


def hline(draw, x0, x1, y, width=2, fill=INK):
    draw.line([(x0 * SS, y * SS), (x1 * SS, y * SS)], fill=fill, width=max(1, int(width * SS)))


def vgrad(draw, box, top, bot):
    x0, y0, x1, y1 = box
    for yy in range(y0, y1):
        t = (yy - y0) / max(1, (y1 - y0))
        c = tuple(int(top[i] + (bot[i] - top[i]) * t) for i in range(3))
        draw.line([(x0 * SS, yy * SS), (x1 * SS, yy * SS)], fill=c)


def stars(draw, box, n=70, seed=25):
    rng = random.Random(seed)
    x0, y0, x1, y1 = box
    for _ in range(n):
        x = rng.uniform(x0 + 4, x1 - 4)
        y = rng.uniform(y0 + 4, y1 * 0.55)
        r = rng.choice([1, 1, 1.5, 2])
        a = rng.randint(150, 255)
        draw.ellipse([(x - r) * SS, (y - r) * SS, (x + r) * SS, (y + r) * SS],
                     fill=(255, 255, 255, a) if len((255,)) else (255, 255, 255))


# ---------------------------------------------------------------- hero: rocket
def hero_scene(d, x0, y0, x1, y1):
    vgrad(d, (x0, y0, x1, y1), SKY_TOP, SKY_BOT)
    stars(d, (x0, y0, x1, y1))
    # moon
    mx, my, mr = x1 - 92, y0 + 52, 30
    d.ellipse([(mx - mr) * SS, (my - mr) * SS, (mx + mr) * SS, (my + mr) * SS],
              fill=(238, 230, 200))
    d.ellipse([(mx - mr + 14) * SS, (my - mr + 8) * SS, (mx - mr + 26) * SS, (my - mr + 20) * SS],
              fill=(214, 203, 168))
    d.ellipse([(mx - 6) * SS, (my + 10) * SS, (mx + 8) * SS, (my + 24) * SS],
              fill=(214, 203, 168))
    # distant hills
    d.polygon([((x0) * SS, (y1 - 34) * SS), ((x0 + 260) * SS, (y1 - 62) * SS),
               ((x0 + 560) * SS, (y1 - 30) * SS), ((x1) * SS, (y1 - 52) * SS),
               ((x1) * SS, (y1) * SS), ((x0) * SS, (y1) * SS)], fill=(16, 32, 56))
    # ground
    d.rectangle([(x0 * SS, (y1 - 26) * SS), (x1 * SS, y1 * SS)], fill=(10, 20, 36))
    # launch tower (left of rocket)
    tx = x0 + 300
    d.rectangle([(tx * SS, (y0 + 52) * SS), ((tx + 16) * SS, (y1 - 26) * SS)], fill=(52, 66, 88))
    for yy in range(y0 + 66, y1 - 40, 16):
        d.line([(tx * SS, yy * SS), ((tx + 16) * SS, (yy + 12) * SS)], fill=(120, 135, 158), width=SS)
    d.line([(tx * SS, (y0 + 52) * SS), ((tx + 60) * SS, (y0 + 66) * SS)], fill=(120, 135, 158), width=2 * SS)
    # rocket
    rx = x0 + 420
    ry_top = y0 + 34
    ry_bot = y1 - 78
    # flame
    d.polygon([((rx - 16) * SS, (ry_bot + 6) * SS), ((rx + 16) * SS, (ry_bot + 6) * SS),
               ((rx) * SS, (ry_bot + 62) * SS)], fill=(255, 122, 26))
    d.polygon([((rx - 8) * SS, (ry_bot + 6) * SS), ((rx + 8) * SS, (ry_bot + 6) * SS),
               ((rx) * SS, (ry_bot + 40) * SS)], fill=(255, 214, 90))
    # smoke puffs at base
    for cx, cy, cr in [(rx - 52, y1 - 44, 26), (rx + 54, y1 - 40, 30), (rx - 8, y1 - 34, 34),
                       (rx + 96, y1 - 46, 20), (rx - 96, y1 - 48, 18)]:
        d.ellipse([(cx - cr) * SS, (cy - cr * 0.6) * SS, (cx + cr) * SS, (cy + cr * 0.6) * SS],
                  fill=(198, 205, 212))
    # body
    d.rectangle([(rx - 16) * SS, ry_top * SS, (rx + 16) * SS, ry_bot * SS], fill=(240, 238, 230))
    d.polygon([((rx - 16) * SS, ry_top * SS), ((rx + 16) * SS, ry_top * SS),
               ((rx) * SS, (ry_top - 26) * SS)], fill=(178, 34, 28))
    d.ellipse([(rx - 7) * SS, (ry_top + 26) * SS, (rx + 7) * SS, (ry_top + 40) * SS],
              fill=(39, 75, 115), outline=(26, 22, 18), width=SS)
    # fins
    d.polygon([((rx - 16) * SS, (ry_bot - 26) * SS), ((rx - 16) * SS, ry_bot * SS),
               ((rx - 34) * SS, ry_bot * SS)], fill=(178, 34, 28))
    d.polygon([((rx + 16) * SS, (ry_bot - 26) * SS), ((rx + 16) * SS, ry_bot * SS),
               ((rx + 34) * SS, ry_bot * SS)], fill=(178, 34, 28))
    # flag-ish stripe + label
    d.rectangle([(rx - 16) * SS, (ry_top + 52) * SS, (rx + 16) * SS, (ry_top + 60) * SS],
                fill=(39, 75, 115))
    # small crew capsule / station arc top-right
    d.arc([((x1 - 190) * SS, (y0 + 18) * SS), ((x1 - 40) * SS, (y0 + 92) * SS)],
          start=200, end=340, fill=(238, 230, 200), width=3 * SS)
    d.ellipse([((x1 - 122) * SS, (y0 + 30) * SS), ((x1 - 106) * SS, (y0 + 46) * SS)],
              fill=(238, 230, 200))


# ---------------------------------------------------------------- sea strike
def sea_scene(d, x0, y0, x1, y1):
    vgrad(d, (x0, y0, x1, y1), (58, 42, 66), (214, 126, 62))
    # sun low
    sx, sy, sr = x0 + 52, y0 + 34, 20
    d.ellipse([(sx - sr) * SS, (sy - sr) * SS, (sx + sr) * SS, (sy + sr) * SS], fill=(255, 196, 110))
    # sea
    d.rectangle([(x0 * SS, (y0 + 78) * SS), (x1 * SS, y1 * SS)], fill=(36, 84, 128))
    for wy in range(y0 + 84, y1 - 4, 12):
        for wx in range(x0 + 6, x1 - 20, 44):
            d.arc([(wx * SS, wy * SS), ((wx + 26) * SS, (wy + 8) * SS)],
                  start=180, end=360, fill=(140, 190, 225), width=SS)
    # cargo ship
    hx0, hx1 = x0 + 66, x1 - 60
    hy = y0 + 66
    d.polygon([((hx0) * SS, hy * SS), ((hx1) * SS, hy * SS), ((hx1 - 12) * SS, (hy + 22) * SS),
               ((hx0 + 16) * SS, (hy + 22) * SS)], fill=(30, 30, 34))
    for i, col in enumerate([(178, 60, 44), (44, 120, 90), (206, 150, 44), (44, 90, 140)]):
        cx = hx0 + 22 + i * 34
        d.rectangle([(cx * SS, (hy - 16) * SS), ((cx + 28) * SS, hy * SS)], fill=col)
    d.rectangle([((hx1 - 34) * SS, (hy - 30) * SS), ((hx1 - 8) * SS, (hy - 16) * SS)], fill=(220, 220, 214))
    # explosion flash above ship
    ex, ey = x1 - 108, y0 + 30
    for r, col in [(26, (255, 214, 90)), (17, (255, 140, 40)), (9, (255, 240, 180))]:
        d.polygon([((ex) * SS, (ey - r) * SS), ((ex + r * 0.4) * SS, (ey - r * 0.4) * SS),
                   ((ex + r) * SS, (ey) * SS), ((ex + r * 0.4) * SS, (ey + r * 0.4) * SS),
                   ((ex) * SS, (ey + r) * SS), ((ex - r * 0.4) * SS, (ey + r * 0.4) * SS),
                   ((ex - r) * SS, (ey) * SS), ((ex - r * 0.4) * SS, (ey - r * 0.4) * SS)],
                  fill=col)
    # drone top-left
    dx, dy = x0 + 40, y0 + 22
    d.ellipse([(dx - 5) * SS, (dy - 3) * SS, (dx + 5) * SS, (dy + 3) * SS], fill=(20, 20, 22))
    for ox in (-12, 12):
        d.line([((dx + ox - 7) * SS, dy * SS), ((dx + ox + 7) * SS, dy * SS)], fill=(20, 20, 22), width=2 * SS)


# ---------------------------------------------------------------- market chart
def chart_scene(d, x0, y0, x1, y1):
    d.rectangle([(x0 * SS, y0 * SS), (x1 * SS, y1 * SS)], fill=(12, 26, 20))
    for gy in range(y0 + 14, y1 - 6, 16):
        d.line([(x0 * SS, gy * SS), (x1 * SS, gy * SS)], fill=(30, 58, 42), width=SS)
    for gx in range(x0 + 14, x1 - 6, 22):
        d.line([(gx * SS, y0 * SS), (gx * SS, y1 * SS)], fill=(30, 58, 42), width=SS)
    # candles descending
    pts = [(x0 + 16, y0 + 30), (x0 + 44, y0 + 38), (x0 + 72, y0 + 34), (x0 + 100, y0 + 52),
           (x0 + 128, y0 + 48), (x0 + 156, y0 + 66), (x0 + 184, y0 + 62), (x0 + 212, y0 + 84),
           (x0 + 240, y0 + 80), (x0 + 268, y0 + 98)]
    for i, (cx, cy) in enumerate(pts):
        up = (i % 3 == 0)
        col = (74, 190, 120) if up else (224, 70, 60)
        top = cy - 8 if up else cy
        bot = cy + 8 if up else cy + 16
        d.line([((cx) * SS, (cy - 12) * SS), ((cx) * SS, (bot + 4) * SS)], fill=col, width=SS)
        d.rectangle([((cx - 6) * SS, top * SS), ((cx + 6) * SS, bot * SS)], fill=col)
    for i in range(len(pts) - 1):
        d.line([(pts[i][0] * SS, pts[i][1] * SS), (pts[i + 1][0] * SS, pts[i + 1][1] * SS)],
               fill=(224, 70, 60), width=2 * SS)
    for cx, cy in pts:
        d.ellipse([(cx - 3) * SS, (cy - 3) * SS, (cx + 3) * SS, (cy + 3) * SS], fill=(255, 255, 255))
    f = F(SANS_B, 13)
    d.text(((x0 + 8) * SS, (y0 + 6) * SS), "NVDA", font=f, fill=(140, 220, 170))
    f2 = F(SANS_B, 15)
    d.text(((x1 - 52) * SS, (y0 + 6) * SS), "-6%", font=f2, fill=(224, 70, 60))


# ---------------------------------------------------------------- gaza dusk
def gaza_scene(d, x0, y0, x1, y1):
    vgrad(d, (x0, y0, x1, y1), (72, 52, 88), (216, 130, 74))
    sx, sy, sr = x1 - 56, y0 + 30, 18
    d.ellipse([(sx - sr) * SS, (sy - sr) * SS, (sx + sr) * SS, (sy + sr) * SS], fill=(255, 200, 120))
    # skyline
    base = y1 - 8
    bx = x0
    for bw, bh in [(34, 46), (26, 62), (40, 40), (30, 70), (36, 48), (28, 58), (44, 42), (30, 66)]:
        d.rectangle([(bx * SS, (base - bh) * SS), ((bx + bw) * SS, base * SS)], fill=(34, 26, 44))
        for wy in range(base - bh + 8, base - 6, 12):
            for wx in range(bx + 6, bx + bw - 6, 11):
                if (wx + wy) % 23 < 11:
                    d.rectangle([(wx * SS, wy * SS), ((wx + 4) * SS, (wy + 5) * SS)], fill=(255, 196, 110))
        bx += bw + 4
        if bx > x1 - 30:
            break
    # smoke plume
    for cx, cy, cr in [(x0 + 120, y0 + 34, 16), (x0 + 132, y0 + 22, 20), (x0 + 148, y0 + 12, 14)]:
        d.ellipse([(cx - cr) * SS, (cy - cr * 0.7) * SS, (cx + cr) * SS, (cy + cr * 0.7) * SS],
                  fill=(120, 112, 118))
    # small fires
    for fx, fy in [(x0 + 60, base - 8), (x0 + 210, base - 6)]:
        d.polygon([((fx) * SS, (fy - 12) * SS), ((fx + 6) * SS, fy * SS), ((fx - 6) * SS, fy * SS)],
                  fill=(255, 140, 40))


# ---------------------------------------------------------------- small icons
def icon_tower(d, x, y, s):
    d.polygon([((x + s * 0.5) * SS, y * SS), ((x + s * 0.72) * SS, (y + s * 0.55) * SS),
               ((x + s * 0.28) * SS, (y + s * 0.55) * SS)], fill=(120, 90, 60))
    d.rectangle([(x * SS, (y + s * 0.55) * SS), ((x + s) * SS, (y + s * 0.72) * SS)], fill=(90, 60, 40))
    d.line([((x + s * 0.5) * SS, y * SS), ((x + s * 0.5) * SS, (y - s * 0.14) * SS)],
           fill=(178, 34, 28), width=2 * SS)
    d.ellipse([((x + s * 0.42) * SS, (y - s * 0.2) * SS), ((x + s * 0.58) * SS, (y - s * 0.04) * SS)],
              fill=(255, 140, 40))


def icon_chip(d, x, y, s):
    d.rectangle([(x * SS, y * SS), ((x + s) * SS, (y + s) * SS)], fill=(28, 47, 74))
    d.rectangle([((x + s * 0.22) * SS, (y + s * 0.22) * SS), ((x + s * 0.78) * SS, (y + s * 0.78) * SS)],
                fill=(140, 190, 225))
    for i in range(3):
        px = x + s * (0.2 + i * 0.3)
        d.line([(px * SS, (y - s * 0.14) * SS), (px * SS, y * SS)], fill=(26, 22, 18), width=2 * SS)
        d.line([(px * SS, (y + s) * SS), (px * SS, (y + s * 1.14) * SS)], fill=(26, 22, 18), width=2 * SS)


def icon_shield(d, x, y, s):
    d.polygon([((x) * SS, (y + s * 0.12) * SS), ((x + s * 0.5) * SS, y * SS),
               ((x + s) * SS, (y + s * 0.12) * SS), ((x + s) * SS, (y + s * 0.55) * SS),
               ((x + s * 0.5) * SS, (y + s) * SS), ((x) * SS, (y + s * 0.55) * SS)],
              fill=(178, 34, 28))
    d.line([((x + s * 0.3) * SS, (y + s * 0.5) * SS), ((x + s * 0.46) * SS, (y + s * 0.68) * SS),
            ((x + s * 0.74) * SS, (y + s * 0.3) * SS)], fill=(255, 255, 255), width=2 * SS)


def icon_tanker(d, x, y, s):
    d.polygon([((x) * SS, (y + s * 0.55) * SS), ((x + s) * SS, (y + s * 0.55) * SS),
               ((x + s * 0.88) * SS, (y + s * 0.85) * SS), ((x + s * 0.12) * SS, (y + s * 0.85) * SS)],
              fill=(30, 30, 34))
    for i, col in enumerate([(178, 60, 44), (44, 120, 90), (206, 150, 44)]):
        cx = x + s * (0.16 + i * 0.28)
        d.ellipse([(cx * SS, (y + s * 0.3) * SS), ((cx + s * 0.2) * SS, (y + s * 0.5) * SS)], fill=col)
    d.line([(x * SS, (y + s * 0.95) * SS), ((x + s) * SS, (y + s * 0.95) * SS)], fill=(36, 84, 128), width=2 * SS)


def icon_plane(d, x, y, s):
    d.polygon([((x + s * 0.08) * SS, (y + s * 0.55) * SS), ((x + s * 0.85) * SS, (y + s * 0.3) * SS),
               ((x + s) * SS, (y + s * 0.38) * SS), ((x + s * 0.5) * SS, (y + s * 0.62) * SS),
               ((x + s * 0.3) * SS, (y + s * 0.72) * SS), ((x + s * 0.14) * SS, (y + s * 0.72) * SS)],
              fill=(28, 47, 74))


def icon_people(d, x, y, s):
    for ox, r, col in [(0.3, 0.16, (178, 34, 28)), (0.68, 0.16, (28, 47, 74))]:
        cx = x + s * ox
        d.ellipse([((cx - s * r) * SS, y * SS), ((cx + s * r) * SS, (y + s * r * 2) * SS)], fill=col)
        d.pieslice([((cx - s * r * 1.2) * SS, (y + s * r * 2) * SS),
                    ((cx + s * r * 1.2) * SS, (y + s * 1.05) * SS)], start=180, end=360, fill=col)


def icon_quake(d, x, y, s):
    d.line([(x * SS, (y + s * 0.8) * SS), ((x + s) * SS, (y + s * 0.8) * SS)], fill=(96, 89, 75), width=2 * SS)
    d.line([((x + s * 0.2) * SS, (y + s * 0.8) * SS), ((x + s * 0.35) * SS, (y + s * 0.5) * SS),
            ((x + s * 0.5) * SS, (y + s * 0.72) * SS), ((x + s * 0.68) * SS, (y + s * 0.42) * SS),
            ((x + s * 0.82) * SS, (y + s * 0.62) * SS)], fill=(178, 34, 28), width=2 * SS)
    d.polygon([((x + s * 0.42) * SS, (y + s * 0.1) * SS), ((x + s * 0.58) * SS, (y + s * 0.1) * SS),
               ((x + s * 0.5) * SS, (y + s * 0.34) * SS)], fill=(90, 60, 40))


def icon_medal(d, x, y, s):
    d.polygon([((x + s * 0.3) * SS, y * SS), ((x + s * 0.7) * SS, y * SS),
               ((x + s * 0.58) * SS, (y + s * 0.4) * SS), ((x + s * 0.42) * SS, (y + s * 0.4) * SS)],
              fill=(178, 34, 28))
    d.ellipse([((x + s * 0.18) * SS, (y + s * 0.36) * SS), ((x + s * 0.82) * SS, (y + s) * SS)],
              fill=(206, 150, 44), outline=(120, 90, 20), width=2 * SS)
    d.text(((x + s * 0.42) * SS, (y + s * 0.48) * SS), "1", font=F(SANS_B, 13), fill=(255, 255, 255))


def icon_search(d, x, y, s):
    d.ellipse([(x * SS, y * SS), ((x + s * 0.66) * SS, (y + s * 0.66) * SS)],
              outline=(28, 47, 74), width=3 * SS)
    d.line([((x + s * 0.55) * SS, (y + s * 0.55) * SS), ((x + s * 0.95) * SS, (y + s * 0.95) * SS)],
           fill=(28, 47, 74), width=3 * SS)
    d.text(((x + s * 0.18) * SS, (y + s * 0.1) * SS), "?", font=F(SANS_B, 15), fill=(178, 34, 28))


def icon_radar(d, x, y, s):
    d.ellipse([(x * SS, y * SS), ((x + s) * SS, (y + s) * SS)], outline=(28, 47, 74), width=2 * SS)
    d.ellipse([((x + s * 0.25) * SS, (y + s * 0.25) * SS), ((x + s * 0.75) * SS, (y + s * 0.75) * SS)],
              outline=(28, 47, 74), width=SS)
    d.line([((x + s * 0.5) * SS, (y + s * 0.5) * SS), ((x + s * 0.85) * SS, (y + s * 0.2) * SS)],
           fill=(178, 34, 28), width=2 * SS)
    d.ellipse([((x + s * 0.44) * SS, (y + s * 0.44) * SS), ((x + s * 0.56) * SS, (y + s * 0.56) * SS)],
              fill=(178, 34, 28))


ICONS = {"tower": icon_tower, "chip": icon_chip, "shield": icon_shield, "tanker": icon_tanker,
         "plane": icon_plane, "people": icon_people, "quake": icon_quake, "medal": icon_medal,
         "search": icon_search, "radar": icon_radar}


# ---------------------------------------------------------------- content
HERO = ("SPACE · JIUQUAN, CHINA",
        "PAKISTAN'S FIRST ASTRONAUT REACHES ORBIT",
        "Muhammad Zeeshan Ali, a Pakistan Air Force pilot, launches aboard China's "
        "Shenzhou-24 to the Tiangong station — the first Pakistani in orbit, and the "
        "first foreign astronaut aboard Tiangong. He will spend a week in orbit running "
        "four biotech experiments.",
        "REUTERS · AP")

SECONDARY = [
    ("UKRAINE · GULF OF FINLAND",
     "KYIV: WE HIT A RUSSIAN SHIP",
     "Zelenskiy confirms a Ukrainian drone strike on a Russian cargo ship. "
     "Norway, a staunch ally, urges caution.",
     "REUTERS", "sea"),
    ("TECH · MARKETS",
     "THE AI TRADE CRACKS AGAIN",
     "Nvidia falls 6% and Micron 11% as the Nasdaq drops 1.5%. The White House is "
     "said to be preparing tariff hikes on China, the EU and 14 more economies.",
     "REUTERS · WSJ", "chart"),
    ("GAZA · GAZA CITY",
     "HAMAS SECURITY CHIEF DEAD",
     "An Israeli airstrike kills Naeem Abu Nahel, Hamas' internal security "
     "chief. Seven Palestinians killed on Tuesday.",
     "REUTERS · AP", "gaza"),
]

NUMBERS = [
    ("-6%", "NVIDIA SHARES, TUESDAY"),
    ("-11%", "MICRON SHARES, TUESDAY"),
    ("11", "WOUNDED IN RIYADH TOWER STRIKE"),
    ("13", "KILLED IN UAE BUS–TRUCK CRASH"),
    ("6,500", "ROHINGYA TO BE SENT BACK TO MYANMAR"),
    ("570,000", "AIDS DEATHS IN 2025, LOWEST IN 20+ YEARS"),
]

GRID = [
    ("tower", "RIYADH TOWER HIT",
     "Houthi drone strike wounds 11 in the capital.", "MIDDLE EAST"),
    ("chip", "HUAWEI GUILTY",
     "US jury convicts Huawei of trade-secret theft.", "TECH"),
    ("shield", "CIA BREACH",
     "CIA and ODNI hit by cyber breach; data taken.", "USA"),
    ("tanker", "TANKERS MINED",
     "Three tankers hit by mines in the Strait of Hormuz.", "MIDDLE EAST"),
    ("plane", "HASINA TO RETURN",
     "Ousted PM plans to come home on 16 December.", "ASIA"),
    ("people", "ROHINGYA RETURN",
     "Malaysia to send 6,500 refugees back in December.", "ASIA"),
    ("quake", "NEPAL QUAKE",
     "Magnitude 5.6 quake strikes near Tibet border.", "ASIA"),
    ("medal", "GIULIANI HONOURED",
     "Trump awards Giuliani the Medal of Freedom.", "USA"),
    ("search", "CHINA PROBE",
     "Probe opens into Shanghai Party chief Chen Jining.", "ASIA"),
    ("radar", "NATO TO POLAND",
     "Early-warning aircraft to deploy after reports.", "EUROPE"),
]

WHERE = [
    ("ASIA", "JIUQUAN", "Shenzhou-24 carries Pakistan's first astronaut to Tiangong"),
    ("ASIA", "DHAKA", "Hasina plans return from exile on 16 December"),
    ("ASIA", "KUALA LUMPUR", "Malaysia to send 6,500 Rohingya back to Myanmar"),
    ("MIDDLE EAST", "GAZA CITY", "Airstrike kills Hamas security chief Abu Nahel"),
    ("MIDDLE EAST", "RIYADH", "Houthi drone hits the tallest tower; 11 hurt"),
    ("MIDDLE EAST", "HORMUZ", "Three tankers hit by naval mines"),
    ("EUROPE", "GULF OF FINLAND", "Kyiv confirms drone strike on Russian ship"),
    ("EUROPE", "WARSAW", "NATO to send early-warning aircraft to Poland"),
    ("AMERICAS", "NEW YORK", "Nvidia falls 6% as AI sell-off deepens"),
    ("AMERICAS", "WASHINGTON", "CIA and ODNI report a cyber breach"),
]

ALSO = [
    "Sarkozy case to trial; hearing Apr 2027.",
    "Fort Hood shooter seeks stay of execution.",
    "Libya's frozen conflict may flare again.",
    "Houthis 60 km from Aden; city 'won't fall'.",
    "Saudi strikes kill 17, 26 in Hodeida, Lahj.",
    "Russian jets enter Korea's defence zone.",
    "Trump spares turkeys Freedom and Feathers.",
    "US envoy unsure Israel aid ends this year.",
    "Sweden votes on Kristersson staying PM.",
    "UAE crash toll rises to 13; 14 injured.",
    "EU announces further sanctions on Russia.",
    "Russia, Ukraine trade barbs at the UN.",
    "NATO responds to satellite reports.",
    "DR Congo military plane missing.",
    "Iran lashes singer Ahmadi 74 times.",
    "Houthis threaten Saudi ports.",
    "Iraq cracks down on oil smuggling.",
    "Leaked data on Russian deaths in Mali.",
    "Radar issue delays O'Hare flights.",
    "Dell lifts forecasts on AI server demand.",
    "England beat Australia by 8 wickets.",
]


# ---------------------------------------------------------------- page
def build():
    img = Image.new("RGB", (CW, CH), PAPER)
    d = ImageDraw.Draw(img)
    M = 28                      # margin (final px)
    X0, X1 = M, W - M
    CWID = X1 - X0

    # ---- top kicker row
    fk = F(SANS_B, 12)
    d.text((X0 * SS, 12 * SS), "THE WORLD IN ONE PAGE", font=fk, fill=INK)
    rt = "WEDNESDAY · 25 NOVEMBER 2026"
    d.text(((X1 - d.textlength(rt, font=fk) / SS) * SS, 12 * SS), rt, font=fk, fill=INK)
    hline(d, X0, X1, 32, width=2)

    # ---- masthead
    fm = F(SERIF_B, 52)
    title = "Wednesday 25 November 2026"
    tw = d.textlength(title, font=fm) / SS
    d.text(((W - tw) / 2 * SS, 38 * SS), title, font=fm, fill=INK)
    ft = F(SERIF_I, 15)
    tag = "One day. Every story that mattered. 35 stories, all verified."
    tw = d.textlength(tag, font=ft) / SS
    d.text(((W - tw) / 2 * SS, 96 * SS), tag, font=ft, fill=INK)
    hline(d, X0, X1, 116, width=2)

    # ---- hero: full-width image + white card
    hy0, hy1 = 124, 282
    hero_scene(d, X0, hy0, X1, hy1)
    d.rectangle([(X0 * SS, hy1 * SS), (X1 * SS, (hy1 + 2) * SS)], fill=INK)
    cy0, cy1 = hy1 + 2, 380
    d.rectangle([(X0 * SS, cy0 * SS), (X1 * SS, cy1 * SS)], fill=CARD)
    d.rectangle([(X0 * SS, cy0 * SS), (X1 * SS, cy1 * SS)], outline=FAINT, width=SS)
    kicker, head, summ, src = HERO
    y = cy0 + 8
    d.text(((X0 + 12) * SS, y * SS), kicker, font=F(SANS_B, 11), fill=RED)
    sw = d.textlength(src, font=F(SANS, 10)) / SS
    d.text(((X1 - 12 - sw) * SS, y * SS), src, font=F(SANS, 10), fill=GRAY)
    y += 15
    fh = F(SERIF_B, 28)
    for ln in wrap(d, head, fh, CWID - 24):
        d.text(((X0 + 12) * SS, y * SS), ln, font=fh, fill=INK)
        y += 32
    fb = F(SANS, 11.5)
    y = text_block(d, X0 + 12, y + 2, wrap(d, summ, fb, CWID - 24), fb, leading=1.3)

    # ---- secondary: three columns
    sy0 = 390
    colw = (CWID - 26) // 3
    img_h, card_h = 96, 100
    for i, (kick, head, summ, src, scene) in enumerate(SECONDARY):
        x0 = X0 + i * (colw + 13)
        x1 = x0 + colw
        if scene == "sea":
            sea_scene(d, x0, sy0, x1, sy0 + img_h)
        elif scene == "chart":
            chart_scene(d, x0, sy0, x1, sy0 + img_h)
        else:
            gaza_scene(d, x0, sy0, x1, sy0 + img_h)
        d.rectangle([(x0 * SS, (sy0 + img_h) * SS), (x1 * SS, (sy0 + img_h + 2) * SS)], fill=INK)
        c0 = sy0 + img_h + 2
        d.rectangle([(x0 * SS, c0 * SS), (x1 * SS, (c0 + card_h) * SS)], fill=CARD)
        d.rectangle([(x0 * SS, c0 * SS), (x1 * SS, (c0 + card_h) * SS)], outline=FAINT, width=SS)
        y = c0 + 6
        d.text(((x0 + 8) * SS, y * SS), kick, font=F(SANS_B, 9.5), fill=RED)
        y += 13
        fh2 = F(SERIF_B, 18)
        for ln in wrap(d, head, fh2, colw - 16):
            d.text(((x0 + 8) * SS, y * SS), ln, font=fh2, fill=INK)
            y += 20
        fb2 = F(SANS, 10.5)
        text_block(d, x0 + 8, y + 1, wrap(d, summ, fb2, colw - 16), fb2, leading=1.25)
        d.text(((x0 + 8) * SS, (c0 + card_h - 13) * SS), src, font=F(SANS, 9), fill=GRAY)
    sec_bot = sy0 + img_h + 2 + card_h

    # ---- numbers strip
    ny0 = sec_bot + 10
    ny1 = ny0 + 48
    d.rectangle([(X0 * SS, ny0 * SS), (X1 * SS, ny1 * SS)], fill=CARD)
    d.rectangle([(X0 * SS, ny0 * SS), (X1 * SS, ny1 * SS)], outline=FAINT, width=SS)
    ncols = len(NUMBERS)
    nwid = CWID // ncols
    for i, (num, lab) in enumerate(NUMBERS):
        cx = X0 + i * nwid + nwid // 2
        fn = F(SERIF_B, 26)
        nw = d.textlength(num, font=fn) / SS
        d.text(((cx - nw / 2) * SS, (ny0 + 4) * SS), num, font=fn, fill=RED)
        fl = F(SANS_B, 8)
        for j, ln in enumerate(wrap(d, lab, fl, nwid - 14)):
            lw = d.textlength(ln, font=fl) / SS
            d.text(((cx - lw / 2) * SS, (ny0 + 30 + j * 9) * SS), ln, font=fl, fill=INK)
        if i:
            d.line([((X0 + i * nwid) * SS, (ny0 + 8) * SS), ((X0 + i * nwid) * SS, (ny1 - 8) * SS)],
                   fill=FAINT, width=SS)

    # ---- navy region bar
    by0 = ny1 + 10
    by1 = by0 + 22
    d.rectangle([(X0 * SS, by0 * SS), (X1 * SS, by1 * SS)], fill=NAVY)
    fb3 = F(SANS_B, 11.5)
    bar = "WHERE THE NEWS WAS  ·  Asia 6  ·  Middle East 9  ·  Europe 6  ·  Americas 9  ·  Africa 3  ·  Global 2"
    bw = d.textlength(bar, font=fb3) / SS
    d.text(((W - bw) / 2 * SS, (by0 + 5) * SS), bar, font=fb3, fill=(240, 238, 230))

    # ---- 10-story icon grid: 5 cols x 2 rows
    gy0 = by1 + 10
    grow_h = 52
    gcolw = (CWID - 4 * 10) // 5
    for i, (ic, head, summ, tag) in enumerate(GRID):
        r, c = divmod(i, 5)
        x0 = X0 + c * (gcolw + 10)
        y0 = gy0 + r * (grow_h + 6)
        x1 = x0 + gcolw
        d.rectangle([(x0 * SS, y0 * SS), (x1 * SS, (y0 + grow_h) * SS)], fill=CARD)
        d.rectangle([(x0 * SS, y0 * SS), (x1 * SS, (y0 + grow_h) * SS)], outline=FAINT, width=SS)
        ICONS[ic](d, x0 + 8, y0 + 10, 28)
        tx = x0 + 44
        fh3 = F(SANS_B, 11)
        y = y0 + 5
        for ln in wrap(d, head, fh3, gcolw - 52):
            d.text((tx * SS, y * SS), ln, font=fh3, fill=INK)
            y += 12
        fb4 = F(SANS, 9.5)
        text_block(d, tx, y + 1, wrap(d, summ, fb4, gcolw - 52), fb4, leading=1.2)
    grid_bot = gy0 + 2 * grow_h + 6

    # ---- bottom: where it happened | also on wednesday
    bx0 = grid_bot + 10
    fbh = F(SANS_B, 11.5)
    d.text((X0 * SS, bx0 * SS), "WHERE IT HAPPENED", font=fbh, fill=INK)
    hline(d, X0, X0 + 300, bx0 + 15, width=1)
    fl5 = F(SANS, 10.5)
    fb5 = F(SANS_B, 10.5)
    y = bx0 + 20
    for reg, place, txt in WHERE:
        pre = reg + (" · " + place if place else "") + " — "
        d.text((X0 * SS, y * SS), pre, font=fb5, fill=RED)
        pw = d.textlength(pre, font=fb5) / SS
        d.text(((X0 + pw) * SS, y * SS), txt, font=fl5, fill=INK)
        y += 12
    where_bot = y

    rx0 = X0 + 470
    d.text((rx0 * SS, bx0 * SS), "ALSO ON WEDNESDAY…", font=fbh, fill=INK)
    hline(d, rx0, X1, bx0 + 15, width=1)
    col2w = (X1 - rx0 - 12) // 2
    col_y = [bx0 + 20, bx0 + 20]
    fa = F(SANS, 10)
    for i, item in enumerate(ALSO):
        col = 0 if i < 11 else 1
        xx = rx0 + col * (col2w + 12)
        yy = col_y[col]
        num = f"{i + 1}. "
        fnum = F(SANS_B, 10)
        nw = d.textlength(num, font=fnum) / SS
        d.text((xx * SS, yy * SS), num, font=fnum, fill=RED)
        lines = wrap(d, item, fa, col2w - nw - 2)
        for ln in lines:
            d.text(((xx + nw) * SS, yy * SS), ln, font=fa, fill=INK)
            yy += 11
        col_y[col] = yy + 1
    also_bot = max(col_y)

    # ---- date check box (left column, below where list)
    dc_x0, dc_x1 = X0, X0 + 442
    dy0 = where_bot + 5
    dy1 = dy0 + 46
    d.rectangle([(dc_x0 * SS, dy0 * SS), (dc_x1 * SS, dy1 * SS)], outline=RED, width=2 * SS)
    d.text(((dc_x0 + 8) * SS, (dy0 + 4) * SS), "DATE CHECK", font=F(SANS_B, 10.5), fill=RED)
    fdc = F(SANS, 9.5)
    dc = ("NOT IN TODAY'S PAPER: COP31 collapsed in Antalya on Monday 23 Nov — that was "
          "Monday's front page. Nvidia's +31% surge was Monday too; today the AI trade fell back.")
    text_block(d, dc_x0 + 8, dy0 + 17, wrap(d, dc, fdc, dc_x1 - dc_x0 - 16), fdc, leading=1.25)

    # ---- footer
    ff = F(SANS, 9.5)
    foot = ("Every story here happened, or was first reported, on Wednesday 25 November 2026. "
            "All drawings are original. Sources: Reuters · AP · Al Jazeera · UN News · WSJ · The Guardian")
    fw = d.textlength(foot, font=ff) / SS
    d.text(((W - fw) / 2 * SS, (H - 16) * SS), foot, font=ff, fill=GRAY)

    img = img.resize((W, H), Image.LANCZOS)
    return img


if __name__ == "__main__":
    import os
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    build().save(out, optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")
