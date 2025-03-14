def calculate_moving_averages(df):
    if df.empty or "Close" not in df.columns:
        print("WARNING: DataFrame is empty or missing 'Close' column. Skipping calculation.")
        return df  # Return unmodified DataFrame
    
    df["SMA_10"] = df["Close"].rolling(window=10).mean()
    df["SMA_50"] = df["Close"].rolling(window=50).mean()
    print("Moving Averages calculated successfully.")
    return df
