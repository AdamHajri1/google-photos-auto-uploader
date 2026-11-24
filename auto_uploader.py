
import os
import time
import json
import hashlib
import mimetypes
import requests

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FOLDER = os.path.join(BASE_DIR, "AutoUpload")
TOKEN_FILE = os.path.join(BASE_DIR, "token.json")
HISTORY_FILE = os.path.join(BASE_DIR, "uploaded_files.json")

SCOPES = ["https://www.googleapis.com/auth/photoslibrary.appendonly"]

os.makedirs(FOLDER, exist_ok=True)

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    return {}

def save_history(history):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)

def get_hash(path):
    sha = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            sha.update(chunk)
    return sha.hexdigest()

def wait_until_ready(path):
    previous_size = -1
    stable_checks = 0

    while stable_checks < 3:
        try:
            current_size = os.path.getsize(path)
        except OSError:
            return False

        if current_size > 0 and current_size == previous_size:
            stable_checks += 1
        else:
            stable_checks = 0

        previous_size = current_size
        time.sleep(5)

    return True

def upload_file(path, creds):
    mime_type = mimetypes.guess_type(path)[0]

    if not mime_type or not mime_type.startswith("image/"):
        print("Skipped non-image file:", os.path.basename(path))
        return False

    with open(path, "rb") as f:
        response = requests.post(
            "https://photoslibrary.googleapis.com/v1/uploads",
            headers={
                "Authorization": f"Bearer {creds.token}",
                "Content-type": "application/octet-stream",
                "X-Goog-Upload-Content-Type": mime_type,
                "X-Goog-Upload-Protocol": "raw"
            },
            data=f,
            timeout=(30, 1800)
        )

    if response.status_code != 200:
        print("Upload failed:", response.text)
        return False

    upload_token = response.text

    result = requests.post(
        "https://photoslibrary.googleapis.com/v1/mediaItems:batchCreate",
        headers={
            "Authorization": f"Bearer {creds.token}",
            "Content-type": "application/json"
        },
        json={
            "newMediaItems": [{
                "simpleMediaItem": {
                    "fileName": os.path.basename(path),
                    "uploadToken": upload_token
                }
            }]
        },
        timeout=120
    )

    if result.status_code != 200:
        print("Creation failed:", result.text)
        return False

    data = result.json()
    item = data["newMediaItemResults"][0]

    if item.get("status", {}).get("message") != "Success":
        print("Google Photos error:", item.get("status"))
        return False

    print("SUCCESS:", os.path.basename(path))
    print(item.get("mediaItem", {}).get("productUrl", ""))
    return True

def main():
    creds = Credentials.from_authorized_user_file(
        TOKEN_FILE, SCOPES
    )

    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        with open(TOKEN_FILE, "w") as f:
            f.write(creds.to_json())

    history = load_history()

    print("Automatic Google Photos uploader started!")
    print("Folder:", FOLDER)
    print("Keep this window open while uploading.")
    print("--------------------------------------")

    while True:
        for filename in os.listdir(FOLDER):
            path = os.path.join(FOLDER, filename)

            if not os.path.isfile(path):
                continue

            try:
                if not wait_until_ready(path):
                    continue

                file_hash = get_hash(path)

                if file_hash in history:
                    continue

                print("Uploading:", filename)

                if upload_file(path, creds):
                    history[file_hash] = filename
                    save_history(history)

            except Exception as e:
                print("Error:", filename, "-", e)

        time.sleep(10)

if __name__ == "__main__":
    main()
