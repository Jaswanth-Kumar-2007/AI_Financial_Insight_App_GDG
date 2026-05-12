import requests
import streamlit as st
import pandas as pd
import yfinance as yf

API_KEY = st.secrets["FINNHUB_API_KEY"]


# -----------------------------
# CURRENT STOCK DATA (FINNHUB)
# -----------------------------
def get_stock_data(symbol):

    try:
        quote_url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={API_KEY}"
        profile_url = f"https://finnhub.io/api/v1/stock/profile2?symbol={symbol}&token={API_KEY}"

        quote = requests.get(quote_url, timeout=10).json()
        profile = requests.get(profile_url, timeout=10).json()

        # safety check
        if not quote or quote.get("c") is None:
            return None, None

        stock_info = {
            "currentPrice": quote.get("c"),
            "high": quote.get("h"),
            "low": quote.get("l"),
            "open": quote.get("o"),
            "previousClose": quote.get("pc"),
            "marketCap": profile.get("marketCapitalization"),
            "name": profile.get("name", symbol)
        }

        return stock_info, True

    except Exception as e:
        print("Stock data error:", e)
        return None, None


# -----------------------------
# HISTORICAL DATA (YFINANCE)
# -----------------------------
def get_historical_data(symbol):

    try:
        ticker = yf.Ticker(symbol)

        df = ticker.history(period="6mo")

        if df is None or df.empty:
            return pd.DataFrame()

        return df[["Open", "High", "Low", "Close", "Volume"]]

    except Exception as e:
        print("YFinance error:", e)
        return pd.DataFrame()