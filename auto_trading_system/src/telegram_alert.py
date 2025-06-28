import requests
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

def send_alert(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    try:
        response = requests.post(url, data=payload)
        if response.status_code != 200:
            print(f"[❌] Telegram Error: {response.status_code} | {response.text}")
        else:
            print(f"[✅] Telegram message sent.")
    except Exception as e:
        print(f"[❌] Failed to send Telegram alert: {e}")