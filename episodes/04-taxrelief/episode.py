"""Episode 04: RM12,000 tax relief doesn't mean RM12,000 back (Budget 2027, checked 16 Oct 2026)"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
from engine import *
from props import *

def income_bar(d, y, width, label, col, a=1.0, cut=0.0):
    """Horizontal income bar from x=130; `cut` px slides off the right end as a separate block."""
    x0 = 130
    rrect(d, (x0, y - 55, x0 + width - cut, y + 55), 22, col)
    text(d, (x0 + (width - cut) / 2, y + 4), label, 48, alpha=a)

# ---------- scenes (t = local seconds); captions sit at CAPTION_Y, keep that lane clear ----------
def s_hook(d, t, sc):
    tt = wt(sc, "twelve", default=2.5)
    note_rain(d, t, tt - 0.2, n=24, seed=12, stop=FLOOR_Y - 20)
    text(d, (W / 2, 260), "BUDGET 2027", 100, alpha=prog(t, 0.05, 0.2))
    text(d, (W / 2, 350), "individual tax relief", 50, fill=MUTED, kind="serif", alpha=prog(t, wt(sc, "tax", default=1.6), 0.2))
    p = ease_out(prog(t, tt - 0.2, 0.8))
    if p > 0: text(d, (W / 2, 560), f"RM{int(round(9000 + 3000 * p)):,}", 190, fill=MUSTARD, off=12)
    stamp(d, W / 2, 760, "NOT CASH BACK", prog(t, wt(sc, "no", default=4.0), 0.18), ang=-8)

def s_what(d, t, sc):
    text(d, (W / 2, 260), "HOW RELIEF WORKS", 96, alpha=prog(t, 0.05, 0.2))
    tc = wt(sc, "cuts", default=2.3)
    cut = 260 * ease_out(prog(t, tc + 0.2, 0.6))
    income_bar(d, 520, 820, "YOUR INCOME", TEAL)
    if cut > 2:
        x = 950 - cut
        rrect(d, (x + cut * 0.2, 640, x + cut * 1.2, 750), 22, MUSTARD)
        text(d, (x + cut * 0.7, 698), "RELIEF", 40, fill=INK, shadow=False, stroke=0)
        d.line((950 - cut, 470, 950 - cut, 570), fill=RED, width=8)
    text(d, (W / 2, 830), "taxed on what's left", 52, fill=INK, kind="serif", alpha=prog(t, tc + 0.6, 0.3))
    pill(d, W / 2, 1220, "not a cut to your tax", RED, prog(t, wt(sc, "doesn't", default=0.6), 0.3), size=52)

def s_example(d, t, sc):
    text(d, (W / 2, 260), "EXAMPLE", 110, alpha=prog(t, 0.05, 0.2))
    pill(d, W / 2, 400, "3% tax band", TEAL, prog(t, wt(sc, "three", default=1.7), 0.3), size=60)
    te = wt(sc, "extra", default=3.2)
    slide = ease_out(prog(t, te + 0.3, 0.8))
    rrect(d, (130, 520, 950, 640), 24, PAPER2)
    text(d, (540, 584), "TAXABLE INCOME", 46, fill=INK, shadow=False, stroke=0)
    a = ease_back(prog(t, te, 0.35))
    if a > 0.02:
        bx = lerp(700, 620, slide); by = lerp(720, 800, slide)
        rrect(d, (bx - 150 * a, by - 60 * a, bx + 150 * a, by + 60 * a), 22, MUSTARD)
        if a > 0.6: text(d, (bx, by + 4), "−RM3,000", 54, fill=INK, shadow=False, stroke=0)

def s_math(d, t, sc):
    text(d, (W / 2, 250), "3% × RM3,000", 110, alpha=prog(t, 0.05, 0.2))
    p = ease_out(prog(t, wt(sc, "ninety", default=2.9) - 0.3, 0.6))
    if p > 0:
        text(d, (W / 2, 520), f"RM{int(round(90 * p))}", 240, fill=MUSTARD, off=14)
        text(d, (W / 2, 690), "saved a year", 60, fill=INK, kind="serif", alpha=clamp(p * 2))
    coin(d, W / 2, 1290, 90 * ease_back(prog(t, wt(sc, "ninety", default=2.9), 0.4)), label="RM")

def s_higher(d, t, sc):
    text(d, (W / 2, 250), "EARN MORE, SAVE MORE", 88, alpha=prog(t, 0.05, 0.2))
    text(d, (W / 2, 340), "yearly saving from the extra RM3,000 relief", 40, fill=MUTED, kind="serif", alpha=prog(t, 0.1, 0.2))
    bars = [("3%", 90, TEAL, 0.1), ("11%", 330, MUSTARD, wt(sc, "eleven", default=1.8)), ("18%", 540, RED, wt(sc, "eighteen", default=5.3))]
    base = 860
    for i, (band, val, col, cue) in enumerate(bars):
        x = 250 + i * 290
        p = ease_out(prog(t, cue, 0.6))
        h = 370 * val / 540 * p
        if h > 12: rrect(d, (x - 95, base - h, x + 95, base), 18, col)
        text(d, (x, base - h - 45), f"RM{int(round(val * p))}", 56, alpha=clamp(p * 3))
        text(d, (x, base + 50), band, 52, fill=INK, shadow=False, stroke=0, alpha=clamp(p * 3))
    pill(d, W / 2, 1220, "new 18% band (was 19%)", CREAM, prog(t, wt(sc, "new", default=5.1), 0.3), size=46, txt=INK)

def s_receipt(d, t, sc):
    text(d, (W / 2, 250), "THOSE RUNNING SHOES", 90, alpha=prog(t, 0.05, 0.2))
    shoe(d, 300, 640, 1.2 * ease_back(prog(t, wt(sc, "shoes", default=0.9) - 0.2, 0.4)))
    receipt(d, 760, 560, 1.0 * ease_back(prog(t, wt(sc, "thousand", default=2.0) - 0.2, 0.4)))
    tr = wt(sc, "times", default=4.4)
    pill(d, W / 2, 830, "RM1,000 × 3% = RM30", TEAL, prog(t, tr, 0.3), size=56)
    stamp(d, W / 2, 1270, "NOT RM1,000", prog(t, wt(sc, "not", default=5.7), 0.18))

def s_twist(d, t, sc):
    text(d, (W / 2, 260), "SO… DOES IT HELP?", 96, alpha=prog(t, 0.05, 0.2))
    seesaw(d, W / 2, 560, 300, lerp(0, -8, ease_out(prog(t, wt(sc, "help", default=0.8), 0.4))) +
           lerp(0, 18, ease_out(prog(t, wt(sc, "less", default=2.1), 0.5))),
           left=lambda x, y: text(d, (x, y - 70), "HEADLINE", 50, fill=RED),
           right=lambda x, y: coin(d, x, y - 60, 48))
    pill(d, W / 2, 1220, "yes, but less than it sounds", MUSTARD, prog(t, wt(sc, "headline", default=2.6), 0.3), size=50, txt=INK)

def s_outro(d, t, sc):
    tf = wt(sc, "follow", default=3.1)
    if t < tf - 0.1:
        text(d, (W / 2, 270), "WHAT WOULD YOU DO", 92, alpha=prog(t, 0.05, 0.2))
        text(d, (W / 2, 390), "WITH RM90?", 130, fill=MUSTARD, off=9, alpha=prog(t, wt(sc, "ninety", default=0.8), 0.2))
        note_stack(d, 450, 820, int(6 * prog(t, 0.6, 0.6)))
        pill(d, W / 2, 1220, "comment below!", CREAM, prog(t, wt(sc, "comment", default=2.0), 0.3), size=56, txt=INK)
    else:
        end_card(d, t, tf, hero=lambda s, hop: coin(d, W / 2, FLOOR_Y - 120 - hop, 110 * s))

DRAW = dict(hook=s_hook, what=s_what, example=s_example, math=s_math, higher=s_higher,
            receipt=s_receipt, twist=s_twist, outro=s_outro)

SUBS = [("twelve thousand ringgit", "RM12,000"), ("twelve thousand", "RM12,000"), ("three percent", "3%"),
        ("three thousand ringgit", "RM3,000"), ("three thousand", "RM3,000"), ("ninety ringgit", "RM90"),
        ("eleven percent", "11%"), ("three hundred and thirty", "RM330"), ("eighteen percent", "18%"),
        ("five hundred and forty", "RM540"), ("a thousand ringgit", "RM1,000"), ("2027", "2027")]

SFX = [("hook", "twelve", "drumroll", 0.5, -0.8), ("hook", "ringgit", "chaching", 0.8), ("hook", "no", "stamp", 1.0),
       ("what", "cuts", "whoosh", 0.6, 0.2), ("what", "doesn't", "pop", 0.7),
       ("example", "three", "pop", 0.8), ("example", "extra", "pop", 0.8), ("example", "comes", "whoosh", 0.6),
       ("math", "ninety", "coins", 0.7, -0.2), ("math", "ninety", "boing", 0.5, 0.4),
       ("higher", 0.1, "pop", 0.7), ("higher", "eleven", "pop", 0.8), ("higher", "eighteen", "chaching", 0.8),
       ("receipt", "shoes", "pop", 0.8), ("receipt", "thousand", "pop", 0.8), ("receipt", "not", "stamp", 1.0),
       ("twist", "less", "slide_down", 0.6),
       ("outro", "ninety", "coins", 0.6), ("outro", "comment", "pop", 0.7), ("outro", "follow", "boing", 0.8, -0.1)]

run(DRAW, subs=SUBS, sfx=SFX)
