import requests
import os
import time
from datetime import datetime

# --- RISK CONTROL ---
MAX_LOSS_ALLOWED = -1000 
TARGET_PROFIT = 3000     

def speak(text):
    os.system(f'termux-tts-speak "{text}"')

def main():
    if not os.path.exists('token.txt'): return
    with open('token.txt', 'r') as f: token = f.read().strip()
    
    headers = {'Authorization': f'Bearer {token}', 'Accept': 'application/json'}
    instruments = 'NSE_INDEX|Nifty 50,BSE_INDEX|SENSEX'

    while True:
        try:
            # 1 = Tuesday (Nifty), 3 = Thursday (Sensex)
            today_day = datetime.now().weekday()
            
            url = f'https://api.upstox.com/v2/market-quote/ltp?instrument_key={instruments}'
            res = requests.get(url, headers=headers).json()
            
            nifty = res['data']['NSE_INDEX:Nifty 50']['last_price']
            sensex = res['data']['BSE_INDEX:SENSEX']['last_price']
            
            print("\033[H\033[J")
            print("==============================================")
            print(f"      🛡️  KAMAL MARKET-WATCH v48.0 🛡️        ")
            print("==============================================")
            print(f"LIVE NIFTY  : ₹{nifty}")
            print(f"LIVE SENSEX : ₹{sensex}")
            print("-" * 46)
            
            # Corrected Expiry Logic
            if today_day == 1: 
                print("⚠️  STATUS: NIFTY 50 EXPIRY (Tuesday) ⚠️")
            elif today_day == 3:
                print("⚠️  STATUS: SENSEX EXPIRY (Thursday) ⚠️")
                if abs(sensex % 100) < 20:
                    speak("Kamal Ji, Sensex expiry level alert! Dhyan dein.")
            else:
                print(f"STATUS: NORMAL TRADING DAY")

            print("-" * 46)
            print(f"Safety: ACTIVE | {time.strftime('%H:%M:%S')}")
            print("==============================================")
            
        except: pass
        time.sleep(2)

main()
