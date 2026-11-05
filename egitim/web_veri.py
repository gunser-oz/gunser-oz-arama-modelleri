"""
FAISS indeksini tarayıcı sayfasının (web/) okuduğu küçük dosyalara çevirir.

  - veri/vektorler.i8   : her vektör 8 bit tam sayıya sıkıştırılmış (384 bayt/parça)
  - veri/olcek.f16      : her vektörün geri çevirme çarpanı
  - veri/meta.json      : parça -> dosya adı eşlemesi (metin yok, küçük kalır)
  - veri/metin/NNNN.json: 200'er parçalık metin grupları; sayfa sadece gerekenleri çeker

  python egitim/web_veri.py --indeks deneme/indeks --cikti web/veri
"""
import argparse
import json
import shutil
from pathlib import Path

import faiss
import numpy as np

GRUP = 200


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--indeks", default="deneme/indeks")
    p.add_argument("--cikti", default="web/veri")
    a = p.parse_args()
    cikti = Path(a.cikti)
    shutil.rmtree(cikti, ignore_errors=True)
    (cikti / "metin").mkdir(parents=True)

    ind = faiss.read_index(str(Path(a.indeks) / "vektorler.faiss"))
    v = ind.reconstruct_n(0, ind.ntotal)
    olcek = np.abs(v).max(axis=1, keepdims=True) / 127.0
    olcek[olcek == 0] = 1
    np.round(v / olcek).astype("int8").tofile(cikti / "vektorler.i8")
    olcek.astype("float16").tofile(cikti / "olcek.f16")

    kay = [json.loads(s) for s in open(Path(a.indeks) / "kayitlar.jsonl", encoding="utf-8")]
    dosyalar = sorted({k["dosya"] for k in kay})
    dosya_no = {d: i for i, d in enumerate(dosyalar)}
    meta = {"boyut": int(ind.d), "adet": int(ind.ntotal), "grup": GRUP, "dosyalar": dosyalar,
            "dosya": [dosya_no[k["dosya"]] for k in kay]}
    json.dump(meta, open(cikti / "meta.json", "w", encoding="utf-8"), ensure_ascii=False)
    for g in range(0, len(kay), GRUP):
        json.dump([k["metin"] for k in kay[g:g + GRUP]], open(cikti / "metin" / f"{g // GRUP:04d}.json", "w", encoding="utf-8"), ensure_ascii=False)
    boyut = sum(f.stat().st_size for f in cikti.rglob("*") if f.is_file())
    print(f"{len(dosyalar)} dosya, {len(kay)} parça, toplam {boyut/1e6:.1f} MB -> {cikti}")


if __name__ == "__main__":
    main()
