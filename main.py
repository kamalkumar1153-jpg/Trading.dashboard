import yfinance as yf
import pandas_ta as ta

def fetch_live_signals():
    # सेंसेक्स (^BSESN) और निफ्टी (^NSEI) का डेटा
    indices = {"SENSEX": "^BSESN", "NIFTY": "^NSEI"}
    
    for name, ticker in indices.items():
        data = yf.download(ticker, period="2d", interval="5m")
        if data.empty: continue
        
        # इंडिकेटर्स कैलकुलेशन
        data['RSI'] = ta.rsi(data['Close'], length=14)
        data['EMA_20'] = ta.ema(data['Close'], length=20)
        
        last_price = data['Close'].iloc[-1]
        last_rsi = data['RSI'].iloc[-1]
        last_ema = data['EMA_20'].iloc[-1]
        change = ((last_price - data['Close'].iloc[-2]) / data['Close'].iloc[-2]) * 100

        print(f"--- {name} Update ---")
        print(f"Price: {last_price:.2f} ({change:+.2f}%)")
        print(f"RSI: {last_rsi:.2f} | EMA 20: {last_ema:.2f}")
        
        # यहाँ आप Firebase या Telegram Bot का कोड जोड़ सकते हैं 
        # ताकि index.html में वैल्यू बदल सके।

if __name__ == "__main__":
    fetch_live_signals()

