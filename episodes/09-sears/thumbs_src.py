# Thumbnail options -> thumbs/optionN.png (python3 thumbs_src.py). Pick one as thumbs/main.jpg.
import os, sys
sys.argv = [sys.argv[0], "--scan"]                       # doodle parses argv on import; don't render
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
from doodle import *
from PIL import ImageFilter

def bg(key, blur_box=None):
    def f(d):
        im = Image.open(f"images/{key}.jpg").convert("RGB")
        if blur_box:                                     # soften stray AI lettering
            x0, y0, x1, y1 = blur_box; reg = im.crop(blur_box)
            m = Image.new("L", reg.size, 0); ImageDraw.Draw(m).ellipse((0, 0, x1 - x0, y1 - y0), fill=255)
            im.paste(Image.composite(reg.filter(ImageFilter.GaussianBlur(9)), reg, m.filter(ImageFilter.GaussianBlur(10))), blur_box[:2])
        d._image.paste(im)
    return f

os.makedirs("thumbs", exist_ok=True)
thumbnail("thumbs/option1.png", "SEARS WAS AMAZON FIRST", "1886 – 2018", bg("thumb_ruin"))
thumbnail("thumbs/option2.png", "IT SHUT DOWN IN 1993", "SEARS VS AMAZON", bg("catalog_closed"))
thumbnail("thumbs/option3.png", "AMAZON... IN 1905?", "THE SEARS CATALOG", bg("farm_catalog"))
