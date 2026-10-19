"""TETRIS MODE 5. video kapagi - REF-056 kapak DUZENININ AYNISI, siluet hareketleri farkli (kullanici 19 Eki 2026:
"referans kanalin kapagi cok iyi ... o ne yaptiysa aynisini yap ama siluetin hareketleri farkli olsun"; deneme 1'e "hic begenmedim").

    python kapak-x3-05-ref.py --grup a --cikti KAPAK-A.jpg

REF-056 kapagi (14-GLOWMOTION-X3-2-KAPAK-OLCUM.md): ustte tam genislik tombul parlak baslik; hemen altindan zemine kadar UC KISILIK
SIKISIK ve UZUN grup silueti (duz siyah, kalin beyaz dis kontur, kisiler arasinda ince beyaz hat), kadrajin orta-solunda; sagda TEK
kafes kapi, icinde turuncu renk gecisli panelde ayni grup kucuk; arka plan PARLAK doygun gok (galaksi), sade - siluetin arkasi temiz;
sag ustte egik etiket (Full Body), sol ortada etiket (x3 player), sag altta NEW!.
Bizde: yazi YALNIZ "TETRIS MODE" (baslik) + "HALLOWEEN" (sag ustteki egik etiket yerinde; kullanici "full body olmayacak").
x3 player / NEW! yerleri 3B balkabagi fenerleri. Gok = videonun gok.png'i (dolunay + ruh girdabi), kapi = videonun P1 seridi.
"""
import argparse, math, os, random, json
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont, ImageEnhance

KOK = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
p = argparse.ArgumentParser()
p.add_argument("--grup", default="a")
p.add_argument("--varlik", default=os.path.join(KOK, "03-motor", "tetris-pvp", "varlik-05"))
p.add_argument("--oge", default=os.path.join(KOK, "03-motor", "tetris-pvp", "varlik-05-kapak"))
p.add_argument("--cikti", required=True)
a = p.parse_args()
V, O = a.varlik, a.oge
W, H = 1280, 720
FONT = os.path.join(KOK, "05-kapak", "fontlar", "TitanOne.ttf")
yfont = lambda boy: ImageFont.truetype(FONT, boy)
_k = open(os.path.join(KOK, "05-kapak", "kapak-pvp-04.py"), encoding="utf-8").read()
_g = {"Image": Image, "ImageDraw": ImageDraw, "ImageFilter": ImageFilter, "math": math, "PARLAK_BANT": 150}
exec(_k[_k.index("def parlak_yazi"):_k.index("def gecis")], _g)
parlak_yazi = _g["parlak_yazi"]
gecis = lambda n, c0, c1: [tuple(int(c0[j] + (c1[j] - c0[j]) * (i / max(1, n - 1))) for j in range(3)) for i in range(n)]
ORAN = 1100 / 904

# ---------------------------------------------------------------- 1) gok: parlak, doygun (REF-056 gibi), siluetin arkasi temiz
im = Image.open(os.path.join(V, "gok.png")).convert("RGB").resize((W, H), Image.LANCZOS)
im = ImageEnhance.Contrast(ImageEnhance.Brightness(ImageEnhance.Color(im).enhance(1.45)).enhance(1.12)).enhance(1.08).convert("RGBA")

# ---------------------------------------------------------------- 2) zemin + sagda TEK kapi: kapak icin render edilen sahne (kamera sola kayik,
# kapi sagda, tabela YAZISIZ - deneme 2: video seridi "PLAYER 1" yazisi tasiyordu ve sol alt zeminsiz simsiyah kaliyordu)
zemin = Image.open(os.path.join(O, "kapak-serit.png")).convert("RGBA")
zemin = ImageEnhance.Color(zemin).enhance(1.3)
YK = json.load(open(os.path.join(O, "yerlesim.json"), encoding="utf-8"))
ac = YK["kapak_aciklik"]
# deneme 3: kapi kucuk ve yuksekteydi (REF-056 paneli ~290 px, y~350-600) -> zemin katmani kapi merkezli buyutulur, kapi sag ortaya iner
ZS = 1.35
kcx, kcy = (ac[0] + ac[2]) / 2, (ac[1] + ac[3]) / 2
ox, oy = 885 - kcx * ZS, 470 - kcy * ZS
zemin = zemin.resize((int(W * ZS), int(H * ZS)), Image.LANCZOS)
kat = Image.new("RGBA", (W, H)); kat.alpha_composite(zemin.crop((int(-ox), int(-oy), int(-ox) + W, int(-oy) + H)) if oy <= 0 else zemin, (0, 0) if oy <= 0 else (int(ox), int(oy)))
im.alpha_composite(kat)
ac = [ac[0] * ZS + ox, ac[1] * ZS + oy, ac[2] * ZS + ox, ac[3] * ZS + oy]
GR = Image.open(os.path.join(O, f"kapak-grup-{a.grup}.png")).getchannel("A")
bb = GR.getbbox()
ax0, ay0, ax1, ay1 = ac
pw = ax1 - ax0; ph = pw / ORAN
if ph > ay1 - ay0:
    ph = ay1 - ay0; pw = ph * ORAN
pw, ph = int(pw), int(ph)
pn = Image.open(os.path.join(V, "panel-p1.png")).convert("RGBA").resize((pw, ph), Image.LANCZOS)
pn = ImageEnhance.Color(pn).enhance(1.25)
g = GR.crop(bb); gs = min(ph * 0.84 / g.height, pw * 0.88 / g.width)
g = g.resize((int(g.width * gs), int(g.height * gs)), Image.LANCZOS)
mm = Image.new("L", (pw, ph)); mm.paste(g, ((pw - g.width) // 2, ph - g.height - int(ph * 0.03)))
pn.alpha_composite(Image.merge("RGBA", [Image.new("L", (pw, ph), c) for c in (8, 4, 16)] + [mm]))
PX, PY = int(ax0 + (ax1 - ax0 - pw) / 2), int(ay1 - ph)
im.alpha_composite(pn, (PX, PY))

# ---------------------------------------------------------------- 3) etiket yerleri: goruntu (balkabagi + yarasa)
def oge(ad, merkez_x, alt_y, gen, isilti=0.55):
    o = Image.open(os.path.join(O, ad)).convert("RGBA")
    o.putalpha(o.getchannel("A").point(lambda v: 0 if v < 60 else v)); o = o.crop(o.getbbox())
    s = gen / o.width; o = o.resize((int(o.width * s), int(o.height * s)), Image.LANCZOS)
    e = 60; big = Image.new("RGBA", (o.width + 2 * e, o.height + 2 * e)); big.alpha_composite(o, (e, e))
    gl = big.getchannel("A").filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.GaussianBlur(22))
    x, y = int(merkez_x - big.width / 2), int(alt_y + e - big.height)
    im.alpha_composite(Image.merge("RGBA", [Image.new("L", big.size, c) for c in (255, 150, 40)] + [gl.point(lambda v: int(v * isilti))]), (x, y))
    im.alpha_composite(big, (x, y))


oge("kapak-kabak.png", 150, 560, 170)                 # REF-056 "x3 player" yeri (sol orta)
oge("kapak-kabak-kume.png", 1120, 712, 250)           # REF-056 NEW! yeri (sag alt)
rnd = random.Random(56)
fx = Image.new("RGBA", (W, H)); df = ImageDraw.Draw(fx)
for _ in range(10):                                    # sol ust ve sag ust gokte yarasa surusu
    x, y, s = rnd.choice([rnd.uniform(40, 330), rnd.uniform(900, 1250)]), rnd.uniform(160, 330), rnd.uniform(20, 42)
    k = rnd.random() < 0.5; uy = (-0.55 if k else 0.25) * s
    df.polygon([(x, y - 0.12 * s), (x + 0.3 * s, y - 0.1 * s), (x + 0.62 * s, y + uy), (x + 0.42 * s, y + 0.12 * s), (x + 0.22 * s, y + 0.06 * s),
                (x + 0.1 * s, y + 0.2 * s), (x, y + 0.12 * s), (x - 0.1 * s, y + 0.2 * s), (x - 0.22 * s, y + 0.06 * s), (x - 0.42 * s, y + 0.12 * s),
                (x - 0.62 * s, y + uy), (x - 0.3 * s, y - 0.1 * s)], fill=(8, 3, 14, 255))
    df.ellipse((x - 0.09 * s, y - 0.24 * s, x + 0.09 * s, y - 0.06 * s), fill=(8, 3, 14, 255))
im.alpha_composite(fx)

# ---------------------------------------------------------------- 4) baslik (tam genislik, ustte) - REF-056 gibi kelime ici renk gecisi
renk = gecis(6, (255, 110, 20), (255, 215, 60)) + [(255, 255, 255)] + gecis(4, (150, 80, 255), (240, 120, 255))
yz = parlak_yazi("TETRIS MODE", yfont(156), renk, kontur=10, derinlik=15, dis=(60, 10, 90), parlama=(255, 150, 230), zipla=0, don=0)
if yz.width > 1230:
    yz = yz.resize((1230, int(yz.height * 1230 / yz.width)), Image.LANCZOS)
by = int(78 - yz.height / 2)
baslik_alt = by + yz.getchannel("A").point(lambda v: 255 if v > 200 else 0).getbbox()[3]

# ---------------------------------------------------------------- 5) GRUP SILUETI: sikisik, uzun, orta-solda (kisi basi beyaz hat)
KON = 19
ust = baslik_alt + KON + 4
hh = H - 2 - ust
kisi = [Image.open(os.path.join(O, f"kapak-grup-{a.grup}-{j}.png")).getchannel("A").crop(bb) for j in range(3)]
olc = hh / bb_h if (bb_h := bb[3] - bb[1]) else 1
if (bb[2] - bb[0]) * olc > 560:
    olc = 560 / (bb[2] - bb[0])
gw, gh = int((bb[2] - bb[0]) * olc), int((bb[3] - bb[1]) * olc)
cx_, alt_ = 520, H - 2


def yerles(m):
    m = m.resize((gw, gh), Image.LANCZOS)
    t = Image.new("L", (W, H)); t.paste(m, (int(cx_ - gw / 2), alt_ - gh))
    return t.point(lambda v: 255 if v > 110 else 0)


K = [yerles(m) for m in kisi]
# ince ayar (kullanici 19 Eki: "A olsun, son ince ayarlari yap"): siluetin arkasi REF-056'daki gibi sade ve parlak ->
# kume cevresinde arka plan hafif bulanik + mor-pembe isik halesi (galaksi parlamasinin bizdeki karsiligi)
bolge = Image.new("L", (W, H)); ImageDraw.Draw(bolge).ellipse((cx_ - 380, 150, cx_ + 200, H + 160), fill=255)   # sagdaki kapiya tasmaz
bolge = bolge.filter(ImageFilter.GaussianBlur(70))
im = Image.composite(im.filter(ImageFilter.GaussianBlur(5)), im, bolge)
hale = Image.new("L", (W, H)); ImageDraw.Draw(hale).ellipse((cx_ - 300, 190, cx_ + 300, H + 120), fill=255)
hale = hale.filter(ImageFilter.GaussianBlur(90))
im.alpha_composite(Image.merge("RGBA", [Image.new("L", (W, H), c) for c in (200, 90, 255)] + [hale.point(lambda v: int(v * 0.42))]))
birlesik = ImageChops.lighter(ImageChops.lighter(K[0], K[1]), K[2]).filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.MinFilter(3))
dis = birlesik.filter(ImageFilter.MaxFilter(KON))
isilti = dis.filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.GaussianBlur(18))
im.alpha_composite(Image.merge("RGBA", [Image.new("L", (W, H), c) for c in (255, 220, 255)] + [isilti.point(lambda v: int(v * 0.55))]))
im.alpha_composite(Image.merge("RGBA", [Image.new("L", (W, H), 255)] * 3 + [dis]))
for j in (1, 0, 2):                                    # ortadaki arkada, yanlar onde (kollari ortadakinin onunden gecer)
    hat = K[j].filter(ImageFilter.MaxFilter(7))
    im.alpha_composite(Image.merge("RGBA", [Image.new("L", (W, H), 255)] * 3 + [hat]))
    im.alpha_composite(Image.merge("RGBA", [Image.new("L", (W, H), c) for c in (6, 4, 14)] + [K[j].filter(ImageFilter.GaussianBlur(0.6))]))
print("grup kutusu", birlesik.getbbox(), "baslik alti", baslik_alt)

# ---------------------------------------------------------------- 6) baslik + HALLOWEEN etiketi (REF-056 "Full Body" yeri: sag ust, egik)
im.alpha_composite(yz, (int(W / 2 - yz.width / 2), by))
yazi_m = Image.new("L", (W, H)); yazi_m.paste(yz.getchannel("A"), (int(W / 2 - yz.width / 2), by))
hw = parlak_yazi("HALLOWEEN", yfont(64), gecis(9, (255, 150, 40), (190, 110, 255)), kontur=8, derinlik=9, dis=(50, 10, 70),
                 parlama=(255, 170, 90), zipla=3, don=3, aralik=4)
hw = hw.rotate(-14, Image.BICUBIC, expand=True)
_hx = min(W - 8 - hw.width, int(1060 - hw.width / 2)); _hy = int(int(ac[1]) - 95 - hw.height / 2)
yazi_m.paste(hw.getchannel("A"), (_hx, _hy), hw.getchannel("A"))
im.alpha_composite(hw, (min(W - 8 - hw.width, int(1060 - hw.width / 2)), int(int(ac[1]) - 95 - hw.height / 2)))   # kapinin ust-saginda (REF "Full Body" yeri), kadraja sigar
# doygunluk referansa yaklasir (0,63), sicaklik mor-mavi ile dengelenir (deneme 2 sicak 0,20 / ref 0,08)
# ince ayar 1 olcumu: mor tonlama siluetin siyahini da aciyordu (siyah 0,000) -> yalniz ARKA PLANA; siluet + kontur + yazilar korunur
ham = im.convert("RGB")
son = ImageEnhance.Color(ham).enhance(1.18)
son = Image.blend(son, ImageChops.screen(son, Image.new("RGB", (W, H), (70, 40, 160))), 0.18)
kart_m = Image.new("L", (W, H)); ImageDraw.Draw(kart_m).rectangle((PX - 4, PY - 4, PX + pw + 4, PY + ph + 4), fill=255)
koru = ImageChops.lighter(ImageChops.lighter(dis, yazi_m), kart_m).filter(ImageFilter.MaxFilter(3))   # kart + kucuk siluet de korunur
Image.composite(ham, son, koru).save(a.cikti, quality=93)
print(a.cikti, os.path.getsize(a.cikti) // 1024, "KB")
