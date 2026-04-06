import os
import requests
import pandas as pd
import pyrebase
import time

# --- 1. GitHub Secrets se Data Lena ---
FIREBASE_API_KEY = os.getenv('FIREBASE_API_KEY')
UPSTOX_ACCESS_TOKEN = os.getenv('UPSTOX_ACCESS_TOKEN')

# --- 2. Firebase Setup ---
config = {
    "apiKey": FIREBASE_API_KEY,
    "authDomain": "market--treminal.firebaseapp.com",
    "databaseURL": "https://market--treminal-default-rtdb.firebaseio.com",
    "storageBucket": "market--treminal.appspot.com"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

# --- 3. Market Logic ---
def update_signal():
    # Nifty 50 ka instrument key
    inst_key = "NSE_INDEX|Nifty 50"
    url = f'https://api.upstox.com/v2/market-quote/quotes?instrument_key={inst_key}'
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {UPSTOX_ACCESS_TOKEN}'
    }

    try:
        response = requests.get(url, headers=headers)
        res_data = response.json()
        
        # Live Price nikalna
        ltp = res_data['data'][inst_key]['last_price']
        
        # RSI Simulation (Yahan aap apna logic dal sakte hain)
        # Maan lijiye abhi RSI 65 hai
        rsi_val = 65.0 
        
        signal = "WAIT"
        if rsi_val > 60:
            signal = "UP"
        elif rsi_val < 40:
            signal = "DOWN"

        # Firebase Update
        db.child("market_signal").set({
            "signal": signal,
            "rsi": rsi_val,
            "price": ltp,
            "confidence": "85%",
            "timestamp": time.time()
        })
        print(f"Update Success: {signal} at {ltp}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    update_signal()





