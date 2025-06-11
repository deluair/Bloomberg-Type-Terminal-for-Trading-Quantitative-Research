"""Algorithmic trading strategies component."""
import dash_bootstrap_components as dbc
from dash import html, dcc, dash_table
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random


def generate_strategy_performance():
    """Generate algorithmic trading strategy performance data."""
    strategies = [
        {
            'name': 'Mean Reversion Alpha',
            'status': 'ACTIVE',
            'daily_pnl': 2845.32,
            'total_pnl': 185420.18,
            'sharpe': 1.89,
            'max_dd': -0.032,
            'win_rate': 0.684,
            'trades_today': 28,
            'avg_trade': 101.62,
            'allocation': 2500000,
            'risk_level': 'Medium'
        },
        {
            'name': 'Momentum Breakout',
            'status': 'ACTIVE',
            'daily_pnl': -1245.89,
            'total_pnl': 97532.45,
            'sharpe': 1.45,
            'max_dd': -0.058,
            'win_rate': 0.592,
            'trades_today': 15,
            'avg_trade': -83.06,
            'allocation': 1800000,
            'risk_level': 'High'
        },
        {
            'name': 'Pairs Trading Stat Arb',
            'status': 'ACTIVE',
            'daily_pnl': 3156.78,
            'total_pnl': 245890.33,
            'sharpe': 2.12,
            'max_dd': -0.024,
            'win_rate': 0.729,
            'trades_today': 42,
            'avg_trade': 75.16,
            'allocation': 3200000,
            'risk_level': 'Low'
        },
        {
            'name': 'Vol Surface Arbitrage',
            'status': 'PAUSED',
            'daily_pnl': 0.00,
            'total_pnl': 156742.91,
            'sharpe': 1.67,
            'max_dd': -0.041,
            'win_rate': 0.651,
            'trades_today': 0,
            'avg_trade': 0.00,
            'allocation': 2100000,
            'risk_level': 'Medium'
        },
        {
            'name': 'ML Sentiment Predictor',
            'status': 'ACTIVE',
            'daily_pnl': 4892.15,
            'total_pnl': 312456.78,
            'sharpe': 2.34,
            'max_dd': -0.028,
            'win_rate': 0.742,
            'trades_today': 18,
            'avg_trade': 271.79,
            'allocation': 4000000,
            'risk_level': 'Medium'
        }
    ]
    
    return strategies


def generate_strategy_equity_curves():
    """Generate equity curves for strategies."""
    dates = pd.date_range(start=datetime.now() - timedelta(days=90), end=datetime.now(), freq='D')
    
    strategies = {
        'Mean Reversion Alpha': [100000],
        'Momentum Breakout': [100000],
        'Pairs Trading Stat Arb': [100000],
        'ML Sentiment Predictor': [100000]
    }
    
    # Simulate daily returns
    for i in range(1, len(dates)):
        strategies['Mean Reversion Alpha'].append(
            strategies['Mean Reversion Alpha'][-1] * (1 + np.random.normal(0.001, 0.015))
        )
        strategies['Momentum Breakout'].append(
            strategies['Momentum Breakout'][-1] * (1 + np.random.normal(0.0008, 0.025))
        )
        strategies['Pairs Trading Stat Arb'].append(
            strategies['Pairs Trading Stat Arb'][-1] * (1 + np.random.normal(0.0012, 0.012))
        )
        strategies['ML Sentiment Predictor'].append(
            strategies['ML Sentiment Predictor'][-1] * (1 + np.random.normal(0.0015, 0.018))
        )
    
    return dates, strategies


def create_strategy_overview_chart():
    """Create strategy performance overview chart."""
    strategies = generate_strategy_performance()
    
    # Extract data for charts
    names = [s['name'] for s in strategies if s['status'] == 'ACTIVE']
    daily_pnls = [s['daily_pnl'] for s in strategies if s['status'] == 'ACTIVE']
    sharpe_ratios = [s['sharpe'] for s in strategies if s['status'] == 'ACTIVE']
    allocations = [s['allocation'] for s in strategies if s['status'] == 'ACTIVE']
    
    # Create subplots
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Daily P&L by Strategy', 'Sharpe Ratios', 'Capital Allocation', 'Win Rates'),
        specs=[[{"type": "bar"}, {"type": "bar"}],
               [{"type": "pie"}, {"type": "bar"}]]
    )
    
    # Daily P&L
    colors_pnl = ['green' if x > 0 else 'red' for x in daily_pnls]
    fig.add_trace(
        go.Bar(x=names, y=daily_pnls, marker_color=colors_pnl, name="Daily P&L"),
        row=1, col=1
    )
    
    # Sharpe ratios
    fig.add_trace(
        go.Bar(x=names, y=sharpe_ratios, marker_color='lightblue', name="Sharpe Ratio"),
        row=1, col=2
    )
    
    # Capital allocation pie chart
    fig.add_trace(
        go.Pie(labels=names, values=allocations, name="Allocation"),
        row=2, col=1
    )
    
    # Win rates
    win_rates = [s['win_rate'] * 100 for s in strategies if s['status'] == 'ACTIVE']
    fig.add_trace(
        go.Bar(x=names, y=win_rates, marker_color='orange', name="Win Rate %"),
        row=2, col=2
    )
    
    fig.update_layout(
        title="Strategy Performance Dashboard",
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=600,
        showlegend=False
    )
    
    return fig


def create_equity_curves_chart():
    """Create equity curves for all strategies."""
    dates, strategies = generate_strategy_equity_curves()
    
    fig = go.Figure()
    
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
    
    for i, (strategy_name, equity_curve) in enumerate(strategies.items()):
        fig.add_trace(go.Scatter(
            x=dates,
            y=equity_curve,
            mode='lines',
            name=strategy_name,
            line=dict(color=colors[i], width=2)
        ))
    
    fig.update_layout(
        title="Strategy Equity Curves (90 Days)",
        xaxis_title="Date",
        yaxis_title="Portfolio Value ($)",
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=400,
        legend=dict(x=0.02, y=0.98)
    )
    
    return fig


def create_risk_metrics_heatmap():
    """Create risk metrics heatmap for strategies."""
    strategies = generate_strategy_performance()
    active_strategies = [s for s in strategies if s['status'] == 'ACTIVE']
    
    metrics = ['Sharpe Ratio', 'Max Drawdown', 'Win Rate', 'Volatility']
    strategy_names = [s['name'][:15] + '...' if len(s['name']) > 15 else s['name'] for s in active_strategies]
    
    # Normalize metrics for heatmap (0-1 scale)
    data = []
    for strategy in active_strategies:
        row = [
            strategy['sharpe'] / 3.0,  # Normalize Sharpe (assume max 3.0)
            1 - abs(strategy['max_dd']),  # Invert drawdown (lower is better)
            strategy['win_rate'],  # Already 0-1
            1 - (0.02 + random.random() * 0.03)  # Simulated volatility (inverted)
        ]
        data.append(row)
    
    fig = go.Figure(data=go.Heatmap(
        z=data,
        x=metrics,
        y=strategy_names,
        colorscale='RdYlGn',
        text=[[f"{val:.2f}" for val in row] for row in data],
        texttemplate="%{text}",
        textfont={"size": 12},
        hoverongaps=False
    ))
    
    fig.update_layout(
        title="Strategy Risk Metrics Heatmap",
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=300
    )
    
    return fig


def create_real_time_trades_chart():
    """Create real-time trades chart."""
    # Generate sample intraday trades
    now = datetime.now()
    times = [now - timedelta(minutes=x) for x in range(60, 0, -5)]
    
    trades_data = []
    cumulative_pnl = 0
    
    for time in times:
        trade_pnl = random.uniform(-500, 800)
        cumulative_pnl += trade_pnl
        trades_data.append({
            'time': time,
            'trade_pnl': trade_pnl,
            'cumulative_pnl': cumulative_pnl
        })
    
    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=('Individual Trade P&L', 'Cumulative P&L'),
        shared_xaxes=True,
        vertical_spacing=0.1
    )
    
    # Individual trades
    colors = ['green' if x['trade_pnl'] > 0 else 'red' for x in trades_data]
    fig.add_trace(
        go.Bar(
            x=[x['time'] for x in trades_data],
            y=[x['trade_pnl'] for x in trades_data],
            marker_color=colors,
            name="Trade P&L"
        ),
        row=1, col=1
    )
    
    # Cumulative P&L
    fig.add_trace(
        go.Scatter(
            x=[x['time'] for x in trades_data],
            y=[x['cumulative_pnl'] for x in trades_data],
            mode='lines+markers',
            line=dict(color='white', width=2),
            name="Cumulative P&L"
        ),
        row=2, col=1
    )
    
    fig.update_layout(
        title="Real-Time Trading Activity",
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=500,
        showlegend=False
    )
    
    return fig


def create_ml_features_importance():
    """Create ML model features importance chart."""
    features = [
        'Price Momentum (5d)', 'Volume Ratio', 'RSI', 'MACD Signal',
        'Bollinger Position', 'Sentiment Score', 'Options Flow',
        'Sector Rotation', 'VIX Level', 'Yield Curve'
    ]
    
    importance = [0.18, 0.15, 0.12, 0.11, 0.10, 0.09, 0.08, 0.07, 0.06, 0.04]
    
    fig = go.Figure(data=[
        go.Bar(
            y=features,
            x=importance,
            orientation='h',
            marker_color='lightblue'
        )
    ])
    
    fig.update_layout(
        title="ML Model Feature Importance",
        xaxis_title="Importance Score",
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=400
    )
    
    return fig


def get_layout():
    """Return the layout for algorithmic trading."""
    
    strategies = generate_strategy_performance()
    
    # Calculate summary metrics
    total_daily_pnl = sum(s['daily_pnl'] for s in strategies if s['status'] == 'ACTIVE')
    total_allocation = sum(s['allocation'] for s in strategies if s['status'] == 'ACTIVE')
    active_strategies_count = len([s for s in strategies if s['status'] == 'ACTIVE'])
    total_trades_today = sum(s['trades_today'] for s in strategies if s['status'] == 'ACTIVE')
    
    # Strategy table data
    table_data = []
    for strategy in strategies:
        status_badge = "success" if strategy['status'] == 'ACTIVE' else "warning"
        risk_color = "danger" if strategy['risk_level'] == 'High' else "warning" if strategy['risk_level'] == 'Medium' else "success"
        
        table_data.append({
            'Strategy': strategy['name'],
            'Status': strategy['status'],
            'Daily P&L': f"${strategy['daily_pnl']:,.2f}",
            'Total P&L': f"${strategy['total_pnl']:,.2f}",
            'Sharpe': f"{strategy['sharpe']:.2f}",
            'Max DD': f"{strategy['max_dd']:.1%}",
            'Win Rate': f"{strategy['win_rate']:.1%}",
            'Trades Today': strategy['trades_today'],
            'Allocation': f"${strategy['allocation']:,.0f}",
            'Risk Level': strategy['risk_level']
        })
    
    algo_trading_card = dbc.Card([
        dbc.CardHeader(html.H5("Algorithmic Trading Strategies")),
        dbc.CardBody([
            # Summary metrics row
            dbc.Row([
                dbc.Col([
                    html.H6("Total Daily P&L", className="text-muted"),
                    html.H4(
                        f"${total_daily_pnl:,.2f}", 
                        className="text-success" if total_daily_pnl >= 0 else "text-danger"
                    )
                ], width=3),
                dbc.Col([
                    html.H6("Active Strategies", className="text-muted"),
                    html.H4(f"{active_strategies_count}", className="text-primary")
                ], width=3),
                dbc.Col([
                    html.H6("Total Allocation", className="text-muted"),
                    html.H4(f"${total_allocation:,.0f}", className="text-info")
                ], width=3),
                dbc.Col([
                    html.H6("Trades Today", className="text-muted"),
                    html.H4(f"{total_trades_today}", className="text-warning")
                ], width=3),
            ], className="mb-4"),
            
            # Strategy controls
            dbc.Row([
                dbc.Col([
                    dbc.ButtonGroup([
                        dbc.Button("Start All", color="success", size="sm"),
                        dbc.Button("Pause All", color="warning", size="sm"),
                        dbc.Button("Emergency Stop", color="danger", size="sm"),
                    ])
                ], width=6),
                dbc.Col([
                    dbc.ButtonGroup([
                        dbc.Button("Rebalance", color="info", size="sm"),
                        dbc.Button("Deploy New", color="primary", size="sm"),
                        dbc.Button("Backtest", color="secondary", size="sm"),
                    ])
                ], width=6),
            ], className="mb-4"),
            
            # Charts tabs
            dbc.Tabs([
                dbc.Tab(label="Performance Overview", tab_id="performance"),
                dbc.Tab(label="Equity Curves", tab_id="equity"),
                dbc.Tab(label="Real-time Trades", tab_id="trades"),
                dbc.Tab(label="Risk Metrics", tab_id="risk"),
                dbc.Tab(label="ML Features", tab_id="ml"),
            ], id="algo-tabs", active_tab="performance"),
            
            html.Div(id="algo-content", children=[
                # Default performance chart
                dcc.Graph(
                    figure=create_strategy_overview_chart(),
                    config={'displayModeBar': True}
                )
            ], className="mt-3"),
            
            # Strategy table
            html.H6("Strategy Status & Performance", className="mt-4 mb-3"),
            dash_table.DataTable(
                data=table_data,
                columns=[
                    {"name": "Strategy", "id": "Strategy"},
                    {"name": "Status", "id": "Status"},
                    {"name": "Daily P&L", "id": "Daily P&L"},
                    {"name": "Total P&L", "id": "Total P&L"},
                    {"name": "Sharpe", "id": "Sharpe"},
                    {"name": "Max DD", "id": "Max DD"},
                    {"name": "Win Rate", "id": "Win Rate"},
                    {"name": "Trades Today", "id": "Trades Today"},
                    {"name": "Allocation", "id": "Allocation"},
                    {"name": "Risk Level", "id": "Risk Level"},
                ],
                style_cell={
                    'backgroundColor': 'rgba(0,0,0,0.3)',
                    'color': 'white',
                    'textAlign': 'center',
                    'fontSize': '12px',
                    'fontFamily': 'Arial'
                },
                style_header={
                    'backgroundColor': 'rgba(0,0,0,0.5)',
                    'fontWeight': 'bold'
                },
                style_data_conditional=[
                    {
                        'if': {'filter_query': '{Status} = ACTIVE'},
                        'backgroundColor': 'rgba(40, 167, 69, 0.3)',
                    },
                    {
                        'if': {'filter_query': '{Status} = PAUSED'},
                        'backgroundColor': 'rgba(255, 193, 7, 0.3)',
                    },
                    {
                        'if': {'filter_query': '{Daily P&L} contains "-"'},
                        'color': '#ff6b6b',
                    }
                ],
                page_size=10,
                sort_action="native",
                filter_action="native"
            ),
            
            # Risk management section
            html.Div([
                html.H6("Risk Management Controls", className="mt-4 mb-3"),
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                html.H6("Max Portfolio Risk", className="text-muted"),
                                html.H5("2.5%", className="text-warning"),
                                html.Small("Current: 1.8%", className="text-success")
                            ])
                        ], className="text-center")
                    ], width=3),
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                html.H6("Position Limits", className="text-muted"),
                                html.H5("$5M", className="text-info"),
                                html.Small("Largest: $4M", className="text-success")
                            ])
                        ], className="text-center")
                    ], width=3),
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                html.H6("Daily Loss Limit", className="text-muted"),
                                html.H5("$50K", className="text-danger"),
                                html.Small("Used: 22%", className="text-success")
                            ])
                        ], className="text-center")
                    ], width=3),
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                html.H6("Circuit Breakers", className="text-muted"),
                                html.H5("Active", className="text-success"),
                                html.Small("All systems OK", className="text-muted")
                            ])
                        ], className="text-center")
                    ], width=3),
                ])
            ])
        ])
    ], className="mb-4")
    
    return algo_trading_card 