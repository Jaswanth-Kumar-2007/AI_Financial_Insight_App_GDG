from firebase.firebase_config import db
from datetime import datetime, timezone

# -----------------------------
# ADD TO WATCHLIST (IMPROVED)
# -----------------------------
def add_to_watchlist(user_id, stock_symbol, stock_info=None):

    if not user_id or not stock_symbol:
        return

    data = {
        "symbol": stock_symbol.upper(),
        "added_at": datetime.utcnow(),
    }

    # enrich with stock data if available
    if stock_info:
        data["price"] = stock_info.get("currentPrice", "N/A") if stock_info else "N/A"
        data["market_cap"] = stock_info.get("marketCap", "N/A") if stock_info else "N/A"
        data["volume"] = stock_info.get("volume", None)

    db.collection("users") \
      .document(user_id) \
      .collection("watchlist") \
      .document(stock_symbol.upper()) \
      .set(data)


# -----------------------------
# REMOVE FROM WATCHLIST
# -----------------------------
def remove_from_watchlist(user_id, stock_symbol):

    if not user_id or not stock_symbol:
        return

    db.collection("users") \
      .document(user_id) \
      .collection("watchlist") \
      .document(stock_symbol.upper()) \
      .delete()


# -----------------------------
# GET WATCHLIST (IMPROVED)
# -----------------------------


def safe_time(value):
    if value is None:
        return datetime.min.replace(tzinfo=timezone.utc)

    # Firestore timestamp already has timezone → OK
    return value


def get_watchlist(user_id):

    docs = db.collection("users") \
             .document(user_id) \
             .collection("watchlist") \
             .stream()

    watchlist = []

    for doc in docs:
        data = doc.to_dict()

        watchlist.append({
            "symbol": data.get("symbol"),
            "price": data.get("price", "N/A"),
            "market_cap": data.get("market_cap", "N/A"),
            "volume": data.get("volume", "N/A"),
            "added_at": data.get("added_at")
        })

    watchlist.sort(
        key=lambda x: safe_time(x["added_at"]),
        reverse=True
    )

    return watchlist