"""HT42 kapak siluet adaylari (REF-094: IKI dev siyah figur, sol alcak hamle + sag hamle kol yukari, beyaz kontur).
TALIMATLAR §8 harmanlama (37 gibi): bu videonun onayli duvar maskeleri (M onek, varlik-42s1/poz), hamle / genis pozlar.
Asagisi 37nin aciklamasi.
HT37 kapak siluet adaylari (REF-089: IKI dev siyah figur, hamle pozlari, beyaz kontur). Asagisi 36nin aciklamasi.
HT36 kapak siluet adaylari (REF-088 kapagi: TEK dev siyah figur, ucgen yoga pozu, beyaz kontur; arkada panoda ayni poz).
siluet-havuz.py 36 havuzu (181) elle elendi: elbise/etek, nesne, sembol, oturan, yarim govde, havada, dokulu cizim -> 5 CC0.
Havuzda ucgen/hamle gibi uzun ayakta yoga pozu az -> TALIMATLAR §8 (7 Kas: "oncekilerden harmanla") geregi bu videonun onayli
solo duvar maskelerinden 4 aday (M onek, varlik-36s1/poz). Tek figur gosterilir (ayna cifti yok).
"""
import glob, os, re
import numpy as np
from PIL import Image, ImageDraw, ImageFont

KOK = os.path.dirname(os.path.abspath(__file__))
REF = r"C:\Users\eleme\OneDrive\Masaüstü\REFERANSLAR"
CIK = os.path.join(KOK, "kapak-taslak", "42")
DUVAR = "C:/Users/eleme/DANCE-MODE/03-motor/tetris-pvp/varlik-42s1/poz/%s.png"
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
# 37: havuz (176) elle elendi: REF-089 gibi giysisiz ayakta HAMLE pozu yok (S1443648 okcu = nesne, S2037797 havada, S1300135 cizgi karakter,
# S1299125 genis durus ama kollar govdede) -> TALIMATLAR §8 harmanlama: bu videonun onayli maskeleri (M onek, varlik-42s1/poz)
ADAY = [("Mgroove-w-low-lunge", "24 BOSS P2: alçak hamle + W kollar (REF sol figür gibi)"),
        ("Mphantom-t-t-kick-lean-l", "24 BOSS P1: T kollar + yana tekme"),
        ("Mneon-v-goal-lunge", "17 FINAL P1: hamle + V kollar"),
        ("Mcandle-wide-lunge-salute-low", "17 FINAL P2: geniş hamle + selam"),
        ("Mblaze-hip-head-lunge", "18 FINAL P1: hamle + el başta"),
        ("Msakura-deep-side-lunge-arm-over", "18 FINAL P2: derin yan hamle + kol üstten (REF sağ gibi)"),
        ("Mblossom-wave-t-goddess", "16 FREEZE P2: tanrıça duruşu + T kollar"),
        ("Mtundra-cactus-v-goddess", "14 FREEZE P2: tanrıça duruşu + kaktüs/V kollar"),
        ("Mribbon-low-comet-wide", "13 FREEZE P1: tek kol dik yukarı (REF sağ figürün kolu)"),
        ("Mstep-diag-cactus-wide", "15 FREEZE P2: geniş duruş + çapraz/kaktüs kollar"),
        ("Mmeteor-eagle-diag-horse", "16 FREEZE P1: at duruşu + çapraz kollar"),
        ("Mshine-halo-t-tree", "12 R2 P1: ağaç duruşu + hale/T kollar")]

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
            dr.text((x + 8, y + 6), "%d  %s" % (k + 1, i[:27]), fill="black", font=f1)
            dr.text((x + 8, y + HC - 50), ad[:52], fill="black", font=f2)
            if i[0] != "M":
                dr.text((x + 8, y + HC - 30), "son kapaklar %.2f · tüm kapaklar %.2f" % (v, ev), fill="#060", font=f2)
            t.write("%d\t%s\t%s\tson %.3f (%s)\ttum kapaklar %.3f (%s)\t%s\n" % (k + 1, i, ad, v, en, ev, ek, yol(i)))
    sayfa.save(os.path.join(CIK, "siluet-aday.jpg"), quality=88)
    print(open(os.path.join(CIK, "siluet-aday.txt"), encoding="utf-8").read())
