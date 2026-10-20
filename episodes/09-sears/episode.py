"""Episode 09 (long-form): Sears Was Amazon Before Amazon. So Why Did It Die? Facts: SOURCES.md."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
from doodle import *
from doodle import _at

def gap_timeline(d, t, sc):
    """Jan 1993 catalog ends -> Jul 1994 Amazon founded -> Jul 1995 site opens."""
    overlay_dim(d, 0.5)
    rrect(d, (260, 300, 1660, 700), 24, WHITE)
    timeline(d, 420, 1500, 470, [("1993", "Sears ends\nits catalog"), ("1994", "Amazon\nfounded"), ("1995", "Amazon.com\nopens")],
             ease_out(prog(t, 0.4, 3.0)), hi=0)

def walmart_bars(d, t, sc):
    overlay_dim(d, 0.5)
    rrect(d, (560, 220, 1360, 820), 24, WHITE)
    text(d, (W / 2, 270), "US RETAIL SALES, 1990", 40, fill=GREY, w="xbold")
    bar_chart(d, (680, 320, 1240, 720), [("Walmart", 32.6, YELLOW), ("Sears stores", 31.9, RED)],
              prog(t, _at(sc, "thirty"), 2.0), fmt=lambda v: f"${v}bn")

def tower_years(d, t, sc):
    overlay_dim(d, 0.45)
    rrect(d, (400, 300, 1520, 640), 24, WHITE)
    timeline(d, 600, 1320, 440, [("1973", "Sears Tower\ntallest on Earth"), ("1998", "Petronas Towers,\nKuala Lumpur")],
             ease_out(prog(t, 0.5, 2.5)), hi=1)

def catalog_cuts(d, t, sc):
    overlay_dim(d, 0.5)
    card_box([("Big catalog: ENDED", RED), ("113 stores closed", INK), ("~50,000 jobs cut", INK)], "ending", y=330, w=900)(d, t, sc)

PLAN = {
 "h1": ("farm_catalog", "in", yr("1905")),
 "h2": ("catalog_pages", "right", None),
 "h3": ("parcel_porch", "in", head("THE EVERYTHING STORE, 100 YEARS EARLY", "century")),
 "h4": ("office_tower", "up", label("SEARS", "America's biggest retailer for most of the 1900s", 0.4)),
 "h5": ("catalog_closed", "in", yr("JANUARY 1993")),
 "h6": ("seattle_garage", "in", yr("JULY 1994")),
 "h7": ("crossroads", "in", head("COULD SEARS HAVE BEEN AMAZON?", "Amazon")),
 "a1": ("rail_station", "in", both(yr("1886"), label("RICHARD SEARS", "railroad station agent, Minnesota", "Richard"))),
 "a2": ("pocket_watches", "in", None),
 "a3": ("general_store", "right", head("STUCK WITH THE LOCAL STORE", "stuck")),
 "a4": ("watchmaker", "in", both(yr("1887"), label("ALVAH ROEBUCK", "watchmaker", "Alvah"))),
 "a5": ("catalog_pages", "left", None),
 "a5b": ("mail_room", "in", head("NOT HAPPY? SEND IT BACK", "send")),
 "a6": ("mail_room", "right", None),
 "a7": ("rfd_road", "in", both(yr("1896"), label("RURAL FREE DELIVERY", "the mail comes to the farm", "Rural"), src("Britannica; Richmond Fed"))),
 "a8": ("parcel_post", "in", both(yr("1913"), label("PARCEL POST", "the post office carries packages", "parcel"))),
 "a9": ("parcel_porch", "right", head("THE LAST MILE WAS ALREADY SOLVED", "last")),
 "a10": ("kit_house_rail", "in", yr("1908 – 1940")),
 "a11": ("kit_house_build", "in", None),
 "a12": ("kit_house_today", "right", both(bignum("70,000+", "catalog homes (most estimates)", "seventy"), src("Richmond Fed; NPR"))),
 "a13": ("everything_store", "in", card_box([("Huge selection", INK), ("Low prices", INK), ("Delivered to your door", RED)], 1.0, y=330)),
 "a13b": ("data_ledgers", "in", head("A DATA BUSINESS BEFORE DATA", "data")),
 "b1": ("cars_1920s", "in", yr("1920s")),
 "b2": ("general_wood", "in", label("ROBERT WOOD", "former army general, Sears executive", "Robert")),
 "b3": ("store_1925", "in", both(yr("1925"), label("FIRST SEARS STORE", "Chicago", "first"))),
 "b4": ("parking_lot", "right", head("FREE PARKING", "Free")),
 "b5": ("parking_lot", "out", both(yr("1929"), bignum("~300", "Sears stores", "three"), src("Britannica; EBSCO"))),
 "b6": ("store_1925", "right", head("MOVE BEFORE THE OLD BUSINESS DIES", "before")),
 "b7": ("catalog_closed", "in", None),
 "b8": ("tyre_insurance", "in", both(yr("1931"), label("ALLSTATE", "car insurance, named after a Sears tyre", "Allstate"))),
 "b9": ("suburb_1950s", "in", None),
 "b10": ("everything_store", "right", None),
 "c1": ("tower_build", "up", None),
 "c2": ("office_tower", "up", both(yr("1973"), head("TALLEST BUILDING IN THE WORLD", "tallest"))),
 "c3": ("kl_towers", "in", both(tower_years, src("New World Encyclopedia; CS Monitor"))),
 "c4": ("office_tower", "out", None),
 "c5": ("discount_store", "in", None),
 "c6": ("mall_1970s", "right", None),
 "c6b": ("boardroom", "in", None),
 "c7": ("boardroom", "right", None),
 "d1": ("stock_floor", "in", both(yr("1981"), card_box([("Dean Witter: stockbrokers", INK), ("Coldwell Banker: real estate", INK)], "Dean", y=330, w=1000))),
 "d2": ("boardroom", "in", head("SOCKS → STOCKS → HOUSE", "socks")),
 "d3": ("stock_floor", "right", head('"SOCKS AND STOCKS"', "Socks")),
 "d4": ("credit_card", "in", both(yr("1986"), label("DISCOVER CARD", "launched nationally by Sears", "Discover"))),
 "d5": ("dim_store", "in", None),
 "d6": ("arkansas_town", "in", None),
 "d7": ("number_two", "in", both(yr("1990"), walmart_bars, src("Retail Dive (Chicago Tribune); PBS"))),
 "d8": ("number_two", "out", head("SEARS IS NUMBER TWO", "number")),
 "e1": ("layoffs", "in", yr("JANUARY 1993")),
 "e2": ("catalog_closed", "in", head("LOSING $100 MILLION+ A YEAR", "losing")),
 "e3": ("layoffs", "right", both(catalog_cuts, src("Deseret News; CS Monitor; UPI"))),
 "e4": ("boardroom", "in", None),
 "e5": ("warehouse_90s", "in", card_box([("Famous brand", INK), ("Customers who order from home", INK), ("Warehouses + national shipping", INK)], "famous", y=330, w=1100)),
 "e6": ("warehouse_90s", "right", head("THE PAPER WAS THE EXPENSIVE PART", "paper")),
 "e6b": ("prodigy_pc", "in", both(yr("1984"), label("PRODIGY", "online service started by Sears + IBM", "Prodigy"), src("EBSCO; Encyclopedia.com"))),
 "e6c": ("prodigy_pc", "right", head("SEARS WASN'T LATE. IT WAS EARLY.", "early")),
 "e6d": ("catalog_closed", "in", yr("1995")),
 "e7": ("seattle_garage", "in", both(gap_timeline, src("HISTORY.com; HistoryLink"))),
 "e8": ("warehouse_90s", "in", None),
 "e9": ("prodigy_pc", "out", None),
 "e10": ("cars_1920s", "in", checklist("1990s", ["Cut the catalog first", "Before the web was visible", "Amazon built it instead"], "1920s", ["Saw the car coming", "Built stores early", "While the catalog was strong"], at=0.4)),
 "f1": ("dim_store", "in", None),
 "f2": ("dim_store", "right", both(yr("2005"), label("KMART BUYS SEARS", "deal worth about $11 billion → Sears Holdings", "Kmart"), src("NBC News; SEC filing"))),
 "f3": ("dim_store", "out", None),
 "f4": ("boardroom", "in", label("CRITICS", "sold assets, starved the stores", "Critics")),
 "f5": ("mall_1970s", "in", label("DEFENDERS", "the whole department-store sector was sinking", "Defenders")),
 "f6": ("closed_store", "in", both(yr("15 OCT 2018"), bignum("~700", "stores left at bankruptcy", "seven", col=RED), src("UPI; Chicago Sun-Times"))),
 "f7": ("office_tower", "in", label("WILLIS TOWER", "renamed in 2009", "Willis")),
 "g1": ("boardroom", "in", label("DOOMED?", "big companies protect what they have", 0.6)),
 "g2": ("discount_store", "in", None),
 "g3": ("warehouse_90s", "in", label("OR BEST PLACED OF ALL?", "customers, trust, warehouses, delivery", 0.6)),
 "g3b": ("prodigy_pc", "in", None),
 "g4": ("cars_1920s", "in", None),
 "g5": ("parking_lot", "in", head("FOLLOW CUSTOMERS EARLY", "follow")),
 "g6": ("../07-zimbabwe/images/market_cash.jpg", "in", label("THE MONEY STORIES", "Zimbabwe · lottery winners · Sears", 0.6)),
 "g7": ("crossroads", "in", head("COULD SEARS HAVE BECOME AMAZON?", "become")),
 "g8": ("crossroads", "out", end_screen("subscribe")),
}
CHAPTERS = {"ch1": (1, "THE AMAZON OF 1900", "catalog_pages"), "ch2": (2, "FOLLOWING THE CARS", "parking_lot"),
            "ch3": (3, "TOP OF THE WORLD", "office_tower"), "ch4": (4, "SOCKS AND STOCKS", "stock_floor"),
            "ch5": (5, "THE WORST-TIMED\nDECISION IN RETAIL", "catalog_closed"), "ch6": (6, "THE LONG GOODBYE", "closed_store"),
            "ch7": (7, "COULD SEARS HAVE\nBEEN AMAZON?", "crossroads")}
SUBS = [("seventy thousand", "70,000"), ("three hundred", "300"), ("twenty five years", "25 years"),
        ("thirty two point six billion dollars", "$32.6 billion"), ("thirty one point nine billion", "$31.9 billion"),
        ("one hundred and thirteen", "113"), ("fifty thousand", "50,000"), ("eleven billion dollars", "$11 billion"),
        ("seven hundred", "700"), ("twenty fifth of January", "25 January"), ("fifteenth of October", "15 October")]
SFX = [("h1", 0.4, "paper", 0.5), ("h5", 0.3, "impact", 0.6), ("a1", 0.5, "bell", 0.4), ("a12", "seventy", "soft_pop", 0.6),
       ("c2", "tallest", "impact", 0.6), ("d7", "thirty", "type", 0.6), ("e3", "ending", "impact", 0.7),
       ("e6b", "Prodigy", "soft_pop", 0.6), ("f6", "seven", "impact", 0.7), ("g8", "subscribe", "soft_pop", 0.8)]
documentary(PLAN, CHAPTERS, SUBS, SFX)
