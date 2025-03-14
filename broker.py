import requests
from config import BROKER_API_KEY, BROKER_SECRET

# broker.py (Modify this)
def place_trade(order_type, quantity=1):
    """Simulate a trade instead of executing it for testing."""
    log_entry = f"TRADE EXECUTED: {order_type} | Quantity: {quantity}"
    print(log_entry)
    with open("logs/trading_log.txt", "a") as file:
        file.write(log_entry + "\n")
