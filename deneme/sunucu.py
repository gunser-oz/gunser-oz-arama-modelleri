"""
Modeli tarayıcıdan denemek için küçük bir sunucu.

  python deneme/sunucu.py                      # depodaki temel modeli yükler
  python deneme/sunucu.py --model cikti/e5-small-tr/final   # ince ayarlı modeli yükler
  python deneme/sunucu.py --karsilastir cikti/e5-small-tr/final  # ikisini yan yana
  python deneme/sunucu.py --indeks deneme/indeks   # indeksle.py ile kurulan FAISS indeksini kullanır

Sonra tarayıcıda http://localhost:8000 açın.
"""
import argparse
import json
from pathlib import Path

import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer

KOK = Path(__file__).resolve().parent.parent
BURASI = Path(__file__).resolve().parent
TEMEL_MODEL = KOK / "modeller" / "intfloat-multilingual-e5-small"

p = argparse.ArgumentParser()
p.add_argument("--model", default=str(TEMEL_MODEL))
p.add_argument("--karsilastir", default=None, help="İkinci model (ör. ince ayarlı)")
p.add_argument("--belgeler", default=str(BURASI / "belgeler.txt"))
p.add_argument("--indeks", default=None, help="indeksle.py çıktısı; verilirse --belgeler yok sayılır")
p.add_argument("--port", type=int, default=8000)
p.add_argument("--rapor", default=str(KOK / "cikti" / "degerlendirme.json"), help="degerlendir.py --rapor çıktısı")
a = p.parse_args()

if a.indeks:
    # indeksle.py ile hazırlanmış FAISS indeksi: belgeler ve vektörler diskten gelir
    import faiss
    kayitlar = [json.loads(s) for s in open(Path(a.indeks) / "kayitlar.jsonl", encoding="utf-8")]
    belgeler = [k["metin"] for k in kayitlar]
    kaynaklar = [k["dosya"] for k in kayitlar]
    bilgi = json.loads((Path(a.indeks) / "bilgi.json").read_text(encoding="utf-8"))
    modeller = {"temel": SentenceTransformer(bilgi["model"])}
    faiss_indeks = faiss.read_index(str(Path(a.indeks) / "vektorler.faiss"))
    indeks = None
    if a.karsilastir:
        # İnce ayarlı modelle aynı belgeleri yeniden vektörleyip ikinci bir FAISS indeksi kur
        import numpy as np
        m2 = SentenceTransformer(a.karsilastir)
        modeller["ince_ayar"] = m2
        v2 = np.asarray(m2.encode(["passage: " + b for b in belgeler], normalize_embeddings=True, batch_size=32), dtype="float32")
        faiss2 = faiss.IndexFlatIP(v2.shape[1]); faiss2.add(v2)
        faiss_indeksler = {"temel": faiss_indeks, "ince_ayar": faiss2}
    else:
        faiss_indeksler = {"temel": faiss_indeks}
else:
    belgeler = [s.strip() for s in Path(a.belgeler).read_text(encoding="utf-8").splitlines() if s.strip()]
    kaynaklar = [None] * len(belgeler)
    modeller = {"temel": SentenceTransformer(a.model)}
    if a.karsilastir:
        modeller["ince_ayar"] = SentenceTransformer(a.karsilastir)
    # Belgeleri bir kez vektöre çevir, her sorguda yeniden hesaplama
    indeks = {
        ad: m.encode(["passage: " + b for b in belgeler], normalize_embeddings=True, convert_to_tensor=True)
        for ad, m in modeller.items()
    }
    faiss_indeks = None

app = FastAPI()


class Sorgu(BaseModel):
    sorgu: str
    k: int = 5


class Cift(BaseModel):
    a: str
    b: str


@app.get("/")
def sayfa():
    return FileResponse(BURASI / "index.html")


@app.get("/kontrol")
def kontrol_sayfasi():
    return FileResponse(BURASI / "kontrol.html")


def _json_oku(yol):
    try:
        return json.loads(Path(yol).read_text(encoding="utf-8"))
    except Exception:
        return None


@app.get("/kontrol-veri")
def kontrol_veri():
    """Kontrol kartlarının okuduğu durum özeti."""
    agirlik = TEMEL_MODEL / "model.safetensors"
    lfs_cekilmis = agirlik.exists() and agirlik.stat().st_size > 1_000_000
    ozetler = {str(y.parent.parent.name): _json_oku(y) for y in (KOK / "cikti").glob("*/final/egitim_ozeti.json")} if (KOK / "cikti").exists() else {}
    rapor = _json_oku(a.rapor)
    ind = _json_oku(Path(a.indeks) / "bilgi.json") if a.indeks else None
    kontroller = [
        {"ad": "Model ağırlıkları indirildi (git lfs pull)", "durum": lfs_cekilmis},
        {"ad": "Sorgu/belge önekleri (query:, passage:) uygulanıyor", "durum": True},
        {"ad": "Eğitim verisi hazır (egitim/veri/*.jsonl)", "durum": any((KOK / "egitim" / "veri").glob("*.jsonl")) if (KOK / "egitim" / "veri").exists() else False},
        {"ad": "İnce ayar tamamlandı (cikti/*/final)", "durum": bool(ozetler)},
        {"ad": "Test kümesi eğitimden ayrıldı", "durum": any((o or {}).get("test_ayrilan", 0) > 0 for o in ozetler.values()) if ozetler else False},
        {"ad": "Değerlendirme raporu üretildi", "durum": rapor is not None},
        {"ad": "İnce ayarlı model temel modeli geçti (nDCG@10)", "durum": None},
        {"ad": "Belge indeksi kurulu (FAISS)", "durum": ind is not None},
    ]
    if rapor and len(rapor.get("modeller", {})) >= 2:
        degerler = [m["ndcg@10"] for m in rapor["modeller"].values()]
        kontroller[6]["durum"] = max(degerler[1:]) > degerler[0]
    return {
        "model": {"ad": "intfloat/multilingual-e5-small", "boyut": 384, "katman": 12, "maks_token": 512,
                  "yuklu": list(modeller), "belge_sayisi": len(belgeler)},
        "egitimler": ozetler, "degerlendirme": rapor, "indeks": ind, "kontroller": kontroller,
    }


@app.get("/bilgi")
def bilgi():
    return {"modeller": list(modeller), "belge_sayisi": len(belgeler),
            "dosya_sayisi": len(set(kaynaklar)) if a.indeks else None}


@app.post("/ara")
def ara(s: Sorgu):
    cikti = {}
    for ad, m in modeller.items():
        if faiss_indeks is not None:
            q = m.encode(["query: " + s.sorgu], normalize_embeddings=True)
            skor, idx = faiss_indeksler[ad].search(q.astype("float32"), s.k)
            ciftler = [(int(i), float(sk)) for i, sk in zip(idx[0], skor[0]) if i >= 0]
        else:
            q = m.encode("query: " + s.sorgu, normalize_embeddings=True, convert_to_tensor=True)
            skorlar = (indeks[ad] @ q).tolist()
            ciftler = [(i, skorlar[i]) for i in sorted(range(len(belgeler)), key=lambda i: -skorlar[i])[: s.k]]
        cikti[ad] = [{"belge": belgeler[i], "skor": round(sk, 4), "kaynak": kaynaklar[i]} for i, sk in ciftler]
    return cikti


@app.post("/benzerlik")
def benzerlik(c: Cift):
    cikti = {}
    for ad, m in modeller.items():
        v = m.encode(["query: " + c.a, "query: " + c.b], normalize_embeddings=True)
        cikti[ad] = round(float(v[0] @ v[1]), 4)
    return cikti


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=a.port)
