"""Reusable cartoon props for The Common Cents episodes (same ink-outline / hard-shadow style as engine.py)."""
from engine import *

NOTE = (122, 158, 96); NOTE_D = (86, 120, 66); RICE = (250, 248, 240); YOLK = (244, 176, 40)
SWEAT = (140, 196, 226); SACK = (204, 164, 98)
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

def note_stack(d, x, base, n, w=180):
    for i in range(n):
        y = base - i * 15
        d.rounded_rectangle((x, y - 15, x + w, y), radius=4, fill=NOTE if i % 2 else NOTE_D, outline=INK, width=3)
    if n:
        y = base - (n - 1) * 15
        text(d, (x + w / 2, y - 8), "RM", 22, fill=CREAM, shadow=False, stroke=2)

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


def car(d, cx, base, s, col, tall=False, facing=1, face=None, spin=0.0, t=0.0):
    """Side-view cartoon car (tall=True draws a boxy SUV). facing=1 points right, -1 left.
    face: 'happy' | 'smug' | 'shock' | None (eyes in the windscreen, grin on the front bumper)."""
    if s <= 0.05: return
    X = lambda dx: cx + dx * s * facing
    bt, ch = (150, 100) if tall else (116, 80)                       # body top, cabin height
    cab = [(-150, -140, 100, 132) if tall else (-110, -70, 80, 125)][0]
    poly(d, [(X(cab[0]), base - bt * s), (X(cab[1]), base - (bt + ch) * s), (X(cab[2]), base - (bt + ch) * s),
             (X(cab[3]), base - bt * s)], col, sh=6)
    d.polygon([(X(cab[0] + 22), base - (bt + 4) * s), (X(cab[1] + 12), base - (bt + ch - 8) * s),
               (X(cab[2] - 10), base - (bt + ch - 8) * s), (X(cab[3] - 22), base - (bt + 4) * s)], fill=CREAM, outline=INK, width=4)
    pillar = (cab[0] + cab[3]) / 2 - 25
    d.line((X(pillar), base - (bt + 4) * s, X(pillar), base - (bt + ch - 8) * s), fill=INK, width=5)
    if tall: d.line((X(-130), base - (bt + ch + 12) * s, X(80), base - (bt + ch + 12) * s), fill=INK, width=max(3, int(8 * s)))  # roof rack
    x0, x1 = sorted((X(-180), X(180)))
    rrect(d, (x0, base - bt * s, x1, base - 34 * s), 30 * s, col)
    d.ellipse((X(155) - 15 * s, base - (bt - 18) * s, X(155) + 15 * s, base - (bt - 42) * s), fill=MUSTARD, outline=INK, width=3)
    r = (46 if tall else 38) * s
    for wx in (-110, 110):
        wcx, wcy = X(wx), base - 34 * s
        ell(d, (wcx - r, wcy - r, wcx + r, wcy + r), INK, sh=0, ow=4)
        d.ellipse((wcx - r * 0.4, wcy - r * 0.4, wcx + r * 0.4, wcy + r * 0.4), fill=CREAM)
        for k in range(2):                                          # spokes show the wheel turning
            a = spin + k * math.pi / 2
            d.line((wcx - r * 0.7 * math.cos(a), wcy - r * 0.7 * math.sin(a), wcx + r * 0.7 * math.cos(a), wcy + r * 0.7 * math.sin(a)),
                   fill=CREAM, width=max(2, int(5 * s)))
    if not face: return
    lw = max(3, int(6 * s))
    ex, ey = X((pillar + cab[3] - 22) / 2 + 4), base - (bt + ch * 0.45) * s
    blink = face == "happy" and (t % 3.3) < 0.12
    for dx in (-19, 19):
        px = ex + dx * s
        if face == "smug":
            d.rounded_rectangle((px - 17 * s, ey - 11 * s, px + 17 * s, ey + 11 * s), radius=int(7 * s), fill=INK)
            d.line((px - 10 * s, ey - 5 * s, px - 2 * s, ey - 5 * s), fill=CREAM, width=max(2, int(3 * s)))
        else:
            big = face == "shock"
            pie_eye(d, px, ey, (13 if big else 11) * s, (22 if big else 18) * s, CREAM, closed=blink, lw=lw)
    if face == "smug": d.line((ex - 4 * s, ey - 2 * s, ex + 4 * s, ey - 2 * s), fill=INK, width=lw)
    mx, my = X(138), base - (bt * 0.7) * s
    if face == "shock":
        d.ellipse((mx - 13 * s, my - 15 * s, mx + 13 * s, my + 17 * s), fill=INK)
    elif face == "smug":
        d.arc((mx - 34 * s, my - 30 * s, mx + 34 * s, my + 16 * s), 20 if facing > 0 else 60, 120 if facing > 0 else 160, fill=INK, width=lw + 1)
    else:
        d.chord((mx - 30 * s, my - 18 * s, mx + 30 * s, my + 22 * s), 0, 180, fill=INK)
        d.ellipse((mx - 13 * s, my + 6 * s, mx + 13 * s, my + 20 * s), fill=RED)

def banknote(d, cx, cy, s, ang):
    """A ringgit note rotated by ang (radians)."""
    c, sn = math.cos(ang), math.sin(ang)
    R = lambda w, h: [(cx + x * c - y * sn, cy + x * sn + y * c) for x, y in ((-w, -h), (w, -h), (w, h), (-w, h))]
    d.polygon(R(56 * s, 28 * s), fill=NOTE, outline=INK, width=max(2, int(3 * s)))
    d.polygon(R(40 * s, 16 * s), outline=NOTE_D, width=max(1, int(3 * s)))
    d.ellipse((cx - 9 * s, cy - 9 * s, cx + 9 * s, cy + 9 * s), fill=NOTE_D)

def note_rain(d, t, t0, n=26, seed=1, speed=850, x_range=(150, 930), stop=FLOOR_Y - 20):
    if t < t0: return
    r = random.Random(seed)
    for _ in range(n):
        x0, delay, v, ph, sway = r.uniform(*x_range), r.uniform(0, 1.3), r.uniform(0.7, 1.3), r.uniform(0, 6.3), r.uniform(20, 60)
        y = -60 + (t - t0 - delay) * speed * v
        if -60 < y < stop:
            banknote(d, x0 + math.sin(t * 3 + ph) * sway, y, 0.8, math.sin(t * 4 + ph) * 0.7)

def notes_fly(d, t, t0, src, dst, n=6, dur=0.7, stagger=0.12, seed=3):
    """Notes arcing from src to dst, one after another."""
    r = random.Random(seed)
    for k in range(n):
        u = (t - t0 - k * stagger) / dur
        if 0 <= u <= 1:
            x = lerp(src[0], dst[0], u); y = lerp(src[1], dst[1], u) - math.sin(math.pi * u) * r.uniform(120, 220)
            banknote(d, x, y, 0.7, u * 6 + k)

def moneybag(d, cx, cy, s, label="GOVT"):
    if s <= 0.05: return
    ell(d, (cx - 120 * s, cy - 90 * s, cx + 120 * s, cy + 120 * s), SACK)
    poly(d, [(cx - 40 * s, cy - 82 * s), (cx + 40 * s, cy - 82 * s), (cx + 64 * s, cy - 150 * s), (cx - 64 * s, cy - 150 * s)], SACK, sh=0)
    d.line((cx - 46 * s, cy - 92 * s, cx + 46 * s, cy - 92 * s), fill=INK, width=max(3, int(10 * s)))
    text(d, (cx, cy + 22 * s), "RM", 86 * s, fill=INK, shadow=False, stroke=0)
    if label: text(d, (cx, cy + 160 * s), label, 46 * s)

def sweat(d, cx, cy, t, spread=1.0):
    for k in range(6):
        ph = (t * 1.7 + k / 6) % 1
        side = -1 if k % 2 else 1
        x = cx + side * (40 + 150 * ph) * spread
        y = cy - 120 * ph + 260 * ph * ph
        drop(d, x, y, 16, fill=SWEAT)

def tank(d, cx, top, bottom, frac, col=ORANGE, w=70):
    rrect(d, (cx - w / 2, top, cx + w / 2, bottom), w / 2, CREAM)
    y = max(bottom - (bottom - top) * frac, top + 8)
    if y < bottom - 12:
        d.rounded_rectangle((cx - w / 2 + 8, y, cx + w / 2 - 8, bottom - 8), radius=int(min(w / 2 - 8, (bottom - 8 - y) / 2)), fill=col)
    for k in range(1, 4):
        y = bottom - (bottom - top) * k / 4
        d.line((cx - w / 2 + 2, y, cx - w / 2 + 18, y), fill=INK, width=4)

def top_hat(d, cx, base, s):
    if s <= 0.05: return
    rrect(d, (cx - 46 * s, base - 112 * s, cx + 46 * s, base), 8 * s, INK, sh=6, ow=3)
    d.rectangle((cx - 44 * s, base - 38 * s, cx + 44 * s, base - 18 * s), fill=RED)
    d.ellipse((cx - 76 * s, base - 14 * s, cx + 76 * s, base + 12 * s), fill=INK)

def stamp(d, cx, cy, label, a, col=RED, ang=-12):
    """Rubber-stamp slam: starts big and see-through, lands at size 1 (a: 0..1)."""
    if a <= 0: return
    sc = lerp(2.2, 1.0, ease_out(a))
    f = F(int(110 * sc)); w = d.textlength(label, font=f)
    layer = Image.new("RGBA", (int(w + 120 * sc), int(220 * sc)), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    alpha = int(255 * clamp(a * 2))
    ld.rounded_rectangle((10, 10, layer.width - 10, layer.height - 10), radius=int(24 * sc), outline=col + (alpha,), width=int(14 * sc))
    ld.text((layer.width / 2, layer.height / 2 + 6 * sc), label, font=f, fill=col + (alpha,), anchor="mm")
    layer = layer.rotate(ang, expand=True, resample=Image.BICUBIC)
    d._image.paste(layer, (int(cx - layer.width / 2), int(cy - layer.height / 2)), layer)

def clock(d, cx, cy, r, t, speed=1.0):
    if r <= 8: return
    ell(d, (cx - r, cy - r, cx + r, cy + r), CREAM, sh=7)
    for k in range(12):
        a = k * math.pi / 6
        d.line((cx + r * 0.78 * math.cos(a), cy + r * 0.78 * math.sin(a), cx + r * 0.9 * math.cos(a), cy + r * 0.9 * math.sin(a)),
               fill=INK, width=max(2, int(r / 18)))
    for frac, ln, wd in ((t * speed / 12, 0.45, r / 9), (t * speed, 0.72, r / 14)):     # hour / minute hands
        a = 2 * math.pi * frac - math.pi / 2
        d.line((cx, cy, cx + r * ln * math.cos(a), cy + r * ln * math.sin(a)), fill=INK, width=max(2, int(wd)))
    d.ellipse((cx - r / 10, cy - r / 10, cx + r / 10, cy + r / 10), fill=RED)

def train(d, x, base, s, cars=3, col=TEAL, riders=None):
    """Commuter train heading right; x is the nose. riders: list of 0/1 per window (who's on board)."""
    seg = 300 * s
    for k in range(cars):
        x1 = x - k * (seg + 12 * s); x0 = x1 - seg
        rrect(d, (x0, base - 150 * s, x1, base - 20 * s), (40 if k == 0 else 14) * s, col)
        d.rectangle((x0 + 4, base - 62 * s, x1 - 4, base - 50 * s), fill=MUSTARD)
        for w in range(4):
            wx = x0 + 28 * s + w * 64 * s
            d.rounded_rectangle((wx, base - 130 * s, wx + 46 * s, base - 82 * s), radius=int(8 * s), fill=CREAM, outline=INK, width=3)
            i = k * 4 + w
            if riders and i < len(riders) and riders[i]:
                d.ellipse((wx + 13 * s, base - 120 * s, wx + 33 * s, base - 100 * s), fill=MUTED)
                d.chord((wx + 6 * s, base - 102 * s, wx + 40 * s, base - 70 * s), 180, 360, fill=MUTED)
        for wx in (x0 + 50 * s, x1 - 50 * s):
            d.ellipse((wx - 20 * s, base - 40 * s, wx + 20 * s, base), fill=INK)
    d.line((x - cars * (seg + 12 * s) - 40, base + 2, x + 40, base + 2), fill=INK, width=max(3, int(8 * s)))

def house(d, cx, base, s):
    rrect(d, (cx - 90 * s, base - 140 * s, cx + 90 * s, base), 6 * s, PAPER2)
    poly(d, [(cx - 115 * s, base - 130 * s), (cx, base - 230 * s), (cx + 115 * s, base - 130 * s)], RED, sh=6)
    rrect(d, (cx - 25 * s, base - 80 * s, cx + 25 * s, base), 6 * s, TEAL, sh=0, ow=4)
    rrect(d, (cx + 38 * s, base - 110 * s, cx + 74 * s, base - 74 * s), 4 * s, MUSTARD, sh=0, ow=4)

def station(d, cx, base, s):
    rrect(d, (cx - 130 * s, base - 170 * s, cx + 130 * s, base), 10 * s, CREAM)
    rrect(d, (cx - 150 * s, base - 215 * s, cx + 150 * s, base - 160 * s), 14 * s, TEAL)
    text(d, (cx, base - 186 * s), "STATION", 40 * s, shadow=False, stroke=3)
    for k in range(3):
        x = cx - 95 * s + k * 70 * s
        d.rounded_rectangle((x, base - 130 * s, x + 50 * s, base - 30 * s), radius=int(8 * s), fill=MUSTARD, outline=INK, width=4)

def price_tag(d, cx, cy, label, a, col=MUSTARD, ang=-8, size=96):
    """Swing-tag that drops in from above (a: 0..1)."""
    if a <= 0: return
    f = F(size); w = d.textlength(label, font=f)
    lw_, lh = int(w + 170), int(size * 1.9)
    layer = Image.new("RGBA", (lw_ + 40, lh + 40), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    pts = lambda o: [(20 + o, lh / 2 + 20 + o), (90 + o, 20 + o), (lw_ + o, 20 + o), (lw_ + o, lh + 20 + o), (90 + o, lh + 20 + o)]
    ld.polygon(pts(10), fill=INK + (255,))
    ld.polygon(pts(0), fill=col + (255,), outline=INK + (255,), width=7)
    ld.ellipse((60, lh / 2 + 6, 88, lh / 2 + 34), fill=CREAM + (255,), outline=INK + (255,), width=5)
    ld.text(((lw_ + 90) / 2 + 10, lh / 2 + 24), label, font=f, fill=INK + (255,), anchor="mm")
    layer = layer.rotate(ang + (1 - ease_out(a)) * 25, expand=True, resample=Image.BICUBIC)
    y = cy - (1 - ease_back(a, 1.2)) * 500
    d._image.paste(layer, (int(cx - layer.width / 2), int(y - layer.height / 2)), layer)

def topcar(d, cx, cy, col, s=1.0):
    """Top-down car pointing right (for highway scenes)."""
    rrect(d, (cx - 52 * s, cy - 26 * s, cx + 52 * s, cy + 26 * s), 14 * s, col, sh=4, ow=4)
    d.rounded_rectangle((cx + 6 * s, cy - 19 * s, cx + 30 * s, cy + 19 * s), radius=int(6 * s), fill=CREAM, outline=INK, width=3)
    d.rounded_rectangle((cx - 38 * s, cy - 17 * s, cx - 22 * s, cy + 17 * s), radius=int(5 * s), fill=CREAM, outline=INK, width=3)

def road(d, x0, x1, top, lanes, lane_h=110):
    bot = top + lanes * lane_h
    d.rectangle((x0, top - 14, x1, bot + 14), fill=(96, 88, 80), outline=INK, width=5)
    for k in range(1, lanes):
        y = top + k * lane_h
        for x in range(int(x0) + 10, int(x1) - 30, 70):
            d.line((x, y, x + 36, y), fill=CREAM, width=6)
    return bot

def end_card(d, t, tf, hero=None):
    """Channel end card shown from tf - 0.1: title, tagline, follow pill, and a bouncing hero prop.
    hero(scale, hop) draws the episode's bouncing prop standing on the floor."""
    text(d, (W / 2, 280), "THE COMMON", 116, alpha=prog(t, tf, 0.25))
    text(d, (W / 2, 420), "CENTS", 160, fill=MUSTARD, off=10, alpha=prog(t, tf + 0.1, 0.25))
    text(d, (W / 2, 545), "money, explained", 58, fill=MUTED, kind="serif", alpha=prog(t, tf + 0.2, 0.25))
    pill(d, W / 2, 700, "FOLLOW " + HANDLE, RED, prog(t, tf + 0.3, 0.3), size=50)
    if hero:
        hero(ease_back(prog(t, tf - 0.1, 0.45)), abs(math.sin(t * math.pi * 1.8)) * 30)

def shop(d, cx, base, s, sign="KEDAI", col=TEAL):
    if s <= 0.05: return
    rrect(d, (cx - 160 * s, base - 220 * s, cx + 160 * s, base), 10 * s, CREAM)
    rrect(d, (cx - 180 * s, base - 300 * s, cx + 180 * s, base - 235 * s), 14 * s, col)
    text(d, (cx, base - 266 * s), sign, 44 * s, shadow=False, stroke=3)
    for k in range(6):                                            # striped awning
        x0 = cx - 180 * s + k * 60 * s
        d.polygon([(x0, base - 235 * s), (x0 + 60 * s, base - 235 * s), (x0 + 60 * s, base - 195 * s), (x0, base - 195 * s)],
                  fill=RED if k % 2 == 0 else CREAM, outline=INK)
    rrect(d, (cx - 40 * s, base - 150 * s, cx + 40 * s, base), 6 * s, MUSTARD, sh=0, ow=4)
    rrect(d, (cx - 140 * s, base - 160 * s, cx - 60 * s, base - 80 * s), 6 * s, PAPER2, sh=0, ow=4)
    rrect(d, (cx + 60 * s, base - 160 * s, cx + 140 * s, base - 80 * s), 6 * s, PAPER2, sh=0, ow=4)

def worker(d, cx, base, s, col=TEAL, t=0.0, wave=False):
    """Little cartoon person (head, body, arms) standing on base."""
    if s <= 0.05: return
    lw = max(3, int(8 * s))
    arm = -0.9 + 0.35 * math.sin(t * 8) if wave else 0.6
    for side in (-1, 1):
        a = arm if side > 0 else 0.6
        d.line((cx + side * 34 * s, base - 120 * s, cx + side * (34 + 40 * math.cos(a)) * s, base - (120 - 40 * math.sin(a)) * s),
               fill=INK, width=lw)
    rrect(d, (cx - 36 * s, base - 140 * s, cx + 36 * s, base), 22 * s, col, sh=5, ow=max(2, int(5 * s)))
    ell(d, (cx - 30 * s, base - 200 * s, cx + 30 * s, base - 140 * s), CREAM, sh=4, ow=max(2, int(5 * s)))
    for dx in (-10, 10):
        d.ellipse((cx + (dx - 4) * s, base - 178 * s, cx + (dx + 4) * s, base - 166 * s), fill=INK)
    d.arc((cx - 12 * s, base - 172 * s, cx + 12 * s, base - 154 * s), 20, 160, fill=INK, width=max(2, int(4 * s)))

def receipt(d, cx, cy, s, lines=("SHOES", "RM1,000"), ang=0.0):
    if s <= 0.05: return
    w, h = 210 * s, 300 * s
    pts = [(cx - w / 2, cy - h / 2), (cx + w / 2, cy - h / 2)]
    for k in range(9):                                            # torn zigzag bottom
        pts.append((cx + w / 2 - k * w / 8, cy + h / 2 - (12 * s if k % 2 else 0)))
    poly(d, pts, CREAM, sh=7, ow=5)
    text(d, (cx, cy - h / 2 + 40 * s), "RECEIPT", 34 * s, fill=INK, shadow=False, stroke=0)
    for k in range(3):
        y = cy - 50 * s + k * 30 * s
        d.line((cx - 70 * s, y, cx + 70 * s, y), fill=PAPER2, width=max(2, int(8 * s)))
    text(d, (cx, cy + 60 * s), lines[0], 34 * s, fill=MUTED, kind="serif", shadow=False)
    text(d, (cx, cy + 105 * s), lines[1], 42 * s, fill=INK, shadow=False, stroke=0)

def shoe(d, cx, base, s, col=RED):
    if s <= 0.05: return
    poly(d, [(cx - 120 * s, base - 30 * s), (cx - 110 * s, base - 110 * s), (cx - 40 * s, base - 120 * s), (cx + 10 * s, base - 70 * s),
             (cx + 110 * s, base - 50 * s), (cx + 130 * s, base - 20 * s)], col, sh=6, ow=5)
    rrect(d, (cx - 128 * s, base - 34 * s, cx + 136 * s, base), 14 * s, CREAM, sh=0, ow=5)
    for k in range(3):
        x = cx - 60 * s + k * 26 * s
        d.line((x, base - 100 * s + k * 8 * s, x + 24 * s, base - 84 * s + k * 8 * s), fill=CREAM, width=max(2, int(6 * s)))

def line_chart(d, x0, y0, x1, y1, values, prog_, col=RED):
    """Axes + a line through `values` (0..1 heights) revealed left-to-right by prog_."""
    d.line((x0, y0, x0, y1, x1, y1), fill=INK, width=6)
    n = len(values) - 1
    pts = [(x0 + (x1 - x0) * i / n, y1 - (y1 - y0) * v) for i, v in enumerate(values)]
    upto = prog_ * n
    shown = [p for i, p in enumerate(pts) if i <= upto]
    if 0 < upto < n:
        i = int(upto); f = upto - i
        shown.append((lerp(pts[i][0], pts[i + 1][0], f), lerp(pts[i][1], pts[i + 1][1], f)))
    if len(shown) > 1:
        d.line([(x + 6, y + 6) for x, y in shown], fill=INK, width=14, joint="curve")
        d.line(shown, fill=col, width=12, joint="curve")
        ex, ey = shown[-1]
        ell(d, (ex - 16, ey - 16, ex + 16, ey + 16), col, sh=4, ow=4)

def seesaw(d, cx, cy, L, tilt_deg, left=None, right=None, col=TEAL):
    r = math.radians(tilt_deg)
    lx, ly = cx - L * math.cos(r), cy - L * math.sin(r)
    rx, ry = cx + L * math.cos(r), cy + L * math.sin(r)
    poly(d, [(cx, cy), (cx - 80, cy + 230), (cx + 80, cy + 230)], col)
    d.line((lx + 8, ly + 8, rx + 8, ry + 8), fill=INK, width=24)
    d.line((lx, ly, rx, ry), fill=ORANGE, width=24)
    if left: left(lx, ly)
    if right: right(rx, ry)
