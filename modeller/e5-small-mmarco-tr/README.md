---
tags:
- sentence-transformers
- sentence-similarity
- feature-extraction
- dense
- generated_from_trainer
- dataset_size:9800
- loss:MultipleNegativesRankingLoss
widget:
- source_sentence: 'query: bir llc için bir işletme sözleşmesi nedir'
  sentences:
  - 'passage: LLC İşletim Anlaşması. ''LLC İşletim Anlaşması'' nın DEFINITION''. Bir
    LLC İşletim Anlaşması, bir Sınırlı Sorumluluk Şirketi''nin (LLC) şartlarını sahiplerinin
    özel ihtiyaçlarına göre özelleştiren ve finansal ve işlevsel karar vermeyi yapılandırılmış
    bir şekilde ana hatlarıyla belirleyen bir belgedir.'
  - 'passage: Gri kurt (Canis lupus, evcil köpek ve dingo hariç), aynı zamanda kurt
    olarak da bilinir, Canidae ailesinin en büyük mevcut vahşi üyesidir.'
  - 'passage: .'
- source_sentence: 'query: Akran baskısı ne yapar'
  sentences:
  - 'passage: Zararlı akran baskısı ne anlama gelir? sigara içmek, kokain yapmak veya
    içmek ve orada birini ölüme yol açabilecek güzel şeyleri ikna etmek gibi bir başkasına
    zarar verebilecek akran baskısı Edit'
  - 'passage: Akran baskısı, başkalarını tutumlarını, değerlerini veya davranışlarını
    gruplara uymaya teşvik eden bir akran grubu, gözlemci veya birey üzerinde etkilidir.'
  - 'passage: Paraguay, Güney Amerika''daki gizli mücevherlerden biridir ve en ünlüsü
    Guarani kültürüne ve İsa''nın (resimde) ve Trinidad''ın dini kalıntılarına ev
    sahipliği yapmasıyla bilinir.'
- source_sentence: 'query: katot negatif'
  sentences:
  - 'passage: Avelox dozu, her 24 saatte bir 400 mg''dır (ya da intravenöz infüzyon
    olarak). Terapi süresi, Tablo 1''de açıklandığı gibi enfeksiyonun türüne bağlıdır.
    Tablo 1: Yetişkin Hastalarda Dozaj ve Terapinin Süresi.'
  - 'passage: 1 Katot negatif yüklü elektrottur. 2 Katot, katyonları veya pozitif
    yükü çeker. 3 Katot elektronların veya elektron vericisinin kaynağıdır. 4 Pozitif
    yükü kabul edebilir.'
  - 'passage: Sir Joseph John Thomson, bir İngiliz fizikçi, 1897 yılında elektronu
    keşfetti. Katot tüplerinde elektrik deşarjı üzerinde yapılan deneylerde, yük oranı
    için yüksek bir değere dikkat çekti. Onun...'
- source_sentence: 'query: yoğunluk için eş anlamlılar'
  sentences:
  - 'passage: Princeton WordNet(4.00 / 2 oy)Bu eşanlamlıları derecelendirin: 1 yoğunluk,
    yoğunluk(noun) birim büyüklüğü başına miktar. 2 konsantrasyon, yoğunluk, yoğunluk,
    sıkılık, kompaktlık(noun) birlikte kalabalık olmanın mekansal özelliği.'
  - 'passage: Mahamrityunjaya Mantra Hint Mitolojisi ve Maneviyat en iyi Mantra biri
    Lord Shiva aittir.Üç Hintçe dil kelimelerinin bir kombinasyonudur.yani Maha Büyük
    anlamına gelir, Mrityun Ölüm anlamına gelir ve Jaya zafere dönüşen veya ölüm üzerinde
    zafer anlamına gelir.'
  - 'passage: Bir çaba eşanlamlıları yapın. Üst bir çaba eşanlamlıları yapmak (sadece
    idioms) bir çatlak var, çip uzakta ve bir gitmek vermek.'
- source_sentence: 'query: dramaturjik sosyoloji tanımı'
  sentences:
  - 'passage: dramaturjik. Drama veya tiyatro ile ilgili veya: dramatik, dramaturjik,
    histrionik, histriyonik, teatral, tiyatro, tespih.'
  - 'passage: wikipedia/Cburnett. San Diego Hayvanat Bahçesi, 800''den fazla türden
    4.000''den fazla hayvanla dünyanın en ünlü hayvanat bahçelerinden biridir. 100
    dönümlük (40 ha) park alanı San Diego şehrinden kiralanmıştır.'
  - 'passage: Kırsal sosyoloji, tersine, metropol olmayan alanların analizidir. Tarım
    ve vahşi yaşam kırsal bölgelerde daha belirgin bir sosyal gerçek olma eğiliminde
    olduğundan, kırsal sosyologlar genellikle çevre sosyologları ile örtüşmektedir.
    Toplum sosyolojisi'
pipeline_tag: sentence-similarity
library_name: sentence-transformers
---

# SentenceTransformer

This is a [sentence-transformers](https://www.SBERT.net) model trained on the json dataset. It maps inputs to a 384-dimensional dense vector space and can be used for semantic textual similarity, semantic search, paraphrase mining, classification, clustering, and more.

## Model Details

### Model Description
- **Model Type:** Sentence Transformer
<!-- - **Base model:** [Unknown](https://huggingface.co/unknown) -->
- **Maximum Sequence Length:** 192 tokens
- **Output Dimensionality:** 384 dimensions
- **Similarity Function:** Cosine Similarity
- **Supported Modality:** Text
- **Training Dataset:**
    - json
<!-- - **Language:** Unknown -->
<!-- - **License:** Unknown -->

### Model Sources

- **Documentation:** [Sentence Transformers Documentation](https://sbert.net)
- **Repository:** [Sentence Transformers on GitHub](https://github.com/huggingface/sentence-transformers)
- **Hugging Face:** [Sentence Transformers on Hugging Face](https://huggingface.co/models?library=sentence-transformers)

### Full Model Architecture

```
SentenceTransformer(
  (0): Transformer({'transformer_task': 'feature-extraction', 'modality_config': {'text': {'method': 'forward', 'method_output_name': 'last_hidden_state'}}, 'module_output_name': 'token_embeddings', 'architecture': 'BertModel'})
  (1): Pooling({'embedding_dimension': 384, 'pooling_mode': 'mean', 'include_prompt': True})
  (2): Normalize({'module_input_name': 'sentence_embedding', 'module_output_name': 'sentence_embedding'})
)
```

## Usage

### Direct Usage (Sentence Transformers)

First install the Sentence Transformers library:

```bash
pip install -U sentence-transformers
```
Then you can load this model and run inference.
```python
from sentence_transformers import SentenceTransformer

# Download from the 🤗 Hub
model = SentenceTransformer("sentence_transformers_model_id")
# Run inference
sentences = [
    'query: dramaturjik sosyoloji tanımı',
    'passage: dramaturjik. Drama veya tiyatro ile ilgili veya: dramatik, dramaturjik, histrionik, histriyonik, teatral, tiyatro, tespih.',
    'passage: Kırsal sosyoloji, tersine, metropol olmayan alanların analizidir. Tarım ve vahşi yaşam kırsal bölgelerde daha belirgin bir sosyal gerçek olma eğiliminde olduğundan, kırsal sosyologlar genellikle çevre sosyologları ile örtüşmektedir. Toplum sosyolojisi',
]
embeddings = model.encode(sentences)
print(embeddings.shape)
# [3, 384]

# Get the similarity scores for the embeddings
similarities = model.similarity(embeddings, embeddings)
print(similarities)
# tensor([[1.0000, 0.6866, 0.5855],
#         [0.6866, 1.0000, 0.3722],
#         [0.5855, 0.3722, 1.0000]])
```
<!--
### Direct Usage (Transformers)

<details><summary>Click to see the direct usage in Transformers</summary>

</details>
-->

<!--
### Downstream Usage (Sentence Transformers)

You can finetune this model on your own dataset.

<details><summary>Click to expand</summary>

</details>
-->

<!--
### Out-of-Scope Use

*List how the model may foreseeably be misused and address what users ought not to do with the model.*
-->

<!--
## Bias, Risks and Limitations

*What are the known or foreseeable issues stemming from this model? You could also flag here known failure cases or weaknesses of the model.*
-->

<!--
### Recommendations

*What are recommendations with respect to the foreseeable issues? For example, filtering explicit content.*
-->

## Training Details

### Training Dataset

#### json

* Dataset: json
* Size: 9,800 training samples
* Columns: <code>anchor</code>, <code>positive</code>, and <code>negative</code>
* Approximate statistics based on the first 100 samples:
  |          | anchor                                                                            | positive                                                                            | negative                                                                            |
  |:---------|:----------------------------------------------------------------------------------|:------------------------------------------------------------------------------------|:------------------------------------------------------------------------------------|
  | type     | string                                                                            | string                                                                              | string                                                                              |
  | modality | text                                                                              | text                                                                                | text                                                                                |
  | details  | <ul><li>min: 8 tokens</li><li>mean: 13.42 tokens</li><li>max: 23 tokens</li></ul> | <ul><li>min: 35 tokens</li><li>mean: 79.71 tokens</li><li>max: 134 tokens</li></ul> | <ul><li>min: 27 tokens</li><li>mean: 80.36 tokens</li><li>max: 141 tokens</li></ul> |
* Samples:
  | anchor                                                               | positive                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          | negative                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
  |:---------------------------------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
  | <code>query: Bir nöronun dinlenme anındaki elektriksel durumu</code> | <code>passage: Nöron dinlendiğinde, sodyum iyonlarının hücreden dışarı taşınmasından ne sorumludur? Sodyum-potasyum pompası Bir nöronun zarı dinlendiğinde, konsantrasyon gradyanı sodyumu hareket ettirme eğilimindedir. Hücre ve elektrik gradyanı hücreyi hareket ettirme eğilimindedir.</code>                                                                                                                                                                                                                | <code>passage: Sinirsel impulslar, nöronlar boyunca hareket eden elektriksel sinyallerdir. Elektrik sinyalleri bir nörondan diğerine doğrudan gidemez. Sinyal, sinaps adı verilen, kimyasal formda hücreler arasındaki boşluğu geçer. Bir nöron, bir eylem potansiyeline (sinir impuls) yanıt olarak kimyasalları serbest bırakır. Bu kimyasallar, bir sonraki nörondaki bir etki potansiyelini uyarır ve bir sonraki nörondaki bir etki potansiyelini uyarır. Bu kimyasallar nörotransmitter olarak bilinir. Sinyal, bir sinaps olarak adlandırılan hücreler arasındaki boşluğu geçer.</code> |
  | <code>query: Araçta pas delikleri nasıl onarılır</code>              | <code>passage: Tamir edilecek olan deliğin çevresinden katı olmayan herhangi bir metali çıkarın. Delikten uzak tüm yönlerde 3 ila 4 inçlik bir mesafe boyunca herhangi bir boya ve astarı çıkarmak için kaba gri zımpara kağıdı kullanın. En iyi ve en uzun ömürlü onarım için, tüm paslar da kaldırılmalıdır. Bununla birlikte, bazı küçük pas çukurlarının kalabileceği muhtemeldir. Deliğin arkasında dolgu yapmak için naylon pencere ekranı kullanın ve otodan bir arka gövde oluşturun.</code>              | <code>passage: Onarımları karşılayacak araba sigortanız olsa bile, çoğu poliçe, onarımların geri kalanını ödemeden önce bir indirim ödemenizi gerektirir. Bir araba tamir kredisi, ödemek için yeterli nakit paranız yoksa, indirimi karşılamak için kullanılabilir. Araba tamir kredisi, bir araca yatırım yapıldığından, kişisel krediden farklıdır. Genellikle bakım onarım kredileri, aracı çalışır durumda tutan ancak bazı araba tamir tiplerinde onarımlar için olmalıdır.</code>                                                                                                       |
  | <code>query: habitat ve adaptasyon sincaplarının tanımı</code>       | <code>passage: Adaptasyon. Bir sincap yaşam tarzına son derece yararlı olan bir adaptasyon, arka bacaklarının anatomisidir. Sincaplar, önce bir ağaç kafasının aşağı inmesine izin veren arka ayaklarını döndürebilirler. Bu, predasyondan kaçınmanın yanı sıra, ağaçtan ağaca ulaşmak ve seyahat etmek için yararlıdır. daptasyon. Bir sincapın yaşam tarzına son derece faydalı olan bir adaptasyon, arka ayaklarının anatomisidir. Sincaplar, ilk olarak arka ayaklarının aşağısına dönmelerini sağlar.</code> | <code>passage: Bir uyarlama, mevcut işlevi için doğal seçilim tarafından üretilen bir özelliktir. Bu tanıma dayanarak belirli tahminler yapabiliriz (X belirli bir fonksiyon için bir uyarlama ise, o zaman bunu tahmin ederiz...) ve tahminlerimizin gözlemlerimizle uyuşup uyuşmadığını göreceğiz. Örnek olarak, hipotezi ele alacağız: tüyler kuş uçuşu için bir uyarlamadır.</code>                                                                                                                                                                                                        |
* Loss: [<code>MultipleNegativesRankingLoss</code>](https://sbert.net/docs/package_reference/sentence_transformer/losses.html#multiplenegativesrankingloss) with these parameters:
  ```json
  {
      "scale": 50,
      "similarity_fct": "cos_sim",
      "gather_across_devices": false,
      "directions": [
          "query_to_doc"
      ],
      "partition_mode": "joint",
      "hardness_mode": null,
      "hardness_strength": 0.0
  }
  ```

### Evaluation Dataset

#### json

* Dataset: json
* Size: 200 evaluation samples
* Columns: <code>anchor</code>, <code>positive</code>, and <code>negative</code>
* Approximate statistics based on the first 100 samples:
  |          | anchor                                                                            | positive                                                                            | negative                                                                           |
  |:---------|:----------------------------------------------------------------------------------|:------------------------------------------------------------------------------------|:-----------------------------------------------------------------------------------|
  | type     | string                                                                            | string                                                                              | string                                                                             |
  | modality | text                                                                              | text                                                                                | text                                                                               |
  | details  | <ul><li>min: 7 tokens</li><li>mean: 13.22 tokens</li><li>max: 23 tokens</li></ul> | <ul><li>min: 35 tokens</li><li>mean: 80.57 tokens</li><li>max: 138 tokens</li></ul> | <ul><li>min: 6 tokens</li><li>mean: 81.34 tokens</li><li>max: 126 tokens</li></ul> |
* Samples:
  | anchor                                                                                                        | positive                                                                                                                                                                                                                                                                                                                                                                                                                                                           | negative                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
  |:--------------------------------------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
  | <code>query: Minyatür inek türleri</code>                                                                     | <code>passage: Minyatür sığırlar kalça yüksekliği ile ölçülen üç kategoride sınıflandırılır. Bu üç kategori (1) orta boy minyatür, 42 ila 48 inç; (2) standart minyatür, 36 ila 42 inç; ve (3) mikro minyatür, 36 inç ve altı. Küçük cins sığırlar 500 ila 800 pound arasında değişir. Genel olarak, minyatür süt inekleri standart süt ineklerinin üçte biri ila yarısı büyüklüğündedir. 42 ila 44 inç boyunda küçük bir ailenin en ideal olduğunu buldum.</code> | <code>passage: Caribou, her iki cinsin de boynuzları olan tek geyik türüdür. Olgun boğalar muazzam ve karmaşık boynuzlar taşıyabilirken, inekler ve genç hayvanlar genellikle daha küçük ve daha basit boynuzlara sahiptir. Olgun boğalar genellikle boynuzlarını ruttan kısa bir süre sonra dökerler, oysa inekler ilkbahara kadar boynuzlarını tutabilirler.</code>                                                                                                                 |
  | <code>query: Kelimelerin bireysel konuşma seslerinden oluştuğunu fark etme yeteneğini tanımlayan terim</code> | <code>passage: Kelimelerin bireysel konuşma seslerinin birleşiminden oluştuğunu anlama bilgi ve yeteneği. Fonikler 44 İngilizce konuşma sesini sembolize etmek için kullanılan 26 harften oluşan bir bilgi gövdesi.</code>                                                                                                                                                                                                                                         | <code>passage: Eski Çince'nin kavramsal bir dil olduğunu söylediğimizde, sadece konuşulan bir dilin seslerini temsil etmediğini değil, aynı zamanda konuşulan bir dilde kullandığımız konuşma bölümlerini bile temsil etmediğini kastediyoruz. Eski Çince'nin kavramsal bir dil olduğunu söylediğimizde, sadece konuşulan bir dilin seslerini temsil etmediğini değil, aynı zamanda konuşulan bir dilde kullandığımız konuşma bölümlerini bile temsil etmediğini kastediyoruz.</code> |
  | <code>query: getcomponent fonksiyonu nedir</code>                                                             | <code>passage: GetComponent() MonoBehaviour sınıfından diğer bileşenlerdeki verilere erişmek için kullanılan bir Unity yöntemidir. Bu yöntemin nasıl çalıştığını tam olarak anlamak için kafanızı birkaç farklı kavram etrafında sarmanız gerekir.</code>                                                                                                                                                                                                          | <code>passage: Etki alanı ve aralık. Bir fonksiyonun etki alanı, fonksiyona (yani x'in alabileceği tüm değerler) koymanıza izin verilen değerler kümesidir. Fonksiyonun aralığı, fonksiyonun alabileceği tüm değerlerin kümesidir, başka bir deyişle y = f(x) olduğunda y'nin olası değerlerinin tümüdir.</code>                                                                                                                                                                      |
* Loss: [<code>MultipleNegativesRankingLoss</code>](https://sbert.net/docs/package_reference/sentence_transformer/losses.html#multiplenegativesrankingloss) with these parameters:
  ```json
  {
      "scale": 50,
      "similarity_fct": "cos_sim",
      "gather_across_devices": false,
      "directions": [
          "query_to_doc"
      ],
      "partition_mode": "joint",
      "hardness_mode": null,
      "hardness_strength": 0.0
  }
  ```

### Training Hyperparameters
#### Non-Default Hyperparameters

- `per_device_train_batch_size`: 16
- `num_train_epochs`: 1.0
- `learning_rate`: 2e-05
- `warmup_steps`: 0.1
- `batch_sampler`: no_duplicates

#### All Hyperparameters
<details><summary>Click to expand</summary>

- `per_device_train_batch_size`: 16
- `num_train_epochs`: 1.0
- `max_steps`: -1
- `learning_rate`: 2e-05
- `lr_scheduler_type`: linear
- `lr_scheduler_kwargs`: None
- `warmup_steps`: 0.1
- `optim`: adamw_torch_fused
- `optim_args`: None
- `weight_decay`: 0.0
- `adam_beta1`: 0.9
- `adam_beta2`: 0.999
- `adam_epsilon`: 1e-08
- `optim_target_modules`: None
- `gradient_accumulation_steps`: 1
- `average_tokens_across_devices`: True
- `max_grad_norm`: 1.0
- `label_smoothing_factor`: 0.0
- `bf16`: False
- `fp16`: False
- `bf16_full_eval`: False
- `fp16_full_eval`: False
- `tf32`: None
- `gradient_checkpointing`: False
- `gradient_checkpointing_kwargs`: None
- `torch_compile`: False
- `torch_compile_backend`: None
- `torch_compile_mode`: None
- `use_liger_kernel`: False
- `liger_kernel_config`: None
- `use_cache`: False
- `neftune_noise_alpha`: None
- `torch_empty_cache_steps`: None
- `auto_find_batch_size`: False
- `log_on_each_node`: True
- `logging_nan_inf_filter`: True
- `include_num_input_tokens_seen`: no
- `log_level`: passive
- `log_level_replica`: warning
- `disable_tqdm`: False
- `project`: huggingface
- `trackio_space_id`: None
- `trackio_bucket_id`: None
- `trackio_static_space_id`: None
- `per_device_eval_batch_size`: 8
- `prediction_loss_only`: True
- `eval_on_start`: False
- `eval_do_concat_batches`: True
- `eval_use_gather_object`: False
- `eval_accumulation_steps`: None
- `include_for_metrics`: []
- `batch_eval_metrics`: False
- `save_only_model`: False
- `save_on_each_node`: False
- `enable_jit_checkpoint`: False
- `push_to_hub`: False
- `hub_private_repo`: None
- `hub_model_id`: None
- `hub_strategy`: every_save
- `hub_always_push`: False
- `hub_revision`: None
- `load_best_model_at_end`: False
- `ignore_data_skip`: False
- `restore_callback_states_from_checkpoint`: False
- `full_determinism`: False
- `seed`: 42
- `data_seed`: None
- `use_cpu`: False
- `accelerator_config`: {'split_batches': False, 'dispatch_batches': None, 'even_batches': True, 'use_seedable_sampler': True, 'non_blocking': False, 'gradient_accumulation_kwargs': None}
- `parallelism_config`: None
- `dataloader_drop_last`: False
- `dataloader_num_workers`: 0
- `dataloader_pin_memory`: True
- `dataloader_persistent_workers`: False
- `dataloader_prefetch_factor`: None
- `dataloader_multiprocessing_context`: None
- `dataloader_in_order`: True
- `remove_unused_columns`: True
- `label_names`: None
- `train_sampling_strategy`: random
- `length_column_name`: length
- `ddp_find_unused_parameters`: None
- `ddp_bucket_cap_mb`: None
- `ddp_broadcast_buffers`: False
- `ddp_static_graph`: None
- `ddp_backend`: None
- `ddp_timeout`: 1800
- `fsdp`: None
- `fsdp_config`: None
- `deepspeed`: None
- `debug`: []
- `skip_memory_metrics`: True
- `do_predict`: False
- `resume_from_checkpoint`: None
- `local_rank`: -1
- `prompts`: None
- `batch_sampler`: no_duplicates
- `multi_dataset_batch_sampler`: proportional
- `router_mapping`: {}
- `learning_rate_mapping`: {}
- `warmup_ratio`: None

</details>

### Training Logs
| Epoch  | Step | Training Loss | Validation Loss |
|:------:|:----:|:-------------:|:---------------:|
| 0.7504 | 460  | 0.2173        | -               |
| 0.7667 | 470  | 0.2560        | -               |
| 0.7830 | 480  | 0.1359        | -               |
| 0.7993 | 490  | 0.1038        | -               |
| 0.8157 | 500  | 0.1592        | -               |
| 0.8320 | 510  | 0.2808        | -               |
| 0.8483 | 520  | 0.2331        | -               |
| 0.8646 | 530  | 0.1450        | -               |
| 0.8809 | 540  | 0.2115        | -               |
| 0.8972 | 550  | 0.2300        | -               |
| 0.9135 | 560  | 0.1599        | -               |
| 0.9299 | 570  | 0.2240        | -               |
| 0.9462 | 580  | 0.1429        | -               |
| 0.9625 | 590  | 0.2330        | -               |
| 0.9788 | 600  | 0.2691        | -               |
| 0.9951 | 610  | 0.2034        | -               |
| 1.0    | 613  | -             | 0.2266          |


### Training Time
- **Training**: 10.2 minutes
- **Evaluation**: 8.6 seconds
- **Total**: 10.4 minutes

### Framework Versions
- Python: 3.13.18
- Sentence Transformers: 6.2.0
- Transformers: 5.22.1
- PyTorch: 2.15.0+cu132
- Accelerate: 1.15.0
- Datasets: 5.1.0
- Tokenizers: 0.23.3

## Additional Resources

- [Training and Finetuning Embedding Models with Sentence Transformers](https://huggingface.co/blog/train-sentence-transformers): the end-to-end guide for training or finetuning Sentence Transformer models.
- [Introduction to Matryoshka Embedding Models](https://huggingface.co/blog/matryoshka): variable-size embeddings that can be truncated with minimal quality loss.
- [Binary and Scalar Embedding Quantization for Significantly Faster & Cheaper Retrieval](https://huggingface.co/blog/embedding-quantization): post-training compression of embedding vectors.
- [Multimodal Embedding & Reranker Models with Sentence Transformers](https://huggingface.co/blog/multimodal-sentence-transformers): use text, image, audio, and video models through the same API.
- [Training and Finetuning Multimodal Embedding & Reranker Models with Sentence Transformers](https://huggingface.co/blog/train-multimodal-sentence-transformers): train multimodal embedding models, with a Visual Document Retrieval walkthrough.

## Citation

### BibTeX

#### Sentence Transformers
```bibtex
@inproceedings{reimers-2019-sentence-bert,
    title = "Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks",
    author = "Reimers, Nils and Gurevych, Iryna",
    booktitle = "Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing",
    month = "11",
    year = "2019",
    publisher = "Association for Computational Linguistics",
    url = "https://arxiv.org/abs/1908.10084",
}
```

#### MultipleNegativesRankingLoss
```bibtex
@misc{oord2019representationlearningcontrastivepredictive,
      title={Representation Learning with Contrastive Predictive Coding},
      author={Aaron van den Oord and Yazhe Li and Oriol Vinyals},
      year={2019},
      eprint={1807.03748},
      archivePrefix={arXiv},
      primaryClass={cs.LG},
      url={https://arxiv.org/abs/1807.03748},
}
```

<!--
## Glossary

*Clearly define terms in order to be accessible across audiences.*
-->

<!--
## Model Card Authors

*Lists the people who create the model card, providing recognition and accountability for the detailed work that goes into its construction.*
-->

<!--
## Model Card Contact

*Provides a way for people who have updates to the Model Card, suggestions, or questions, to contact the Model Card authors.*
-->