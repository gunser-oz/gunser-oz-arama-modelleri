"""
Bir klasördeki belgeleri (pdf, docx, txt, md, html) düz metin dosyalarına çevirir.
Büyük arşivlerde indeksleme öncesi disk ve bellek tasarrufu sağlar; indeksle.py sonra bu
txt klasörünü okur.

  python deneme/metin_cikar.py --klasor /tmp/acilan --cikti /tmp/metin --en-fazla 300000
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from indeksle import UZANTILAR, metin_cikar  # noqa: E402


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--klasor", required=True)
    p.add_argument("--cikti", required=True)
    p.add_argument("--en-fazla", type=int, default=300_000, help="Dosya başına en çok bu kadar karakter tutulur")
    a = p.parse_args()
    kok, cikti = Path(a.klasor), Path(a.cikti)
    sayac = atlanan = 0
    for f in sorted(kok.rglob("*")):
        if f.suffix.lower() not in UZANTILAR:
            continue
        hedef = cikti / f.relative_to(kok).with_suffix(f.suffix + ".txt")
        if hedef.exists():
            continue
        try:
            metin = metin_cikar(f)
        except Exception as e:
            print(f"Atlandı {f.name}: {e}", file=sys.stderr); atlanan += 1; continue
        metin = metin.strip()
        if len(metin) < 50:
            atlanan += 1; continue
        hedef.parent.mkdir(parents=True, exist_ok=True)
        hedef.write_text(metin[: a.en_fazla], encoding="utf-8")
        sayac += 1
    print(f"{sayac} dosya metne çevrildi, {atlanan} atlandı -> {cikti}", file=sys.stderr)


if __name__ == "__main__":
    main()
