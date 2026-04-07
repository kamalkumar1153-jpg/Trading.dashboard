
import os
import requests
import pyrebase
import time

# GitHub Secrets se credentials uthana
config = {
    "apiKey": os.getenv('FIREBASE_API_KEY'),
    "authDomain": "market--treminal.firebaseapp.com",
    "databaseURL": "https://market--treminal-default-rtdb.firebaseio.com",
    "storageBucket": "market--treminal.appspot.com"
}

# Firebase setup
firebase = pyrebase.initialize_app(config)
db = firebase.database()

def get_market_data():
    access_token = os.getenv('UPSTOX_ACCESS_TOKEN')
    # Nifty 50 ka live price lene ke liye URL
    url = "https://api.upstox.com/v2/market-quote/quotes?instrument_key=NSE_INDEX|Nifty 50"
    headers = {'Authorization': f'Bearer {access_token}', 'Accept': 'application/json'}
    
    try:
        response = requests.get(url, headers=headers).json()
        # Price nikalna
        price = response['data']['NSE_INDEX|Nifty 50']['last_price']
        
        # Dummy RSI calculation (Aap baad mein apna logic yahan daal sakte hain)
        data_to_send = {
            "price": float(price),
            "rsi": "58.20",
            "signal": "STRONG BUY" if float(price) > 22500 else "WAIT",
            "update_time": time.strftime("%H:%M:%S")
        }
        
        # Firebase mein 'market_signal' folder ke andar data save karna
        db.child("market_signal").set(data_to_send)
        print(f"Success! Nifty Price: {price} pushed to Firebase.")
        
    except Exception as e:
        print(f"Galti hui: {e}")

if __name__ == "__main__":
    get_market_data()



