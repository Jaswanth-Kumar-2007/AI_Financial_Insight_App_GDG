import requests
import streamlit as st

API_KEY = st.secrets["FINNHUB_API_KEY"]


# -----------------------------
# STOCK DATA (MAIN FUNCTION)
# -----------------------------
def get_stock_data(symbol):

    try:
        # Price data
        quote_url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={API_KEY}"
        quote = requests.get(quote_url).json()

        # Company profile
        profile_url = f"https://finnhub.io/api/v1/stock/profile2?symbol={symbol}&token={API_KEY}"
        profile = requests.get(profile_url).json()

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
        print("Error:", e)
        return None, None