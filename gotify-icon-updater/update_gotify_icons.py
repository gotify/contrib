#!/path/to/your/python/virtual/env/.venv/bin/python
# update_gotify_icons.py
# https://gotify.net/api-docs
# https://raw.githubusercontent.com/gotify/server/v2.6.1/docs/spec.json

import os
import requests
from dotenv import load_dotenv
from pathlib import Path

# Load environment
load_dotenv("/path-to/you/.env")

GOTIFY_URL = os.getenv("GOTIFY_URL")
GOTIFY_TOKEN = os.getenv("GOTIFY_TOKEN")

if not GOTIFY_TOKEN:
    raise ValueError("❌ GOTIFY_TOKEN not found in .env")

#print("Loaded token:", os.getenv("GOTIFY_TOKEN"))

APP_ICON_ENV_MAP = {
    "Backups": "RESTIC_ICON",
    "Cron": "UBUNTU_ICON"
}

HEADERS = {
    "Authorization": f"Bearer {GOTIFY_TOKEN}",
    "accept": "application/json"
}

TMP_DIR = Path("/tmp/gotify_icons")
TMP_DIR.mkdir(exist_ok=True)


def get_apps():
    response = requests.get(f"{GOTIFY_URL}/application", headers=HEADERS)
    response.raise_for_status()
    return response.json()


def delete_app_icon(app_id):
    response = requests.delete(f"{GOTIFY_URL}/application/{app_id}/image", headers=HEADERS)
    if response.status_code == 400:
        # No custom image — not an error
        print(f"  ℹ️  No existing image to delete for app {app_id}")
    elif response.status_code != 200:
        print(f"  ⚠️  Failed to delete image for app {app_id}: {response.text}")


def upload_icon(app_id, app_name):
    env_var_name = APP_ICON_ENV_MAP.get(app_name, f"{app_name.upper()}_ICON")
    icon_url = os.getenv(env_var_name)

    if not icon_url:
        print(f"  ❌ No icon URL found in .env for {env_var_name}")
        return

    response = requests.get(icon_url, stream=True)
    if response.status_code != 200:
        print(f"  ⚠️  Failed to download image for {app_name} from {icon_url}")
        return

    tmp_path = TMP_DIR / f"{app_name.lower()}.png"
    with open(tmp_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

    with open(tmp_path, "rb") as f:
        files = {'file': (tmp_path.name, f, 'image/png')}
        upload_resp = requests.post(f"{GOTIFY_URL}/application/{app_id}/image", headers=HEADERS, files=files)

    if upload_resp.status_code != 200:
        print(f"  ⚠️  Failed to upload icon for {app_name}: {upload_resp.text}")
    else:
        print(f"  ✅ Updated icon for {app_name}")

    tmp_path.unlink(missing_ok=True)

def refresh_all_icons():
    print("🔄 Refreshing Gotify app icons...")
    apps = get_apps()
    for app in apps:
        app_id = app["id"]
        app_name = app["name"]
        print(f"👉 {app_name} (ID: {app_id})")
        delete_app_icon(app_id)
        upload_icon(app_id, app_name)

if __name__ == "__main__":
    refresh_all_icons()
