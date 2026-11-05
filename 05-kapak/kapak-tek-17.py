"""HUMAN TETRIS 17 kapagi (REF-068 TetrisBounce, SOLO) - 1280x720. kapak-tek-12.py'den (tek oyuncu kapak dili).

    python kapak-tek-17.py --poz nebula-airplane-wings --arka varlik-17-kapak-0 --cikti A.jpg

REF-068 kapagi (olculdu: 26-TETRISBOUNCE-02-KAPAK-OLCUM.md; doygunluk 0,505, parlaklik 0,616, renklilik 0,339, beyaz 0,197):
ustte tam genislikte BEYAZ kalin HUMAN TETRIS, arkasinda saga-asagi kayan pembe-mercan katman kopyalari (golge yerine) + pembe isilti;
galaksi gogu + neon izgara (Blender kapak modu), sagda truss kapi ve kapida pembe-sari degrade duvar (ayni pozun oyugu);
ortada buyuk DUZ SIMSIYAH siluet + kalin beyaz kontur + beyaz hale; sagda beyaz egik "SOLO", solda beyaz egik etiket, sol altta pembe neon oyun kolu.
Referanstaki "-400 KCAL" (5 dk icin gercek degil) ve "BEST CHOICE" rozeti (gercek degil) ALINMAZ; sol etiket gercek bilgi: "24 WALLS".
Cizim sirasi: arka plan -> kapidaki duvar -> etiketler / oyun kolu -> siluet -> baslik.
"""
import argparse, json, math, os
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont, ImageEnhance

KOK = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
TP = os.path.join(KOK, "03-motor", "tetris-pvp")
p = argparse.ArgumentParser()
p.add_argument("--poz", required=True); p.add_argument("--ayna", action="store_true")
p.add_argument("--arka", default="varlik-17-kapak-0")
p.add_argument("--boy", type=float, default=600); p.add_argument("--x", type=float, default=0.44)
p.add_argument("--renk", type=float, default=1.0); p.add_argument("--parlak", type=float, default=1.0)   # yalniz hafif genel ayar
p.add_argument("--parilti", type=float, default=0.6)
p.add_argument("--etiket", default="24 WALLS")
p.add_argument("--cikti", required=True)
a = p.parse_args()
W, H = 1280, 720
FFONT = os.path.join(KOK, "05-kapak", "fontlar", "Fredoka.ttf")


def font(boy):
    f = ImageFont.truetype(FFONT, boy)
    try:
        f.set_variation_by_axes([700, 100][:len(f.get_variation_axes())])   # Fredoka degisken: en kalin
    except Exception:
        pass
    return f


V = os.path.join(TP, a.arka, "tetris-varlik")
im = Image.open(os.path.join(V, "kapak-gok.png")).convert("RGBA").resize((W, H), Image.LANCZOS)
im.alpha_composite(Image.open(os.path.join(V, "kapak-serit.png")).convert("RGBA").resize((W, H), Image.LANCZOS))
Y = json.load(open(os.path.join(V, "yerlesim.json"), encoding="utf-8"))
ac = Y["kapak-aciklik_p1"]; s = W / 1920
x0, y0, x1, y1 = ac[0] * s, ac[1] * s, ac[2] * s, ac[3] * s
maske = Image.open(os.path.join(TP, "varlik-17", "poz", a.poz + ".png")).convert("RGBA")
if a.ayna:
    maske = maske.transpose(Image.FLIP_LEFT_RIGHT)
ma = maske.getchannel("A")

# neon parlamasi (Blender kapakta glare yok): yalniz parlak neon piksellerden
par = im.convert("RGB").point(lambda v: 0 if v < 150 else v).filter(ImageFilter.GaussianBlur(14))
im = ImageChops.add(im.convert("RGB"), par.point(lambda v: int(v * a.parilti))).convert("RGBA")

# kapidaki duvar: REF-068 pembe (sol-alt) -> sari (sag-ust) degrade, ortasinda ayni pozun oyugu (oyuktan gok gorunur)
pw, ph = int(x1 - x0), int(y1 - y0)
grad = Image.linear_gradient("L").rotate(90).resize((pw, ph))
panel = Image.composite(Image.new("RGBA", (pw, ph), "#ffe86a"), Image.new("RGBA", (pw, ph), "#ff8ae6"), grad)
mh = int(ph * 0.82); mw = int(mh * maske.width / maske.height)
if mw > pw * 0.8:
    mw = int(pw * 0.8); mh = int(mw * maske.height / maske.width)
delik = Image.new("L", (pw, ph), 0); delik.paste(ma.resize((mw, mh), Image.LANCZOS), ((pw - mw) // 2, int(ph * 0.95) - mh))
panel.putalpha(Image.eval(delik, lambda v: 255 - v))
im.alpha_composite(panel, (int(x0), int(y0)))
if a.renk != 1.0:
    im = ImageEnhance.Color(im).enhance(a.renk)
if a.parlak != 1.0:
    im = ImageEnhance.Brightness(im).enhance(a.parlak)


def egik_yazi(metin, cx, cy, boy, aci, renk="#ffffff", isilti="#ff5fd2"):
    """REF-068 yan etiketleri: beyaz kalin, hafif egik, pembe isilti"""
    f = font(boy)
    k = Image.new("RGBA", (int(boy * len(metin) * 0.9) + 80, boy * 2), (0, 0, 0, 0))
    ImageDraw.Draw(k).text((k.width / 2, k.height / 2), metin, font=f, fill=renk, anchor="mm")
    k = k.rotate(aci, resample=Image.BICUBIC, expand=True)
    g = Image.new("RGBA", k.size, isilti); g.putalpha(k.getchannel("A").filter(ImageFilter.GaussianBlur(boy * 0.18)))
    for q in (g, k):
        im.alpha_composite(q, (int(cx - k.width / 2), int(cy - k.height / 2)))


def oyun_kolu(cx, cy, w):
    """REF-068 sol alt: pembe neon cizgi oyun kolu (genel simge, marka yok)"""
    S = 3; h = int(w * 0.62)
    k = Image.new("RGBA", ((w + 60) * S, (h + 60) * S), (0, 0, 0, 0)); d = ImageDraw.Draw(k); o = 30 * S; lw = int(w * 0.045 * S)
    r = h * S * 0.42
    d.rounded_rectangle((o, o, o + w * S, o + h * 0.62 * S), radius=int(r * 0.6), outline="#ff4fc8", width=lw)
    for sx in (0.22, 0.78):
        d.ellipse((o + (sx * w - h * 0.24) * S, o + h * 0.38 * S, o + (sx * w + h * 0.24) * S, o + h * 0.98 * S), outline="#ff4fc8", width=lw)
    c1, c2 = o + w * 0.25 * S, o + h * 0.31 * S; u = h * 0.12 * S
    d.line((c1 - u, c2, c1 + u, c2), fill="#ff4fc8", width=lw); d.line((c1, c2 - u, c1, c2 + u), fill="#ff4fc8", width=lw)
    for dx, dy in ((0.72, 0.2), (0.8, 0.31), (0.72, 0.42), (0.64, 0.31)):
        q = h * 0.05 * S; X, Y_ = o + w * dx * S, o + h * dy * S
        d.ellipse((X - q, Y_ - q, X + q, Y_ + q), outline="#ff4fc8", width=int(lw * 0.6))
    k = k.resize((w + 60, h + 60), Image.LANCZOS)
    g = Image.new("RGBA", k.size, "#ff3fbf"); g.putalpha(k.getchannel("A").filter(ImageFilter.GaussianBlur(10)))
    for q in (g, g, k):
        im.alpha_composite(q, (int(cx - k.width / 2), int(cy - k.height / 2)))


egik_yazi(a.etiket, 215, 340, 70, 12)
egik_yazi("SOLO", 1135, 365, 84, -8)
oyun_kolu(200, 575, 270)   # kapak 1: referanstan kucuktu

# siluet: duz simsiyah + kalin beyaz dis kontur + beyaz hale (REF-068), tabani alt kenarda
sb = int(a.boy); sw = int(sb * maske.width / maske.height)
if sw > W * 0.66:
    sw = int(W * 0.66); sb = int(sw * maske.height / maske.width)
sa = ma.resize((sw, sb), Image.LANCZOS)
sx, sy = int(W * a.x - sw / 2), H - sb - 10
kont = Image.new("L", (sw + 60, sb + 60), 0); kont.paste(sa, (30, 30))
hale = kont.filter(ImageFilter.MaxFilter(25)).filter(ImageFilter.GaussianBlur(14))
im.paste((255, 255, 255, 255), (sx - 30, sy - 30), hale.point(lambda v: min(255, int(v * 1.1))))
im.paste((255, 255, 255, 255), (sx - 30, sy - 30), kont.filter(ImageFilter.MaxFilter(15)))
im.paste((0, 0, 0, 255), (sx, sy), sa)

# baslik en onde: beyaz kalin, arkasinda saga-asagi kayan pembe katman kopyalari + pembe isilti
# kapak 1: baslik referanstan kucuk (genisligin %86'si, ref ~%95), katmanlar zayif, beyaz oran 0,10 (ref 0,20)
f = font(168)   # kapak 2: H ve S kenara degiyordu
bas = Image.new("RGBA", (W, 260), (0, 0, 0, 0))
for i, (dx, dy, rk, al) in enumerate(((-34, 22, "#ffb0c8", 140), (-24, 14, "#ff86b4", 190), (-12, 7, "#ff5aa0", 240))):
    k = Image.new("RGBA", bas.size, (0, 0, 0, 0)); ImageDraw.Draw(k).text((W / 2 + dx, 120 + dy), "HUMAN TETRIS", font=f, fill=rk, anchor="mm")
    k.putalpha(k.getchannel("A").point(lambda v: v * al // 255)); bas.alpha_composite(k)
ust = Image.new("RGBA", bas.size, (0, 0, 0, 0)); ImageDraw.Draw(ust).text((W / 2, 120), "HUMAN TETRIS", font=f, fill="#ffffff", anchor="mm")
isk = Image.new("RGBA", bas.size, "#ff3fbf"); isk.putalpha(bas.getchannel("A").filter(ImageFilter.GaussianBlur(22)).point(lambda v: min(255, int(v * 1.5))))
for q in (isk, bas, ust):
    im.alpha_composite(q, (0, -30))

im.convert("RGB").save(a.cikti, quality=95)
print("->", a.cikti)
