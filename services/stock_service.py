import yfinance as yf
import streamlit as st

@st.cache_data(ttl=300)
def get_stock_data(symbol):

    try:
        ticker = yf.Ticker(symbol)

        stock_info = ticker.info

        hist_data = ticker.history(period="1y")

        return stock_info, hist_data

    except:
        return None, None