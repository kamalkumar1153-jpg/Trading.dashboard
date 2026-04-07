import os
import requests
import pyrebase

# GitHub Secrets se data lena
config = {
    "apiKey": os.getenv('FIREBASE_API_KEY'),
    "authDomain": "market--treminal.firebaseapp.com",
    "databaseURL": "https://market--treminal-default-rtdb.firebaseio.com",
    "storageBucket": "market--treminal.appspot.com"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

def push_data():
    access_token = os.getenv('UPSTOX_ACCESS_TOKEN')
    url = "https://api.upstox.com/v2/market-quote/quotes?instrument_key=NSE_INDEX|Nifty 50"
    headers = {'Authorization': f'Bearer {access_token}', 'Accept': 'application/json'}
    
    try:
        response = requests.get(url, headers=headers).json()
        price = response['data']['NSE_INDEX|Nifty 50']['last_price']
        
        # Firebase mein bhejna
        db.child("market_signal").set({
            "price": price,
            "rsi": "52.30", # Aap yahan apna calculation add kar sakte hain
            "signal": "NEUTRAL / WAIT"
        })
        print(f"Data pushed successfully: {price}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    push_data()



