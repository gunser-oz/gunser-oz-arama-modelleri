"""
Bir klasördeki belgeleri (pdf, docx, txt, md, html) parçalara böler, vektöre çevirir
ve FAISS indeksi olarak kaydeder. Sunucu bu indeksi okur.

  python deneme/indeksle.py --klasor belgelerim --indeks deneme/indeks
  python deneme/indeksle.py --klasor belgelerim --indeks deneme/indeks --model cikti/e5-small-mmarco-tr/final
"""
import argparse
import json
import re
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
TEMEL_MODEL = KOK / "modeller" / "intfloat-multilingual-e5-small"
UZANTILAR = {".pdf", ".docx", ".txt", ".md", ".html", ".htm"}


def metin_cikar(yol: Path) -> str:
    u = yol.suffix.lower()
    if u == ".pdf":
        from pypdf import PdfReader
        return "\n".join((s.extract_text() or "") for s in PdfReader(str(yol)).pages)
    if u == ".docx":
        import docx
        return "\n".join(p.text for p in docx.Document(str(yol)).paragraphs)
    if u in (".html", ".htm"):
        ham = yol.read_text(encoding="utf-8", errors="ignore")
        ham = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", ham, flags=re.S | re.I)
        return re.sub(r"<[^>]+>", " ", ham)
    return yol.read_text(encoding="utf-8", errors="ignore")


def parcala(metin: str, boy=700, bindirme=100):
    """Cümle sınırlarına saygılı, yaklaşık `boy` karakterlik parçalar."""
    metin = re.sub(r"\s+", " ", metin).strip()
    if not metin:
        return []
    cumleler = re.split(r"(?<=[.!?])\s+", metin)
    parcalar, simdiki = [], ""
    for c in cumleler:
        if len(simdiki) + len(c) > boy and simdiki:
            parcalar.append(simdiki.strip())
            simdiki = simdiki[-bindirme:] + " " + c
        else:
            simdiki += " " + c
    if simdiki.strip():
        parcalar.append(simdiki.strip())
    return parcalar


def main():
    # Ağır kütüphaneler yalnızca indeksleme yapılırken yüklenir (metin_cikar.py bu dosyayı içe aktarır)
    import faiss
    import numpy as np
    from sentence_transformers import SentenceTransformer

    p = argparse.ArgumentParser()
    p.add_argument("--klasor", required=True)
    p.add_argument("--indeks", default=str(KOK / "deneme" / "indeks"))
    p.add_argument("--model", default=str(TEMEL_MODEL))
    p.add_argument("--parca-boyu", type=int, default=700)
    p.add_argument("--dosya-sinir", type=int, default=0, help="Dosya başına en çok bu kadar karakter indekslenir (0 = sınırsız)")
    a = p.parse_args()

    dosyalar = sorted(f for f in Path(a.klasor).rglob("*") if f.suffix.lower() in UZANTILAR)
    if not dosyalar:
        sys.exit(f"{a.klasor} içinde desteklenen belge yok ({', '.join(sorted(UZANTILAR))})")

    kayitlar = []
    for f in dosyalar:
        try:
            metin = metin_cikar(f)
            if a.dosya_sinir and len(metin) > a.dosya_sinir:
                metin = metin[: a.dosya_sinir]
            parcalar = parcala(metin, a.parca_boyu)
        except Exception as e:
            print(f"Atlandı {f}: {e}", file=sys.stderr)
            continue
        for i, metin in enumerate(parcalar):
            ad = str(f.relative_to(a.klasor))
            if ad.endswith(".txt") and ad.count(".") >= 2:
                ad = ad[:-4]  # metin_cikar.py çıktısı: "karar.pdf.txt" -> "karar.pdf"
            kayitlar.append({"dosya": ad, "parca": i, "metin": metin})
        print(f"{f.name}: {len(parcalar)} parça", file=sys.stderr)

    model = SentenceTransformer(a.model)
    model.max_seq_length = 512
    vek = model.encode(["passage: " + k["metin"] for k in kayitlar],
                       batch_size=32, normalize_embeddings=True, show_progress_bar=True)
    vek = np.asarray(vek, dtype="float32")

    indeks = faiss.IndexFlatIP(vek.shape[1])  # normalize vektörlerde iç çarpım = kosinüs
    indeks.add(vek)

    cikti = Path(a.indeks)
    cikti.mkdir(parents=True, exist_ok=True)
    faiss.write_index(indeks, str(cikti / "vektorler.faiss"))
    with open(cikti / "kayitlar.jsonl", "w", encoding="utf-8") as fh:
        for k in kayitlar:
            fh.write(json.dumps(k, ensure_ascii=False) + "\n")
    (cikti / "bilgi.json").write_text(json.dumps(
        {"model": a.model, "dosya_sayisi": len(dosyalar), "parca_sayisi": len(kayitlar)},
        ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"İndeks yazıldı: {cikti} ({len(dosyalar)} dosya, {len(kayitlar)} parça)", file=sys.stderr)


if __name__ == "__main__":
    main()
