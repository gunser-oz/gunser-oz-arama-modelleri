"""
Türkçe MS MARCO çevirisinden eğitim JSONL'i üretir.

Not: unicamp-dl/mmarco setinde Türkçe YOKTUR. Türkçe için topluluk çevirileri kullanılır:
  - newmindai/ms-marco-turkish-triplets  (sorgu / ilgili pasaj / ilgisiz pasaj, varsayılan)
  - parsak/msmarco-tr                    (ham çeviri, sütunlar farklı olabilir)

Sütun adları kaynaktan kaynağa değiştiği için otomatik eşleştirilir.

Kullanım:
  python egitim/veri_mmarco.py --adet 100000 --cikti egitim/mmarco_tr.jsonl
  python egitim/veri_mmarco.py --kaynak parsak/msmarco-tr --adet 50000
"""
import argparse
import json
import sys
from pathlib import Path

from datasets import load_dataset

ADAYLAR = {
    "anchor": ["anchor", "query", "question", "sorgu", "soru", "queries"],
    "positive": ["positive", "pos", "positive_passage", "passage", "pozitif", "answer", "document"],
    "negative": ["negative", "neg", "negative_passage", "hard_negative", "negatif"],
}


def sutun_bul(sutunlar, hedef):
    kucuk = {s.lower(): s for s in sutunlar}
    for aday in ADAYLAR[hedef]:
        if aday in kucuk:
            return kucuk[aday]
    # kısmi eşleşme (ör. "positive_passages")
    for aday in ADAYLAR[hedef]:
        for s in kucuk:
            if aday in s:
                return kucuk[s]
    return None


def metin(deger):
    """Liste gelirse ilk elemanı, sözlük gelirse 'text' alanını al."""
    if isinstance(deger, list):
        deger = deger[0] if deger else None
    if isinstance(deger, dict):
        deger = deger.get("text") or deger.get("passage") or next(iter(deger.values()), None)
    return deger.strip() if isinstance(deger, str) else None


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--kaynak", default="newmindai/ms-marco-turkish-triplets")
    p.add_argument("--bolum", default="train")
    p.add_argument("--adet", type=int, default=100_000)
    p.add_argument("--cikti", default="egitim/mmarco_tr.jsonl")
    a = p.parse_args()

    print(f"Kaynak: {a.kaynak} ({a.bolum})", file=sys.stderr)
    ds = load_dataset(a.kaynak, split=a.bolum, streaming=True)
    ilk = next(iter(ds))
    sutunlar = list(ilk.keys())
    print(f"Sütunlar: {sutunlar}", file=sys.stderr)
    print(f"İlk satır: {json.dumps(ilk, ensure_ascii=False)[:500]}", file=sys.stderr)

    es = {h: sutun_bul(sutunlar, h) for h in ADAYLAR}
    print(f"Eşleme: {es}", file=sys.stderr)
    if not es["anchor"] or not es["positive"]:
        raise SystemExit("Sorgu veya pozitif pasaj sütunu bulunamadı; ADAYLAR listesini genişletin.")

    Path(a.cikti).parent.mkdir(parents=True, exist_ok=True)
    yazilan = atlanan = 0
    with open(a.cikti, "w", encoding="utf-8") as f:
        for satir in ds:
            if yazilan >= a.adet:
                break
            kayit = {"anchor": metin(satir[es["anchor"]]), "positive": metin(satir[es["positive"]])}
            if es["negative"]:
                neg = metin(satir[es["negative"]])
                if neg:
                    kayit["negative"] = neg
            if not kayit["anchor"] or not kayit["positive"]:
                atlanan += 1
                continue
            f.write(json.dumps(kayit, ensure_ascii=False) + "\n")
            yazilan += 1
    print(f"{yazilan} satır yazıldı, {atlanan} boş satır atlandı: {a.cikti}", file=sys.stderr)


if __name__ == "__main__":
    main()
