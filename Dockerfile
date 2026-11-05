# Hugging Face Spaces (Docker) ve benzeri bulutlar için arama sunucusu.
FROM python:3.12-slim

WORKDIR /app
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY deneme/ deneme/
COPY modeller/e5-small-mmarco-tr/ modeller/e5-small-mmarco-tr/
COPY cikti/degerlendirme.json cikti/degerlendirme.json
# Parçalı ağırlıkları birleştir, parçaları sil
RUN sh modeller/e5-small-mmarco-tr/birlestir.sh && rm modeller/e5-small-mmarco-tr/model.safetensors.part_*

# Temel model Hugging Face Hub'dan iner (depodaki LFS kopyasıyla aynı)
ENV ARAMA_MODEL=intfloat/multilingual-e5-small \
    ARAMA_KARSILASTIR=modeller/e5-small-mmarco-tr \
    ARAMA_INDEKS=deneme/indeks \
    HF_HOME=/app/.cache \
    PORT=7860
RUN mkdir -p /app/.cache && chmod -R 777 /app

EXPOSE 7860
CMD ["python", "deneme/sunucu.py"]
