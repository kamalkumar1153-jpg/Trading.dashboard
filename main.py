import yfinance as yf
import pandas_ta as ta
import pandas as pd

def get_market_signal(ticker_symbol):
    # 5 मिनट के इंटरवल पर डेटा लेना (Intraday के लिए)
    df = yf.download(ticker_symbol, period="5d", interval="5m")
    
    # इंडिकेटर्स कैलकुलेट करना
    df['RSI'] = ta.rsi(df['Close'], length=14)
    df['EMA_20'] = ta.ema(df['Close'], length=20)
    
    last_row = df.iloc[-1]
    price = last_row['Close']
    rsi = last_row['RSI']
    ema = last_row['EMA_20']
    
    # सिग्नल लॉजिक
    signal = "NEUTRAL ⚪"
    if rsi > 60 and price > ema:
        signal = "STRONG BUY 🚀"
    elif rsi < 40 and price < ema:
        signal = "STRONG SELL 📉"
    elif rsi > 50:
        signal = "BULLISH BIAS 🔼"
    elif rsi < 50:
        signal = "BEARISH BIAS 🔽"
    
    return f"{ticker_symbol}: {price:.2f} | RSI: {rsi:.2f} | Signal: {signal}"

# Sensex और Nifty दोनों के लिए चेक करें
print(get_market_signal("^BSESN")) # Sensex
print(get_market_signal("^NSEI"))  # Nifty 50
