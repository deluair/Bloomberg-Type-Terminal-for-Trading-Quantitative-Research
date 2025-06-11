"""Enhanced market overview component for the dashboard."""
import dash_bootstrap_components as dbc
from dash import html, dcc, dash_table
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from datetime import datetime, timedelta
import random
import numpy as np


def generate_market_data():
    """Get real market data from Yahoo Finance for major symbols."""
    import yfinance as yf
    
    symbols = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'META', 'NVDA', 'SPY', 'QQQ', 'IWM', 'XLF', 'XLK', 'XLE']
    
    symbols_data = {}
    
    try:
        # Get data for all symbols at once for efficiency
        tickers = yf.Tickers(' '.join(symbols))
        
        for symbol in symbols:
            try:
                ticker = yf.Ticker(symbol)
                info = ticker.info
                hist = ticker.history(period='2d', interval='1m')
                
                if hist.empty:
                    continue
                
                # Get latest data
                latest_price = hist['Close'].iloc[-1]
                previous_close = info.get('previousClose', latest_price)
                change = latest_price - previous_close
                change_pct = (change / previous_close) * 100 if previous_close != 0 else 0
                
                symbols_data[symbol] = {
                    'name': info.get('longName', symbol),
                    'price': latest_price,
                    'change': change,
                    'change_pct': change_pct,
                    'volume': int(hist['Volume'].iloc[-1]) if 'Volume' in hist.columns else 0
                }
                
            except Exception as e:
                print(f"Error fetching data for {symbol}: {e}")
                # Fallback data
                symbols_data[symbol] = {
                    'name': symbol,
                    'price': 100.0,
                    'change': 0.0,
                    'change_pct': 0.0,
                    'volume': 0
                }
                
    except Exception as e:
        print(f"Error fetching Yahoo Finance data: {e}")
        # Return fallback data if API fails
        symbols_data = {
            'AAPL': {'name': 'Apple Inc.', 'price': 185.50, 'change': 2.35, 'volume': 45623000, 'change_pct': 1.28},
            'MSFT': {'name': 'Microsoft Corp.', 'price': 378.85, 'change': -1.20, 'volume': 28450000, 'change_pct': -0.32},
            'GOOGL': {'name': 'Alphabet Inc.', 'price': 141.75, 'change': 0.85, 'volume': 32187000, 'change_pct': 0.60},
        }
    
    return symbols_data


def create_market_heatmap():
    """Create a heatmap showing market performance."""
    market_data = generate_market_data()
    
    # Separate stocks and ETFs
    stocks = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'META', 'NVDA']
    etfs = ['SPY', 'QQQ', 'IWM', 'XLF', 'XLK', 'XLE']
    
    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=('Major Stocks', 'ETFs & Indices'),
        vertical_spacing=0.15
    )
    
    # Stocks heatmap
    stock_changes = [market_data[symbol]['change_pct'] for symbol in stocks]
    stock_colors = ['green' if x > 0 else 'red' for x in stock_changes]
    
    fig.add_trace(
        go.Bar(
            x=stocks,
            y=stock_changes,
            marker_color=stock_colors,
            text=[f"{x:.2f}%" for x in stock_changes],
            textposition='outside',
            name='Stocks'
        ),
        row=1, col=1
    )
    
    # ETFs heatmap
    etf_changes = [market_data[symbol]['change_pct'] for symbol in etfs]
    etf_colors = ['green' if x > 0 else 'red' for x in etf_changes]
    
    fig.add_trace(
        go.Bar(
            x=etfs,
            y=etf_changes,
            marker_color=etf_colors,
            text=[f"{x:.2f}%" for x in etf_changes],
            textposition='outside',
            name='ETFs'
        ),
        row=2, col=1
    )
    
    fig.update_layout(
        title="Market Performance Overview",
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=400,
        showlegend=False
    )
    
    return fig


def create_volume_treemap():
    """Create a treemap showing relative volume."""
    market_data = generate_market_data()
    
    symbols = list(market_data.keys())
    volumes = [market_data[symbol]['volume'] for symbol in symbols]
    changes = [market_data[symbol]['change_pct'] for symbol in symbols]
    
    # Create colors based on performance
    colors = ['green' if change > 0 else 'red' for change in changes]
    
    fig = go.Figure(go.Treemap(
        labels=symbols,
        values=volumes,
        parents=[""] * len(symbols),
        textinfo="label+value+percent parent",
        marker=dict(
            colorscale='RdYlGn',
            cmid=0,
            colorbar=dict(title="Performance %"),
            line=dict(width=2)
        ),
        hovertemplate='<b>%{label}</b><br>Volume: %{value:,}<br>Change: %{color:.2f}%<extra></extra>'
    ))
    
    fig.update_layout(
        title="Market Volume Distribution",
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=300
    )
    
    return fig


def create_market_breadth_chart():
    """Create a chart showing market breadth indicators."""
    # Generate sample breadth data
    dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
    
    # Advance/Decline ratio
    ad_ratio = [random.uniform(0.3, 3.0) for _ in range(30)]
    
    # New highs/lows
    new_highs = [random.randint(20, 200) for _ in range(30)]
    new_lows = [random.randint(5, 100) for _ in range(30)]
    
    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=('Advance/Decline Ratio', 'New Highs vs New Lows'),
        vertical_spacing=0.2
    )
    
    # A/D Ratio
    fig.add_trace(
        go.Scatter(
            x=dates,
            y=ad_ratio,
            mode='lines+markers',
            name='A/D Ratio',
            line=dict(color='cyan', width=2),
            marker=dict(size=4)
        ),
        row=1, col=1
    )
    
    # Add neutral line
    fig.add_hline(y=1.0, line_dash="dash", line_color="white", row=1, col=1)
    
    # New Highs/Lows
    fig.add_trace(
        go.Bar(
            x=dates,
            y=new_highs,
            name='New Highs',
            marker_color='green'
        ),
        row=2, col=1
    )
    
    fig.add_trace(
        go.Bar(
            x=dates,
            y=[-x for x in new_lows],  # Make negative for visual contrast
            name='New Lows',
            marker_color='red'
        ),
        row=2, col=1
    )
    
    fig.update_layout(
        title="Market Breadth Indicators",
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=400,
        showlegend=True
    )
    
    return fig


def get_layout():
    """Return the layout for the enhanced market overview."""
    
    # Generate sample data
    market_data = generate_market_data()
    
    # Create DataFrame for the table
    table_data = []
    for symbol, data in market_data.items():
        table_data.append({
            'Symbol': symbol,
            'Name': data['name'][:20] + '...' if len(data['name']) > 20 else data['name'],
            'Price': f"${data['price']:.2f}",
            'Change': f"${data['change']:+.2f}",
            'Change %': f"{data['change_pct']:+.2f}%",
            'Volume': f"{data['volume']:,}",
            'Raw Change %': data['change_pct']  # For conditional formatting
        })
    
    df = pd.DataFrame(table_data)
    
    # Calculate market summary stats
    total_gainers = len([x for x in market_data.values() if x['change'] > 0])
    total_losers = len([x for x in market_data.values() if x['change'] < 0])
    unchanged = len(market_data) - total_gainers - total_losers
    
    # Market sentiment
    sentiment = "Bullish" if total_gainers > total_losers else "Bearish" if total_losers > total_gainers else "Mixed"
    sentiment_color = "text-success" if sentiment == "Bullish" else "text-danger" if sentiment == "Bearish" else "text-warning"
    
    enhanced_market_card = dbc.Card([
        dbc.CardHeader(html.H5("Enhanced Market Overview")),
        dbc.CardBody([
            # Market summary row
            dbc.Row([
                dbc.Col([
                    html.H6("Market Sentiment", className="text-muted"),
                    html.H4(sentiment, className=sentiment_color)
                ], width=3),
                dbc.Col([
                    html.H6("Gainers", className="text-muted"),
                    html.H4(f"{total_gainers}", className="text-success")
                ], width=3),
                dbc.Col([
                    html.H6("Losers", className="text-muted"),
                    html.H4(f"{total_losers}", className="text-danger")
                ], width=3),
                dbc.Col([
                    html.H6("Unchanged", className="text-muted"),
                    html.H4(f"{unchanged}", className="text-info")
                ], width=3),
            ], className="mb-4"),
            
            # Main charts row
            dbc.Row([
                dbc.Col([
                    dcc.Graph(
                        figure=create_market_heatmap(),
                        config={'displayModeBar': False}
                    )
                ], width=8),
                dbc.Col([
                    dcc.Graph(
                        figure=create_volume_treemap(),
                        config={'displayModeBar': False}
                    )
                ], width=4),
            ], className="mb-4"),
            
            # Second row with market breadth and watchlist
            dbc.Row([
                dbc.Col([
                    dcc.Graph(
                        figure=create_market_breadth_chart(),
                        config={'displayModeBar': False}
                    )
                ], width=6),
                dbc.Col([
                    html.H6("Market Watchlist", className="mb-3"),
                    dash_table.DataTable(
                        data=df.drop('Raw Change %', axis=1).to_dict('records'),
                        columns=[
                            {"name": col, "id": col, "type": "text"}
                            for col in df.columns if col != 'Raw Change %'
                        ],
                        style_cell={
                            'backgroundColor': 'rgba(0,0,0,0)',
                            'color': 'white',
                            'textAlign': 'center',
                            'border': '1px solid #444',
                            'fontSize': '10px',
                            'fontFamily': 'monospace'
                        },
                        style_header={
                            'backgroundColor': '#2c3e50',
                            'fontWeight': 'bold',
                            'color': 'white'
                        },
                        style_data_conditional=[
                            {
                                'if': {'filter_query': '{Change %} contains +'},
                                'backgroundColor': 'rgba(40, 167, 69, 0.2)',
                                'color': '#28a745',
                            },
                            {
                                'if': {'filter_query': '{Change %} contains -'},
                                'backgroundColor': 'rgba(220, 53, 69, 0.2)',
                                'color': '#dc3545',
                            }
                        ],
                        sort_action="native",
                        filter_action="native",
                        page_size=15,
                        style_table={'height': '400px', 'overflowY': 'auto'}
                    )
                ], width=6),
            ])
        ])
    ], className="mb-4")
    
    return enhanced_market_card 