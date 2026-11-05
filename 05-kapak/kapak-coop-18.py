"""HUMAN TETRIS 18 kapagi (REF-069 TetrisBounce, 2 oyuncu cift / CO-OP) - 1280x720. kapak-pvp-16.py (baloncuk baslik) + kapak-coop-15.py (kapidaki duvar).

    python kapak-coop-18.py --poz duo-back-to-back-peace-up --arka varlik-18-kapak-03 --grup varlik-18-poz --cikti A.jpg

REF-069 kapagi (olculdu 5 Kas 2026: doygunluk 0,668, parlaklik 0,735, renklilik 0,540, siyah 0,094, beyaz 0,104):
ustte tum genislikte baloncuk HUMAN TETRIS (HUMAN camgobegi->mavi->pembe, TETRIS pembe->sari->camgobegi), solda egik beyaz "COUPLE",
sagda egik beyaz "WARM UP" (pembe kontur, kivilcim cizgileri); neon yildiz sahnesi (Blender kapak modu, varlik-yildizsahne.py), saga kacik kapida
SARI DAMALI duvar karti ve kartta ayni pozun siyah silueti; on planda dev duz simsiyah cift silueti + kalin beyaz kontur; sag altta kalp rozeti.
Referanstaki KUCAKTA TASIMA silueti alinmaz (kullanici karari B: kaldirma yok) -> videodaki yere basan bir cift pozu.
Alinmaz (telif): semsiyeli anime kiz, kanatli sari yaratik ve kalpteki karakterler -> kalp rozeti kendi cizimimiz (iki yildiz).
Cizim sirasi: arka plan -> kapidaki kart -> etiketler -> siluet -> kalp -> baslik.
"""
import argparse, json, math, os
import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont, ImageEnhance

KOK = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
TP = os.path.join(KOK, "03-motor", "tetris-pvp")
p = argparse.ArgumentParser()
p.add_argument("--poz", required=True); p.add_argument("--ayna", action="store_true")
p.add_argument("--arka", default="varlik-18-kapak-03"); p.add_argument("--grup", default="varlik-18-poz")
p.add_argument("--boy", type=float, default=560); p.add_argument("--x", type=float, default=0.40)
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

maske = Image.open(os.path.join(klasor(a.grup), "grup", a.poz + ".png")).convert("RGBA")
if a.ayna:
    maske = maske.transpose(Image.FLIP_LEFT_RIGHT)
maske = maske.crop(maske.getchannel("A").getbbox())
ma = maske.getchannel("A")

# kapidaki duvar: REF-069 sari damali kart, ortasinda ayni pozun SIYAH silueti (referansta kart dolu, siluet siyah)
pw, ph = int(x1 - x0), int(y1 - y0)
kare = max(8, pw // 12)
kart = Image.new("RGBA", (pw, ph), "#ffe04a"); kd = ImageDraw.Draw(kart)
for j in range(0, ph, kare):
    for i in range(0, pw, kare):
        if (i // kare + j // kare) % 2:
            kd.rectangle((i, j, i + kare - 1, j + kare - 1), fill="#fff6c8")
mh = int(ph * 0.82); mw = int(mh * maske.width / maske.height)
if mw > pw * 0.82:
    mw = int(pw * 0.82); mh = int(mw * maske.height / maske.width)
kart.paste((0, 0, 0, 255), ((pw - mw) // 2, int(ph * 0.96) - mh), ma.resize((mw, mh), Image.LANCZOS))
im.alpha_composite(kart, (int(x0), int(y0)))
if a.renk != 1.0:
    im = ImageEnhance.Color(im).enhance(a.renk)
if a.parlak != 1.0:
    im = ImageEnhance.Brightness(im).enhance(a.parlak)


def baloncuk(metin, cx, cy, boy, renkler, kontur="#4a1f86", hedef=None):
    """REF-069 basligi: yatay cok renkli degrade, kalin mor dis kontur, ustte cam yansimasi, beyaz ince ic hat (kapak-pvp-16 ile ayni dil)"""
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
    dol = Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8), "RGB").convert("RGBA")
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
    """REF-069 yan etiketi: beyaz kalin yazi, pembe kontur + pembe isilti, ustunde uc kivilcim cizgisi"""
    S = 2; f = font(boy * S)
    k = Image.new("RGBA", (int(boy * S * len(metin) * 0.75) + 200, boy * S * 3), (0, 0, 0, 0)); d = ImageDraw.Draw(k)
    c = (k.width / 2, k.height * 0.58)
    d.text(c, metin, font=f, anchor="mm", fill="#ffffff", stroke_width=int(boy * S * 0.11), stroke_fill="#ff3fae")
    d.text(c, metin, font=f, anchor="mm", fill="#ffffff")
    bx = d.textbbox(c, metin, font=f, anchor="mm")
    for j, q in enumerate((-0.5, 0.0, 0.5)):                       # kivilcim: yazinin ustunde yelpaze
        ang = math.radians(-90 + q * 70); L = boy * S * 0.32; r0 = boy * S * 0.42
        ox, oy = (bx[0] + bx[2]) / 2 + q * boy * S * 0.9, bx[1] - boy * S * 0.08
        d.line((ox + math.cos(ang) * r0 * 0.2, oy + math.sin(ang) * r0 * 0.2, ox + math.cos(ang) * (r0 * 0.2 + L), oy + math.sin(ang) * (r0 * 0.2 + L)),
               fill="#ffffff", width=int(boy * S * 0.08))
    k = k.resize((k.width // S, k.height // S), Image.LANCZOS).rotate(aci, resample=Image.BICUBIC, expand=True)
    g = Image.new("RGBA", k.size, "#ff3fbf"); g.putalpha(k.getchannel("A").filter(ImageFilter.GaussianBlur(boy * 0.16)))
    for q in (g, k):
        im.alpha_composite(q, (int(cx - k.width / 2), int(cy - k.height / 2)))


def kalp(cx, cy, r):
    """kendi kalp rozetimiz: parlak kirmizi kalp, beyaz kontur, ustte cam yansimasi, iki yildiz (REF-069'daki karakterler yerine)"""
    S = 3; R = r * S
    k = Image.new("RGBA", (int(R * 2.6), int(R * 2.6)), (0, 0, 0, 0)); d = ImageDraw.Draw(k)
    ox, oy = k.width / 2, k.height / 2
    pts = []
    for i in range(120):
        t = i / 120 * 2 * math.pi
        x = 16 * math.sin(t) ** 3; y = 13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)
        pts.append((ox + x / 17 * R, oy - y / 17 * R))
    d.polygon(pts, fill="#ffffff")
    ic = [(ox + (x - ox) * 0.88, oy + (y - oy) * 0.88) for x, y in pts]
    d.polygon(ic, fill="#ff2a5a")
    d.ellipse((ox - R * 0.62, oy - R * 0.62, ox - R * 0.12, oy - R * 0.25), fill=(255, 255, 255, 150))
    for dx, rr, c in ((-0.28, 0.3, "#ffe04a"), (0.3, 0.26, "#4ae8ff")):
        q = []
        for i in range(10):
            t = -math.pi / 2 + i * math.pi / 5; rq = R * rr * (1 if i % 2 == 0 else 0.45)
            q.append((ox + dx * R + math.cos(t) * rq, oy + R * 0.12 + math.sin(t) * rq))
        d.polygon(q, fill=c, outline="#ffffff", width=int(S * 3))
    k = k.resize((k.width // S, k.height // S), Image.LANCZOS)
    g = Image.new("RGBA", k.size, "#ff3f8a"); g.putalpha(k.getchannel("A").filter(ImageFilter.GaussianBlur(r * 0.18)))
    for q in (g, k):
        im.alpha_composite(q, (int(cx - k.width / 2), int(cy - k.height / 2)))


etiket("COUPLE", 205, 300, 74, 10)
etiket("WARM UP", 1100, 290, 66, -10)

# siluet: duz simsiyah + kalin beyaz dis kontur, tabani alt kenarda, basliga degmez
ust_sinir = 175
sb = int(min(a.boy, H - 6 - ust_sinir)); sw = int(sb * maske.width / maske.height)
if sw > W * 0.62:
    sw = int(W * 0.62); sb = int(sw * maske.height / maske.width)
sa = ma.resize((sw, sb), Image.LANCZOS)
sx, sy = int(max(10, min(W - sw - 10, W * a.x - sw / 2))), H - sb - 6
kont = Image.new("L", (sw + 60, sb + 60), 0); kont.paste(sa, (30, 30))
im.paste((255, 255, 255, 255), (sx - 30, sy - 30), kont.filter(ImageFilter.MaxFilter(17)))
im.paste((0, 0, 0, 255), (sx, sy), sa)
print(a.cikti, "siluet kutu", sx, sy, sx + sw, sy + sb, "kapi", int(x0), int(y0), int(x1), int(y1))

kalp(1180, 640, 62)

# baslik en onde: HUMAN camgobegi->mavi->pembe, TETRIS pembe->sari->camgobegi (REF-069 harf renkleri)
baloncuk("HUMAN", 345, 88, 150, ["#9ef4ff", "#5ab8ff", "#8a8cff", "#ff7ad8"], hedef=560)
baloncuk("TETRIS", 935, 88, 150, ["#ff6ad0", "#ff9ab0", "#ffe24a", "#b8f06a", "#7ae8ff"], hedef=560)

im.convert("RGB").save(a.cikti, quality=95)
print("->", a.cikti)
