import requests
import streamlit as st
import time
import pandas as pd
import yfinance as yf


API_KEY = st.secrets["FINNHUB_API_KEY"]


# -----------------------------
# GET HISTORICAL DATA
# -----------------------------
def get_history(symbol):

    to_time = int(time.time())
    from_time = to_time - (60 * 60 * 24 * 180)  # 6 months

    url = f"https://finnhub.io/api/v1/stock/candle?symbol={symbol}&resolution=D&from={from_time}&to={to_time}&token={API_KEY}"

    data = requests.get(url).json()

    if data.get("s") != "ok":
        return None

    df = pd.DataFrame({
        "Close": data["c"]
    })

    return df


# -----------------------------
# COMPARE STOCKS
# -----------------------------


def compare_stocks(stock1, stock2):

    try:
        data1 = yf.Ticker(stock1).history(period="6mo")
        data2 = yf.Ticker(stock2).history(period="6mo")

        if data1 is None or data1.empty:
            data1 = pd.DataFrame()

        if data2 is None or data2.empty:
            data2 = pd.DataFrame()

        return data1, data2

    except Exception as e:
        print("Compare error:", e)
        return pd.DataFrame(), pd.DataFrame()