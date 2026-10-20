"""Episode 08 (long-form): Do Lottery Winners Really Go Broke? (myth vs the research). Facts: SOURCES.md."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
from doodle import *

ZIM = "../07-zimbabwe/images/market_cash.jpg"     # callback to the previous video

def odds_counter(d, t, sc):
    """'1 in 292,201,338' typing in, with a tiny highlighted '1'."""
    overlay_dim(d, 0.5)
    a = prog(t, 1.0, 2.5)
    rrect(d, (360, 330, 1560, 600), 24, WHITE)
    text(d, (W / 2, 400), "POWERBALL JACKPOT ODDS", 44, fill=GREY, w="xbold")
    zeros(d, W / 2, 500, "1 in 292,201,338", 110, a, col=RED)

def cash_split(d, t, sc):
    overlay_dim(d, 0.5)
    a = prog(t, wt(sc, "two", default=2.0), 0.5)
    b = prog(t, wt(sc, "nine", default=5.0), 0.5)
    if a > 0:
        rrect(d, (240, 300, 900, 640), 24, WHITE)
        text(d, (570, 380), "ADVERTISED (ANNUITY)", 38, fill=GREY, w="xbold")
        text(d, (570, 500), "$2.04 billion", 88, fill=INK, alpha=a)
    if b > 0:
        rrect(d, (1020, 300, 1680, 640), 24, WHITE)
        text(d, (1350, 380), "CASH OPTION", 38, fill=GREY, w="xbold")
        text(d, (1350, 500), "$997.6 million", 80, fill=RED, alpha=b)
    c = prog(t, wt(sc, "half", default=9.0), 0.4)
    if c > 0: pill(d, W / 2, 740, "≈ HALF", YELLOW, fg=INK, a=c, size=60)

def tax_stack(d, t, sc):
    overlay_dim(d, 0.5)
    card_box([("24% withheld up front", INK), ("top federal bracket: 37%", RED), ("+ state tax in most places", GREY)],
             at="twenty", y=380, w=1000)(d, t, sc)

def bankruptcy_lines(d, t, sc):
    """Two lines converging: big winners start lower, catch up with small winners by year 5 (shape only, no numbers)."""
    overlay_dim(d, 0.55)
    rrect(d, (360, 200, 1560, 800), 24, WHITE)
    text(d, (W / 2, 250), "Share going bankrupt (illustration of the finding)", 34, fill=GREY, w="xbold")
    p = ease_out(prog(t, 0.6, 3.0))
    box = (440, 290, 1500, 720)
    small = [0.55, 0.6, 0.62, 0.64, 0.66, 0.67]; big = [0.2, 0.28, 0.42, 0.55, 0.63, 0.67]
    line_chart(d, box, [x * 100 for x in small], p, col=GREY, area=False, labels=["", "yr 1", "yr 2", "yr 3", "yr 4", "yr 5"])
    line_chart(d, box, [x * 100 for x in big], p, col=RED, area=False)
    text(d, (470, 320), "small winners", 30, fill=GREY, w="xbold", anchor="lm")
    text(d, (470, 360), "big winners ($50k–$150k)", 30, fill=RED, w="xbold", anchor="lm")

PLAN = {
 "h1": ("phone_win", "in", None),
 "h2": ("ticket_check", "in", both(head('"70% OF WINNERS GO BROKE"', "Seventy"))),
 "h3": ("headlines", "right", None),
 "h4": ("archive", "in", head("NO STUDY FOUND", "Nobody")),
 "h5": ("researcher", "in", card_box([("1. Do winners blow it all?", INK), ("2. Who wins long-term?", INK), ("3. What does it teach us?", RED)], 0.4, y=330)),
 "h6": ("canada_street", "right", head("THE TWIST: NEXT DOOR", "twist")),
 "a1": ("headlines", "in", None),
 "a1b": ("mansion_empty", "in", head('"THE LOTTERY CURSE"', "curse")),
 "a2": ("archive", "left", both(yr("2018"), card_box([('NEFE: "not from our research"', INK), ("and can't be confirmed", RED)], "statement", y=300, w=1100), src("NEFE statement (2018); The Times Herald"))),
 "a3": ("meeting_2001", "in", yr("2001")),
 "a4": ("party_gossip", "right", None),
 "a4b": ("quiet_family", "in", head("THE QUIET WINNERS DON'T MAKE NEWS", "never")),
 "a4c": ("headlines", "out", None),
 "a5": ("researcher", "in", head("WE NEED DATA", "data")),
 "b1": ("store_counter", "in", both(odds_counter, src("Powerball prize chart; AP"))),
 "b2": ("lightning", "in", both(label("$100 BILLION+ A YEAR", "spent on US lottery tickets", "hundred"), src("NASPL via NGPF; Scripps News; Motley Fool"))),
 "b2b": ("rollover", "right", None),
 "b3": ("billboard", "in", None),
 "b4": ("annuity_years", "in", card_box([("ANNUITY: paid over ~30 years", INK), ("CASH OPTION: much smaller, all now", RED)], "annuity", y=300, w=1100)),
 "b4b": ("cash_vault", "in", None),
 "b4c": ("crossroads", "in", None),
 "b5": ("cash_vault", "out", both(yr("NOVEMBER 2022"), cash_split, src("Axios; Yahoo News"))),
 "b6": ("tax_forms", "in", both(tax_stack, src("TurboTax; NerdWallet"))),
 "b7": ("split_money", "in", head("THE NUMBER YOU HEAR ≠ THE NUMBER YOU KEEP", "never")),
 "c1": ("florida_street", "right", both(yr("1993 – 2002"), label("~35,000 FLORIDA WINNERS", "Fantasy 5 lottery", "thirty"), src("Hankins, Hoekstra & Skiba (2011); Vanderbilt University"))),
 "c2": ("two_tickets", "in", card_box([("BIG: $50,000 – $150,000", RED), ("SMALL: under $10,000", GREY)], "fifty", y=280, w=900)),
 "c2b": ("researcher", "in", head("A NATURAL EXPERIMENT", "natural")),
 "c3": ("court_papers", "in", bankruptcy_lines),
 "c4": ("court_papers", "out", both(bankruptcy_lines, head("POSTPONED, NOT PREVENTED", "postponed", y=900))),
 "c5": ("late_notices", "in", None),
 "c5b": ("shopping", "right", None),
 "c6": ("quiet_family", "in", head("NOT 70% OF JACKPOT WINNERS", "not")),
 "c7": ("sweden_town", "right", None),
 "d1": ("sweden_town", "in", both(label("~250,000 PLAYERS", "followed for up to 20 years", "two"), src("Cesarini et al. (AER 2017); J-PAL"))),
 "d2": ("beach", "in", head("DID THEY QUIT WORK? MOSTLY NO", "Mostly")),
 "d3": ("sweden_office", "in", both(bignum("≈1% of the prize", "lower earnings per year", "one"), src("J-PAL; Cesarini et al. (AER 2017)"))),
 "d3b": ("sweden_town", "left", card_box([("Higher taxes · stronger safety net", INK), ("smaller prizes than US jackpots", INK)], 1.0, y=280, w=1100)),
 "d3c": ("store_counter", "in", None),
 "d3d": ("sweden_couple", "in", None),
 "d4": ("calm_porch", "in", yr("5–22 YEARS LATER")),
 "d5": ("calm_porch", "right", both(head("MORE SATISFIED FOR 10+ YEARS", "satisfied"), src("Lindqvist, Östling & Cesarini (2020); Stockholm University"))),
 "d6": ("sweden_couple", "in", card_box([("Life satisfaction: UP, lasting", DKGREEN), ("Day-to-day happiness: barely changed", GREY)], "happiness", y=280, w=1100)),
 "d7": ("calm_porch", "out", head("MONEY BOUGHT SECURITY, NOT JOY", "security")),
 "d8": ("canada_street", "in", None),
 "e1": ("dutch_street", "in", label("NETHERLANDS", "Postcode Lottery: a whole street wins", 0.6)),
 "e2": ("neighbors_car", "in", both(head("NEIGHBOURS BOUGHT MORE CARS", "buying"), src("Kuhn et al. (AER 2011); Tilburg University"))),
 "e2b": ("car_sale", "in", head("WINNERS SOLD THEIRS", "sold")),
 "e3": ("canada_street", "right", label("CANADA", "neighbours of lottery winners", 0.6)),
 "e4": ("bills_couple", "in", both(bignum("+2.4%", "neighbour bankruptcy risk per $1,000 won", "two", col=RED), src("Agarwal, Mikhed & Scholnick via ABI; Money.com"))),
 "e5": ("keeping_up", "in", head("MORE VISIBLE STUFF: CARS, HOUSES", "visible")),
 "e5b": ("pension", "in", head("HIDDEN SAVINGS: NO DIFFERENCE", "hidden")),
 "e6": ("keeping_up", "right", head("KEEPING UP WITH THE JONESES", "keeping")),
 "e7": ("neighbors_car", "out", None),
 "e8": ("canada_street", "in", head("THE REAL RISK: EVERYONE WATCHING", "watching")),
 "f1": ("ticket_check", "out", None),
 "f2": ("headlines", "in", checklist("MYTH", ['"70% go broke"'], "THE DATA", ["Medium wins: delayed, not fixed", "Big wins: keep working", "More satisfied for years", "Neighbours feel the pressure"], at=0.3)),
 "f3": ("late_notices", "in", None),
 "f4": ("sweden_office", "in", None),
 "f5": ("keeping_up", "in", None),
 "f5b": ("overwhelmed", "in", head("BIG WINS HAVE REAL RISKS", "risk")),
 "f5c": ("advisor", "in", None),
 "f6": ("bonus", "in", head("A WINDFALL CHANGES NOTHING IF HABITS DON'T", "habits")),
 "f6b": (ZIM, "in", label("LAST VIDEO", "Zimbabwe: when money disappears", 0.6)),
 "f7": ("phone_win", "out", None),
 "f8": ("crossroads", "in", card_box([("LUMP SUM: ~half, right now", INK), ("ANNUITY: full amount over 30 years", INK)], "lump", y=280, w=1150)),
 "f9": ("crossroads", "out", end_screen("subscribe")),
}
CHAPTERS = {"ch1": (1, "THE MYTH", "headlines"), "ch2": (2, "THE MONEY ISN'T\nWHAT YOU THINK", "cash_vault"),
            "ch3": (3, "DO WINNERS GO BROKE?", "court_papers"), "ch4": (4, "THE SWEDISH EXPERIMENT", "sweden_town"),
            "ch5": (5, "THE NEIGHBOURS", "neighbors_car"), "ch6": (6, "THE VERDICT", "ticket_check")}
SUBS = [("seventy percent", "70%"), ("two hundred and ninety two million", "292 million"),
        ("one hundred billion dollars", "$100 billion"), ("two point oh four billion dollar", "$2.04 billion"),
        ("nine hundred and ninety seven point six million", "$997.6 million"), ("twenty four percent", "24%"),
        ("thirty seven percent", "37%"), ("thirty five thousand", "35,000"), ("fifty and one hundred and fifty thousand dollars", "$50,000–$150,000"),
        ("two hundred and fifty thousand", "250,000"), ("one percent", "1%"), ("ten thousand", "10,000"),
        ("one thousand dollars", "$1,000"), ("two point four percent", "2.4%")]
SFX = [("h1", 0.4, "bell", 0.5), ("h4", "Nobody", "impact", 0.6), ("b1", "two", "type", 0.6), ("b5", "nine", "impact", 0.7),
       ("b6", "twenty", "paper", 0.6), ("c4", "postponed", "impact", 0.6), ("d3", "one", "soft_pop", 0.6),
       ("e4", "two", "impact", 0.8), ("f2", 0.3, "soft_pop", 0.6), ("f9", "subscribe", "soft_pop", 0.8)]
documentary(PLAN, CHAPTERS, SUBS, SFX)
