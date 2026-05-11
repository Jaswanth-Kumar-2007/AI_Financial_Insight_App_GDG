from ta.trend import SMAIndicator
from ta.trend import EMAIndicator
from ta.trend import MACD
from ta.momentum import RSIIndicator


def add_indicators(df):

    sma = SMAIndicator(close=df['Close'], window=14)
    ema = EMAIndicator(close=df['Close'], window=14)
    rsi = RSIIndicator(close=df['Close'], window=14)
    macd = MACD(close=df['Close'])

    df['SMA'] = sma.sma_indicator()
    df['EMA'] = ema.ema_indicator()
    df['RSI'] = rsi.rsi()
    df['MACD'] = macd.macd()

    return df