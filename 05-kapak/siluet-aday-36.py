"""HT36 kapak siluet adaylari (REF-088 kapagi: TEK dev siyah figur, ucgen yoga pozu, beyaz kontur; arkada panoda ayni poz).
siluet-havuz.py 36 havuzu (181) elle elendi: elbise/etek, nesne, sembol, oturan, yarim govde, havada, dokulu cizim -> 5 CC0.
Havuzda ucgen/hamle gibi uzun ayakta yoga pozu az -> TALIMATLAR §8 (7 Kas: "oncekilerden harmanla") geregi bu videonun onayli
solo duvar maskelerinden 4 aday (M onek, varlik-36s1/poz). Tek figur gosterilir (ayna cifti yok).
"""
import glob, os, re
import numpy as np
from PIL import Image, ImageDraw, ImageFont

KOK = os.path.dirname(os.path.abspath(__file__))
REF = r"C:\Users\eleme\OneDrive\Masaüstü\REFERANSLAR"
CIK = r"C:\Users\eleme\OneDrive\Masaüstü\POZ-DUVARI\kapak-taslak\36"
DUVAR = "C:/Users/eleme/DANCE-MODE/03-motor/tetris-pvp/varlik-36s1/poz/%s.png"
YOL = {"S": "SVGSILH-dans-siluet/png512/%s.png", "D": "OC-dans-siluet/buyuk/%s.png", "K": "OC-dans-siluet/%s-2000.png",
       "Y": "OC-yoga-siluet/%s-2000.png"}


def yol(i):
    return DUVAR % i[1:] if i[0] == "M" else os.path.join(REF, YOL[i[0]] % i[1:])


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
        "D259886 D255536 S1220742 D259887 D273072 S2029430 D277856 S1399919 D340781 S1300393").split()
# kontak 1'de elenen (kural §8): S1191059 mozaik dokulu cizim, S1073747 etek, S1285505 bol pantolon, S1299753 iki kisi
ADAY = [("S1226176", "kadın, eller başın arkasında, ayakta (giysisiz düz hat)"),
        ("Mwerewolf-low-lunge-hip-diag", "video pozu: alçak hamle + çapraz kol (BOSS WALL)"),
        ("Mvampire-lunge-bent-up-diag", "video pozu: hamle + kol yukarı çapraz"),
        ("Mpetal-hip-t-horse", "video pozu: geniş at duruşu + T kol"),
        ("Mdisco-standing-knee-lift-tall-arms", "video pozu: diz kaldırma + kollar dik yukarı (ilk duvar)")]

if __name__ == "__main__":
    kul = set()
    for f in glob.glob(os.path.join(KOK, "kapak-*.py")):
        kul |= set(re.findall(r"(?<!\d)(\d{6,7})(?!\d)", open(f, encoding="utf-8", errors="ignore").read()))
    ESKI = [on + u for on, pat in YOL.items() for u in sorted(kul) if os.path.exists(os.path.join(REF, pat % u))]
    assert all(s in ESKI for s in SON4), [s for s in SON4 if s not in ESKI]
    sm = {i: maske(i) for i in SON4}
    em = {i: maske(i) for i in ESKI}
    S, HC, C = 330, 330, 4
    n = len(ADAY)
    sayfa = Image.new("RGB", (C * S, ((n + C - 1) // C) * HC), "white")
    dr = ImageDraw.Draw(sayfa)
    f1 = ImageFont.truetype("arialbd.ttf", 20)
    f2 = ImageFont.truetype("arial.ttf", 13)
    with open(os.path.join(CIK, "siluet-aday.txt"), "w", encoding="utf-8") as t:
        for k, (i, ad) in enumerate(ADAY):
            im = Image.open(yol(i)).convert("RGBA"); im = im.crop(im.getbbox())
            if i[0] == "M":
                v = ev = 0.0; en = ek = "-"
                cift = im
            else:
                m = maske(i)
                en = max(SON4, key=lambda s: benz(m, sm[s])); v = benz(m, sm[en])
                ek = max(ESKI, key=lambda s: benz(m, em[s])); ev = benz(m, em[ek])
                assert ev < 0.90, (i, ek, ev)
                cift = im
            cift.thumbnail((S - 20, HC - 90))
            bg = Image.new("RGBA", cift.size, (255, 226, 40, 255)); bg.alpha_composite(cift)
            x, y = (k % C) * S, (k // C) * HC
            sayfa.paste(bg.convert("RGB"), (x + (S - cift.width) // 2, y + 34))
            dr.text((x + 8, y + 6), "%d  %s" % (k + 1, i[:30]), fill="black", font=f1)
            dr.text((x + 8, y + HC - 50), ad[:52], fill="black", font=f2)
            if i[0] != "M":
                dr.text((x + 8, y + HC - 30), "son kapaklar %.2f · tüm kapaklar %.2f" % (v, ev), fill="#060", font=f2)
            t.write("%d\t%s\t%s\tson %.3f (%s)\ttum kapaklar %.3f (%s)\t%s\n" % (k + 1, i, ad, v, en, ev, ek, yol(i)))
    sayfa.save(os.path.join(CIK, "siluet-aday.jpg"), quality=88)
    print(open(os.path.join(CIK, "siluet-aday.txt"), encoding="utf-8").read())
