import requests
import os
import time
from bs4 import BeautifulSoup

# === KONFIGURATION ===
URL = "https://www.stwdo.de/wohnen/aktuelle-wohnangebote"
CHECK_INTERVAL = 1800  # alle 30 Minuten (in Sekunden)
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
PREVIOUS_CONTENT_FILE = "previous_content.txt"

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": text})

def get_page_content():
    response = requests.get(URL, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")
    main_content = soup.find("div", {"class": "content"})
    return main_content.get_text(strip=True) if main_content else ""

def main():
    print("🏠 Starte Wohnungsüberwachung...")
    send_telegram_message("✅ STWDO-Bot gestartet und überwacht nun die Seite!")

    try:
        with open(PREVIOUS_CONTENT_FILE, "r", encoding="utf-8") as f:
            previous_content = f.read()
    except FileNotFoundError:
        previous_content = ""

    while True:
        try:
            current_content = get_page_content()
            if current_content != previous_content:
                send_telegram_message("🚨 Änderung erkannt auf STWDO: Neue Wohnangebote!\n" + URL)
                with open(PREVIOUS_CONTENT_FILE, "w", encoding="utf-8") as f:
                    f.write(current_content)
                previous_content = current_content
            time.sleep(CHECK_INTERVAL)
        except Exception as e:
            print("❌ Fehler:", e)
            time.sleep(60)

if __name__ == "__main__":
    main()
