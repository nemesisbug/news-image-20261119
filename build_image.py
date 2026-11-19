#!/usr/bin/env python3
"""Draw "The World Today" - the front page of Thursday 19 November 2026.

One 1024x1024 PNG: masthead, a hero panel on the day's biggest story
(GTA VI launch day), a lon/lat world map with six numbered pins for the
other lead stories, three columns of shorter stories, a by-the-numbers
strip and a sources footer. Deterministic: same bytes every run.
"""
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.environ.get("ENTRY_OUT", "entry.png")

SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF_REG = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"

PAPER = (248, 243, 232)
INK = (24, 24, 24)
MUTED = (92, 84, 72)
RED = (176, 38, 30)
NAVY = (31, 58, 95)
TEAL = (15, 118, 110)
GOLD = (176, 128, 28)
RULE = (196, 186, 166)
OCEAN = (224, 232, 238)
LAND = (235, 226, 200)
LAND_EDGE = (168, 156, 128)
WHITE = (255, 255, 255)


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w, max_lines=None):
    """Greedy word wrap; returns a list of lines (at most max_lines)."""
    words, lines, cur = text.split(), [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    if max_lines and len(lines) > max_lines:
        lines = lines[:max_lines]
        # mark the cut with an ellipsis on the last line
        while lines and draw.textlength(lines[-1] + " ...", font=fnt) > max_w:
            lines[-1] = lines[-1][:-1].rstrip()
        lines[-1] += " ..."
    return lines


def text_block(draw, x, y, lines, fnt, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


# --- the six lead stories, pinned on the map -------------------------------
# (number, lon, lat, headline for the legend, label offset dx, dy)
LEADS = [
    (1, -80.2, 25.8, "GTA VI opens worldwide",
     "Midnight launch; critics score it 99", 14, 4),
    (2, -74.0, 40.7, "Anthropic lists on Nasdaq",
     "Debuts today; priced $83 Wednesday", 14, -16),
    (3, 4.3, 52.1, "ICJ to deliver Myanmar judgment",
     "Due today, 10:00 The Hague", 14, 4),
    (4, 113.8, 22.6, "Trump, Xi and Putin due to meet",
     "First trilateral, in Shenzhen", -14, 4),
    (5, 88.0, 17.0, "Cyclone Akvan nears India",
     "Landfall due Friday noon", -14, -16),
    (6, 13.4, 52.5, "Coalition of the Willing",
     "Meets in Berlin today on Ukraine", 14, -16),
]

# --- the shorter stories, three columns ------------------------------------
# (tag, colour, headline, one-line summary)
STORIES = [
    ("SPACE", TEAL, "Voyager 1 confirmed one light-day away",
     "NASA confirms today the probe crossed the mark on Wednesday — the farthest human-made object."),
    ("DIPLOMACY", NAVY, "India and Japan hold 2+2 talks",
     "Defence and foreign ministers meet in Tokyo to deepen security ties."),
    ("MARKETS", GOLD, "Bitcoin holds near $63,000",
     "The token trades around $63,000 in early Thursday trading."),
    ("MARKETS", GOLD, "Nikkei opens higher",
     "Tokyo's Nikkei 225 opens up 0.36% at 59,238, led higher by SoftBank."),
    ("ENERGY", GOLD, "Oil falls to near $82",
     "WTI crude slides to about $82 a barrel in early Thursday trading."),
    ("ASIA", NAVY, "Korea delays market open for exam",
     "Seoul pushes trading back an hour so students can sit the college entrance exam in quiet."),
    ("SPORT", TEAL, "Women's Champions League tonight",
     "Arsenal host OL Lyonnes and Barcelona face Servette in matchday five."),
    ("TECH", NAVY, "Anthropic tracker to launch today",
     "Ondo's ANTon token goes live for non-US investors — exposure to ANT, not shares."),
    ("SPORT", TEAL, "Nepal league Qualifier 2 today",
     "Sudurpaschim Royals meet Chitwan Rhinos for a place in the final."),
    ("SPORT", TEAL, "Abu Dhabi T10 reaches climax",
     "Three matches at Sheikh Zayed Stadium as the league nears its final."),
    ("GAMES", RED, "Britain braces for GTA VI",
     "2.8m UK adults set to play on launch day; broadband firms brace for record downloads."),
    ("GAMES", RED, "No PC version announced",
     "Rockstar lists PlayStation 5 and Xbox only — no PC date for now."),
]

NUMBERS = [
    ("99", "GTA VI Metacritic score, tying the all-time high"),
    ("$1.65bn", "Estimated GTA VI pre-sales (Sensor Tower)"),
    ("$83", "Anthropic IPO price, set Wednesday"),
    ("$82", "WTI crude in early Thursday trading"),
    ("~$63,000", "Bitcoin in early Thursday trading"),
    ("1 light-day", "Voyager 1's distance from Earth"),
]

# --- world map: coarse continent outlines, equirectangular -----------------
# Simplified shapes drawn from general geography, for a stylised map.
MAP_X0, MAP_X1 = 28, 996
MAP_Y0, MAP_Y1 = 362, 462
LAT_TOP, LAT_BOT = 78, -42

CONTINENTS = [
    # North America: Arctic coast east, Atlantic coast down, Gulf round,
    # Central America to Panama, Pacific coast back up to Alaska.
    [(-168, 66), (-158, 71), (-145, 70), (-135, 69), (-128, 70), (-120, 69),
     (-110, 68), (-100, 68), (-95, 69), (-92, 66), (-85, 66), (-82, 66),
     (-80, 69), (-78, 62), (-75, 62), (-70, 60), (-65, 60), (-60, 55),
     (-55, 52), (-60, 47), (-65, 44), (-68, 44), (-70, 42), (-74, 39),
     (-76, 35), (-80, 32), (-81, 26), (-82, 28), (-84, 30), (-89, 29),
     (-91, 29), (-94, 29), (-97, 26), (-97, 22), (-94, 19), (-91, 19),
     (-87, 16), (-84, 13), (-83, 9), (-80, 8), (-78, 7), (-80, 9),
     (-83, 10), (-86, 12), (-89, 14), (-92, 15), (-95, 16), (-97, 16),
     (-101, 18), (-105, 20), (-108, 23), (-111, 25), (-114, 28), (-117, 33),
     (-121, 36), (-124, 40), (-124, 46), (-127, 49), (-131, 54), (-137, 58),
     (-144, 60), (-151, 59), (-158, 58), (-162, 55), (-166, 60), (-168, 66)],
    # Greenland
    [(-58, 64), (-50, 60), (-43, 60), (-40, 64), (-32, 68), (-25, 70),
     (-22, 70), (-25, 76), (-35, 77), (-45, 76), (-55, 74), (-58, 70),
     (-58, 64)],
    # South America
    [(-80, 9), (-77, 8), (-72, 12), (-64, 11), (-60, 9), (-52, 5),
     (-50, 0), (-44, -3), (-38, -5), (-35, -8), (-38, -15), (-40, -21),
     (-48, -27), (-52, -33), (-57, -38), (-63, -41), (-65, -45), (-68, -50),
     (-69, -54), (-71, -54), (-73, -50), (-73, -44), (-72, -37), (-71, -30),
     (-70, -23), (-70, -18), (-75, -15), (-78, -8), (-81, -4), (-80, 1),
     (-80, 9)],
    # Africa
    [(-17, 15), (-16, 12), (-12, 8), (-8, 5), (-4, 5), (2, 6), (6, 4),
     (9, 4), (9, -1), (12, -5), (13, -12), (12, -18), (14, -22), (16, -28),
     (18, -32), (20, -35), (26, -34), (28, -33), (32, -29), (33, -26),
     (35, -22), (36, -18), (40, -15), (40, -10), (42, -5), (46, -1),
     (51, 11), (48, 11), (44, 11), (41, 12), (39, 15), (38, 18), (37, 20),
     (35, 24), (33, 27), (32, 31), (30, 31), (25, 32), (22, 33), (19, 31),
     (15, 32), (11, 34), (10, 37), (6, 37), (0, 36), (-2, 35), (-6, 34),
     (-9, 32), (-11, 30), (-14, 27), (-16, 23), (-17, 19), (-17, 15)],
    # Eurasia
    [(-10, 37), (-9, 38), (-9, 43), (-4, 44), (-2, 48), (-4, 49),
     (-1, 50), (2, 51), (4, 53), (7, 54), (8, 57), (10, 59), (12, 56),
     (18, 56), (21, 55), (24, 58), (26, 60), (28, 62), (30, 62), (32, 66),
     (35, 67), (40, 68), (48, 68), (55, 68), (62, 69), (68, 72), (75, 72),
     (82, 73), (90, 75), (100, 76), (110, 74), (120, 73), (130, 72),
     (140, 72), (150, 71), (160, 70), (170, 67), (178, 65), (178, 62),
     (170, 60), (163, 60), (160, 56), (158, 53), (156, 51), (150, 59),
     (143, 55), (141, 50), (140, 46), (135, 43), (132, 43), (130, 42),
     (127, 40), (124, 39), (122, 38), (120, 34), (118, 30), (116, 23),
     (112, 22), (109, 20), (108, 18), (106, 10), (104, 9), (102, 7),
     (100, 7), (98, 9), (97, 10), (95, 15), (93, 17), (91, 22), (89, 22),
     (87, 21), (85, 19), (82, 17), (80, 15), (80, 13), (77, 8), (76, 10),
     (74, 14), (73, 19), (72, 21), (70, 22), (68, 23), (66, 25), (63, 25),
     (60, 25), (57, 26), (55, 26), (52, 27), (50, 29), (49, 30), (47, 30),
     (44, 29), (42, 28), (40, 26), (39, 21), (38, 18), (36, 22), (35, 28),
     (34, 29), (34, 31), (33, 34), (32, 36), (30, 36), (28, 37), (26, 38),
     (23, 36), (22, 37), (19, 40), (16, 38), (15, 40), (14, 42), (12, 44),
     (10, 44), (8, 44), (5, 43), (3, 43), (1, 41), (-1, 38), (-3, 36),
     (-6, 36), (-9, 37), (-10, 37)],
    # Australia
    [(113, -22), (114, -28), (115, -32), (116, -35), (119, -34), (122, -34),
     (125, -32), (129, -32), (132, -32), (134, -33), (136, -35), (138, -35),
     (140, -38), (144, -38), (147, -39), (150, -37), (153, -32), (153, -27),
     (151, -24), (149, -20), (146, -19), (143, -15), (142, -11), (141, -13),
     (138, -15), (136, -12), (135, -15), (133, -12), (131, -12), (129, -14),
     (126, -14), (124, -15), (122, -17), (119, -19), (116, -20), (113, -22)],
    # United Kingdom
    [(-5, 50), (-3, 53), (-5, 55), (-5, 57), (-3, 58), (-1, 57), (0, 54),
     (1, 51), (-2, 50), (-5, 50)],
    # Japan
    [(130, 31), (132, 33), (134, 34), (136, 35), (138, 35), (140, 36),
     (141, 39), (141, 42), (143, 43), (145, 44), (144, 44), (142, 42),
     (140, 39), (139, 37), (137, 36), (135, 34), (132, 33), (130, 31)],
    # South-East Asian islands
    [(95, 5), (98, 4), (100, 0), (102, -2), (104, -3), (106, -6),
     (108, -7), (111, -7), (114, -8), (117, -9), (119, -9), (120, -10),
     (123, -10), (126, -8), (128, -5), (130, -3), (132, -2), (135, -3),
     (138, -4), (140, -7), (141, -8), (138, -8), (135, -6), (132, -4),
     (129, -2), (126, 0), (123, 1), (121, 0), (119, 1), (117, 2),
     (115, 2), (113, 1), (111, 0), (108, -1), (106, -2), (104, -1),
     (101, 0), (98, 2), (95, 5)],
    # New Zealand
    [(167, -45), (169, -43), (171, -42), (173, -41), (175, -39), (177, -38),
     (178, -38), (177, -39), (175, -41), (173, -42), (171, -44), (168, -46),
     (167, -45)],
]


def project(lon, lat):
    x = MAP_X0 + (lon + 180) / 360 * (MAP_X1 - MAP_X0)
    y = MAP_Y0 + (LAT_TOP - lat) / (LAT_TOP - LAT_BOT) * (MAP_Y1 - MAP_Y0)
    return (x, y)


def draw_map(d):
    d.rectangle([MAP_X0, MAP_Y0, MAP_X1, MAP_Y1], fill=OCEAN)
    for lon in range(-150, 181, 30):
        x = MAP_X0 + (lon + 180) / 360 * (MAP_X1 - MAP_X0)
        d.line([(x, MAP_Y0), (x, MAP_Y1)], fill=(205, 214, 220), width=1)
    for lat in range(-30, 61, 30):
        _, y = project(0, lat)
        d.line([(MAP_X0, y), (MAP_X1, y)], fill=(205, 214, 220), width=1)
    for poly in CONTINENTS:
        d.polygon([project(lon, lat) for lon, lat in poly],
                  fill=LAND, outline=LAND_EDGE)
    d.rectangle([MAP_X0, MAP_Y0, MAP_X1, MAP_Y1], outline=INK, width=1)
    f_pin = font(SANS_B, 11)
    f_lab = font(SANS_B, 11)
    for num, lon, lat, _headline, _sub, dx, dy in LEADS:
        x, y = project(lon, lat)
        lx, ly = x + dx, y + dy
        d.line([(x, y), (lx, ly)], fill=RED, width=1)
        d.ellipse([x - 8, y - 8, x + 8, y + 8], fill=RED, outline=WHITE, width=1)
        s = str(num)
        nw = d.textlength(s, font=f_pin)
        d.text((x - nw / 2, y - 7), s, font=f_pin, fill=WHITE)


def draw_hero_art(d, x0, y0, x1, y1):
    """Stylised Vice City sunset: gradient sky, sun, skyline, palms, water."""
    # sunset gradient in horizontal bands
    top = (255, 158, 74)
    mid = (255, 107, 141)
    bot = (122, 74, 166)
    hh = y1 - y0
    for i in range(hh):
        t = i / max(hh - 1, 1)
        if t < 0.5:
            u = t / 0.5
            c = tuple(round(top[k] + (mid[k] - top[k]) * u) for k in range(3))
        else:
            u = (t - 0.5) / 0.5
            c = tuple(round(mid[k] + (bot[k] - mid[k]) * u) for k in range(3))
        d.line([(x0, y0 + i), (x1, y0 + i)], fill=c)
    # sun
    cx, cy = x0 + (x1 - x0) * 0.68, y0 + hh * 0.42
    d.ellipse([cx - 30, cy - 30, cx + 30, cy + 30], fill=(255, 240, 180))
    d.ellipse([cx - 22, cy - 22, cx + 22, cy + 22], fill=(255, 246, 210))
    # skyline silhouettes
    base = y1 - 34
    buildings = [(0.00, 52), (0.08, 84), (0.16, 64), (0.24, 96), (0.33, 70),
                 (0.41, 110), (0.50, 78), (0.58, 92), (0.66, 62), (0.74, 100),
                 (0.82, 72), (0.90, 88), (0.96, 58)]
    wdt = x1 - x0
    for frac, bh in buildings:
        bx = x0 + frac * wdt
        bw = wdt * 0.075
        bx2 = min(bx + bw, x1)
        d.rectangle([bx, base - bh, bx2, base], fill=(42, 26, 62))
        for wy in range(int(base - bh + 8), int(base - 6), 12):
            for wx in range(int(bx + 4), int(bx2 - 3), 9):
                d.rectangle([wx, wy, wx + 3, wy + 4], fill=(255, 214, 120))
    # water strip with light streaks
    d.rectangle([x0, base, x1, y1], fill=(58, 32, 96))
    for i, fx in enumerate([0.12, 0.30, 0.47, 0.63, 0.80, 0.93]):
        sx = x0 + fx * wdt
        d.line([(sx - 26, base + 8 + (i % 3) * 7),
                (sx + 26, base + 8 + (i % 3) * 7)],
               fill=(255, 190, 140), width=2)
    # birds over the skyline
    for bx, by, s in [(0.22, 0.22, 9), (0.30, 0.16, 7), (0.55, 0.14, 8)]:
        px, py = x0 + bx * wdt, y0 + by * hh
        d.line([(px - s, py), (px, py - 4), (px + s, py)],
               fill=(42, 26, 62), width=2)
    d.rectangle([x0, y0, x1, y1], outline=INK, width=1)

def draw_masthead(d):
    f_name = font(SERIF, 58)
    f_small = font(SANS_B, 13)
    f_tag = font(SERIF_REG, 15)
    name = "THE WORLD TODAY"
    nw = d.textlength(name, font=f_name)
    d.text(((W - nw) / 2, 26), name, font=f_name, fill=INK)
    d.line([(28, 96), (996, 96)], fill=INK, width=2)
    d.line([(28, 100), (996, 100)], fill=INK, width=1)
    d.text((28, 106), "THURSDAY", font=f_small, fill=RED)
    date = "19 NOVEMBER 2026"
    dw = d.textlength(date, font=f_small)
    d.text(((W - dw) / 2, 106), date, font=f_small, fill=INK)
    right = "ONE DAY · ONE IMAGE"
    rw = d.textlength(right, font=f_small)
    d.text((996 - rw, 106), right, font=f_small, fill=RED)
    tag = "The whole world, in one picture — the news of today, as it stands this morning."
    tw = d.textlength(tag, font=f_tag)
    d.text(((W - tw) / 2, 126), tag, font=f_tag, fill=MUTED)


def draw_hero(d):
    ax0, ay0, ax1, ay1 = 28, 148, 436, 336
    draw_hero_art(d, ax0, ay0, ax1, ay1)
    tx = 452
    f_kick = font(SANS_B, 12)
    f_head = font(SERIF, 34)
    f_dek = font(SERIF_REG, 16)
    f_body = font(SANS, 13)
    d.text((tx, ay0 + 6), "GAMES  ·  LAUNCH DAY", font=f_kick, fill=RED)
    y = ay0 + 28
    y = text_block(d, tx, y, ["VICE CITY OPENS", "ITS DOORS"], f_head, INK, 36)
    y += 6
    y = text_block(d, tx, y, wrap(d, "After 13 years, Grand Theft Auto VI begins its worldwide rollout.",
                          f_dek, 996 - tx, 1), f_dek, MUTED, 20)
    y += 6
    y = text_block(d, tx, y, wrap(d, "Reviews out Wednesday score it 99 on Metacritic, "
                          "tying the all-time high, as pre-sales pass an estimated "
                          "$1.65 billion. Take-Two rose 7.5% on Wednesday.",
                          f_body, 996 - tx, 2), f_body, INK, 17)
    y = 318
    f_chip = font(SANS_B, 11)
    chips = ["99 METACRITIC", "17.1M COPIES", "$1.65BN PRE-SALES"]
    cx = tx
    for chip in chips:
        cw = d.textlength(chip, font=f_chip) + 16
        d.rounded_rectangle([cx, y, cx + cw, y + 22], radius=4,
                            fill=NAVY, outline=NAVY)
        d.text((cx + 8, y + 4.5), chip, font=f_chip, fill=WHITE)
        cx += cw + 8


def draw_map_section(d):
    f_sec = font(SANS_B, 13)
    d.text((28, 348), "THE DAY AROUND THE WORLD", font=f_sec, fill=RED)
    d.line([(28, 356), (996, 356)], fill=RULE, width=1)
    draw_map(d)
    # legend: three rows, two leads per row
    f_num = font(SANS_B, 12)
    f_leg = font(SANS, 12)
    rows = [(LEADS[0], LEADS[1]), (LEADS[2], LEADS[3]), (LEADS[4], LEADS[5])]
    y = 470
    for left, right in rows:
        for item, lx in ((left, 28), (right, 520)):
            num, _lon, _lat, head, sub, _dx, _dy = item
            d.ellipse([lx, y + 1, lx + 15, y + 16], fill=RED)
            s = str(num)
            sw = d.textlength(s, font=f_num)
            d.text((lx + (15 - sw) / 2, y + 2.5), s, font=f_num, fill=WHITE)
            d.text((lx + 21, y + 2), head, font=f_leg, fill=INK)
            hw = d.textlength(head, font=f_leg)
            d.text((lx + 21 + hw + 6, y + 2), "— " + sub, font=f_leg, fill=MUTED)
        y += 20
    d.line([(28, 538), (996, 538)], fill=INK, width=2)


def draw_columns(d):
    col_w = 306
    col_x = [28, 359, 690]
    top, bottom = 550, 874
    f_tag = font(SANS_B, 11)
    f_head = font(SANS_B, 15)
    f_sum = font(SANS, 12)
    per_col = 4
    slot = (bottom - top) / per_col
    for ci in range(3):
        x = col_x[ci]
        for ri in range(per_col):
            tag, colour, head, summ = STORIES[ci * per_col + ri]
            y = top + ri * slot
            d.text((x, y), tag, font=f_tag, fill=colour)
            y += 15
            y = text_block(d, x, y, wrap(d, head, f_head, col_w, 2),
                           f_head, INK, 18)
            y = text_block(d, x, y, wrap(d, summ, f_sum, col_w, 2),
                           f_sum, MUTED, 15)
    d.line([(28, 880), (996, 880)], fill=INK, width=2)


def draw_numbers(d):
    f_big = font(SERIF, 26)
    f_lab = font(SANS, 11)
    x0, y0 = 28, 892
    bw, bh = 156, 58
    gap = (996 - 28 - 6 * bw) / 5
    for i, (num, lab) in enumerate(NUMBERS):
        x = x0 + i * (bw + gap)
        d.rectangle([x, y0, x + bw, y0 + bh], outline=RULE, width=1)
        nw = d.textlength(num, font=f_big)
        d.text((x + (bw - nw) / 2, y0 + 4), num, font=f_big, fill=RED)
        for j, line in enumerate(wrap(d, lab, f_lab, bw - 12, 2)):
            lw = d.textlength(line, font=f_lab)
            d.text((x + (bw - lw) / 2, y0 + 34 + j * 12), line,
                   font=f_lab, fill=MUTED)


def draw_footer(d):
    f_f = font(SANS, 11)
    d.line([(28, 966), (996, 966)], fill=RULE, width=1)
    line = ("Sources: Reuters · AP · BBC · Nasdaq · India Meteorological Department · "
            "NASA · Sensor Tower · CNBC · The Hindu")
    d.text((28, 974), line, font=f_f, fill=MUTED)
    d.text((28, 990), "All stories are from Thursday 19 November 2026.",
           font=f_f, fill=MUTED)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([10, 10, W - 11, H - 11], outline=INK, width=1)
    draw_masthead(d)
    draw_hero(d)
    draw_map_section(d)
    draw_columns(d)
    draw_numbers(d)
    draw_footer(d)
    img.save(OUT, "PNG", optimize=True)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
