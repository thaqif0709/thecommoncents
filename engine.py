"""The Common Cents video engine: 1930s rubber-hose cartoon style (vaudeville stage, cartoon props,
old-film grain/flicker), word-timed captions, 1080x1920 @ 30fps.

Each episode lives in episodes/<name>/ with script.json + audio/<scene>.{mp3,srt} and an episode.py that does
`from engine import *`, defines one draw function per scene, and calls run(DRAW, subs=[...]).
Run it from the episode folder:  python3 episode.py [out.mp4] [--preview]"""
import json, math, os, random, re, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1080, 1920, 30
GAP, TAIL = 0.15, 1.0      # pause between scenes; hold after the last line
OUT = next((a for a in sys.argv[1:] if not a.startswith("--")), "episode.mp4")
PREVIEW = "--preview" in sys.argv  # renders one still per scene instead of video
HANDLE = "@thecommoncents"

# ---------- palette ----------
INK = (30, 22, 18); CREAM = (250, 240, 215); GLOVE = (252, 248, 238); MUTED = (110, 86, 64)
WALL = (206, 180, 140); SPOT = (246, 232, 202)
CURTAIN = (156, 34, 38); CURTAIN_D = (104, 18, 24); GOLD = (226, 174, 62)
FLOOR = (132, 84, 50); FLOOR_D = (92, 56, 32)
FLOOR_Y = 1545
CAPTION_Y = 1000          # captions sit in a clear lane at the screen centre
RED = (182, 52, 44); TEAL = (58, 116, 118); MUSTARD = (226, 172, 62); ORANGE = (214, 112, 46); OLIVE = (118, 136, 62)
PAPER2 = (232, 214, 176)
BUN = (222, 150, 70); BUN_D = (196, 120, 55); PATTY = (104, 58, 36)
COIN = (232, 176, 92); COIN_EDGE = (178, 120, 54); COIN_RIM = (204, 146, 70); SHOE = (196, 136, 70); BLUSH = (226, 128, 92)
SH = 10; OW = 6

_FD = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts")
FONT_FILES = dict(toon=f"{_FD}/LuckiestGuy-Regular.ttf", slab=f"{_FD}/AlfaSlabOne-Regular.ttf",
                  serif=f"{_FD}/DMSerifDisplay-Regular.ttf", sans=f"{_FD}/WorkSans.ttf")
FONTS = {}
def F(size, kind="toon"):
    k = (int(size), kind)
    if k not in FONTS:
        f = ImageFont.truetype(FONT_FILES[kind], int(size))
        if kind == "sans": f.set_variation_by_axes([700])
        FONTS[k] = f
    return FONTS[k]

# ---------- easing ----------
def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def prog(t, start, dur=0.4): return clamp((t - start) / dur)
def ease_out(x): return 1 - (1 - x) ** 3
def ease_back(x, s=1.70158):
    x -= 1
    return x * x * ((s + 1) * x + s) + 1
def lerp(a, b, x): return a + (b - a) * x
def mix(c1, c2, x): return tuple(int(lerp(a, b, clamp(x))) for a, b in zip(c1, c2))

# ---------- timing ----------
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
SCENES, t0 = [], 0.0
for i, (key, _) in enumerate(SCRIPT):
    words = parse_srt(f"audio/{key}.srt")
    lead = max(0.0, words[0][0] - 0.06) if words else 0.0           # trim TTS silence before the first word
    words = [(a - lead, b - lead, w) for a, b, w in words]
    spoken = words[-1][1] + 0.15 if words else duration(f"audio/{key}.mp3")
    d = spoken + (TAIL if i == len(SCRIPT) - 1 else GAP)
    SCENES.append(dict(key=key, start=t0, dur=d, lead=lead, words=words))
    t0 += d
TOTAL = t0

def wt(scene, word, nth=0, default=0.0):
    """Local start time of a spoken word in a scene (case/punct-insensitive)."""
    norm = lambda s: re.sub(r"[^a-z0-9]", "", s.lower())
    hits = [w[0] for w in scene["words"] if norm(w[2]).startswith(norm(word))]
    return hits[nth] if len(hits) > nth else default

# ---------- the stage (built once) ----------
def make_stage():
    ys, xs = np.mgrid[0:H, 0:W].astype(np.float32)
    folds = 1 + 0.05 * np.sin(xs / 46 * np.pi)
    spot = np.clip(1 - (((xs - W / 2) / 640) ** 2 + ((ys - 820) / 860) ** 2), 0, 1) ** 0.6
    wall, lit = np.array(WALL, np.float32), np.array(SPOT, np.float32)
    img = (wall * (1 - spot[..., None]) + lit * spot[..., None]) * folds[..., None]
    floor = ys >= FLOOR_Y
    pool = np.clip(1 - (((xs - W / 2) / 460) ** 2 + ((ys - FLOOR_Y - 65) / 90) ** 2), 0, 1) ** 0.8
    fl = np.array(FLOOR, np.float32) * (1 + 0.35 * pool[..., None])
    img[floor] = fl[floor]
    im = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))
    d = ImageDraw.Draw(im)
    y, gap = FLOOR_Y, 34
    while y < H:                                         # floorboards, widening toward the viewer
        d.line((0, y, W, y), fill=FLOOR_D, width=3)
        off = (y * 7) % 220
        for x in range(-off, W, 220): d.line((x, y, x, y + gap), fill=FLOOR_D, width=2)
        y += gap; gap = int(gap * 1.18)
    d.rectangle((0, FLOOR_Y - 6, W, FLOOR_Y + 4), fill=INK)
    edge = FLOOR_Y + 160                               # stage front, footlights, orchestra pit
    d.rectangle((0, edge, W, H), fill=(34, 22, 18))
    d.rectangle((0, edge, W, edge + 36), fill=CURTAIN_D, outline=INK, width=5)
    for x in range(60, W, 120):
        for r, col in ((46, (120, 88, 50)), (34, (190, 150, 80)), (22, (250, 226, 160))):   # soft glow
            d.ellipse((x - r, edge - r * 0.55, x + r, edge + r * 0.55), fill=col)
        d.chord((x - 26, edge - 26, x + 26, edge + 26), 180, 360, fill=(255, 240, 190), outline=INK, width=4)
        d.rectangle((x - 30, edge, x + 30, edge + 14), fill=GOLD, outline=INK, width=4)
    return im

def make_curtains():
    """Valance + side drapes as an RGBA overlay drawn in front of the artwork."""
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    for side in (0, 1):
        for k in range(5):                                # folds: alternating light/dark strips
            x0 = k * 22; col = CURTAIN if k % 2 == 0 else CURTAIN_D
            pts = [(x0, 0), (x0 + 24, 0), (x0 + 24 - k * 4, FLOOR_Y), (x0 - k * 4, FLOOR_Y)]
            if side: pts = [(W - x, y) for x, y in pts]
            d.polygon(pts, fill=col + (255,))
        xe = 112 if not side else W - 112
        d.line((xe, 0, xe - (16 if not side else -16), FLOOR_Y), fill=INK + (255,), width=6)
    d.rectangle((0, 0, W, 120), fill=CURTAIN + (255,))
    for x in range(0, W, 30): d.line((x, 0, x, 120), fill=CURTAIN_D + (255,), width=8)
    for x in range(-45, W + 90, 90):                      # scalloped edge with gold fringe
        d.pieslice((x, 70, x + 90, 170), 0, 180, fill=CURTAIN + (255,), outline=INK + (255,), width=5)
        d.arc((x + 6, 82, x + 84, 162), 10, 170, fill=GOLD + (255,), width=6)
    d.line((0, 120, W, 120), fill=GOLD + (255,), width=6)
    return ov

STAGE = make_stage()
CURTAINS = make_curtains()

# ---------- old-film finish ----------
ys, xs = np.mgrid[0:H, 0:W].astype(np.float32)
VIGNETTE = (1 - 0.42 * np.clip(((xs - W / 2) / (W * 0.62)) ** 2 + ((ys - H / 2) / (H * 0.6)) ** 2, 0, 1) ** 1.4)[..., None]
_rng = np.random.default_rng(7)
GRAIN = [(_rng.standard_normal((H, W)).astype(np.float32) * 7)[..., None] for _ in range(6)]
del ys, xs

def film(img, k):
    a = np.asarray(img, dtype=np.float32)
    gray = a @ np.array([0.3, 0.59, 0.11], np.float32)
    a = a * 0.84 + (gray[..., None] * np.array([1.08, 0.96, 0.78], np.float32)) * 0.16   # sepia grade
    r = random.Random(k)
    a = a * VIGNETTE * (1 + r.uniform(-0.008, 0.008)) + GRAIN[(k // 2) % len(GRAIN)]
    if r.random() < 0.06: a = np.roll(a, r.choice((-1, 1)), axis=0)    # gate weave
    out = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    d = ImageDraw.Draw(out)
    for _ in range(r.choice((0, 0, 0, 1, 1, 2))):                                                       # dust
        x, y, s = r.uniform(0, W), r.uniform(0, H), r.uniform(1.5, 5)
        d.ellipse((x - s, y - s * r.uniform(0.6, 1.4), x + s, y + s), fill=(25, 18, 14) if r.random() < .7 else (250, 240, 220))
    if r.random() < 0.02:                                                                  # scratch
        x = r.uniform(80, W - 80)
        d.line((x, 0, x + r.uniform(-20, 20), H), fill=(235, 225, 200), width=2)
    return out

# ---------- drawing primitives ----------
def text(d, xy, s, size, fill=CREAM, kind="toon", anchor="mm", stroke=None, shadow=True, alpha=1.0, off=7):
    """Cartoon title text: ink outline + hard ink drop shadow by default (toon font)."""
    if alpha <= 0: return
    f = F(size, kind)
    max_w = 830 if anchor[0] == "m" else 950 - xy[0]          # keep text clear of the curtains
    while size > 20 and f.getlength(s) > max_w:
        size *= 0.94; f = F(size, kind)
    if stroke is None: stroke = max(3, int(size / 14)) if kind == "toon" else 0
    if shadow and kind == "toon":
        d.text((xy[0] + off, xy[1] + off), s, font=f, fill=INK, anchor=anchor, stroke_width=stroke, stroke_fill=INK)
    bg = SPOT
    d.text(xy, s, font=f, fill=mix(bg, fill, alpha), anchor=anchor, stroke_width=stroke, stroke_fill=mix(bg, INK, alpha))

def rrect(d, box, r, fill, sh=SH, ow=OW):
    x0, y0, x1, y1 = box
    r = int(max(0, min(r, (x1 - x0) / 2, (y1 - y0) / 2)))
    if sh: d.rounded_rectangle((x0 + sh, y0 + sh, x1 + sh, y1 + sh), radius=r, fill=INK)
    d.rounded_rectangle(box, radius=r, fill=fill, outline=INK, width=ow)

def ell(d, box, fill, sh=SH, ow=OW):
    x0, y0, x1, y1 = box
    if sh: d.ellipse((x0 + sh, y0 + sh, x1 + sh, y1 + sh), fill=INK)
    d.ellipse(box, fill=fill, outline=INK, width=ow)

def poly(d, pts, fill, sh=SH, ow=OW):
    if sh: d.polygon([(x + sh, y + sh) for x, y in pts], fill=INK)
    d.polygon(pts, fill=fill, outline=INK, width=ow)

def sunburst(d, cx, cy, t, rays=18, R=900, col=PAPER2):
    for k in range(rays):
        a0 = (k / rays) * 2 * math.pi + t * 0.15
        a1 = a0 + math.pi / rays
        d.polygon([(cx, cy), (cx + R * math.cos(a0), cy + R * math.sin(a0)), (cx + R * math.cos(a1), cy + R * math.sin(a1))], fill=col)

def pie_eye(d, ex, ey, w, h, face_col, look=(0, 0), closed=False, lw=4):
    """Classic 1930s 'pie-cut' eye: black oval with a wedge notch."""
    if closed:
        d.arc((ex - w, ey - h * 0.4, ex + w, ey + h * 0.5), 200, 340, fill=INK, width=lw)
        return
    box = (ex - w + look[0], ey - h + look[1], ex + w + look[0], ey + h + look[1])
    d.ellipse(box, fill=INK)
    d.pieslice(box, 285, 325, fill=face_col)

LETTUCE = (128, 168, 62); CHEESE = (244, 192, 58); BUN_HI = (240, 186, 112)

def _superellipse(cx, cy, a, b_top, b_bot, n=2.6, steps=48):
    """Dome-like outline: separate heights above/below the centre line."""
    pts = []
    for i in range(steps):
        th = 2 * math.pi * i / steps
        c, sn = math.cos(th), math.sin(th)
        x = a * math.copysign(abs(c) ** (2 / n), c)
        y = math.copysign(abs(sn) ** (2 / n), sn)
        pts.append((cx + x, cy + y * (b_bot if y > 0 else b_top)))
    return pts

def _capsule(x0, x1, y0, y1, amp=0.0, seed=0.0, steps=26):
    """Rounded slab; amp adds lumpy grilled edges."""
    r = (y1 - y0) / 2; my = (y0 + y1) / 2
    top = [(x, y0 + amp * math.sin(x * 0.045 + seed) * 0.6) for x in
           (x0 + r + (x1 - x0 - 2 * r) * i / steps for i in range(steps + 1))]
    right = [(x1 - r + r * math.cos(th), my + r * math.sin(th)) for th in (-math.pi / 2 + math.pi * i / 8 for i in range(1, 8))]
    bot = [(x, y1 + amp * (0.5 + 0.5 * math.sin(x * 0.06 + seed * 3))) for x, _ in reversed(top)]
    left = [(x0 + r - r * math.cos(th), my - r * math.sin(th)) for th in (-math.pi / 2 + math.pi * i / 8 for i in range(1, 8))]
    return top + right + bot + left

def _burger_parts(face):
    """(polygon, colour) list in burger units, drawn bottom layer first."""
    parts = [(_superellipse(0, 150, 205, 14, 46), BUN_D)]                                   # bottom bun
    parts.append((_capsule(-218, 218, 102, 152, amp=6, seed=1.3), PATTY))                     # patty 2
    parts.append((_capsule(-205, 205, 72, 108), BUN))                                        # middle bun
    parts.append((_capsule(-218, 218, 20, 76, amp=6, seed=0.4), PATTY))                       # patty 1
    def drip(xc, depth, w=18):
        return [(xc + w, 24), (xc + w * 0.8, 24 + depth * 0.7), (xc + w * 0.5, 24 + depth * 0.95), (xc, 24 + depth),
                (xc - w * 0.5, 24 + depth * 0.95), (xc - w * 0.8, 24 + depth * 0.7), (xc - w, 24)]
    cheese = [(-222, 4), (222, 4), (222, 30), (196, 24)] + drip(150, 44) + drip(20, 58) + drip(-115, 38) + [(-196, 24), (-222, 30)]
    parts.append((cheese, CHEESE))
    lett = [(x, -32 + 4 * math.sin(x * 0.08)) for x in range(-226, 227, 10)]
    lett += [(x, 4 + 14 * abs(math.sin((x + 226) / 452 * math.pi * 5.5))) for x in range(226, -227, -8)]
    parts.append((lett, LETTUCE))
    parts.append((_superellipse(0, -36, 218, 196, 20), BUN))                                 # top bun dome
    return parts

def _burger(d, cx, cy, s, mono=None, face=False, t=0.0):
    ow = max(2, int(OW * s))
    T = lambda pts: [(cx + x * s, cy + y * s) for x, y in pts]
    for pts, col in _burger_parts(face):
        if mono: d.polygon(T(pts), fill=mono)
        else: d.polygon(T(pts), fill=col, outline=INK, width=ow)
    if mono: return
    R = lambda x0, y0, x1, y1: (cx + x0 * s, cy + y0 * s, cx + x1 * s, cy + y1 * s)
    d.chord(R(-150, -210, 40, -120), 160, 290, fill=BUN_HI)                                   # shine on the bun
    seeds = [(-150, -110), (-105, -170), (-30, -200), (60, -195), (130, -165), (175, -110), (-185, -60), (190, -55)] if face else \
            [(-120, -150), (-40, -185), (50, -170), (130, -140), (-80, -95), (20, -110), (110, -80), (-150, -85), (160, -60)]
    for sx, sy in seeds:
        d.ellipse(R(sx - 11, sy - 6, sx + 11, sy + 6), fill=CREAM, outline=INK, width=max(1, int(2 * s)))
    if face:
        blink = (t % 4.3) < 0.12
        for sx in (-1, 1):
            pie_eye(d, cx + sx * 50 * s, cy - 120 * s, 19 * s, 32 * s, BUN, closed=blink, lw=max(2, int(6 * s)))
            d.ellipse(R(sx * 108 - 20, -88, sx * 108 + 20, -66), fill=BLUSH)
        d.chord(R(-44, -110, 44, -46), 0, 180, fill=INK)                                      # grin
        d.ellipse(R(-22, -66, 22, -48), fill=RED)
        d.rectangle(R(-30, -78, 30, -70), fill=GLOVE)

def burger(d, cx, cy, s=1.0, shadow=True, face=None, t=0.0):
    if s <= 0.02: return
    face = s >= 0.4 if face is None else face
    if shadow: _burger(d, cx + 14 * s, cy + 14 * s, s, mono=INK)
    _burger(d, cx, cy, s, face=face, t=t)

def pill(d, cx, cy, label, color, a, size=50, txt=CREAM):
    if a <= 0: return
    f = F(size); w = d.textlength(label, font=f)
    y = cy + (1 - ease_out(a)) * 50
    sc = ease_back(a)
    hw, hh = (w / 2 + 34) * sc, size * 0.9 * sc
    rrect(d, (cx - hw, y - hh, cx + hw, y + hh), hh, color, sh=8)
    if a > 0.5: text(d, (cx, y + 4), label, size, fill=txt, shadow=False, stroke=4 if txt == CREAM else 0)

def header(d, num, label, t):
    a = ease_out(prog(t, 0, 0.35))
    x = lerp(-320, 0, a)
    ell(d, (150 + x, 220, 274 + x, 344), MUSTARD, sh=7)
    text(d, (212 + x, 290), str(num), 70, fill=INK, shadow=False, stroke=0)
    text(d, (305 + x, 290), label, 96, anchor="lm", alpha=a)

def bolt(d, cx, cy, s, fill):
    pts = [(10, -60), (-30, 8), (0, 8), (-10, 60), (30, -8), (0, -8)]
    poly(d, [(cx + x * s, cy + y * s) for x, y in pts], fill, sh=0, ow=4)

def building(d, x, base, w, h, color, a):
    hh = h * ease_out(a)
    if hh < 12: return
    rrect(d, (x, base - hh, x + w, base), 6, color)
    for r in range(int((hh - 30) // 70)):
        for c in range(int((w - 30) // 60)):
            wx = x + 30 + c * 60; wy = base - 70 - r * 70
            d.rectangle((wx, wy, wx + 30, wy + 38), fill=MUSTARD, outline=INK, width=3)

# ---------- captions ----------
CAPTION_SUBS = []   # [("one ringgit ninety-nine", "RM1.99"), ...] set via run(subs=...)

def _norm(s): return re.sub(r"[^a-z0-9]", "", s.lower())

def apply_subs(words):
    """Merge spoken word runs into their written form for captions (timings span the merged words)."""
    subs = [(_norm(spoken), shown) for spoken, shown in CAPTION_SUBS]
    out, i = [], 0
    while i < len(words):
        for target, shown in subs:
            joined, j = "", i
            while j < len(words) and len(joined) < len(target):   # compare letters, ignoring token boundaries
                joined += _norm(words[j][2]); j += 1
            if joined == target:
                out.append((words[i][0], words[j - 1][1], shown)); i = j; break
        else:
            out.append(words[i]); i += 1
    return out

def caption_groups(d, words, max_words=3, max_w=860, pause=0.22):
    """Split words into short caption lines: break on max words, max width, or a spoken pause."""
    f, groups, cur = F(76), [], []
    for w in apply_subs(words):
        trial = " ".join(x[2].upper() for x in cur + [w])
        if cur and (len(cur) >= max_words or d.textlength(trial, font=f) > max_w or w[0] - cur[-1][1] > pause):
            groups.append(cur); cur = []
        cur.append(w)
    if cur: groups.append(cur)
    return groups

def captions(d, t, sc):
    groups = sc.setdefault("groups", caption_groups(d, sc["words"]))
    for i, grp in enumerate(groups):
        nxt = groups[i + 1][0][0] if i + 1 < len(groups) else sc["dur"]
        if grp[0][0] <= t < nxt:
            f = F(76)
            labels = [g[2].upper() for g in grp]
            widths = [d.textlength(s + " ", font=f) for s in labels]
            x = W / 2 - sum(widths) / 2; y = CAPTION_Y
            for (ws, we, _), s, w in zip(grp, labels, widths):
                col = MUSTARD if ws <= t < max(we, ws + 0.15) else CREAM
                d.text((x + 6, y + 6), s, font=f, fill=INK, anchor="lm", stroke_width=6, stroke_fill=INK)
                d.text((x, y), s, font=f, fill=col, anchor="lm", stroke_width=6, stroke_fill=INK)
                x += w
            return

def chrome(d, T):
    p = T / TOTAL
    if p > 0.005: d.rectangle((0, 0, W * p, 12), fill=GOLD)
    d.text((W / 2, FLOOR_Y + 280), HANDLE, font=F(40, "serif"), fill=PAPER2, anchor="mm")

def frame(T, k):
    sc = next((s for s in SCENES if s["start"] <= T < s["start"] + s["dur"]), SCENES[-1])
    t = T - sc["start"]
    img = STAGE.copy()
    d = ImageDraw.Draw(img)
    DRAW[sc["key"]](d, t, sc)
    img.paste(CURTAINS, (0, 0), CURTAINS)
    captions(d, t, sc)
    chrome(d, T)
    return film(img, k)

def run(draw, subs=(), sfx=(), music=True):
    """sfx: [(scene_key, cue, name[, gain[, offset]])] where cue is a spoken word or seconds into the scene."""
    global DRAW
    DRAW = draw
    CAPTION_SUBS[:] = subs
    if PREVIEW:
        for s in SCENES:
            T = s["start"] + s["dur"] * 0.8
            frame(T, int(T * FPS)).save(f"preview_{s['key']}.png")
        return

    import audio
    by_key = {s["key"]: s for s in SCENES}
    events = []
    for cue in sfx:
        key, when, name, gain, offset = tuple(cue) + (1.0, 0.0)[len(cue) - 3:]
        sc = by_key[key]
        at = wt(sc, when, default=0.0) if isinstance(when, str) else when
        events.append((sc["start"] + at + offset, name, gain))
    voice = []
    for s in SCENES:
        clip = audio.load(f"audio/{s['key']}.mp3")
        clip = clip[int(s["lead"] * audio.SR):int((s["lead"] + s["dur"]) * audio.SR)]
        voice.append((s["start"], clip))
    mixfile = audio.mix(TOTAL, voice, events, music=music, out="mix.wav")
    if "--audio-only" in sys.argv:                 # re-mix sound onto an already-rendered video, keep the picture
        tmp = OUT + ".tmp.mp4"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", OUT, "-i", mixfile, "-map", "0:v", "-map", "1:a",
                        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "-shortest", tmp], check=True)
        os.replace(tmp, OUT)
        print("re-mixed audio", OUT)
        return

    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
           "-i", "-", "-i", mixfile, "-map", "0:v", "-map", "1:a",
           "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
           "-movflags", "+faststart", "-shortest", OUT]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    n = int(TOTAL * FPS)
    for k in range(n):
        p.stdin.write(frame(k / FPS, k).tobytes())
        if k % 300 == 0: print(f"frame {k}/{n}", flush=True)
    p.stdin.close(); p.wait()
    print("done", OUT, f"{TOTAL:.1f}s")
