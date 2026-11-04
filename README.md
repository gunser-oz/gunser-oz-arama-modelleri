# Günser Öz Arama Modelleri

Türkçe destekli anlamsal arama için `intfloat/multilingual-e5-small` gömme modeli,
Türkçe ince ayar betiği ve tarayıcıdan deneme sayfası.

## Kurulum

```bash
git lfs pull
pip install -r requirements.txt
```

## Deneme sayfası

```bash
python deneme/sunucu.py
```

Tarayıcıda `http://localhost:8000` açın. Anlamsal arama ve iki metin benzerliği sekmeleri var.
Aranan belgeler `deneme/belgeler.txt` dosyasından okunur; her satır bir belgedir, kendi metinlerinizi koyabilirsiniz.

## Türkçe ince ayar

Veri: JSONL, her satırda `anchor` (sorgu), `positive` (ilgili belge), isteğe bağlı `negative` (ilgisiz belge).
Örnek: `egitim/veri_ornek.jsonl`.

```bash
python egitim/egit.py --veri egitim/veri_ornek.jsonl --cikti cikti/e5-small-tr --epoch 2
```

İnce ayarlı modeli temel modelle yan yana denemek için:

```bash
python deneme/sunucu.py --karsilastir cikti/e5-small-tr/final
```

Notlar:
- Öneklerle (`query: `, `passage: `) eğitim ve çıkarım betiklerde otomatik yapılır.
- Küçük öğrenme oranı ve 1 ile 3 epoch yeterlidir; fazlası modelin genel bilgisini bozar.
- Örnek veri sadece akışı göstermek içindir. Gerçek iyileşme için binlerce gerçek sorgu-belge çifti gerekir.
