"""HUMAN TETRIS 19 kapagi (REF-070 TetrisBounce, SOLO Easy Beginner) - 1280x720. kapak-coop-18.py'den (baloncuk baslik, egik etiket).

    python kapak-tek-19.py --poz easy-bird-dog --arka varlik-19-kapak-1 --poz-klasor varlik-19-poz-1 --cikti A.jpg

REF-070 kapagi (olculdu 5 Kas 2026: doygunluk 0,582, parlaklik 0,756, renklilik 0,509, siyah 0,095, beyaz 0,109;
siluet yukseklik %53,8, alan %8,3 - kapak-siluet-olc.py): ustte tum genislikte baloncuk HUMAN TETRIS, solda egik beyaz "EASY",
sagda egik beyaz "1 PLAYER" (mor kontur + isilti); neon yildiz koprusu (Blender kapak modu, varlik-yildizkopru.py), ortada kapida
YANARDONER PASTEL HOLOGRAM kart ve kartta ayni pozun siyah silueti; on planda dev duz simsiyah siluet + kalin beyaz kontur
(referans: bird-dog, yatay ve genis); sag altta kirmizi-sari patlama icinde "NEW" rozeti.
Kural (5 Kas 2026): siluet referanstaki boyutta, kucuk degil -> yukseklik ve alan >= referans (kapak-siluet-olc.py).
Alinmaz (telif): anime kiz karakterler.
Cizim sirasi: arka plan -> kapidaki kart -> etiketler -> siluet -> NEW -> baslik.
"""
import argparse, json, math, os
import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont, ImageEnhance

KOK = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
TP = os.path.join(KOK, "03-motor", "tetris-pvp")
p = argparse.ArgumentParser()
p.add_argument("--poz", required=True); p.add_argument("--ayna", action="store_true")
p.add_argument("--arka", default="varlik-19-kapak-1"); p.add_argument("--poz-klasor", default="varlik-19-poz-1")
p.add_argument("--gen", type=float, default=0.70, help="siluet genisligi (kadraj orani), yatay pozda")
p.add_argument("--boy", type=float, default=470, help="siluet yuksekligi (px), dik pozda")
p.add_argument("--x", type=float, default=0.5)
p.add_argument("--renk", type=float, default=1.0); p.add_argument("--parlak", type=float, default=1.0)   # yalniz hafif genel ayar
p.add_argument("--cikti", required=True)
a = p.parse_args()
W, H = 1280, 720
FONT = os.path.join(KOK, "05-kapak", "fontlar", "Fredoka.ttf")


def font(boy):
    f = ImageFont.truetype(FONT, boy)
    try:
        f.set_variation_by_name("Bold")
    except Exception:
        pass
    return f


def klasor(ad):
    v = os.path.join(TP, ad, "tetris-varlik")
    return v if os.path.isdir(v) else os.path.join(TP, ad)


V = klasor(a.arka)
im = Image.open(os.path.join(V, "kapak-gok.png")).convert("RGBA").resize((W, H), Image.LANCZOS)
im.alpha_composite(Image.open(os.path.join(V, "kapak-serit.png")).convert("RGBA").resize((W, H), Image.LANCZOS))
Y = json.load(open(os.path.join(V, "yerlesim.json"), encoding="utf-8"))
ac = Y["kapak-aciklik_p1"]; s = W / 1920
x0, y0, x1, y1 = ac[0] * s, ac[1] * s, ac[2] * s, ac[3] * s

maske = Image.open(os.path.join(klasor(a.poz_klasor), "poz", a.poz + ".png")).convert("RGBA")
if a.ayna:
    maske = maske.transpose(Image.FLIP_LEFT_RIGHT)
maske = maske.crop(maske.getchannel("A").getbbox())
ma = maske.getchannel("A")


def hologram(w, h):
    """REF-070 kart: yanardoner pastel (pembe-lila-camgobegi-sari) capraz degrade + yumusak parilti, yuvarlak kose"""
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    t = (xx / w * 0.65 + yy / h * 0.35)
    cs = np.array([[255, 190, 235], [210, 190, 255], [170, 240, 255], [255, 245, 200], [255, 190, 235]], np.float32)
    pos = np.linspace(0, 1, len(cs)); rgb = np.zeros((h, w, 3), np.float32)
    for ch in range(3):
        rgb[..., ch] = np.interp(t + 0.08 * np.sin(yy / h * 9 + xx / w * 4), pos, cs[:, ch])
    k = Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8)).convert("RGBA")
    d = ImageDraw.Draw(k); rnd = np.random.default_rng(19)
    for _ in range(int(w * h / 900)):
        px, py = rnd.uniform(0, w), rnd.uniform(0, h); r = rnd.choice((1, 1, 2))
        d.ellipse((px - r, py - r, px + r, py + r), fill=(255, 255, 255, 220))
    m = Image.new("L", (w, h), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), radius=max(6, w // 14), fill=255)
    k.putalpha(m)
    return k


# kapidaki duvar: hologram kart, ortasinda ayni pozun SIYAH silueti
pw, ph = int(x1 - x0), int(y1 - y0)
kart = hologram(pw, ph)
mh = int(ph * 0.78); mw = int(mh * maske.width / maske.height)
if mw > pw * 0.84:
    mw = int(pw * 0.84); mh = int(mw * maske.height / maske.width)
kart.paste((0, 0, 0, 255), ((pw - mw) // 2, int(ph * 0.92) - mh), ma.resize((mw, mh), Image.LANCZOS))
im.alpha_composite(kart, (int(x0), int(y0)))
if a.renk != 1.0:
    im = ImageEnhance.Color(im).enhance(a.renk)
if a.parlak != 1.0:
    im = ImageEnhance.Brightness(im).enhance(a.parlak)


def baloncuk(metin, cx, cy, boy, renkler, kontur="#4a1f86", hedef=None):
    """baloncuk baslik: yatay cok renkli degrade, kalin mor dis kontur, ustte cam yansimasi, beyaz ince ic hat (kapak-coop-18 ile ayni dil)"""
    S = 2; fS = font(boy * S)
    bx = fS.getbbox(metin); tw, th = bx[2] - bx[0], bx[3] - bx[1]
    pad = int(boy * S * 0.25); w, h = tw + 2 * pad, th + 2 * pad
    m = Image.new("L", (w, h), 0); ImageDraw.Draw(m).text((pad - bx[0], pad - bx[1]), metin, font=fS, fill=255)
    dis = Image.new("L", (w, h), 0); ImageDraw.Draw(dis).text((pad - bx[0], pad - bx[1]), metin, font=fS, fill=255, stroke_width=int(boy * S * 0.075), stroke_fill=255)
    ic = Image.new("L", (w, h), 0); ImageDraw.Draw(ic).text((pad - bx[0], pad - bx[1]), metin, font=fS, fill=255, stroke_width=int(boy * S * 0.02), stroke_fill=255)
    xs = np.linspace(0, 1, w)[None, :].repeat(h, 0); cs = [np.array([int(c[i:i + 2], 16) for i in (1, 3, 5)], np.float32) for c in renkler]
    pos = np.linspace(0, 1, len(cs)); rgb = np.zeros((h, w, 3), np.float32)
    for ch in range(3):
        rgb[..., ch] = np.interp(xs, pos, [c[ch] for c in cs])
    yy = np.linspace(0, 1, h)[:, None]
    rgb = rgb * (0.9 + 0.25 * (1 - yy))[..., None].clip(0, 1.15)
    dol = Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8)).convert("RGBA")
    K = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    K.paste(Image.new("RGBA", (w, h), (40, 10, 80, 160)), (int(boy * S * 0.03), int(boy * S * 0.05)), dis)
    K.paste(Image.new("RGBA", (w, h), kontur), (0, 0), dis)
    K.paste(Image.new("RGBA", (w, h), "#ffffff"), (0, 0), ic)
    K.paste(dol, (0, 0), m)
    yans = Image.new("L", (w, h), 0); ImageDraw.Draw(yans).rectangle((0, pad + int(th * 0.06), w, pad + int(th * 0.38)), fill=120)
    yans = ImageChops.multiply(yans, m.filter(ImageFilter.MinFilter(int(boy * S * 0.05) | 1))).filter(ImageFilter.GaussianBlur(boy * S * 0.012))
    K.paste(Image.new("RGBA", (w, h), "#ffffff"), (0, 0), yans)
    K = K.resize((w // S, h // S), Image.LANCZOS)
    if hedef and K.width > hedef:
        K = K.resize((hedef, int(K.height * hedef / K.width)), Image.LANCZOS)
    im.alpha_composite(K, (int(cx - K.width / 2), int(cy - K.height / 2)))
    return K.width


def etiket(metin, cx, cy, boy, aci):
    """REF-070 yan etiketi: beyaz kalin yazi, koyu mor kontur + mor isilti (REF-069'daki kivilcim yok)"""
    S = 2; f = font(boy * S)
    k = Image.new("RGBA", (int(boy * S * len(metin) * 0.75) + 200, boy * S * 2), (0, 0, 0, 0)); d = ImageDraw.Draw(k)
    c = (k.width / 2, k.height / 2)
    d.text(c, metin, font=f, anchor="mm", fill="#ffffff", stroke_width=int(boy * S * 0.11), stroke_fill="#5a2aa8")
    d.text(c, metin, font=f, anchor="mm", fill="#ffffff")
    k = k.resize((k.width // S, k.height // S), Image.LANCZOS).rotate(aci, resample=Image.BICUBIC, expand=True)
    g = Image.new("RGBA", k.size, "#c86aff"); g.putalpha(k.getchannel("A").filter(ImageFilter.GaussianBlur(boy * 0.16)))
    for q in (g, k):
        im.alpha_composite(q, (int(cx - k.width / 2), int(cy - k.height / 2)))


def yeni(cx, cy, r):
    """REF-070 sag alt rozeti: sari-turuncu cizgi roman patlamasi, kirmizi kalin 'NEW' (beyaz-sari kontur), cevrede kivilcim"""
    S = 3; R = r * S
    k = Image.new("RGBA", (int(R * 2.8), int(R * 2.4)), (0, 0, 0, 0)); d = ImageDraw.Draw(k)
    ox, oy = k.width / 2, k.height / 2
    for (rr, ic, renk) in ((1.0, 0.72, "#ff7a1a"), (0.9, 0.7, "#ffd21a")):
        pts = []
        for i in range(28):
            t = i / 28 * 2 * math.pi; q = rr if i % 2 == 0 else rr * ic
            pts.append((ox + math.cos(t) * R * 1.25 * q, oy + math.sin(t) * R * 0.95 * q))
        d.polygon(pts, fill=renk)
    for _ in range(80):   # nokta deseni (cizgi roman)
        t = np.random.uniform(0, 2 * math.pi); q = np.random.uniform(0.3, 0.7)
        px, py = ox + math.cos(t) * R * 1.2 * q, oy + math.sin(t) * R * 0.9 * q; rr = S * 2.5
        d.ellipse((px - rr, py - rr, px + rr, py + rr), fill=(255, 150, 30, 160))
    f = font(int(R * 0.72))
    d.text((ox, oy), "NEW", font=f, anchor="mm", fill="#fff2a0", stroke_width=int(R * 0.1), stroke_fill="#ffffff")
    d.text((ox, oy), "NEW", font=f, anchor="mm", fill="#ff2a1a", stroke_width=int(R * 0.045), stroke_fill="#ffe24a")
    d.text((ox - R * 0.02, oy - R * 0.05), "NEW", font=f, anchor="mm", fill="#ff4a2a")
    k = k.resize((k.width // S, k.height // S), Image.LANCZOS).rotate(-8, resample=Image.BICUBIC, expand=True)
    g = Image.new("RGBA", k.size, "#ff9a2a"); g.putalpha(k.getchannel("A").filter(ImageFilter.GaussianBlur(r * 0.14)))
    for q in (g, k):
        im.alpha_composite(q, (int(cx - k.width / 2), int(cy - k.height / 2)))


etiket("EASY", 150, 300, 78, 18)
etiket("1 PLAYER", 1110, 330, 70, -16)

# siluet: duz simsiyah + kalin beyaz dis kontur; yatay poz genislikten, dik poz yukseklikten olculenir; basliga degmez
ust_sinir = 180
oran = maske.width / maske.height
if oran >= 1.2:
    sw = int(W * a.gen); sb = int(sw / oran)
else:
    sb = int(a.boy); sw = int(sb * oran)
sb = min(sb, H - 12 - ust_sinir); sw = int(sb * oran)
sa = ma.resize((sw, sb), Image.LANCZOS)
sx, sy = int(max(10, min(W - sw - 10, W * a.x - sw / 2))), H - sb - 12
kont = Image.new("L", (sw + 60, sb + 60), 0); kont.paste(sa, (30, 30))
im.paste((255, 255, 255, 255), (sx - 30, sy - 30), kont.filter(ImageFilter.MaxFilter(17)))
im.paste((0, 0, 0, 255), (sx, sy), sa)
print(a.cikti, "siluet kutu", sx, sy, sx + sw, sy + sb, "kapi", int(x0), int(y0), int(x1), int(y1))

yeni(1135, 600, 92)

# baslik en onde: HUMAN camgobegi->pembe, TETRIS pembe->sari->camgobegi (REF-070 harf renkleri)
baloncuk("HUMAN", 345, 90, 150, ["#8af0ff", "#5ac8ff", "#c88aff", "#ff6ad0"], hedef=560)
baloncuk("TETRIS", 935, 90, 150, ["#ff6ac8", "#ff9ab0", "#ffe24a", "#9ae86a", "#5ad8ff"], hedef=560)

im.convert("RGB").save(a.cikti, quality=95)
print("->", a.cikti)
