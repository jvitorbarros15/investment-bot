import pandas as pd

def trading_signal(price, sma_10, sma_50, sentiment):
    if isinstance(price, (pd.Series, list)) or isinstance(sma_10, (pd.Series, list)) or isinstance(sma_50, (pd.Series, list)):
        print("ERROR: trading_signal received a Series instead of a scalar value.")
        return "HOLD"

    if price > sma_10 and sma_10 > sma_50 and sentiment > 0:
        return "BUY"
    elif price < sma_10 and sma_10 < sma_50 and sentiment < 0:
        return "SELL"
    else:
        return "HOLD"
