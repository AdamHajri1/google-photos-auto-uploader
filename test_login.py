
from pathlib import Path
from google_auth_oauthlib.flow import InstalledAppFlow

folder = Path(__file__).resolve().parent
client_file = folder / "client_secret.json"
token_file = folder / "token.json"

scopes = [
    "https://www.googleapis.com/auth/photoslibrary.appendonly"
]

if not client_file.exists():
    print("ERROR: client_secret.json is missing from this folder.")
    input("Press Enter to close.")
    raise SystemExit(1)

flow = InstalledAppFlow.from_client_secrets_file(
    str(client_file), scopes
)

credentials = flow.run_local_server(port=0)

token_file.write_text(credentials.to_json(), encoding="utf-8")

print("Google authorization successful!")
input("Press Enter to close.")
