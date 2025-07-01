# telegram_utils.py

import requests
import os

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
USER_ID = os.getenv("TELEGRAM_USER_ID")

def send_telegram_message(message):
    if not BOT_TOKEN or not USER_ID:
        print("⚠️ Telegram token or user ID not set.")
        return

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": USER_ID,
        "text": message
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        print(f"📲 Telegram alert sent.")
    except Exception as e:
        print(f"❌ Failed to send Telegram message: {e}")