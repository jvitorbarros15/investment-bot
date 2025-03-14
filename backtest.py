def run_backtest():
    """Run backtest with detailed performance metrics"""
    from fetch_data import fetch_stock_data
    from indicators import calculate_moving_averages
    from strategy import trading_signal
    import pandas as pd
    
    # Fetch historical data
    df = fetch_stock_data(period="60d")
    if df is None or df.empty:
        print("No data available for backtesting")
        return
        
    # Calculate indicators
    df = calculate_moving_averages(df)
    
    # Initialize tracking variables
    initial_balance = 10000
    balance = initial_balance
    position = 0
    trades = []
    entry_price = 0
    stop_loss_pct = 0.02  # 2% stop loss
    take_profit_pct = 0.03  # 3% take profit
    
    # Run backtest
    for i in range(50, len(df)):
        price = df["Close"].iloc[i].item()
        sma_10 = df["SMA_10"].iloc[i].item()
        sma_50 = df["SMA_50"].iloc[i].item()
        
        # Check stop loss and take profit if we have a position
        if position > 0:
            loss_pct = (price - entry_price) / entry_price
            if loss_pct <= -stop_loss_pct:  # Stop loss hit
                revenue = position * price
                balance += revenue
                trades.append({
                    'date': df.index[i],
                    'type': 'STOP_LOSS',
                    'price': price,
                    'position': 0,
                    'balance': balance,
                    'return_pct': (balance - initial_balance) / initial_balance * 100
                })
                position = 0
                continue
                
            if loss_pct >= take_profit_pct:  # Take profit hit
                revenue = position * price
                balance += revenue
                trades.append({
                    'date': df.index[i],
                    'type': 'TAKE_PROFIT',
                    'price': price,
                    'position': 0,
                    'balance': balance,
                    'return_pct': (balance - initial_balance) / initial_balance * 100
                })
                position = 0
                continue
        
        decision = trading_signal(price, sma_10, sma_50, sentiment=0)
        
        if decision == "BUY" and balance > price and position == 0:
            position = (balance * 0.95) // price  # Use 95% of balance for position
            cost = position * price
            balance -= cost
            entry_price = price
            trades.append({
                'date': df.index[i],
                'type': 'BUY',
                'price': price,
                'position': position,
                'balance': balance,
                'return_pct': (balance - initial_balance) / initial_balance * 100
            })
            
        elif decision == "SELL" and position > 0:
            revenue = position * price
            balance += revenue
            trades.append({
                'date': df.index[i],
                'type': 'SELL',
                'price': price,
                'position': 0,
                'balance': balance,
                'return_pct': (balance - initial_balance) / initial_balance * 100
            })
            position = 0
    
    # Close any remaining position at the end
    if position > 0:
        final_price = df["Close"].iloc[-1].item()
        final_position_value = position * final_price
        balance += final_position_value
        position = 0
    
    total_value = balance
    
    # Print results
    print(f"\nBacktest Results:")
    print(f"Initial Balance: ${initial_balance:,.2f}")
    print(f"Final Balance: ${balance:,.2f}")
    print(f"Return: {((balance/initial_balance)-1)*100:.2f}%")
    print(f"Number of Trades: {len(trades)}")
    
    trades_df = pd.DataFrame(trades)
    if not trades_df.empty:
        print("\nStrategy Performance:")
        print(f"Win Rate: {len(trades_df[trades_df['return_pct'] > 0])/len(trades_df)*100:.1f}%")
        print(f"Average Return per Trade: {trades_df['return_pct'].mean():.2f}%")
        print(f"Best Trade: {trades_df['return_pct'].max():.2f}%")
        print(f"Worst Trade: {trades_df['return_pct'].min():.2f}%")
    
    return trades_df

if __name__ == "__main__":
    trades_df = run_backtest()
    if trades_df is not None and not trades_df.empty:
        print("\nTrade History:")
        print(trades_df)
