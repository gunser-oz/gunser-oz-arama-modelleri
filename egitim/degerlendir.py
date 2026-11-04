"""
Bir veya daha fazla modeli aynı test kümesinde arama başarısıyla karşılaştırır.

Test kümesi: JSONL'in SON N satırı (eğitimde --test-ayir ile aynı N kullanılırsa
eğitim bu satırları görmez). Korpus = bu N satırın pozitif ve negatif pasajları,
sorgular = bunların ilk --sorgu kadarı.

  python egitim/degerlendir.py --veri egitim/veri/mmarco_tr_100000.jsonl --test 5000 \
      --model modeller/intfloat-multilingual-e5-small --model cikti/e5-small-mmarco-tr/final
"""
import argparse
import json

from sentence_transformers import SentenceTransformer
from sentence_transformers.evaluation import InformationRetrievalEvaluator


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--veri", required=True)
    p.add_argument("--test", type=int, default=5000, help="Sondan kaç satır korpusa girer")
    p.add_argument("--sorgu", type=int, default=1000, help="Bunların kaçı sorgu olarak kullanılır")
    p.add_argument("--model", action="append", required=True)
    a = p.parse_args()

    satirlar = [json.loads(s) for s in open(a.veri, encoding="utf-8")][-a.test:]
    sorgular, korpus, ilgili = {}, {}, {}
    pid = {}
    for i, s in enumerate(satirlar):
        q = f"q{i}"
        if i < a.sorgu:
            sorgular[q] = "query: " + s["anchor"]
        for metin in (s["positive"], s.get("negative")):
            if metin and metin not in pid:
                pid[metin] = f"p{len(pid)}"
                korpus[pid[metin]] = "passage: " + metin
        if i < a.sorgu:
            ilgili[q] = {pid[s["positive"]]}

    print(f"{len(sorgular)} sorgu, {len(korpus)} pasaj")
    ev = InformationRetrievalEvaluator(sorgular, korpus, ilgili, name="tr", show_progress_bar=False)
    for m in a.model:
        r = ev(SentenceTransformer(m))
        print(f"\n{m}")
        for k in ("tr_cosine_ndcg@10", "tr_cosine_mrr@10", "tr_cosine_recall@1", "tr_cosine_recall@10"):
            print(f"  {k.replace('tr_cosine_', ''):10s} {r[k]:.4f}")


if __name__ == "__main__":
    main()
