"""Episode 02: Who really pays for Malaysia's petrol subsidies? (figures checked 16 Oct 2026)"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
from engine import *

NOTE = (122, 158, 96); NOTE_D = (86, 120, 66); RICE = (250, 248, 240); YOLK = (244, 176, 40)

# ---------- props ----------
def curve(d, p0, p1, sag, width, fill=INK):
    (x0, y0), (x1, y1) = p0, p1
    L = math.hypot(x1 - x0, y1 - y0) or 1
    cx, cy = (x0 + x1) / 2 - (y1 - y0) / L * sag, (y0 + y1) / 2 + (x1 - x0) / L * sag
    pts = [((1 - u) ** 2 * x0 + 2 * (1 - u) * u * cx + u * u * x1, (1 - u) ** 2 * y0 + 2 * (1 - u) * u * cy + u * u * y1)
           for u in (i / 16 for i in range(17))]
    d.line(pts, fill=fill, width=width, joint="curve")

def pump(d, cx, base, s, price="RM1.99", price_col=INK, face=None, t=0.0):
    if s <= 0.02: return
    w, h = 230 * s, 420 * s
    x0, top = cx - w / 2, base - h
    rrect(d, (cx - w / 2 - 26 * s, base - 30 * s, cx + w / 2 + 26 * s, base), 8 * s, (70, 50, 40))
    rrect(d, (x0, top, x0 + w, base - 30 * s), 30 * s, RED)
    rrect(d, (x0 - 14 * s, top - 44 * s, x0 + w + 14 * s, top + 18 * s), 20 * s, MUSTARD)
    text(d, (cx, top - 12 * s), "RON95", 40 * s, fill=INK, shadow=False, stroke=0)
    rrect(d, (x0 + 22 * s, top + 42 * s, x0 + w - 22 * s, top + 148 * s), 14 * s, CREAM, sh=0, ow=max(2, int(5 * s)))
    text(d, (cx, top + 100 * s), price, 58 * s, fill=price_col, shadow=False, stroke=0)
    curve(d, (x0 + w - 2 * s, base - 80 * s), (x0 + w + 36 * s, top + 232 * s), 46 * s, max(3, int(14 * s)))   # hose
    rrect(d, (x0 + w - 4 * s, top + 196 * s, x0 + w + 54 * s, top + 236 * s), 10 * s, MUSTARD, sh=0, ow=max(2, int(4 * s)))  # nozzle
    rrect(d, (x0 + 32 * s, top + 300 * s, x0 + w - 32 * s, base - 54 * s), 12 * s, (150, 40, 36), sh=0, ow=max(2, int(4 * s)))
    if face:
        lw = max(2, int(6 * s))
        blink = (t % 3.9) < 0.12 and face == "happy"
        big = face == "shock"
        for sx in (-1, 1):
            pie_eye(d, cx + sx * 42 * s, top + 214 * s, (17 if big else 14) * s, (30 if big else 24) * s, RED, closed=blink, lw=lw)
        if big: d.ellipse((cx - 16 * s, top + 248 * s, cx + 16 * s, top + 290 * s), fill=INK)
        else:   d.arc((cx - 34 * s, top + 222 * s, cx + 34 * s, top + 280 * s), 25, 155, fill=INK, width=lw)

def drop(d, cx, cy, r, fill=ORANGE):
    if r <= 10: return
    d.ellipse((cx - r + 6, cy - r + 6, cx + r + 6, cy + r + 6), fill=INK)
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=fill, outline=INK, width=5)
    apex, lft, rgt = (cx, cy - 2.1 * r), (cx - 0.87 * r, cy - 0.5 * r), (cx + 0.87 * r, cy - 0.5 * r)
    d.polygon([apex, lft, rgt, (cx, cy)], fill=fill)
    d.line((apex, lft), fill=INK, width=5); d.line((apex, rgt), fill=INK, width=5)

def coin(d, cx, cy, r, label="RM"):
    if r <= 10: return
    ell(d, (cx - r, cy - r, cx + r, cy + r), MUSTARD, sh=5, ow=5)
    d.ellipse((cx - r + 8, cy - r + 8, cx + r - 8, cy + r - 8), outline=COIN_RIM, width=4)
    text(d, (cx, cy + 3), label, r * 0.8, fill=INK, shadow=False, stroke=0)

def barrel(d, cx, base, s):
    if s <= 0.1: return
    w, h = 220 * s, 300 * s
    rrect(d, (cx - w / 2, base - h, cx + w / 2, base), 26 * s, TEAL)
    for f in (0.3, 0.7):
        y = base - h * f
        d.line((cx - w / 2 + 4, y, cx + w / 2 - 4, y), fill=INK, width=max(3, int(8 * s)))
    d.ellipse((cx - w / 2 + 6, base - h - 16 * s, cx + w / 2 - 6, base - h + 22 * s), fill=(44, 92, 94), outline=INK, width=5)
    drop(d, cx, base - h / 2 + 20 * s, 34 * s, fill=CREAM)

def car(d, cx, base, s, col, tall=False):
    if s <= 0.05: return
    ch = 105 if tall else 78
    poly(d, [(cx - 110 * s, base - 108 * s), (cx - 70 * s, base - (108 + ch) * s), (cx + 80 * s, base - (108 + ch) * s),
             (cx + 125 * s, base - 108 * s)], col, sh=6)
    d.polygon([(cx - 88 * s, base - 112 * s), (cx - 60 * s, base - (104 + ch) * s), (cx + 70 * s, base - (104 + ch) * s),
               (cx + 102 * s, base - 112 * s)], fill=CREAM, outline=INK, width=4)
    d.line((cx + 5 * s, base - 112 * s, cx + 5 * s, base - (104 + ch) * s), fill=INK, width=5)
    rrect(d, (cx - 175 * s, base - 116 * s, cx + 175 * s, base - 34 * s), 30 * s, col)
    for wx in (-108, 108):
        ell(d, (cx + (wx - 38) * s, base - 72 * s, cx + (wx + 38) * s, base + 4 * s), INK, sh=0, ow=4)
        d.ellipse((cx + (wx - 15) * s, base - 49 * s, cx + (wx + 15) * s, base - 19 * s), fill=CREAM)

def note_stack(d, x, base, n, w=180):
    for i in range(n):
        y = base - i * 15
        d.rounded_rectangle((x, y - 15, x + w, y), radius=4, fill=NOTE if i % 2 else NOTE_D, outline=INK, width=3)
    if n:
        y = base - (n - 1) * 15
        text(d, (x + w / 2, y - 8), "RM", 22, fill=CREAM, shadow=False, stroke=2)

def licence(d, cx, cy, s):
    rrect(d, (cx - 230 * s, cy - 145 * s, cx + 230 * s, cy + 145 * s), 24 * s, CREAM)
    d.rounded_rectangle((cx - 227 * s, cy - 142 * s, cx + 227 * s, cy - 82 * s), radius=int(20 * s), fill=TEAL)
    d.line((cx - 227 * s, cy - 82 * s, cx + 227 * s, cy - 82 * s), fill=INK, width=5)
    text(d, (cx, cy - 110 * s), "DRIVING LICENCE", 38 * s, shadow=False, stroke=3)
    rrect(d, (cx - 200 * s, cy - 60 * s, cx - 70 * s, cy + 118 * s), 12 * s, PAPER2, sh=0, ow=4)
    d.ellipse((cx - 162 * s, cy - 36 * s, cx - 108 * s, cy + 18 * s), fill=MUTED)
    d.chord((cx - 190 * s, cy + 22 * s, cx - 80 * s, cy + 150 * s), 180, 360, fill=MUTED)
    for i, wd in enumerate((250, 200, 230, 150)):
        d.rounded_rectangle((cx - 40 * s, cy - 44 * s + i * 42 * s, cx - 40 * s + wd * s, cy - 26 * s + i * 42 * s), radius=6, fill=PAPER2)

def check_badge(d, cx, cy, r, a):
    if a <= 0: return
    r *= ease_back(a)
    ell(d, (cx - r, cy - r, cx + r, cy + r), OLIVE, sh=6, ow=6)
    d.line([(cx - r * 0.45, cy), (cx - r * 0.1, cy + r * 0.35), (cx + r * 0.5, cy - r * 0.35)], fill=CREAM, width=int(r * 0.22), joint="curve")

def gauge(d, cx, cy, R, frac):
    d.pieslice((cx - R + 8, cy - R + 8, cx + R + 8, cy + R + 8), 180, 360, fill=INK)
    d.pieslice((cx - R, cy - R, cx + R, cy + R), 180, 360, fill=CREAM, outline=INK, width=6)
    for k, col in enumerate((RED, MUSTARD, OLIVE)):
        d.arc((cx - R + 22, cy - R + 22, cx + R - 22, cy + R - 22), 180 + k * 60, 240 + k * 60, fill=col, width=22)
    text(d, (cx - R + 50, cy - 26), "E", 40, fill=INK, shadow=False, stroke=0)
    text(d, (cx + R - 50, cy - 26), "F", 40, fill=INK, shadow=False, stroke=0)
    a = math.radians(180 + 180 * frac)
    d.line((cx, cy, cx + (R - 46) * math.cos(a), cy + (R - 46) * math.sin(a)), fill=INK, width=12)
    d.ellipse((cx - 18, cy - 18, cx + 18, cy + 18), fill=INK)
    d.line((cx - R, cy, cx + R, cy), fill=INK, width=6)

def lorry(d, cx, base, s):
    rrect(d, (cx - 175 * s, base - 210 * s, cx + 45 * s, base - 40 * s), 14 * s, MUSTARD)
    rrect(d, (cx + 45 * s, base - 160 * s, cx + 175 * s, base - 40 * s), 18 * s, RED)
    rrect(d, (cx + 80 * s, base - 140 * s, cx + 150 * s, base - 95 * s), 8 * s, CREAM, sh=0, ow=4)
    for wx in (-115, 115):
        ell(d, (cx + (wx - 36) * s, base - 72 * s, cx + (wx + 36) * s, base), INK, sh=0, ow=4)
        d.ellipse((cx + (wx - 14) * s, base - 50 * s, cx + (wx + 14) * s, base - 22 * s), fill=CREAM)

def nasi_lemak(d, cx, cy, s):
    ell(d, (cx - 160 * s, cy - 40 * s, cx + 160 * s, cy + 70 * s), CREAM, sh=8)
    d.ellipse((cx - 135 * s, cy - 28 * s, cx + 135 * s, cy + 56 * s), fill=OLIVE, outline=INK, width=4)    # banana leaf
    d.chord((cx - 95 * s, cy - 110 * s, cx + 35 * s, cy + 40 * s), 180, 360, fill=RICE, outline=INK, width=5)  # rice
    d.ellipse((cx + 20 * s, cy - 30 * s, cx + 110 * s, cy + 22 * s), fill=RICE, outline=INK, width=4)    # egg
    d.ellipse((cx + 48 * s, cy - 16 * s, cx + 82 * s, cy + 10 * s), fill=YOLK)
    d.ellipse((cx - 70 * s, cy + 2 * s, cx + 10 * s, cy + 40 * s), fill=RED, outline=INK, width=4)      # sambal
    for k in range(3):                                                                                  # cucumber
        x = cx + 60 * s + k * 24 * s
        d.ellipse((x - 14 * s, cy + 18 * s, x + 14 * s, cy + 46 * s), fill=(176, 206, 120), outline=INK, width=3)
    for px, py in [(-110, 18), (-100, 34), (-118, 30), (-90, 22)]:                                       # peanuts
        d.ellipse((cx + (px - 7) * s, cy + (py - 5) * s, cx + (px + 7) * s, cy + (py + 5) * s), fill=(196, 140, 84), outline=INK, width=2)

def trolley(d, cx, base, s):
    pts = [(cx - 150 * s, base - 200 * s), (cx + 130 * s, base - 200 * s), (cx + 95 * s, base - 70 * s), (cx - 115 * s, base - 70 * s)]
    poly(d, pts, TEAL, sh=6)
    for k in range(1, 4):
        x = cx - 150 * s + k * 70 * s
        d.line((x, base - 200 * s, x - 9 * s * k / 2 + 5 * s, base - 70 * s), fill=INK, width=3)
    d.line((cx - 140 * s, base - 135 * s, cx + 112 * s, base - 135 * s), fill=INK, width=3)
    d.line((cx - 150 * s, base - 200 * s, cx - 185 * s, base - 245 * s), fill=INK, width=int(10 * s))
    d.line((cx - 115 * s, base - 70 * s, cx - 125 * s, base - 40 * s, cx + 100 * s, base - 40 * s), fill=INK, width=int(8 * s))
    for wx in (-95, 80):
        ell(d, (cx + (wx - 20) * s, base - 40 * s, cx + (wx + 20) * s, base), INK, sh=0, ow=3)

def up_arrow(d, cx, cy, s, a, col=RED):
    if a <= 0: return
    s *= ease_back(a)
    poly(d, [(cx, cy - 70 * s), (cx + 55 * s, cy - 10 * s), (cx + 22 * s, cy - 10 * s), (cx + 22 * s, cy + 60 * s),
             (cx - 22 * s, cy + 60 * s), (cx - 22 * s, cy - 10 * s), (cx - 55 * s, cy - 10 * s)], col, sh=6, ow=5)

# ---------- scenes (t = local seconds); captions sit at CAPTION_Y, keep that lane clear ----------
def s_hook(d, t, sc):
    text(d, (W / 2, 270), "PETROL AT", 96, alpha=prog(t, 0, 0.3))
    text(d, (W / 2, 400), "RM1.99?", 140, fill=MUSTARD, off=9, alpha=prog(t, wt(sc, "one", default=2), 0.3))
    pump(d, W / 2, 930, 0.9 * ease_back(prog(t, 0.1, 0.6)), face="happy", t=t)
    pill(d, W / 2, 1210, "the government pays the rest", CREAM, prog(t, wt(sc, "government", default=3.5), 0.35), size=46, txt=INK)

def s_real(d, t, sc):
    text(d, (W / 2, 270), "THE REAL PRICE", 104, alpha=prog(t, 0, 0.3))
    text(d, (W / 2, 365), "unsubsidised RON95, 15–21 Oct 2026", 44, fill=MUTED, kind="serif", alpha=prog(t, 0.1, 0.3))
    p = ease_out(prog(t, wt(sc, "four", default=2.5) - 0.5, 0.9))
    price = lerp(1.99, 4.62, p)
    shake = math.sin(t * 60) * 6 * (1 - p) if 0 < p < 1 else 0
    pump(d, W / 2 + shake, 930, 0.9, price=f"RM{price:.2f}", price_col=mix(INK, RED, p), face="shock" if p > 0.5 else "happy", t=t)
    pill(d, W / 2, 1180, "you pay RM1.99", TEAL, prog(t, 0.3, 0.35), size=48)
    pill(d, W / 2, 1310, "real price RM4.62", RED, prog(t, wt(sc, "four", default=2.5), 0.35), size=48)

def s_gap(d, t, sc):
    text(d, (W / 2, 270), "EVERY LITRE", 110, alpha=prog(t, 0, 0.3))
    text(d, (W / 2, 365), "RON95 this week", 44, fill=MUTED, kind="serif", alpha=prog(t, 0.1, 0.3))
    x0, x1, y0, y1 = 130, 950, 520, 650
    split = x0 + (x1 - x0) * 1.99 / 4.62
    pa = ease_out(prog(t, 0.2, 0.6)); pb = ease_out(prog(t, wt(sc, "two", default=1.5) - 0.2, 0.7))
    d.rounded_rectangle((x0 + SH, y0 + SH, x1 + SH, y1 + SH), radius=26, fill=INK)
    d.rounded_rectangle((x0, y0, x1, y1), radius=26, fill=PAPER2, outline=INK, width=OW)
    if pa > 0: d.rounded_rectangle((x0, y0, lerp(x0 + 52, split, pa), y1), radius=26, fill=TEAL, outline=INK, width=OW)
    if pb > 0: d.rounded_rectangle((split, y0, lerp(split + 52, x1, pb), y1), radius=26, fill=RED, outline=INK, width=OW)
    text(d, ((x0 + split) / 2, 720), "YOU PAY", 46, alpha=pa)
    text(d, ((x0 + split) / 2, 800), "RM1.99", 70, fill=TEAL, alpha=pa)
    text(d, ((split + x1) / 2, 720), "GOVT PAYS", 46, alpha=pb)
    text(d, ((split + x1) / 2, 800), "≈RM2.63", 70, fill=RED, alpha=pb)
    pill(d, W / 2, 1220, "paid with public money", MUSTARD, prog(t, wt(sc, "public", default=3), 0.35), size=50, txt=INK)

def s_cost(d, t, sc):
    text(d, (W / 2, 260), "FUEL SUBSIDIES", 100, alpha=prog(t, 0, 0.3))
    text(d, (W / 2, 355), "2026 projection · Ministry of Finance", 42, fill=MUTED, kind="serif", alpha=prog(t, 0.1, 0.3))
    p = ease_out(prog(t, wt(sc, "forty", default=2) - 0.3, 1.0))
    if p > 0:
        text(d, (W / 2, 540), f"RM{int(round(40 * p))}", 190, fill=MUSTARD, off=12)
        text(d, (W / 2, 690), "BILLION", 100, alpha=clamp(p * 2))
    pill(d, W / 2, 850, "over RM1,000 per Malaysian", TEAL, prog(t, wt(sc, "thousand", default=4.5), 0.35), size=46)
    for i, x in enumerate((150, 350, 550, 750)):
        n = int(22 * clamp(p * 1.6 - i * 0.18))
        note_stack(d, x, FLOOR_Y - 12, n)

def s_why(d, t, sc):
    text(d, (W / 2, 280), "WHY SO MUCH?", 110, alpha=prog(t, 0, 0.3))
    barrel(d, 360, 900, 1.05 * ease_back(prog(t, 0.2, 0.5)))
    pa = ease_out(prog(t, wt(sc, "pushed", default=2.5) - 0.1, 0.9))
    if pa > 0:
        top = lerp(900, 520, pa)
        d.line((626, 900, 626, top + 50), fill=INK, width=44)
        d.line((620, 900, 620, top + 50), fill=RED, width=32)
        poly(d, [(620, top), (674, top + 70), (566, top + 70)], RED, sh=6, ow=5)
    pl = prog(t, wt(sc, "hundred", default=3.8), 0.3)
    text(d, (790, 560), "US$120+", 62, fill=MUSTARD, alpha=pl)
    text(d, (790, 628), "per barrel", 42, fill=INK, kind="serif", alpha=pl)
    pill(d, W / 2, 1220, "conflict in West Asia", RED, prog(t, wt(sc, "conflict", default=1.5), 0.35), size=52)

def s_twist(d, t, sc):
    text(d, (W / 2, 260), "THE CONTROVERSIAL", 92, alpha=prog(t, 0, 0.3))
    text(d, (W / 2, 370), "PART…", 110, fill=RED, alpha=prog(t, 0.2, 0.3))
    car(d, 290, 900, 0.62 * ease_back(prog(t, 0.3, 0.5)), TEAL)
    car(d, 750, 900, 1.0 * ease_back(prog(t, 0.45, 0.5)), RED, tall=True)
    pd = prog(t, wt(sc, "petrol", default=2.2) - 0.1, 0.35)
    if pd > 0:
        drop(d, 290, 640, 28 * ease_back(pd))
        for k in range(4): drop(d, 650 + k * 66, 620, 28 * ease_back(clamp(pd * 1.5 - k * 0.12)))
    pc = prog(t, wt(sc, "subsidy", default=3.5) - 0.1, 0.35)
    if pc > 0:
        coin(d, 290, 520, 34 * ease_back(pc))
        for k in range(4): coin(d, 650 + k * 66, 500, 34 * ease_back(clamp(pc * 1.5 - k * 0.12)))
    pill(d, W / 2, 1220, "more petrol = more subsidy", MUSTARD, prog(t, wt(sc, "subsidy", default=3.5), 0.35), size=50, txt=INK)

def s_t20(d, t, sc):
    text(d, (W / 2, 260), "EVERY RM1 OF SUBSIDY", 84, alpha=prog(t, 0, 0.3))
    text(d, (W / 2, 350), "Ministry of Finance, 2022", 42, fill=MUTED, kind="serif", alpha=prog(t, 0.1, 0.3))
    x0, x1, y0, y1 = 120, 950, 470, 600
    a1 = x0 + (x1 - x0) * 0.53; a2 = x0 + (x1 - x0) * 0.85
    pr = ease_out(prog(t, wt(sc, "fifty", default=4) - 0.2, 0.6))
    pt = ease_out(prog(t, wt(sc, "fifteen", default=7) - 0.2, 0.6))
    d.rounded_rectangle((x0 + SH, y0 + SH, x1 + SH, y1 + SH), radius=26, fill=INK)
    d.rounded_rectangle((x0, y0, x1, y1), radius=26, fill=PAPER2, outline=INK, width=OW)
    if pt > 0: d.rounded_rectangle((a1, y0, a2, y1), radius=26, fill=MUSTARD, outline=INK, width=OW)
    if pr > 0: d.rounded_rectangle((x0, y0, lerp(x0 + 52, a1, pr), y1), radius=26, fill=RED, outline=INK, width=OW)
    if pt > 0: d.rounded_rectangle((lerp(x1 - 52, a2, pt), y0, x1, y1), radius=26, fill=TEAL, outline=INK, width=OW)
    text(d, ((x0 + a1) / 2, 680), "53 SEN", 64, fill=RED, alpha=pr)
    text(d, ((a1 + a2) / 2, 680), "32", 52, fill=MUSTARD, alpha=pt)
    text(d, ((a2 + x1) / 2, 680), "15", 64, fill=TEAL, alpha=pt)
    text(d, ((x0 + a1) / 2, 755), "richest 20%", 40, fill=INK, kind="serif", alpha=pr)
    text(d, ((a1 + a2) / 2, 755), "middle", 34, fill=INK, kind="serif", alpha=pt)
    text(d, ((a2 + x1) / 2 - 8, 755), "poorest", 34, fill=INK, kind="serif", alpha=pt)
    text(d, ((a2 + x1) / 2 - 8, 795), "40%", 34, fill=INK, kind="serif", alpha=pt)
    pill(d, W / 2, 1190, "richest 20%: 53 sen", RED, prog(t, wt(sc, "richest", default=5.5), 0.35), size=52)
    pill(d, W / 2, 1320, "poorest 40%: 15 sen", TEAL, prog(t, wt(sc, "poorest", default=8.5), 0.35), size=52)

def s_budi(d, t, sc):
    text(d, (W / 2, 280), "BUDI95", 150, fill=MUSTARD, off=10, alpha=prog(t, 0, 0.3))
    a = ease_back(prog(t, 0.2, 0.5))
    if a > 0.02: licence(d, W / 2, 640, a)
    check_badge(d, 750, 520, 60, prog(t, wt(sc, "licence", default=4), 0.4))
    pill(d, W / 2, 860, "RM1.99 a litre", TEAL, prog(t, wt(sc, "cheap", default=4.6), 0.35), size=50)
    fr = ease_out(prog(t, wt(sc, "three", default=5.5) - 0.2, 0.9))
    if prog(t, wt(sc, "up", default=5.2) - 0.3, 0.3) > 0:
        gauge(d, W / 2, 1340, 190, fr)
        text(d, (W / 2, 1420), "300 L / MONTH", 66, alpha=prog(t, wt(sc, "three", default=5.5), 0.3))

def s_flip(d, t, sc):
    text(d, (W / 2, 260), "BUT CUT IT", 104, alpha=prog(t, 0, 0.3))
    text(d, (W / 2, 380), "TOO HARD?", 120, fill=RED, alpha=prog(t, 0.2, 0.3))
    items = [("transport", "TRANSPORT", lambda s: lorry(d, 255, 800, 0.62 * s)),
             ("food", "FOOD", lambda s: nasi_lemak(d, 540, 735, 0.72 * s)),
             ("everything", "EVERYTHING", lambda s: trolley(d, 835, 800, 0.62 * s))]
    for i, (cue, lab, draw_it) in enumerate(items):
        ti = wt(sc, cue, default=2 + i * 1.2)
        a = ease_back(prog(t, ti - 0.1, 0.45))
        if a > 0.02: draw_it(a)
        up_arrow(d, [255, 540, 835][i], 560, 0.8, prog(t, ti + 0.25, 0.35))
        text(d, ([255, 540, 835][i], 870), lab, 38, alpha=prog(t, ti, 0.3))
    pill(d, W / 2, 1220, "poorest families hit first", RED, prog(t, wt(sc, "poorest", default=6.5), 0.35), size=50)

def s_outro(d, t, sc):
    tf = wt(sc, "follow", default=4)
    if t < tf - 0.1:
        text(d, (W / 2, 270), "SHOULD SUBSIDIES", 92, alpha=prog(t, 0, 0.3))
        text(d, (W / 2, 390), "BE CUT?", 130, fill=MUSTARD, off=9, alpha=prog(t, 0.1, 0.3))
        pill(d, 330, 640, "YES", RED, prog(t, 0.5, 0.35), size=96)
        pill(d, 750, 640, "NO", TEAL, prog(t, 0.7, 0.35), size=96)
        pill(d, W / 2, 1220, "comment below!", CREAM, prog(t, wt(sc, "comments", default=2.5), 0.35), size=52, txt=INK)
    else:
        text(d, (W / 2, 280), "THE COMMON", 116, alpha=prog(t, tf, 0.3))
        text(d, (W / 2, 420), "CENTS", 160, fill=MUSTARD, off=10, alpha=prog(t, tf + 0.1, 0.3))
        text(d, (W / 2, 545), "money, explained", 58, fill=MUTED, kind="serif", alpha=prog(t, tf + 0.2, 0.3))
        pill(d, W / 2, 700, "FOLLOW " + HANDLE, RED, prog(t, tf + 0.3, 0.35), size=50)
        hop = abs(math.sin(t * math.pi * 1.8)) * 30
        pump(d, W / 2, FLOOR_Y - 10 - hop, 0.78 * ease_back(prog(t, tf - 0.1, 0.5)), face="happy", t=t)

DRAW = dict(hook=s_hook, real=s_real, gap=s_gap, cost=s_cost, why=s_why, twist=s_twist,
            t20=s_t20, budi=s_budi, flip=s_flip, outro=s_outro)

SUBS = [("RON ninety-five", "RON95"), ("one ringgit ninety-nine", "RM1.99"), ("four ringgit sixty", "RM4.60"),
        ("two ringgit sixty", "RM2.60"), ("forty billion ringgit", "RM40 BILLION"), ("a thousand ringgit", "RM1,000"),
        ("a hundred and twenty US dollars", "US$120"), ("fifty-three sen", "53 SEN"), ("twenty percent", "20%"),
        ("fifteen sen", "15 SEN"), ("poorest forty", "POOREST 40%"), ("BUDI ninety-five", "BUDI95"),
        ("three hundred litres", "300 LITRES"), ("in 2022", "IN 2022")]

run(DRAW, subs=SUBS)
