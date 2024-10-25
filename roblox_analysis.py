import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def analyze_stock(ticker_symbol, period='2y'):
    # Download stock data
    stock = yf.Ticker(ticker_symbol)
    hist = stock.history(period=period)
    
    # Calculate key metrics
    hist['SMA_50'] = hist['Close'].rolling(window=50).mean()
    hist['SMA_200'] = hist['Close'].rolling(window=200).mean()
    hist['Daily_Return'] = hist['Close'].pct_change()
    hist['Volatility'] = hist['Daily_Return'].rolling(window=20).std() * np.sqrt(252) * 100
    
    # Create the visualization
    fig = make_subplots(rows=3, cols=1, 
                        subplot_titles=('Price and Moving Averages', 'Volume', 'Volatility'),
                        vertical_spacing=0.1,
                        row_heights=[0.5, 0.25, 0.25])

    # Price and Moving Averages
    fig.add_trace(
        go.Scatter(x=hist.index, y=hist['Close'], name='Close Price', line=dict(color='blue')),
        row=1, col=1
    )
    fig.add_trace(
        go.Scatter(x=hist.index, y=hist['SMA_50'], name='50-day SMA', line=dict(color='orange')),
        row=1, col=1
    )
    fig.add_trace(
        go.Scatter(x=hist.index, y=hist['SMA_200'], name='200-day SMA', line=dict(color='red')),
        row=1, col=1
    )

    # Volume
    fig.add_trace(
        go.Bar(x=hist.index, y=hist['Volume'], name='Volume', marker_color='gray'),
        row=2, col=1
    )

    # Volatility
    fig.add_trace(
        go.Scatter(x=hist.index, y=hist['Volatility'], name='20-day Volatility', 
                  line=dict(color='purple')),
        row=3, col=1
    )

    fig.update_layout(
        title=f'{ticker_symbol} Stock Analysis',
        height=1000,
        showlegend=True
    )

    # Calculate key statistics
    current_price = hist['Close'][-1]
    peak_price = hist['Close'].max()
    drawdown = ((peak_price - current_price) / peak_price) * 100
    volatility = hist['Daily_Return'].std() * np.sqrt(252) * 100
    total_return = ((hist['Close'][-1] / hist['Close'][0]) - 1) * 100
    
    stats = {
        'Current Price': f"${current_price:.2f}",
        'Peak Price': f"${peak_price:.2f}",
        'Drawdown from Peak': f"{drawdown:.1f}%",
        'Annual Volatility': f"{volatility:.1f}%",
        'Total Return': f"{total_return:.1f}%"
    }
    
    return fig, stats, stock.info

# Run the analysis for Roblox
fig, stats, company_info = analyze_stock('RBLX')

# Print key statistics and company information
print("\nKey Statistics:")
for key, value in stats.items():
    print(f"{key}: {value}")

print("\nCompany Information:")
key_metrics = ['marketCap', 'forwardPE', 'priceToBook', 'enterpriseValue', 'revenueGrowth']
for metric in key_metrics:
    if metric in company_info:
        if metric in ['marketCap', 'enterpriseValue']:
            value = f"${company_info[metric]:,.0f}"
        elif metric == 'revenueGrowth':
            value = f"{company_info[metric]:.1%}"
        else:
            value = f"{company_info[metric]:.2f}"
        print(f"{metric}: {value}")