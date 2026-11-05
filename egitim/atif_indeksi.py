"""
Parça metinlerinden kanun maddesi atıflarını çıkarır ve tarayıcı için küçük bir dizin yazar.
"TCK 181", "TCK'nın 181. maddesi", "TCK m. 181", "5237 sayılı Kanun'un 181. maddesi",
"181. madde" gibi ifadeler "tck:181" / "madde:181" anahtarlarına bağlanır.

  python egitim/atif_indeksi.py --veri web/veri        -> web/veri/atif.json
"""
import argparse
import json
import re
from collections import defaultdict
from pathlib import Path

# Kanun numarası -> kısaltma
KANUN_NO = {
    "5237": "tck", "5271": "cmk", "6100": "hmk", "4721": "tmk", "6098": "tbk", "6102": "ttk",
    "2004": "iik", "4857": "isk", "2577": "iyuk", "213": "vuk", "6698": "kvkk", "6502": "tkhk",
    "1086": "humk", "5510": "sgk", "4734": "kik", "4054": "rkhk", "2709": "anayasa", "5275": "ceza_infaz",
    "6284": "ailenin_korunmasi", "2918": "ktk", "3194": "imar", "6183": "aatuhk", "193": "gvk", "5520": "kvk",
    "3065": "kdv", "6769": "smk", "5846": "fsek", "4982": "bilgi_edinme", "7201": "tebligat", "5393": "belediye",
    "657": "dmk", "2577": "iyuk", "6325": "arabuluculuk", "4686": "tahkim", "5607": "kacakcilik", "3713": "tmk_terorle",
}
KISALTMA = r"(?:T\.?C\.?K|C\.?M\.?K|H\.?M\.?K|T\.?M\.?K|T\.?B\.?K|T\.?T\.?K|İ\.?İ\.?K|H\.?U\.?M\.?K|İ\.?Y\.?U\.?K|V\.?U\.?K|K\.?V\.?K\.?K|T\.?K\.?H\.?K|S\.?M\.?K|F\.?S\.?E\.?K|K\.?T\.?K|A\.?A\.?T\.?U\.?H\.?K|G\.?V\.?K|K\.?V\.?K|K\.?İ\.?K|R\.?K\.?H\.?K|D\.?M\.?K|İş\s?K(?:anunu)?|AİHS|Anayasa)"
MADDE = r"(?:'?[nN]ın|'?[nN]in|'?[nN]un|'?[nN]ün|'?nda|'?nde)?\s*(?:m(?:adde(?:si|sinin|sinde)?|d)?\.?\s*)?(\d{1,4})(?:\s*[./]\s*\d{1,2})?(?:\s*\.?\s*(?:madde|md|m)\b)?"
DESENLER = [
    (re.compile(rf"\b({KISALTMA})" + MADDE, re.I), "kisaltma"),
    (re.compile(r"\b(\d{3,4})\s*sayılı\s*(?:Türk\s+)?[\w' ]{0,40}?(?:Kanun|Yasa)[^.\d]{0,30}?(\d{1,4})\s*\.?\s*(?:madde|md|m)", re.I), "kanun_no"),
    (re.compile(r"\b(\d{1,4})\s*\.?\s*madde(?:si|sinin|sinde|ye|yi)?\b", re.I), "madde"),
    (re.compile(r"\bmadde\s*(\d{1,4})\b", re.I), "madde"),
]


def kisalt(k: str) -> str:
    k = k.replace(".", "").replace(" ", "").replace("İ", "i").replace("I", "i").lower()
    k = k.replace("ı", "i").replace("ş", "s").replace("ü", "u").replace("ö", "o").replace("ç", "c").replace("ğ", "g")
    return {"iskanunu": "isk", "aihs": "aihs", "anayasa": "anayasa"}.get(k, k)


def atiflar(metin: str):
    cikti = set()
    for desen, tur in DESENLER:
        for e in desen.finditer(metin):
            if tur == "kisaltma":
                cikti.add(f"{kisalt(e.group(1))}:{int(e.group(2))}")
            elif tur == "kanun_no":
                ad = KANUN_NO.get(e.group(1), "kanun" + e.group(1))
                cikti.add(f"{ad}:{int(e.group(2))}")
            else:
                cikti.add(f"madde:{int(e.group(1))}")
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
    ornek = sorted(dizin.items(), key=lambda x: -len(x[1]))[:8]
    print(f"{len(dizin)} atıf anahtarı, {sum(len(v) for v in dizin.values())} eşleme, {(veri/'atif.json').stat().st_size/1e6:.1f} MB")
    print("en sık:", [(k, len(v)) for k, v in ornek])
    print("tck:181 ->", len(dizin.get("tck:181", [])), "parça")


if __name__ == "__main__":
    main()
