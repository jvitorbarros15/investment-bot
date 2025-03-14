from fetch_data import fetch_stock_data
from indicators import calculate_moving_averages
from strategy import trading_signal

def backtest():
    df = fetch_stock_data()
    df = calculate_moving_averages(df)

    balance = 10000  # Starting money
    position = 0

    for i in range(50, len(df)):
        price = df["Close"].iloc[i]
        sma_10 = df["SMA_10"].iloc[i]
        sma_50 = df["SMA_50"].iloc[i]
        decision = trading_signal(price, sma_10, sma_50, sentiment=0)

        if decision == "BUY" and balance > price:
            position = balance // price
            balance -= position * price
        elif decision == "SELL" and position > 0:
            balance += position * price
            position = 0

    print(f"Final balance: {balance:.2f}")

if __name__ == "__main__":
    backtest()
