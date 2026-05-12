from google import genai
import streamlit as st

client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

def generate_ai_analysis(symbol, rsi, macd, sentiment):

    prompt = f"""
    You are an AI Financial Market Assistant.

    Analyze the stock using:
    - technical indicators
    - news sentiment
    - recent market behavior

    Stock Symbol:
    {symbol}

    Technical Indicators:
    RSI: {rsi}
    MACD: {macd}

    News Sentiment:
    Positive: {sentiment['positive']}%
    Negative: {sentiment['negative']}%
    Neutral: {sentiment['neutral']}%

    Give a professional but beginner-friendly analysis.

    IMPORTANT RULES:
    - Use simple understandable English.
    - Explain financial terms briefly.
    - Do NOT claim guaranteed prediction accuracy.
    - Mention both positive and negative factors.
    - Explain whether market trend currently looks:
        - Uptrend
        - Downtrend
        - Sideways
    - Instead of only saying bullish/bearish:
        explain what it means in simple words.

    Response Format:

    1. Market Summary
    2. Current Trend
    3. Risk Level
    4. Positive Signals
    5. Negative Signals
    6. Beginner Explanation
    7. Estimated Market Confidence

    Explain:
    - Bullish means price may move upward
    - Bearish means price may move downward

    Example style:
    "The stock currently shows moderate upward momentum. Positive news sentiment and stable indicators suggest buyers are active, but some volatility still exists."

    Keep response concise, professional, and easy to understand.
    """
    try:

        response = client.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=prompt
        )

        return response.text

    except Exception as e:

        return f"""
        Gemini API quota exceeded or unavailable.

        Possible reasons:
        - Free quota finished
        - Billing not enabled
        - Too many requests

        Error:
        {e}
        """

    