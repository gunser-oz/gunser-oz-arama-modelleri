"""
mMARCO Türkçe setini indirir ve egit.py'nin beklediği JSONL formatına çevirir.

Üç dosya iner (Hugging Face, unicamp-dl/mmarco):
  - Türkçe sorgular (~800k satır)
  - Türkçe pasaj koleksiyonu (~8.8M satır, ~1.3 GB)
  - sorgu / ilgili pasaj / ilgisiz pasaj kimlik üçlüleri

Kullanım:
  python egitim/veri_mmarco.py --adet 100000 --cikti egitim/mmarco_tr.jsonl

100k üçlü CPU'da birkaç saat, GPU'da yarım saat civarı eğitim demektir.
"""
import argparse
import csv
import json
import random
import sys
from pathlib import Path

from huggingface_hub import hf_hub_download

DEPO = "unicamp-dl/mmarco"
DOSYALAR = {
    "sorgular": "data/google/queries/train/turkish_queries.train.tsv",
    "koleksiyon": "data/google/collections/turkish_collection.tsv",
    "ucluler": "data/triples.train.ids.small.tsv",
}


def indir(ad):
    print(f"İndiriliyor: {DOSYALAR[ad]}", file=sys.stderr)
    return hf_hub_download(DEPO, DOSYALAR[ad], repo_type="dataset")


def tsv_oku(yol):
    with open(yol, encoding="utf-8", newline="") as f:
        for satir in csv.reader(f, delimiter="\t", quoting=csv.QUOTE_NONE):
            if len(satir) >= 2:
                yield satir[0], satir[1]


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--adet", type=int, default=100_000, help="Kaç üçlü alınacak")
    p.add_argument("--cikti", default="egitim/mmarco_tr.jsonl")
    p.add_argument("--atla", type=int, default=0, help="Üçlü dosyasında kaç satır atlanacak")
    a = p.parse_args()

    # 1) İlk N üçlüyü oku, hangi sorgu ve pasajların gerektiğini belirle
    ucluler = []
    with open(indir("ucluler"), encoding="utf-8") as f:
        for i, satir in enumerate(f):
            if i < a.atla:
                continue
            if len(ucluler) >= a.adet:
                break
            q, pos, neg = satir.rstrip("\n").split("\t")[:3]
            ucluler.append((q, pos, neg))
    gerekli_q = {q for q, _, _ in ucluler}
    gerekli_p = {pid for _, pos, neg in ucluler for pid in (pos, neg)}
    print(f"{len(ucluler)} üçlü, {len(gerekli_q)} sorgu, {len(gerekli_p)} pasaj gerekli", file=sys.stderr)

    # 2) Sadece gerekli sorgu ve pasajları belleğe al (koleksiyon tek geçişte taranır)
    sorgular = {k: v for k, v in tsv_oku(indir("sorgular")) if k in gerekli_q}
    pasajlar = {}
    for k, v in tsv_oku(indir("koleksiyon")):
        if k in gerekli_p:
            pasajlar[k] = v
            if len(pasajlar) == len(gerekli_p):
                break

    # 3) JSONL yaz
    random.seed(42)
    random.shuffle(ucluler)
    Path(a.cikti).parent.mkdir(parents=True, exist_ok=True)
    yazilan = 0
    with open(a.cikti, "w", encoding="utf-8") as f:
        for q, pos, neg in ucluler:
            if q not in sorgular or pos not in pasajlar or neg not in pasajlar:
                continue
            f.write(json.dumps(
                {"anchor": sorgular[q], "positive": pasajlar[pos], "negative": pasajlar[neg]},
                ensure_ascii=False) + "\n")
            yazilan += 1
    print(f"{yazilan} satır yazıldı: {a.cikti}", file=sys.stderr)


if __name__ == "__main__":
    main()
