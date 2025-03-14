import logging
from typing import Literal, Optional
from datetime import datetime
from config import BROKER_API_KEY, BROKER_SECRET

OrderType = Literal["BUY", "SELL"]

def place_trade(order_type: OrderType, quantity: int = 1) -> bool:
    """
    Simulate placing a trade and log the action.
    
    Args:
        order_type (str): Type of order ('BUY' or 'SELL')
        quantity (int): Number of shares to trade
        
    Returns:
        bool: True if trade was logged successfully, False otherwise
    """
    try:
        if order_type not in ["BUY", "SELL"]:
            raise ValueError(f"Invalid order type: {order_type}")
        if quantity < 1:
            raise ValueError(f"Invalid quantity: {quantity}")
            
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"{timestamp} - TRADE EXECUTED: {order_type} | Quantity: {quantity}"
        
        print(log_entry)
        with open("logs/trading_log.txt", "a") as file:
            file.write(log_entry + "\n")
        return True
        
    except Exception as e:
        print(f"Error placing trade: {str(e)}")
        return False
