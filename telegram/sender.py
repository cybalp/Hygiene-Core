import os
import requests
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=BASE_DIR / ".env")

class TelegramSender:
    def __init__(self):
        self.token = os.getenv("TELEGRAM_TOKEN")
        self.chat_id = os.getenv("CHAT_ID")
        self.url = f"https://api.telegram.org/bot{self.token}/sendMessage"

    def send_report(self, text):
        if not self.token or not self.chat_id:
            return False
        
        payload = {
            "chat_id": self.chat_id,
            "text": text,
            "parse_mode": "Markdown"
        }
        try:
            response = requests.post(self.url, json=payload)
            return response.status_code == 200
        except Exception:
            return False
