"""CubeCut 3D marka gorselleri: banner yazisi + profil kirpma + kanal onizlemesi.
python marka.py <MARKA klasoru>   (ham/ altindaki Actions renderlarini kullanir)
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFilter, ImageFont

K = sys.argv[1]
HAM = os.path.join(K, "ham")
F_BAS = ImageFont.truetype("C:/Windows/Fonts/seguibl.ttf", 124)
F_ALT = ImageFont.truetype("C:/Windows/Fonts/seguisb.ttf", 66)
KOYU = (24, 46, 22)
KREM = (246, 241, 222)


def lum(c):
    c = [v / 255 for v in c]
    c = [v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4 for v in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def kontrast(a, b):
    la, lb = sorted([lum(a), lum(b)], reverse=True)
    return (la + 0.05) / (lb + 0.05)


def banner(ham, cikti):
    im = Image.open(os.path.join(HAM, ham)).convert("RGB")
    # yazi plakasi: guvenli alan (orta 1546x423 -> x 507..2053, y 508..931) sag yarisi
    plaka = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(plaka)
    x0, y0, x1, y1 = 1300, 530, 2040, 915
    d.rounded_rectangle([x0, y0, x1, y1], radius=40, fill=KREM + (228,))
    im = Image.alpha_composite(im.convert("RGBA"), plaka.filter(ImageFilter.GaussianBlur(1))).convert("RGB")
    d = ImageDraw.Draw(im)
    cx = (x0 + x1) // 2
    d.text((cx, 650), "CubeCut 3D", font=F_BAS, fill=KOYU, anchor="mm")
    d.text((cx, 790), "1 cut \u2192 1,000 cuts", font=F_ALT, fill=(86, 60, 34), anchor="mm")
    d.text((cx, 870), "2 new videos every day", font=F_ALT, fill=(86, 60, 34), anchor="mm")
    im.save(os.path.join(K, cikti), quality=95)
    print(cikti, "kontrast baslik", round(kontrast(KOYU, KREM), 1), "alt", round(kontrast((86, 60, 34), KREM), 1))
    return im


def profil(ham, cikti):
    im = Image.open(os.path.join(HAM, ham)).convert("RGB").resize((800, 800), Image.LANCZOS)
    im.save(os.path.join(K, cikti), quality=95)
    return im


ba = banner("banner-a2-kare_0649.png", "banner-A-yarim-kesik.jpg")
bb = banner("banner-c2-kare_0418.png", "banner-B-kup-yigini.jpg")
bc = banner("banner-b2-kare_1786.png", "banner-C-1000-kesim.jpg")
pa = profil("profil-a-kare_0142.png", "profil-A-iri-kupler.png")
pb = profil("profil-b-kare_0418.png", "profil-B-kup-yigini.png")


def daire(p, r):
    m = Image.new("L", (r, r), 0)
    ImageDraw.Draw(m).ellipse([0, 0, r - 1, r - 1], fill=255)
    out = Image.new("RGBA", (r, r))
    out.paste(p.resize((r, r)), (0, 0), m)
    return out


# kanal onizlemesi: masaustu (tam banner) + mobil (guvenli alan kirpma) + yuvarlak profil
W = 1600
sayfa = Image.new("RGB", (W, 1640), (255, 255, 255))
d = ImageDraw.Draw(sayfa)
F_K = ImageFont.truetype("C:/Windows/Fonts/seguisb.ttf", 30)
y = 10
for ad, b, p in (("A", ba, pa), ("B", bb, pb), ("C", bc, pa)):
    d.text((10, y), f"Banner {ad}  (ust: masaustu/TV tam, alt: mobil guvenli alan)", font=F_K, fill=(40, 40, 40))
    sayfa.paste(b.resize((800, 450)), (10, y + 40))
    mobil = b.crop((507, 508, 2053, 931)).resize((780, 213))
    sayfa.paste(mobil, (820, y + 40))
    av = daire(p, 160)
    sayfa.paste(av, (830, y + 280), av)
    d.text((1010, y + 330), "CubeCut 3D", font=ImageFont.truetype("C:/Windows/Fonts/seguibl.ttf", 54), fill=(20, 20, 20))
    d.text((1010, y + 395), "@cubecut3d", font=F_K, fill=(90, 90, 90))
    y += 540
sayfa.save(os.path.join(K, "ONIZLEME-kanal.jpg"), quality=88)
print("onizleme yazildi")
