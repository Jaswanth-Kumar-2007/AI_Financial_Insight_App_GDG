from google import genai
import os
import streamlit as st
import re

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY") or st.secrets["GEMINI_API_KEY"]
)


def get_stock_symbol(user_input):

    local_symbols = {
        "apple": "AAPL",
        "tesla": "TSLA",
        "google": "GOOGL",
        "amazon": "AMZN",
        "microsoft": "MSFT",
        "tcs": "TCS.NS",
        "infosys": "INFY.NS",
        "infy": "INFY.NS",
        "reliance": "RELIANCE.NS"
    }

    text = user_input.strip().lower()

    # ---------------------------
    # 1. Local mapping
    # ---------------------------
    if text in local_symbols:
        return local_symbols[text]

    # ---------------------------
    # 2. If already valid symbol
    # (AAPL, TSLA, INFY.NS)
    # ---------------------------
    if re.match(r"^[A-Z]{1,6}(\.NS)?$", user_input.strip().upper()):
        return user_input.strip().upper()

    # ---------------------------
    # 3. Gemini fallback
    # ---------------------------
    prompt = f"""
Convert this company name into ONLY a Yahoo Finance stock symbol.

Rules:
- Return ONLY symbol
- No explanation
- No text
- Indian stocks end with .NS
- If invalid return INVALID

Input:
{user_input}
"""

    try:
        response = client.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=prompt
        )

        symbol = response.text.strip().split()[0]
        symbol = symbol.replace("\n", "").upper()

        return symbol

    except Exception as e:
        print("Gemini error:", e)
        return "INVALID"