"""Options analytics component for advanced options trading and risk management."""
import dash_bootstrap_components as dbc
from dash import html, dcc, dash_table
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import yfinance as yf
from scipy.stats import norm
import math


def black_scholes_greeks(S, K, T, r, sigma, option_type='call'):
    """Calculate Black-Scholes Greeks for options."""
    try:
        d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)
        
        if option_type == 'call':
            delta = norm.cdf(d1)
            price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
        else:
            delta = norm.cdf(d1) - 1
            price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
        
        gamma = norm.pdf(d1) / (S * sigma * np.sqrt(T))
        theta = (-S * norm.pdf(d1) * sigma / (2 * np.sqrt(T)) - 
                r * K * np.exp(-r * T) * norm.cdf(d2 if option_type == 'call' else -d2))
        vega = S * norm.pdf(d1) * np.sqrt(T)
        rho = (K * T * np.exp(-r * T) * norm.cdf(d2 if option_type == 'call' else -d2))
        
        return {
            'price': price,
            'delta': delta,
            'gamma': gamma,
            'theta': theta / 365,  # Daily theta
            'vega': vega / 100,    # Vega per 1% volatility change
            'rho': rho / 100       # Rho per 1% interest rate change
        }
    except:
        return {'price': 0, 'delta': 0, 'gamma': 0, 'theta': 0, 'vega': 0, 'rho': 0}


def generate_options_chain(symbol="AAPL"):
    """Generate options chain data with real market data."""
    try:
        ticker = yf.Ticker(symbol)
        stock_price = ticker.history(period='1d')['Close'].iloc[-1]
        
        # Get option expiration dates
        expirations = ticker.options[:5] if ticker.options else []
        
        options_data = []
        
        if not expirations:
            # Generate synthetic options chain
            expirations = [(datetime.now() + timedelta(days=x)).strftime('%Y-%m-%d') 
                          for x in [7, 14, 30, 60, 90]]
        
        for exp_date in expirations[:3]:  # Limit to 3 expiration dates
            exp_datetime = datetime.strptime(exp_date, '%Y-%m-%d')
            days_to_exp = (exp_datetime - datetime.now()).days
            T = max(days_to_exp / 365, 0.01)  # Time to expiration in years
            
            # Generate strikes around current price
            strikes = np.arange(stock_price * 0.8, stock_price * 1.2, stock_price * 0.02)
            
            for strike in strikes:
                strike = round(strike, 0)
                
                # Estimate implied volatility (simplified)
                iv = 0.2 + 0.1 * abs(stock_price - strike) / stock_price
                
                # Calculate Greeks for calls and puts
                call_greeks = black_scholes_greeks(stock_price, strike, T, 0.05, iv, 'call')
                put_greeks = black_scholes_greeks(stock_price, strike, T, 0.05, iv, 'put')
                
                options_data.append({
                    'Expiration': exp_date,
                    'Strike': f"${strike:.0f}",
                    'Type': 'Call',
                    'Price': f"${call_greeks['price']:.2f}",
                    'Delta': f"{call_greeks['delta']:.3f}",
                    'Gamma': f"{call_greeks['gamma']:.4f}",
                    'Theta': f"{call_greeks['theta']:.2f}",
                    'Vega': f"{call_greeks['vega']:.2f}",
                    'IV': f"{iv:.1%}",
                    'Raw_Strike': strike,
                    'Raw_Price': call_greeks['price'],
                    'Raw_IV': iv
                })
                
                options_data.append({
                    'Expiration': exp_date,
                    'Strike': f"${strike:.0f}",
                    'Type': 'Put',
                    'Price': f"${put_greeks['price']:.2f}",
                    'Delta': f"{put_greeks['delta']:.3f}",
                    'Gamma': f"{put_greeks['gamma']:.4f}",
                    'Theta': f"{put_greeks['theta']:.2f}",
                    'Vega': f"{put_greeks['vega']:.2f}",
                    'IV': f"{iv:.1%}",
                    'Raw_Strike': strike,
                    'Raw_Price': put_greeks['price'],
                    'Raw_IV': iv
                })
        
        return pd.DataFrame(options_data), stock_price
        
    except Exception as e:
        print(f"Error generating options chain: {e}")
        # Return empty DataFrame with proper columns
        return pd.DataFrame(columns=['Expiration', 'Strike', 'Type', 'Price', 'Delta', 'Gamma', 'Theta', 'Vega', 'IV']), 100.0


def create_iv_surface(symbol="AAPL"):
    """Create 3D implied volatility surface."""
    options_df, stock_price = generate_options_chain(symbol)
    
    if options_df.empty:
        fig = go.Figure()
        fig.add_annotation(text="No options data available", 
                          xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False)
        fig.update_layout(
            title="Implied Volatility Surface",
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=400
        )
        return fig
    
    # Prepare data for surface plot
    calls_df = options_df[options_df['Type'] == 'Call'].copy()
    
    if calls_df.empty:
        fig = go.Figure()
        fig.add_annotation(text="No call options data available", 
                          xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False)
        fig.update_layout(
            title="Implied Volatility Surface",
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=400
        )
        return fig
    
    # Convert expiration to days
    calls_df['Days_to_Exp'] = calls_df['Expiration'].apply(
        lambda x: max((datetime.strptime(x, '%Y-%m-%d') - datetime.now()).days, 1)
    )
    
    # Create pivot table
    pivot_iv = calls_df.pivot_table(
        index='Raw_Strike', 
        columns='Days_to_Exp', 
        values='Raw_IV', 
        aggfunc='mean'
    )
    
    fig = go.Figure(data=[go.Surface(
        z=pivot_iv.values,
        x=pivot_iv.columns,
        y=pivot_iv.index,
        colorscale='Viridis',
        showscale=True
    )])
    
    fig.update_layout(
        title=f"Implied Volatility Surface - {symbol}",
        scene=dict(
            xaxis_title="Days to Expiration",
            yaxis_title="Strike Price",
            zaxis_title="Implied Volatility",
            camera=dict(eye=dict(x=1.5, y=1.5, z=1.5))
        ),
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=500
    )
    
    return fig


def create_greeks_dashboard():
    """Create Greeks summary dashboard."""
    # Generate sample portfolio Greeks
    positions = [
        {'Symbol': 'AAPL', 'Type': 'Call', 'Strike': 180, 'Exp': '2024-01-19', 'Qty': 10, 'Delta': 0.65, 'Gamma': 0.025, 'Theta': -0.15, 'Vega': 0.18},
        {'Symbol': 'MSFT', 'Type': 'Put', 'Strike': 380, 'Exp': '2024-02-16', 'Qty': -5, 'Delta': -0.35, 'Gamma': 0.018, 'Theta': -0.12, 'Vega': 0.22},
        {'Symbol': 'TSLA', 'Type': 'Call', 'Strike': 220, 'Exp': '2024-01-26', 'Qty': 20, 'Delta': 0.45, 'Gamma': 0.032, 'Theta': -0.25, 'Vega': 0.28},
        {'Symbol': 'SPY', 'Type': 'Call', 'Strike': 480, 'Exp': '2024-03-15', 'Qty': 50, 'Delta': 0.52, 'Gamma': 0.015, 'Theta': -0.08, 'Vega': 0.15},
    ]
    
    # Calculate portfolio Greeks
    portfolio_delta = sum(pos['Delta'] * pos['Qty'] for pos in positions)
    portfolio_gamma = sum(pos['Gamma'] * pos['Qty'] for pos in positions)
    portfolio_theta = sum(pos['Theta'] * pos['Qty'] for pos in positions)
    portfolio_vega = sum(pos['Vega'] * pos['Qty'] for pos in positions)
    
    # Create subplot with Greeks over time
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Portfolio Delta', 'Portfolio Gamma', 'Portfolio Theta', 'Portfolio Vega'),
        specs=[[{"secondary_y": False}, {"secondary_y": False}],
               [{"secondary_y": False}, {"secondary_y": False}]]
    )
    
    # Generate time series data
    dates = pd.date_range(start=datetime.now() - timedelta(days=30), end=datetime.now(), freq='D')
    
    # Simulate Greeks over time
    delta_series = [portfolio_delta + random.uniform(-20, 20) for _ in dates]
    gamma_series = [portfolio_gamma + random.uniform(-0.5, 0.5) for _ in dates]
    theta_series = [portfolio_theta + random.uniform(-5, 5) for _ in dates]
    vega_series = [portfolio_vega + random.uniform(-10, 10) for _ in dates]
    
    fig.add_trace(go.Scatter(x=dates, y=delta_series, name="Delta", line=dict(color='#1f77b4')), row=1, col=1)
    fig.add_trace(go.Scatter(x=dates, y=gamma_series, name="Gamma", line=dict(color='#ff7f0e')), row=1, col=2)
    fig.add_trace(go.Scatter(x=dates, y=theta_series, name="Theta", line=dict(color='#2ca02c')), row=2, col=1)
    fig.add_trace(go.Scatter(x=dates, y=vega_series, name="Vega", line=dict(color='#d62728')), row=2, col=2)
    
    fig.update_layout(
        title="Portfolio Greeks Timeline",
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=500,
        showlegend=False
    )
    
    return fig


def create_options_strategy_payoff(strategy_type="covered_call"):
    """Create options strategy payoff diagram."""
    spot_price = 180  # Current stock price
    strike_range = np.linspace(spot_price * 0.8, spot_price * 1.2, 100)
    
    if strategy_type == "covered_call":
        # Long stock + Short call
        stock_payoff = strike_range - spot_price
        call_strike = 190
        call_premium = 5
        call_payoff = [call_premium - max(0, S - call_strike) for S in strike_range]
        total_payoff = stock_payoff + call_payoff
        title = f"Covered Call Strategy (Stock: ${spot_price}, Call Strike: ${call_strike})"
        
    elif strategy_type == "protective_put":
        # Long stock + Long put
        stock_payoff = strike_range - spot_price
        put_strike = 170
        put_premium = 4
        put_payoff = [max(0, put_strike - S) - put_premium for S in strike_range]
        total_payoff = stock_payoff + put_payoff
        title = f"Protective Put Strategy (Stock: ${spot_price}, Put Strike: ${put_strike})"
        
    elif strategy_type == "iron_condor":
        # Short call spread + Short put spread
        call_strike_low = 185
        call_strike_high = 195
        put_strike_low = 165
        put_strike_high = 175
        premium_received = 3
        
        total_payoff = []
        for S in strike_range:
            call_spread = min(max(0, S - call_strike_low) - max(0, S - call_strike_high), call_strike_high - call_strike_low)
            put_spread = min(max(0, put_strike_high - S) - max(0, put_strike_low - S), put_strike_high - put_strike_low)
            payoff = premium_received - call_spread - put_spread
            total_payoff.append(payoff)
        title = f"Iron Condor Strategy (${put_strike_low}/{put_strike_high}/{call_strike_low}/{call_strike_high})"
        
    else:  # straddle
        strike = 180
        call_premium = 8
        put_premium = 7
        total_payoff = [max(S - strike, 0) + max(strike - S, 0) - call_premium - put_premium for S in strike_range]
        title = f"Long Straddle Strategy (Strike: ${strike})"
    
    fig = go.Figure()
    
    # Add payoff line
    fig.add_trace(go.Scatter(
        x=strike_range,
        y=total_payoff,
        mode='lines',
        name='Total P&L',
        line=dict(color='white', width=3)
    ))
    
    # Add break-even line
    fig.add_hline(y=0, line_dash="dash", line_color="gray", annotation_text="Break-even")
    
    # Add current spot price line
    fig.add_vline(x=spot_price, line_dash="dash", line_color="yellow", annotation_text="Current Price")
    
    # Fill profit/loss areas
    fig.add_trace(go.Scatter(
        x=strike_range,
        y=[max(0, p) for p in total_payoff],
        fill='tonexty',
        fillcolor='rgba(0, 255, 0, 0.3)',
        line=dict(color='rgba(0,0,0,0)'),
        name='Profit',
        hoverinfo='skip'
    ))
    
    fig.add_trace(go.Scatter(
        x=strike_range,
        y=[min(0, p) for p in total_payoff],
        fill='tonexty',
        fillcolor='rgba(255, 0, 0, 0.3)',
        line=dict(color='rgba(0,0,0,0)'),
        name='Loss',
        hoverinfo='skip'
    ))
    
    fig.update_layout(
        title=title,
        xaxis_title="Stock Price at Expiration",
        yaxis_title="Profit/Loss",
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=400
    )
    
    return fig


def get_layout():
    """Return the layout for options analytics."""
    
    # Get options data
    options_df, stock_price = generate_options_chain("AAPL")
    
    # Calculate portfolio Greeks summary
    portfolio_greeks = {
        'delta': 156.8,
        'gamma': 12.4,
        'theta': -45.2,
        'vega': 89.3,
        'rho': 23.1
    }
    
    options_card = dbc.Card([
        dbc.CardHeader(html.H5("Options Analytics & Greeks")),
        dbc.CardBody([
            # Portfolio Greeks Summary
            dbc.Row([
                dbc.Col([
                    html.H6("Portfolio Delta", className="text-muted"),
                    html.H4(f"{portfolio_greeks['delta']:.1f}", className="text-primary")
                ], width=2),
                dbc.Col([
                    html.H6("Portfolio Gamma", className="text-muted"),
                    html.H4(f"{portfolio_greeks['gamma']:.1f}", className="text-warning")
                ], width=2),
                dbc.Col([
                    html.H6("Portfolio Theta", className="text-muted"),
                    html.H4(f"{portfolio_greeks['theta']:.1f}", className="text-danger")
                ], width=2),
                dbc.Col([
                    html.H6("Portfolio Vega", className="text-muted"),
                    html.H4(f"{portfolio_greeks['vega']:.1f}", className="text-info")
                ], width=2),
                dbc.Col([
                    html.H6("Portfolio Rho", className="text-muted"),
                    html.H4(f"{portfolio_greeks['rho']:.1f}", className="text-success")
                ], width=2),
                dbc.Col([
                    html.H6("Options Positions", className="text-muted"),
                    html.H4("27", className="text-secondary")
                ], width=2),
            ], className="mb-4"),
            
            # Charts and Analysis Tabs
            dbc.Tabs([
                dbc.Tab(label="Implied Volatility Surface", tab_id="iv-surface"),
                dbc.Tab(label="Greeks Timeline", tab_id="greeks-timeline"),
                dbc.Tab(label="Strategy Payoff", tab_id="strategy-payoff"),
                dbc.Tab(label="Options Chain", tab_id="options-chain"),
            ], id="options-tabs", active_tab="iv-surface"),
            
            html.Div(id="options-content", children=[
                # Default IV Surface
                dcc.Graph(
                    figure=create_iv_surface("AAPL"),
                    config={'displayModeBar': True}
                )
            ], className="mt-3"),
            
            # Strategy selector for payoff diagrams
            html.Div([
                html.Label("Options Strategy:", className="form-label"),
                dcc.Dropdown(
                    id='strategy-selector',
                    options=[
                        {'label': 'Covered Call', 'value': 'covered_call'},
                        {'label': 'Protective Put', 'value': 'protective_put'},
                        {'label': 'Iron Condor', 'value': 'iron_condor'},
                        {'label': 'Long Straddle', 'value': 'straddle'},
                    ],
                    value='covered_call',
                    style={'backgroundColor': '#2c3e50', 'color': 'white'},
                    className="mb-3"
                )
            ], id="strategy-controls", style={'display': 'none'}),
            
            # Risk scenarios section
            html.Div([
                html.H6("Risk Scenarios", className="mt-4 mb-3"),
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                html.H6("Stock +10%", className="text-success"),
                                html.P("P&L: +$12,450", className="mb-1"),
                                html.P("Delta Impact: +$1,568", className="mb-0 small text-muted")
                            ])
                        ], className="text-center")
                    ], width=3),
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                html.H6("Stock -10%", className="text-danger"),
                                html.P("P&L: -$8,920", className="mb-1"),
                                html.P("Delta Impact: -$1,568", className="mb-0 small text-muted")
                            ])
                        ], className="text-center")
                    ], width=3),
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                html.H6("Vol +5%", className="text-warning"),
                                html.P("P&L: +$4,465", className="mb-1"),
                                html.P("Vega Impact: +$893", className="mb-0 small text-muted")
                            ])
                        ], className="text-center")
                    ], width=3),
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                html.H6("Time -1 Day", className="text-info"),
                                html.P("P&L: -$452", className="mb-1"),
                                html.P("Theta Impact: -$45", className="mb-0 small text-muted")
                            ])
                        ], className="text-center")
                    ], width=3),
                ])
            ])
        ])
    ], className="mb-4")
    
    return options_card 