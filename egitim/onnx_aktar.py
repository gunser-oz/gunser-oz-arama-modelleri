"""
Sentence-Transformers modelini tarayıcıda (Transformers.js) çalışacak ONNX biçimine çevirir
ve 8 bit nicemler. Çıktı düzeni Transformers.js'in beklediği gibidir:
  <cikti>/config.json, tokenizer.json, tokenizer_config.json, onnx/model.onnx, onnx/model_quantized.onnx

  python egitim/onnx_aktar.py --model cikti/e5-small-mmarco-tr/final --cikti web/model
"""
import argparse
import shutil
from pathlib import Path

import torch
from onnxruntime.quantization import QuantType, quantize_dynamic
from transformers import AutoModel, AutoTokenizer


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--model", required=True)
    p.add_argument("--cikti", required=True)
    a = p.parse_args()
    cikti = Path(a.cikti)
    (cikti / "onnx").mkdir(parents=True, exist_ok=True)

    tok = AutoTokenizer.from_pretrained(a.model)
    model = AutoModel.from_pretrained(a.model).eval()
    tok.save_pretrained(cikti)
    model.config.save_pretrained(cikti)

    class Sarmal(torch.nn.Module):
        """Anahtar kelimeli çağrıyı konumsal girdilere çevirir (ONNX dışa aktarımı için)."""
        def __init__(self, m):
            super().__init__(); self.m = m
        def forward(self, input_ids, attention_mask):
            return self.m(input_ids=input_ids, attention_mask=attention_mask).last_hidden_state

    ornek = tok(["query: deneme"], return_tensors="pt", padding=True)
    ham = cikti / "onnx" / "model.onnx"
    torch.onnx.export(
        Sarmal(model), (ornek["input_ids"], ornek["attention_mask"]), str(ham),
        input_names=["input_ids", "attention_mask"], output_names=["last_hidden_state"],
        dynamic_axes={"input_ids": {0: "batch", 1: "sequence"}, "attention_mask": {0: "batch", 1: "sequence"},
                      "last_hidden_state": {0: "batch", 1: "sequence"}},
        opset_version=17, dynamo=False,
    )
    quantize_dynamic(str(ham), str(cikti / "onnx" / "model_quantized.onnx"), weight_type=QuantType.QUInt8)
    for f in cikti.glob("onnx/*.onnx"):
        print(f, round(f.stat().st_size / 1e6, 1), "MB")
    # Doğrulama: ONNX ile ST aynı vektörü üretiyor mu?
    import numpy as np
    import onnxruntime as ort
    from sentence_transformers import SentenceTransformer
    st = SentenceTransformer(a.model)
    metin = "query: kira sözleşmesi feshi"
    ref = st.encode(metin, normalize_embeddings=True)
    oturum = ort.InferenceSession(str(cikti / "onnx" / "model_quantized.onnx"))
    g = tok([metin], return_tensors="np")
    cikis = oturum.run(None, {"input_ids": g["input_ids"], "attention_mask": g["attention_mask"]})[0]
    maske = g["attention_mask"][..., None]
    v = (cikis * maske).sum(1) / maske.sum(1)
    v = v[0] / np.linalg.norm(v[0])
    print("kosinus(ST, ONNX-int8) =", round(float(ref @ v), 4))


if __name__ == "__main__":
    main()
