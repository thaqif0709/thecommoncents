"""Episode 03: Why is Malaysia always jammed? (figures checked 16 Oct 2026)"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
from engine import *
from props import *

JAM_COLS = [TEAL, RED, MUSTARD, OLIVE, ORANGE, (120, 96, 150)]

def jam_row(d, t, base=FLOOR_Y - 12, s=0.42, gap=205, speed=6, seed=0, faces=False):
    """Bumper-to-bumper cars along the floor, creeping forward."""
    off = (t * speed) % gap
    for k in range(-1, 6):
        x = 70 + k * gap + off
        col = JAM_COLS[(k + seed) % len(JAM_COLS)]
        car(d, x, base, s, col, tall=(k + seed) % 3 == 1, face="shock" if faces and k == 2 else None,
            spin=x / 30, t=t)

# ---------- scenes (t = local seconds); captions sit at CAPTION_Y, keep that lane clear ----------
def s_hook(d, t, sc):
    text(d, (W / 2, 260), "YOU SPENT", 100, alpha=prog(t, 0.05, 0.2))
    p = ease_out(prog(t, wt(sc, "three", default=0.5) - 0.1, 0.7))
    if p > 0:
        text(d, (W / 2, 470), f"{3.5 * p:.1f} DAYS", 190, fill=MUSTARD, off=12)
    text(d, (W / 2, 610), "sitting in traffic", 62, fill=INK, kind="serif", alpha=prog(t, wt(sc, "sitting", default=2.6), 0.25))
    clock(d, W / 2, 800, 95 * ease_back(prog(t, 0.2, 0.4)), t, speed=6)
    jam_row(d, t, faces=True)

def s_why(d, t, sc):
    te = wt(sc, "eighty-four", default=0.3)
    clock(d, W / 2, 470, 150, t + 30, speed=6)
    stamp(d, W / 2, 470, "84 HOURS", prog(t, te, 0.18))
    text(d, (W / 2, 680), "KL rush hour, 2025 · TomTom", 44, fill=MUTED, kind="serif", alpha=prog(t, te + 0.2, 0.25))
    tw = wt(sc, "why", default=2.5)
    text(d, (W / 2, 260), "WHY?", 130, fill=RED, alpha=prog(t, tw, 0.2))
    pill(d, W / 2, 830, "driving = the easy option", TEAL, prog(t, wt(sc, "easy", default=5.2), 0.3), size=52)
    jam_row(d, t, seed=2)

CAR_PILE = [(x + (row % 2) * 115, FLOOR_Y - 12 - row * 92) for row in range(4) for x in (190, 420, 650, 880) if not (row % 2 and x == 880)]

def s_cars(d, t, sc):
    tf = wt(sc, "forty", default=0.3)
    p = ease_out(prog(t, tf - 0.2, 1.4))
    if p > 0:
        text(d, (W / 2, 300), f"{40.8 * p:.1f}", 200, fill=MUSTARD, off=12)
        text(d, (W / 2, 450), "MILLION VEHICLES", 84, alpha=clamp(p * 3))
        text(d, (W / 2, 535), "registered (26.6M still active)", 42, fill=MUTED, kind="serif", alpha=clamp(p * 3))
    pill(d, W / 2, 700, "more vehicles than Malaysians", RED, prog(t, wt(sc, "more", default=2.8), 0.3), size=50)
    for i, (x, y) in enumerate(CAR_PILE):                       # cars rain down and pile up
        t0 = tf - 0.1 + i * 0.16
        u = t - t0
        if u <= 0: continue
        fall = min(1.0, u / 0.35)
        yy = lerp(-200, y, fall * fall)
        if fall >= 1: yy = y - abs(math.sin(min(u - 0.35, 0.3) / 0.3 * math.pi)) * 18 * (1 - min(1, (u - 0.35) / 0.3))
        car(d, x, yy, 0.42, JAM_COLS[i % len(JAM_COLS)], tall=i % 3 == 1)

def s_cheap(d, t, sc):
    text(d, (W / 2, 260), "DRIVING IS CHEAP", 100, alpha=prog(t, 0.05, 0.2))
    cards = [("petrol", "subsidised", "RM1.99"), ("loans", "car loans", "9 YEARS"), ("national", "national cars", "LOW PRICES")]
    for i, (cue, lab, big) in enumerate(cards):
        a = ease_back(prog(t, wt(sc, cue, default=0.2 + i * 1.8) - 0.1, 0.4))
        if a <= 0.02: continue
        cx = [250, 540, 830][i]; cy = 600 + (1 - a) * 80
        rrect(d, (cx - 135, cy - 230, cx + 135, cy + 230), 26, CREAM)
        if i == 0: pump(d, cx, cy + 40, 0.48, face="happy", t=t)
        elif i == 1:
            rrect(d, (cx - 80, cy - 150, cx + 80, cy + 10), 14, PAPER2, sh=0, ow=5)
            d.rectangle((cx - 77, cy - 147, cx + 77, cy - 110), fill=RED)
            text(d, (cx, cy - 45), "9", 110, fill=INK, shadow=False, stroke=0)
        else: car(d, cx, cy + 20, 0.62, TEAL, face="happy", t=t)
        text(d, (cx, cy + 105), big, 46 if len(big) > 7 else 56, fill=MUSTARD if i else TEAL, alpha=a)
        text(d, (cx, cy + 170), lab, 36, fill=INK, kind="serif", alpha=a)
    pill(d, W / 2, 1230, "cheap to drive", RED, prog(t, wt(sc, "low", default=5.3), 0.3), size=56)

def s_trains(d, t, sc):
    text(d, (W / 2, 260), "PUBLIC TRANSPORT", 96, alpha=prog(t, 0.05, 0.2))
    text(d, (W / 2, 350), "share of trips, Klang Valley", 44, fill=MUTED, kind="serif", alpha=prog(t, 0.1, 0.2))
    x0, x1, y0, y1 = 130, 950, 470, 590
    d.rounded_rectangle((x0 + SH, y0 + SH, x1 + SH, y1 + SH), radius=26, fill=INK)
    d.rounded_rectangle((x0, y0, x1, y1), radius=26, fill=PAPER2, outline=INK, width=OW)
    p = ease_out(prog(t, wt(sc, "one", default=1.3) - 0.1, 0.6))
    if p > 0: d.rounded_rectangle((x0, y0, lerp(x0 + 52, x0 + (x1 - x0) * 0.2, p), y1), radius=26, fill=TEAL, outline=INK, width=OW)
    text(d, (x0 + (x1 - x0) * 0.1, 650), "~20%", 60, fill=TEAL, alpha=p)
    tt = wt(sc, "target", default=4.7)
    a = ease_back(prog(t, tt, 0.35))
    if a > 0:
        fx = x0 + (x1 - x0) * 0.4
        d.line((fx, y0 - 40, fx, y1 + 20), fill=INK, width=8)
        poly(d, [(fx, y0 - 40), (fx + 90 * a, y0 - 20), (fx, y0)], RED, sh=4, ow=4)
        text(d, (fx + 40, 660), "TARGET 40%", 54, fill=RED, alpha=a)
    tx = lerp(-150, W + 700, prog(t, 0.2, 7.5))
    train(d, tx, 1480, 0.62, cars=3, riders=[0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0])
    pill(d, W / 2, 1210, "1 in 5 trips", TEAL, prog(t, wt(sc, "five", default=1.7), 0.3), size=54)

def s_lastmile(d, t, sc):
    text(d, (W / 2, 260), "THE LAST MILE", 104, alpha=prog(t, 0.05, 0.2))
    house(d, 230, 760, 1.0)
    station(d, 830, 760, 0.95)
    for k in range(9):                                        # dotted path with a gap of "?"
        x = 360 + k * 40
        d.ellipse((x - 7, 805, x + 7, 819), fill=INK)
    text(d, (W / 2 + 10, 640), "?", 140, fill=RED, alpha=prog(t, wt(sc, "door", default=1.6), 0.25))
    tg = wt(sc, "grab", default=3.9)
    if t > wt(sc, "car", default=3.0) - 0.2:
        x = lerp(230, 830, ease_out(prog(t, tg - 0.3, 1.2)))
        car(d, x, 1480, 0.7, OLIVE, face="happy", spin=x / 25, t=t)
    pill(d, W / 2, 1210, "you still need a car", RED, prog(t, wt(sc, "need", default=2.8), 0.3), size=54)

def s_sg(d, t, sc):
    text(d, (W / 2, 260), "SINGAPORE", 110, alpha=prog(t, 0.05, 0.2))
    text(d, (W / 2, 355), "just the right to own a car (COE, Oct 2026)", 40, fill=MUTED, kind="serif", alpha=prog(t, wt(sc, "right", default=1.7), 0.25))
    th = wt(sc, "hundred", default=3.1)
    squash = 1 - 0.18 * ease_out(prog(t, th + 0.15, 0.15)) * (1 - prog(t, th + 0.45, 0.4))
    car(d, W / 2, 860, 0.55 * squash, RED, face="shock" if t > th else "happy", t=t)
    price_tag(d, W / 2, 560, "S$130,000", prog(t, th - 0.15, 0.35), size=92)
    tx = lerp(-300, W + 1100, prog(t, 0.8, 3.5))
    train(d, tx, 1480, 0.62, cars=3, col=RED, riders=[1] * 12)
    pill(d, W / 2, 1210, "trains everywhere", TEAL, prog(t, wt(sc, "singapore", default=4.4), 0.3), size=52)

def s_roads(d, t, sc):
    text(d, (W / 2, 250), "MORE ROADS?", 110, alpha=prog(t, 0.05, 0.2))
    text(d, (W / 2, 345), "economists call it induced demand", 44, fill=MUTED, kind="serif", alpha=prog(t, wt(sc, "induced", default=2.6), 0.25))
    tn, tm = wt(sc, "new", default=3.9), wt(sc, "more", nth=1, default=4.8)
    grow = ease_out(prog(t, tn - 0.1, 0.4))
    lanes_h = 3 * 100 + 100 * grow
    top = 430
    d.rectangle((110, top - 14, 970, top + lanes_h + 14), fill=(96, 88, 80), outline=INK, width=5)
    for k in range(1, 4 if grow < 0.5 else 4):
        y = top + k * 100
        if y < top + lanes_h - 5:
            for x in range(120, 950, 70): d.line((x, y, x + 36, y), fill=CREAM, width=6)
    creep = t * 10
    for lane in range(3):
        for k in range(7):
            x = 150 + k * 125 + (creep + lane * 40) % 125
            if x < 915: topcar(d, x, top + 50 + lane * 100, JAM_COLS[(k + lane) % 6])
    if grow > 0.6:                                          # the new lane fills up almost instantly
        fill = ease_out(prog(t, tm - 0.3, 0.9))
        for k in range(7):
            x = 150 + k * 125 + creep % 125
            if x < min(915, 150 + fill * 900): topcar(d, x, top + 350, JAM_COLS[(k + 3) % 6])
        text(d, (W / 2, top + lanes_h + 70), "NEW LANE", 44, fill=MUSTARD, alpha=prog(t, tn, 0.2))
    stamp(d, W / 2, 1270, "SAME JAM", prog(t, wt(sc, "same", default=5.4), 0.18))

def s_outro(d, t, sc):
    tf = wt(sc, "follow", default=4.2)
    if t < tf - 0.1:
        text(d, (W / 2, 260), "SHOULD DRIVING", 96, alpha=prog(t, wt(sc, "should", default=0.7), 0.2))
        text(d, (W / 2, 380), "COST MORE?", 130, fill=MUSTARD, off=9, alpha=prog(t, wt(sc, "expensive", default=1.9), 0.2))
        pill(d, 330, 620, "YES", RED, prog(t, 2.2, 0.3), size=96)
        pill(d, 750, 620, "NO", TEAL, prog(t, 2.4, 0.3), size=96)
        pill(d, W / 2, 1210, "comment below!", CREAM, prog(t, wt(sc, "comment", default=3.0), 0.3), size=56, txt=INK)
        jam_row(d, t, seed=4)
    else:
        text(d, (W / 2, 280), "THE COMMON", 116, alpha=prog(t, tf, 0.25))
        text(d, (W / 2, 420), "CENTS", 160, fill=MUSTARD, off=10, alpha=prog(t, tf + 0.1, 0.25))
        text(d, (W / 2, 545), "money, explained", 58, fill=MUTED, kind="serif", alpha=prog(t, tf + 0.2, 0.25))
        pill(d, W / 2, 700, "FOLLOW " + HANDLE, RED, prog(t, tf + 0.3, 0.3), size=50)
        hop = abs(math.sin(t * math.pi * 1.8)) * 30
        car(d, W / 2, FLOOR_Y - 12 - hop, 0.95 * ease_back(prog(t, tf - 0.1, 0.45)), TEAL, face="happy", t=t)

DRAW = dict(hook=s_hook, why=s_why, cars=s_cars, cheap=s_cheap, trains=s_trains, lastmile=s_lastmile,
            sg=s_sg, roads=s_roads, outro=s_outro)

SUBS = [("three and a half days", "3.5 DAYS"), ("eighty-four hours", "84 HOURS"), ("forty million", "40 MILLION"),
        ("nine years", "9 YEARS"), ("one in five", "1 IN 5"), ("forty percent", "40%"),
        ("a hundred and thirty thousand Singapore dollars", "S$130,000"), ("KL", "KL")]

SFX = [("hook", "three", "drumroll", 0.5, -0.4), ("hook", "days", "chaching", 0.7), ("hook", 0.4, "tick", 0.5),
       ("hook", "traffic", "honk", 0.6),
       ("why", "eighty-four", "stamp", 1.0), ("why", "why", "boing", 0.7), ("why", "easy", "pop", 0.8),
       ("cars", "forty", "drumroll", 0.5, -0.2)] + \
      [("cars", "forty", "pop", 0.45, i * 0.16 + 0.25) for i in range(len(CAR_PILE))] + \
      [("cars", "more", "honk", 0.6),
       ("cheap", "petrol", "pop", 0.8), ("cheap", "loans", "pop", 0.8), ("cheap", "national", "pop", 0.8),
       ("cheap", "low", "chaching", 0.7),
       ("trains", 0.3, "whoosh", 0.5), ("trains", "five", "pop", 0.8), ("trains", "target", "slide_down", 0.6),
       ("lastmile", "door", "boing", 0.6), ("lastmile", "grab", "whoosh", 0.6, -0.3), ("lastmile", "grab", "honk", 0.5, 0.6),
       ("sg", "hundred", "stamp", 1.0, -0.05), ("sg", "thousand", "chaching", 0.7), ("sg", 0.8, "whoosh", 0.5),
       ("roads", "new", "slide_up", 0.6), ("roads", "drivers", "honk", 0.6), ("roads", "same", "stamp", 1.0),
       ("outro", "expensive", "pop", 0.7), ("outro", "comment", "pop", 0.7), ("outro", "follow", "boing", 0.8, -0.1)]

run(DRAW, subs=SUBS, sfx=SFX)
