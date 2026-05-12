import requests
import streamlit as st
import time
import pandas as pd

API_KEY = st.secrets["FINNHUB_API_KEY"]


# -----------------------------
# GET CURRENT STOCK DATA
# -----------------------------
def get_stock_data(symbol):

    try:
        quote_url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={API_KEY}"
        profile_url = f"https://finnhub.io/api/v1/stock/profile2?symbol={symbol}&token={API_KEY}"

        quote = requests.get(quote_url).json()
        profile = requests.get(profile_url).json()

        print("QUOTE RESPONSE:", quote)
        print("PROFILE RESPONSE:", profile)

        stock_info = {
            "currentPrice": quote.get("c"),
            "high": quote.get("h"),
            "low": quote.get("l"),
            "open": quote.get("o"),
            "previousClose": quote.get("pc"),
            "marketCap": profile.get("marketCapitalization"),
            "name": profile.get("name", symbol)
        }

        return stock_info, None

    except Exception as e:
        print("Stock data error:", e)
        return None, None


def get_historical_data(symbol):

    try:
        # last 6 months (better than 30 days for charts)
        to_time = int(time.time())
        from_time = to_time - (60 * 60 * 24 * 180)

        url = "https://finnhub.io/api/v1/stock/candle"

        params = {
            "symbol": symbol,
            "resolution": "D",
            "from": from_time,
            "to": to_time,
            "token": API_KEY
        }

        response = requests.get(url, params=params, timeout=10).json()

        # ---------------- DEBUG (optional) ----------------
        print("HIST RESPONSE:", response)

        # Finnhub success check
        if response.get("s") != "ok":
            return pd.DataFrame()

        # ---------------- CREATE DATAFRAME ----------------
        df = pd.DataFrame({
            "Open": response.get("o", []),
            "High": response.get("h", []),
            "Low": response.get("l", []),
            "Close": response.get("c", []),
            "Volume": response.get("v", [])
        })

        # safety check
        if df.empty:
            return pd.DataFrame()

        return df

    except Exception as e:
        print("Historical data error:", e)
        return pd.DataFrame()
