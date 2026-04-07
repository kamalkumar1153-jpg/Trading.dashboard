import os
import requests
import pyrebase
import time

# GitHub Secrets se data uthana
FIREBASE_API_KEY = os.getenv('FIREBASE_API_KEY')
UPSTOX_ACCESS_TOKEN = os.getenv('UPSTOX_ACCESS_TOKEN')

config = {
    "apiKey": FIREBASE_API_KEY,
    "authDomain": "market--treminal.firebaseapp.com",
    "databaseURL": "https://market--treminal-default-rtdb.firebaseio.com",
    "storageBucket": "market--treminal.appspot.com"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

def start_bot():
    try:
        # Nifty Price Lena
        url = "https://api.upstox.com/v2/market-quote/quotes?instrument_key=NSE_INDEX|Nifty 50"
        headers = {'Authorization': f'Bearer {UPSTOX_ACCESS_TOKEN}', 'Accept': 'application/json'}
        
        r = requests.get(url, headers=headers).json()
        price = r['data']['NSE_INDEX|Nifty 50']['last_price']
        
        # Firebase mein bhej dena
        db.child("market_signal").set({
            "price": price,
            "rsi": "62.45",
            "signal": "STRONG BUY",
            "time": time.strftime("%H:%M:%S")
        })
        print(f"Success! Price: {price}")
    except Exception as e:
        print(f"Galti Hui: {e}")

if __name__ == "__main__":
    start_bot()



