# Hugging Face Spaces (Docker SDK) için arama sunucusu.
# Spaces konteyneri 1000 numaralı kullanıcıyla çalışır; resmi rehbere göre önce kullanıcı kurulur.
FROM python:3.12-slim

RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH
WORKDIR $HOME/app

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu
COPY --chown=user requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=user deneme/ deneme/
COPY --chown=user modeller/e5-small-mmarco-tr/ modeller/e5-small-mmarco-tr/
COPY --chown=user cikti/degerlendirme.json cikti/degerlendirme.json
# Parçalı ağırlıkları birleştir, parçaları sil
RUN sh modeller/e5-small-mmarco-tr/birlestir.sh && rm modeller/e5-small-mmarco-tr/model.safetensors.part_*

# Temel model Hugging Face Hub'dan iner (depodaki LFS kopyasıyla aynı model)
ENV ARAMA_MODEL=intfloat/multilingual-e5-small \
    ARAMA_KARSILASTIR=modeller/e5-small-mmarco-tr \
    ARAMA_INDEKS=deneme/indeks \
    HF_HOME=/home/user/.cache \
    PORT=7860
# ARAMA_SIFRE, Space ayarlarındaki secret'tan çalışma anında gelir

EXPOSE 7860
CMD ["python", "deneme/sunucu.py"]
