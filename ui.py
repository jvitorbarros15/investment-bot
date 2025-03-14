import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
from fetch_data import fetch_stock_data
from indicators import calculate_moving_averages
from strategy import trading_signal
import numpy as np

def plot_trades(df, trades_df):
    """Create an interactive plot with price, MAs, and trade points"""
    fig = go.Figure()

    # Add price line
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df['Close'],
        name='Price',
        line=dict(color='#1f77b4', width=2)
    ))

    # Add moving averages
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df['SMA_10'],
        name='SMA 10',
        line=dict(color='#ff7f0e', width=1.5, dash='dot')
    ))

    fig.add_trace(go.Scatter(
        x=df.index,
        y=df['SMA_50'],
        name='SMA 50',
        line=dict(color='#2ca02c', width=1.5, dash='dot')
    ))

    # Add buy points
    buy_points = trades_df[trades_df['type'] == 'BUY']
    fig.add_trace(go.Scatter(
        x=buy_points['date'],
        y=buy_points['price'],
        mode='markers',
        name='Buy',
        marker=dict(
            color='green',
            size=12,
            symbol='triangle-up'
        )
    ))

    # Add sell points
    sell_points = trades_df[trades_df['type'].isin(['SELL', 'STOP_LOSS', 'TAKE_PROFIT'])]
    fig.add_trace(go.Scatter(
        x=sell_points['date'],
        y=sell_points['price'],
        mode='markers',
        name='Sell',
        marker=dict(
            color='red',
            size=12,
            symbol='triangle-down'
        )
    ))

    fig.update_layout(
        title='Trading Strategy Backtest Results',
        xaxis_title='Date',
        yaxis_title='Price',
        template='plotly_dark',
        height=600
    )

    return fig

def run_backtest(initial_balance, stop_loss_pct, take_profit_pct, position_size_pct):
    """Run backtest with given parameters"""
    df = fetch_stock_data(period="60d")
    if df is None or df.empty:
        return None, None
        
    df = calculate_moving_averages(df)
    
    balance = initial_balance
    position = 0
    trades = []
    entry_price = 0
    
    for i in range(50, len(df)):
        price = df["Close"].iloc[i].item()
        sma_10 = df["SMA_10"].iloc[i].item()
        sma_50 = df["SMA_50"].iloc[i].item()
        
        if position > 0:
            loss_pct = (price - entry_price) / entry_price
            if loss_pct <= -stop_loss_pct:
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
                
            if loss_pct >= take_profit_pct:
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
            position = (balance * position_size_pct) // price
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
    
    if position > 0:
        final_price = df["Close"].iloc[-1].item()
        final_position_value = position * final_price
        balance += final_position_value
        position = 0
    
    trades_df = pd.DataFrame(trades)
    return df, trades_df

def main():
    st.set_page_config(page_title="Trading Bot Backtest", layout="wide")
    
    st.title("Trading Bot Backtest Dashboard")
    
    # Sidebar controls
    st.sidebar.header("Backtest Parameters")
    
    initial_balance = st.sidebar.number_input(
        "Initial Balance ($)",
        min_value=1000,
        max_value=1000000,
        value=10000,
        step=1000
    )
    
    stop_loss_pct = st.sidebar.slider(
        "Stop Loss (%)",
        min_value=0.5,
        max_value=10.0,
        value=2.0,
        step=0.5
    ) / 100
    
    take_profit_pct = st.sidebar.slider(
        "Take Profit (%)",
        min_value=0.5,
        max_value=10.0,
        value=3.0,
        step=0.5
    ) / 100
    
    position_size_pct = st.sidebar.slider(
        "Position Size (%)",
        min_value=10,
        max_value=100,
        value=95,
        step=5
    ) / 100
    
    if st.sidebar.button("Run Backtest"):
        with st.spinner("Running backtest..."):
            df, trades_df = run_backtest(
                initial_balance,
                stop_loss_pct,
                take_profit_pct,
                position_size_pct
            )
            
            if trades_df is not None and not trades_df.empty:
                # Display chart
                fig = plot_trades(df, trades_df)
                st.plotly_chart(fig, use_container_width=True)
                
                # Display metrics in columns
                col1, col2, col3, col4 = st.columns(4)
                
                final_balance = trades_df['balance'].iloc[-1] if len(trades_df) > 0 else initial_balance
                total_return = ((final_balance/initial_balance)-1)*100
                
                col1.metric(
                    "Final Balance",
                    f"${final_balance:,.2f}",
                    f"{total_return:+.2f}%"
                )
                
                col2.metric(
                    "Number of Trades",
                    len(trades_df)
                )
                
                if len(trades_df) > 0:
                    win_rate = len(trades_df[trades_df['return_pct'] > 0])/len(trades_df)*100
                    col3.metric(
                        "Win Rate",
                        f"{win_rate:.1f}%"
                    )
                    
                    avg_return = trades_df['return_pct'].mean()
                    col4.metric(
                        "Avg Return per Trade",
                        f"{avg_return:.2f}%"
                    )
                
                # Display trade history
                st.subheader("Trade History")
                st.dataframe(
                    trades_df.style.format({
                        'price': '${:.2f}',
                        'balance': '${:.2f}',
                        'return_pct': '{:.2f}%'
                    })
                )

if __name__ == "__main__":
    main() 