"""
multilingual-e5-small modelini Türkçe sorgu-belge çiftleriyle ince ayarlar.

Veri: JSONL, her satırda "anchor" (sorgu), "positive" (ilgili belge),
isteğe bağlı "negative" (ilgisiz belge). Önekler burada otomatik eklenir.

Kullanım:
  python egitim/egit.py --veri egitim/veri_ornek.jsonl --cikti cikti/e5-small-tr --epoch 2
"""
import argparse
import json
import time
from pathlib import Path

from datasets import load_dataset
from sentence_transformers import (
    SentenceTransformer,
    SentenceTransformerTrainer,
    SentenceTransformerTrainingArguments,
    losses,
)

KOK = Path(__file__).resolve().parent.parent
TEMEL_MODEL = KOK / "modeller" / "intfloat-multilingual-e5-small"


def onek_ekle(satir):
    satir["anchor"] = "query: " + satir["anchor"]
    satir["positive"] = "passage: " + satir["positive"]
    if satir.get("negative"):
        satir["negative"] = "passage: " + satir["negative"]
    return satir


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--veri", required=True, help="Eğitim JSONL dosyası")
    p.add_argument("--cikti", default="cikti/e5-small-tr")
    p.add_argument("--model", default=str(TEMEL_MODEL))
    p.add_argument("--epoch", type=float, default=2)
    p.add_argument("--batch", type=int, default=32)
    p.add_argument("--lr", type=float, default=2e-5)
    p.add_argument("--dogrulama-orani", type=float, default=0.1)
    p.add_argument("--test-ayir", type=int, default=0, help="Sondan bu kadar satırı hiç kullanma (degerlendir.py için)")
    p.add_argument("--en-fazla", type=int, default=0, help="En fazla bu kadar satırla eğit (0 = hepsi)")
    p.add_argument("--maks-uzunluk", type=int, default=256, help="Token cinsinden en uzun girdi")
    p.add_argument("--kaydet-adim", type=int, default=200, help="Bu kadar adımda bir ara kayıt (0 = kapalı)")
    p.add_argument("--fp16", action="store_true", help="GPU'da yarı hassasiyet (daha hızlı)")
    p.add_argument("--devam", default=None, help="Ara kayıt klasörü (ör. cikti/x/checkpoint-450); eğitime oradan devam eder")
    a = p.parse_args()

    model = SentenceTransformer(a.model)
    model.max_seq_length = a.maks_uzunluk
    ds = load_dataset("json", data_files=a.veri)["train"]
    if a.test_ayir:
        ds = ds.select(range(ds.num_rows - a.test_ayir))
    if a.en_fazla and ds.num_rows > a.en_fazla:
        ds = ds.select(range(a.en_fazla))
    ds = ds.map(onek_ekle)
    if "negative" in ds.column_names and ds.filter(lambda s: not s["negative"]).num_rows:
        ds = ds.remove_columns("negative")  # eksik negatif varsa sütunu bırak

    egitim, dogrulama = ds, None
    if a.dogrulama_orani > 0 and ds.num_rows >= 10:
        b = ds.train_test_split(test_size=a.dogrulama_orani, seed=42)
        egitim, dogrulama = b["train"], b["test"]

    # E5'in kendi eğitimiyle aynı yaklaşım: InfoNCE, batch içi negatifler
    kayip = losses.MultipleNegativesRankingLoss(model, scale=50)

    args = SentenceTransformerTrainingArguments(
        output_dir=a.cikti,
        num_train_epochs=a.epoch,
        per_device_train_batch_size=a.batch,
        learning_rate=a.lr,
        warmup_steps=0.1,  # oran olarak (transformers v5)
        fp16=a.fp16,
        batch_sampler="no_duplicates",
        eval_strategy="epoch" if dogrulama else "no",
        save_strategy="steps" if a.kaydet_adim else "no",
        save_steps=a.kaydet_adim or 500,
        save_total_limit=1,
        logging_steps=10,
        report_to="none",
    )
    trainer = SentenceTransformerTrainer(
        model=model, args=args, train_dataset=egitim, eval_dataset=dogrulama, loss=kayip
    )
    baslangic = time.time()
    sonuc = trainer.train(resume_from_checkpoint=a.devam)
    sure = time.time() - baslangic

    son = Path(a.cikti) / "final"
    model.save_pretrained(str(son))
    dogrulama_kaybi = None
    if dogrulama:
        kayitlar = [k for k in trainer.state.log_history if "eval_loss" in k]
        dogrulama_kaybi = [round(k["eval_loss"], 4) for k in kayitlar]
    ozet = {
        "temel_model": a.model,
        "veri": a.veri,
        "egitim_satiri": egitim.num_rows,
        "dogrulama_satiri": dogrulama.num_rows if dogrulama else 0,
        "test_ayrilan": a.test_ayir,
        "epoch": a.epoch,
        "batch": a.batch,
        "ogrenme_orani": a.lr,
        "maks_uzunluk": a.maks_uzunluk,
        "kayip": "MultipleNegativesRankingLoss (InfoNCE, scale=50)",
        "egitim_kaybi": round(sonuc.training_loss, 4),
        "dogrulama_kaybi": dogrulama_kaybi,
        "adim": sonuc.global_step,
        "sure_dk": round(sure / 60, 1),
        "tarih": time.strftime("%Y-%m-%d %H:%M"),
    }
    (son / "egitim_ozeti.json").write_text(json.dumps(ozet, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Model kaydedildi: {son}")


if __name__ == "__main__":
    main()
