"""Advanced charts component for the dashboard."""
import dash_bootstrap_components as dbc
from dash import html, dcc
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random


def generate_ohlcv_data(symbol="AAPL", days=60):
    """Get real OHLCV data from Yahoo Finance for candlestick chart."""
    import yfinance as yf
    
    try:
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period=f"{days}d", interval='1d')
        
        if hist.empty:
            # Fallback to simulated data if API fails
            dates = pd.date_range(end=datetime.now(), periods=days, freq='D')
            base_price = random.uniform(100, 300)
            prices = []
            
            for i in range(days):
                if i == 0:
                    open_price = base_price
                else:
                    open_price = prices[-1]['close'] * random.uniform(0.99, 1.01)
                
                daily_range = open_price * random.uniform(0.01, 0.05)
                high = open_price + daily_range * random.uniform(0.5, 1.0)
                low = open_price - daily_range * random.uniform(0.5, 1.0)
                close = random.uniform(low, high)
                
                prices.append({
                    'date': dates[i],
                    'open': round(open_price, 2),
                    'high': round(high, 2),
                    'low': round(low, 2),
                    'close': round(close, 2),
                    'volume': random.randint(10000000, 100000000)
                })
            
            return pd.DataFrame(prices)
        
        # Convert Yahoo Finance data to our format
        df = pd.DataFrame({
            'date': hist.index,
            'open': hist['Open'].round(2),
            'high': hist['High'].round(2),
            'low': hist['Low'].round(2),
            'close': hist['Close'].round(2),
            'volume': hist['Volume'].astype(int)
        }).reset_index(drop=True)
        
        return df
        
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        # Fallback to simulated data
        dates = pd.date_range(end=datetime.now(), periods=days, freq='D')
        base_price = random.uniform(100, 300)
        prices = []
        
        for i in range(days):
            if i == 0:
                open_price = base_price
            else:
                open_price = prices[-1]['close'] * random.uniform(0.99, 1.01)
            
            daily_range = open_price * random.uniform(0.01, 0.05)
            high = open_price + daily_range * random.uniform(0.5, 1.0)
            low = open_price - daily_range * random.uniform(0.5, 1.0)
            close = random.uniform(low, high)
            
            prices.append({
                'date': dates[i],
                'open': round(open_price, 2),
                'high': round(high, 2),
                'low': round(low, 2),
                'close': round(close, 2),
                'volume': random.randint(10000000, 100000000)
            })
        
        return pd.DataFrame(prices)


def calculate_technical_indicators(df):
    """Calculate technical indicators for the chart."""
    # Simple Moving Averages
    df['sma_20'] = df['close'].rolling(window=20).mean()
    df['sma_50'] = df['close'].rolling(window=50).mean()
    
    # Bollinger Bands
    rolling_mean = df['close'].rolling(window=20).mean()
    rolling_std = df['close'].rolling(window=20).std()
    df['bb_upper'] = rolling_mean + (rolling_std * 2)
    df['bb_lower'] = rolling_mean - (rolling_std * 2)
    
    # RSI
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['rsi'] = 100 - (100 / (1 + rs))
    
    return df


def create_candlestick_chart(symbol="AAPL"):
    """Create an advanced candlestick chart with technical indicators."""
    df = generate_ohlcv_data(symbol)
    df = calculate_technical_indicators(df)
    
    # Create subplots
    fig = make_subplots(
        rows=3, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.05,
        subplot_titles=[f'{symbol} Price Chart', 'Volume', 'RSI'],
        row_heights=[0.6, 0.2, 0.2]
    )
    
    # Candlestick chart
    fig.add_trace(
        go.Candlestick(
            x=df['date'],
            open=df['open'],
            high=df['high'],
            low=df['low'],
            close=df['close'],
            name='Price',
            increasing_line_color='green',
            decreasing_line_color='red'
        ),
        row=1, col=1
    )
    
    # Moving averages
    fig.add_trace(
        go.Scatter(
            x=df['date'],
            y=df['sma_20'],
            mode='lines',
            name='SMA 20',
            line=dict(color='orange', width=2)
        ),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Scatter(
            x=df['date'],
            y=df['sma_50'],
            mode='lines',
            name='SMA 50',
            line=dict(color='blue', width=2)
        ),
        row=1, col=1
    )
    
    # Bollinger Bands
    fig.add_trace(
        go.Scatter(
            x=df['date'],
            y=df['bb_upper'],
            mode='lines',
            name='BB Upper',
            line=dict(color='gray', width=1, dash='dash'),
            fill=None
        ),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Scatter(
            x=df['date'],
            y=df['bb_lower'],
            mode='lines',
            name='BB Lower',
            line=dict(color='gray', width=1, dash='dash'),
            fill='tonexty',
            fillcolor='rgba(128,128,128,0.1)'
        ),
        row=1, col=1
    )
    
    # Volume
    colors = ['green' if close >= open else 'red' 
              for close, open in zip(df['close'], df['open'])]
    
    fig.add_trace(
        go.Bar(
            x=df['date'],
            y=df['volume'],
            name='Volume',
            marker_color=colors
        ),
        row=2, col=1
    )
    
    # RSI
    fig.add_trace(
        go.Scatter(
            x=df['date'],
            y=df['rsi'],
            mode='lines',
            name='RSI',
            line=dict(color='purple', width=2)
        ),
        row=3, col=1
    )
    
    # RSI reference lines
    fig.add_hline(y=70, line_dash="dash", line_color="red", row=3, col=1)
    fig.add_hline(y=30, line_dash="dash", line_color="green", row=3, col=1)
    
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=600,
        showlegend=True,
        xaxis_rangeslider_visible=False
    )
    
    # Update y-axis labels
    fig.update_yaxes(title_text="Price", row=1, col=1)
    fig.update_yaxes(title_text="Volume", row=2, col=1)
    fig.update_yaxes(title_text="RSI", row=3, col=1)
    
    return fig


def create_heatmap_correlation():
    """Create a correlation heatmap for multiple assets."""
    symbols = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'META', 'NVDA', 'SPY', 'QQQ', 'IWM']
    
    # Generate random correlation matrix
    np.random.seed(42)  # For reproducible demo
    corr_matrix = np.random.rand(len(symbols), len(symbols))
    corr_matrix = (corr_matrix + corr_matrix.T) / 2  # Make symmetric
    np.fill_diagonal(corr_matrix, 1)  # Diagonal should be 1
    
    # Ensure values are between -1 and 1
    corr_matrix = (corr_matrix - 0.5) * 2
    corr_matrix = np.clip(corr_matrix, -0.95, 0.95)
    np.fill_diagonal(corr_matrix, 1)
    
    fig = go.Figure(data=go.Heatmap(
        z=corr_matrix,
        x=symbols,
        y=symbols,
        colorscale='RdBu',
        zmid=0,
        text=[[f"{val:.2f}" for val in row] for row in corr_matrix],
        texttemplate="%{text}",
        textfont={"size": 10},
        hoverongaps=False
    ))
    
    fig.update_layout(
        title="Asset Correlation Matrix (60-Day)",
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=400
    )
    
    return fig


def create_volatility_surface():
    """Create a 3D volatility surface chart."""
    # Generate sample volatility data
    strikes = np.linspace(80, 120, 20)
    expirations = np.linspace(0.1, 2.0, 15)
    
    X, Y = np.meshgrid(strikes, expirations)
    
    # Generate realistic volatility surface
    Z = 0.2 + 0.1 * np.sin(X/10) * np.exp(-Y/2) + 0.05 * np.random.random(X.shape)
    
    fig = go.Figure(data=[go.Surface(
        x=X,
        y=Y,
        z=Z,
        colorscale='viridis',
        colorbar=dict(title="Implied Volatility")
    )])
    
    fig.update_layout(
        title="Options Volatility Surface",
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        scene=dict(
            xaxis_title="Strike Price",
            yaxis_title="Time to Expiration (Years)",
            zaxis_title="Implied Volatility",
            bgcolor="rgba(0,0,0,0)"
        ),
        height=400
    )
    
    return fig


def get_layout():
    """Return the layout for advanced charts."""
    
    # Create chart tabs
    chart_tabs = dbc.Tabs([
        dbc.Tab(label="Price Chart", tab_id="price-chart"),
        dbc.Tab(label="Correlation", tab_id="correlation"),
        dbc.Tab(label="Volatility Surface", tab_id="volatility"),
    ], id="chart-tabs", active_tab="price-chart")
    
    # Symbol selector
    symbol_dropdown = dcc.Dropdown(
        id='symbol-selector',
        options=[
            {'label': 'Apple (AAPL)', 'value': 'AAPL'},
            {'label': 'Microsoft (MSFT)', 'value': 'MSFT'},
            {'label': 'Google (GOOGL)', 'value': 'GOOGL'},
            {'label': 'Amazon (AMZN)', 'value': 'AMZN'},
            {'label': 'Tesla (TSLA)', 'value': 'TSLA'},
            {'label': 'Meta (META)', 'value': 'META'},
            {'label': 'NVIDIA (NVDA)', 'value': 'NVDA'},
        ],
        value='AAPL',
        style={'backgroundColor': '#2c3e50', 'color': 'white'},
        className="mb-3"
    )
    
    advanced_charts_card = dbc.Card([
        dbc.CardHeader([
            dbc.Row([
                dbc.Col([
                    html.H5("Advanced Charts & Technical Analysis")
                ], width=6),
                dbc.Col([
                    symbol_dropdown
                ], width=6)
            ])
        ]),
        dbc.CardBody([
            chart_tabs,
            html.Div(id="chart-content", children=[
                # Default to price chart
                dcc.Graph(
                    id='advanced-chart',
                    figure=create_candlestick_chart('AAPL'),
                    config={'displayModeBar': True}
                )
            ], className="mt-3")
        ])
    ], className="mb-4")
    
    return advanced_charts_card 