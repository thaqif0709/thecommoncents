"""YouTube channel banner (2560x1440). Everything important sits in the 1546x423 centre safe area
that shows on every device; curtains, floor and extra props fill the rest for TV/desktop."""
import math, os, sys
import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(os.path.join(HERE, "episodes", "01-bigmac"))      # engine loads an episode script on import
sys.argv = ["banner", "--preview"]
sys.path.insert(0, HERE)
import engine
from props import burger, pump, coin, car, note_stack, ell
os.chdir(HERE)

BW, BH = 2560, 1440
SAFE = (507, 508, 2053, 931)                                  # x0, y0, x1, y1
INK, CREAM, MUSTARD, MUTED = engine.INK, engine.CREAM, engine.MUSTARD, engine.MUTED
CURTAIN, CURTAIN_D, GOLD = engine.CURTAIN, engine.CURTAIN_D, engine.GOLD

# backdrop: wall with folds + spotlight, floorboards
ys, xs = np.mgrid[0:BH, 0:BW].astype(np.float32)
folds = 1 + 0.05 * np.sin(xs / 46 * np.pi)
spot = np.clip(1 - (((xs - BW / 2) / 1200) ** 2 + ((ys - 720) / 520) ** 2), 0, 1) ** 0.6
wall, lit = np.array(engine.WALL, np.float32), np.array(engine.SPOT, np.float32)
img = (wall * (1 - spot[..., None]) + lit * spot[..., None]) * folds[..., None]
FLOOR = 1010
fl = np.array(engine.FLOOR, np.float32) * (1 + 0.3 * np.clip(1 - (((xs - BW / 2) / 900) ** 2 + ((ys - 1060) / 90) ** 2), 0, 1)[..., None])
img[ys >= FLOOR] = fl[ys >= FLOOR]
im = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))
d = ImageDraw.Draw(im)
y, gap = FLOOR, 40
while y < BH:
    d.line((0, y, BW, y), fill=engine.FLOOR_D, width=3)
    for x in range(-((y * 7) % 260), BW, 260): d.line((x, y, x, y + gap), fill=engine.FLOOR_D, width=2)
    y += gap; gap = int(gap * 1.18)
d.rectangle((0, FLOOR - 6, BW, FLOOR + 4), fill=INK)

# props on stage (inside the safe band)
burger(d, 650, 745, 0.58, face=True, t=0.5)
pump(d, 1890, 990, 0.78, face="happy", t=0.5)
note_stack(d, 2050, 990, 7, w=150)
coin(d, 450, 945, 46)
coin(d, 2190, 870, 40)

# title block
def title(xy, s, size, fill, off=12):
    f = engine.F(size)
    stroke = max(4, size // 14)
    d.text((xy[0] + off, xy[1] + off), s, font=f, fill=INK, anchor="mm", stroke_width=stroke, stroke_fill=INK)
    d.text(xy, s, font=f, fill=fill, anchor="mm", stroke_width=stroke, stroke_fill=INK)
title((BW / 2, 625), "THE COMMON", 150, CREAM)
title((BW / 2, 770), "CENTS", 190, MUSTARD, off=14)
d.text((BW / 2, 885), "money, explained · new videos every week", font=engine.F(52, "serif"), fill=INK, anchor="mm")

# curtains: side drapes + scalloped valance
for side in (0, 1):
    for k in range(9):
        x0 = k * 34; col = CURTAIN if k % 2 == 0 else CURTAIN_D
        pts = [(x0, 0), (x0 + 36, 0), (x0 + 36 - k * 6, FLOOR), (x0 - k * 6, FLOOR)]
        if side: pts = [(BW - x, yy) for x, yy in pts]
        d.polygon(pts, fill=col)
    xe = 300 if not side else BW - 300
    d.line((xe, 0, xe - (50 if not side else -50), FLOOR), fill=INK, width=8)
d.rectangle((0, 0, BW, 300), fill=CURTAIN)
for x in range(0, BW, 40): d.line((x, 0, x, 300), fill=CURTAIN_D, width=12)
for x in range(-60, BW + 120, 120):
    d.pieslice((x, 240, x + 120, 360), 0, 180, fill=CURTAIN, outline=INK, width=6)
    d.arc((x + 8, 254, x + 112, 346), 10, 170, fill=GOLD, width=8)
d.line((0, 300, BW, 300), fill=GOLD, width=8)

# light old-film finish
a = np.asarray(im, dtype=np.float32)
vig = 1 - 0.35 * np.clip(((xs - BW / 2) / (BW * 0.62)) ** 2 + ((ys - BH / 2) / (BH * 0.62)) ** 2, 0, 1) ** 1.4
a = a * vig[..., None] + np.random.default_rng(5).standard_normal((BH, BW, 1)).astype(np.float32) * 5
out = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
out.save("banner_youtube_2560x1440.png")

# preview: full banner with the phone/desktop safe area outlined
p = out.copy(); pd = ImageDraw.Draw(p)
pd.rectangle(SAFE, outline=(0, 200, 255), width=6)
p.resize((1280, 720)).save("banner_preview.png")
out.crop(SAFE).resize((1159, 317)).save("banner_safe_area.png")
print("saved")
