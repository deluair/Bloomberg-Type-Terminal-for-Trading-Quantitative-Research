"""Market Overview component for the dashboard."""
from datetime import datetime
from collections import deque
import yfinance as yf

import dash_bootstrap_components as dbc
from dash import html, dcc
import plotly.graph_objects as go

# Use a deque to hold a rolling window of prices (for lightweight example)
MAX_POINTS = 120  # e.g., last 2 minutes if interval is 1s
price_history = deque(maxlen=MAX_POINTS)

# Add real data cache
_real_data_cache = {}


def get_real_market_data(symbol: str = "AAPL"):
    """Get real market data from Yahoo Finance."""
    try:
        ticker = yf.Ticker(symbol)
        
        # Get current data
        info = ticker.info
        hist = ticker.history(period='5d', interval='1m')
        
        if hist.empty:
            return None
            
        # Get latest price
        latest_price = hist['Close'].iloc[-1]
        previous_close = info.get('previousClose', latest_price)
        
        # Calculate change
        change = latest_price - previous_close
        change_percent = (change / previous_close) * 100 if previous_close != 0 else 0
        
        # Get recent price history for the chart
        recent_prices = hist['Close'].tail(MAX_POINTS).tolist()
        
        return {
            'symbol': symbol,
            'current_price': latest_price,
            'change': change,
            'change_percent': change_percent,
            'volume': int(hist['Volume'].iloc[-1]),
            'open': hist['Open'].iloc[-1],
            'high': hist['High'].iloc[-1],
            'low': hist['Low'].iloc[-1],
            'previous_close': previous_close,
            'price_history': recent_prices,
            'timestamp': datetime.now(),
            'market_cap': info.get('marketCap'),
            'pe_ratio': info.get('trailingPE'),
            'company_name': info.get('longName', symbol)
        }
        
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return None


def get_layout(symbol: str = "AAPL") -> dbc.Card:
    """Return the layout for the market overview card."""
    
    # Get real market data
    market_data = get_real_market_data(symbol)
    
    if market_data:
        # Update price history with real data
        global price_history
        price_history.clear()
        price_history.extend(market_data['price_history'])
        
        # Cache the data for callbacks
        _real_data_cache[symbol] = market_data
        
        # Format display values
        current_price = f"${market_data['current_price']:.2f}"
        change_text = f"${market_data['change']:+.2f} ({market_data['change_percent']:+.2f}%)"
        change_color = "text-success" if market_data['change'] >= 0 else "text-danger"
        volume_text = f"{market_data['volume']:,}"
        
        # Additional metrics
        market_cap_text = f"${market_data['market_cap']/1e9:.1f}B" if market_data['market_cap'] else "N/A"
        pe_ratio_text = f"{market_data['pe_ratio']:.2f}" if market_data['pe_ratio'] else "N/A"
        
    else:
        # Fallback values if data fetch fails
        current_price = "Loading..."
        change_text = "Loading..."
        change_color = "text-muted"
        volume_text = "Loading..."
        market_cap_text = "N/A"
        pe_ratio_text = "N/A"

    card = dbc.Card(
        [
            dbc.CardHeader(
                html.Div([
                    html.H5(f"Real-Time Market Data - {symbol}", className="mb-0"),
                    html.Small(f"Last updated: {datetime.now().strftime('%H:%M:%S')}", 
                              className="text-muted")
                ])
            ),
            dbc.CardBody(
                [
                    # Price and change row
                    dbc.Row([
                        dbc.Col([
                            html.Div(id="price-ticker", children=current_price, 
                                    className="fs-2 text-primary mb-2"),
                            html.Div(change_text, className=f"fs-5 {change_color}")
                        ], width=6),
                        dbc.Col([
                            html.Div([
                                html.Small("Volume", className="text-muted d-block"),
                                html.Strong(volume_text, className="fs-6")
                            ], className="mb-2"),
                            html.Div([
                                html.Small("Market Cap", className="text-muted d-block"),
                                html.Strong(market_cap_text, className="fs-6")
                            ])
                        ], width=3),
                        dbc.Col([
                            html.Div([
                                html.Small("P/E Ratio", className="text-muted d-block"),
                                html.Strong(pe_ratio_text, className="fs-6")
                            ], className="mb-2"),
                            html.Div([
                                html.Small("Updated", className="text-muted d-block"),
                                html.Strong("Live", className="fs-6 text-success")
                            ])
                        ], width=3)
                    ], className="mb-3"),
                    
                    # Chart
                    dcc.Graph(id="price-chart", style={"height": "300px"}),
                    
                    # Hidden components for updates
                    dcc.Store(id="price-store"),
                    dcc.Interval(id="price-interval", interval=10000, n_intervals=0),  # 10 seconds for real data
                ]
            ),
        ],
        className="mb-4",
    )
    return card
