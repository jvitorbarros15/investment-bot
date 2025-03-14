import yfinance as yf

def fetch_stock_data(ticker="PETR4.SA", period="60d", interval="15m"):
    print(f"Fetching stock data for {ticker}...")
    df = yf.download(ticker, period=period, interval=interval)

    if df.empty:
        print("WARNING: No stock data fetched.")
        return df  # Returns empty DataFrame

    print(df.tail())  # Print the last few rows to check structure
    return df
