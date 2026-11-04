"""
Modeli tarayıcıdan denemek için küçük bir sunucu.

  python deneme/sunucu.py                      # depodaki temel modeli yükler
  python deneme/sunucu.py --model cikti/e5-small-tr/final   # ince ayarlı modeli yükler
  python deneme/sunucu.py --karsilastir cikti/e5-small-tr/final  # ikisini yan yana

Sonra tarayıcıda http://localhost:8000 açın.
"""
import argparse
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
p.add_argument("--port", type=int, default=8000)
a = p.parse_args()

belgeler = [s.strip() for s in Path(a.belgeler).read_text(encoding="utf-8").splitlines() if s.strip()]

modeller = {"temel": SentenceTransformer(a.model)}
if a.karsilastir:
    modeller["ince_ayar"] = SentenceTransformer(a.karsilastir)

# Belgeleri bir kez vektöre çevir, her sorguda yeniden hesaplama
indeks = {
    ad: m.encode(["passage: " + b for b in belgeler], normalize_embeddings=True, convert_to_tensor=True)
    for ad, m in modeller.items()
}

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


@app.get("/bilgi")
def bilgi():
    return {"modeller": list(modeller), "belge_sayisi": len(belgeler)}


@app.post("/ara")
def ara(s: Sorgu):
    cikti = {}
    for ad, m in modeller.items():
        q = m.encode("query: " + s.sorgu, normalize_embeddings=True, convert_to_tensor=True)
        skorlar = (indeks[ad] @ q).tolist()
        sirali = sorted(range(len(belgeler)), key=lambda i: -skorlar[i])[: s.k]
        cikti[ad] = [{"belge": belgeler[i], "skor": round(skorlar[i], 4)} for i in sirali]
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
