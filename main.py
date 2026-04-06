import yfinance as yf
import pandas_ta as ta
import requests
import pandas as pd
import json

# --- कॉन्फ़िगरेशन ---
# सुनिश्चित करें कि URL के अंत में .json है
FIREBASE_URL = "https://ai-pro-terminal-default-rtdb.firebaseio.com/market_data.json"

def get_market_data():
    # टिकर सिंबल्स: निफ्टी (^NSEI) और सेंसेक्स (^BSESN)
    symbols = {
        "nifty": "^NSEI",
        "sensex": "^BSESN"
    }
    
    final_payload = {}

    print("🔍 Fetching market data...")

    for name, ticker in symbols.items():
        try:
            # पिछले 5 दिन का 15 मिनट वाला डेटा (इंडिकेटर्स के लिए ज़रूरी)
            df = yf.download(ticker, period="5d", interval="15m", progress=False)
            
            if df.empty:
                print(f"⚠️ {name} का डेटा नहीं मिला।")
                continue

            # 1. लाइव प्राइस (Latest Close)
            current_price = round(float(df['Close'].iloc[-1]), 2)

            # 2. RSI (14) कैलकुलेशन
            df['RSI'] = ta.rsi(df['Close'], length=14)
            current_rsi = round(float(df['RSI'].iloc[-1]), 2)

            # 3. EMA (20) कैलकुलेशन
            df['EMA_20'] = ta.ema(df['Close'], length=20)
            current_ema = round(float(df['EMA_20'].iloc[-1]), 2)

            # 4. प्रतिशत बदलाव (पिछले दिन की क्लोजिंग से)
            hist = yf.download(ticker, period="2d", interval="1d", progress=False)
            if len(hist) >= 2:
                prev_close = hist['Close'].iloc[-2]
                change_pct = round(((current_price - prev_close) / prev_close) * 100, 2)
            else:
                change_pct = 0.0

            # पेलोड तैयार करना (आपके HTML के JavaScript वेरिएबल नाम के अनुसार)
            final_payload[f"{name}_price"] = current_price
            final_payload[f"{name}_change"] = change_pct
            
            # डैशबोर्ड के लिए RSI और EMA (निफ्टी को प्राथमिकता)
            if name == "nifty":
                final_payload["rsi_val"] = current_rsi
                final_payload["ema_20"] = current_ema
                # अलग से नाम भी रख रहे हैं ताकि कोई कंफ्यूजन न हो
                final_payload["nifty_rsi"] = current_rsi
                final_payload["nifty_ema_20"] = current_ema
            else:
                final_payload["sensex_rsi"] = current_rsi
                final_payload["sensex_ema_20"] = current_ema

        except Exception as e:
            print(f"❌ Error fetching {name}: {e}")

    # --- Firebase में डेटा भेजना ---
    if final_payload:
        try:
            print("📤 Updating Firebase...")
            response = requests.put(FIREBASE_URL, json=final_payload, timeout=15)
            if response.status_code == 200:
                print("✅ Success! Dashboard Updated.")
                print(json.dumps(final_payload, indent=2))
            else:
                print(f"❌ Firebase Error: {response.status_code}")
        except Exception as e:
            print(f"❌ Connection Error: {e}")

if __name__ == "__main__":
    # मार्केट खुला है या नहीं, यह चेक किए बिना डेटा भेजेगा (टेस्टिंग के लिए)
    get_market_data()




