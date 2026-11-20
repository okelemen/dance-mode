"""HT34 kapak siluet adaylari: siluet-havuz.py havuzundan (203) elle secilen kisa liste.
Her aday iki olcumle gelir: son 4 kapak (30-33) IoU ve BUTUN onceki kapak siluetleriyle (05-kapak/kapak-*.py'deki id'lerin
diskteki dosyalari) en yuksek IoU. Baska kaynakta ayni cizimin ikizi (IoU >= 0,90) assert ile durdurur (gozlem 0017).
Elenen ikizler: S1300070~S1300068, D241477~S1220742, D245206~S1289271, S1132027~D255374, S1296472~D222008 (onceki kapaklar);
D268290~S2029430, D333846~S2025657 (aday ici).  Normalize maske 120x160, ayna da olculur.
"""
import glob, os, re
import numpy as np
from PIL import Image, ImageDraw, ImageFont

KOK = os.path.dirname(os.path.abspath(__file__))
REF = r"C:\Users\eleme\OneDrive\Masaüstü\REFERANSLAR"
CIK = r"C:\Users\eleme\OneDrive\Masaüstü\POZ-DUVARI\kapak-taslak\34"
YOL = {"S": "SVGSILH-dans-siluet/png512/%s.png", "D": "OC-dans-siluet/buyuk/%s.png", "K": "OC-dans-siluet/%s-2000.png",
       "Y": "OC-yoga-siluet/%s-2000.png"}


def yol(i):
    return os.path.join(REF, YOL[i[0]] % i[1:])


def maske(i):
    a = np.array(Image.open(yol(i)).convert("RGBA"))[..., 3] > 127
    ys, xs = np.where(a)
    a = a[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    return np.array(Image.fromarray(a.astype(np.uint8) * 255).resize((120, 160))) > 127


def iou(a, b):
    return (a & b).sum() / max((a | b).sum(), 1)


def benz(m, s):
    return max(iou(m, s), iou(m[:, ::-1], s))


SON4 = ("S1043468 S1132025 S1119167 S1289371 S1043462 S1299042 S1824819 S1289271 D331548 S1300068 S2026663 D320699 D314205 "
        "D259886 D255536 S1220742 D259887").split()
# Elenen (kural): S1074932 elinde kilic (nesne), S1254588 kisa tutu (etek).
ADAY = [("S1300393", "kadın, ağaç duruşu"),
        ("S2025657", "kadın, ağaç, kollar yukarı"), ("S2029430", "kadın, ağaç, eğik"), ("D273072", "kadın, sıçrama hamlesi"),
        ("D277856", "kadın, geriye esneme"), ("D340781", "kadın, kollar baş üstü kavis"),
        ("S1399919", "erkek, çömelme (32'de aday, kullanılmadı)")]

if __name__ == "__main__":
    kul = set()
    for f in glob.glob(os.path.join(KOK, "kapak-*.py")):
        kul |= set(re.findall(r"(?<!\d)(\d{6,7})(?!\d)", open(f, encoding="utf-8", errors="ignore").read()))
    ESKI = [on + u for on, pat in YOL.items() for u in sorted(kul) if os.path.exists(os.path.join(REF, pat % u))]
    assert all(s in ESKI for s in SON4), [s for s in SON4 if s not in ESKI]
    sm = {i: maske(i) for i in SON4}
    em = {i: maske(i) for i in ESKI}
    S, HC, C = 250, 330, 5
    n = len(ADAY)
    sayfa = Image.new("RGB", (C * S, ((n + C - 1) // C) * HC), "white")
    dr = ImageDraw.Draw(sayfa)
    f1 = ImageFont.truetype("arialbd.ttf", 22)
    f2 = ImageFont.truetype("arial.ttf", 15)
    with open(os.path.join(CIK, "siluet-aday.txt"), "w", encoding="utf-8") as t:
        for k, (i, ad) in enumerate(ADAY):
            m = maske(i)
            en = max(SON4, key=lambda s: benz(m, sm[s])); v = benz(m, sm[en])
            ek = max(ESKI, key=lambda s: benz(m, em[s])); ev = benz(m, em[ek])
            assert ev < 0.90, (i, ek, ev)
            im = Image.open(yol(i)).convert("RGBA"); im = im.crop(im.getbbox()); im.thumbnail((S - 20, HC - 80))
            bg = Image.new("RGBA", im.size, (215, 232, 250, 255)); bg.alpha_composite(im)
            x, y = (k % C) * S, (k // C) * HC
            sayfa.paste(bg.convert("RGB"), (x + (S - im.width) // 2, y + 34))
            dr.text((x + 8, y + 6), "%d  %s" % (k + 1, i), fill="black", font=f1)
            dr.text((x + 8, y + HC - 40), ad[:34], fill="black", font=f2)
            dr.text((x + 8, y + HC - 22), "son4 %.2f · tüm kapaklar %.2f" % (v, ev), fill="#060", font=f2)
            t.write("%d\t%s\t%s\tson4 %.3f (%s)\ttum kapaklar %.3f (%s)\t%s\n" % (k + 1, i, ad, v, en, ev, ek, yol(i)))
    sayfa.save(os.path.join(CIK, "siluet-aday.jpg"), quality=88)
    print(open(os.path.join(CIK, "siluet-aday.txt"), encoding="utf-8").read())
