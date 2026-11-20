"""KESIM SAYACI - zaman plani.

Tek dogruluk kaynagi: Blender sahnesi (sahne.py), yazi katmani (hud.py) ve ses (ses.py)
hepsi bu dosyanin urettigi plan JSON'unu okur. Kup sayilari burada geometriden hesaplanir.

Kullanim: python plan.py --meyve avokado --cikti plan-avokado.json
"""
import argparse
import json
import math

import numpy as np

FPS = 30
SURE = 60.0  # kullanici: 1 dakikalik video

# Avokado x boyunca yatar; cilek kameraya donuk XZ duzleminde dik durur.
MEYVELER = {
    "avokado": {
        "A": 1.15,      # yarim boy (x)
        "R": 0.78,      # en genis yaricap
        "boyun": 0.55,  # dar uc / genis uc orani
        "cekirdek": {"x": 0.28, "r": 0.40},  # x: A'ya oranla merkez, r: R'ye oranla yaricap
    },
    "strawberry": {
        # Nesne karti: kameraya donuk dik kalp silueti. Ust omuzlar genis,
        # alt uc yumusak sivri; yesil canak/sap usttedir.
        # Kirmizi yuzeyde altin oval akenler ve sig cukurlar; kesitte kirmizi
        # dis halka -> pembe et -> beyaz oz vardir, iri cekirdek/oyuk yoktur.
        "A": 0.91,  # yatay yari genislik
        "B": 0.62,  # kameraya dogru derinlik
        "R": 0.88,  # dikey yari yukseklik
        "profil": "strawberry",
    },
    "watermelon": {
        # Nesne karti: tahtaya yatmis, iki ucu yuvarlak kisa elipsoid;
        # koyu/acik yesil boyuna serit, kalin beyaz-yesil ara kabuk,
        # kirmizi sulu et ve yalniz et icinde seyrek yassi koyu cekirdek.
        "A": 1.14,
        "R": 0.72,
        "boyun": 1.0,
    },
    "kiwi": {
        # Nesne karti: yatay tombul oval, hafif basik uclar, kisa tuy ve sap izi.
        # Ince kahve kabuk; parlak yesil et, krem merkez, radyal acik isinlar
        # ve yalniz merkez cevresindeki halkada minik koyu tohumlar.
        "A": 0.96,
        "R": 0.66,
        "boyun": 1.0,
        "profil": "kiwi",
    },
    "pineapple": {
        # Yatay uzun oval-silindir; sag ucta yesil yaprak tac, solda sap tabani.
        # Capraz sarmal baklava gozleri kabariktir. Kesitte altin sari lifli et,
        # boyuna soluk silindirik merkez vardir; sert cekirdek/oyuk yoktur.
        "A": 1.10,
        "R": 0.65,
        "boyun": 1.0,
        "profil": "pineapple",
        "xmin": -1.20,  # sol sap tabani da kesim hacmine dahil
        "xmax": 1.68,   # sag yaprak tacinin son ucu da kup olur
    },
    "apple": {
        "A": 0.86, "R": 0.76, "boyun": 1.0, "profil": "apple",
    },
    "orange": {
        "A": 0.80, "R": 0.75, "boyun": 1.0, "profil": "orange",
    },
    "banana": {
        "A": 1.33, "R": 0.30, "boyun": 1.0, "profil": "banana",
        "xmin": -1.43, "xmax": 1.52,
    },
    "peach": {
        "A": 0.78, "R": 0.72, "boyun": 1.0, "profil": "peach",
    },
    "pomegranate": {
        "A": 0.78, "R": 0.76, "boyun": 1.0, "profil": "pomegranate",
        "zmax": 0.96,
    },
    "tomato": {
        "A": 0.78, "R": 0.72, "boyun": 1.0, "profil": "tomato",
        "zmax": 0.87,
    },
    "cucumber": {
        "A": 1.26, "R": 0.30, "boyun": 1.0, "profil": "cucumber",
        "xmax": 1.39,
    },
    "red-bell-pepper": {
        "A": 0.70, "B": 0.66, "R": 0.77, "boyun": 1.0,
        "profil": "red-bell-pepper", "zmax": 0.99,
    },
}

# Turlar: (kesim sayisi, kesim suresi sn). Acilis 0.4 sn + sonuc 1.3 sn eklenir -> toplam 60 sn
TURLAR = [(10, 3.4), (50, 7.4), (100, 8.2), (240, 8.3), (500, 8.8), (1000, 13.7)]  # 6 tur, 60 sn  # REF-080: 6 tur 10 -> 1000
ACILIS = 0.7  # yeni meyve yukaridan duser + seker
SONUC = 1.0
CIZGI_PAY = 0.6  # tur suresinin ilk %60'i kabukta cizgiler (z, y); son %40 soldan saga supurme (x)
US = 0.7  # kesim hizlanma ussu (<1 = hizlanir)
VURUS_ARA = 0.1  # gorunur bicak vuruslari arasi en az sure (sn)


def profil(xn, boyun):
    xn = np.clip(xn, -1.0, 1.0)
    s = (xn + 1.0) / 2.0
    return np.sqrt(np.maximum(0.0, 1.0 - xn * xn)) * (boyun + (1.0 - boyun) * s)


def fmax(boyun):
    xs = np.linspace(-1, 1, 20001)
    return float(profil(xs, boyun).max())


def meyve_profil(xn, m):
    """Plan, Blender govdesi, kesit ve kup izgarasinin ortak dis profili."""
    if m.get("profil") == "strawberry":
        s = (np.clip(xn, -1.0, 1.0) + 1.0) / 2.0
        return s ** 0.62 * (1.0 - s) ** 0.25
    if m.get("profil") == "kiwi":
        xn = np.clip(xn, -1.0, 1.0)
        return np.maximum(0.0, 1.0 - xn * xn) ** 0.38
    if m.get("profil") == "pineapple":
        xn = np.clip(xn, -1.0, 1.0)
        return np.maximum(0.0, 1.0 - xn * xn) ** 0.31
    if m.get("profil") == "apple":
        return np.maximum(0.0, 1.0 - xn * xn) ** 0.46
    if m.get("profil") == "orange":
        return np.maximum(0.0, 1.0 - xn * xn) ** 0.50
    if m.get("profil") == "banana":
        return np.maximum(0.0, 1.0 - xn ** 2) ** 0.48 * (1.0 - .25*np.abs(xn)**2) * (.96 + .04*xn)
    if m.get("profil") == "peach":
        return np.maximum(0.0, 1.0 - xn * xn) ** 0.46
    if m.get("profil") in ("pomegranate", "tomato"):
        return np.maximum(0.0, 1.0 - xn*xn) ** 0.48
    if m.get("profil") == "cucumber":
        return np.maximum(0.0, 1.0 - np.abs(xn)**8) ** 0.34 * (0.97 + 0.03*xn)
    return profil(xn, m["boyun"])


def meyve_fmax(m):
    if m.get("profil") == "strawberry":
        return float(meyve_profil(np.linspace(-1, 1, 20001), m).max())
    if m.get("profil") in ("kiwi", "pineapple", "apple", "orange", "peach", "pomegranate", "tomato"):
        return 1.0
    if m.get("profil") == "banana":
        return float(meyve_profil(np.linspace(-1, 1, 20001), m).max())
    if m.get("profil") == "cucumber":
        return float(meyve_profil(np.linspace(-1, 1, 20001), m).max())
    return fmax(m["boyun"])


def profil_yaricap(x, m, fm=None):
    fm = meyve_fmax(m) if fm is None else fm
    if m.get("profil") == "strawberry":
        # Dikey z boyunca yatay elipsin boyutsuz yari genisligi.
        return meyve_profil(np.asarray(x) / m["R"], m) / fm
    return m["R"] * meyve_profil(np.asarray(x) / m["A"], m) / fm


def ananas_goz(x, aci, m):
    """0..1 kabarik baklava gozu; x ve aci boyunca capraz sarmal sira."""
    s = (np.asarray(x) / m["A"] + 1.0) * 0.5
    ax = np.abs(((18.0 * s + 0.5) % 1.0) - 0.5) * 2.0
    cevre = np.asarray(aci) * (12.0 / (2.0 * np.pi)) + 0.45 * 18.0 * s
    an = np.abs(((cevre + 0.5) % 1.0) - 0.5) * 2.0
    baklava = np.maximum(0.0, 1.0 - 0.72 * (ax + an))
    zarf = np.minimum(1.0, meyve_profil(np.asarray(x) / m["A"], m) / 0.35)
    return baklava * zarf


def ananas_tac(x, y, z, m):
    """On alti sivri yaprak ve merkez dip: ayni hacim gorunur tac/kup icin."""
    base = 0.78 * m["A"]
    aci = np.arctan2(z, y)
    sektor = (aci * 16.0 / (2.0 * np.pi)) % 16.0
    indeks = np.floor(sektor + 0.5) % 16.0
    faz = np.abs(((sektor + 0.5) % 1.0) - 0.5)
    uzunluk = np.minimum(0.81, 0.77 + 0.035 * np.sin(indeks * 2.3) + 0.020 * np.cos(indeks * 3.7))
    t = (x - base) / uzunluk
    rho = np.sqrt(y * y + z * z) / m["R"]
    merkez = 0.19 + 0.53 * np.clip(t, 0, 1)
    yaricap = (0.26 * (1.0 - np.clip(t, 0, 1)) + 0.15) * np.minimum(1.0, (1.0 - np.clip(t, 0, 1)) / 0.10)
    aci_pay = 0.44 * (1.0 - np.clip(t, 0, 1)) + 0.09
    yaprak = (np.abs(rho - merkez) <= yaricap) & (faz <= aci_pay)
    dip = (x <= m["A"] + 0.18) & (rho <= 0.19 * np.sqrt(np.maximum(0.0, 1.0 - np.clip(t, 0, 1))))
    return (t >= 0) & (t <= 1) & (yaprak | dip)


def ananas_sap(x, y, z, m):
    return ((x >= m["xmin"]) & (x <= -m["A"] + 0.025) &
            (y * y + z * z <= 0.07 * 0.07))


def muz_egri(x, m):
    """Muzun egri merkez cizgisi, plan ve sahnede ayni."""
    return 0.30 * (np.asarray(x) / m["A"]) ** 2 - 0.12


def salatalik_egri(x, m):
    """Hafif dogal egri; kesit, govde ve kupte ayni merkez ekseni."""
    return 0.085 * (np.asarray(x) / m["A"]) ** 2 - 0.035


def biber_profil(z, m):
    """Dort loblu dolmalik biberin altta dolgun, ustte daralan govde yaricapi."""
    zn=np.clip(np.asarray(z)/m["R"],-1.0,1.0)
    s=(zn+1.0)*.5
    return (0.95-0.19*s+0.06*np.sin(np.pi*s))*np.maximum(0.0,1.0-np.abs(zn)**8)**.28


def biber_canak(x,y,z,m):
    r=np.sqrt(x*x+y*y)
    angle=np.arctan2(y,x)
    star=.11+.23*np.maximum(0.0,np.cos(5*angle))**5
    leaf=(z>=.70)&(z<=.77)&(r<=star)
    stem=(z>=.75)&(z<=m["zmax"])&(r<=.053)
    return leaf|stem


def muz_sirt(y, z):
    return 1.0 + 0.11 * np.cos(5.0 * np.arctan2(z, y))


def nar_tac(x, y, z, m):
    """Acik merkezli bes sivri tac lobu; govdeyle birlikte kesim hacminde."""
    r = np.sqrt(x*x+y*y)
    angle = np.arctan2(y,x)
    peak = .82 + .14*np.maximum(0.0,np.cos(5*angle))**3
    return (z >= .69) & (z <= peak) & (r >= .075) & (r <= .21*(1-.25*np.clip((z-.69)/.27,0,1)))


def domates_canak(x, y, z, m):
    r = np.sqrt(x*x+y*y)
    angle = np.arctan2(y,x)
    star = .11 + .20*np.maximum(0.0,np.cos(5*angle))**6
    leaf = (z >= .69) & (z <= .74) & (r <= star)
    stem = (z >= .73) & (z <= m["zmax"]) & (r <= .045)
    return leaf | stem


def icinde(x, y, z, m):
    """Meyvenin merkezine gore (x,y,z) noktasi govdenin icinde mi."""
    if m.get("profil") == "strawberry":
        p = profil_yaricap(z, m)
        return (np.abs(z) <= m["R"]) & ((x / m["A"]) ** 2 + (y / m["B"]) ** 2 <= p * p)
    if m.get("profil") == "red-bell-pepper":
        theta=np.arctan2(y/m["B"],x/m["A"])
        lob=1.0+.08*np.cos(4*theta)
        rr=np.maximum(.001,biber_profil(z,m)*lob)
        rad=np.sqrt((x/m["A"])**2+(y/m["B"])**2)/rr
        shell=(np.abs(z)<=m["R"])&(rad<=1.0)
        cavity=(z>-.62*m["R"])&(z<.70*m["R"])&(rad<.72)
        body=shell&~cavity
        pith=(np.sqrt(x*x+y*y)<.12)&(z>-.22)&(z<.72)
        seeds=(rad>.14)&(rad<.49)&(z>.20)&(z<.68)&(np.cos(29*x+37*y+41*z)>.86)
        return body|pith|seeds|biber_canak(x,y,z,m)
    xn = x / m["A"]
    rr = profil_yaricap(x, m)
    if m.get("profil") == "pineapple":
        rr = rr + 0.035 * ananas_goz(x, np.arctan2(z, y), m)
        govde = (np.abs(xn) <= 1.0) & (y * y + z * z <= rr * rr)
        return govde | ananas_tac(x, y, z, m) | ananas_sap(x, y, z, m)
    if m.get("profil") == "apple":
        # Gercek ust sap cukuru ve alt cicek cukuru; sap/yaprak da kesim hacminde.
        cukur = 0.105 * np.exp(-(x*x + y*y) / 0.032)
        omuz = 1.0 + 0.08 * np.tanh(z / (0.20*m["R"]))
        r_app = m["R"] * meyve_profil(x/(m["A"]*omuz), m)
        govde = (np.abs(x/(m["A"]*omuz)) <= 1.0) & ((y/omuz)**2 + (np.abs(z) + cukur)**2 <= r_app*r_app)
        sap = (x*x + y*y <= 0.050**2) & (z >= 0.56) & (z <= 0.76)
        yaprak = ((x-0.23)/0.25)**2 + ((y+0.36)/0.14)**2 + ((z-0.715)/0.055)**2 <= 1
        return govde | sap | yaprak
    if m.get("profil") == "orange":
        govde = (np.abs(xn) <= 1.0) & (y*y + z*z <= rr*rr)
        calyx = (x*x+y*y <= 0.21**2) & (z >= 0.70) & (z <= 0.76)
        return govde | calyx
    if m.get("profil") == "banana":
        dz = z - muz_egri(x, m)
        aci = np.arctan2(dz, y)
        rib = 1.0 + 0.11 * np.cos(5.0 * aci)
        govde = (np.abs(xn) <= 1.0) & (y*y + dz*dz <= (rr*rib)**2)
        sap = (x >= m["A"]-0.04) & (x <= m["xmax"]) & (y*y+(dz-0.01)**2 <= .072**2)
        uc = (x >= m["xmin"]) & (x <= -m["A"]+0.05) & (y*y+dz*dz <= .048**2)
        return govde | sap | uc
    if m.get("profil") == "peach":
        # Kameraya bakan x=0 duzleminde sap cukurundan asagi inen oluk.
        angle = np.arctan2(z, y)
        groove = 1.0 - 0.045 * np.exp(-(x / .09)**2) * (y < 0)
        wobble = 1.0 + 0.035*np.sin(3*angle + 0.5)
        body = (np.abs(xn) <= 1.0) & (y*y+z*z <= (rr*groove*wobble)**2)
        return body
    if m.get("profil") == "pomegranate":
        # Hafif bes lob ve derimsi kabuk altinda aril odalari.
        angle = np.arctan2(y,z)
        lob = 1.0 + .025*np.cos(5*angle)
        body = (np.abs(xn)<=1.0) & (y*y+z*z <= (rr*lob)**2)
        return body | nar_tac(x,y,z,m)
    if m.get("profil") == "tomato":
        angle=np.arctan2(y,z)
        lob=1.0+.035*np.cos(5*angle)
        body=(np.abs(xn)<=1.0)&(y*y+z*z<=(rr*lob)**2)
        return body | domates_canak(x,y,z,m)
    if m.get("profil") == "cucumber":
        dz = z - salatalik_egri(x, m)
        angle = np.arctan2(dz, y)
        ridge = 1.0 + .025*np.cos(9*angle + .8*x)
        body = (np.abs(xn) <= 1.0) & (y*y + dz*dz <= (rr*ridge)**2)
        stem = (x >= m["A"]-.025) & (x <= m["xmax"]) & (y*y + dz*dz <= .052**2)
        return body | stem
    return (np.abs(xn) <= 1.0) & (y * y + z * z <= rr * rr)


def eksen_bol(n):
    cx = math.ceil(n / 3)
    cy = math.ceil((n - cx) / 2)
    cz = n - cx - cy
    return cx, cy, cz


def kup_say(m, cx, cy, cz):
    """Kesimlerle olusan hucrelerden merkezi meyvenin icinde kalanlar = kup sayisi."""
    A, R, B = m["A"], m["R"], m.get("B", m["R"])
    xmin, xmax = m.get("xmin", -A), m.get("xmax", A)
    xs = xmin + (np.arange(cx + 1) + 0.5) * ((xmax - xmin) / (cx + 1))
    ys = -B + (np.arange(cy + 1) + 0.5) * (2 * B / (cy + 1))
    zmin, zmax = m.get("zmin", -R), m.get("zmax", R)
    zs = zmin + (np.arange(cz + 1) + 0.5) * ((zmax-zmin) / (cz + 1))
    say = 0
    Y, Z = np.meshgrid(ys, zs, indexing="ij")
    for x in xs:  # bellek dostu: x dilim dilim
        say += int(icinde(np.full_like(Y, x), Y, Z, m).sum())
    return say


def dilim_say(m, cx, cy, cz):
    """x dilimi basina (soldan saga) kup sayisi; toplam = kup_say."""
    A, R, B = m["A"], m["R"], m.get("B", m["R"])
    xmin, xmax = m.get("xmin", -A), m.get("xmax", A)
    xs = xmin + (np.arange(cx + 1) + 0.5) * ((xmax - xmin) / (cx + 1))
    ys = -B + (np.arange(cy + 1) + 0.5) * (2 * B / (cy + 1))
    zmin, zmax = m.get("zmin", -R), m.get("zmax", R)
    zs = zmin + (np.arange(cz + 1) + 0.5) * ((zmax-zmin) / (cz + 1))
    Y, Z = np.meshgrid(ys, zs, indexing="ij")
    return np.array([int(icinde(np.full_like(Y, x), Y, Z, m).sum()) for x in xs])


def plan_kur(meyve):
    m = MEYVELER[meyve]
    turlar = []
    t = 0.0
    for n, tc in TURLAR:
        cx, cy, cz = eksen_bol(n)
        bas = t
        kes_bas = bas + ACILIS
        kes_son = kes_bas + tc
        son = kes_son + SONUC
        kesimler = []
        # REF-080 sirasi: once z (yatay) + y (kameraya dik halkalar) cizgileri, sonra x supurmesi soldan saga
        sira = [("z", j, cz) for j in range(1, cz + 1)] + [("y", j, cy) for j in range(1, cy + 1)]
        sira += [("x", j, cx) for j in range(1, cx + 1)]
        n_c = cz + cy
        for i, (eks, j, c) in enumerate(sira, 1):
            if i <= n_c:
                tt = kes_bas + tc * CIZGI_PAY * (i / n_c) ** US
            else:
                tt = kes_bas + tc * CIZGI_PAY + tc * (1 - CIZGI_PAY) * ((i - n_c) / cx) ** 0.85
            yar = m["A"] if eks == "x" else (m.get("B", m["R"]) if eks == "y" else m["R"])
            if eks == "x":
                xmin, xmax = m.get("xmin", -yar), m.get("xmax", yar)
                konum = xmin + j * (xmax - xmin) / (c + 1)  # sap -> tac
            else:
                konum = yar - j * 2 * yar / (c + 1)
            kesimler.append([round(tt, 4), eks, round(konum, 5), j])
        # gorunur vuruslar: ayni eksende VURUS_ARA'dan sik kesimler tek vurusta toplanir; vurus ani = grubun
        # son kesimi (bicak o anda tahtada, dilim o anda ayrilir, ses o anda)
        vuruslar = []
        grup = []
        kova_onceki = None
        for idx, (tt, eks, konum, j) in enumerate(kesimler):
            kova = int((tt - kes_bas) / VURUS_ARA)
            if grup and (eks != kesimler[grup[0]][1] or kova != kova_onceki):
                vuruslar.append(grup)
                grup = []
            grup.append(idx)
            kova_onceki = kova
        if grup:
            vuruslar.append(grup)
        vurus_liste = []
        onceki_v = kes_bas - 1.0
        for g in vuruslar:
            son_k = kesimler[g[-1]]
            vt = son_k[0]
            if len(g) > 1:  # yogun bolge: vurus kovanin sonunda (grubun tum kesimleri yapilmis)
                vt = kes_bas + (int((son_k[0] - kes_bas) / VURUS_ARA) + 1) * VURUS_ARA
            vt = max(vt, onceki_v + 3.0 / FPS, son_k[0])
            vt = math.ceil(vt * FPS - 1e-6) / FPS  # vurus tam bir karede: bicak o karede tahtada
            if vt > kes_son + 1e-6 and vurus_liste and vurus_liste[-1][1] == son_k[1]:
                # tur sonuna sigmayan vurus: kesimleri bir onceki (son) vurusa katilir, o vurus tur sonuna kayar
                onceki = vurus_liste[-1]
                onceki[0] = round(math.ceil(kes_son * FPS - 1e-6) / FPS, 6)
                onceki[2] = son_k[2]
                onceki[3] += len(g)
                for k_ in kesimler:
                    if len(k_) == 5 and abs(k_[4] - onceki_v) < 1e-6:
                        k_[4] = onceki[0]
                for idx in g:
                    kesimler[idx].append(onceki[0])
                onceki_v = onceki[0]
                continue
            vt = min(vt, math.ceil(kes_son * FPS - 1e-6) / FPS)
            onceki_v = vt
            vurus_liste.append([round(vt, 6), son_k[1], son_k[2], len(g)])
            for idx in g:
                kesimler[idx].append(round(vt, 6))  # 5. alan: bu kesimin goruldugu vurus ani
        dilim = dilim_say(m, cx, cy, cz)
        turlar.append({
            "bas": round(bas, 4), "kes_bas": round(kes_bas, 4), "kes_son": round(kes_son, 4),
            "son": round(son, 4), "n": n, "cx": cx, "cy": cy, "cz": cz,
            "kup": int(dilim.sum()), "dilim": dilim.tolist(), "kesimler": kesimler, "vuruslar": vurus_liste,
        })
        t = son
    assert abs(t - SURE) < 1e-6, t
    return {"meyve": meyve, "fps": FPS, "sure": SURE, "kare": int(SURE * FPS), "sekil": m,
            "fmax": meyve_fmax(m), "turlar": turlar}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--meyve", default="avokado")
    ap.add_argument("--cikti", required=True)
    a = ap.parse_args()
    p = plan_kur(a.meyve)
    with open(a.cikti, "w", encoding="utf-8") as f:
        json.dump(p, f, ensure_ascii=False)
    for tr in p["turlar"]:
        print(f"tur {tr['bas']:5.1f}-{tr['son']:5.1f}s  kesim {tr['n']:4d}  ({tr['cx']},{tr['cy']},{tr['cz']})  kup {tr['kup']:,}")
