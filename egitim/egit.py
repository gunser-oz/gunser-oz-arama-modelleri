"""
multilingual-e5-small modelini Türkçe sorgu-belge çiftleriyle ince ayarlar.

Veri: JSONL, her satırda "anchor" (sorgu), "positive" (ilgili belge),
isteğe bağlı "negative" (ilgisiz belge). Önekler burada otomatik eklenir.

Kullanım:
  python egitim/egit.py --veri egitim/veri_ornek.jsonl --cikti cikti/e5-small-tr --epoch 2
"""
import argparse
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
    a = p.parse_args()

    model = SentenceTransformer(a.model)
    ds = load_dataset("json", data_files=a.veri)["train"].map(onek_ekle)
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
        batch_sampler="no_duplicates",
        eval_strategy="epoch" if dogrulama else "no",
        save_strategy="no",
        logging_steps=10,
        report_to="none",
    )
    trainer = SentenceTransformerTrainer(
        model=model, args=args, train_dataset=egitim, eval_dataset=dogrulama, loss=kayip
    )
    trainer.train()

    son = Path(a.cikti) / "final"
    model.save_pretrained(str(son))
    print(f"Model kaydedildi: {son}")


if __name__ == "__main__":
    main()
