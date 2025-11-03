from flask import Flask, request, jsonify
import os
import requests

# === KONFIGURACJA ===
BOT_TOKEN = "8428959424:AAHtN6ulpgFbI-4nxuU1f5oz67hNVkdkxn8"
CHAT_ID = "7324665959"
WEBHOOK_SECRET = "GOLD2025"

app = Flask(__name__)

# === GŁÓWNY ROUTE (testowy) ===
@app.route('/', methods=['GET'])
def home():
    return "✅ XAUUSD Signal Bot działa 24/7", 200


# === WEBHOOK ODBIERAJĄCY ALERTY Z TRADINGVIEW ===
@app.route('/tv', methods=['POST'])
def tradingview_webhook():
    try:
        data = request.get_json(force=True)
        print("📩 Odebrano dane:", data)

        # 🔒 Weryfikacja sekretu
        if data.get("secret") != WEBHOOK_SECRET:
            return jsonify({"error": "Błędny sekret"}), 403

        # Pobieramy dane z JSON
        symbol = data.get("symbol", "N/A")
        side = data.get("side", "N/A")
        price = data.get("price", "N/A")
        tp1 = data.get("tp1", "N/A")
        tp2 = data.get("tp2", "N/A")
        sl = data.get("sl", "N/A")
        rsi = data.get("rsi", "N/A")
        adx = data.get("adx", "N/A")

        # Tworzymy wiadomość do Telegrama
        message = f"""
📊 *{symbol}* – *{side}*
💰 Cena: `{price}`
🎯 TP1: `{tp1}`
🎯 TP2: `{tp2}`
🛑 SL: `{sl}`
📈 RSI: `{rsi}`
📊 ADX: `{adx}`
🕒 Wysłano automatycznie z TradingView
"""
        # Wysyłamy do Telegrama
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
        requests.post(url, json=payload)

        return jsonify({"status": "ok"}), 200

    except Exception as e:
        print("❌ Błąd:", e)
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
