"""Episode 05 (quick hit): What RM100 of 2015 stuff costs today (CPI, checked 16 Oct 2026)
CPI (2010=100): 2015 annual average ~112.8 (World Bank via FRED); Aug 2026 137.5 (DOSM via Bernama). 137.5/112.8 = 1.219."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
from engine import *
from props import *

def s_hook(d, t, sc):
    text(d, (W / 2, 260), "RM100 IN 2015", 110, alpha=prog(t, 0.05, 0.2))
    note_stack(d, 450, 760, int(8 * ease_out(prog(t, 0.3, 0.6))))
    text(d, (W / 2, 420), "costs how much today?", 60, fill=INK, kind="serif", alpha=prog(t, wt(sc, "costs", default=2.5), 0.25))
    text(d, (W / 2, 1260), "?", 220, fill=RED, alpha=prog(t, wt(sc, "today", default=3.2), 0.2))

def s_index(d, t, sc):
    text(d, (W / 2, 250), "PRICE INDEX", 110, alpha=prog(t, 0.05, 0.2))
    text(d, (W / 2, 340), "Malaysia CPI (2010 = 100)", 44, fill=MUTED, kind="serif", alpha=prog(t, 0.1, 0.2))
    vals = [0.0, 0.08, 0.17, 0.26, 0.24, 0.31, 0.43, 0.57, 0.66, 0.79, 0.9, 1.0]   # shape of 2015→2026 rise
    p = ease_out(prog(t, wt(sc, "went", default=1.7), wt(sc, "thirty-seven", default=6.4) - 1.2))
    line_chart(d, 150, 430, 930, 860, vals, p)
    text(d, (190, 870 - 0 * 430 + 50), "2015", 40, fill=INK, shadow=False, stroke=0)
    text(d, (890, 910), "2026", 40, fill=INK, shadow=False, stroke=0)
    text(d, (330, 770), "~113", 60, fill=TEAL, alpha=prog(t, wt(sc, "thirteen", default=2.9), 0.2))
    text(d, (820, 400), "~137", 60, fill=RED, alpha=prog(t, wt(sc, "thirty-seven", default=6.4), 0.2))

def s_now(d, t, sc):
    text(d, (W / 2, 250), "TODAY", 120, alpha=prog(t, 0.05, 0.2))
    trolley(d, W / 2, 900, 1.15 * ease_back(prog(t, 0.1, 0.4)))
    price_tag(d, W / 2 + 40, 520, "RM122", prog(t, wt(sc, "twenty-two", default=2.8) - 0.2, 0.35), size=110)
    pill(d, W / 2, 1220, "+22% since 2015", RED, prog(t, wt(sc, "twenty-two", default=2.8) + 0.2, 0.3), size=58)

def s_outro(d, t, sc):
    tf = wt(sc, "follow", default=3.4)
    if t < tf - 0.1:
        text(d, (W / 2, 270), "DID YOUR SALARY", 100, alpha=prog(t, 0.05, 0.2))
        text(d, (W / 2, 400), "RISE 22%?", 140, fill=MUSTARD, off=9, alpha=prog(t, wt(sc, "twenty-two", default=0.9), 0.2))
        pill(d, 330, 640, "YES", TEAL, prog(t, 1.2, 0.3), size=96)
        pill(d, 750, 640, "LOL NO", RED, prog(t, 1.4, 0.3), size=80)
        pill(d, W / 2, 1220, "comment below!", CREAM, prog(t, wt(sc, "comment", default=2.2), 0.3), size=56, txt=INK)
    else:
        end_card(d, t, tf, hero=lambda s, hop: trolley(d, W / 2, FLOOR_Y - 10 - hop, 0.9 * s))

DRAW = dict(hook=s_hook, index=s_index, now=s_now, outro=s_outro)
SUBS = [("a hundred ringgit", "RM100"), ("hundred ringgit", "RM100"), ("in 2015", "IN 2015"),
        ("one hundred and thirteen", "113"), ("one hundred and thirty-seven", "137"),
        ("a hundred and twenty-two", "RM122"), ("twenty-two percent", "22%")]
SFX = [("hook", 0.3, "coins", 0.6), ("hook", "today", "boing", 0.7),
       ("index", "went", "slide_up", 0.6), ("index", "thirty-seven", "pop", 0.8),
       ("now", "twenty-two", "stamp", 0.9, -0.05), ("now", "twenty-two", "chaching", 0.7, 0.3),
       ("outro", "comment", "pop", 0.7), ("outro", "follow", "boing", 0.8, -0.1)]
run(DRAW, subs=SUBS, sfx=SFX)
