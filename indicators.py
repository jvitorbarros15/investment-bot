import pandas as pd
from typing import Optional

def calculate_moving_averages(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate Simple Moving Averages for the given DataFrame.
    
    Args:
        df (pd.DataFrame): DataFrame with 'Close' price column
        
    Returns:
        pd.DataFrame: DataFrame with added SMA columns
    """
    try:
        if df.empty:
            raise ValueError("Empty DataFrame provided")
        
        if "Close" not in df.columns:
            raise KeyError("DataFrame missing 'Close' column")
        
        df = df.copy()  # Create copy to avoid modifying original
        df["SMA_10"] = df["Close"].rolling(window=10, min_periods=1).mean()
        df["SMA_50"] = df["Close"].rolling(window=50, min_periods=1).mean()
        
        print("Moving Averages calculated successfully.")
        return df

    except Exception as e:
        print(f"Error calculating moving averages: {str(e)}")
        return df
