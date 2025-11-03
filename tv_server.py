import os, json
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

TELEGRAM_ENABLED = os.getenv("TELEGRAM_ENABLED", "1") in ["1", "true", "True"]
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
CHAT_ID = os.getenv("CHAT_ID", "")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "GOLD2025")

def send_telegram(text: str):
    if not TELEGRAM_ENABLED or not BOT_TOKEN or not CHAT_ID:
        print("Telegram disabled or credentials missing")
        return
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"}
    try:
        r = requests.post(url, json=payload, timeout=10)
        print("Telegram status:", r.status_code, r.text)
    except Exception as e:
        print("Telegram error:", e)

@app.route("/health", methods=["GET"])
def health():
    return "OK", 200

@app.route("/tv", methods=["POST"])
def tv():
    try:
        data = request.get_json(force=True)
    except Exception as e:
        print("❌ JSON parse error:", e)
        return jsonify({"ok": False, "error": "invalid_json"}), 400

    print("✅ Alert:", data)

    # weryfikacja sekretu
    secret = data.get("secret", "")
    if WEBHOOK_SECRET and secret != WEBHOOK_SECRET:
        print("❌ Bad secret")
        return jsonify({"ok": False, "error": "unauthorized"}), 401

    # sformatuj wiadomość
    symbol = data.get("symbol", "UNK")
    side = data.get("side", "UNK")
    price = data.get("price", "?")
    tp1 = data.get("tp1", "?")
    tp2 = data.get("tp2", "?")
    sl = data.get("sl", "?")

    msg = f"""<b>📊 XAUUSD SIGNAL</b>
<b>{side}</b> @ {price}
🎯 TP1: {tp1}
🎯 TP2: {tp2}
⛔ SL: {sl}"""

    send_telegram(msg)
    return jsonify({"ok": True}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
