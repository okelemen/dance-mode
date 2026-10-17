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
p.add_argument("--poz", type=int, default=0)
p.add_argument("--sadece-yazi", action="store_true",
               help="arka = Blender 3B render (siluetler icinde); yalniz baslik/etiket/NEW eklenir (md. 21)")
p.add_argument("--sol", default="2 Player|Co-op")
p.add_argument("--sag", default="80 Walls|10 MIN")
p.add_argument("--font", default="fontlar/TitanOne.ttf", help="baslik+etiket fontu (05-kapak'a gore)")
p.add_argument("--agirlik", type=int, default=0, help="degisken fontta wght (Fredoka 700, Baloo2 800)")
p.add_argument("--cikti", required=True)
a = p.parse_args()


def yfont(boy):
    """baslik/etiket fontu: referans kanal kalin, genis, oyunvari display font kullaniyor
    (kullanici 17 Eki: "referanstaki yazilar ... daha goz alici guzel yazi fontlari")"""
    yol = a.font if os.path.isabs(a.font) else os.path.join(KOK, a.font)
    f = ImageFont.truetype(yol, boy)
    if a.agirlik:
        try:
            f.set_variation_by_axes([a.agirlik] + ([100] if "Fredoka" in yol else []))
        except Exception:
            pass
    return f
P = json.load(open(os.path.join(KOK, "poz-noktalari.json"), encoding="utf-8"))
BOY, KAL = P["BOY"], P["KALINLIK"]
poz = P["poz"].get(str(a.poz))

if a.sadece_yazi:
    im = Image.open(a.arka).convert("RGB").resize((W, H), Image.LANCZOS).convert("RGBA")
    # baslik bandi okunurlugu: ust bandi hafif karart (referansta baslik arkasi koyu gok)
    bant = Image.new("RGBA", (W, H)); ImageDraw.Draw(bant).rectangle((0, 0, W, 175), fill=(10, 4, 30, 90))
    im.alpha_composite(bant.filter(ImageFilter.GaussianBlur(30)))
else:
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


def parlak_yazi(metin, f, renkler, kontur=9, derinlik=12, dis=(30, 0, 70), parlama=(255, 80, 220),
                zipla=6, don=4, aralik=4, golge=True):
    """Oyun logosu harfleri (kullanici 17 Eki: "yazilar cok basit ... Tetris mod yazisi cok soluk, al benisi yok"):
    harf harf dikey renk gecisi + ust yarida parlak bant + beyaz kontur + koyu 3B derinlik + renkli isilti,
    harfler hafif zipliyor ve donuyor."""
    d0 = ImageDraw.Draw(Image.new("L", (10, 10)))
    asc, desc = f.getmetrics(); hh = asc + desc
    pad = derinlik + kontur + 40
    gen = int(sum(d0.textlength(c, font=f) for c in metin) + aralik * len(metin)) + 2 * pad
    tuval = Image.new("RGBA", (gen, hh + 2 * pad + zipla * 2))
    x = pad
    for i, c in enumerate(metin):
        cw = d0.textlength(c, font=f)
        if c == " ":
            x += cw + aralik; continue
        # harf maskesi
        hm = Image.new("L", (int(cw) + 2 * pad, hh + 2 * pad)); ImageDraw.Draw(hm).text((pad, pad), c, font=f, fill=255)
        km = Image.new("L", hm.size); ImageDraw.Draw(km).text((pad, pad), c, font=f, fill=255, stroke_width=kontur, stroke_fill=255)
        L = Image.new("RGBA", hm.size)
        # koyu dis kontur (beyaz konturun etrafinda) — yaziyi arka plandan ayirir
        dm = km.filter(ImageFilter.MaxFilter(9))
        for k_ in range(derinlik, -1, -2):
            sh = Image.new("RGBA", hm.size, dis + (0,)); sh.putalpha(dm)
            L.alpha_composite(sh, (k_ // 2, k_))
        # 3B derinlik: koyu kopya asagi-saga kaydirilarak ust uste
        for k_ in range(derinlik, 0, -1):
            sh = Image.new("RGBA", hm.size, dis + (0,)); sh.putalpha(km)
            L.alpha_composite(sh, (k_ // 2, k_))
        # beyaz kontur
        bk = Image.new("RGBA", hm.size, (255, 255, 255, 0)); bk.putalpha(km); L.alpha_composite(bk)
        # dolgu: dikey gecis (acik ust -> doygun alt)
        r, g, b = renkler[i % len(renkler)]
        grad = Image.new("RGBA", hm.size)
        gd = ImageDraw.Draw(grad)
        for yy in range(hm.size[1]):
            q = min(1, max(0, (yy - pad) / max(1, asc)))
            if q < 0.45:                                          # ustte hafif acik (soluklasmasin: en fazla %20)
                m_ = 0.20 * (1 - q / 0.45)
                cc = (r + (255 - r) * m_, g + (255 - g) * m_, b + (255 - b) * m_)
            else:                                                 # altta derinlesen doygun ton
                m_ = 0.35 * (q - 0.45) / 0.55
                cc = (r * (1 - m_), g * (1 - m_), b * (1 - m_))
            gd.line([(0, yy), (hm.size[0], yy)], fill=tuple(int(v) for v in cc) + (255,))
        grad.putalpha(hm); L.alpha_composite(grad)
        # parlak bant: harfin ust yarisi, yari saydam beyaz, alt kenari yumusak
        band = Image.new("L", hm.size, 0); ImageDraw.Draw(band).ellipse((pad - cw * 0.2, pad - hh * 0.3, pad + cw * 1.2, pad + asc * 0.34), fill=120)
        band = Image.composite(band, Image.new("L", hm.size, 0), hm).filter(ImageFilter.GaussianBlur(2))
        bw_ = Image.new("RGBA", hm.size, (255, 255, 255, 0)); bw_.putalpha(band); L.alpha_composite(bw_)
        # hafif donme + ziplama
        aci = don * (1 if i % 2 == 0 else -1) * (0.6 + 0.4 * ((i * 37) % 5) / 4)
        L = L.rotate(aci, Image.BICUBIC, expand=False)
        dy = int(zipla * math.sin(i * 1.9))
        tuval.alpha_composite(L, (int(x - pad), zipla + dy))
        x += cw + aralik
    tuval = tuval.crop(tuval.getchannel("A").getbbox())
    if parlama:                                                   # renkli neon isilti
        e = 40
        big = Image.new("RGBA", (tuval.width + 2 * e, tuval.height + 2 * e)); big.alpha_composite(tuval, (e, e))
        g = big.getchannel("A").filter(ImageFilter.MaxFilter(11)).filter(ImageFilter.GaussianBlur(18))
        gl = Image.merge("RGBA", [Image.new("L", big.size, c) for c in parlama] + [g.point(lambda v: min(255, int(v * 1.3)))])
        gl.alpha_composite(big); tuval = gl
    return tuval


def koy(k, merkez, genislik=None):
    if genislik and k.width > genislik:
        k = k.resize((genislik, int(k.height * genislik / k.width)), Image.LANCZOS)
    im.alpha_composite(k, (int(merkez[0] - k.width / 2), int(merkez[1] - k.height / 2)))


GOKKUSAGI = [(255, 30, 140), (255, 120, 0), (255, 205, 0), (40, 210, 60), (0, 170, 255), (140, 70, 255)]
koy(parlak_yazi("TETRIS MODE", yfont(150), GOKKUSAGI, kontur=9, derinlik=14,
                 parlama=(255, 70, 210), zipla=7, don=4), (W / 2, 98), genislik=1210)

kucuk = yfont(54)
s1, s2 = a.sol.split("|"); g1, g2 = a.sag.split("|")
for metin, merkez, aci, renk in [(s1, (190, 238), 6, (60, 200, 255)), (s2, (175, 318), 6, (255, 80, 190)),
                                 (g1, (1090, 238), -6, (255, 200, 30)), (g2, (1110, 318), -6, (90, 230, 120))]:
    k_ = parlak_yazi(metin, kucuk, [renk], kontur=6, derinlik=7, parlama=(255, 255, 255), zipla=3, don=2, aralik=2)
    koy(k_.rotate(aci, Image.BICUBIC, expand=True), merkez)


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
    d.text(c, "NEW", font=yfont(int(r * 0.6)), fill=(255, 255, 255), anchor="mm",
           stroke_width=3, stroke_fill=(120, 0, 20))
    k = k.rotate(-8, Image.BICUBIC, expand=True)
    g = k.getchannel("A").filter(ImageFilter.GaussianBlur(10))
    sh = Image.merge("RGBA", [Image.new("L", k.size, 0)] * 3 + [g.point(lambda v: int(v * 0.6))])
    im.alpha_composite(sh, (int(merkez[0] - k.width / 2) + 6, int(merkez[1] - k.height / 2) + 8))
    im.alpha_composite(k, (int(merkez[0] - k.width / 2), int(merkez[1] - k.height / 2)))


rozet_new((128, 560))
im.convert("RGB").save(a.cikti, quality=93)
print(a.cikti, os.path.getsize(a.cikti) // 1024, "KB")
