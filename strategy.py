import pandas as pd

def trading_signal(price: float, sma_10: float, sma_50: float, sentiment: float) -> str:
    """
    Generate trading signals based on price, moving averages and sentiment.
    
    Args:
        price (float): Current stock price
        sma_10 (float): 10-period Simple Moving Average
        sma_50 (float): 50-period Simple Moving Average
        sentiment (float): Sentiment score between -1 and 1
        
    Returns:
        str: Trading signal ('BUY', 'SELL', or 'HOLD')
    """
    try:
        # Calculate percentage differences
        price_vs_sma10 = ((price - sma_10) / sma_10) * 100
        sma10_vs_sma50 = ((sma_10 - sma_50) / sma_50) * 100
        
        # Enhanced trading conditions
        if (price_vs_sma10 < -1.0 and sma10_vs_sma50 > 0):  # Buy on dips when trend is up
            return "BUY"
        elif (price_vs_sma10 > 1.5 or  # Sell on significant price increase
              (price_vs_sma10 < -2.0 and sma10_vs_sma50 < 0)):  # Or cut losses in downtrend
            return "SELL"
        return "HOLD"
        
    except Exception as e:
        print(f"Error in trading_signal: {str(e)}")
        return "HOLD"
