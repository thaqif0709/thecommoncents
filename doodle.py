"""The Common Cents long-form engine (rebrand, 18 Oct 2026): flat 2D doodle-explainer style copied from breakout
history/money videos — clean vector shapes, white-headed stick-figure characters with expressive eyes, bold caps
labels, timelines, simple charts, something moving every ~2 s, word-timed lower-third captions. 1920x1080 @ 30fps.

Each episode lives in episodes/<name>/ with script.json ([[key, text], ...]) + audio/<key>.{mp3,srt} (from
tools/make_voice.py) and an episode.py that does `from doodle import *`, defines one draw function per scene
key: f(d, t, sc) and calls run(DRAW, subs=SUBS, sfx=SFX, cams=CAMS).
Run from the episode folder:  python3 episode.py [out.mp4] [--preview] [--audio-only] [--from KEY --to KEY]"""
import json, math, os, random, re, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1920, 1080, 30
GAP, TAIL = 0.25, 2.0
ARGS = [a for a in sys.argv[1:]]
OUT = next((a for a in ARGS if a.endswith(".mp4")), "episode.mp4")
PREVIEW = "--preview" in ARGS

# ---------- palette ----------
BG = (247, 244, 237); BG2 = (236, 231, 220); INK = (28, 28, 32); WHITE = (255, 255, 255); GREY = (150, 148, 145)
LIGHT = (214, 210, 202); RED = (222, 66, 56); YELLOW = (250, 200, 50); BLUE = (64, 128, 206); SKY = (190, 222, 244)
GREEN = (84, 170, 104); DKGREEN = (52, 120, 72); ORANGE = (240, 140, 50); BROWN = (150, 100, 62); TAN = (222, 190, 140)
NOTE = (150, 196, 150); NOTE_D = (96, 150, 104); GOLD = (240, 186, 46); PURPLE = (120, 92, 180)
LW = 5   # standard outline width

_FD = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts")
_WEIGHTS = dict(black="Inter-Black.otf", xbold="Inter-ExtraBold.otf", bold="Inter-Bold.otf", semi="Inter-SemiBold.otf",
                med="Inter-Medium.otf", hand="LuckiestGuy-Regular.ttf", serif="DMSerifDisplay-Regular.ttf")
_FONTS = {}
def F(size, w="black"):
    k = (int(size), w)
    if k not in _FONTS: _FONTS[k] = ImageFont.truetype(os.path.join(_FD, _WEIGHTS[w]), max(6, int(size)))
    return _FONTS[k]

# ---------- easing ----------
def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def prog(t, start, dur=0.4): return clamp((t - start) / dur) if dur > 0 else float(t >= start)
def ease_out(x): return 1 - (1 - clamp(x)) ** 3
def ease_in_out(x): x = clamp(x); return 3 * x * x - 2 * x * x * x
def ease_back(x, s=1.70158):
    x = clamp(x) - 1
    return x * x * ((s + 1) * x + s) + 1
def lerp(a, b, x): return a + (b - a) * x
def mix(c1, c2, x): return tuple(int(lerp(a, b, clamp(x))) for a, b in zip(c1, c2))
def pop(t, start, dur=0.35): return ease_back(prog(t, start, dur))

# ---------- timing (same scheme as the Shorts engine) ----------
def parse_srt(path):
    words = []
    ts = lambda s: (lambda h, m, r: int(h) * 3600 + int(m) * 60 + float(r.replace(",", ".")))(*s.split(":"))
    for block in open(path).read().strip().split("\n\n"):
        lines = block.strip().split("\n")
        if len(lines) < 3: continue
        a, b = lines[1].split(" --> ")
        words.append((ts(a), ts(b), " ".join(lines[2:])))
    return words

def duration(path):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
                                capture_output=True, text=True).stdout)

SCRIPT = json.load(open("script.json"))
SCENES, _t0 = [], 0.0
for _i, (_key, _text) in enumerate(SCRIPT):
    _words = parse_srt(f"audio/{_key}.srt")
    _lead = max(0.0, _words[0][0] - 0.06) if _words else 0.0
    _words = [(a - _lead, b - _lead, w) for a, b, w in _words]
    _spoken = _words[-1][1] + 0.15 if _words else duration(f"audio/{_key}.mp3")
    _gap = TAIL if _i == len(SCRIPT) - 1 else (0.7 if _key.startswith("ch") else GAP)   # breathe after chapter cards
    SCENES.append(dict(key=_key, start=_t0, dur=_spoken + _gap, lead=_lead, words=_words, idx=_i))
    _t0 += _spoken + _gap
TOTAL = _t0
BY_KEY = {s["key"]: s for s in SCENES}

def wt(scene, word, nth=0, default=None):
    """Local start time of a spoken word in a scene (case/punct-insensitive prefix match)."""
    norm = lambda s: re.sub(r"[^a-z0-9]", "", s.lower())
    hits = [w[0] for w in scene["words"] if norm(w[2]).startswith(norm(word))]
    if len(hits) > nth: return hits[nth]
    return scene["dur"] * 0.4 if default is None else default

# ---------- primitives ----------
def text(d, xy, s, size, fill=INK, w="black", anchor="mm", stroke=0, stroke_fill=WHITE, alpha=1.0, max_w=1700):
    if alpha <= 0 or not s: return
    f = F(size, w)
    while size > 14 and d.textlength(s, font=f) > max_w:
        size *= 0.94; f = F(size, w)
    col = mix(BG, fill, alpha) if alpha < 1 else fill
    d.text(xy, s, font=f, fill=col, anchor=anchor, stroke_width=stroke, stroke_fill=stroke_fill)

def marker(d, xy, s, size, fill=INK, hi=YELLOW, a=1.0, w="black", anchor="mm", pad=14):
    """Bold label with a highlighter-marker box behind it that wipes in left to right (a: 0..1)."""
    if a <= 0: return
    f = F(size, w); tw = d.textlength(s, font=f)
    x, y = xy
    x0 = x - tw / 2 if anchor[0] == "m" else (x if anchor[0] == "l" else x - tw)
    box = (x0 - pad, y - size * 0.62, x0 - pad + (tw + 2 * pad) * ease_out(a), y + size * 0.62)
    if box[2] > box[0]: d.rounded_rectangle(box, radius=8, fill=hi)
    if a > 0.3: text(d, (x0, y), s, size, fill=fill, w=w, anchor="l" + anchor[1])

def rrect(d, box, r, fill, ow=LW, outline=INK):
    x0, y0, x1, y1 = box
    if x1 - x0 < 2 or y1 - y0 < 2: return
    d.rounded_rectangle(box, radius=int(max(0, min(r, (x1 - x0) / 2, (y1 - y0) / 2))), fill=fill, outline=outline if ow else None, width=ow)

def circle(d, cx, cy, r, fill, ow=LW, outline=INK):
    if r < 1: return
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=fill, outline=outline if ow else None, width=ow)

def poly(d, pts, fill, ow=LW, outline=INK):
    d.polygon(pts, fill=fill, outline=outline if ow else None, width=ow)

def line(d, pts, w=LW, fill=INK):
    d.line(pts, fill=fill, width=int(w), joint="curve")
    if len(pts) >= 2 and w > 4:
        r = w / 2 - 0.5
        for (x, y) in (pts[0], pts[-1]): d.ellipse((x - r, y - r, x + r, y + r), fill=fill)

def shadow(d, cx, base, rx, a=1.0):
    if rx < 2: return
    d.ellipse((cx - rx, base - rx * 0.12, cx + rx, base + rx * 0.12), fill=mix(BG, BG2, a))

def pill(d, cx, cy, label, bg=RED, fg=WHITE, a=1.0, size=40, w="black"):
    if a <= 0: return
    s = ease_back(a)
    f = F(size, w); tw = d.textlength(label, font=f)
    hw, hh = (tw / 2 + size * 0.7) * s, size * 0.85 * s
    rrect(d, (cx - hw, cy - hh, cx + hw, cy + hh), hh, bg, ow=0)
    if a > 0.4: text(d, (cx, cy + 1), label, size * s, fill=fg, w=w)

def arrow(d, p0, p1, a=1.0, col=INK, w=8, head=26, bend=0.0):
    """Arrow drawn from p0 toward p1 (a: 0..1 reveal). bend > 0 curves it."""
    if a <= 0: return
    (x0, y0), (x1, y1) = p0, p1
    L = math.hypot(x1 - x0, y1 - y0) or 1
    cx, cy = (x0 + x1) / 2 - (y1 - y0) / L * bend * L, (y0 + y1) / 2 + (x1 - x0) / L * bend * L
    n = 24; upto = max(2, int(n * clamp(a)) + 1)
    pts = [((1 - u) ** 2 * x0 + 2 * (1 - u) * u * cx + u * u * x1, (1 - u) ** 2 * y0 + 2 * (1 - u) * u * cy + u * u * y1)
           for u in (i / n for i in range(upto))]
    line(d, pts, w, col)
    if a >= 0.98:
        (ax, ay), (bx, by) = pts[-2], pts[-1]
        ang = math.atan2(by - ay, bx - ax)
        poly(d, [(bx + head * 0.4 * math.cos(ang), by + head * 0.4 * math.sin(ang)),
                 (bx - head * math.cos(ang - 0.5), by - head * math.sin(ang - 0.5)),
                 (bx - head * math.cos(ang + 0.5), by - head * math.sin(ang + 0.5))], col, ow=0)

def ground(d, y=860, col=BG2):
    d.rectangle((0, y, W, H), fill=col)
    d.line((0, y, W, y), fill=INK, width=LW)

# ---------- stick figure ----------
POSES = {   # arm angles in degrees from straight down (positive = outward), per side (L, R); legs spread
    "stand": (12, 12), "wave": (12, 150), "shrug": (70, 70), "point": (12, 95), "cheer": (150, 150),
    "hold": (55, 55), "think": (12, 140), "sad": (6, 6), "push": (80, 80), "carry": (100, 100),
}
def stick(d, x, base, s=1.0, pose="stand", mood="neutral", look=0, t=0.0, walk=0.0, col=INK, shirt=None, hat=None,
          flip=False, held=None):
    """White-headed stick figure standing on `base`. walk: walking speed (0 = still). held(hx, hy): draw an object at
    the hands. look: -1..1 eye direction. mood: neutral/happy/sad/shock/angry/think/smug/worried."""
    if s <= 0.05: return
    lw = max(3, int(9 * s))
    hr = 46 * s
    leg = 120 * s; body = 130 * s
    hip = (x, base - leg)
    neck = (x, hip[1] - body)
    head = (x, neck[1] - hr * 0.95)
    ph = t * 7 * walk
    sw = math.sin(ph) * 0.45 if walk else 0.0
    spread = 0.18
    for side, k in ((-1, 0), (1, 1)):
        a = side * spread + (sw if k else -sw)
        foot = (hip[0] + math.sin(a) * leg, hip[1] + math.cos(a) * leg)
        if walk: foot = (foot[0], min(base, foot[1] - max(0, math.sin(ph + k * math.pi)) * 14 * s))
        line(d, [hip, foot], lw, col)
    if shirt:   # simple tunic / shirt shape
        poly(d, [(neck[0] - 30 * s, neck[1] + 8 * s), (neck[0] + 30 * s, neck[1] + 8 * s), (hip[0] + 38 * s, hip[1] + 6 * s),
                 (hip[0] - 38 * s, hip[1] + 6 * s)], shirt, ow=max(2, int(4 * s)))
    else:
        line(d, [neck, hip], lw, col)
    la, ra = POSES.get(pose, POSES["stand"])
    if pose == "wave": ra += math.sin(t * 9) * 18
    if walk: la, ra = la + math.sin(ph) * 25, ra - math.sin(ph) * 25
    if flip: la, ra = ra, la
    sh = (neck[0], neck[1] + 14 * s)
    hands = []
    for side, ang in ((-1, la), (1, ra)):
        r = math.radians(ang)
        elbow = (sh[0] + side * math.sin(r) * 60 * s, sh[1] + math.cos(r) * 60 * s)
        r2 = math.radians(ang + (25 if ang > 60 else 8))
        hand = (elbow[0] + side * math.sin(r2) * 58 * s, elbow[1] + math.cos(r2) * 58 * s)
        line(d, [sh, elbow, hand], lw, col)
        hands.append(hand)
    if held: held((hands[0][0] + hands[1][0]) / 2, (hands[0][1] + hands[1][1]) / 2)
    # head
    circle(d, head[0], head[1], hr, WHITE, ow=max(2, int(6 * s)), outline=col)
    if hat: hat(head[0], head[1] - hr * 0.7, s)
    ex = look * 10 * s
    blink = (t + x * 0.001) % 3.9 < 0.1
    eh = {"shock": 13, "worried": 10}.get(mood, 9) * s
    for side in (-1, 1):
        cx, cy = head[0] + side * 16 * s + ex, head[1] - 4 * s
        if blink: d.line((cx - 6 * s, cy, cx + 6 * s, cy), fill=INK, width=max(2, int(4 * s)))
        else: d.ellipse((cx - 6 * s, cy - eh, cx + 6 * s, cy + eh), fill=INK)
        bw = max(2, int(5 * s)); by = cy - eh - 9 * s
        if mood in ("angry",): d.line((cx - 10 * s * side, by - 6 * s, cx + 10 * s * side, by + 4 * s), fill=INK, width=bw)
        elif mood in ("sad", "worried"): d.line((cx - 10 * s * side, by + 4 * s, cx + 10 * s * side, by - 6 * s), fill=INK, width=bw)
        elif mood in ("shock",): d.arc((cx - 11 * s, by - 10 * s, cx + 11 * s, by + 6 * s), 200, 340, fill=INK, width=bw)
        elif mood == "smug": d.line((cx - 10 * s, by, cx + 10 * s, by - 3 * s * side), fill=INK, width=bw)
    my = head[1] + 22 * s; mw = max(2, int(5 * s))
    if mood == "happy": d.chord((head[0] - 16 * s + ex, my - 12 * s, head[0] + 16 * s + ex, my + 12 * s), 0, 180, fill=INK)
    elif mood in ("sad", "worried"): d.arc((head[0] - 14 * s + ex, my, head[0] + 14 * s + ex, my + 16 * s), 200, 340, fill=INK, width=mw)
    elif mood == "shock": d.ellipse((head[0] - 9 * s + ex, my - 6 * s, head[0] + 9 * s + ex, my + 14 * s), fill=INK)
    elif mood == "smug": d.arc((head[0] - 14 * s + ex, my - 12 * s, head[0] + 18 * s + ex, my + 6 * s), 20, 150, fill=INK, width=mw)
    elif mood == "think": d.line((head[0] - 8 * s + ex, my + 4 * s, head[0] + 12 * s + ex, my), fill=INK, width=mw)
    else: d.line((head[0] - 10 * s + ex, my + 2 * s, head[0] + 10 * s + ex, my + 2 * s), fill=INK, width=mw)
    return dict(head=head, hands=hands, top=head[1] - hr)

def bubble(d, x, y, s, a=1.0, kind="think", label="", size=44, fill=WHITE):
    """Speech/thought bubble with an optional label, tail pointing down-left toward (x, y)."""
    if a <= 0: return
    sc = ease_back(a)
    f = F(size, "xbold"); tw = d.textlength(label, font=f) if label else 120
    bw, bh = (tw / 2 + 40) * sc, (size * 1.1) * sc
    cx, cy = x + 40 * sc + bw, y - 70 * sc - bh
    rrect(d, (cx - bw, cy - bh, cx + bw, cy + bh), bh, fill)
    if kind == "think":
        for k, r in enumerate((14, 9)): circle(d, x + 10 + k * 18 * sc, y - 30 - k * 26 * sc, r * sc, fill)
    else:
        poly(d, [(cx - bw * 0.6, cy + bh - 6), (cx - bw * 0.3, cy + bh - 6), (x + 10, y - 10)], fill, ow=0)
        d.line((cx - bw * 0.6, cy + bh - 3, x + 10, y - 10, cx - bw * 0.3, cy + bh - 3), fill=INK, width=LW)
    if label and a > 0.5: text(d, (cx, cy + 2), label, size * sc, w="xbold")

# ---------- objects (flat, outlined) ----------
def banknote(d, cx, cy, s=1.0, value="100", unit="", ang=0.0, col=NOTE, dark=NOTE_D):
    """Generic cartoon banknote (not a real design)."""
    if s <= 0.05: return
    w, h = int(300 * s), int(150 * s)
    lay = Image.new("RGBA", (w + 10, h + 10), (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
    ld.rounded_rectangle((3, 3, w + 3, h + 3), radius=int(10 * s), fill=col + (255,), outline=INK + (255,), width=max(2, int(5 * s)))
    ld.rounded_rectangle((3 + 12 * s, 3 + 12 * s, w + 3 - 12 * s, h + 3 - 12 * s), radius=int(6 * s), outline=dark + (255,), width=max(1, int(4 * s)))
    ld.ellipse((w * 0.6, h * 0.22, w * 0.86, h * 0.8), fill=dark + (255,))
    ld.text((w * 0.32, h * (0.42 if unit else 0.5)), value, font=F(max(8, int(66 * s)), "black"), fill=INK + (255,), anchor="mm")
    if unit: ld.text((w * 0.32, h * 0.76), unit, font=F(max(6, int(20 * s)), "xbold"), fill=INK + (255,), anchor="mm")
    if ang: lay = lay.rotate(math.degrees(-ang), expand=True, resample=Image.BICUBIC)
    d._image.paste(lay, (int(cx - lay.width / 2), int(cy - lay.height / 2)), lay)

def cash_brick(d, x, base, s=1.0, col=NOTE):
    if s <= 0.05: return
    rrect(d, (x - 70 * s, base - 46 * s, x + 70 * s, base), 6 * s, col, ow=max(2, int(4 * s)))
    d.rectangle((x - 14 * s, base - 46 * s, x + 14 * s, base), fill=TAN, outline=INK, width=max(2, int(3 * s)))

def cash_pile(d, cx, base, n, s=1.0):
    """Pyramid of cash bricks (n bricks)."""
    k = 0; row = 0
    while k < n:
        per = max(1, 5 - row)
        for j in range(per):
            if k >= n: break
            cash_brick(d, cx + (j - (per - 1) / 2) * 142 * s, base - row * 46 * s, s); k += 1
        row += 1

def coin(d, cx, cy, r, label="$", col=GOLD):
    if r < 4: return
    circle(d, cx, cy, r, col, ow=max(2, int(r / 9)))
    circle(d, cx, cy, r * 0.74, None, ow=max(1, int(r / 14)), outline=mix(col, INK, 0.35))
    if label: text(d, (cx, cy + 1), label, r * 0.95, fill=INK)

def house(d, cx, base, s=1.0, col=TAN, roof=RED):
    if s <= 0.05: return
    rrect(d, (cx - 110 * s, base - 160 * s, cx + 110 * s, base), 4, col, ow=max(2, int(5 * s)))
    poly(d, [(cx - 140 * s, base - 150 * s), (cx, base - 270 * s), (cx + 140 * s, base - 150 * s)], roof, ow=max(2, int(5 * s)))
    rrect(d, (cx - 26 * s, base - 90 * s, cx + 26 * s, base), 4, BROWN, ow=max(2, int(4 * s)))
    rrect(d, (cx + 46 * s, base - 125 * s, cx + 90 * s, base - 80 * s), 3, SKY, ow=max(2, int(4 * s)))
    rrect(d, (cx - 90 * s, base - 125 * s, cx - 46 * s, base - 80 * s), 3, SKY, ow=max(2, int(4 * s)))

def shop(d, cx, base, s=1.0, sign="SHOP", col=BLUE, shelves=1.0):
    """Shop front; shelves 0..1 = how full the window shelves are."""
    if s <= 0.05: return
    rrect(d, (cx - 200 * s, base - 260 * s, cx + 200 * s, base), 4, WHITE, ow=max(2, int(5 * s)))
    rrect(d, (cx - 215 * s, base - 330 * s, cx + 215 * s, base - 260 * s), 6, col, ow=max(2, int(5 * s)))
    text(d, (cx, base - 295 * s), sign, 42 * s, fill=WHITE, max_w=380 * s)
    for k in range(7):
        x0 = cx - 215 * s + k * 430 / 7 * s
        poly(d, [(x0, base - 260 * s), (x0 + 430 / 7 * s, base - 260 * s), (x0 + 430 / 7 * s, base - 225 * s), (x0, base - 225 * s)],
             RED if k % 2 == 0 else WHITE, ow=max(1, int(3 * s)))
    rrect(d, (cx + 40 * s, base - 190 * s, cx + 110 * s, base), 4, BROWN, ow=max(2, int(4 * s)))
    rrect(d, (cx - 180 * s, base - 200 * s, cx + 10 * s, base - 40 * s), 4, SKY, ow=max(2, int(4 * s)))
    for row in range(2):
        y = base - 140 * s + row * 60 * s
        d.line((cx - 170 * s, y, cx, y), fill=INK, width=max(2, int(3 * s)))
        for j in range(int(5 * shelves)):
            c = (RED, YELLOW, GREEN, ORANGE, BLUE)[(j + row) % 5]
            rrect(d, (cx - 165 * s + j * 33 * s, y - 34 * s, cx - 140 * s + j * 33 * s, y), 3, c, ow=max(1, int(2 * s)))

def bank(d, cx, base, s=1.0, label="BANK"):
    if s <= 0.05: return
    rrect(d, (cx - 250 * s, base - 36 * s, cx + 250 * s, base), 3, LIGHT, ow=max(2, int(5 * s)))
    for k in range(5):
        x = cx - 190 * s + k * 95 * s
        rrect(d, (x - 22 * s, base - 270 * s, x + 22 * s, base - 36 * s), 3, WHITE, ow=max(2, int(4 * s)))
    rrect(d, (cx - 260 * s, base - 316 * s, cx + 260 * s, base - 270 * s), 3, LIGHT, ow=max(2, int(5 * s)))
    poly(d, [(cx - 280 * s, base - 316 * s), (cx, base - 430 * s), (cx + 280 * s, base - 316 * s)], WHITE, ow=max(2, int(5 * s)))
    text(d, (cx, base - 293 * s), label, 34 * s, max_w=480 * s)

def factory(d, cx, base, s=1.0, smoke=True, t=0.0, col=LIGHT):
    if s <= 0.05: return
    for k in range(3):
        x = cx - 210 * s + k * 140 * s
        poly(d, [(x, base - 150 * s), (x + 140 * s, base - 220 * s), (x + 140 * s, base - 150 * s)], col, ow=max(2, int(5 * s)))
    rrect(d, (cx - 210 * s, base - 150 * s, cx + 210 * s, base), 3, col, ow=max(2, int(5 * s)))
    rrect(d, (cx + 120 * s, base - 330 * s, cx + 170 * s, base - 150 * s), 3, RED, ow=max(2, int(5 * s)))
    for k in range(4): rrect(d, (cx - 180 * s + k * 90 * s, base - 110 * s, cx - 130 * s + k * 90 * s, base - 60 * s), 3, YELLOW, ow=max(2, int(4 * s)))
    if smoke:
        for k in range(4):
            ph = (t * 0.5 + k / 4) % 1
            circle(d, cx + 145 * s + ph * 80 * s, base - 350 * s - ph * 160 * s, (18 + ph * 30) * s, mix(LIGHT, BG, ph), ow=0)

def farm(d, cx, base, s=1.0, crop=1.0, col=GREEN):
    """Field with rows of crops; crop 0..1 = how much is growing."""
    if s <= 0.05: return
    poly(d, [(cx - 330 * s, base), (cx + 330 * s, base), (cx + 250 * s, base - 120 * s), (cx - 250 * s, base - 120 * s)], TAN, ow=max(2, int(5 * s)))
    for row in range(4):
        y = base - 20 * s - row * 28 * s; half = (320 - row * 22) * s
        for j in range(int(14 * crop)):
            x = cx - half + (j + 0.5) * (2 * half / 14)
            line(d, [(x, y), (x, y - 26 * s)], max(2, 4 * s), DKGREEN)
            circle(d, x, y - 30 * s, 9 * s, col, ow=max(1, int(3 * s)))

def tractor(d, cx, base, s=1.0, col=RED):
    if s <= 0.05: return
    rrect(d, (cx - 120 * s, base - 150 * s, cx + 40 * s, base - 60 * s), 8, col, ow=max(2, int(5 * s)))
    rrect(d, (cx - 100 * s, base - 240 * s, cx - 10 * s, base - 150 * s), 6, SKY, ow=max(2, int(5 * s)))
    rrect(d, (cx + 40 * s, base - 120 * s, cx + 130 * s, base - 60 * s), 6, col, ow=max(2, int(5 * s)))
    circle(d, cx - 70 * s, base - 70 * s, 70 * s, INK); circle(d, cx - 70 * s, base - 70 * s, 26 * s, GREY, ow=0)
    circle(d, cx + 100 * s, base - 38 * s, 38 * s, INK); circle(d, cx + 100 * s, base - 38 * s, 14 * s, GREY, ow=0)

def bread(d, cx, base, s=1.0):
    if s <= 0.05: return
    pts = [(cx + 140 * s * math.cos(a), base - 70 * s - 80 * s * math.sin(a) ** 0.7) for a in (math.pi * i / 30 for i in range(31))]
    poly(d, pts + [(cx - 140 * s, base), (cx + 140 * s, base)], (226, 160, 82), ow=max(2, int(5 * s)))
    for k in (-1, 0, 1): d.arc((cx + k * 70 * s - 26 * s, base - 128 * s - abs(k) * 0 * s, cx + k * 70 * s + 26 * s, base - 84 * s), 200, 340, fill=BROWN, width=max(2, int(6 * s)))

def egg(d, cx, base, s=1.0):
    if s <= 0.05: return
    d.ellipse((cx - 30 * s, base - 84 * s, cx + 30 * s, base), fill=WHITE, outline=INK, width=max(2, int(4 * s)))

def cow(d, cx, base, s=1.0, t=0.0):
    if s <= 0.05: return
    lw = max(2, int(5 * s))
    for dx in (-100, -60, 60, 100): line(d, [(cx + dx * s, base - 80 * s), (cx + dx * s, base)], max(3, 14 * s))
    rrect(d, (cx - 150 * s, base - 210 * s, cx + 140 * s, base - 70 * s), 60 * s, WHITE, ow=lw)
    for (x0, y0, x1, y1) in ((-110, -190, -40, -130), (10, -185, 80, -120), (-50, -120, 0, -82)):
        d.ellipse((cx + x0 * s, base + y0 * s, cx + x1 * s, base + y1 * s), fill=INK)
    hx, hy = cx + 165 * s, base - 200 * s
    rrect(d, (hx - 55 * s, hy - 55 * s, hx + 55 * s, hy + 60 * s), 40 * s, WHITE, ow=lw)
    rrect(d, (hx - 46 * s, hy + 10 * s, hx + 46 * s, hy + 60 * s), 24 * s, (240, 170, 160), ow=lw)
    for side in (-1, 1):
        d.ellipse((hx + side * 22 * s - 6 * s, hy - 26 * s, hx + side * 22 * s + 6 * s, hy - 8 * s), fill=INK)
        line(d, [(hx + side * 40 * s, hy - 46 * s), (hx + side * 64 * s, hy - 78 * s)], max(3, 9 * s), TAN)

def gold_bar(d, cx, base, s=1.0):
    if s <= 0.05: return
    poly(d, [(cx - 100 * s, base), (cx + 100 * s, base), (cx + 72 * s, base - 70 * s), (cx - 72 * s, base - 70 * s)], GOLD, ow=max(2, int(5 * s)))
    line(d, [(cx - 50 * s, base - 54 * s), (cx + 10 * s, base - 54 * s)], max(2, 7 * s), (255, 236, 160))

def press(d, cx, base, s=1.0, t=0.0, running=True, label="PRINT"):
    """Money printing press — the recurring 'machine' in money stories."""
    if s <= 0.05: return
    bob = math.sin(t * 10) * 7 * s if running else 0
    rrect(d, (cx - 220 * s, base - 240 * s, cx + 220 * s, base), 14, BLUE, ow=max(2, int(5 * s)))
    rrect(d, (cx - 160 * s, base - 360 * s + bob, cx + 160 * s, base - 236 * s + bob), 12, RED, ow=max(2, int(5 * s)))
    text(d, (cx, base - 298 * s + bob), label, 46 * s, fill=WHITE, max_w=290 * s)
    for side in (-1, 1):
        wx, wy, r = cx + side * 140 * s, base - 120 * s, 58 * s
        circle(d, wx, wy, r, YELLOW, ow=max(2, int(5 * s)))
        for k in range(3):
            aa = t * (5 if running else 0) * side + k * 2.094
            d.line((wx, wy, wx + r * 0.8 * math.cos(aa), wy + r * 0.8 * math.sin(aa)), fill=INK, width=max(2, int(5 * s)))
    rrect(d, (cx - 70 * s, base - 70 * s, cx + 70 * s, base - 30 * s), 6, INK, ow=0)

def notes_out(d, t, src, n=8, spread=500, speed=1.0, seed=2, value="", s=0.45, until=1e9, floor=850):
    """Banknotes spewing out of src and fluttering to the floor (continuous while t < until)."""
    r = random.Random(seed)
    for k in range(n * 3):
        st = k * 0.33 / speed
        u = (t - st) / 1.6
        if 0 <= u <= 1 and st < until:
            dx = r.uniform(-1, 1) * spread
            x = src[0] + dx * u
            y = min(floor, src[1] - 160 * math.sin(math.pi * min(1, u * 1.3)) + 320 * u * u)
            banknote(d, x, y, s, value, ang=u * 5 * r.choice((-1, 1)))

def wheelbarrow(d, cx, base, s=1.0, bricks=10):
    if s <= 0.05: return
    poly(d, [(cx - 190 * s, base - 160 * s), (cx + 140 * s, base - 160 * s), (cx + 100 * s, base - 66 * s), (cx - 140 * s, base - 66 * s)], RED, ow=max(2, int(5 * s)))
    for k in range(bricks):
        cash_brick(d, cx - 120 * s + (k % 4) * 78 * s, base - 160 * s - (k // 4) * 40 * s, 0.55 * s)
    line(d, [(cx - 140 * s, base - 100 * s), (cx - 310 * s, base - 140 * s)], max(3, 12 * s))
    line(d, [(cx - 60 * s, base - 66 * s), (cx - 90 * s, base)], max(3, 10 * s))
    circle(d, cx + 110 * s, base - 40 * s, 40 * s, INK); circle(d, cx + 110 * s, base - 40 * s, 14 * s, GREY, ow=0)

def calendar(d, cx, cy, s=1.0, top="", big=""):
    if s <= 0.05: return
    rrect(d, (cx - 110 * s, cy - 120 * s, cx + 110 * s, cy + 120 * s), 14, WHITE, ow=max(2, int(5 * s)))
    rrect(d, (cx - 110 * s, cy - 120 * s, cx + 110 * s, cy - 50 * s), 14, RED, ow=max(2, int(5 * s)))
    text(d, (cx, cy - 85 * s), top, 36 * s, fill=WHITE, max_w=200 * s)
    text(d, (cx, cy + 35 * s), big, 90 * s, max_w=200 * s)

def clock(d, cx, cy, r, t, speed=1.0):
    circle(d, cx, cy, r, WHITE, ow=max(3, int(r / 14)))
    for frac, ln, wd in ((t * speed / 12, 0.48, r / 10), (t * speed, 0.74, r / 16)):
        a = 2 * math.pi * frac - math.pi / 2
        d.line((cx, cy, cx + r * ln * math.cos(a), cy + r * ln * math.sin(a)), fill=INK, width=max(2, int(wd)))
    circle(d, cx, cy, r / 10, RED, ow=0)

def scale_balance(d, cx, base, s=1.0, tilt=0.0, left=None, right=None):
    """Balance scale; tilt -1..1 (positive = right side down). left/right(x, y) draw items on the pans."""
    if s <= 0.05: return
    line(d, [(cx, base), (cx, base - 300 * s)], max(3, 12 * s)); line(d, [(cx - 90 * s, base), (cx + 90 * s, base)], max(3, 12 * s))
    a = tilt * 0.35; L = 230 * s
    lx, ly = cx - L * math.cos(a), base - 300 * s - L * math.sin(a)
    rx, ry = cx + L * math.cos(a), base - 300 * s + L * math.sin(a)
    line(d, [(lx, ly), (rx, ry)], max(3, 10 * s))
    for (px, py, item) in ((lx, ly, left), (rx, ry, right)):
        d.line((px, py, px - 70 * s, py + 110 * s), fill=INK, width=max(2, int(3 * s)))
        d.line((px, py, px + 70 * s, py + 110 * s), fill=INK, width=max(2, int(3 * s)))
        d.chord((px - 90 * s, py + 80 * s, px + 90 * s, py + 140 * s), 0, 180, fill=LIGHT, outline=INK, width=max(2, int(4 * s)))
        if item: item(px, py + 110 * s)
    circle(d, cx, base - 300 * s, 14 * s, YELLOW)

def flag(d, x, base, s=1.0, cols=(GREEN, YELLOW, RED, INK), t=0.0):
    """Generic striped flag on a pole (abstract — not a real national flag)."""
    if s <= 0.05: return
    line(d, [(x, base), (x, base - 300 * s)], max(3, 8 * s))
    n = len(cols)
    for k, c in enumerate(cols):
        y0 = base - 300 * s + k * 120 / n * s
        pts = [(x + u * 180 * s, y0 + math.sin(t * 4 + u * 4) * 8 * s) for u in (i / 8 for i in range(9))]
        pts += [(px, py + 120 / n * s) for px, py in reversed(pts)]
        poly(d, pts, c, ow=max(1, int(3 * s)))

# ---------- charts / info graphics ----------
def line_chart(d, box, values, p=1.0, col=RED, labels=(), log=False, area=True, ylabels=()):
    """values: list of y in data units, auto-scaled (log10 if log). Revealed left to right by p."""
    x0, y0, x1, y1 = box
    d.line((x0, y0, x0, y1, x1, y1), fill=INK, width=LW)
    vs = [math.log10(max(v, 1e-9)) for v in values] if log else list(values)
    lo, hi = min(vs), max(vs); hi = hi if hi > lo else lo + 1
    pts = [(x0 + 20 + (x1 - x0 - 40) * i / max(1, len(vs) - 1), y1 - 20 - (y1 - y0 - 40) * (v - lo) / (hi - lo)) for i, v in enumerate(vs)]
    upto = clamp(p) * (len(pts) - 1)
    shown = [q for i, q in enumerate(pts) if i <= upto]
    if 0 < upto < len(pts) - 1:
        i = int(upto); f = upto - i
        shown.append((lerp(pts[i][0], pts[i + 1][0], f), lerp(pts[i][1], pts[i + 1][1], f)))
    if len(shown) > 1:
        if area: poly(d, shown + [(shown[-1][0], y1), (shown[0][0], y1)], mix(BG, col, 0.18), ow=0)
        line(d, shown, 9, col)
        circle(d, shown[-1][0], shown[-1][1], 12, col, ow=4)
    for i, lab in enumerate(labels):
        if lab and i < len(pts): text(d, (pts[i][0], y1 + 34), str(lab), 28, fill=GREY, w="bold")
    for frac, lab in ylabels:
        yy = y1 - 20 - (y1 - y0 - 40) * frac
        text(d, (x0 - 16, yy), lab, 26, fill=GREY, w="bold", anchor="rm")
    return pts

def bar_chart(d, box, items, p=1.0, fmt=str):
    """items: [(label, value, colour)] — bars grow with p."""
    x0, y0, x1, y1 = box
    d.line((x0, y1, x1, y1), fill=INK, width=LW)
    mx = max(v for _, v, _ in items) or 1
    n = len(items); bw = (x1 - x0) / n * 0.6
    for i, (lab, v, c) in enumerate(items):
        cx = x0 + (x1 - x0) * (i + 0.5) / n
        hh = (y1 - y0 - 60) * v / mx * ease_out(clamp(p * n - i * 0.6))
        if hh > 2: rrect(d, (cx - bw / 2, y1 - hh, cx + bw / 2, y1), 8, c)
        text(d, (cx, y1 + 36), lab, 30, w="bold", max_w=bw * 1.6)
        if hh > 2: text(d, (cx, y1 - hh - 30), fmt(v), 32, w="black")

def timeline(d, x0, x1, y, items, p=1.0, hi=None):
    """items = [(year, label)] evenly spaced, revealed by p; hi = index to highlight."""
    d.line((x0, y, x1, y), fill=LIGHT, width=10)
    d.line((x0, y, x0 + (x1 - x0) * clamp(p), y), fill=INK, width=10)
    n = len(items)
    for k, (yr, lab) in enumerate(items):
        u = k / max(1, n - 1)
        if p + 1e-6 < u: break
        x = x0 + (x1 - x0) * u
        circle(d, x, y, 20, RED if k == hi else YELLOW)
        text(d, (x, y - 56), str(yr), 44, fill=RED if k == hi else INK)
        for j, ln in enumerate(lab.split("\n")): text(d, (x, y + 56 + j * 38), ln, 32, fill=GREY, w="bold")

def big_number(d, cx, cy, value, label="", a=1.0, col=INK, size=200, sub_col=GREY):
    if a <= 0: return
    s = ease_back(a)
    text(d, (cx, cy), value, size * s, fill=col)
    if label and a > 0.5: text(d, (cx, cy + size * 0.68), label, size * 0.24, fill=sub_col, w="xbold")

def zeros(d, cx, cy, digits, size=110, a=1.0, col=INK):
    """A long number like 100,000,000,000,000 that types itself in (a: 0..1)."""
    n = max(1, int(len(digits) * clamp(a)))
    text(d, (cx, cy), digits[:n], size, fill=col)

def card(d, box, title="", body="", col=WHITE, a=1.0, title_col=INK):
    if a <= 0: return
    x0, y0, x1, y1 = box
    off = (1 - ease_out(a)) * 60
    rrect(d, (x0, y0 + off, x1, y1 + off), 22, col)
    if title: text(d, ((x0 + x1) / 2, y0 + off + 60), title, 50, fill=title_col, max_w=x1 - x0 - 40)
    for j, ln in enumerate(body.split("\n") if body else []):
        text(d, ((x0 + x1) / 2, y0 + off + 130 + j * 50), ln, 36, fill=INK, w="semi", max_w=x1 - x0 - 40)

def check_cross(d, cx, cy, ok, a=1.0, r=46):
    if a <= 0: return
    s = ease_back(a)
    circle(d, cx, cy, r * s, GREEN if ok else RED, ow=0)
    w = max(3, int(12 * s))
    if ok: d.line((cx - 20 * s, cy, cx - 4 * s, cy + 18 * s, cx + 24 * s, cy - 18 * s), fill=WHITE, width=w, joint="curve")
    else:
        d.line((cx - 18 * s, cy - 18 * s, cx + 18 * s, cy + 18 * s), fill=WHITE, width=w)
        d.line((cx + 18 * s, cy - 18 * s, cx - 18 * s, cy + 18 * s), fill=WHITE, width=w)

# ---------- framing ----------
def chapter_card(d, t, num, title, col=INK):
    """Full-screen chapter title (scene keys starting with 'ch')."""
    d.rectangle((0, 0, W, H), fill=col)
    a = ease_out(prog(t, 0.05, 0.5))
    text(d, (W / 2, 420 - (1 - a) * 40), f"CHAPTER {num}", 46, fill=YELLOW, w="xbold", alpha=1, stroke=0)
    for j, ln in enumerate(title.split("\n")):
        text(d, (W / 2, 540 + j * 120 + (1 - a) * 60), ln, 110, fill=WHITE)
    d.rectangle((W / 2 - 120 * a, 460, W / 2 + 120 * a, 468), fill=YELLOW)

def year_tag(d, year, a=1.0):
    if a <= 0: return
    f = F(34, "xbold"); s = f"{year}"; tw = d.textlength(s, font=f)
    rrect(d, (50, 40, 50 + tw + 44, 98), 29, INK, ow=0)
    text(d, (72, 70), s, 34, fill=YELLOW, w="xbold", anchor="lm")

def source_tag(d, label, a=1.0):
    if a <= 0 or not label: return
    text(d, (52, 935), "Source: " + label, 24, fill=GREY, w="semi", anchor="lm", max_w=1100)

# ---------- captions (lower third) ----------
CAPTION_SUBS = []
CAPTION_Y = 1000
def _norm(s): return re.sub(r"[^a-z0-9]", "", s.lower())

def apply_subs(words):
    subs = [(_norm(spoken), shown) for spoken, shown in CAPTION_SUBS]
    out, i = [], 0
    while i < len(words):
        for target, shown in subs:
            joined, j = "", i
            while j < len(words) and len(joined) < len(target):
                joined += _norm(words[j][2]); j += 1
            if joined == target:
                out.append((words[i][0], words[j - 1][1], shown)); i = j; break
        else:
            out.append(words[i]); i += 1
    return out

def caption_groups(d, words, max_words=7, max_w=1400, pause=0.28):
    f, groups, cur = F(48, "xbold"), [], []
    for w in apply_subs(words):
        trial = " ".join(x[2] for x in cur + [w])
        if cur and (len(cur) >= max_words or d.textlength(trial, font=f) > max_w or w[0] - cur[-1][1] > pause
                    or cur[-1][2].rstrip()[-1:] in ".?!"):
            groups.append(cur); cur = []
        cur.append(w)
    if cur: groups.append(cur)
    return groups

def captions(d, t, sc):
    if sc.get("nocap"): return
    groups = sc.setdefault("groups", caption_groups(d, sc["words"]))
    for i, grp in enumerate(groups):
        nxt = groups[i + 1][0][0] if i + 1 < len(groups) else sc["dur"]
        if grp[0][0] <= t < min(nxt, grp[-1][1] + 0.6):
            f = F(48, "xbold")
            labels = [g[2] for g in grp]
            widths = [d.textlength(s + " ", font=f) for s in labels]
            x = W / 2 - (sum(widths) - d.textlength(" ", font=f)) / 2
            for (ws, we, _), s, w in zip(grp, labels, widths):
                col = YELLOW if ws <= t < max(we, ws + 0.15) else WHITE
                d.text((x, CAPTION_Y), s, font=f, fill=col, anchor="lm", stroke_width=6, stroke_fill=INK)
                x += w
            return

# ---------- camera ----------
CAMS = {}   # scene key -> (zoom0, zoom1, (fx, fy)) focus point in screen coords; default gentle push to centre
def camera(img, sc, t):
    z0, z1, (fx, fy) = CAMS.get(sc["key"], (1.0, 1.045, (W / 2, H * 0.45)))
    if sc["key"].startswith("ch"): return img
    z = lerp(z0, z1, ease_in_out(t / max(sc["dur"], 0.1)))
    if abs(z - 1) < 1e-3: return img
    cw, ch = W / z, H / z
    x0 = clamp(fx - cw * fx / W, 0, W - cw); y0 = clamp(fy - ch * fy / H, 0, H - ch)
    return img.resize((W, H), Image.BILINEAR, box=(x0, y0, x0 + cw, y0 + ch))

# ---------- frame + run ----------
_BGIMG = None
def background():
    global _BGIMG
    if _BGIMG is None:
        rng = np.random.default_rng(3)
        a = np.ones((H, W, 3), np.float32) * np.array(BG, np.float32)
        a += rng.standard_normal((H, W, 1)).astype(np.float32) * 1.6      # faint paper tooth (static: compresses well)
        _BGIMG = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    return _BGIMG

def frame(T):
    sc = next((s for s in SCENES if s["start"] <= T < s["start"] + s["dur"]), SCENES[-1])
    t = T - sc["start"]
    img = background().copy()
    d = ImageDraw.Draw(img)
    DRAW[sc["key"]](d, t, sc)
    img = camera(img, sc, t)
    d = ImageDraw.Draw(img)
    captions(d, t, sc)
    if T < 0.25 or T > TOTAL - 0.6:   # fade from / to black
        k = clamp(T / 0.25) if T < 0.25 else clamp((TOTAL - T) / 0.6)
        img = Image.blend(Image.new("RGB", (W, H), (0, 0, 0)), img, k)
    return img

def _range():
    keys = [s["key"] for s in SCENES]
    a = ARGS[ARGS.index("--from") + 1] if "--from" in ARGS else keys[0]
    b = ARGS[ARGS.index("--to") + 1] if "--to" in ARGS else keys[-1]
    return BY_KEY[a]["start"], BY_KEY[b]["start"] + BY_KEY[b]["dur"]

def run(draw, subs=(), sfx=(), cams=None, music=True):
    """sfx: [(scene_key, cue, name[, gain[, offset]])] where cue is a spoken word or seconds into the scene."""
    global DRAW
    DRAW = draw
    CAPTION_SUBS[:] = subs
    if cams: CAMS.update(cams)
    missing = [s["key"] for s in SCENES if s["key"] not in DRAW]
    if missing: raise SystemExit(f"no draw function for scenes: {missing}")
    if PREVIEW:
        os.makedirs("preview", exist_ok=True)
        for s in SCENES:
            T = s["start"] + s["dur"] * 0.75
            frame(T).save(f"preview/{s['idx']:03d}_{s['key']}.png")
        print("previews in preview/")
        return
    if "--scan" in ARGS:
        from PIL import Image as _I
        for k in range(int(TOTAL * FPS)):
            T = k / FPS; sc = next((s for s in SCENES if s["start"] <= T < s["start"] + s["dur"]), SCENES[-1])
            DRAW[sc["key"]](ImageDraw.Draw(_I.new("RGB", (W, H))), T - sc["start"], sc)
        print("scan ok"); return

    import audio
    events = []
    for cue in sfx:
        key, when, name, gain, offset = tuple(cue) + (1.0, 0.0)[len(cue) - 3:]
        sc = BY_KEY[key]
        at = wt(sc, when) if isinstance(when, str) else when
        events.append((sc["start"] + at + offset, name, gain))
    voice = []
    for s in SCENES:
        clip = audio.load(f"audio/{s['key']}.mp3")
        clip = clip[int(s["lead"] * audio.SR):int((s["lead"] + s["dur"]) * audio.SR)]
        voice.append((s["start"], clip))
    chapters = [s["start"] for s in SCENES if s["key"].startswith("ch")]
    mixfile = audio.mix(TOTAL, voice, events, music="doc" if music else False, out="mix.wav", sections=chapters)
    if "--audio-only" in ARGS:
        tmp = OUT + ".tmp.mp4"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", OUT, "-i", mixfile, "-map", "0:v", "-map", "1:a",
                        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "-shortest", tmp], check=True)
        os.replace(tmp, OUT); print("re-mixed audio", OUT); return
    t_from, t_to = _range()
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
           "-i", "-", "-ss", f"{t_from:.3f}", "-i", mixfile, "-map", "0:v", "-map", "1:a",
           "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-tune", "animation", "-pix_fmt", "yuv420p",
           "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "-shortest", OUT]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    k0, k1 = int(t_from * FPS), int(t_to * FPS)
    for k in range(k0, k1):
        p.stdin.write(frame(k / FPS).tobytes())
        if (k - k0) % 900 == 0: print(f"frame {k - k0}/{k1 - k0}", flush=True)
    p.stdin.close(); p.wait()
    print("done", OUT, f"{t_to - t_from:.1f}s")

# ---------- thumbnails (1280x720), copying the winning layout ----------
def thumbnail(path, headline, tag="", scene=None, bg=BG, banner=RED):
    """Huge caps headline on a coloured banner (top), small era tag above it, scene(d) draws the art below
    (one reacting character + one money visual). Saves path and a 320x180 phone-size check next to it."""
    TW, TH = 1280, 720
    big = Image.new("RGB", (W, H), bg); d = ImageDraw.Draw(big)
    if scene: scene(d)
    img = big.resize((TW, TH), Image.LANCZOS); d = ImageDraw.Draw(img)
    size = 118; f = F(size)
    while d.textlength(headline, font=f) > TW - 90: size -= 4; f = F(size)
    tw = d.textlength(headline, font=f)
    y0 = 70 if tag else 30
    d.rectangle((40, y0, 40 + tw + 50, y0 + size * 1.12), fill=banner)
    d.text((65, y0 + size * 0.56), headline, font=f, fill=WHITE, anchor="lm", stroke_width=4, stroke_fill=INK)
    if tag:
        ft = F(40, "black"); w2 = d.textlength(tag, font=ft)
        d.rectangle((40, 18, 40 + w2 + 30, 70), fill=INK)
        d.text((55, 44), tag, font=ft, fill=WHITE, anchor="lm")
    img.save(path)
    img.resize((320, 180), Image.LANCZOS).save(path.replace(".png", "_phone.png"))
    return img
