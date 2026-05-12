import streamlit as st
import pandas as pd

from streamlit_autorefresh import st_autorefresh

from services.stock_service import get_stock_data
from services.news_service import get_stock_news
from services.sentiment_service import analyze_sentiment
from indicators.indicators import add_indicators

from ai.symbol_ai import get_stock_symbol
from ai.gemini_analysis import generate_ai_analysis

from charts.chart_builder import create_line_chart, create_candlestick_chart

from services.compare_service import compare_stocks
from services.export_service import convert_to_csv

from services.portfolio_service import add_stock, get_portfolio

from services.stock_service import get_stock_data

from firebase.auth_service import signup_user, login_user

from firebase.watchlist_service import add_to_watchlist, get_watchlist


# ---------------- CONFIG ----------------
st.set_page_config(page_title="AI Financial Assistant", layout="wide")
st_autorefresh(interval=60000, key="refresh")

st.sidebar.title("AI Finance Dashboard")

# ---------------- AUTH ----------------
if "user" not in st.session_state:

    st.sidebar.subheader("Login / Signup")

    auth_mode = st.sidebar.selectbox("Mode", ["Login", "Signup"])

    email = st.sidebar.text_input("Email", key="email")
    password = st.sidebar.text_input("Password", type="password", key="password")

    # ---------------- SIGNUP ----------------
    if auth_mode == "Signup":

        username_input = st.sidebar.text_input("Username", key="signup_username")

        if st.sidebar.button("Create Account"):

            user = signup_user(email, password)

            if user:
                st.session_state["user"] = user
                st.session_state["username"] = username_input   # ✅ FIXED
                st.success("Account created")
                st.rerun()
            else:
                st.error("Signup failed")

    # ---------------- LOGIN ----------------
    else:

        if st.sidebar.button("Login"):

            user = login_user(email, password)

            if user:
                st.session_state["user"] = user
                st.session_state["username"] = user["email"].split("@")[0]  # ✅ safe default
                st.success("Login successful")
                st.rerun()
            else:
                st.error("Login failed")

    st.stop()

# ---------------- LOGOUT ----------------
st.sidebar.markdown("---")

if st.sidebar.button("Logout"):
    st.session_state.clear()
    st.rerun()


# ---------------- USER INFO ----------------
user_id = st.session_state["user"]["uid"]

st.sidebar.success(f"Logged in as {st.session_state.get('username')}")

# ---------------- NAVIGATION ----------------
page = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Compare Stocks", "Portfolio", "Watchlist"]
)

# ---------------- DASHBOARD ----------------
if page == "Dashboard":

    st.title("AI Financial Insight Assistant")

    # ---------------- INPUT ----------------
    user_input = st.text_input("Enter Company or Symbol", "Apple")

    symbol = get_stock_symbol(user_input)
    st.session_state["symbol"] = symbol

    # ---------------- ANALYZE ----------------
    if st.button("Analyze Stock"):

        stock_info, hist_data = get_stock_data(symbol)

        if stock_info is None or hist_data is None or hist_data.empty:
            st.error("No stock data found (invalid or unlisted company)")
            st.stop()

        hist_data = add_indicators(hist_data)

        # store in session
        st.session_state["hist_data"] = hist_data
        st.session_state["stock_info"] = stock_info

        # ---------------- METRICS ----------------
        col1, col2, col3 = st.columns(3)

        col1.metric("Price", stock_info.get("currentPrice", "N/A"))
        col2.metric("Market Cap", stock_info.get("marketCap", "N/A"))
        col3.metric("Volume", stock_info.get("volume", "N/A"))

        # ---------------- CHARTS ----------------
        st.subheader("Price Chart")
        st.plotly_chart(create_line_chart(hist_data), use_container_width=True)

        st.subheader("Candlestick Chart")
        st.plotly_chart(create_candlestick_chart(hist_data), use_container_width=True)

        # ---------------- INDICATORS (SAFE) ----------------
        st.subheader("Technical Indicators")

        try:
            latest_rsi = hist_data["RSI"].dropna().iloc[-1]
            latest_macd = hist_data["MACD"].dropna().iloc[-1]
            latest_sma = hist_data["SMA"].dropna().iloc[-1]
            latest_ema = hist_data["EMA"].dropna().iloc[-1]

            c1, c2, c3, c4 = st.columns(4)

            c1.metric("RSI", round(latest_rsi, 2))
            c2.metric("MACD", round(latest_macd, 2))
            c3.metric("SMA", round(latest_sma, 2))
            c4.metric("EMA", round(latest_ema, 2))

        except:
            st.warning("Indicators not fully available for this stock")

        # ---------------- NEWS ----------------
        st.subheader("News")

        news = get_stock_news(symbol)

        if news:
            for article in news[:5]:
                st.write("•", article["title"])

            sentiment = analyze_sentiment(news)

            st.subheader("Sentiment")

            st.metric("Positive %", sentiment["positive"])
            st.metric("Negative %", sentiment["negative"])
            st.metric("Neutral %", sentiment["neutral"])

        else:
            sentiment = {"positive": 0, "negative": 0, "neutral": 0}
            st.info("No news available")

        # ---------------- BUY / SELL ----------------
        st.subheader("Market Suggestion")

        if 'latest_rsi' in locals():

            if latest_rsi < 30:
                st.success("🟢 BUY Signal (Oversold zone)")
            elif latest_rsi > 70:
                st.error("🔴 SELL Signal (Overbought zone)")
            else:
                st.warning("🟡 HOLD Signal (Neutral market)")

        # ---------------- AI ----------------
        st.subheader("AI Analysis")

        ai_response = generate_ai_analysis(
            symbol,
            locals().get("latest_rsi", 0),
            locals().get("latest_macd", 0),
            sentiment
        )

        st.write(ai_response)

    # ---------------- WATCHLIST (FIXED SAFE VERSION) ----------------

    if "hist_data" in st.session_state and st.session_state["hist_data"] is not None:

        st.markdown("---")

        st.subheader("Watchlist")

        symbol = st.session_state.get("symbol")

        # extra safety check
        if symbol and st.session_state.get("stock_info"):

            if st.button("⭐ Add To Watchlist"):

                stock_info = st.session_state.get("stock_info", None)

                add_to_watchlist(user_id,symbol,stock_info=stock_info)

                st.success(f"{symbol} added to watchlist")

                st.rerun()

    # ---------------- DOWNLOAD ----------------
    if st.session_state.get("hist_data") is not None:

        csv = convert_to_csv(st.session_state["hist_data"])

        st.download_button(
            "Download Data",
            csv,
            "stock_data.csv",
            "text/csv"
        )


# ---------------- WATCHLIST ----------------
elif page == "Watchlist":

    st.title("My Watchlist")

    watchlist = get_watchlist(user_id)

    if not watchlist:
        st.info("No stocks in watchlist")

    else:
        for stock in watchlist:

            symbol = stock.get("symbol", "UNKNOWN")
            price = stock.get("price", "N/A")
            market_cap = stock.get("market_cap", "N/A")

            st.write(f"""
            ### {symbol}
            💰 Price: {price}  
            🏢 Market Cap: {market_cap}
            """)


# ---------------- COMPARE ----------------
elif page == "Compare Stocks":

    st.title("Compare Stocks")

    stock1 = st.text_input("Stock 1", "AAPL")
    stock2 = st.text_input("Stock 2", "TSLA")

    if st.button("Compare"):

        data1, data2 = compare_stocks(stock1, stock2)

        st.subheader(stock1)
        st.line_chart(data1["Close"])

        st.subheader(stock2)
        st.line_chart(data2["Close"])


# ---------------- PORTFOLIO ----------------
elif page == "Portfolio":

    st.title("📊 My Portfolio")

    symbol_input = st.text_input("Stock Symbol", "AAPL")
    qty = st.number_input("Quantity", min_value=1)
    price = st.number_input("Buy Price", min_value=1.0)

    if st.button("Add Stock"):

        add_stock(
            user_id,
            symbol_input,
            qty,
            price
        )

        st.success("Stock Added")
        st.rerun()

    # ---------------- SHOW PORTFOLIO ----------------

    portfolio = get_portfolio(user_id)

    if not portfolio:
        st.info("No stocks in portfolio")

    else:

        total_investment = 0
        total_current = 0

        for stock in portfolio:

            symbol = stock["symbol"]
            qty = stock["quantity"]
            buy_price = stock["buy_price"]

            stock_info, _ = get_stock_data(symbol)

            if stock_info:

                current_price = stock_info.get("currentPrice", 0)

                investment = qty * buy_price
                current_value = qty * current_price

                profit = current_value - investment
                profit_percent = (profit / investment) * 100 if investment > 0 else 0

                total_investment += investment
                total_current += current_value

                st.write(f"""
                ### {symbol}
                - Qty: {qty}
                - Buy Price: {buy_price}
                - Current Price: {current_price}
                - Profit: {round(profit, 2)}
                - Return: {round(profit_percent, 2)}%
                """)

        # ---------------- SUMMARY ----------------

        total_profit = total_current - total_investment
        total_return = (total_profit / total_investment) * 100 if total_investment > 0 else 0

        st.subheader("📊 Portfolio Summary")

        st.metric("Investment", round(total_investment, 2))
        st.metric("Current Value", round(total_current, 2))
        st.metric("Profit/Loss", round(total_profit, 2))
        st.metric("Return %", round(total_return, 2))


# # ---------------- DEBUG ----------------
# st.write("DEBUG USER:", st.session_state.get("user"))