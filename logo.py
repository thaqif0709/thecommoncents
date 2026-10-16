"""The Common Cents profile picture: 1930s-cartoon gold coin with a cent sign and arched lettering."""
import math, random
import numpy as np
from PIL import Image, ImageDraw, ImageFont

S = 1024; C = S / 2
INK = (30, 22, 18); CREAM = (250, 240, 215)
CURTAIN = (156, 34, 38); CURTAIN_D = (104, 18, 24); GOLD = (226, 174, 62)
COIN = (232, 176, 92); COIN_EDGE = (178, 120, 54); COIN_RIM = (204, 146, 70)
TOON = "fonts/LuckiestGuy-Regular.ttf"

img = Image.new("RGB", (S, S), CURTAIN)
d = ImageDraw.Draw(img)
for x in range(0, S, 64):                                         # curtain folds behind the coin
    d.rectangle((x + 32, 0, x + 64, S), fill=CURTAIN_D)

def circle(r, **kw):
    d.ellipse((C - r, C - r, C + r, C + r), **kw)

d.ellipse((C - 452 + 16, C - 452 + 16, C + 452 + 16, C + 452 + 16), fill=INK)     # hard drop shadow
circle(452, fill=COIN_EDGE, outline=INK, width=14)
for k in range(120):                                              # milled edge
    a = 2 * math.pi * k / 120
    d.line((C + 432 * math.cos(a), C + 432 * math.sin(a), C + 446 * math.cos(a), C + 446 * math.sin(a)), fill=INK, width=4)
circle(424, fill=COIN_EDGE, outline=INK, width=8)
circle(318, fill=COIN, outline=INK, width=12)
circle(296, outline=COIN_RIM, width=8)
d.arc((C - 270, C - 270, C + 270, C + 270), 200, 250, fill=CREAM, width=14)        # shine

def arched(text, radius, size, top=True):
    f = ImageFont.truetype(TOON, size)
    widths = [f.getlength(ch) * 1.08 for ch in text]
    total = sum(widths) / radius
    cum = 0.0
    for ch, w in zip(text, widths):
        if top: a = -math.pi / 2 - total / 2 + (cum + w / 2) / radius
        else:   a = math.pi / 2 + total / 2 - (cum + w / 2) / radius
        cum += w
        if ch == " ": continue
        g = Image.new("RGBA", (size * 2, size * 2), (0, 0, 0, 0))
        gd = ImageDraw.Draw(g)
        gd.text((size + 6, size + 6), ch, font=f, fill=INK, anchor="mm", stroke_width=7, stroke_fill=INK)
        gd.text((size, size), ch, font=f, fill=CREAM, anchor="mm", stroke_width=7, stroke_fill=INK)
        rot = -(math.degrees(a) + 90) if top else -(math.degrees(a) - 90)
        g = g.rotate(rot, resample=Image.BICUBIC)
        x, y = C + radius * math.cos(a), C + radius * math.sin(a)
        img.paste(g, (int(x - size), int(y - size)), g)

arched("THE COMMON", 372, 86, top=True)
arched("CENTS", 372, 86, top=False)
for sx in (-1, 1):                                                # star separators
    cx, cy = C + sx * 372, C
    pts = [(cx + (22 if i % 2 == 0 else 9) * math.cos(-math.pi / 2 + i * math.pi / 5),
            cy + (22 if i % 2 == 0 else 9) * math.sin(-math.pi / 2 + i * math.pi / 5)) for i in range(10)]
    d.polygon(pts, fill=GOLD, outline=INK, width=4)

f = ImageFont.truetype(TOON, 470)                                 # the big cent sign
for off, col in ((16, INK), (0, CREAM)):
    d.text((C + off - 4, C + 40 + off), "¢", font=f, fill=col, anchor="mm", stroke_width=16, stroke_fill=INK)

# light old-film finish
a = np.asarray(img, dtype=np.float32)
ys, xs = np.mgrid[0:S, 0:S].astype(np.float32)
vig = 1 - 0.28 * np.clip(((xs - C) / (S * 0.6)) ** 2 + ((ys - C) / (S * 0.6)) ** 2, 0, 1)
a = a * vig[..., None] + np.random.default_rng(3).standard_normal((S, S, 1)).astype(np.float32) * 5
img = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))

img.save("logo_thecommoncents_1024.png")
img.resize((800, 800), Image.LANCZOS).save("logo_thecommoncents_800.png")

# preview: how it looks cropped to a circle at a few sizes
prev = Image.new("RGB", (1000, 420), (24, 24, 24))
for i, sz in enumerate((360, 160, 64)):
    im = img.resize((sz, sz), Image.LANCZOS)
    m = Image.new("L", (sz, sz), 0); ImageDraw.Draw(m).ellipse((0, 0, sz - 1, sz - 1), fill=255)
    prev.paste(im, (30 + [0, 420, 640][i], (420 - sz) // 2), m)
prev.save("logo_preview.png")
