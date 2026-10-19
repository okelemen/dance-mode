"""TETRIS MODE 5. video KAPAK - 3 kisilik grup siluetleri (REF-056 kapagindaki gibi uc kisi birbirine deger; hareketler FARKLI).

    python kapak-grup-kur-05.py   -> kapak-grup-05.json (varlik.py --mod cadi --yalniz kapak2 okur)

Kullanici 19 Eki 2026: "referans kanalin kapagi cok iyi ... o ne yaptiysa aynisini yap ama siluetin hareketleri farkli olsun".
REF-056 kapaginda: uc kisi sarilmis, ortadaki dizini kaldirmis (sakin). Bizde dikkat ceken, hareketli Halloween pozlari; kurallar §14c:
kameraya donuk, yanlar ayna (simetri), ic eller/kollar ortadakine deger.
"""
import json, os

BURA = os.path.dirname(os.path.abspath(__file__))
_k = open(os.path.join(BURA, "grup-listesi-kur-05.py"), encoding="utf-8").read().split(chr(10) + "TUR1 = [")[0]
_g = {"__file__": os.path.join(BURA, "grup-listesi-kur-05.py")}
exec(compile(_k, "grup-listesi-kur-05.py", "exec"), _g)
on, grup = _g["on"], _g["grup"]

G = {
    # A - "Parti": ortada genis V kollar + derin goddess; yanlar DISA derin hamle, ic kol yukari ortadakinin eline, dis kol asagi-disa
    "a": grup("Halloween Party", on("", "lowv", "v", "lunge", "tog", govde=170), on("", "v", "v", "goddess", "goddess")),
    # B - "Yarasa kanadi": yanlar ice egilip ic eli ortadakinin omzuna koyar, dis kol yarasa kanadi (W), dis diz yukari;
    #     ortada W kanat kollar + goddess
    "b": grup("Bat Wing Hug", on("", "w", [105, 105], "kneeup", "tog", govde=165), on("", "w", "w", "goddess", "goddess"),
              temas=("el", "omuz")),
}
for k, g in G.items():
    for i, f in enumerate(g["figurler"]):
        f["ad"] = f"{g['ad']} {'ABC'[i]}"
json.dump({"_not": "Kapak grup pozlari (5. video). Figurler soldan saga; temas [sol eklem, sag eklem] ya da 'yan'.", "gruplar": G},
          open(os.path.join(BURA, "kapak-grup-05.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("kapak-grup-05.json:", list(G))
