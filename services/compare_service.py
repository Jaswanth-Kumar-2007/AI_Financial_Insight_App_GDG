import yfinance as yf


def compare_stocks(stock1, stock2):

    data1 = yf.Ticker(stock1).history(period="6mo")
    data2 = yf.Ticker(stock2).history(period="6mo")

    return data1, data2