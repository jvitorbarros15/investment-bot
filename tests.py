import unittest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from model import prepare_data, create_lstm_model
from strategy import trading_signal
from sentiment import get_news_sentiment
from indicators import calculate_moving_averages
from broker import place_trade
from fetch_data import fetch_stock_data

class TestTradingBot(unittest.TestCase):
    def setUp(self):
        # Create sample data for testing
        dates = pd.date_range(start='2024-01-01', periods=100, freq='15T')
        self.sample_data = pd.DataFrame({
            'Open': np.random.uniform(10, 20, 100),
            'High': np.random.uniform(10, 20, 100),
            'Low': np.random.uniform(10, 20, 100),
            'Close': np.random.uniform(10, 20, 100),
            'Volume': np.random.uniform(1000, 5000, 100)
        }, index=dates)

    def test_fetch_data(self):
        """Test data fetching functionality"""
        df = fetch_stock_data(period="5d")
        self.assertIsNotNone(df)
        self.assertFalse(df.empty)
        required_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
        for col in required_columns:
            self.assertIn(col, df.columns)

    def test_indicators(self):
        """Test technical indicators calculation"""
        df = calculate_moving_averages(self.sample_data)
        self.assertIn('SMA_10', df.columns)
        self.assertIn('SMA_50', df.columns)
        # Check if SMAs are calculated correctly
        self.assertEqual(
            df['SMA_10'].iloc[-1],
            df['Close'].iloc[-10:].mean()
        )

    def test_trading_signals(self):
        """Test trading signal generation"""
        # Test BUY signal
        signal = trading_signal(price=15.0, sma_10=14.0, sma_50=13.0, sentiment=0.5)
        self.assertEqual(signal, "BUY")

        # Test SELL signal
        signal = trading_signal(price=13.0, sma_10=14.0, sma_50=15.0, sentiment=-0.5)
        self.assertEqual(signal, "SELL")

        # Test HOLD signal
        signal = trading_signal(price=14.0, sma_10=14.0, sma_50=14.0, sentiment=0)
        self.assertEqual(signal, "HOLD")

    def test_sentiment_analysis(self):
        """Test sentiment analysis"""
        sentiment = get_news_sentiment()
        self.assertIsInstance(sentiment, float)
        self.assertTrue(-1 <= sentiment <= 1)

    def test_broker(self):
        """Test broker functionality"""
        result = place_trade("BUY", quantity=10)
        self.assertTrue(result)
        result = place_trade("SELL", quantity=10)
        self.assertTrue(result)

    def test_model(self):
        """Test LSTM model creation and data preparation"""
        # Test data preparation
        X, y = prepare_data(self.sample_data)
        self.assertEqual(X.shape[2], 1)  # Check if data is properly shaped for LSTM
        self.assertEqual(len(X), len(y))  # Check if X and y have matching lengths

        # Test model creation
        model = create_lstm_model()
        self.assertEqual(model.layers[0].input_shape, (None, 50, 1))

def run_integration_test():
    """Run a full integration test"""
    try:
        # 1. Fetch Data
        df = fetch_stock_data(period="5d")
        print("1. Data fetching: Success")

        # 2. Calculate Indicators
        df = calculate_moving_averages(df)
        print("2. Indicator calculation: Success")

        # 3. Get Sentiment
        sentiment = get_news_sentiment()
        print(f"3. Sentiment analysis: Success (score: {sentiment:.2f})")

        # 4. Generate Signal
        signal = trading_signal(
            df['Close'].iloc[-1],
            df['SMA_10'].iloc[-1],
            df['SMA_50'].iloc[-1],
            sentiment
        )
        print(f"4. Signal generation: Success (signal: {signal})")

        # 5. Place Test Trade
        if place_trade(signal, quantity=1):
            print("5. Trade placement: Success")

        print("\nAll integration tests passed successfully!")
        return True

    except Exception as e:
        print(f"Integration test failed: {str(e)}")
        return False

if __name__ == '__main__':
    print("Running unit tests...")
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
    
    print("\nRunning integration test...")
    run_integration_test()
