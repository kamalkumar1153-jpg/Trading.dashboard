import os
import requests
import pyrebase

config = {
    "apiKey": os.getenv('FIREBASE_API_KEY'),
    "authDomain": "market--treminal.firebaseapp.com",
    "databaseURL": "https://market--treminal-default-rtdb.firebaseio.com",
    "storageBucket": "market--treminal.appspot.com"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

def get_data():
    token = os.getenv('UPSTOX_ACCESS_TOKEN')
    # Nifty aur Sensex dono ke liye keys
    instruments = "NSE_INDEX|Nifty 50,BSE_INDEX|SENSEX"
    url = f"https://api.upstox.com/v2/market-quote/quotes?instrument_key={instruments}"
    headers = {'Authorization': f'Bearer {token}', 'Accept': 'application/json'}
    
    try:
        res = requests.get(url, headers=headers).json()
        nifty = res['data']['NSE_INDEX|Nifty 50']['last_price']
        sensex = res['data']['BSE_INDEX|SENSEX']['last_price']
        
        # Firebase mein update karna
        db.child("market_data").set({
            "nifty": nifty,
            "sensex": sensex,
            "signal": "STRONG BUY" if nifty > 22000 else "WAIT",
            "rsi": "54.20"
        })
        print("Market Data Updated!")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_data()




