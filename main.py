import yfinance as yf
import pandas_ta as ta
import requests
import json
import time

# --- कॉन्फ़िगरेशन (अपनी डिटेल्स यहाँ भरें) ---
PUSHBULLET_TOKEN = "o.uG2ufY2g2A0m2GqXcMO0LwZtRX10lZMV" # अपना टोकन यहाँ पेस्ट करें
FIREBASE_URL = "https://ai-pro-terminal-default-rtdb.firebaseio.com/market_data.json"

def send_push(title, body):
    """Pushbullet के ज़रिए मोबाइल पर नोटिफिकेशन भेजना"""
    try:
        url = "https://api.pushbullet.com/v2/pushes"
        headers = {"Access-Token": PUSHBULLET_TOKEN, "Content-Type": "application/json"}
        payload = {"type": "note", "title": title, "body": body}
        requests.post(url, headers=headers, json=payload, timeout=10)
    except Exception as e:
        print(f"Pushbullet Error: {e}")

def run_engine():
    # ट्रैक करने के लिए इंडेक्स (Nifty और Sensex)
    indices = {"NIFTY 50": "^NSEI", "SENSEX": "^BSESN"}
    market_payload = {}

    print("🔄 Fetching Live Market Data...")

    for name, ticker in indices.items():
        # 15 मिनट का डेटा (पिछले 5 दिनों का ताकि इंडिकेटर्स सही आएं)
        df = yf.download(ticker, period="5d", interval="15m", progress=False)
        
        if df.empty:
            print(f"⚠️ {name} का डेटा नहीं मिल पाया।")
            continue

        # टेक्निकल इंडिकेटर्स कैलकुलेशन
        df['RSI'] = ta.rsi(df['Close'], length=14)
        df['EMA_20'] = ta.ema(df['Close'], length=20)

        # करंट और पिछली कैंडल का डेटा (Crossover चेक करने के लिए)
        last_row = df.iloc[-1]
        prev_row = df.iloc[-2]

        price = round(float(last_row['Close']), 2)
        prev_price = round(float(prev_row['Close']), 2)
        ema = round(float(last_row['EMA_20']), 2)
        prev_ema = round(float(prev_row['EMA_20']), 2)
        rsi = round(float(last_row['RSI']), 2)

        # 🔥 SMART ALERT LOGIC (EMA + RSI)
        alert_title = ""
        alert_body = ""

        # 1. Bullish Crossover (प्राइस EMA के ऊपर गया)
        if prev_price <= prev_ema and price > ema:
            alert_title = f"🚀 BUY SIGNAL: {name}"
            alert_body = f"Price crossed ABOVE EMA 20\nPrice: {price}\nRSI: {rsi}"
            send_push(alert_title, alert_body)

        # 2. Bearish Crossover (प्राइस EMA के नीचे आया)
        elif prev_price >= prev_ema and price < ema:
            alert_title = f"🔥 SELL SIGNAL: {name}"
            alert_body = f"Price dropped BELOW EMA 20\nPrice: {price}\nRSI: {rsi}"
            send_push(alert_title, alert_body)

        # 3. RSI Extreme (ओवरसोल्ड या ओवरबॉट)
        elif rsi > 75:
            send_push(f"⚠️ {name} Overbought", f"RSI is very high: {rsi}\nPrice: {price}")
        elif rsi < 25:
            send_push(f"✅ {name} Oversold", f"RSI is very low: {rsi}\nPrice: {price}")

        # Firebase पेलोड तैयार करना
        prefix = "nifty" if "NIFTY" in name else "sensex"
        market_payload[f"{prefix}_price"] = price
        market_payload[f"{prefix}_rsi"] = rsi
        market_payload[f"{prefix}_ema_20"] = ema
        
        # प्रतिशत बदलाव कैलकुलेशन (सिर्फ डैशबोर्ड के लिए)
        day_open = df['Open'].iloc[0]
        change_pct = round(((price - day_open) / day_open) * 100, 2)
        market_payload[f"{prefix}_change"] = change_pct

    # 4. Firebase Database अपडेट करें
    try:
        if market_payload:
            requests.put(FIREBASE_URL, json=market_payload, timeout=10)
            print("✅ Firebase updated and Alerts processed!")
    except Exception as e:
        print(f"Firebase Update Error: {e}")

if __name__ == "__main__":
    run_engine()

