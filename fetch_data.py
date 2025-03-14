import yfinance as yf
import pandas as pd
from typing import Optional
from config import TICKER, LOOKBACK_DAYS, INTERVAL

def fetch_stock_data(
    ticker: str = TICKER,
    period: str = f"{LOOKBACK_DAYS}d",
    interval: str = INTERVAL
) -> Optional[pd.DataFrame]:
    """
    Fetch stock data from Yahoo Finance.
    
    Args:
        ticker (str): Stock ticker symbol
        period (str): Time period to fetch
        interval (str): Data interval
        
    Returns:
        Optional[pd.DataFrame]: DataFrame with stock data or None if error
    """
    try:
        print(f"Fetching stock data for {ticker}...")
        df = yf.download(ticker, period=period, interval=interval, progress=False)
        
        if df.empty:
            print(f"Warning: No data found for {ticker}")
            return None
            
        # Ensure all required columns exist
        required_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
        if not all(col in df.columns for col in required_columns):
            raise ValueError("Missing required columns in data")
            
        print(f"Successfully fetched {len(df)} rows of data")
        return df

    except Exception as e:
        print(f"Error fetching stock data: {str(e)}")
        return None
