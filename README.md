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
python egitim/egit.py --veri mmarco_tr_100000.jsonl --cikti cikti/e5-small-mmarco-tr --test-ayir 5000 --epoch 1 --batch 64
```

Son 5000 satır eğitimde kullanılmaz, değerlendirme için ayrılır. CPU'da `--en-fazla 20000` ile sınırlayın.

### Değerlendirme

Temel modeli ve ince ayarlı modeli aynı test kümesinde karşılaştırır (nDCG@10, MRR@10, Recall@k):

```bash
python egitim/degerlendir.py --veri mmarco_tr_100000.jsonl --test 5000 --sorgu 1000 \
    --model modeller/intfloat-multilingual-e5-small --model cikti/e5-small-mmarco-tr/final
```

## Google Drive arşivini indeksleme

Drive'daki tüm belgeleri (binlerce karar) indekslemenin iki yolu vardır:

**Kendi makinenizde** (bir kez OAuth izni gerekir, adımlar `deneme/drive_indir.py` başında):

```bash
python deneme/drive_indir.py --klasor-id <klasör kimliği> --hedef belgelerim
python deneme/indeksle.py --klasor belgelerim --indeks deneme/indeks --model modeller/e5-small-mmarco-tr
python deneme/sunucu.py --indeks deneme/indeks
```

**GitHub Actions ile** ("Drive belgelerini indeksle" iş akışı): bir Google servis hesabı oluşturup JSON
anahtarını `GDRIVE_SERVIS_HESABI` adlı repo secret'ına koyun, Drive klasörünü servis hesabının
e-postasıyla paylaşın, iş akışını klasör kimliğiyle çalıştırın. İndeks `drive-indeks` release'ine yüklenir:

```bash
curl -L -o drive_indeks.tar.gz https://github.com/gunser-oz/gunser-oz-arama-modelleri/releases/download/drive-indeks/drive_indeks.tar.gz
tar -xzf drive_indeks.tar.gz && python deneme/sunucu.py --indeks indeks
```

## İnce ayarlı model

`modeller/e5-small-mmarco-tr/` Türkçe MS MARCO ile ince ayarlanmış sürümdür. Ağırlıklar GitHub'ın
100 MB sınırı yüzünden parçalı durur; kullanmadan önce birleştirin:

```bash
sh modeller/e5-small-mmarco-tr/birlestir.sh
```

## Web'den kullanım (Hugging Face Static Space, ücretsiz)

`web/` klasörü sunucusuz bir arama sayfasıdır: ince ayarlı model 8 bit ONNX olarak tarayıcıda çalışır,
indeks statik dosyadan okunur, sorgular hiçbir sunucuya gitmez. Hugging Face'te **Static** türünde,
**Private** bir Space açın; GitHub secret'larına `HF_TOKEN` (write) ve `HF_SPACE` (ör. `ozanser/arama`)
ekleyin. "Hugging Face Space'e yayınla" iş akışı `web/` her değiştiğinde sayfayı gönderir.

Yerelde denemek için:

```bash
sh web/birlestir.sh
cd web && python -m http.server 8003
```

Tarayıcı modelini ve verisini yeniden üretmek için:

```bash
python egitim/onnx_aktar.py --model modeller/e5-small-mmarco-tr --cikti web/model
```

## GPU'da eğitim (Google Colab, ücretsiz)

`egitim/colab_egitim.ipynb` defterini Colab'da açın, T4 GPU seçin ve hücreleri sırayla çalıştırın.
Tam veriyle eğitim yaklaşık 10 dakika sürer; sonuç `model-gpu` release'ine yüklenir.
Doğrudan açmak için: https://colab.research.google.com/github/gunser-oz/gunser-oz-arama-modelleri/blob/main/egitim/colab_egitim.ipynb

## Drive belgelerini zip ile indeksleme (önerilen)

Drive API ile toplu indirme Google'ın kötüye kullanım uyarılarını tetikleyebilir. Bunun yerine klasörü
Drive'dan elle indirin (sağ tık → İndir), zip'i `belgeler` adlı release'e ekleyin ve
"Belgeleri indeksle (release zip'inden)" iş akışını çalıştırın. İş akışı indeksi kurar, `web/veri`
klasörünü günceller ve main'e commit eder; ardından "Hugging Face Space'e yayınla" iş akışını çalıştırın.
