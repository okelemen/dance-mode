"""TETRIS MODE kapagi — @HumanWarmUp kapak kalibi (kullanici, 17 Eki 2026: "bu verdigim referans kanalin kapak
fotograflarina bak ... cok begendim, ben bu sekilde kapak fotografi istiyorum. Yaptiklarini begenmedim.")

Kalip (kanalin en cok izlenen 16 + en yeni 8 kapagi, REFERANS-KANALLAR/humanwarmup-kapaklar/):
- ustte ortada yuvarlak hatli kalin baslik, harf harf gokkusagi + beyaz kontur + koyu dis kontur + isilti
- arka: birinci sahis neon yol, uzakta cerceveli renkli duvar paneli, icinde kucuk poz (VIDEONUN KENDI KARESI)
- on planda DEV siyah siluetler, kalin beyaz kontur, paneldeki pozun aynisi (poz-noktalari.json, pozlar.js'ten)
- yanlarda egik, parlayan kucuk etiketler (2 Player, Co-op, 80 Walls, 10 MIN), kirmizi kurdeleli NEW rozeti
Yalniz baslik yazisi Dance Mode'dan: "TETRIS MODE". Kalori, "1M VIEWS", gercek insan yok.

    python kapak-tetris.py --arka kare.png --poz 80 --cikti A.jpg [--sol "2 Player|Co-op"] [--sag "80 Walls|10 MIN"]
"""
import argparse, json, math, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

F = "C:/Windows/Fonts/"
YUVARLAK = "ARLRDBD.TTF"                 # Arial Rounded MT Bold — referanstaki yuvarlak baslik
W, H = 1280, 720
KOK = os.path.dirname(os.path.abspath(__file__))

p = argparse.ArgumentParser()
p.add_argument("--arka", required=True, help="masterdan 1920x1080 kare: duvar uzakta, poz gorunur")
p.add_argument("--kutu", default="160,90,1760,990", help="HUD/abone dugmesi disarida kalacak kirpma")
p.add_argument("--poz", type=int, required=True)
p.add_argument("--sol", default="2 Player|Co-op")
p.add_argument("--sag", default="80 Walls|10 MIN")
p.add_argument("--cikti", required=True)
a = p.parse_args()
P = json.load(open(os.path.join(KOK, "poz-noktalari.json"), encoding="utf-8"))
BOY, KAL = P["BOY"], P["KALINLIK"]
poz = P["poz"][str(a.poz)]

# ---------------------------------------------------------------- arka plan (videonun kendi karesi)
x0, y0, x1, y1 = (int(v) for v in a.kutu.split(","))
im = Image.open(a.arka).convert("RGB").crop((x0, y0, x1, y1)).resize((W, H), Image.LANCZOS)
im = ImageEnhance.Color(im).enhance(1.45)
im = ImageEnhance.Contrast(im).enhance(1.12)
im = ImageEnhance.Brightness(im).enhance(1.08)
im = Image.blend(im, im.filter(ImageFilter.GaussianBlur(14)), 0.25).convert("RGBA")
# baslik bandi: arkadaki oyun yazilari (sayim rakami, MATCH!) basligin arasindan gorunmesin
bant = im.crop((0, 0, W, 190)).filter(ImageFilter.GaussianBlur(22))
bm = Image.new("L", (W, 190), 0); ImageDraw.Draw(bm).rectangle((0, 0, W, 150), fill=255)
im.paste(bant, (0, 0), bm.filter(ImageFilter.GaussianBlur(25)))


# ---------------------------------------------------------------- dev siluetler
def figur_maske(n, olc, ox, oy):
    m = Image.new("L", (W, H), 0); d = ImageDraw.Draw(m)
    Pn = lambda q: (ox + q[0] * olc, oy - q[1] * olc)
    parca = [("kalca", "boyun", KAL["govde"]), ("omuzSol", "omuzSag", KAL["kol"]), ("kalcaSol", "kalcaSag", KAL["bacak"]),
             ("omuzSol", "solDir", KAL["kol"]), ("solDir", "solEl", KAL["kol"]),
             ("omuzSag", "sagDir", KAL["kol"]), ("sagDir", "sagEl", KAL["kol"]),
             ("kalcaSol", "solDiz", KAL["bacak"]), ("solDiz", "solAyak", KAL["bacak"]),
             ("kalcaSag", "sagDiz", KAL["bacak"]), ("sagDiz", "sagAyak", KAL["bacak"]),
             ("solAyak", "solUc", KAL["ayak"]), ("sagAyak", "sagUc", KAL["ayak"])]
    for u, v, k in parca:
        A, B = Pn(n[u]), Pn(n[v]); w = k * olc
        d.line([A, B], fill=255, width=int(w))
        for c in (A, B):
            d.ellipse((c[0] - w / 2, c[1] - w / 2, c[0] + w / 2, c[1] + w / 2), fill=255)
    b = Pn(n["bas"]); r = BOY["bas"] * olc
    d.ellipse((b[0] - r, b[1] - r, b[0] + r, b[1] + r), fill=255)
    return m


if not poz["temas"]:                                         # temassiz pozda figurler kapakta birbirine girmesin
    gap = 60
    sag1 = max(q[0] for q in poz["p1"].values()); sol2 = min(q[0] for q in poz["p2"].values())
    if sol2 - sag1 < gap:
        dx = (gap - (sol2 - sag1)) / 2
        poz["p1"] = {k_: [q[0] - dx, q[1]] for k_, q in poz["p1"].items()}
        poz["p2"] = {k_: [q[0] + dx, q[1]] for k_, q in poz["p2"].items()}
tum = [q for n in (poz["p1"], poz["p2"]) for q in n.values()]
ymax = max(q[1] for q in tum) + BOY["bas"]
xspan = max(q[0] for q in tum) - min(q[0] for q in tum) + 40
olc = min(560 / ymax, 900 / xspan)
ox, oy = W / 2, H + 6
maske = Image.new("L", (W, H), 0)
for n in (poz["p1"], poz["p2"]):
    maske = Image.composite(Image.new("L", (W, H), 255), maske, figur_maske(n, olc, ox, oy))
kontur = maske.filter(ImageFilter.MaxFilter(17))
isilti = kontur.filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.GaussianBlur(18))
im.alpha_composite(Image.merge("RGBA", [Image.new("L", (W, H), c) for c in (255, 120, 230)] + [isilti.point(lambda v: int(v * 0.85))]))
im.alpha_composite(Image.merge("RGBA", [Image.new("L", (W, H), 255)] * 3 + [kontur]))
im.alpha_composite(Image.merge("RGBA", [Image.new("L", (W, H), c) for c in (8, 6, 16)] + [maske]))
if poz["temas"]:
    t1, t2 = poz["temas"][0], poz["temas"][1]
    cxk = ox + (poz["p1"][t1][0] + poz["p2"][t2][0]) / 2 * olc
    cyk = oy - (poz["p1"][t1][1] + poz["p2"][t2][1]) / 2 * olc
    k = Image.new("RGBA", (W, H)); dk = ImageDraw.Draw(k)
    dk.ellipse((cxk - 70, cyk - 70, cxk + 70, cyk + 70), fill=(255, 240, 160, 255))
    im.alpha_composite(k.filter(ImageFilter.GaussianBlur(26)))
    k = Image.new("RGBA", (W, H)); dk = ImageDraw.Draw(k)
    for i in range(12):
        an = i / 12 * 2 * math.pi
        dk.line([(cxk + math.cos(an) * 16, cyk + math.sin(an) * 16), (cxk + math.cos(an) * 58, cyk + math.sin(an) * 58)],
                fill=(255, 255, 255, 255), width=5)
    dk.ellipse((cxk - 16, cyk - 16, cxk + 16, cyk + 16), fill=(255, 255, 255, 255))
    im.alpha_composite(k)


# ---------------------------------------------------------------- yazilar
def katman_yazi(metin, f, dolgular, kk_ic=7, kk_dis=13, dis=(25, 10, 60), egim=0.0, parlama=None, aralik=0):
    d0 = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    gen = sum(d0.textlength(c, font=f) for c in metin) + aralik * (len(metin) - 1)
    asc, desc = f.getmetrics()
    pad = 70
    k = Image.new("RGBA", (int(gen) + 2 * pad, asc + desc + 2 * pad)); d = ImageDraw.Draw(k)
    for kat in ("dis", "ic", "dolgu"):
        x = pad
        for i, c in enumerate(metin):
            if kat == "dis":
                d.text((x, pad), c, font=f, fill=dis, stroke_width=kk_dis, stroke_fill=dis)
            elif kat == "ic":
                d.text((x, pad), c, font=f, fill=(255, 255, 255), stroke_width=kk_ic, stroke_fill=(255, 255, 255))
            else:
                d.text((x, pad), c, font=f, fill=dolgular[i % len(dolgular)])
            x += d0.textlength(c, font=f) + aralik
    if egim:
        k = k.rotate(egim, Image.BICUBIC, expand=True)
    if parlama:
        g = k.getchannel("A").filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.GaussianBlur(16))
        gl = Image.merge("RGBA", [Image.new("L", k.size, c) for c in parlama] + [g.point(lambda v: int(v * 0.8))])
        gl.alpha_composite(k); k = gl
    return k


def koy(k, merkez, genislik=None):
    if genislik and k.width > genislik:
        k = k.resize((genislik, int(k.height * genislik / k.width)), Image.LANCZOS)
    im.alpha_composite(k, (int(merkez[0] - k.width / 2), int(merkez[1] - k.height / 2)))


GOKKUSAGI = [(255, 70, 160), (255, 150, 30), (255, 220, 40), (90, 230, 90), (40, 200, 255), (150, 110, 255)]
koy(katman_yazi("TETRIS MODE", ImageFont.truetype(F + YUVARLAK, 150), GOKKUSAGI, kk_ic=7, kk_dis=14,
                parlama=(255, 90, 220), aralik=2), (W / 2, 92), genislik=1200)

kucuk = ImageFont.truetype(F + YUVARLAK, 54)
s1, s2 = a.sol.split("|"); g1, g2 = a.sag.split("|")
for metin, merkez, aci, renk in [(s1, (190, 238), 6, (255, 255, 255)), (s2, (175, 312), 6, (255, 120, 220)),
                                 (g1, (1090, 238), -6, (255, 230, 60)), (g2, (1110, 312), -6, (120, 220, 255))]:
    koy(katman_yazi(metin, kucuk, [renk], kk_ic=4, kk_dis=8, egim=aci, parlama=(255, 255, 255)), merkez)


def rozet_new(merkez, r=74):
    k = Image.new("RGBA", (int(r * 3), int(r * 3.4))); d = ImageDraw.Draw(k)
    c = (k.width / 2, r * 1.35)
    for dx in (-1, 1):
        d.polygon([(c[0] + dx * r * 0.25, c[1]), (c[0] + dx * r * 0.85, c[1] + r * 1.9),
                   (c[0] + dx * r * 0.55, c[1] + r * 1.65), (c[0] + dx * r * 0.35, c[1] + r * 2.0),
                   (c[0] + dx * r * 0.05, c[1] + r * 0.4)], fill=(200, 20, 40), outline=(255, 210, 60))
    n = 22; pts = []
    for i in range(n * 2):
        rr = r if i % 2 == 0 else r * 0.88
        an = i * math.pi / n
        pts.append((c[0] + math.cos(an) * rr, c[1] + math.sin(an) * rr))
    d.polygon(pts, fill=(255, 205, 50))
    d.ellipse((c[0] - r * 0.8, c[1] - r * 0.8, c[0] + r * 0.8, c[1] + r * 0.8), fill=(230, 25, 45), outline=(255, 255, 255), width=4)
    d.text(c, "NEW", font=ImageFont.truetype(F + YUVARLAK, int(r * 0.62)), fill=(255, 255, 255), anchor="mm",
           stroke_width=3, stroke_fill=(120, 0, 20))
    k = k.rotate(-8, Image.BICUBIC, expand=True)
    g = k.getchannel("A").filter(ImageFilter.GaussianBlur(10))
    sh = Image.merge("RGBA", [Image.new("L", k.size, 0)] * 3 + [g.point(lambda v: int(v * 0.6))])
    im.alpha_composite(sh, (int(merkez[0] - k.width / 2) + 6, int(merkez[1] - k.height / 2) + 8))
    im.alpha_composite(k, (int(merkez[0] - k.width / 2), int(merkez[1] - k.height / 2)))


rozet_new((128, 560))
im.convert("RGB").save(a.cikti, quality=93)
print(a.cikti, os.path.getsize(a.cikti) // 1024, "KB")
