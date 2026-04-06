import yfinance as yf
import pandas_ta as ta
import requests

# आपका Firebase URL
FIREBASE_URL = "https://ai-pro-terminal-default-rtdb.firebaseio.com/market_data.json"

def update_market():
    # Nifty और Sensex का लाइव डेटा
    symbols = {"nifty": "^NSEI", "sensex": "^BSESN"}
    data_to_upload = {}

    for name, ticker in symbols.items():
        # 15 मिनट के इंटरवल पर डेटा
        df = yf.download(ticker, period="1d", interval="15m", progress=False)
        if not df.empty:
            current_price = round(df['Close'].iloc[-1], 2)
            # कल की क्लोजिंग से तुलना करके बदलाव (%)
            prev_close = yf.download(ticker, period="2d", interval="1d", progress=False)['Close'].iloc[-2]
            change = round(((current_price - prev_close) / prev_close) * 100, 2)
            
            data_to_upload[f"{name}_price"] = current_price
            data_to_upload[f"{name}_change"] = change

    # Firebase पर डेटा भेजना
    requests.put(FIREBASE_URL, json=data_to_upload)
    print("Market Data Updated:", data_to_upload)

if __name__ == "__main__":
    update_market()



