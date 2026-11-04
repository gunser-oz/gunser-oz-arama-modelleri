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
from pathlib import Path

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
        r = servis.files().list(
            q=f"'{klasor_id}' in parents and trashed = false",
            fields="nextPageToken, files(id, name, mimeType)", pageSize=200, pageToken=sayfa,
        ).execute()
        for d in r.get("files", []):
            tur = d["mimeType"]
            if tur == "application/vnd.google-apps.folder":
                indir(servis, d["id"], hedef / d["name"])
                continue
            if tur in DISA_AKTAR:
                mime, ek = DISA_AKTAR[tur]
                istek = servis.files().export_media(fileId=d["id"], mimeType=mime)
                ad = d["name"] + ek
            elif tur in INDIRILEN:
                istek = servis.files().get_media(fileId=d["id"])
                ad = d["name"]
            else:
                print(f"Atlandı ({tur}): {d['name']}", file=sys.stderr)
                continue
            tampon = io.BytesIO()
            yukleyici = MediaIoBaseDownload(tampon, istek)
            bitti = False
            while not bitti:
                _, bitti = yukleyici.next_chunk()
            (hedef / ad).write_bytes(tampon.getvalue())
            print(f"İndi: {hedef / ad}", file=sys.stderr)
        sayfa = r.get("nextPageToken")
        if not sayfa:
            break


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--klasor-id", required=True)
    p.add_argument("--hedef", default="belgelerim")
    p.add_argument("--kimlik", default="credentials.json")
    p.add_argument("--token", default="token.json")
    a = p.parse_args()
    from googleapiclient.discovery import build
    servis = build("drive", "v3", credentials=yetki(a.kimlik, a.token))
    indir(servis, a.klasor_id, Path(a.hedef))


if __name__ == "__main__":
    main()
