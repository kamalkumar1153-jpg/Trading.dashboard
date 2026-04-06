import yfinance as yf
import pandas_ta as ta
import requests
import pandas as pd

# आपका Firebase URL (अंत में .json होना अनिवार्य है)
FIREBASE_URL = "https://ai-pro-terminal-default-rtdb.firebaseio.com/market_data.json"

def update_market():
    # Nifty और Sensex का लाइव डेटा टिकर
    symbols = {"nifty": "^NSEI", "sensex": "^BSESN"}
    data_to_upload = {}

    print("🔄 Fetching Live Market Data...")

    for name, ticker in symbols.items():
        try:
            # 15 मिनट के इंटरवल पर पिछले 5 दिन का डेटा (Technical Indicators के लिए)
            df = yf.download(ticker, period="5d", interval="15m", progress=False)
            
            if not df.empty:
                # लेटेस्ट क्लोजिंग प्राइस
                current_price = round(float(df['Close'].iloc[-1]), 2)
                
                # टेक्निकल इंडिकेटर्स कैलकुलेशन
                df['RSI'] = ta.rsi(df['Close'], length=14)
                df['EMA_20'] = ta.ema(df['Close'], length=20)
                
                last_rsi = round(float(df['RSI'].iloc[-1]), 2)
                last_ema = round(float(df['EMA_20'].iloc[-1]), 2)

                # कल की क्लोजिंग से तुलना करके बदलाव (%)
                hist = yf.download(ticker, period="2d", interval="1d", progress=False)
                prev_close = hist['Close'].iloc[-2]
                change = round(((current_price - prev_close) / prev_close) * 100, 2)
                
                # डेटा को पेलोड में जोड़ना (डैशबोर्ड के Variable Names के हिसाब से)
                data_to_upload[f"{name}_price"] = current_price
                data_to_upload[f"{name}_change"] = change
                
                # डैशबोर्ड को इन एक्स्ट्रा वैल्यूज़ की ज़रूरत है
                if name == "nifty":
                    data_to_upload["nifty_rsi"] = last_rsi
                    data_to_upload["nifty_ema_20"] = last_ema
                else:
                    data_to_upload["sensex_rsi"] = last_rsi
                    data_to_upload["sensex_ema_20"] = last_ema

        except Exception as e:
            print(f"⚠️ Error fetching {name}: {e}")

    # Firebase पर डेटा भेजना
    if data_to_upload:
        try:
            response = requests.put(FIREBASE_URL, json=data_to_upload, timeout=15)
            if response.status_code == 200:
                print("✅ Market Data Updated Successfully:", data_to_upload)
            else:
                print(f"❌ Firebase Error: {response.status_code}")
        except Exception as e:
            print(f"❌ Connection Error: {e}")

if __name__ == "__main__":
    update_market()



