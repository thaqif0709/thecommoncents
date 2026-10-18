"""Rebrand (18 Oct 2026): channel logo + banner in the doodle-explainer style. Run: python3 brand.py"""
import os, sys, math, json
HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir("/tmp"); open("script.json", "w").write("[]")          # doodle.py loads a script on import
sys.path.insert(0, HERE)
import doodle as D
from PIL import Image, ImageDraw
os.chdir(HERE)

def logo(size=1024):
    im = Image.new("RGB", (size, size), D.YELLOW); d = ImageDraw.Draw(im)
    s = size / 1024
    D.coin(d, 640 * s, 600 * s, 250 * s, label="", col=D.GOLD)
    D.text(d, (640 * s, 606 * s), "¢", 330 * s, fill=D.INK)
    # the stick-figure mascot peeking in from the left, holding the coin
    D.stick(d, 330 * s, 1130 * s, 2.6 * s, pose="hold", mood="happy", t=1.0, look=0.6)
    return im

def banner():
    BW, BH = 2560, 1440
    im = Image.new("RGB", (BW, BH), D.BG); d = ImageDraw.Draw(im)
    d.rectangle((0, 980, BW, BH), fill=D.BG2); d.line((0, 980, BW, 980), fill=D.INK, width=6)
    # safe area 1546x423 centred (507..2053, 508..931)
    D.text(d, (BW / 2, 640), "THE COMMON CENTS", 150, fill=D.INK, max_w=1500)
    D.marker(d, (BW / 2, 800), "the money stories behind history", 64, a=1, w="xbold")
    D.stick(d, 420, 980, 1.4, pose="wave", mood="happy", t=0.4, shirt=D.BLUE)
    D.press(d, 2150, 980, 0.8, t=0.3)
    D.cash_pile(d, 760, 980, 6, 0.7)
    D.gold_bar(d, 1820, 980, 0.8)
    D.coin(d, 1950, 900, 50)
    return im

if __name__ == "__main__":
    for n in (1024, 800):
        logo(1024).resize((n, n), Image.LANCZOS).save(f"logo_thecommoncents_{n}.png")
    banner().save("banner_youtube_2560x1440.png")
    print("saved")
