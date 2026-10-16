"""Episode 02 (v2, story cut): Who really pays for your petrol? Myvi vs SUV. (figures checked 16 Oct 2026)"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
from engine import *
from props import *

MYVI_X, SUV_X, CAR_BASE = 280, 765, 905
MYVI_S, SUV_S = 0.76, 1.12

def drive_in(t, t0, x_end, from_left, dur=0.7):
    """x position + wheel spin for a car driving in and braking with a little overshoot."""
    p = ease_back(prog(t, t0, dur), 1.2)
    start = -260 if from_left else W + 260
    x = lerp(start, x_end, p)
    return x, (x - start) / 38 * (1 if from_left else -1)

# ---------- scenes (t = local seconds); captions sit at CAPTION_Y, keep that lane clear ----------
def s_hook(d, t, sc):
    note_rain(d, t, wt(sc, "seven", default=1.7) - 0.2, n=30, seed=4)
    text(d, (W / 2, 270), "THE GOVERNMENT", 96, alpha=prog(t, 0.1, 0.25))
    text(d, (W / 2, 385), "PAYS YOU…", 110, fill=MUSTARD, alpha=prog(t, wt(sc, "paying", default=1.1), 0.25))
    p = ease_out(prog(t, wt(sc, "seven", default=1.7), 1.0))
    if p > 0:
        pop = 1 + 0.12 * math.sin(math.pi * prog(t, wt(sc, "eighty", default=2.5) + 0.3, 0.3))
        text(d, (W / 2, 640), f"RM{int(round(789 * p))}", int(200 * pop), fill=MUSTARD, off=12)
        text(d, (W / 2, 790), "a month", 60, fill=INK, kind="serif", alpha=prog(t, wt(sc, "month", default=3.3), 0.25))
    pill(d, W / 2, 1240, "here's the catch", RED, prog(t, wt(sc, "catch", default=4.5) - 0.1, 0.3), size=60)

def s_meet(d, t, sc):
    text(d, (W / 2, 270), "MEET TWO DRIVERS", 92, alpha=prog(t, 0.1, 0.25))
    tm, ts = wt(sc, "myvi", default=1.6) - 0.35, wt(sc, "giant", default=2.6) - 0.3
    if t > tm:
        x, spin = drive_in(t, tm, MYVI_X, True)
        car(d, x, CAR_BASE, MYVI_S, TEAL, face="happy", spin=spin, t=t)
        text(d, (MYVI_X, 580), "MYVI", 64, alpha=prog(t, tm + 0.5, 0.25))
    if t > ts:
        x, spin = drive_in(t, ts, SUV_X, False)
        car(d, x, CAR_BASE, SUV_S, RED, tall=True, facing=-1, face="smug", spin=spin, t=t)
        text(d, (SUV_X, 470), "SUV", 76, alpha=prog(t, ts + 0.5, 0.25))
    tb = wt(sc, "both", default=4.0)
    pill(d, MYVI_X, 1220, "RM1.99", TEAL, prog(t, tb, 0.3), size=58)
    pill(d, SUV_X, 1220, "RM1.99", TEAL, prog(t, tb + 0.15, 0.3), size=58)

def s_real(d, t, sc):
    text(d, (W / 2, 270), "THE REAL PRICE", 100, alpha=prog(t, 0.05, 0.25))
    text(d, (W / 2, 362), "unsubsidised RON95 · 15–21 Oct 2026", 42, fill=MUTED, kind="serif", alpha=prog(t, 0.1, 0.25))
    tf = wt(sc, "four", default=2.0)
    p = ease_out(prog(t, tf - 0.4, 0.9))
    shake = math.sin(t * 70) * 7 if 0 < p < 1 else 0
    pump(d, W / 2 + shake, 930, 0.9, price=f"RM{lerp(1.99, 4.62, p):.2f}", price_col=mix(INK, RED, p),
         face="shock" if p > 0.4 else "happy", t=t)
    if p > 0.4: sweat(d, W / 2, 930 - 0.9 * 420 + 40, t, spread=1.1)
    tg = wt(sc, "government", default=3.7)
    if t > tg - 0.1:
        moneybag(d, W / 2, 1290, 0.75 * ease_back(prog(t, tg - 0.1, 0.4)))
        notes_fly(d, t, tg + 0.2, (W / 2, 1200), (W / 2 + 40, 640), n=5, dur=0.6)

def s_fill(d, t, sc):
    text(d, (W / 2, 260), "FULL TANK", 104, alpha=prog(t, 0.05, 0.25))
    car(d, MYVI_X, CAR_BASE, MYVI_S, TEAL, face="happy", t=t)
    tsuv = wt(sc, "every", default=4.4)
    car(d, SUV_X, CAR_BASE, SUV_S, RED, tall=True, facing=-1, face="smug", t=t)
    fm = ease_out(prog(t, wt(sc, "forty", default=1.0) - 0.2, 0.8))
    fs = ease_out(prog(t, wt(sc, "eighty", default=3.4) - 0.6, 1.1))
    tank(d, MYVI_X, 480, 590, fm, w=110)                     # same litres-per-pixel: 40 L tank is half as tall
    tank(d, SUV_X, 370, 590, fs, w=110)
    text(d, (MYVI_X + 135, 535), "40 L", 60, alpha=clamp(fm * 3))
    text(d, (SUV_X - 140, 480), "80 L", 60, alpha=clamp(fs * 3))
    if t > tsuv:
        notes_fly(d, t, tsuv, (W / 2, 160), (MYVI_X, 780), n=2, dur=0.6, seed=5)
        notes_fly(d, t, tsuv + 0.1, (W / 2, 160), (SUV_X, 760), n=5, dur=0.6, seed=6)
    pill(d, MYVI_X, 1180, "≈RM105", TEAL, prog(t, wt(sc, "full", default=4.7), 0.3), size=56)
    pill(d, SUV_X, 1180, "≈RM210", RED, prog(t, wt(sc, "full", default=4.7) + 0.2, 0.3), size=56)
    pill(d, W / 2, 1330, "subsidy per full tank", CREAM, prog(t, wt(sc, "double", default=6.4), 0.3), size=44, txt=INK)

def s_t20(d, t, sc):
    text(d, (W / 2, 260), "EVERY RM1 OF SUBSIDY", 84, alpha=prog(t, 0.05, 0.25))
    text(d, (W / 2, 350), "Ministry of Finance, 2022", 42, fill=MUTED, kind="serif", alpha=prog(t, 0.1, 0.25))
    x0, x1, y0, y1 = 120, 950, 520, 650
    a1 = x0 + (x1 - x0) * 0.53; a2 = x0 + (x1 - x0) * 0.85
    pr = ease_out(prog(t, wt(sc, "fifty", default=1.5) - 0.2, 0.5))
    pt = ease_out(prog(t, wt(sc, "poorest", default=5.3) - 0.2, 0.5))
    d.rounded_rectangle((x0 + SH, y0 + SH, x1 + SH, y1 + SH), radius=26, fill=INK)
    d.rounded_rectangle((x0, y0, x1, y1), radius=26, fill=PAPER2, outline=INK, width=OW)
    if pt > 0: d.rounded_rectangle((a1, y0, a2, y1), radius=26, fill=MUSTARD, outline=INK, width=OW)
    if pr > 0: d.rounded_rectangle((x0, y0, lerp(x0 + 52, a1, pr), y1), radius=26, fill=RED, outline=INK, width=OW)
    if pt > 0: d.rounded_rectangle((lerp(x1 - 52, a2, pt), y0, x1, y1), radius=26, fill=TEAL, outline=INK, width=OW)
    top_hat(d, (x0 + a1) / 2, y0 - 6, 0.9 * ease_back(prog(t, wt(sc, "richest", default=3.7), 0.35)))
    text(d, ((x0 + a1) / 2, 730), "53 SEN", 66, fill=RED, alpha=pr)
    text(d, ((x0 + a1) / 2, 805), "richest 20%", 40, fill=INK, kind="serif", alpha=pr)
    text(d, ((a2 + x1) / 2, 730), "15", 66, fill=TEAL, alpha=pt)
    text(d, ((a2 + x1) / 2 - 6, 800), "poorest", 34, fill=INK, kind="serif", alpha=pt)
    text(d, ((a2 + x1) / 2 - 6, 838), "40%", 34, fill=INK, kind="serif", alpha=pt)
    pill(d, W / 2, 1190, "richest 20%: 53 sen", RED, prog(t, wt(sc, "richest", default=3.7), 0.3), size=52)
    pill(d, W / 2, 1320, "poorest 40%: 15 sen", TEAL, prog(t, wt(sc, "fifteen", default=6.3), 0.3), size=52)

def s_cost(d, t, sc):
    tf = wt(sc, "forty", default=1.6)
    note_rain(d, t, tf - 0.3, n=40, seed=9, speed=1100)
    text(d, (W / 2, 270), "THE BILL", 110, alpha=prog(t, 0.05, 0.2))
    text(d, (W / 2, 362), "2026 projection · Ministry of Finance", 42, fill=MUTED, kind="serif", alpha=prog(t, 0.1, 0.2))
    p = ease_out(prog(t, tf - 0.5, 0.7))
    if p > 0:
        text(d, (W / 2, 590), f"RM{int(round(40 * p))}", 210, fill=MUSTARD, off=12)
        text(d, (W / 2, 750), "BILLION", 110, alpha=clamp(p * 2))
    for i, x in enumerate((150, 350, 550, 750)):
        note_stack(d, x, FLOOR_Y - 12, int(22 * clamp(p * 1.6 - i * 0.18)))

def s_budi(d, t, sc):
    text(d, (W / 2, 280), "BUDI95", 150, fill=MUSTARD, off=10, alpha=prog(t, 0, 0.2))
    tc = wt(sc, "caps", default=1.2)
    fr = min(ease_out(prog(t, 0.2, 0.8)) * 1.2, 1.0)
    gauge(d, W / 2, 760, 230, fr)
    stamp(d, W / 2, 640, "CAPPED", prog(t, tc, 0.18))
    pill(d, W / 2, 1230, "300 L / month", TEAL, prog(t, wt(sc, "three", default=1.7), 0.3), size=60)

def s_flip(d, t, sc):
    text(d, (W / 2, 260), "BUT SCRAP IT", 100, alpha=prog(t, 0, 0.2))
    text(d, (W / 2, 375), "COMPLETELY?", 110, fill=RED, alpha=prog(t, 0.15, 0.2))
    xs = [255, 540, 835]
    items = [("transport", "TRANSPORT", lambda s: lorry(d, xs[0], 800, 0.62 * s)),
             ("food", "FOOD", lambda s: nasi_lemak(d, xs[1], 735, 0.72 * s)),
             ("everything", "EVERYTHING", lambda s: trolley(d, xs[2], 800, 0.62 * s))]
    for i, (cue, lab, draw_it) in enumerate(items):
        ti = wt(sc, cue, default=1.5 + i * 0.6)
        a = ease_back(prog(t, ti - 0.1, 0.35))
        if a > 0.02: draw_it(a)
        up_arrow(d, xs[i], 560 - 14 * abs(math.sin(t * 6 + i)), 0.8, prog(t, ti + 0.15, 0.3))
        text(d, (xs[i], 870), lab, 38, alpha=prog(t, ti, 0.25))
    pill(d, W / 2, 1220, "everything gets pricier", RED, prog(t, wt(sc, "pricier", default=3.1), 0.3), size=54)

def s_outro(d, t, sc):
    tf = wt(sc, "follow", default=3.0)
    if t < tf - 0.1:
        text(d, (W / 2, 280), "KEEP IT", 120, fill=TEAL, alpha=prog(t, wt(sc, "keep", default=0.3), 0.2))
        text(d, (W / 2, 420), "OR CUT IT?", 120, fill=RED, alpha=prog(t, wt(sc, "cut", default=1.0), 0.2))
        car(d, MYVI_X, 860, 0.55, TEAL, face="happy", t=t)
        car(d, SUV_X, 860, 0.85, RED, tall=True, facing=-1, face="shock" if t > wt(sc, "cut", default=1.0) else "smug", t=t)
        pill(d, W / 2, 1220, "comment below!", CREAM, prog(t, wt(sc, "comment", default=1.8), 0.3), size=56, txt=INK)
    else:
        text(d, (W / 2, 280), "THE COMMON", 116, alpha=prog(t, tf, 0.25))
        text(d, (W / 2, 420), "CENTS", 160, fill=MUSTARD, off=10, alpha=prog(t, tf + 0.1, 0.25))
        text(d, (W / 2, 545), "money, explained", 58, fill=MUTED, kind="serif", alpha=prog(t, tf + 0.2, 0.25))
        pill(d, W / 2, 700, "FOLLOW " + HANDLE, RED, prog(t, tf + 0.3, 0.3), size=50)
        hop = abs(math.sin(t * math.pi * 1.8)) * 30
        pump(d, W / 2, FLOOR_Y - 10 - hop, 0.78 * ease_back(prog(t, tf - 0.1, 0.45)), face="happy", t=t)

DRAW = dict(hook=s_hook, meet=s_meet, real=s_real, fill=s_fill, t20=s_t20, cost=s_cost,
            budi=s_budi, flip=s_flip, outro=s_outro)

SUBS = [("seven hundred and eighty-nine ringgit", "RM789"), ("one ringgit ninety-nine", "RM1.99"),
        ("four ringgit sixty", "RM4.60"), ("forty litres", "40 LITRES"), ("fifty-three sen", "53 SEN"),
        ("twenty percent", "20%"), ("poorest forty", "POOREST 40%"), ("fifteen", "15 SEN"),
        ("forty billion ringgit", "RM40 BILLION"), ("BUDI ninety-five", "BUDI95"), ("three hundred litres", "300 LITRES"),
        ("in 2022", "IN 2022")]

# (scene, cue word or seconds, effect, volume, offset seconds)
SFX = [("hook", "seven", "coins", 0.8), ("hook", "eighty-nine", "chaching", 1.0, 0.3), ("hook", "catch", "boing", 0.9, -0.1),
       ("meet", "myvi", "whoosh", 0.7, -0.4), ("meet", "myvi", "honk", 0.55, 0.3),
       ("meet", "giant", "whoosh", 0.8, -0.35), ("meet", "SUV", "honk", 0.7, 0.2), ("meet", "both", "pop", 0.8),
       ("meet", "both", "pop", 0.8, 0.15),
       ("real", "four", "slide_up", 0.7, -0.4), ("real", "sixty", "chaching", 0.9, 0.15), ("real", "government", "coins", 0.7, 0.2),
       ("fill", "forty", "glug", 0.8, -0.2), ("fill", "eighty", "glug", 0.9, -0.6), ("fill", "eighty", "glug", 0.9, -0.05),
       ("fill", "full", "chaching", 0.9), ("fill", "double", "coins", 0.7),
       ("t20", "fifty", "drumroll", 0.6, -0.9), ("t20", "fifty", "chaching", 0.8, 0.05), ("t20", "richest", "pop", 0.8),
       ("t20", "fifteen", "slide_down", 0.6),
       ("cost", "forty", "drumroll", 0.7, -1.0), ("cost", "billion", "cymbal", 0.6), ("cost", "billion", "chaching", 0.8),
       ("budi", "caps", "stamp", 1.0),  ("budi", "three", "pop", 0.8),
       ("flip", "transport", "pop", 0.8), ("flip", "food", "pop", 0.8), ("flip", "everything", "pop", 0.8),
       ("flip", "pricier", "slide_up", 0.6),
       ("outro", "keep", "pop", 0.7), ("outro", "cut", "honk", 0.5), ("outro", "follow", "boing", 0.8, -0.1)]

run(DRAW, subs=SUBS, sfx=SFX)
