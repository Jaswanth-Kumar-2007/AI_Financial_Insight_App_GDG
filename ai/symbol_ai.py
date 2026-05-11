import google.generativeai as genai
import os

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel("gemini-3.1-flash-lite")


def get_stock_symbol(user_input):

    # Fast local mappings first
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

    # Local mapping
    if text in local_symbols:

        return local_symbols[text]

    # If already looks like stock symbol
    if len(text) <= 10 and " " not in text:

        if text in ["tcs", "infy", "reliance"]:
            return text.upper() + ".NS"

        return text.upper()

    # Gemini fallback
    prompt = f"""
    Convert this company name into ONLY a Yahoo Finance stock symbol.

    Rules:
    - Return ONLY symbol
    - No explanation
    - No sentences
    - Indian stocks end with .NS
    - If invalid return INVALID

    Example:
    Apple -> AAPL
    TCS -> TCS.NS

    Input:
    {user_input}
    """

    try:

        response = model.generate_content(prompt)

        symbol = response.text.strip()

        # Remove spaces/newlines
        symbol = symbol.split()[0]

        symbol = symbol.replace("\n", "")

        symbol = symbol.upper()

        return symbol

    except Exception as e:

        print(e)

        return "INVALID"