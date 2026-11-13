"""Yazi -> kup izgarasi (marka gorselleri). Yerelde calisir (yalniz veri uretir, render yok).
python harf_voksel.py "CUBECUT" 30 harf-cubecut.json
Cikti: her kup icin (sutun, satir) + kenar bayragi; Blender (marka3b.py) bunlari avokado kuplerine cevirir.
"""
import json
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

yazi, yuk, cikti = sys.argv[1], int(sys.argv[2]), sys.argv[3]
font = ImageFont.truetype("C:/Windows/Fonts/seguibl.ttf", 400)
l, t, r, b = font.getbbox(yazi)
im = Image.new("L", (r - l + 40, b - t + 40), 0)
ImageDraw.Draw(im).text((20 - l, 20 - t), yazi, font=font, fill=255)
oran = yuk / (b - t)
kucuk = im.resize((max(1, int(im.width * oran)), max(1, int(im.height * oran))), Image.LANCZOS)
m = np.asarray(kucuk) > 110
H, W = m.shape
p = np.pad(m, 1)
kenar = m & ~(p[2:, 1:-1] & p[:-2, 1:-1] & p[1:-1, 2:] & p[1:-1, :-2])
ys, xs = np.nonzero(m)
veri = {"yazi": yazi, "en": int(W), "boy": int(H),
        "kupler": [[int(x), int(H - 1 - y), int(kenar[y, x])] for y, x in zip(ys, xs)]}
json.dump(veri, open(cikti, "w"))
print(yazi, W, "x", H, "kup", len(veri["kupler"]))
