"""
Parça metinlerinden kanun maddesi atıflarını çıkarır ve tarayıcı için küçük bir dizin yazar.
Tanınanlar (egitim/kanunlar.json tek kaynaktır):
  - kısaltma + madde: "TCK 181", "TCK'nın 181. maddesi", "HMK m. 166", "İİK md. 67"
  - tam ad + madde:   "Türk Ceza Kanunu'nun 181. maddesi"
  - numara + madde:   "5237 sayılı Kanun'un 181. maddesi"
  - bilinmeyen K ile biten kısaltmalar: "KVKK 12" -> "kvkk:12" (genel kural)
  - geçici/ek madde:  "geçici 1. madde" -> "gecici:1"
  - yalnız madde:     "181. madde" -> "madde:181"

  python egitim/atif_indeksi.py --veri web/veri   -> web/veri/atif.json (+ kanunlar.json kopyası)
"""
import argparse
import json
import re
import shutil
from collections import defaultdict
from pathlib import Path

KANUNLAR = json.load(open(Path(__file__).resolve().parent / "kanunlar.json", encoding="utf-8"))
NO2KIS = {v["no"]: k for k, v in KANUNLAR.items() if v["no"]}
AD2KIS = {ad: k for k, v in KANUNLAR.items() for ad in v["adlar"]}
AD2KIS_KUCUK = {ad.lower(): k for ad, k in AD2KIS.items()}
KANUN_NOLARI = set(NO2KIS)


def kucult(k: str) -> str:
    k = k.replace("İ", "i").replace("I", "i").lower()
    return k.replace("ı", "i").replace("ş", "s").replace("ü", "u").replace("ö", "o").replace("ç", "c").replace("ğ", "g")


# Kısaltma: iki ile sekiz büyük harf, K ile biten (kanun) veya bilinen özel adlar; noktalı yazım da olur (T.C.K.)
KIS = r"((?:[A-ZÇĞİÖŞÜ]\.?){1,7}K\.?|AİHS|Anayasa|AY|İş\s?K(?:anunu)?)"
EK = r"(?:'?[nN][ıiuü]n|'?nda|'?nde|'?na|'?ne|'?ya|'?ye)?"
MADDE = r"\s*(?:(m(?:adde(?:si|sinin|sinde|sine)?|d)?)\.?\s*)?(?:(geçici|ek)\s*)?(\d{1,4})(?!\d)(?:\s*[./]\s*\d{1,2})?"
AD_DESENI = "|".join(sorted((re.escape(a) for a in AD2KIS), key=len, reverse=True))
DESENLER = [
    (re.compile(r"\b" + KIS + EK + MADDE, re.U), "kis"),
    (re.compile(r"\b(" + AD_DESENI + r")" + EK + r"[^.\d]{0,20}?" + MADDE, re.U | re.I), "ad"),
    (re.compile(r"\b(\d{3,4})\s*sayılı\s*(?:Türk\s+)?[\w' ]{0,50}?(?:Kanun|Yasa|Sözleşme)[^.\d]{0,30}?" + MADDE, re.U | re.I), "no"),
    (re.compile(r"\b(?:(geçici|ek)\s*)?(\d{1,4})\s*\.?\s*(?:madde|md)\b|\bmadde\s*(\d{1,4})\b", re.U | re.I), "madde"),
]


def kisaltma_anahtari(ham: str) -> str:
    k = kucult(ham.replace(".", "").replace(" ", ""))
    return {"iskanunu": "isk", "ay": "anayasa"}.get(k, k)


def _on_ek(tip):
    return "gecici_" if tip and kucult(tip).startswith("ge") else "ek_" if tip else ""


def atiflar(metin: str, sorgu: bool = False):
    """sorgu=True: kullanıcı sorgusu; küçük harfli kısaltmalar da ('tck 181') tanınır."""
    cikti = set()
    for desen, tur in DESENLER:
        if tur == "kis" and sorgu:
            desen = re.compile(desen.pattern, re.U | re.I)
        for e in desen.finditer(metin):
            g = e.groups()
            if tur in ("kis", "ad", "no"):
                madde_kelimesi, tip, no = g[1], g[2], g[3]
                # "4054 sayılı RKHK" gibi yazımlarda sayı madde değil kanun numarasıdır; "madde" kelimesi yoksa atla
                if not madde_kelimesi and not tip and no in KANUN_NOLARI:
                    continue
                if tur == "kis":
                    kis = kisaltma_anahtari(g[0])
                elif tur == "ad":
                    kis = AD2KIS.get(g[0]) or AD2KIS_KUCUK.get(g[0].lower(), "kanun")
                else:
                    kis = NO2KIS.get(g[0], "kanun" + g[0])
                cikti.add(f"{kis}:{_on_ek(tip)}{int(no)}")
            else:
                tip, no, no2 = g
                n = int(no or no2)
                cikti.add(f"{'gecici' if tip and kucult(tip).startswith('ge') else 'ek' if tip else 'madde'}:{n}")
    return cikti


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--veri", default="web/veri")
    a = p.parse_args()
    veri = Path(a.veri)
    meta = json.load(open(veri / "meta.json", encoding="utf-8"))
    grup = meta["grup"]
    dizin = defaultdict(list)
    for dosya in sorted((veri / "metin").glob("*.json")):
        g = int(dosya.stem)
        for j, metin in enumerate(json.load(open(dosya, encoding="utf-8"))):
            for anahtar in atiflar(metin):
                dizin[anahtar].append(g * grup + j)
    json.dump(dizin, open(veri / "atif.json", "w", encoding="utf-8"), separators=(",", ":"))
    shutil.copy(Path(__file__).resolve().parent / "kanunlar.json", veri / "kanunlar.json")
    ornek = sorted(((k, len(v)) for k, v in dizin.items() if not k.startswith("madde:")), key=lambda x: -x[1])[:12]
    print(f"{len(dizin)} atıf anahtarı, {sum(len(v) for v in dizin.values())} eşleme, {(veri/'atif.json').stat().st_size/1e6:.1f} MB")
    print("en sık (madde: hariç):", ornek)


if __name__ == "__main__":
    main()
