"""CubeCut banner: eglenceli abone etiketi + profil + kanal onizlemesi.
python marka2.py <MARKA klasoru> <ham klasor adi>
"""
import math
import os
import sys

from PIL import Image, ImageDraw, ImageFilter, ImageFont

K, HAMAD = sys.argv[1], sys.argv[2]
HAM = os.path.join(K, HAMAD)
F_B = "C:/Windows/Fonts/seguibl.ttf"
F_S = "C:/Windows/Fonts/seguisb.ttf"


def lum(c):
    c = [v / 255 for v in c]
    c = [v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4 for v in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def kon(a, b):
    la, lb = sorted([lum(a), lum(b)], reverse=True)
    return (la + 0.05) / (lb + 0.05)


im = Image.open(os.path.join(HAM, "banner-banner.png")).convert("RGBA")
kat = Image.new("RGBA", im.size, (0, 0, 0, 0))
d = ImageDraw.Draw(kat)
# golge + egik kirmizi SUBSCRIBE etiketi
KIRMIZI, BEYAZ, SARI, KOYU = (226, 35, 26), (255, 255, 255), (255, 214, 64), (35, 30, 25)
etiket = Image.new("RGBA", (560, 300), (0, 0, 0, 0))
de = ImageDraw.Draw(etiket)
de.rounded_rectangle([10, 60, 550, 190], radius=65, fill=KIRMIZI, outline=BEYAZ, width=8)
de.text((280, 125), "SUBSCRIBE", font=ImageFont.truetype(F_B, 84), fill=BEYAZ, anchor="mm")
de.rounded_rectangle([60, 205, 500, 280], radius=37, fill=SARI, outline=KOYU, width=5)
de.text((280, 242), "before you get cubed!", font=ImageFont.truetype(F_B, 40), fill=KOYU, anchor="mm")
etiket = etiket.rotate(6, resample=Image.BICUBIC, expand=True)
etiket = etiket.resize((int(etiket.width * 0.56), int(etiket.height * 0.56)), Image.LANCZOS)
golge = Image.new("RGBA", etiket.size, (0, 0, 0, 0))
golge.putalpha(etiket.split()[3].point(lambda a: int(a * 0.35)))
golge = golge.filter(ImageFilter.GaussianBlur(10))
x, y = 1712, 600
kat.alpha_composite(golge, (x + 10, y + 14))
kat.alpha_composite(etiket, (x, y))
im = Image.alpha_composite(im, kat).convert("RGB")
im.save(os.path.join(K, "banner-CubeCut.jpg"), quality=95)
print("etiket kontrast: SUBSCRIBE", round(kon(BEYAZ, KIRMIZI), 1), "alt", round(kon(KOYU, SARI), 1))

pr = Image.open(os.path.join(HAM, "profil-profil.png")).convert("RGB").resize((800, 800), Image.LANCZOS)
pr.save(os.path.join(K, "profil-CubeCut.png"))


def daire(p, r):
    m = Image.new("L", (r, r), 0)
    ImageDraw.Draw(m).ellipse([0, 0, r - 1, r - 1], fill=255)
    o = Image.new("RGBA", (r, r))
    o.paste(p.resize((r, r)), (0, 0), m)
    return o


s = Image.new("RGB", (1620, 760), (255, 255, 255))
ds = ImageDraw.Draw(s)
fk = ImageFont.truetype(F_S, 28)
ds.text((10, 8), "Masaustu / TV (tam banner)", font=fk, fill=(60, 60, 60))
s.paste(im.resize((960, 540)), (10, 44))
ds.text((990, 8), "Mobil (orta serit) + profil", font=fk, fill=(60, 60, 60))
s.paste(im.crop((507, 508, 2053, 931)).resize((620, 170)), (990, 44))
av = daire(pr, 200)
s.paste(av, (995, 250), av)
ds.text((1215, 300), "CubeCut", font=ImageFont.truetype(F_B, 64), fill=(20, 20, 20))
ds.text((1218, 382), "@cubecut", font=fk, fill=(100, 100, 100))
s.save(os.path.join(K, "ONIZLEME-CubeCut.jpg"), quality=88)
print("tamam")
