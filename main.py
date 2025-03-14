import time
import logging
import pandas as pd
from fetch_data import fetch_stock_data
from indicators import calculate_moving_averages
from sentiment import get_news_sentiment
from strategy import trading_signal
from broker import place_trade

# Setup logging to track trades & errors
logging.basicConfig(
    filename="logs/trading_log.txt",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def run_bot():
    try:
        while True:
            print("\nFetching stock data...")
            df = fetch_stock_data()

            # Check if the DataFrame is empty
            if df is None or df.empty:
                print("Skipping this cycle due to empty stock data.")
                logging.warning("No stock data fetched. Skipping cycle.")
                time.sleep(60)
                continue  # Skip this loop iteration

            df = calculate_moving_averages(df)

            # Extract latest values from DataFrame
            latest_price = df["Close"].iloc[-1]
            sma_10 = df["SMA_10"].iloc[-1]
            sma_50 = df["SMA_50"].iloc[-1]
            sentiment_score = get_news_sentiment()

            # Convert Series to scalar values (if necessary)
            if isinstance(latest_price, pd.Series):
                latest_price = latest_price.iloc[-1].item()
            if isinstance(sma_10, pd.Series):
                sma_10 = sma_10.iloc[-1].item()
            if isinstance(sma_50, pd.Series):
                sma_50 = sma_50.iloc[-1].item()

            # Ensure sentiment is a float
            sentiment_score = float(sentiment_score)

            # Debugging print
            print(f"DEBUG: Price={latest_price}, SMA_10={sma_10}, SMA_50={sma_50}, Sentiment={sentiment_score}")

            # Determine trade action
            decision = trading_signal(latest_price, sma_10, sma_50, sentiment_score)
            print(f"Trading Signal: {decision} | Price: {latest_price:.2f}")

            # Execute trade if BUY/SELL signal is given
            if decision in ["BUY", "SELL"]:
                place_trade(decision, quantity=10)
                logging.info(f"Trade executed: {decision} at {latest_price:.2f}")

            time.sleep(60)  # Run every minute

    except KeyboardInterrupt:
        print("\nBot stopped manually. Exiting...")
        logging.info("Bot stopped manually.")

    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    run_bot()
