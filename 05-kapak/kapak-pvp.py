"""TETRIS MODE PVP kapagi (REF-053 duzeni, bizim renkler) - 1280x720.

    python kapak-pvp.py --p1 gate-pose --p2 extended-side-angle [--ayna2] --cikti KAPAK-A.jpg

REF-053 kapagi (olculdu: 11-GLOWMOTION-PVP3-KAPAK-OLCUM.md): ustte tam genislik iki renkli tombul parlak baslik; arkada videonun
kendi sahnesi (iki kafes kapi + jole yol); onde yazinin ALTINDA iki dev DUZ SIMSIYAH siluet + kalin beyaz dis kontur; ortada VS.
Sayi / soru / yuz / P1-P2 yazisi YOK. Bizde: baslik seri adi TETRIS MODE (kullanici 18 Eki 2026), TETRIS yesil, MODE turuncu;
arka plan videonun Blender varliklari (03-motor/tetris-pvp/varlik), siluet = videodaki pozun Mixamo maskesi; VS altin + camgobegi.
Baslik harf yontemi kapak-tetris.py parlak_yazi ile ayni (17 Eki onayli: hacim + beyaz kontur + parlak bant + isilti).
"""
import argparse, math, os
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont, ImageEnhance

KOK = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
p = argparse.ArgumentParser()
p.add_argument("--tema", default="02", choices=["02", "03"])   # 03: REF-054, mor/sari, galaksi, jole VS
p.add_argument("--p1", required=True); p.add_argument("--p2", required=True)
p.add_argument("--ayna1", action="store_true"); p.add_argument("--ayna2", action="store_true")
p.add_argument("--baslik", default="TETRIS MODE")
p.add_argument("--boy1", type=float, default=540); p.add_argument("--boy2", type=float, default=540)
p.add_argument("--gen1", type=float, default=600); p.add_argument("--gen2", type=float, default=600)
p.add_argument("--cikti", required=True)
a = p.parse_args()
T3 = a.tema == "03"
V = os.path.join(KOK, "03-motor", "tetris-pvp", "varlik-03" if T3 else "varlik")
W, H = 1280, 720
FONT = os.path.join(KOK, "05-kapak", "fontlar", "TitanOne.ttf")
yfont = lambda boy: ImageFont.truetype(FONT, boy)

# ---------------------------------------------------------------- arka plan: videonun sahnesi
im = Image.open(os.path.join(V, "gok.png")).convert("RGBA").resize((W, H), Image.LANCZOS)
for i, ad in enumerate(("serit-p1.png", "serit-p2.png")):
    s = Image.open(os.path.join(V, ad)).convert("RGBA").resize((W // 2, H), Image.LANCZOS)
    im.alpha_composite(s, (i * W // 2, 0))
import json
Y = json.load(open(os.path.join(V, "yerlesim.json"), encoding="utf-8"))
for i, (ad, ac) in enumerate((("panel-p1.png", Y["aciklik_p1"]), ("panel-p2.png", Y["aciklik_p2"]))):
    sx = (W / 2) / 960; sy = H / 1080
    x0, y0, x1, y1 = ac[0] * sx + i * W / 2, ac[1] * sy, ac[2] * sx + i * W / 2, ac[3] * sy
    pw = x1 - x0; ph = pw / (1100 / 904)
    pn = Image.open(os.path.join(V, ad)).convert("RGBA").resize((int(pw), int(ph)), Image.LANCZOS)
    if T3:   # REF-054 kapaginda kapi icinden isin patlamasi + arkadaki gok goruluyor: panel yari saydam
        pn.putalpha(pn.getchannel("A").point(lambda v: int(v * 0.38)))
    im.alpha_composite(pn, (int(x0), int(y1 - ph)))
# ampul isiltisi (videodaki kayan isik)
gl = Image.new("RGBA", (W, H)); dg = ImageDraw.Draw(gl)
for i in range(2):
    for q in Y.get("ampul_p%d" % (i + 1), []):
        x = i * W / 2 + q[0] * (W / 2) / 960; y = q[1] * H / 1080
        dg.ellipse((x - 7, y - 7, x + 7, y + 7), fill=(255, 236, 170, 230))
im.alpha_composite(gl.filter(ImageFilter.GaussianBlur(3)))
im.alpha_composite(gl)
# deneme 1 olcumu: referanstan koyu (0,64 / 0,78), az renkli (0,38 / 0,57), az ayrintili (0,10 / 0,26) -> kisma katmani
# kaldirildi, arka plan canlandirildi, goge videodaki gibi havai fisek + huzme + parilti (REF-053'te gok denizanasiyla dolu)
im = ImageEnhance.Color(im).enhance(1.0 if T3 else 1.35)   # 3. video: limon sarisi zaten doygun, yazi/siluet yutulmasin
im = ImageEnhance.Brightness(im).enhance(0.9 if T3 else 1.12)
import random
rnd = random.Random(53)
fx = Image.new("RGBA", (W, H)); df = ImageDraw.Draw(fx)
for bx, ang, renk in (((0.06, -0.25, (190, 120, 255)), (0.5, 0.0, (255, 250, 140)), (0.94, 0.25, (230, 255, 110))) if T3 else
                      ((0.06, -0.25, (90, 255, 240)), (0.5, 0.0, (255, 220, 120)), (0.94, 0.25, (140, 255, 160)))):
    x0, y0, L = W * bx, H * 0.95, H * 1.2
    ux, uy = math.sin(ang), -math.cos(ang)
    df.polygon([(x0, y0), (x0 + ux * L - uy * 60, y0 + uy * L + ux * 60), (x0 + ux * L + uy * 60, y0 + uy * L - ux * 60)], fill=renk + (60,))
for _ in range(7):                                            # havai fisek patlamalari (gokte, kapilarin ustunde ve ortada)
    cx_, cy_ = rnd.choice([rnd.uniform(560, 720), rnd.uniform(20, 1260)]), rnd.uniform(150, 330)
    renk = rnd.choice([(245, 255, 61), (180, 92, 255), (255, 122, 230), (255, 255, 255), (143, 180, 255)] if T3 else
                      [(255, 215, 90), (90, 255, 230), (150, 255, 140), (255, 255, 255), (255, 160, 60)])
    R = rnd.uniform(40, 80)
    for i in range(28):
        an = i / 28 * 2 * math.pi; rr = R * rnd.uniform(0.75, 1.05)
        df.line([(cx_ + math.cos(an) * rr * 0.35, cy_ + math.sin(an) * rr * 0.35), (cx_ + math.cos(an) * rr, cy_ + math.sin(an) * rr)], fill=renk + (230,), width=3)
for _ in range(26):                                           # jole isik kureleri (parlak ust, renkli govde)
    x, y, r = rnd.uniform(0, W), rnd.uniform(140, H * 0.7), rnd.uniform(8, 26)
    renk = rnd.choice([(180, 92, 255), (245, 255, 61), (255, 122, 230), (143, 180, 255)] if T3 else
                      [(90, 255, 220), (170, 255, 120), (255, 210, 110), (120, 220, 255)])
    df.ellipse((x - r, y - r, x + r, y + r), fill=renk + (150,), outline=(255, 255, 255, 200), width=2)
    df.ellipse((x - r * 0.55, y - r * 0.7, x - r * 0.05, y - r * 0.25), fill=(255, 255, 255, 210))
for _ in range(10):                                           # kucuk havai fisekler
    cx_, cy_ = rnd.uniform(0, W), rnd.uniform(160, 420); R = rnd.uniform(16, 32)
    renk = rnd.choice([(245, 255, 61), (200, 140, 255), (255, 255, 255)] if T3 else [(255, 230, 120), (120, 255, 230), (255, 255, 255)])
    for i in range(16):
        an = i / 16 * 2 * math.pi
        df.line([(cx_ + math.cos(an) * R * 0.3, cy_ + math.sin(an) * R * 0.3), (cx_ + math.cos(an) * R, cy_ + math.sin(an) * R)], fill=renk + (220,), width=2)
for _ in range(420):                                          # parilti
    x, y, r = rnd.uniform(0, W), rnd.uniform(0, H * 0.75), rnd.uniform(1.5, 4.5)
    df.ellipse((x - r, y - r, x + r, y + r), fill=(255, 245, 210, rnd.randint(140, 255)))
im.alpha_composite(fx.filter(ImageFilter.GaussianBlur(5))); im.alpha_composite(fx)

# ---------------------------------------------------------------- siluetler (yazinin altinda, iki yanda dev)
def siluet(ad, ayna, merkez_x, alt_y, hedef_h, max_w):
    m = Image.open(os.path.join(V, "poz", ad + ".png")).getchannel("A")
    m = m.crop(m.getbbox())
    if ayna:
        m = m.transpose(Image.FLIP_LEFT_RIGHT)
    s = min(hedef_h / m.height, max_w / m.width)
    m = m.resize((int(m.width * s), int(m.height * s)), Image.LANCZOS)
    tam = Image.new("L", (W, H)); tam.paste(m, (int(merkez_x - m.width / 2), int(alt_y - m.height)))
    return tam.point(lambda v: 255 if v > 110 else 0)

KONTUR = 21                                                   # referansta kontur kalin


def yerlestir(ad, ayna, x0, boy, gen, engel, yon, ust_sinir):
    """deneme 4 (kullanici 18 Eki: "VS yazisi siluetlere degmesin ... VS on planda olsun ama siluetleri de kapatmasin"):
    siluet (kontur + 6 px pay dahil) VS rozetinin dolu alanina ve basliga degene kadar disa kayar; kenara dayaninca %4 kuculur."""
    olc = 1.0
    for _ in range(80):
        x = x0
        while True:
            m = siluet(ad, ayna, x, 718, boy * olc, gen * olc)
            bb = m.getbbox()
            genis = m.filter(ImageFilter.MaxFilter(KONTUR + 12))
            carpisma = ImageChops.multiply(genis, engel).getbbox() is not None
            icerde = bb[0] >= 12 and bb[2] <= W - 12                 # deneme 4 B: kenardan tasip kesiliyordu
            if not carpisma and bb[1] >= ust_sinir and icerde:
                return m
            if carpisma and icerde and (bb[0] - 10 >= 12 if yon < 0 else bb[2] + 10 <= W - 12):
                x += 10 * yon                                    # once disa kay
                continue
            break
        olc *= 0.96                                              # kenara dayandi ya da basliga degiyor -> kucul
    return m


def siluetleri_ciz(maskeler):
    mk = Image.new("L", (W, H))
    for m in maskeler:
        mk = Image.composite(Image.new("L", (W, H), 255), mk, m)
    mk = mk.filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.MinFilter(3))
    kontur = mk.filter(ImageFilter.MaxFilter(KONTUR))
    isilti = kontur.filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.GaussianBlur(16))
    # 3. video: limon sarisi zeminde beyaz kontur kayboluyordu -> konturun disinda koyu mor hale (beyaz kontur ayrisir)
    hale_renk, hale_guc = ((40, 8, 80), 0.85) if T3 else ((255, 236, 160), 0.55)
    im.alpha_composite(Image.merge("RGBA", [Image.new("L", (W, H), c) for c in hale_renk] + [isilti.point(lambda v: int(v * hale_guc))]))
    im.alpha_composite(Image.merge("RGBA", [Image.new("L", (W, H), 255)] * 3 + [kontur]))
    im.alpha_composite(Image.merge("RGBA", [Image.new("L", (W, H), c) for c in (6, 4, 14)] + [mk.filter(ImageFilter.GaussianBlur(0.7))]))


# ---------------------------------------------------------------- VS rozeti (bizim: camgobegi simsek + altin harf)
def vs_jole(merkez, r=150):
    """REF-054 kapagindaki VS: parlak yesil jole harf + arkasinda sari simsek + egik halka ve jole kabarciklar (bizim cizim)"""
    k = Image.new("RGBA", (int(r * 3.4), int(r * 3.4))); d = ImageDraw.Draw(k); c = (k.width / 2, k.height / 2)
    sm = [(c[0] + 40, c[1] - r * 1.35), (c[0] - 55, c[1] + 5), (c[0] + 5, c[1] + 2), (c[0] - 45, c[1] + r * 1.35),
          (c[0] + 70, c[1] - 20), (c[0] + 8, c[1] - 16)]
    d.polygon(sm, fill=(245, 255, 61), outline=(255, 255, 255), width=5)
    halka = Image.new("RGBA", k.size); dh = ImageDraw.Draw(halka)
    dh.ellipse((c[0] - r * 1.45, c[1] - r * 0.42, c[0] + r * 1.45, c[1] + r * 0.42), outline=(150, 255, 60), width=9)
    k.alpha_composite(halka.rotate(-12, Image.BICUBIC, center=c))
    import random as _r
    rr_ = _r.Random(11)
    for _ in range(9):
        an = rr_.uniform(0, 2 * math.pi); uz = r * rr_.uniform(1.1, 1.5); br = rr_.uniform(9, 20)
        x, y = c[0] + math.cos(an) * uz, c[1] + math.sin(an) * uz * 0.6
        d.ellipse((x - br, y - br, x + br, y + br), fill=(150, 240, 50), outline=(230, 255, 180), width=2)
        d.ellipse((x - br * 0.5, y - br * 0.65, x - br * 0.05, y - br * 0.25), fill=(255, 255, 255))
    g = k.getchannel("A").filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.GaussianBlur(16))
    gl = Image.merge("RGBA", [Image.new("L", k.size, c_) for c_ in (200, 255, 120)] + [g.point(lambda v: int(v * 0.6))])
    dolu = k.getchannel("A")
    gl.alpha_composite(k); k = gl
    kat = Image.new("RGBA", (W, H)); ox, oy = int(merkez[0] - k.width / 2), int(merkez[1] - k.height / 2)
    kat.alpha_composite(k, (ox, oy))
    engel = Image.new("L", (W, H)); engel.paste(dolu.point(lambda v: 255 if v > 60 else 0), (ox, oy))
    yz2 = parlak_yazi("VS", yfont(210), [(190, 255, 70), (90, 220, 40)], kontur=12, derinlik=16, dis=(20, 70, 10),
                      parlama=(220, 255, 140), zipla=0, don=7)
    tx, ty = int(merkez[0] - yz2.width / 2), int(merkez[1] - yz2.height / 2 - 6)
    kat.alpha_composite(yz2, (tx, ty))
    ym = Image.new("L", (W, H)); ym.paste(yz2.getchannel("A").point(lambda v: 255 if v > 120 else 0), (tx, ty))
    return kat, ImageChops.lighter(engel, ym)


def vs(merkez, r=150):
    """deneme 3: VS buyuk ve en onde (kullanici: "VS yazisini biraz daha buyutelim ... ön planda olsun"),
    atesli: altin-turuncu alev patlamasi + kivilcimlar + camgobegi simsekler (referanstaki kirmizi atesin bizim tonu)"""
    k = Image.new("RGBA", (int(r * 3.4), int(r * 3.4))); d = ImageDraw.Draw(k); c = (k.width / 2, k.height / 2)
    import random as _r
    rr_ = _r.Random(7)
    # alev patlamasi: iki kat dikenli yildiz (dis turuncu, ic altin)
    for kat, (renk, olc) in enumerate((((255, 110, 20), 1.0), ((255, 200, 40), 0.78), ((255, 245, 170), 0.5))):
        n = 22; pts = []
        for i in range(n * 2):
            uz = r * olc * (1.35 + 0.25 * rr_.random() if i % 2 == 0 else 0.8)
            an = i * math.pi / n + kat * 0.07
            pts.append((c[0] + math.cos(an) * uz, c[1] + math.sin(an) * uz * 0.82))
        d.polygon(pts, fill=renk)
    # camgobegi simsekler (iki yana)
    for s_ in (-1, 1):
        x0 = c[0] + s_ * r * 0.55
        sm = [(x0, c[1] - r * 1.25), (x0 - s_ * 26, c[1] - 10), (x0 + s_ * 6, c[1] - 6), (x0 - s_ * 22, c[1] + r * 1.2),
              (x0 + s_ * 34, c[1] + 18), (x0 + s_ * 4, c[1] + 14)]
        d.polygon(sm, fill=(110, 250, 255), outline=(255, 255, 255), width=4)
    # kivilcimlar
    for _ in range(46):
        an = rr_.uniform(0, 2 * math.pi); uz = r * rr_.uniform(1.15, 1.6); ln = rr_.uniform(8, 22)
        x, y = c[0] + math.cos(an) * uz, c[1] + math.sin(an) * uz * 0.85
        d.line([(x, y), (x + math.cos(an) * ln, y + math.sin(an) * ln * 0.85)], fill=rr_.choice([(255, 230, 120), (255, 160, 40), (255, 255, 255)]), width=3)
    g = k.getchannel("A").filter(ImageFilter.MaxFilter(11)).filter(ImageFilter.GaussianBlur(18))
    gl = Image.merge("RGBA", [Image.new("L", k.size, c_) for c_ in (255, 170, 60)] + [g.point(lambda v: int(v * 0.8))])
    dolu = k.getchannel("A")                                      # isiltisiz dolu alan (carpisma maskesi)
    gl.alpha_composite(k); k = gl
    kat = Image.new("RGBA", (W, H)); ox, oy = int(merkez[0] - k.width / 2), int(merkez[1] - k.height / 2)
    kat.alpha_composite(k, (ox, oy))
    engel = Image.new("L", (W, H)); engel.paste(dolu.point(lambda v: 255 if v > 60 else 0), (ox, oy))
    # VS harfi: kirmizi -> turuncu sicak gecis, beyaz kontur, koyu derinlik
    yz2 = parlak_yazi("VS", yfont(200), [(255, 60, 40), (255, 150, 20)], kontur=12, derinlik=16, dis=(90, 10, 30),
                      parlama=(255, 200, 80), zipla=0, don=7)
    tx, ty = int(merkez[0] - yz2.width / 2), int(merkez[1] - yz2.height / 2 - 6)
    kat.alpha_composite(yz2, (tx, ty))
    ym = Image.new("L", (W, H)); ym.paste(yz2.getchannel("A").point(lambda v: 255 if v > 120 else 0), (tx, ty))
    engel = ImageChops.lighter(engel, ym)
    return kat, engel


PARLAK_BANT = 150
# ---------------------------------------------------------------- baslik harfleri (kapak-tetris.py ile ayni yontem)
def parlak_yazi(metin, f, renkler, kontur=9, derinlik=12, dis=(30, 0, 70), parlama=(255, 80, 220),
                zipla=6, don=4, aralik=4):
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
        hm = Image.new("L", (int(cw) + 2 * pad, hh + 2 * pad)); ImageDraw.Draw(hm).text((pad, pad), c, font=f, fill=255)
        km = Image.new("L", hm.size); ImageDraw.Draw(km).text((pad, pad), c, font=f, fill=255, stroke_width=kontur, stroke_fill=255)
        L = Image.new("RGBA", hm.size)
        dm = km.filter(ImageFilter.MaxFilter(9))
        for k_ in range(derinlik, -1, -2):
            sh = Image.new("RGBA", hm.size, dis + (0,)); sh.putalpha(dm); L.alpha_composite(sh, (k_ // 2, k_))
        for k_ in range(derinlik, 0, -1):
            sh = Image.new("RGBA", hm.size, dis + (0,)); sh.putalpha(km); L.alpha_composite(sh, (k_ // 2, k_))
        bk = Image.new("RGBA", hm.size, (255, 255, 255, 0)); bk.putalpha(km); L.alpha_composite(bk)
        r, g, b = renkler[i % len(renkler)]
        grad = Image.new("RGBA", hm.size); gd = ImageDraw.Draw(grad)
        for yy in range(hm.size[1]):
            q = min(1, max(0, (yy - pad) / max(1, asc)))
            if q < 0.45:
                m_ = 0.20 * (1 - q / 0.45); cc = (r + (255 - r) * m_, g + (255 - g) * m_, b + (255 - b) * m_)
            else:
                m_ = 0.35 * (q - 0.45) / 0.55; cc = (r * (1 - m_), g * (1 - m_), b * (1 - m_))
            gd.line([(0, yy), (hm.size[0], yy)], fill=tuple(int(v) for v in cc) + (255,))
        grad.putalpha(hm); L.alpha_composite(grad)
        band = Image.new("L", hm.size, 0); ImageDraw.Draw(band).ellipse((pad - cw * 0.2, pad - hh * 0.3, pad + cw * 1.2, pad + asc * 0.34), fill=PARLAK_BANT)
        band = Image.composite(band, Image.new("L", hm.size, 0), hm).filter(ImageFilter.GaussianBlur(2))
        bw_ = Image.new("RGBA", hm.size, (255, 255, 255, 0)); bw_.putalpha(band); L.alpha_composite(bw_)
        aci = don * (1 if i % 2 == 0 else -1) * (0.6 + 0.4 * ((i * 37) % 5) / 4)
        L = L.rotate(aci, Image.BICUBIC, expand=False)
        dy = int(zipla * math.sin(i * 1.9))
        tuval.alpha_composite(L, (int(x - pad), zipla + dy))
        x += cw + aralik
    tuval = tuval.crop(tuval.getchannel("A").getbbox())
    if parlama:
        e = 40
        big = Image.new("RGBA", (tuval.width + 2 * e, tuval.height + 2 * e)); big.alpha_composite(tuval, (e, e))
        g = big.getchannel("A").filter(ImageFilter.MaxFilter(11)).filter(ImageFilter.GaussianBlur(18))
        gl = Image.merge("RGBA", [Image.new("L", big.size, c) for c in parlama] + [g.point(lambda v: min(255, int(v * 1.3)))])
        gl.alpha_composite(big); tuval = gl
    return tuval


def gecis(n, c0, c1):          # kelime ici soldan saga renk gecisi (referanstaki gibi kelime basina tek degrade)
    return [tuple(int(c0[j] + (c1[j] - c0[j]) * (i / max(1, n - 1))) for j in range(3)) for i in range(n)]
w1, w2 = a.baslik.split(" ", 1)
renk = (gecis(len(w1), (150, 70, 255), (255, 110, 235)) + [(255, 255, 255)] + gecis(len(w2), (255, 250, 70), (190, 255, 40)) if T3 else
        gecis(len(w1), (40, 230, 230), (150, 255, 40)) + [(255, 255, 255)] + gecis(len(w2), (255, 225, 40), (255, 100, 20)))
if T3:
    # kullanici 19 Eki 2026: "ayni yazi fontunda kalsin ama harfler asagida veya yukarida olmasin, normal duz olsun ... sigsin,
    # okunacak, dikkat cekecek" -> Titan One kalir; ziplama/donme 0, tek satir tam genislik, renkler video ile uyumlu
    renk = [(178, 92, 255)] * len(w1) + [(255, 255, 255)] + [(245, 255, 61)] * len(w2)
    yz = parlak_yazi(a.baslik, yfont(160), renk, kontur=10, derinlik=15, dis=(45, 8, 95), parlama=(200, 120, 255), zipla=0, don=0)
else:
    yz = parlak_yazi(a.baslik, yfont(160), renk, kontur=10, derinlik=15, dis=(20, 10, 60), parlama=(255, 236, 150), zipla=7, don=4)
if yz.width > 1240:
    yz = yz.resize((1240, int(yz.height * 1240 / yz.width)), Image.LANCZOS)
by = int(96 - yz.height / 2)
baslik_alt = by + int(yz.getchannel("A").point(lambda v: 255 if v > 200 else 0).getbbox()[3])
vs_kat, vs_engel = (vs_jole if T3 else vs)((640, 455))
m1 = yerlestir(a.p1, a.ayna1, 310, a.boy1, a.gen1, vs_engel, -1, baslik_alt + 4)
m2 = yerlestir(a.p2, a.ayna2, 970, a.boy2, a.gen2, vs_engel, +1, baslik_alt + 4)
print("siluet kutulari:", m1.getbbox(), m2.getbbox(), "baslik alti", baslik_alt)
siluetleri_ciz([m1, m2])                                      # 1) siluetler
im.alpha_composite(yz, (int(W / 2 - yz.width / 2), by))       # 2) baslik
im.alpha_composite(vs_kat)                                    # 3) VS en onde, siluete degmez
im.convert("RGB").save(a.cikti, quality=93)
print(a.cikti, os.path.getsize(a.cikti) // 1024, "KB")
