import yfinance as yf


def get_stock_data(symbol):

    try:
        ticker = yf.Ticker(symbol)

        stock_info = ticker.info

        hist_data = ticker.history(period="1y")

        return stock_info, hist_data

    except:
        return None, None