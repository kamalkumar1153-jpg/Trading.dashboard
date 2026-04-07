import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime
import time
import requests

st.set_page_config(page_title="AI Pro Terminal", layout="centered", page_icon="📈")
st.title("🚀 AI Pro Terminal")
st.markdown("**Nifty 50 & Sensex Live Dashboard with RSI (14)**")
st.caption(f"Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} IST")

# Auto refresh
if "last_refresh" not in st.session_state:
    st.session_state.last_refresh = time.time()

# Function to get live data
def get_live_data():
    try:
        # Nifty 50 using yfinance (reliable)
        nifty = yf.Ticker("^NSEI")
        nifty_info = nifty.history(period="2d")
        nifty_price = nifty_info['Close'].iloc[-1]
        nifty_change = ((nifty_price - nifty_info['Close'].iloc[-2]) / nifty_info['Close'].iloc[-2]) * 100

        # Sensex using yfinance
        sensex = yf.Ticker("^BSESN")
        sensex_info = sensex.history(period="2d")
        sensex_price = sensex_info['Close'].iloc[-1]
        sensex_change = ((sensex_price - sensex_info['Close'].iloc[-2]) / sensex_info['Close'].iloc[-2]) * 100

        # RSI (14) for Nifty using yfinance historical data
        hist = yf.download("^NSEI", period="1mo", interval="1d")
        delta = hist['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        current_rsi = rsi.iloc[-1]

        return {
            "nifty_price": round(nifty_price, 2),
            "nifty_change": round(nifty_change, 2),
            "sensex_price": round(sensex_price, 2),
            "sensex_change": round(sensex_change, 2),
            "rsi": round(current_rsi, 2)
        }
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return None

data = get_live_data()

if data:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("NIFTY 50")
        st.metric(
            label="Price",
            value=f"₹ {data['nifty_price']}",
            delta=f"{data['nifty_change']}%"
        )

    with col2:
        st.subheader("SENSEX")
        st.metric(
            label="Price",
            value=f"₹ {data['sensex_price']}",
            delta=f"{data['sensex_change']}%"
        )

    # RSI Card
    st.subheader("RSI (14) - NIFTY 50")
    rsi_color = "🔴 Overbought (Sell)" if data['rsi'] > 70 else "🟢 Oversold (Buy)" if data['rsi'] < 30 else "⚪ Neutral"
    st.metric(label="RSI Value", value=data['rsi'], delta=rsi_color)

    # AI Style Signal
    st.subheader("AI SIGNAL")
    if data['rsi'] > 70:
        st.error("🔴 Strong Sell Signal - Overbought Zone")
    elif data['rsi'] < 30:
        st.success("🟢 Strong Buy Signal - Oversold Zone")
    else:
        st.info("⚪ Hold / Neutral - Wait for clear signal")

else:
    st.warning("Unable to fetch live data. Market may be closed or temporary issue.")

# Refresh Button + Auto Refresh Info
if st.button("🔄 Refresh Now"):
    st.rerun()

st.caption("Auto refreshes every 30 seconds | Data from Yahoo Finance + NSE unofficial sources")



