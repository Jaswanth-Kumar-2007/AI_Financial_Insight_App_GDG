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


# -----------------------------
# GET HISTORICAL DATA (FOR CHARTS)
# -----------------------------
def get_historical_data(symbol):

    try:
        to_time = int(time.time())
        from_time = to_time - (60 * 60 * 24 * 30)  # last 30 days

        url = f"https://finnhub.io/api/v1/stock/candle?symbol={symbol}&resolution=D&from={from_time}&to={to_time}&token={API_KEY}"

        data = requests.get(url).json()

        if data.get("s") != "ok":
            return None

        df = pd.DataFrame({
            "Open": data["o"],
            "High": data["h"],
            "Low": data["l"],
            "Close": data["c"],
            "Volume": data["v"]
        })

        return df

    except Exception as e:
        print("Historical data error:", e)
        return None