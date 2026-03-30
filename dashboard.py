import yfinance as yf
import pandas as pd
import pandas_ta as ta
import json
import time

def get_data():
    symbols = {'NIFTY 50': '^NSEI', 'SENSEX': '^BSESN'}
    results = {}
    
    for name, sym in symbols.items():
        data = yf.download(sym, period='1d', interval='1m', progress=False)
        if not data.empty:
            last_price = round(data['Close'].iloc[-1], 2)
            # RSI Calculation (14 period)
            rsi_data = yf.download(sym, period='5d', interval='15m', progress=False)
            rsi = round(ta.rsi(rsi_data['Close'], length=14).iloc[-1], 2)
            
            results[name] = {"price": last_price, "rsi": rsi}
            
    with open('data.json', 'w') as f:
        json.dump(results, f)
    print("Data Updated!")

if __name__ == "__main__":
    get_data()
