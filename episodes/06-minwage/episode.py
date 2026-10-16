"""Episode 06: RM2,000 minimum wage, who actually pays? (Budget 2027, checked 16 Oct 2026)"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
from engine import *
from props import *

WORKER_COLS = [TEAL, RED, MUSTARD, OLIVE, ORANGE, (120, 96, 150)]

def s_hook(d, t, sc):
    text(d, (W / 2, 260), "MINIMUM WAGE", 104, alpha=prog(t, 0.05, 0.2))
    text(d, (W / 2, 350), "from June 2027 · Budget 2027", 44, fill=MUTED, kind="serif", alpha=prog(t, 0.2, 0.2))
    p = ease_out(prog(t, wt(sc, "two", default=4.2) - 0.3, 0.7))
    text(d, (W / 2 - 40, 560), f"RM{int(round(1700 + 300 * p)):,}", 170, fill=MUSTARD if p > 0.99 else CREAM, off=12,
         alpha=prog(t, wt(sc, "seventeen", default=3.3) - 0.2, 0.2))
    up_arrow(d, 905, 560, 0.75, prog(t, wt(sc, "two", default=4.2), 0.3))
    stamp(d, W / 2, 1260, "WHO PAYS?", prog(t, wt(sc, "who", default=5.9), 0.18), ang=-6)

def s_workers(d, t, sc):
    text(d, (W / 2, 250), "4 MILLION+ WORKERS", 96, alpha=prog(t, wt(sc, "four", default=0.4), 0.2))
    for i in range(6):
        a = ease_back(prog(t, 0.3 + i * 0.12, 0.35))
        worker(d, 175 + i * 146, 780, 0.95 * a, WORKER_COLS[i], t=t, wave=t > wt(sc, "three", default=3.4))
    tp = wt(sc, "three", default=3.4)
    for i in range(6):
        pa = prog(t, tp + i * 0.08, 0.3)
        if pa > 0: coin(d, 175 + i * 146, 520 - 40 * ease_out(pa), 34 * ease_back(pa), label="+")
    pill(d, W / 2, 1220, "up to +RM300 a month", TEAL, prog(t, tp, 0.3), size=56)

def s_boss(d, t, sc):
    text(d, (W / 2, 250), "EMPLOYERS PAY FIRST", 92, alpha=prog(t, 0.05, 0.2))
    shop(d, 330, 860, 1.05 * ease_back(prog(t, 0.2, 0.4)))
    tw = wt(sc, "wages", default=3.1)
    moneybag(d, 770, 700, 0.9 * lerp(1, 0.7, ease_out(prog(t, tw, 0.8))), label="COSTS")
    notes_fly(d, t, tw, (770, 650), (330, 640), n=5, dur=0.6)
    pill(d, W / 2, 1220, "wages = a big cost", RED, prog(t, wt(sc, "biggest", default=3.8), 0.3), size=56)

def s_prices(d, t, sc):
    text(d, (W / 2, 250), "…AND YOUR PRICES?", 96, alpha=prog(t, 0.05, 0.2))
    xs = [255, 540, 835]
    items = [("nasi", "NASI LEMAK", lambda s: nasi_lemak(d, xs[0], 735, 0.72 * s)),
             ("grab", "RIDES", lambda s: car(d, xs[1], 800, 0.6 * s, OLIVE, face="happy", t=t)),
             ("groceries", "GROCERIES", lambda s: trolley(d, xs[2], 800, 0.62 * s))]
    for i, (cue, lab, draw_it) in enumerate(items):
        ti = wt(sc, cue, default=2.7 + i * 0.9)
        a = ease_back(prog(t, ti - 0.1, 0.35))
        if a > 0.02: draw_it(a)
        up_arrow(d, xs[i], 560 - 14 * abs(math.sin(t * 6 + i)), 0.8, prog(t, ti + 0.15, 0.3))
        text(d, (xs[i], 870), lab, 38, alpha=prog(t, ti, 0.25))
    pill(d, W / 2, 1220, "some cost can pass to you", MUSTARD, prog(t, wt(sc, "prices", default=1.5), 0.3), size=50, txt=INK)

def s_sme(d, t, sc):
    text(d, (W / 2, 250), "SMALL BUSINESSES", 96, alpha=prog(t, 0.05, 0.2))
    text(d, (W / 2, 340), "sales under RM50 million", 50, fill=INK, kind="serif", alpha=prog(t, wt(sc, "under", default=1.4), 0.2))
    shop(d, W / 2, 910, 0.9 * ease_back(prog(t, 0.2, 0.4)), sign="KEDAI KECIL", col=OLIVE)
    stamp(d, W / 2, 500, "MAY BE EXEMPT", prog(t, wt(sc, "exempt", default=3.3), 0.18), ang=-10)
    pill(d, W / 2, 1220, "details still pending", CREAM, prog(t, wt(sc, "details", default=5.5), 0.3), size=52, txt=INK)

def s_debate(d, t, sc):
    text(d, (W / 2, 250), "ECONOMISTS DISAGREE", 92, alpha=prog(t, 0.05, 0.2))
    th, tb = wt(sc, "higher", default=2.2), wt(sc, "but", default=4.1)
    tilt = lerp(0, -14, ease_out(prog(t, th, 0.5))); tilt = lerp(tilt, 14, ease_out(prog(t, tb, 0.5)))
    seesaw(d, W / 2, 560, 320, tilt,
           left=lambda x, y: (text(d, (x, y - 140), "MORE", 46, fill=TEAL), text(d, (x, y - 90), "SPENDING", 46, fill=TEAL)),
           right=lambda x, y: (text(d, (x, y - 140), "FEWER", 46, fill=RED), text(d, (x, y - 90), "HOURS/JOBS", 46, fill=RED)))
    pill(d, W / 2, 1220, "too much, too fast?", RED, prog(t, wt(sc, "fast", default=4.9), 0.3), size=56)

def s_outro(d, t, sc):
    tf = wt(sc, "follow", default=5.3)
    if t < tf - 0.1:
        text(d, (W / 2, 260), "RM2,000 IS…", 120, fill=MUSTARD, off=9, alpha=prog(t, wt(sc, "two", default=0.7), 0.2))
        pill(d, W / 2, 480, "TOO MUCH", RED, prog(t, wt(sc, "much", default=1.7), 0.3), size=70)
        pill(d, W / 2, 640, "TOO LITTLE", TEAL, prog(t, wt(sc, "little", default=2.3), 0.3), size=70)
        pill(d, W / 2, 800, "JUST RIGHT", OLIVE, prog(t, wt(sc, "right", default=3.2), 0.3), size=70)
        pill(d, W / 2, 1220, "comment below!", CREAM, prog(t, wt(sc, "comment", default=4.1), 0.3), size=56, txt=INK)
    else:
        end_card(d, t, tf, hero=lambda s, hop: worker(d, W / 2, FLOOR_Y - 10 - hop, 1.6 * s, TEAL, t=t, wave=True))

DRAW = dict(hook=s_hook, workers=s_workers, boss=s_boss, prices=s_prices, sme=s_sme, debate=s_debate, outro=s_outro)
SUBS = [("June 2027", "JUNE 2027"), ("seventeen hundred", "RM1,700"), ("two thousand ringgit", "RM2,000"),
        ("four million", "4 MILLION"), ("three hundred ringgit", "RM300"), ("fifty million ringgit", "RM50 MILLION")]
SFX = [("hook", "two", "slide_up", 0.6, -0.3), ("hook", "ringgit", "chaching", 0.8), ("hook", "who", "stamp", 1.0),
       ("workers", 0.3, "pop", 0.6), ("workers", 0.66, "pop", 0.6), ("workers", "three", "coins", 0.7),
       ("boss", 0.2, "pop", 0.7), ("boss", "wages", "whoosh", 0.6),
       ("prices", "nasi", "pop", 0.8), ("prices", "grab", "honk", 0.5), ("prices", "groceries", "pop", 0.8),
       ("sme", "exempt", "stamp", 1.0), ("sme", "details", "pop", 0.6),
       ("debate", "higher", "pop", 0.7), ("debate", "but", "slide_down", 0.6),
       ("outro", "much", "pop", 0.7), ("outro", "little", "pop", 0.7), ("outro", "right", "pop", 0.7),
       ("outro", "follow", "boing", 0.8, -0.1)]
run(DRAW, subs=SUBS, sfx=SFX)
