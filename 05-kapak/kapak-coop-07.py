"""HUMAN TETRIS 7 kapagi (REF-058 duzeni, 2 oyuncu CO-OP) - 1280x720.

    python kapak-coop-07.py --poz duo-lunge-back-hand-link --cikti HUMAN-TETRIS-07-KAPAK-A.jpg

REF-058 kapagi (olculdu: 17-GLOWMOTION-X2-4-KAPAK-OLCUM.md, doygunluk 0,712 / parlaklik 0,732 / baslik bandi 0,803): ustte tam
genislik baloncuk HUMAN TETRIS; arkada videonun synthwave gun batimi sahnesi, kirmizi kafes kapi kadrajin sag-ortasinda, kapidaki
camgobegi panelde AYNI pozun kucuk siyah silueti; onde ortada TEK dev ikili siluet (iki kisi birbirine deger) duz simsiyah + kalin
beyaz dis kontur + kisiler arasi ince beyaz hat; solda egik el yazisi "warm - up", sagda uc okla "couple", sag altta NEW! patlamasi,
siluetin basinin yaninda kucuk neon kalp. Kullanici 23 Eki 2026: "TETRIS MODE" yok, yalniz HUMAN TETRIS.
Cizim sirasi (TALIMATLAR §14c): etiketler -> siluet -> baslik. Siluet maskeleri: varlik-cadi.py --yalniz kapakgrup (Mixamo, Actions);
sahne: varlik-gunbatimi.py --yalniz kapak (kamera sola + one kayik). Baslik harf yontemi kapak-pvp-06.py baloncuk_baslik.
"""
import argparse, json, os
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont, ImageEnhance

KOK = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
p = argparse.ArgumentParser()
p.add_argument("--poz", required=True)
p.add_argument("--sahne", default=os.path.join(KOK, "03-motor", "tetris-pvp", "varlik-07-kapak"))
p.add_argument("--maske", default=os.path.join(KOK, "03-motor", "tetris-pvp", "varlik-07-kapakgrup"))
p.add_argument("--boy", type=float, default=526); p.add_argument("--gen", type=float, default=640)   # boy 526: siluet tepesi baslik altinin ALTINDA (§14c)
p.add_argument("--x", type=float, default=560)
p.add_argument("--dy", type=int, default=112)
p.add_argument("--cikti", required=True)
a = p.parse_args()
W, H = 1280, 720
FRED = os.path.join(KOK, "05-kapak", "fontlar", "Fredoka.ttf")

# baloncuk baslik: kapak-pvp-06.py'deki onayli fonksiyonlar (dosya argparse ile kostugu icin yalniz bu kisim alinir)
_k = open(os.path.join(KOK, "05-kapak", "kapak-pvp-06.py"), encoding="utf-8").read()
_g = {"os": os, "Image": Image, "ImageChops": ImageChops, "ImageDraw": ImageDraw, "ImageFilter": ImageFilter, "ImageFont": ImageFont, "KOK": KOK}
exec(compile(_k[_k.index("def baloncuk_kelime"):_k.index("def gecis")], "kapak-pvp-06.py", "exec"), _g)
baloncuk_baslik = _g["baloncuk_baslik"]


def fred(boy):
    f = ImageFont.truetype(FRED, boy); f.set_variation_by_name("Bold"); return f


# ---------------------------------------------------------------- arka plan: videonun sahnesi (kapak kamerasi)
im = Image.open(os.path.join(a.sahne, "kapak-gok.png")).convert("RGBA")
im.alpha_composite(Image.open(os.path.join(a.sahne, "kapak-serit.png")).convert("RGBA"))
Y = json.load(open(os.path.join(a.sahne, "yerlesim.json"), encoding="utf-8"))
sx = im.width / W
im = im.resize((W, H), Image.LANCZOS)
x0, y0, x1, y1 = (v / sx for v in Y["kapak-aciklik_p1"])
pw = x1 - x0; ph = pw * 9 / 16
if ph > y1 - y0:
    ph = y1 - y0; pw = ph * 16 / 9
px, py = x0 + (x1 - x0 - pw) / 2, y1 - ph
pan = Image.open(os.path.join(KOK, "03-motor", "tetris-pvp", "varlik-07", "panel-a.png")).convert("RGBA").resize((int(pw), int(ph)), Image.LANCZOS)
im.alpha_composite(pan, (int(px), int(py)))
# kapidaki panelde AYNI pozun kucuk siyah silueti (REF-058 kapagi)
kucuk = Image.open(os.path.join(a.maske, "kapak-grup-%s.png" % a.poz)).getchannel("A").resize((int(pw), int(ph)), Image.LANCZOS)
im.alpha_composite(Image.merge("RGBA", [Image.new("L", kucuk.size, c) for c in (8, 4, 20)] + [kucuk.point(lambda v: 255 if v > 110 else 0)]), (int(px), int(py)))
# deneme 1: kapi acikligi y 173-399 (REF-058 275-515) -> kapi basligin arkasina girdi, gunes gorunmedi. Ayni boyut, arka plan
# --dy kadar asagi kayar; acilan ust bant gogun en ust satirlariyla dolar (baslik zaten orayi kaplar)
if a.dy:
    ust = im.crop((0, 0, W, 24)).resize((W, a.dy + 24), Image.LANCZOS)
    yeni = Image.new("RGBA", (W, H)); yeni.alpha_composite(ust); yeni.alpha_composite(im.crop((0, 0, W, H - a.dy)), (0, a.dy)); im = yeni
# olcum deneme 1 (olcum-deneme1.md): parlaklik 0,64 / ref 0,73, renklilik 0,47 / 0,67, sicak 0,10 / 0,19 -> canlandir + sicak
# magenta-turuncu gun batimi tonu (REF-058 baskin #e60ad3); siluetler sonra cizildigi icin yutulmaz
im = ImageEnhance.Color(im).enhance(1.55)
im = ImageEnhance.Brightness(im).enhance(1.12)
ton = Image.new("RGBA", (W, H)); dt_ = ImageDraw.Draw(ton)
for yy in range(H):
    q = yy / H
    dt_.line([(0, yy), (W, yy)], fill=(255, int(60 + 90 * q), int(200 - 120 * q), int(46 + 20 * q)))
im.alpha_composite(ton)


# ---------------------------------------------------------------- etiketler (siluetin ARKASINDA kalir)
def egik_yazi(metin, boy, aci, dolgu=(255, 255, 255), kontur=(255, 90, 200), kal=10):
    f = fred(boy); d0 = ImageDraw.Draw(Image.new("L", (10, 10)))
    w = int(d0.textlength(metin, font=f)) + 4 * kal + 40; h = int(boy * 1.5) + 4 * kal
    t = Image.new("RGBA", (w, h)); d = ImageDraw.Draw(t)
    d.text((2 * kal + 20, kal), metin, font=f, fill=kontur + (255,), stroke_width=kal, stroke_fill=kontur + (255,))
    d.text((2 * kal + 20, kal), metin, font=f, fill=dolgu + (255,))
    g = t.getchannel("A").filter(ImageFilter.MaxFilter(7)).filter(ImageFilter.GaussianBlur(10))
    gl = Image.merge("RGBA", [Image.new("L", t.size, c) for c in kontur] + [g.point(lambda v: int(v * 0.8))]); gl.alpha_composite(t)
    return gl.rotate(aci, Image.BICUBIC, expand=True)


def koy(t, merkez):
    im.alpha_composite(t, (int(merkez[0] - t.width / 2), int(merkez[1] - t.height / 2)))


koy(egik_yazi("warm - up", 74, 11), (215, 455))
d = ImageDraw.Draw(im)
for i, (dx, dy) in enumerate(((-150, -80), (-175, -40), (-140, -118))):          # "warm-up" yanindaki vurgu cizgileri
    d.line([(215 + dx, 455 + dy), (215 + dx + 30, 455 + dy + 18 - i * 6)], fill=(255, 255, 255), width=6)
koy(egik_yazi("couple", 70, -9), (1140, 405))
for i, (ox, renk) in enumerate(((-55, (120, 230, 255)), (0, (255, 255, 255)), (55, (255, 110, 210)))):   # uc ok, "couple"a iner
    ax, ay = 1140 + ox, 300
    d.line([(ax - ox * 0.4, ay - 52), (ax, ay)], fill=renk, width=6)
    d.line([(ax - 14, ay - 16), (ax, ay), (ax + 6, ay - 21)], fill=renk, width=6)


def new_rozet(merkez, r=105):
    import math
    k = Image.new("RGBA", (int(r * 2.8), int(r * 2.8))); dk = ImageDraw.Draw(k); c = (k.width / 2, k.height / 2)
    for olc, renk in ((1.0, (230, 30, 40)), (0.74, (255, 205, 40))):
        pts = []
        for i in range(32):
            uz = r * olc * (1.28 if i % 2 == 0 else 0.92)
            an = i * math.pi / 16
            pts.append((c[0] + math.cos(an) * uz, c[1] + math.sin(an) * uz * 0.8))
        dk.polygon(pts, fill=renk, outline=(255, 255, 255), width=5)
    for i in range(10):                                           # patlama cizgileri
        an = i * math.pi / 5 + 0.3
        dk.line([(c[0] + math.cos(an) * r * 1.38, c[1] + math.sin(an) * r * 1.12), (c[0] + math.cos(an) * r * 1.62, c[1] + math.sin(an) * r * 1.3)], fill=(255, 220, 60), width=5)
    f = fred(int(r * 0.78))
    t = Image.new("RGBA", k.size); dt = ImageDraw.Draw(t)
    dt.text(c, "NEW!", font=f, anchor="mm", fill=(255, 255, 255), stroke_width=9, stroke_fill=(30, 60, 200))
    k.alpha_composite(t.rotate(-8, Image.BICUBIC, center=c))
    koy(k, merkez)


new_rozet((1095, 598))


# ---------------------------------------------------------------- ikili siluet (ortada dev, duz siyah + beyaz kontur + kisiler arasi ince hat)
def maske(ad):
    return Image.open(os.path.join(a.maske, ad)).getchannel("A")


tum = maske("kapak-grup-%s.png" % a.poz)
kisi = [maske("kapak-grup-%s-%d.png" % (a.poz, j)) for j in range(2)]
bb = tum.getbbox()
s = min(a.boy / (bb[3] - bb[1]), a.gen / (bb[2] - bb[0]))


def olcekle(m):
    m = m.crop(bb); m = m.resize((int(m.width * s), int(m.height * s)), Image.LANCZOS)
    t = Image.new("L", (W, H)); t.paste(m, (int(a.x - m.width / 2), int(712 - m.height)))
    return t.point(lambda v: 255 if v > 110 else 0)


mk = olcekle(tum); k0, k1 = (olcekle(m) for m in kisi)
mk = mk.filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.MinFilter(3))
KONTUR = 21
kontur = mk.filter(ImageFilter.MaxFilter(KONTUR))
isilti = kontur.filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.GaussianBlur(16))
im.alpha_composite(Image.merge("RGBA", [Image.new("L", (W, H), c) for c in (255, 150, 230)] + [isilti.point(lambda v: int(v * 0.6))]))
im.alpha_composite(Image.merge("RGBA", [Image.new("L", (W, H), 255)] * 3 + [kontur]))
im.alpha_composite(Image.merge("RGBA", [Image.new("L", (W, H), c) for c in (6, 4, 14)] + [mk.filter(ImageFilter.GaussianBlur(0.7))]))
# kisiler arasi ince beyaz hat: iki kisinin birbirine degdigi / ustune bindigi kenar (dis konturun icinde kalan kisim)
kenar = ImageChops.subtract(k1.filter(ImageFilter.MaxFilter(5)), k1.filter(ImageFilter.MinFilter(3)))
kenar = ImageChops.multiply(kenar, ImageChops.multiply(k0.filter(ImageFilter.MaxFilter(3)), mk.filter(ImageFilter.MinFilter(9))))
im.alpha_composite(Image.merge("RGBA", [Image.new("L", (W, H), 255)] * 3 + [kenar.filter(ImageFilter.GaussianBlur(0.6))]))
# basin yaninda kucuk neon kalp (REF-058)
ub = mk.getbbox(); hx, hy = ub[0] + 40, ub[1] + 60
dh = ImageDraw.Draw(im)
dh.polygon([(hx, hy + 18), (hx - 22, hy - 2), (hx - 18, hy - 16), (hx - 8, hy - 18), (hx, hy - 8), (hx + 8, hy - 18), (hx + 18, hy - 16), (hx + 22, hy - 2)],
           outline=(110, 240, 255), width=5)

# ---------------------------------------------------------------- baslik (en ustte, siluet basliga degmez)
# deneme 2: kelimeler arasinda isilti payi kadar bosluk kaldi, baslik genislige takilip kuculdu -> isiltiler ust uste biner (REF-058'de
# iki kelime neredeyse bitisik)
_bk = _g["baloncuk_kelime"]
k1 = _bk("HUMAN", 196, [(25, 85, 255), (15, 190, 255), (55, 255, 185)])
k2 = _bk("TETRIS", 196, [(255, 35, 205), (255, 105, 95), (255, 238, 35)], kontur_renk=(110, 20, 120), isilti=(255, 210, 245))
ARA = -46
yz = Image.new("RGBA", (k1.width + k2.width + ARA, max(k1.height, k2.height)))
yz.alpha_composite(k2, (k1.width + ARA, (yz.height - k2.height) // 2)); yz.alpha_composite(k1, (0, (yz.height - k1.height) // 2))
if yz.width > 1250:
    yz = yz.resize((1250, int(yz.height * 1250 / yz.width)), Image.LANCZOS)
by = int(92 - yz.height / 2)
im.alpha_composite(yz, (int(W / 2 - yz.width / 2), by))
baslik_alt = by + yz.getchannel("A").point(lambda v: 255 if v > 200 else 0).getbbox()[3]
print("siluet kutusu", mk.getbbox(), "baslik alti", baslik_alt, "UST USTE" if mk.getbbox()[1] < baslik_alt else "ok")
im.convert("RGB").save(a.cikti, quality=93)
print(a.cikti)
