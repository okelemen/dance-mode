"""POZ DUVARI - bolum JSON'u uretir: kartlar, duvarlar, koc cumleleri (tek kaynak).

Sahne (sahne3.html) gorseli, koc-sesi.py konusmayi, efekt.py efektleri ayni
JSON'dan kurar; boylece ses ile goruntu ayni zaman cizelgesine bagli kalir.

    python poz-duvari/kesit-kur.py <cikti.json> --tam     # 80 duvar, ~9:50 (POSE WALL #1)
    python poz-duvari/kesit-kur.py <cikti.json> --kesit   # her turdan 3 duvar + kapanis

Yapi (16 Eki 2026, kullanici: "10 dakikalik ... hepsi birbirinden farkli"):
4 tur x 20 duvar, duvar 7 sn; poz no = duvar no (poz-defteri.md v2).
"""
import json, math, sys

BPM = 120                       # muzik yokken izgara; muzik gelince olculur ve degisir
OLCU = 60 / BPM * 4
DUVAR = 7.0                     # bir duvarin suresi (kesit 2: "tempoyu hizlandir")
# koc: poz adi (0,35) + kisa ipucu (1,25), ipucu penceresi 1,55 sn. Sayim 0,8 sn arayla.
ZAMAN = {"yaklas": 5.2, "goster": 0.3, "tut": 1.2, "gec": 0.4, "say": [2.8, 3.6, 4.4]}

TURLAR = [
    {"no": 1, "ad": "EASY", "renk": "#22d3ee"},
    {"no": 2, "ad": "MEDIUM", "renk": "#facc15"},
    {"no": 3, "ad": "HARD", "renk": "#fb923c"},
    {"no": 4, "ad": "FINAL", "renk": "#e879f9"},
]
TUR_KOC = {1: "Round one! Easy!", 2: "Round two! Medium!", 3: "Round three! Hard!", 4: "Final round!"}
OVGU = ["NICE!", "GREAT!", "PERFECT!", "AWESOME!", "SUPER!"]
OVGU_KOC = ["Nice!", "Great!", "Perfect!", "Awesome!", "Super!"]
TEMAS = {2, 5, 21, 22, 42, 43, 48, 62, 63, 79, 80}   # pozlar.js'deki temasli pozlar (efekt: kivilcim)

# no: (koc adi, ipucu) - ipucu <= ~1,5 sn konusma
KOC = {
    1: ("Star!", "Arms and legs wide!"), 2: ("High five!", "Touch hands up high!"),
    3: ("Rocket!", "Hands up high!"), 4: ("Mirror!", "Outside arm out!"),
    5: ("Big arch!", "Inside hands up!"), 6: ("Robot!", "One up, two down!"),
    7: ("Flamingo!", "Stand on one leg!"), 8: ("Scarecrow!", "Floppy arms!"),
    9: ("Point the way!", "Point up together!"), 10: ("Heart!", "Make a heart!"),
    11: ("Dino arms!", "Little arms, bend knees!"), 12: ("Goalkeeper!", "Wide and ready!"),
    13: ("Wave hello!", "Wave to your partner!"), 14: ("Muscles!", "Show your muscles!"),
    15: ("Thinking!", "Hand on chin!"), 16: ("Lean!", "Lean, arms up!"),
    17: ("Salute!", "Hand to forehead!"), 18: ("Step out!", "Big step, arms out!"),
    19: ("Hands on hips!", "Stand tall!"), 20: ("Disco!", "Point up, point down!"),
    21: ("Back to back!", "Backs together!"), 22: ("Bridge hands!", "Lean in, hands up!"),
    23: ("Low and high!", "One low, two tall!"), 24: ("Lunge twins!", "Lunge, arms up!"),
    25: ("Tree!", "Foot on knee!"), 26: ("Archer!", "Pull the bow!"),
    27: ("Teapot!", "Hand on hip, tip over!"), 28: ("Superhero!", "Fist up high!"),
    29: ("Side bend!", "Arm over, bend!"), 30: ("Knees!", "Hands on your knees!"),
    31: ("Side kick!", "Leg out to the side!"), 32: ("Surfer!", "Ride the wave!"),
    33: ("Windmill!", "One up, one down!"), 34: ("Take a bow!", "Bend forward!"),
    35: ("Runner!", "Knee up, arms swing!"), 36: ("Zombie!", "Arms out in front!"),
    37: ("Penguin!", "Flat hands out!"), 38: ("Cross legs!", "Cross and balance!"),
    39: ("Floor reach!", "Reach for the floor!"), 40: ("Fists up!", "Guard your face!"),
    41: ("Airplane!", "Leg out, wings out!"), 42: ("Wall sit!", "Backs together, sit!"),
    43: ("Leaning tower!", "Lean in, hands meet!"), 44: ("Warrior three!", "Tip forward, leg back!"),
    45: ("Dancer!", "Hold your foot!"), 46: ("Crab and tall!", "One crab, one tall!"),
    47: ("Ski jump!", "Knees bent, arms back!"), 48: ("Seesaw!", "One down, one leans!"),
    49: ("Side plank star!", "Plank and star!"), 50: ("Low lunge!", "Hands down, leg back!"),
    51: ("Chair!", "Sit back, arms up!"), 52: ("Half moon!", "Hand down, leg up!"),
    53: ("Knee hug!", "Hug one knee!"), 54: ("Side lunge!", "Lunge to the side!"),
    55: ("Superman!", "Lie down and fly!"), 56: ("Hips up!", "Lie back, lift hips!"),
    57: ("Mountain climber!", "Plank, knee in!"), 58: ("Down dog!", "Hips up high!"),
    59: ("Lunge twist!", "Lunge, arms wide!"), 60: ("Triangle!", "Hand to your leg!"),
    61: ("Statue!", "Freeze, knee up!"), 62: ("Tunnel!", "Make a tunnel!"),
    63: ("Boat!", "Sit, feet together!"), 64: ("Lightning!", "Zig zag arms!"),
    65: ("Table and chair!", "One table, one chair!"), 66: ("Skater!", "Leg back, swing!"),
    67: ("Fold down!", "Hands to ankles!"), 68: ("Thinker!", "One sits, one scratches!"),
    69: ("Frog!", "Squat, hands down!"), 70: ("Lunge punch!", "Lunge and punch!"),
    71: ("Warrior two!", "Bend and arms out!"), 72: ("Hero kneel!", "Kneel, arm up!"),
    73: ("Hand to toe!", "Leg up, reach!"), 74: ("Squat arms up!", "Squat, reach up!"),
    75: ("Toe touch!", "Sit and reach!"), 76: ("Bird dog!", "Arm and leg out!"),
    77: ("Rock star!", "Play the guitar!"), 78: ("Victory lunge!", "Lunge, arms up!"),
    79: ("Big hug!", "Arms around!"), 80: ("Champions!", "Hands up together!"),
}
assert len(KOC) == 80


def kur(dizi, son=True):
    """dizi: [(tur, [duvar_no, ...]), ...] - poz no = duvar no"""
    kartlar, duvarlar, koc = [], [], []
    kartlar += [
        {"t": 0.0, "sure": 2.5, "tip": "buyuk", "metin": "WELCOME", "alt": "POSE WALL", "renk": "#fb923c"},
        {"t": 2.5, "sure": 4.0, "tip": "nasil"},
        {"t": 6.5, "sure": 1.5, "tip": "buyuk", "metin": "READY?", "renk": "#4ade80"},
    ]
    koc += [
        {"t": 0.3, "metin": "Welcome to Pose Wall!"},
        {"t": 2.6, "metin": "Player one, pink wall. Player two, blue wall."},
        {"t": 5.2, "metin": "Match your pose!"},
        {"t": 6.6, "metin": "Ready?"},
    ]
    t = 8.0
    sayac = 0
    abone = []          # SUBSCRIBE hatirlatmasi: her 2 duvarda bir (14 sn), poz acildiktan sonra
    for tur, liste in dizi:
        kartlar.append({"t": t, "sure": 2.5, "tip": "tur", "tur": tur, "metin": f"ROUND {tur}"})
        koc.append({"t": t + 0.3, "metin": TUR_KOC[tur]})
        t += 2.5
        for no in liste:
            ad, ipucu = KOC[no]
            o = sayac % len(OVGU)
            duvarlar.append({"no": no, "poz": no, "tur": tur, "t0": round(t, 3), "sure": DUVAR,
                             "ovgu": OVGU[o], **({"temas": True} if no in TEMAS else {})})
            koc.append({"t": round(t + 0.35, 3), "metin": ad})
            if ipucu:
                koc.append({"t": round(t + 1.25, 3), "metin": ipucu})
            for i, s in enumerate(ZAMAN["say"]):
                koc.append({"t": round(t + s + 0.05, 3), "metin": ["Three!", "Two!", "One!"][i], "kisa": True})
            koc.append({"t": round(t + ZAMAN["yaklas"] + 0.05, 3), "metin": "Hold it!", "kisa": True})
            koc.append({"t": round(t + ZAMAN["yaklas"] + ZAMAN["tut"] + 0.1, 3), "metin": OVGU_KOC[o], "kisa": True})
            if sayac % 2 == 1:
                abone.append(round(t + 0.6, 3))
            t += DUVAR
            sayac += 1
    if son:
        kartlar.append({"t": round(t, 3), "sure": 7.0, "tip": "son", "metin": "CHALLENGE", "alt": "COMPLETE!"})
        koc.append({"t": round(t + 0.3, 3), "metin": "Challenge complete! Amazing teamwork!"})
        koc.append({"t": round(t + 3.6, 3), "metin": "Subscribe for the next wall!"})
        t += 7.0
    olcu = math.ceil(t / OLCU)
    return {
        "seri": "POSE WALL", "bolum": "pose-wall-01", "bpm": BPM, "toplam_olcu": olcu,
        "toplam_duvar": 80, "zaman": ZAMAN, "turlar": TURLAR,
        "kartlar": kartlar, "duvarlar": duvarlar, "koc": koc, "abone": abone, "abone_sure": 3.0,
        "_not": "POZ DUVARI. Uretici: 03-motor/poz-duvari/kesit-kur.py",
    }


if __name__ == "__main__":
    cikti = sys.argv[1]
    if "--tam" in sys.argv:
        dizi = [(tur, list(range((tur - 1) * 20 + 1, tur * 20 + 1))) for tur in (1, 2, 3, 4)]
    elif "--kesit" in sys.argv:
        # her turdan 3 duvar: temasli, yer ve profil pozlari dahil (kesit 3, 16 Eki 2026)
        dizi = [(1, [1, 2, 7]), (2, [21, 24, 35]), (3, [46, 55, 58]), (4, [63, 76, 80])]
    else:
        raise SystemExit("--tam ya da --kesit")
    b = kur(dizi)
    with open(cikti, "w", encoding="utf-8") as f:
        json.dump(b, f, ensure_ascii=False, indent=1)
    print(f"{cikti}: {len(b['duvarlar'])} duvar, {len(b['koc'])} koc cumlesi, "
          f"{b['toplam_olcu']} olcu = {b['toplam_olcu'] * OLCU:.1f} sn")
