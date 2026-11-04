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

## Türkçe MS MARCO ile eğitim

Resmi mMARCO setinde Türkçe yoktur; topluluk çevirisi `newmindai/ms-marco-turkish-triplets` kullanılır
(sorgu, ilgili pasaj, ilgisiz pasaj). Makine çevirisi olduğu için bazı cümleler bozuk olabilir. Bir alt küme yeterlidir:

```bash
python egitim/veri_mmarco.py --adet 100000 --cikti egitim/mmarco_tr.jsonl
```

```bash
python egitim/egit.py --veri egitim/mmarco_tr.jsonl --cikti cikti/e5-small-mmarco-tr --epoch 1 --batch 64
```

Veri akış halinde okunur, sadece istenen kadarı iner. GPU yoksa `--adet 20000` ile başlayın.

### GitHub Actions ile veri hazırlama

Actions sekmesinde "Türkçe MS MARCO verisini hazırla" iş akışını çalıştırın. Hugging Face'ten veriyi
çekip JSONL üretir ve release'e ek olarak yükler.
Çıkan dosyayı indirip eğitimde kullanın:

```bash
gunzip mmarco_tr_100000.jsonl.gz
python egitim/egit.py --veri mmarco_tr_100000.jsonl --cikti cikti/e5-small-mmarco-tr --epoch 1 --batch 64
```
