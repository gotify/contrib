# gotify-icon-updater

A simple Python script to automatically update Gotify app icons from a centralized `.env` file using the Gotify API.

## Features

- Auto-update Gotify app icons from URLs defined in a `.env` file
- Supports custom mappings when app name and environment variable don't match
- Minimal setup with Python dependencies
- Centralized control over icon sources for multiple apps

---

# Quickstart

```bash
pip install requests python-dotenv

# Clone the repository
 git clone https://github.com/samcro1967/gotify-icon-updater.git
 cd gotify-icon-updater

# Copy and update your .env file (see .env.example)
cp .env.example .env

# Update gotify-icon-updater with the path to your virtual python environment
load_dotenv("/path-to/you/.env")

# Run the script
python update_gotify_icons.py
```

---

# Setup Instructions

## 1. Install Python Dependencies
```bash
pip install requests python-dotenv
```

## 2. Clone This Repository
```bash
git clone https://github.com/samcro1967/gotify-icon-updater.git
cd gotify-icon-updater
```

## 3. Update the `.env` File
Edit or create a `.env` file based on `.env.example`:

| Key | Description |
|:----|:------------|
| `GOTIFY_URL` | Your Gotify server URL (no trailing slash) |
| `GOTIFY_TOKEN` | Your **user** token for Gotify (not an app token) |
| `<APP>_ICON` | URL to the desired icon for each Gotify app |

Example `.env` snippet:
```dotenv
GOTIFY_URL=https://gotify.example.com
GOTIFY_TOKEN=your-user-token
GOTIFY_ICON=https://raw.githubusercontent.com/homarr-labs/dashboard-icons/refs/heads/main/png/gotify.png
GRAFANA_ICON=https://raw.githubusercontent.com/homarr-labs/dashboard-icons/refs/heads/main/png/grafana.png
```

## 4. (Optional) Adjust Environment Variable Loading
In `update_gotify_icons.py`, ensure the `.env` is correctly loaded:
```python
load_dotenv(".env")
```

Modify the path if your `.env` file is elsewhere.

## 5. Run the Script
```bash
python update_gotify_icons.py
```

---

Notes

Ensure your .env variables are accurate.

If an app name doesn't match an environment variable exactly, update APP_ICON_ENV_MAP inside the script.

Example mapping:

APP_ICON_ENV_MAP = {
    "Backups": "RESTIC_ICON",
    "Cron": "UBUNTU_ICON"
}

You can automate this script with a cron job for regular updates.

---
