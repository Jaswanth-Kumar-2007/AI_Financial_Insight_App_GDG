import requests
import os
from dotenv import load_dotenv

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")


def get_stock_news(symbol):

    url = f"https://newsapi.org/v2/everything?q={symbol}&apiKey={NEWS_API_KEY}"

    response = requests.get(url)

    data = response.json()

    return data.get("articles", [])