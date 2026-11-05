"""
Google Drive'daki bir klasörü yerel diske indirir; sonra indeksle.py ile indekslenir.

Hazırlık (bir kez):
  1. https://console.cloud.google.com → proje aç → "Google Drive API" etkinleştir
  2. Credentials → OAuth client ID → Desktop app → JSON indir → credentials.json olarak kaydet
  3. pip install google-api-python-client google-auth-oauthlib

Kullanım:
  python deneme/drive_indir.py --klasor-id 1AbC... --hedef belgelerim
  (Klasör kimliği, Drive'da klasörü açınca adres çubuğundaki son parçadır.)

Google Dokümanlar düz metin, Google E-Tablolar CSV olarak dışa aktarılır;
PDF, DOCX, TXT dosyaları olduğu gibi iner.
"""
import argparse
import io
import sys
import time
from pathlib import Path

BEKLE = 0.5  # dosyalar arası bekleme (saniye); Google kotasını zorlamamak için


def sabirli(cagri, aciklama=""):
    """Google 403/429 (kota) veya 5xx dönerse artan sürelerle yeniden dener."""
    from googleapiclient.errors import HttpError
    for deneme in range(8):
        try:
            return cagri()
        except HttpError as e:
            if e.resp.status in (403, 429, 500, 502, 503) and deneme < 7:
                sure = min(60, 2 ** deneme)
                print(f"Kota/sunucu uyarısı ({e.resp.status}) {aciklama}; {sure} sn bekleniyor", file=sys.stderr)
                time.sleep(sure)
            else:
                raise

KAPSAM = ["https://www.googleapis.com/auth/drive.readonly"]
DISA_AKTAR = {
    "application/vnd.google-apps.document": ("text/plain", ".txt"),
    "application/vnd.google-apps.spreadsheet": ("text/csv", ".csv"),
    "application/vnd.google-apps.presentation": ("text/plain", ".txt"),
}
INDIRILEN = {"application/pdf", "text/plain", "text/markdown", "text/html",
             "application/vnd.openxmlformats-officedocument.wordprocessingml.document"}


def yetki(kimlik: str, token: str):
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    kim = Credentials.from_authorized_user_file(token, KAPSAM) if Path(token).exists() else None
    if not kim or not kim.valid:
        if kim and kim.expired and kim.refresh_token:
            kim.refresh(Request())
        else:
            kim = InstalledAppFlow.from_client_secrets_file(kimlik, KAPSAM).run_local_server(port=0)
        Path(token).write_text(kim.to_json())
    return kim


def indir(servis, klasor_id: str, hedef: Path):
    from googleapiclient.http import MediaIoBaseDownload
    hedef.mkdir(parents=True, exist_ok=True)
    sayfa = None
    while True:
        r = sabirli(lambda: servis.files().list(
            q=f"'{klasor_id}' in parents and trashed = false",
            fields="nextPageToken, files(id, name, mimeType)", pageSize=200, pageToken=sayfa,
        ).execute(), "listeleme")
        for d in r.get("files", []):
            tur = d["mimeType"]
            if tur == "application/vnd.google-apps.folder":
                indir(servis, d["id"], hedef / d["name"])
                continue
            if tur in DISA_AKTAR:
                mime, ek = DISA_AKTAR[tur]
                ad = d["name"].replace("/", "-") + ek
                yap = lambda: servis.files().export_media(fileId=d["id"], mimeType=mime)
            elif tur in INDIRILEN:
                ad = d["name"].replace("/", "-")
                yap = lambda: servis.files().get_media(fileId=d["id"])
            else:
                print(f"Atlandı ({tur}): {d['name']}", file=sys.stderr)
                continue
            if (hedef / ad).exists():
                continue  # daha önce inmiş, atla (kaldığı yerden devam)

            def indir_bir():
                tampon = io.BytesIO()
                yukleyici = MediaIoBaseDownload(tampon, yap())
                bitti = False
                while not bitti:
                    _, bitti = yukleyici.next_chunk()
                return tampon.getvalue()
            (hedef / ad).write_bytes(sabirli(indir_bir, ad))
            print(f"İndi: {hedef / ad}", file=sys.stderr)
            time.sleep(BEKLE)
        sayfa = r.get("nextPageToken")
        if not sayfa:
            break


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--klasor-id", required=True)
    p.add_argument("--hedef", default="belgelerim")
    p.add_argument("--kimlik", default="credentials.json")
    p.add_argument("--token", default="token.json")
    p.add_argument("--servis-hesabi", default=None, help="Servis hesabı JSON anahtarı (etkileşimsiz)")
    p.add_argument("--bekle", type=float, default=0.5, help="Dosyalar arası bekleme, saniye (kota koruması)")
    a = p.parse_args()
    global BEKLE
    BEKLE = a.bekle
    from googleapiclient.discovery import build
    if a.servis_hesabi:
        from google.oauth2 import service_account
        kim = service_account.Credentials.from_service_account_file(a.servis_hesabi, scopes=KAPSAM)
    else:
        kim = yetki(a.kimlik, a.token)
    servis = build("drive", "v3", credentials=kim)
    indir(servis, a.klasor_id, Path(a.hedef))


if __name__ == "__main__":
    main()
