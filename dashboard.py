import yfinance as yf
import pandas as pd
import pandas_ta as ta
import json

def get_signal(df):
    rsi = df['RSI'].iloc[-1]
    ema_20 = df['EMA_20'].iloc[-1]
    price = df['Close'].iloc[-1]
    
    if rsi < 30 and price > ema_20:
        return "🔥 STRONG BUY"
    elif rsi > 70 and price < ema_20:
        return "🚨 STRONG SELL"
    elif price > ema_20:
        return "📈 BULLISH"
    else:
        return "📉 BEARISH"

def update_market():
    symbols = {
        "NIFTY 50": "^NSEI",
        "SENSEX": "^BSESN",
        "BANK NIFTY": "^NSEBANK"
    }
    results = {}
    
    for name, sym in symbols.items():
        try:
            df = yf.download(sym, period="5d", interval="15m", progress=False)
            if not df.empty:
                df['RSI'] = ta.rsi(df['Close'], length=14)
                df['EMA_20'] = ta.ema(df['Close'], length=20)
                
                price = round(df['Close'].iloc[-1], 2)
                rsi_val = round(df['RSI'].iloc[-1], 1)
                signal = get_signal(df)
                
                results[name] = {
                    "price": str(price),
                    "rsi": str(rsi_val),
                    "signal": signal
                }
        except:
            results[name] = {"price": "Data Error", "rsi": "0", "signal": "WAIT"}
            
    with open('data.json', 'w') as f:
        json.dump(results, f)

if __name__ == "__main__":
    update_market()
