"""Episode 07 (long-form): Zimbabwe Printed a 100 Trillion Dollar Note. What Actually Survived?
Painted scenes (images/ from tools/make_images.py) + engine overlays. Facts: SOURCES.md."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
from doodle import *

IMG = lambda k: f"images/{k}.jpg"

# ---------- overlay helpers ----------
def yr(y):            return lambda d, t, sc: year_tag(d, y, prog(t, 0.2, 0.3))
def src(s):           return lambda d, t, sc: source_tag(d, s, prog(t, 0.5, 0.4))
def head(s, at=0.3, y=150):
    return lambda d, t, sc: headline(d, s, prog(t, at if isinstance(at, float) else wt(sc, at), 0.35), y=y)
def label(title, sub="", at=0.4):
    return lambda d, t, sc: lower_label(d, title, sub, prog(t, wt(sc, at) if isinstance(at, str) else at, 0.5))
def bignum(value, lab, word=None, col=YELLOW, y=470, size=170):
    def f(d, t, sc):
        a = prog(t, wt(sc, word) if word else 0.4, 0.4)
        if a <= 0: return
        overlay_dim(d, 0.45 * a)
        big_number(d, W / 2, y, value, lab, a, col=col, size=size, sub_col=WHITE)
    return f
def overlay_dim(d, k):
    if k <= 0: return
    img = d._image
    img.paste(Image.blend(img, Image.new("RGB", img.size, (10, 8, 6)), k))
def both(*fs):
    return lambda d, t, sc: [f(d, t, sc) for f in fs]

def zim_timeline(hi, p_word=None):
    items = [(1980, "independence"), (1997, "Black Friday"), (2000, "land reform"), (2007, "price controls"),
             (2008, "peak"), (2009, "dollar dropped")]
    def f(d, t, sc):
        overlay_dim(d, 0.55)
        timeline(d, 260, 1660, 470, items, ease_out(prog(t, 0.3, 1.6)), hi=hi)
        _recolor_timeline(d)
    return f
def _recolor_timeline(d): pass   # timeline text is drawn dark; the dim layer keeps it readable on paper-like boxes

def card_box(lines, at=0.4, x=W / 2, y=430, w=900):
    """White info card with a few bold lines (appears at local time / word `at`)."""
    def f(d, t, sc):
        a = prog(t, wt(sc, at) if isinstance(at, str) else at, 0.4)
        if a <= 0: return
        h = 90 + 78 * len(lines); off = (1 - ease_out(a)) * 40
        rrect(d, (x - w / 2, y - h / 2 + off, x + w / 2, y + h / 2 + off), 24, WHITE)
        for i, (s, c) in enumerate(lines):
            text(d, (x, y - h / 2 + off + 80 + i * 78), s, 54, fill=c, max_w=w - 60)
    return f

def zeros_count(d, t, sc):
    overlay_dim(d, 0.5)
    first = 0.0 if sc["key"] == "c6" else wt(sc, "2006", default=1.0)
    steps = [("2006", "-3 zeros", first), ("2008", "-10 zeros", wt(sc, "Two", default=99)),
             ("2009", "-12 zeros", wt(sc, "2009", default=99))]
    for i, (yv, lab, at) in enumerate(steps):
        a = prog(t, at, 0.4)
        if a <= 0: continue
        x = 520 + i * 440
        rrect(d, (x - 190, 330, x + 190, 610), 24, WHITE)
        text(d, (x, 410), yv, 80, fill=INK)
        text(d, (x, 520), lab, 60, fill=RED)
    a = prog(t, wt(sc, "Twenty", default=99), 0.4)
    if a > 0: headline(d, "25 ZEROS IN UNDER 3 YEARS", a, y=740, size=70, box=RED)

def price_double(d, t, sc):
    """Illustration of 'prices doubling every day': a multiplier counter (no invented prices)."""
    overlay_dim(d, 0.45)
    days = int(clamp((t - 0.6) / 0.45, 0, 12))
    card_box([("IF PRICES DOUBLE EVERY DAY", INK)], at=0.2, y=300, w=900)(d, t, sc)
    text(d, (W / 2, 520), f"×{2 ** days:,}", 150, fill=YELLOW, stroke=6, stroke_fill=INK)
    text(d, (W / 2, 640), f"after {days} day{'s' if days != 1 else ''}", 50, fill=WHITE, w="xbold", stroke=4, stroke_fill=INK)

def tobacco_bars(d, t, sc):
    overlay_dim(d, 0.55)
    p = prog(t, wt(sc, "1998", default=1.0), 2.5)
    box = (560, 260, 1360, 760)
    rrect(d, (box[0] - 60, box[1] - 80, box[2] + 60, box[3] + 110), 24, WHITE)
    text(d, (W / 2, box[1] - 30), "Tobacco grown (million kg)", 40, w="xbold")
    bar_chart(d, box, [("1998", 260, GREEN), ("2008", 48, RED)], p, fmt=lambda v: f"~{v}")

def inflation_ladder(d, t, sc):
    overlay_dim(d, 0.55)
    rows = [("1997", "~20%"), ("2003", "~600%"), ("2006", "~1,000%"), ("Jul 2008", "231,000,000%")]
    # only the July 2008 official figure is quoted in the voice; earlier rungs are shown without numbers
    rows = [("July 2008 (official, per year)", "231 million %"), ("Nov 2008 (estimate, per month)", "79.6 billion %")]
    for i, (lab, val) in enumerate(rows):
        a = prog(t, 0.4 + i * 1.2, 0.4) if sc["key"] == "c11" else prog(t, 0.4, 0.4) * (i == 0)
        if a <= 0: continue
        y = 360 + i * 230; off = (1 - ease_out(a)) * 30
        rrect(d, (260, y - 90 + off, 1660, y + 90 + off), 24, WHITE)
        text(d, (300, y + off), lab, 38, anchor="lm", w="xbold", fill=GREY, max_w=720)
        text(d, (1620, y + off), val, 72, anchor="rm", fill=RED, max_w=560)

def two_groups_overlay(d, t, sc):
    for i, (lab, col, at) in enumerate((("PROMISES", RED, wt(sc, "promises", default=1.5)), ("THINGS", GREEN, wt(sc, "things", default=3.0)))):
        a = prog(t, at, 0.4)
        if a > 0: pill(d, 560 + i * 800, 200, lab, col, a=a, size=64)

def ledger(d, t, sc):
    overlay_dim(d, 0.6)
    L = [("Savings accounts", False), ("Pensions & insurance", False), ("Fixed salaries", False), ("Bonds", False)]
    R = [("Land & houses", True), ("Cattle & gold", True), ("Real company shares", True), ("Foreign currency", True)]
    rrect(d, (220, 170, 940, 820), 24, WHITE); rrect(d, (980, 170, 1700, 820), 24, WHITE)
    text(d, (580, 240), "LOST", 64, fill=RED); text(d, (1340, 240), "KEPT VALUE", 64, fill=DKGREEN)
    for i in range(4):
        a = prog(t, 0.6 + i * 0.5, 0.35)
        for (x, (s, ok)) in ((580, L[i]), (1340, R[i])):
            if a <= 0: continue
            y = 360 + i * 110
            check_cross(d, x - 260, y, ok, a, r=30)
            text(d, (x - 210, y), s, 44, anchor="lm", w="xbold", max_w=560)

def demonet(d, t, sc):
    overlay_dim(d, 0.55)
    a = prog(t, wt(sc, "thirty", default=3.0), 0.5)
    if a > 0:
        rrect(d, (260, 300, 1660, 560), 24, WHITE)
        zeros(d, W / 2, 400, "Z$35,000,000,000,000,000", 92, a, col=RED)
        text(d, (W / 2, 500), "= US$1", 70, alpha=prog(t, wt(sc, "one", default=4.5), 0.3))
    b = prog(t, wt(sc, "five", default=8.0), 0.4)
    if b > 0: pill(d, W / 2, 700, "Up to Z$175 quadrillion → US$5", YELLOW, fg=INK, a=b, size=52)

def end_overlay(d, t, sc):
    overlay_dim(d, 0.35 * prog(t, 0.2, 0.6))
    end_card_painted(d, t, wt(sc, "subscribe", default=4.0))

def end_card_painted(d, t, tf):
    a = prog(t, tf - 0.5, 0.5)
    if a <= 0: return
    overlay_dim(d, 0.5 * a)
    text(d, (W * 0.3, 380), "THE COMMON CENTS", 96, fill=WHITE, alpha=1, stroke=6, stroke_fill=INK)
    marker(d, (W * 0.3, 500), "the money stories behind history", 46, a=a, w="xbold")
    pill(d, W * 0.3, 640, "SUBSCRIBE", RED, a=prog(t, tf, 0.4), size=52)

def chap(n, title, img):
    def f(d, t, sc):
        painted(d._image, IMG(img), t, sc["dur"], "in", dim=0.65)
        a = ease_out(prog(t, 0.05, 0.5))
        text(d, (W / 2, 430 - (1 - a) * 30), f"CHAPTER {n}", 46, fill=YELLOW, w="xbold")
        d.rectangle((W / 2 - 120 * a, 468, W / 2 + 120 * a, 476), fill=YELLOW)
        text(d, (W / 2, 560 + (1 - a) * 40), title, 110, fill=WHITE)
    return f

# ---------- the shot plan: scene -> (image, camera move, overlay) ----------
PLAN = {
 "h1": ("pensioner", "in", None),
 "h2": ("queue_bank", "right", both(yr("ZIMBABWE · 2008"), head("THIS ACTUALLY HAPPENED", "millions"))),
 "h3": ("note_hand", "in", both(yr("JANUARY 2009"), bignum("Z$100,000,000,000,000", "worth about US$30 on day one", "thirty", size=110), src("Washington Examiner; Banknote News; BBC"))),
 "h4": ("shop_prices", "left", both(price_double, src("Hanke & Kwok via Johns Hopkins Magazine; Cato"))),
 "h5": ("villa_cattle", "in", head("NOT EVERYONE WAS RUINED", "not")),
 "h6": ("harare_dusk", "right", card_box([("1. How does this happen?", INK)], 0.3, y=300)),
 "h7": ("market_cash", "left", card_box([("1. How does this happen?", GREY), ("2. What is life like?", INK)], 0.0, y=330)),
 "h8": ("wallet_today", "in", card_box([("1. How does this happen?", GREY), ("2. What is life like?", GREY), ("3. What actually survived?", RED)], 0.0, y=360)),
 "ch1": None,
 "a1": ("stadium_1980", "in", both(yr("1980"), card_box([("Z$1  >  US$1", INK), ("official exchange rate", GREY)], "worth", y=260, w=700), src("CNBC Africa; Global Financial Data"))),
 "a2": ("landscape", "right", label("ZIMBABWE", "farmland · gold · platinum")),
 "a3": ("tobacco_farm", "left", head("THE BREADBASKET OF SOUTHERN AFRICA", "breadbasket")),
 "a4": ("auction_floor", "in", head("EXPORTS  =  US DOLLARS", "dollars")),
 "a5": ("port_ship", "right", head("REMEMBER THIS", "Keep")),
 "a6": ("harare_90s", "left", yr("1980s – 1997")),
 "ch2": None,
 "b1": ("veterans", "in", both(yr("1997"), head("CRACK 1: UNBUDGETED PAYOUTS", 0.3))),
 "b2": ("trading_room", "in", both(yr("14 NOV 1997"), bignum("−72%", "in one day: 'Black Friday'", "seventy", col=RED), src("Mail & Guardian; InsiderZim"))),
 "b3": ("convoy", "right", both(yr("1998"), head("CRACK 2: A FOREIGN WAR", 0.3), label("~11,000 TROOPS", "sent to the war in the Congo", 2.5))),
 "b4": ("finance_desk", "in", both(card_box([("Officially: a few million $ / month", GREY), ("Admitted later: ~$23 million / month", RED)], "Later", y=330, w=1200), src("AP via GlobalSecurity; WRAL"))),
 "b5": ("farm_aerial", "in", head("CRACK 3: LAND", 0.4)),
 "b6": ("farm_aerial", "right", None),
 "b7": ("new_farmers", "in", yr("2000 →")),
 "b8": ("bank_refuse", "left", card_box([("No seeds · no tractors", INK), ("no irrigation · no loans", INK)], 0.6, y=260)),
 "b9": ("dry_field", "in", both(tobacco_bars, src("IRIN; CORESTA; Mail & Guardian"))),
 "b10": ("fuel_queue", "right", card_box([("fewer crops → fewer dollars", INK), ("→ less fuel & fertiliser → fewer crops", RED)], 0.8, y=250, w=1200)),
 "b11": ("central_bank", "in", head("...AND IT HAD A MACHINE", "machine")),
 "ch3": None,
 "c1": ("press", "in", None),
 "c2": ("payroll", "left", head("PRINTING TO PAY THE BILLS", 0.6)),
 "c2b": ("street_fx", "right", None),
 "c3": ("press", "right", head("MORE PAPER · SAME GOODS", "more")),
 "c4": ("rush_shop", "in", card_box([("prices rise → spend faster", INK), ("→ prices rise faster", RED)], "spend", y=260)),
 "c5": ("note_hand", "out", both(yr("2006"), zeros_count)),
 "c6": ("note_hand", "in", zeros_count),
 "c7": ("inspector", "in", both(yr("JUNE 2007"), head("ORDER: CUT ALL PRICES IN HALF", "half"))),
 "c8": ("empty_shelves", "in", both(label("~1,300 BUSINESSES", "fined or charged", "thirteen"), src("Mail & Guardian; NPR; JURIST"))),
 "c9": ("black_market", "left", head("THE BLACK MARKET", "black")),
 "c10": ("stats_office", "in", both(yr("JULY 2008"), inflation_ladder, src("Central Statistical Office via VOA; Bizcommunity"))),
 "c11": ("economist", "in", both(yr("NOVEMBER 2008"), inflation_ladder, src("Hanke & Kwok (estimate); Johns Hopkins Magazine; Cato"))),
 "c12": ("budapest_1946", "right", both(card_box([("#1  Hungary 1946", INK), ("#2  Zimbabwe 2008", RED)], 0.8, y=300, w=760), src("Hanke–Krus hyperinflation table"))),
 "c13": ("note_hand", "in", both(yr("JANUARY 2009"), bignum("Z$100 TRILLION", "≈ US$30 on day one", "trillion", size=150))),
 "ch4": None,
 "d1": ("market_cash", "in", None),
 "d2": ("payday", "right", head("SPEND IT THE SAME DAY", "same")),
 "d3": ("queue_bank", "left", None),
 "d4": ("bag_of_cash", "in", None),
 "d5": ("teacher", "in", None),
 "d6": ("border_bus", "right", None),
 "d6b": ("barter", "in", head("BARTER CAME BACK", "Barter")),
 "d7": ("stock_board", "in", head("STOCKS 'SOARED' (ON PAPER)", "soaring")),
 "d8": ("balance", "in", head("WHAT KEPT ITS VALUE?", "what")),
 "ch5": None,
 "e1": ("two_groups", "in", two_groups_overlay),
 "e2": ("documents", "in", head("PROMISES IN ZIMBABWE DOLLARS", 0.6)),
 "e3": ("documents", "right", None),
 "e4": ("pensioner", "in", both(bignum("US$3 billion+", "of pensions & insurance wiped out", "three"), src("Smith Commission via NewsDay; Equal Times"))),
 "e5": ("cattle", "right", head("THINGS YOU CAN'T PRINT", "print")),
 "e6": ("house", "in", None),
 "e7": ("two_exchanges", "in", label("THE 'OLD MUTUAL IMPLIED RATE'", "share price gap used to measure the collapse", "gap")),
 "e8": ("loan_repaid", "in", head("DEBTS SHRANK TO NOTHING", "inflation")),
 "e9": ("street_fx", "left", None),
 "e9b": ("house", "right", head("YOU CAN'T EAT A HOUSE", "eat")),
 "e9c": ("exporter", "in", None),
 "e10": ("balance", "in", ledger),
 "e11": ("balance", "out", head("SAVERS LOSE · DEBTORS WIN", 0.5)),
 "ch6": None,
 "f1": ("usd_market", "in", both(yr("2009"), head("THE ZIMBABWE DOLLAR IS DROPPED", "abandoned"), src("Cato; Fin24"))),
 "f2": ("usd_market", "right", head("PRICES STOP RISING", "stopped")),
 "f3": ("teller_2015", "in", both(yr("2015"), demonet, src("BusinessTech; Banknote News; CNN"))),
 "f4": ("new_notes", "in", yr("2019")),
 "f5": ("gold_vault", "in", both(yr("2024"), label("ZiG  ·  'ZIMBABWE GOLD'", "cut by more than 40% within 6 months", "September"), src("Al Jazeera; Africa Confidential"))),
 "f5b": ("weimar_1923", "right", card_box([("Germany 1923 · Hungary 1946", INK), ("Yugoslavia 1990s · Venezuela", INK)], 1.5, y=260, w=1100)),
 "f5c": ("harare_90s", "in", None),
 "f6": ("handover", "in", head("MONEY IS TRUST", "trust")),
 "f7": ("collector", "in", src("Planet Banknote; eBay (Oct 2026)")),
 "f7b": ("wallet_today", "in", both(head("~2% A YEAR: THE SAME PROCESS, SLOWER", "two"), src("US Federal Reserve; European Central Bank"))),
 "f8": ("choices", "in", card_box([("Cash · Gold · Property", INK), ("Foreign currency · Something else?", INK)], "Cash", y=280, w=1100)),
 "f9": ("choices", "out", end_overlay),
}
CHAPTERS = {"ch1": (1, "THE BREADBASKET", "tobacco_farm"), "ch2": (2, "THREE CRACKS", "trading_room"),
            "ch3": (3, "THE MACHINE", "press"), "ch4": (4, "LIFE WHEN MONEY DIES", "queue_bank"),
            "ch5": (5, "WHAT ACTUALLY SURVIVED", "balance"), "ch6": (6, "THE VERDICT", "harare_dusk")}

def make(key):
    if key in CHAPTERS: return chap(*CHAPTERS[key])
    img, move, ov = PLAN[key]
    def f(d, t, sc):
        painted(d._image, IMG(img), t, sc["dur"], move)
        if ov: ov(d, t, sc)
    return f

DRAW = {k: make(k) for k in PLAN}
PAINTED.update(PLAN)
for k in CHAPTERS: BY_KEY[k]["nocap"] = True
SUBS = [("one hundred trillion", "100 trillion"), ("seventy two percent", "72%"), ("eleven thousand", "11,000"),
        ("twenty three million", "23 million"), ("two hundred and sixty million", "260 million"), ("forty eight million", "48 million"),
        ("thirteen hundred", "1,300"), ("two hundred and thirty one million percent", "231 million percent"),
        ("seventy nine point six billion percent", "79.6 billion percent"), ("thirty US dollars", "US$30"),
        ("three billion US dollars", "US$3 billion"), ("thirty five quadrillion", "35 quadrillion"),
        ("one hundred and seventy five quadrillion", "175 quadrillion"), ("forty percent", "40%"), ("two percent", "2%"),
        ("fifteen hours", "15 hours"), ("five dollars", "$5")]
SFX = [("h3", "hundred", "impact", 0.8), ("h4", 0.6, "type", 0.5), ("b2", "seventy", "impact", 0.9),
       ("b9", "1998", "whoosh", 0.5), ("c3", "more", "paper", 0.6), ("c5", "2006", "click", 0.7), ("c6", "Two", "click", 0.7),
       ("c6", "2009", "click", 0.7), ("c6", "Twenty", "impact", 0.7), ("c8", "empty", "whoosh", 0.5), ("c11", "seventy", "impact", 0.9),
       ("c13", "trillion", "bell", 0.5), ("e4", "three", "impact", 0.7), ("e10", 0.6, "soft_pop", 0.6), ("f3", "thirty", "type", 0.6),
       ("f3", "five", "bell", 0.5), ("f9", "subscribe", "soft_pop", 0.8)] + \
      [(k, 0.05, "whoosh", 0.6) for k in CHAPTERS]
run(DRAW, subs=SUBS, sfx=SFX)
