"""Episode 01: Why does a Big Mac cost different prices around the world?"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
from engine import *

# ---------- scenes (t = local seconds) ----------
# Layout keeps a caption lane clear around CAPTION_Y (screen centre): headlines/main visuals above it,
# secondary elements below it. Only tall bars/buildings pass behind the captions.
def s_hook(d, t, sc):
    a = ease_back(prog(t, 0.0, 0.6))
    burger(d, W / 2, 700, 0.95 * a, t=t)
    text(d, (W / 2, 280), "SAME BURGER.", 112, alpha=prog(t, 0.2, 0.3))
    text(d, (W / 2, 410), "EVERYWHERE!", 112, fill=MUSTARD, alpha=prog(t, wt(sc, "everywhere"), 0.3))
    for i, (w_, lab) in enumerate([("bun", "same bun"), ("patties", "same patties"), ("sauce", "same sauce")]):
        pill(d, W / 2, 1150 + i * 120, lab, CREAM, prog(t, wt(sc, w_, default=2 + i), 0.35), size=46, txt=INK)

def s_prices(d, t, sc):
    text(d, (W / 2, 270), "PRICE OF ONE BIG MAC", 80, alpha=prog(t, 0, 0.3))
    text(d, (W / 2, 362), "approx., in US dollars", 46, fill=MUTED, kind="serif", alpha=prog(t, 0, 0.3))
    rows = [("Switzerland", 8.00, RED, "switzerland"), ("USA", 6.00, TEAL, "six"), ("Taiwan", 2.40, OLIVE, "taiwan")]
    for i, (name, v, col, cue) in enumerate(rows):
        y = 505 + i * 185
        p = ease_out(prog(t, wt(sc, cue, default=1 + i) - 0.15, 0.7))
        text(d, (150, y - 66), name, 54, fill=INK, kind="serif", anchor="lm", alpha=clamp(p * 3))
        bw = 560 * (v / 8.0) * p
        if bw > 12: rrect(d, (150, y - 16, 150 + bw, y + 60), 18, col)
        if p > 0: text(d, (180 + bw + 20, y + 24), f"${v * p:.2f}", 64, anchor="lm", alpha=clamp(p * 3))

def s_beef(d, t, sc):
    tn = wt(sc, "everything", default=1.3)
    if t < tn:
        rrect(d, (W / 2 - 250, 560, W / 2 + 250, 720), 60, PATTY)
        x = ease_out(prog(t, wt(sc, "not", default=0.4), 0.3))
        if x > 0:
            for sgn in (1, -1):
                seg = (W / 2 - 290 * x, 640 - 200 * x * sgn, W / 2 + 290 * x, 640 + 200 * x * sgn)
                d.line([(p + 8) for p in seg], fill=INK, width=40)
                d.line(seg, fill=RED, width=34)
        text(d, (W / 2, 250), "IT'S NOT", 130, alpha=prog(t, 0, 0.25))
        text(d, (W / 2, 1200), "THE BEEF!", 140, fill=RED, alpha=prog(t, 0.1, 0.25))
    else:
        a = prog(t, tn, 0.3)
        r = 260 * ease_back(a)
        burger(d, W / 2, 620, 0.6, t=t)
        for k in range(10):
            ang = k / 10 * 2 * math.pi + t * 0.8
            px, py = W / 2 + math.cos(ang) * r, 620 + math.sin(ang) * r
            ell(d, (px - 24, py - 24, px + 24, py + 24), [MUSTARD, RED, OLIVE, TEAL, ORANGE][k % 5], sh=5, ow=4)
        text(d, (W / 2, 1180), "IT'S EVERYTHING", 104, alpha=a)
        text(d, (W / 2, 1310), "AROUND IT", 104, fill=MUSTARD, alpha=a)

def s_wages(d, t, sc):
    header(d, 1, "WAGES", t)
    text(d, (W / 2, 425), "hourly pay at McDonald's", 48, fill=MUTED, kind="serif", alpha=prog(t, 0.3, 0.3))
    base = FLOOR_Y - 10
    for i, (name, h, col, cue) in enumerate([("Switzerland", 700, RED, "swiss"), ("Taiwan", 165, TEAL, "taiwan")]):
        x = 220 + i * 360
        p = ease_out(prog(t, wt(sc, cue, default=1.5 + i) - 0.1, 0.8))
        hh = h * p
        if hh > 12: rrect(d, (x, base - hh, x + 220, base), 20, col)
        if p > 0: text(d, (x + 110, base - hh - 50), name, 46, fill=INK, kind="serif", alpha=clamp(p * 3))
        for c in range(int((hh - 10) // 60)):
            text(d, (x + 110, base - 36 - c * 60), "$", 44, shadow=False, stroke=3)
    pa = ease_back(prog(t, wt(sc, "several", default=3), 0.45))
    if pa > 0:
        cx, cy = 790, 620
        rrect(d, (cx - 140 * pa, cy - 70 * pa, cx + 140 * pa, cy + 70 * pa), 34 * pa, MUSTARD)
        if pa > 0.5: text(d, (cx, cy + 6), "≈4–5×", 80, fill=INK, shadow=False, stroke=0)

def s_rent(d, t, sc):
    header(d, 2, "RENT", t)
    text(d, (W / 2, 425), "cost of space for a restaurant", 48, fill=MUTED, kind="serif", alpha=prog(t, 0.3, 0.3))
    base = FLOOR_Y - 10
    tz, tp = wt(sc, "zurich", default=1.5), wt(sc, "taipei", default=3.5)
    building(d, 200, base, 300, 720, RED, prog(t, tz - 0.1, 0.8))
    building(d, 600, base, 260, 300, TEAL, prog(t, tp - 0.1, 0.8))
    text(d, (350, base - 770), "Zurich $$$$", 60, alpha=prog(t, tz, 0.3))
    text(d, (730, base - 350), "Taipei $", 54, alpha=prog(t, tp, 0.3))

def s_local(d, t, sc):
    header(d, 3, "LOCAL COSTS", t)
    items = [("taxes", "Taxes", "%"), ("energy", "Energy", "bolt"), ("ingredients", "Ingredients", "burger")]
    for i, (cue, lab, icon) in enumerate(items):
        p = ease_out(prog(t, wt(sc, cue, default=2 + i) - 0.1, 0.45))
        if p <= 0: continue
        y = 480 + i * 165; x = lerp(W + 50, 150, p)
        rrect(d, (x, y - 70, x + 780, y + 70), 36, CREAM)
        ell(d, (x + 36, y - 52, x + 140, y + 52), MUSTARD, sh=0, ow=5)
        if icon == "%": text(d, (x + 88, y + 5), "%", 64, fill=INK, shadow=False, stroke=0)
        elif icon == "bolt": bolt(d, x + 88, y, 0.7, ORANGE)
        else: burger(d, x + 88, y + 12, 0.18, shadow=False)
        text(d, (x + 180, y + 4), lab, 62, fill=INK, kind="serif", anchor="lm")
    tl = wt(sc, "locally", default=4)
    if t > tl: pill(d, W / 2, 1220, "priced locally", RED, prog(t, tl, 0.35), size=52)

def s_index(d, t, sc):
    t86 = wt(sc, "1986", default=wt(sc, "in", default=2.5))
    ti = wt(sc, "big", default=4.5)
    if t < ti:
        text(d, (W / 2, 290), "ECONOMISTS LOVE", 84, alpha=prog(t, 0, 0.3))
        text(d, (W / 2, 390), "THIS BURGER", 84, fill=MUSTARD, alpha=prog(t, 0.1, 0.3))
        p = ease_out(prog(t, t86 - 0.3, 0.9))
        if p > 0: text(d, (W / 2, 690), str(int(lerp(2026, 1986, p))), 280, fill=MUSTARD, off=12)
        burger(d, W / 2, 1270, 0.55 * ease_back(prog(t, 0.1, 0.5)), t=t)
    else:
        a = ease_back(prog(t, ti, 0.5))
        rrect(d, (150, 230, 930, 900), 50, CREAM)
        sunburst(d, W / 2, 470, t, R=250, col=PAPER2)
        burger(d, W / 2, 500, 0.62 * a, t=t)
        text(d, (W / 2, 720), "THE BIG MAC", 100, alpha=prog(t, ti, 0.3))
        text(d, (W / 2, 830), "INDEX", 100, fill=RED, alpha=prog(t, ti + 0.15, 0.3))
        text(d, (W / 2, 1170), "since 1986 · The Economist", 50, fill=MUTED, kind="serif", alpha=prog(t, ti + 0.3, 0.3))

def s_fx(d, t, sc):
    to, tu = wt(sc, "overvalued", default=4.5), wt(sc, "undervalued", default=6)
    text(d, (W / 2, 280), "SAME BURGER,", 88, alpha=prog(t, 0, 0.3))
    text(d, (W / 2, 385), "DIFFERENT PRICE?", 88, fill=MUSTARD, alpha=prog(t, 0.1, 0.3))
    tilt = lerp(0, -14, ease_out(prog(t, to - 0.1, 0.5)))
    tilt = lerp(tilt, 14, ease_out(prog(t, tu - 0.1, 0.5)))
    cx, cy, L = W / 2, 660, 320
    r = math.radians(tilt)
    lx, ly = cx - L * math.cos(r), cy - L * math.sin(r)
    rx, ry = cx + L * math.cos(r), cy + L * math.sin(r)
    poly(d, [(cx, cy), (cx - 80, cy + 250), (cx + 80, cy + 250)], TEAL)
    d.line((lx + 8, ly + 8, rx + 8, ry + 8), fill=INK, width=24)
    d.line((lx, ly, rx, ry), fill=ORANGE, width=24)
    ell(d, (lx - 80, ly - 172, lx + 80, ly - 12), MUSTARD)
    text(d, (lx, ly - 88), "$", 104, fill=INK, shadow=False, stroke=0)
    burger(d, rx, ry - 70, 0.33, face=False)
    if t >= to - 0.1:
        lab, col, cue = ("OVERVALUED", RED, to) if t < tu - 0.1 else ("UNDERVALUED", OLIVE, tu)
        pill(d, W / 2, 1210, lab, col, prog(t, cue, 0.3), size=62)

def s_caveat(d, t, sc):
    text(d, (W / 2, 320), "BUT…", 150, fill=MUSTARD, off=10, alpha=prog(t, 0, 0.25))
    a = prog(t, wt(sc, "cheap", default=0.5), 0.3)
    burger(d, W / 2 - 170, 590, 0.5 * ease_back(a), t=t)
    text(d, (W / 2 - 20, 610), "CHEAP", 96, anchor="lm", alpha=a)
    b = prog(t, wt(sc, "life", default=2), 0.3)
    text(d, (W / 2, 790), "=", 120, alpha=b)
    pill(d, W / 2, 1200, "lower cost of living", TEAL, b, size=60)

def s_outro(d, t, sc):
    tf = wt(sc, "follow", default=3)
    if t < tf - 0.1:
        a = ease_back(prog(t, 0, 0.5))
        R = 240 * a
        if R > 5:
            ell(d, (W / 2 - R, 640 - R, W / 2 + R, 640 + R), TEAL)
            for k in (-1, 1):
                ell(d, (W / 2 + k * 100 * a - 75 * a, 640 - 135 * a + k * 120 * a, W / 2 + k * 100 * a + 50 * a, 640 - 35 * a + k * 120 * a), OLIVE, sh=0, ow=5)
        burger(d, W / 2, 665, 0.48 * a, t=t)
        text(d, (W / 2, 280), "TRAVELLING?", 112, alpha=prog(t, 0, 0.3))
        text(d, (W / 2, 1200), "CHECK THE BIG MAC PRICE!", 66, fill=MUSTARD, alpha=prog(t, wt(sc, "check", default=1.5), 0.3))
    else:
        text(d, (W / 2, 280), "THE COMMON", 116, alpha=prog(t, tf, 0.3))
        text(d, (W / 2, 420), "CENTS", 160, fill=MUSTARD, off=10, alpha=prog(t, tf + 0.1, 0.3))
        text(d, (W / 2, 545), "money, explained", 58, fill=MUTED, kind="serif", alpha=prog(t, tf + 0.2, 0.3))
        pill(d, W / 2, 700, "FOLLOW " + HANDLE, RED, prog(t, tf + 0.3, 0.35), size=50)
        hop = abs(math.sin(t * math.pi * 1.8)) * 30
        burger(d, W / 2, 1290 - hop, 0.85 * ease_back(prog(t, tf - 0.1, 0.5)), t=t)

DRAW = dict(hook=s_hook, prices=s_prices, beef=s_beef, wages=s_wages, rent=s_rent,
            local=s_local, index=s_index, fx=s_fx, caveat=s_caveat, outro=s_outro)


run(DRAW)
