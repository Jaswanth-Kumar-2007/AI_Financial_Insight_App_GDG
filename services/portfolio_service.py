from firebase.firebase_config import db


def add_stock(user_id, symbol, quantity, buy_price):

    db.collection("users") \
      .document(user_id) \
      .collection("portfolio") \
      .document(symbol) \
      .set({
          "symbol": symbol,
          "quantity": quantity,
          "buy_price": buy_price
      })


def get_portfolio(user_id):

    docs = db.collection("users") \
             .document(user_id) \
             .collection("portfolio") \
             .stream()

    portfolio = []

    for doc in docs:
        portfolio.append(doc.to_dict())

    return portfolio