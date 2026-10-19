"""TETRIS MODE 5. video kapagi (REF-056, 3 oyuncu, Halloween) - 1280x720.

    python kapak-x3-05.py --duzen 1|2 --sol spider-half-cactus-wide --orta vampire-v-tree --cikti KAPAK-1.jpg

REF-056 kapagi (olculdu: 14-GLOWMOTION-X3-2-KAPAK-OLCUM.md): ustte tombul parlak baslik, ortada uc dev DUZ SIMSIYAH siluet + beyaz
dis kontur (birbirine deger), arkada kapi panelinde ayni poz kucuk, yanlarda etiket, sag altta NEW!.
Kullanici 19 Eki 2026: yazi YALNIZ "TETRIS MODE" ve ayri "HALLOWEEN" ("full body olmayacak ... diger yerler goruntu olsun") ->
etiket / NEW! yerleri 3B balkabagi fenerleri + yarasalar. Videodaki duzen: 3 kapi, 3 kart, her kartta TEK siluet (kullanici).
  --duzen 1: yalniz 3 kart (buyumus duvar ani gibi), her kartta tek siluet oyugu; on planda buyuk siluet yok.
  --duzen 2: arkada kapilarda 3 kart (ayni pozlar) + on planda ayni uc poz dev siluet (sol / orta / sag = solun aynasi), ic eller deger.
Siluet kurallari TALIMATLAR §14c: duz siyah + dis beyaz kontur, kameraya donuk, ayna, temas, yazinin altinda (etiket -> siluet -> baslik).
"""
import argparse, math, os, random, json
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont, ImageEnhance

KOK = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
p = argparse.ArgumentParser()
p.add_argument("--duzen", required=True, choices=["1", "2", "ref"])
p.add_argument("--grup", default="a")          # duzen ref: kapak-grup-<x>.png
p.add_argument("--sol", default="spider-half-cactus-wide"); p.add_argument("--orta", default="vampire-v-tree")
p.add_argument("--varlik", default=os.path.join(KOK, "03-motor", "tetris-pvp", "varlik-05"))
p.add_argument("--oge", default=os.path.join(KOK, "03-motor", "tetris-pvp", "varlik-05-kapak"))
p.add_argument("--cikti", required=True)
a = p.parse_args()
V = a.varlik
W, H = 1280, 720
FONT = os.path.join(KOK, "05-kapak", "fontlar", "TitanOne.ttf")
yfont = lambda boy: ImageFont.truetype(FONT, boy)
LW = W / 3

# baslik harf yontemi (onayli: kapak-pvp-04.py parlak_yazi) - kaynaktan alinir, kopya tutulmaz
_k = open(os.path.join(KOK, "05-kapak", "kapak-pvp-04.py"), encoding="utf-8").read()
_g = {"Image": Image, "ImageDraw": ImageDraw, "ImageFilter": ImageFilter, "math": math, "PARLAK_BANT": 150}
exec(_k[_k.index("def parlak_yazi"):_k.index("def gecis")], _g)
parlak_yazi = _g["parlak_yazi"]


def gecis(n, c0, c1):
    return [tuple(int(c0[j] + (c1[j] - c0[j]) * (i / max(1, n - 1))) for j in range(3)) for i in range(n)]


def maske(ad, ayna=False):
    m = Image.open(os.path.join(V, "poz", ad + ".png")).getchannel("A")
    m = m.crop(m.getbbox())
    return m.transpose(Image.FLIP_LEFT_RIGHT) if ayna else m


POZ = [(a.sol, False), (a.orta, False), (a.sol, True)]        # P1 | P2 | P3: yanlar ayna (simetri, §14c)

# ---------------------------------------------------------------- arka plan: videonun sahnesi (gok + 3 serit)
REF = a.duzen == "ref"
if REF:
    # kullanici 19 Eki 2026: "referans kanalin kapagi ... o ne yaptiysa aynisini yap ama siluetin hareketleri farkli olsun" ->
    # REF-056 kapak duzeni: tek kapi SAGDA (kamera sola kayik Blender sahnesi), onde 3 kisilik TEK grup siluet, kapida ayni grubun kucugu
    im = Image.open(os.path.join(a.oge, "kapak-gok.png")).convert("RGBA")
    im.alpha_composite(Image.open(os.path.join(a.oge, "kapak-serit.png")).convert("RGBA"))
    YK = json.load(open(os.path.join(a.oge, "yerlesim.json"), encoding="utf-8"))
else:
    im = Image.open(os.path.join(V, "gok.png")).convert("RGBA").resize((W, H), Image.LANCZOS)
    for i in range(3):
        s = Image.open(os.path.join(V, f"serit-p{i + 1}.png")).convert("RGBA").resize((int(LW) + 1, H), Image.LANCZOS)
        im.alpha_composite(s, (int(i * LW), 0))
Y = json.load(open(os.path.join(V, "yerlesim.json"), encoding="utf-8"))
SW = Y.get("yol", {}).get("serit_w", 640)
ORAN = 1100 / 904


def kart(i, kutu, ad, ayna):
    """oyuncu renginde panel + tek siluet oyugu (videodaki duvarCiz ile ayni: oyuk koyu, kenarda acik isilti)"""
    x, y, w, h = [int(v) for v in kutu]
    pn = Image.open(os.path.join(V, f"panel-p{i + 1}.png")).convert("RGBA").resize((w, h), Image.LANCZOS)
    m = Image.open(os.path.join(V, "poz", ad + ".png")).getchannel("A")
    if ayna:
        m = m.transpose(Image.FLIP_LEFT_RIGHT)
    m = m.resize((w, h), Image.LANCZOS)
    kenar = m.filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.GaussianBlur(3))
    pn.alpha_composite(Image.merge("RGBA", [Image.new("L", (w, h), c) for c in (255, 240, 215)] + [kenar.point(lambda v: int(v * 0.8))]))
    pn.alpha_composite(Image.merge("RGBA", [Image.new("L", (w, h), c) for c in (20, 6, 36)] + [m]))
    im.alpha_composite(pn, (x, y))


def kapi_kutusu(i):
    ac = Y[f"aciklik_p{i + 1}"]; sx = LW / SW; sy = H / 1080
    x0, y0, x1, y1 = ac[0] * sx + i * LW, ac[1] * sy, ac[2] * sx + i * LW, ac[3] * sy
    w = x1 - x0; h = w / ORAN
    if h > y1 - y0:
        h = y1 - y0; w = h * ORAN
    return (x0 + (x1 - x0 - w) / 2, y1 - h, w, h)


if a.duzen == "2":
    for i, (ad, ay) in enumerate(POZ):
        kart(i, kapi_kutusu(i), ad, ay)
GRUP = None
if REF:
    GRUP = Image.open(os.path.join(a.oge, f"kapak-grup-{a.grup}.png")).getchannel("A")
    GRUP = GRUP.crop(GRUP.getbbox())
    ac = YK["kapak_aciklik"]; aw = ac[2] - ac[0]; ah = ac[3] - ac[1]
    pw = aw; ph = pw / ORAN
    if ph > ah:
        ph = ah; pw = ph * ORAN
    x0 = int(ac[0] + (aw - pw) / 2); y0 = int(ac[3] - ph); pw, ph = int(pw), int(ph)
    pn = Image.open(os.path.join(V, "panel-p1.png")).convert("RGBA").resize((pw, ph), Image.LANCZOS)
    gs = min(ph * 0.82 / GRUP.height, pw * 0.86 / GRUP.width)
    gm = GRUP.resize((int(GRUP.width * gs), int(GRUP.height * gs)), Image.LANCZOS)
    mm = Image.new("L", (pw, ph)); mm.paste(gm, ((pw - gm.width) // 2, ph - gm.height - int(ph * 0.04)))
    pn.alpha_composite(Image.merge("RGBA", [Image.new("L", (pw, ph), c) for c in (8, 4, 16)] + [mm]))
    im.alpha_composite(pn, (x0, y0))
# ampul isiltisi
gl = Image.new("RGBA", (W, H)); dg = ImageDraw.Draw(gl)
for i in range(0 if REF else 3):            # ref duzeninde videonun 3 serit ampulu yok (deneme 1: solda bos ampul cercevesi kaldi)
    for q in Y.get(f"ampul_p{i + 1}", []):
        x = i * LW + q[0] * LW / SW; y = q[1] * H / 1080
        dg.ellipse((x - 5, y - 5, x + 5, y + 5), fill=(255, 210, 150, 230))
im.alpha_composite(gl.filter(ImageFilter.GaussianBlur(3))); im.alpha_composite(gl)
im = ImageEnhance.Brightness(ImageEnhance.Color(im).enhance(1.15)).enhance(0.88)   # kisik: siluetleri yutmasin (§14c)

# ---------------------------------------------------------------- yarasalar (referansin sag ust etiket yeri goruntu olur)
rnd = random.Random(56)
fx = Image.new("RGBA", (W, H)); df = ImageDraw.Draw(fx)


def yarasa(x, y, s, kanat):
    uy = (-0.55 if kanat else 0.25) * s
    pts = [(x, y - 0.12 * s), (x + 0.3 * s, y - 0.1 * s), (x + 0.62 * s, y + uy), (x + 0.42 * s, y + 0.12 * s), (x + 0.22 * s, y + 0.06 * s),
           (x + 0.1 * s, y + 0.2 * s), (x, y + 0.12 * s), (x - 0.1 * s, y + 0.2 * s), (x - 0.22 * s, y + 0.06 * s), (x - 0.42 * s, y + 0.12 * s),
           (x - 0.62 * s, y + uy), (x - 0.3 * s, y - 0.1 * s)]
    df.polygon(pts, fill=(8, 3, 14, 255))
    df.ellipse((x - 0.09 * s, y - 0.24 * s, x + 0.09 * s, y - 0.06 * s), fill=(8, 3, 14, 255))


# deneme 1: duzen 2'de yarasalar arkadaki kartlarin ustune biniyordu -> kart kutularinin disinda kalan gok/kenar alanlari
kartlar = ([(YK["kapak_aciklik"][0], YK["kapak_aciklik"][1], YK["kapak_aciklik"][2] - YK["kapak_aciklik"][0], YK["kapak_aciklik"][3] - YK["kapak_aciklik"][1])]
           if REF else [kapi_kutusu(i) for i in range(3)])
konan = 0
while konan < 14:
    x, y, s_ = rnd.uniform(10, 1270), rnd.uniform(150, 340), rnd.uniform(22, 46)
    if any(k[0] - s_ < x < k[0] + k[2] + s_ and k[1] - s_ < y < k[1] + k[3] + s_ for k in kartlar):
        continue
    if REF and not (x > 960 or x < 260):           # ref: yarasalar referansin etiket yerlerinde (sag ust "Full Body", sol "x3 player")
        continue
    yarasa(x, y, s_, rnd.random() < 0.5); konan += 1
im.alpha_composite(fx)

# ---------------------------------------------------------------- balkabaklari (sol alt tek fener, sag alt kume - NEW!/etiket yerine)
def oge(ad, merkez_x, alt_y, gen):
    o = Image.open(os.path.join(a.oge, ad)).convert("RGBA")
    o.putalpha(o.getchannel("A").point(lambda v: 0 if v < 60 else v))      # deneme 1: dunya isigi zemini yari saydam kutu birakti
    o = o.crop(o.getbbox())
    s = gen / o.width; o = o.resize((int(o.width * s), int(o.height * s)), Image.LANCZOS)
    e = 60                                                    # deneme 2: isilti kirpilan kutuda kesilip dikdortgen gorunuyordu -> pay
    big = Image.new("RGBA", (o.width + 2 * e, o.height + 2 * e)); big.alpha_composite(o, (e, e)); o = big
    alt_y += e
    g = o.getchannel("A").filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.GaussianBlur(22))
    im.alpha_composite(Image.merge("RGBA", [Image.new("L", o.size, c) for c in (255, 150, 40)] + [g.point(lambda v: int(v * 0.6))]),
                       (int(merkez_x - o.width / 2), int(alt_y - o.height)))
    im.alpha_composite(o, (int(merkez_x - o.width / 2), int(alt_y - o.height)))


if REF:   # referansin "x3 player" (sol orta-alt) ve NEW! (sag alt) yerleri
    oge("kapak-kabak.png", 165, 640, 190)
    oge("kapak-kabak-kume.png", 1120, 712, 290)
else:
    oge("kapak-kabak.png", 120, 712, 210)
    oge("kapak-kabak-kume.png", 1150, 712, 270)

# ---------------------------------------------------------------- baslik + HALLOWEEN (ayri yazi)
renk = gecis(6, (255, 122, 26), (255, 205, 60)) + [(255, 255, 255)] + gecis(4, (163, 92, 255), (215, 160, 255))
yz = parlak_yazi("TETRIS MODE", yfont(150), renk, kontur=10, derinlik=15, dis=(40, 8, 60), parlama=(255, 170, 90), zipla=0, don=0)
if yz.width > 1200:
    yz = yz.resize((1200, int(yz.height * 1200 / yz.width)), Image.LANCZOS)
by = int(82 - yz.height / 2)
hw = parlak_yazi("HALLOWEEN", yfont(74), gecis(9, (150, 255, 90), (90, 230, 60)), kontur=8, derinlik=10, dis=(10, 40, 10),
                 parlama=(140, 255, 120), zipla=0, don=0, aralik=6)
hy = by + int(yz.getchannel("A").point(lambda v: 255 if v > 200 else 0).getbbox()[3]) - 18
yazi_alt = hy + int(hw.getchannel("A").point(lambda v: 255 if v > 200 else 0).getbbox()[3])

# ---------------------------------------------------------------- duzen 1: buyumus 3 kart (on plan)
if a.duzen == "1":
    kw = 392; kh = kw / ORAN
    alt = 668
    for i, (ad, ay) in enumerate(POZ):
        cxk = i * LW + LW / 2
        kart(i, (cxk - kw / 2, alt - kh, kw, kh), ad, ay)
    # kart cercevesi ince beyaz-isik (oyuncu renginde parilti)
    cer = Image.new("RGBA", (W, H)); dc = ImageDraw.Draw(cer)
    for i, rr in enumerate(((255, 122, 26), (125, 255, 74), (163, 92, 255))):
        cxk = i * LW + LW / 2
        dc.rounded_rectangle((cxk - kw / 2 - 5, alt - kh - 5, cxk + kw / 2 + 5, alt + 5), radius=10, outline=rr + (255,), width=6)
    im.alpha_composite(cer.filter(ImageFilter.GaussianBlur(6))); im.alpha_composite(cer)

# ---------------------------------------------------------------- duzen 2: on planda dev siluetler (yazinin altinda, ic eller deger)
KONTUR = 19


def yerles(m, merkez_x, alt_y, hedef_h):
    s = hedef_h / m.height
    m = m.resize((max(1, int(m.width * s)), int(m.height * s)), Image.LANCZOS)
    tam = Image.new("L", (W, H)); tam.paste(m, (int(merkez_x - m.width / 2), int(alt_y - m.height)))
    return tam.point(lambda v: 255 if v > 110 else 0)


if a.duzen == "2":
    ust = yazi_alt + KONTUR + 6
    hO = H - 4 - ust                                          # ortadaki: yazinin altindan zemine
    orta = yerles(maske(a.orta), W / 2, H - 4, hO)
    hS = hO * 0.94
    msol = maske(a.sol)
    sol = None
    for x in range(int(W / 2 - 160), 60, -6):                 # disaridan iceri: ilk degdigi (bindirme baslayan) yer
        m = yerles(msol, x, H - 4, hS)
        if ImageChops.multiply(m, orta).getbbox() is None:
            sol = m; break
    sag = sol.transpose(Image.FLIP_LEFT_RIGHT)
    # temas: iki maske arasi bosluk kapanana kadar ice kaydir (ic eller ortadakine deger)
    for _ in range(40):
        if ImageChops.multiply(sol.filter(ImageFilter.MaxFilter(5)), orta).getbbox() is not None:
            break
        sol = ImageChops.offset(sol, 3, 0); sag = ImageChops.offset(sag, -3, 0)
    mk = ImageChops.lighter(ImageChops.lighter(sol, orta), sag)
    mk = mk.filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.MinFilter(3))
    kontur = mk.filter(ImageFilter.MaxFilter(KONTUR))
    isilti = kontur.filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.GaussianBlur(16))
    im.alpha_composite(Image.merge("RGBA", [Image.new("L", (W, H), c) for c in (255, 200, 140)] + [isilti.point(lambda v: int(v * 0.5))]))
    im.alpha_composite(Image.merge("RGBA", [Image.new("L", (W, H), 255)] * 3 + [kontur]))
    im.alpha_composite(Image.merge("RGBA", [Image.new("L", (W, H), c) for c in (6, 4, 14)] + [mk.filter(ImageFilter.GaussianBlur(0.7))]))
    print("siluet kutusu", mk.getbbox(), "yazi alti", yazi_alt)

if REF:
    ust = yazi_alt + KONTUR + 6
    hh = H - 4 - ust; s_ = hh / GRUP.height
    if GRUP.width * s_ > 720:
        s_ = 720 / GRUP.width
    gm = GRUP.resize((int(GRUP.width * s_), int(GRUP.height * s_)), Image.LANCZOS)
    mk = Image.new("L", (W, H)); mk.paste(gm, (int(470 - gm.width / 2), H - 4 - gm.height))
    mk = mk.point(lambda v: 255 if v > 110 else 0).filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.MinFilter(3))
    kontur = mk.filter(ImageFilter.MaxFilter(KONTUR))
    isilti = kontur.filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.GaussianBlur(16))
    im.alpha_composite(Image.merge("RGBA", [Image.new("L", (W, H), c) for c in (255, 200, 140)] + [isilti.point(lambda v: int(v * 0.5))]))
    im.alpha_composite(Image.merge("RGBA", [Image.new("L", (W, H), 255)] * 3 + [kontur]))
    im.alpha_composite(Image.merge("RGBA", [Image.new("L", (W, H), c) for c in (6, 4, 14)] + [mk.filter(ImageFilter.GaussianBlur(0.7))]))
    print("grup siluet kutusu", mk.getbbox())
im.alpha_composite(yz, (int(W / 2 - yz.width / 2), by))
im.alpha_composite(hw, (int(W / 2 - hw.width / 2), hy))
im.convert("RGB").save(a.cikti, quality=93)
print(a.cikti, os.path.getsize(a.cikti) // 1024, "KB")
