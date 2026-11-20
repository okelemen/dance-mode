"""HT35 kapak siluet adaylari (REF-087 kapagi: AYNI figur + aynasi, ic eller yukarida birlesik, genis comelme).
siluet-havuz.py 35 havuzu (188) elle elendi: elbise/etek, nesne, sembol, oturan, yarim govde, havada, dokulu cizim cikti -> 7 CC0.
Havuzda REF-087 gibi genis comelme + el ele figur yok -> TALIMATLAR §8 (7 Kas: "oncekilerden harmanla") geregi bu videonun onayli
es poz duvar maskelerinden 4 aday (M onek, varlik-35-duvar). Her CC0 aday kontakta kendi aynasiyla CIFT olarak gosterilir.
"""
import glob, os, re
import numpy as np
from PIL import Image, ImageDraw, ImageFont

KOK = os.path.dirname(os.path.abspath(__file__))
REF = r"C:\Users\eleme\OneDrive\Masaüstü\REFERANSLAR"
CIK = r"C:\Users\eleme\OneDrive\Masaüstü\POZ-DUVARI\kapak-taslak\35"
DUVAR = "C:/Users/eleme/DANCE-MODE/03-motor/tetris-pvp/varlik-35-duvar/%s.png"
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
# Elenen (kural): S1074932 elinde kilic (nesne), S1254588 kisa tutu (etek).
ADAY = [("S1427077", "erkek, T kollar, ayakta"), ("D271554", "kadın, kollar dik yukarı"), ("S1055879", "kadın, tek kol yukarı"),
        # kontakta elenen: S1201162 elinde bicak (nesne), S1937345 fantastik iskelet + yaratik, S1615089 tutu (etek)   # D245082 elendi: 34 kapagindaki S1300393 ikizi (IoU 0,99)
        ("Mduo-wide-squat-inner-high-five", "video eş pozu: geniş çömelme + iç eller yukarıda (REF-087'ye en yakın)"),
        ("Mduo-wide-squat-crossed-diagonal", "video eş pozu: geniş çömelme + çapraz kollar"),
        ("Mduo-outer-tree-joined-palms", "video eş pozu: dış diz kalkık + avuçlar yukarıda"),
        ("Mduo-heart-arch-hands-on-hips", "video eş pozu: kalp kemeri + eller belde")]

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
                cift = Image.new("RGBA", (im.width * 2 - im.width // 10, im.height), (0, 0, 0, 0))
                cift.alpha_composite(im, (0, 0)); cift.alpha_composite(im.transpose(Image.FLIP_LEFT_RIGHT), (im.width - im.width // 10, 0))
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
