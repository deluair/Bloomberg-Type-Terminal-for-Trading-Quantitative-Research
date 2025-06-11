"""Quantitative Research component for advanced financial analysis and backtesting."""
import dash_bootstrap_components as dbc
from dash import html, dcc, dash_table
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random


def generate_backtest_results():
    """Generate comprehensive backtesting results."""
    strategies = [
        {
            'name': 'Momentum Factor',
            'total_return': 0.18,
            'annual_volatility': 0.12,
            'sharpe_ratio': 1.45,
            'max_drawdown': -0.085,
            'calmar_ratio': 2.12,
            'win_rate': 0.62,
            'avg_win': 0.034,
            'avg_loss': -0.021,
            'trades': 156,
            'exposure': 0.85
        },
        {
            'name': 'Value Factor',
            'total_return': 0.14,
            'annual_volatility': 0.15,
            'sharpe_ratio': 0.89,
            'max_drawdown': -0.12,
            'calmar_ratio': 1.17,
            'win_rate': 0.58,
            'avg_win': 0.029,
            'avg_loss': -0.025,
            'trades': 142,
            'exposure': 0.92
        },
        {
            'name': 'Quality Factor',
            'total_return': 0.16,
            'annual_volatility': 0.11,
            'sharpe_ratio': 1.38,
            'max_drawdown': -0.067,
            'calmar_ratio': 2.39,
            'win_rate': 0.65,
            'avg_win': 0.031,
            'avg_loss': -0.018,
            'trades': 128,
            'exposure': 0.88
        },
        {
            'name': 'Low Volatility',
            'total_return': 0.12,
            'annual_volatility': 0.08,
            'sharpe_ratio': 1.52,
            'max_drawdown': -0.045,
            'calmar_ratio': 2.67,
            'win_rate': 0.69,
            'avg_win': 0.025,
            'avg_loss': -0.014,
            'trades': 98,
            'exposure': 0.95
        },
        {
            'name': 'Multi-Factor',
            'total_return': 0.22,
            'annual_volatility': 0.13,
            'sharpe_ratio': 1.68,
            'max_drawdown': -0.074,
            'calmar_ratio': 2.97,
            'win_rate': 0.67,
            'avg_win': 0.037,
            'avg_loss': -0.019,
            'trades': 186,
            'exposure': 0.89
        }
    ]
    
    return strategies


def generate_factor_exposures():
    """Generate factor exposure analysis."""
    factors = ['Market', 'Size', 'Value', 'Momentum', 'Quality', 'Low Vol', 'Profitability']
    
    portfolio_exposures = {
        'Current Portfolio': [0.95, -0.12, 0.34, 0.28, 0.45, -0.18, 0.31],
        'Benchmark (S&P 500)': [1.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
        'Value Strategy': [0.88, 0.25, 0.78, -0.15, 0.42, 0.08, 0.35],
        'Growth Strategy': [1.02, -0.35, -0.65, 0.55, 0.28, -0.25, 0.18],
        'Quality Strategy': [0.92, -0.08, 0.15, 0.12, 0.82, 0.15, 0.75]
    }
    
    return factors, portfolio_exposures


def generate_monte_carlo_simulation():
    """Generate Monte Carlo simulation results."""
    np.random.seed(42)
    
    # Parameters
    initial_value = 100
    years = 5
    trading_days = 252 * years
    num_simulations = 1000
    
    # Market parameters
    annual_return = 0.08
    annual_volatility = 0.16
    
    # Convert to daily
    daily_return = annual_return / 252
    daily_volatility = annual_volatility / np.sqrt(252)
    
    # Generate simulations
    simulations = []
    final_values = []
    
    for i in range(num_simulations):
        path = [initial_value]
        for day in range(trading_days):
            daily_change = np.random.normal(daily_return, daily_volatility)
            new_value = path[-1] * (1 + daily_change)
            path.append(new_value)
        simulations.append(path)
        final_values.append(path[-1])
    
    # Calculate percentiles
    percentiles = {
        'p5': np.percentile(final_values, 5),
        'p25': np.percentile(final_values, 25),
        'p50': np.percentile(final_values, 50),
        'p75': np.percentile(final_values, 75),
        'p95': np.percentile(final_values, 95)
    }
    
    return simulations, final_values, percentiles


def create_backtest_results_chart():
    """Create comprehensive backtesting results visualization."""
    strategies = generate_backtest_results()
    
    fig = make_subplots(
        rows=2, cols=3,
        subplot_titles=('Total Returns', 'Risk-Adjusted Returns', 'Drawdown Analysis', 
                       'Win Rate vs Avg Win', 'Trading Activity', 'Risk Metrics Comparison'),
        specs=[[{"type": "bar"}, {"type": "bar"}, {"type": "bar"}],
               [{"type": "scatter"}, {"type": "bar"}, {"type": "scatter"}]]
    )
    
    # Extract data
    names = [s['name'] for s in strategies]
    returns = [s['total_return'] * 100 for s in strategies]
    sharpe_ratios = [s['sharpe_ratio'] for s in strategies]
    max_drawdowns = [abs(s['max_drawdown']) * 100 for s in strategies]
    win_rates = [s['win_rate'] * 100 for s in strategies]
    avg_wins = [s['avg_win'] * 100 for s in strategies]
    trades = [s['trades'] for s in strategies]
    volatilities = [s['annual_volatility'] * 100 for s in strategies]
    calmar_ratios = [s['calmar_ratio'] for s in strategies]
    
    # Total Returns
    colors_returns = ['green' if x > 15 else 'orange' if x > 10 else 'red' for x in returns]
    fig.add_trace(
        go.Bar(x=names, y=returns, marker_color=colors_returns, name="Total Return %"),
        row=1, col=1
    )
    
    # Sharpe Ratios
    fig.add_trace(
        go.Bar(x=names, y=sharpe_ratios, marker_color='lightblue', name="Sharpe Ratio"),
        row=1, col=2
    )
    
    # Max Drawdowns
    fig.add_trace(
        go.Bar(x=names, y=max_drawdowns, marker_color='red', name="Max Drawdown %"),
        row=1, col=3
    )
    
    # Win Rate vs Avg Win scatter
    fig.add_trace(
        go.Scatter(x=win_rates, y=avg_wins, mode='markers+text',
                  text=names, textposition="top center",
                  marker=dict(size=10, color='blue'),
                  name="Win Rate vs Avg Win"),
        row=2, col=1
    )
    
    # Trading Activity
    fig.add_trace(
        go.Bar(x=names, y=trades, marker_color='purple', name="Number of Trades"),
        row=2, col=2
    )
    
    # Risk-Return scatter
    fig.add_trace(
        go.Scatter(x=volatilities, y=returns, mode='markers+text',
                  text=names, textposition="top center",
                  marker=dict(size=[c*5 for c in calmar_ratios], 
                            color=sharpe_ratios, colorscale='Viridis',
                            showscale=True),
                  name="Risk vs Return"),
        row=2, col=3
    )
    
    fig.update_layout(
        title="Quantitative Strategy Backtesting Results",
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=700,
        showlegend=False
    )
    
    return fig


def create_factor_exposure_chart():
    """Create factor exposure analysis chart."""
    factors, exposures = generate_factor_exposures()
    
    fig = go.Figure()
    
    colors = ['blue', 'gray', 'green', 'red', 'purple']
    
    for i, (portfolio_name, exposure_values) in enumerate(exposures.items()):
        fig.add_trace(go.Scatterpolar(
            r=exposure_values,
            theta=factors,
            fill='toself',
            name=portfolio_name,
            line_color=colors[i % len(colors)]
        ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[-1, 1]
            )),
        title="Factor Exposure Analysis",
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=500
    )
    
    return fig


def create_monte_carlo_chart():
    """Create Monte Carlo simulation visualization."""
    simulations, final_values, percentiles = generate_monte_carlo_simulation()
    
    # Create dates for x-axis
    dates = pd.date_range(start=datetime.now(), periods=len(simulations[0]), freq='D')
    
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Simulation Paths (Sample)', 'Final Value Distribution', 
                       'Percentile Bands', 'Risk Metrics'),
        specs=[[{"type": "scatter"}, {"type": "histogram"}],
               [{"type": "scatter"}, {"type": "bar"}]]
    )
    
    # Sample simulation paths (show 50 out of 1000)
    for i in range(0, 50, 5):
        fig.add_trace(
            go.Scatter(x=dates, y=simulations[i], mode='lines',
                      line=dict(width=1, color='rgba(100,149,237,0.3)'),
                      showlegend=False, name=f"Path {i}"),
            row=1, col=1
        )
    
    # Final value histogram
    fig.add_trace(
        go.Histogram(x=final_values, nbinsx=50, marker_color='lightblue',
                    name="Final Values"),
        row=1, col=2
    )
    
    # Percentile bands
    percentile_paths = []
    for percentile in [5, 25, 50, 75, 95]:
        path = []
        for day in range(len(dates)):
            day_values = [sim[day] for sim in simulations]
            path.append(np.percentile(day_values, percentile))
        percentile_paths.append(path)
    
    colors_p = ['red', 'orange', 'blue', 'orange', 'red']
    names_p = ['5th %ile', '25th %ile', 'Median', '75th %ile', '95th %ile']
    
    for i, (path, color, name) in enumerate(zip(percentile_paths, colors_p, names_p)):
        fig.add_trace(
            go.Scatter(x=dates, y=path, mode='lines',
                      line=dict(color=color), name=name),
            row=2, col=1
        )
    
    # Risk metrics
    prob_loss = len([x for x in final_values if x < 100]) / len(final_values) * 100
    expected_return = (np.mean(final_values) - 100) / 100 * 100
    volatility = np.std(final_values) / 100 * 100
    var_5 = (100 - percentiles['p5']) / 100 * 100
    
    risk_metrics = ['Prob of Loss (%)', 'Expected Return (%)', 'Volatility (%)', 'VaR 5% (%)']
    risk_values = [prob_loss, expected_return, volatility, var_5]
    
    fig.add_trace(
        go.Bar(x=risk_metrics, y=risk_values, marker_color='green',
               name="Risk Metrics"),
        row=2, col=2
    )
    
    fig.update_layout(
        title="Monte Carlo Simulation Analysis (5 Years, 1000 Paths)",
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=700,
        showlegend=True
    )
    
    return fig


def create_performance_attribution():
    """Create performance attribution analysis."""
    # Attribution data
    sectors = ['Technology', 'Healthcare', 'Financials', 'Consumer Disc.', 'Energy', 'Industrials']
    allocation_effect = [0.45, 0.23, -0.12, 0.18, -0.34, 0.08]
    selection_effect = [0.67, 0.34, 0.45, -0.23, 0.12, 0.28]
    interaction_effect = [0.08, 0.05, -0.03, 0.02, -0.01, 0.04]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='Allocation Effect',
        x=sectors,
        y=allocation_effect,
        marker_color='lightblue'
    ))
    
    fig.add_trace(go.Bar(
        name='Selection Effect',
        x=sectors,
        y=selection_effect,
        marker_color='lightgreen'
    ))
    
    fig.add_trace(go.Bar(
        name='Interaction Effect',
        x=sectors,
        y=interaction_effect,
        marker_color='orange'
    ))
    
    fig.update_layout(
        title="Performance Attribution Analysis (% Contribution)",
        xaxis_title="Sectors",
        yaxis_title="Contribution (%)",
        barmode='group',
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=400
    )
    
    return fig


def get_layout():
    """Return the layout for quantitative research."""
    
    strategies = generate_backtest_results()
    
    # Calculate summary metrics
    best_strategy = max(strategies, key=lambda x: x['sharpe_ratio'])
    avg_return = np.mean([s['total_return'] for s in strategies]) * 100
    avg_sharpe = np.mean([s['sharpe_ratio'] for s in strategies])
    total_trades = sum([s['trades'] for s in strategies])
    
    quant_card = dbc.Card([
        dbc.CardHeader(html.H5("Quantitative Research & Analytics")),
        dbc.CardBody([
            # Summary metrics row
            dbc.Row([
                dbc.Col([
                    html.H6("Best Strategy", className="text-muted"),
                    html.H4(best_strategy['name'], className="text-success")
                ], width=3),
                dbc.Col([
                    html.H6("Average Return", className="text-muted"),
                    html.H4(f"{avg_return:.1f}%", className="text-primary")
                ], width=3),
                dbc.Col([
                    html.H6("Average Sharpe", className="text-muted"),
                    html.H4(f"{avg_sharpe:.2f}", className="text-info")
                ], width=3),
                dbc.Col([
                    html.H6("Total Backtests", className="text-muted"),
                    html.H4(f"{len(strategies)}", className="text-warning")
                ], width=3),
            ], className="mb-4"),
            
            # Research tools controls
            dbc.Row([
                dbc.Col([
                    dbc.ButtonGroup([
                        dbc.Button("Run Backtest", color="primary", size="sm"),
                        dbc.Button("Factor Analysis", color="info", size="sm"),
                        dbc.Button("Monte Carlo", color="success", size="sm"),
                    ])
                ], width=6),
                dbc.Col([
                    dbc.ButtonGroup([
                        dbc.Button("Performance Attribution", color="warning", size="sm"),
                        dbc.Button("Risk Analysis", color="danger", size="sm"),
                        dbc.Button("Export Results", color="secondary", size="sm"),
                    ])
                ], width=6),
            ], className="mb-4"),
            
            # Analysis tabs
            dbc.Tabs([
                dbc.Tab(label="Backtest Results", tab_id="backtest"),
                dbc.Tab(label="Factor Exposure", tab_id="factors"),
                dbc.Tab(label="Monte Carlo", tab_id="monte-carlo"),
                dbc.Tab(label="Performance Attribution", tab_id="attribution"),
            ], id="quant-tabs", active_tab="backtest"),
            
            html.Div(id="quant-content", children=[
                # Default backtest results
                dcc.Graph(
                    figure=create_backtest_results_chart(),
                    config={'displayModeBar': True}
                )
            ], className="mt-3"),
            
            # Strategy Results Table
            html.H6("Strategy Performance Summary", className="mt-4 mb-3"),
            dash_table.DataTable(
                data=[{
                    'Strategy': s['name'],
                    'Total Return': f"{s['total_return']:.1%}",
                    'Volatility': f"{s['annual_volatility']:.1%}",
                    'Sharpe Ratio': f"{s['sharpe_ratio']:.2f}",
                    'Max Drawdown': f"{s['max_drawdown']:.1%}",
                    'Calmar Ratio': f"{s['calmar_ratio']:.2f}",
                    'Win Rate': f"{s['win_rate']:.1%}",
                    'Trades': s['trades'],
                    'Exposure': f"{s['exposure']:.1%}"
                } for s in strategies],
                columns=[
                    {"name": "Strategy", "id": "Strategy"},
                    {"name": "Total Return", "id": "Total Return"},
                    {"name": "Volatility", "id": "Volatility"},
                    {"name": "Sharpe Ratio", "id": "Sharpe Ratio"},
                    {"name": "Max Drawdown", "id": "Max Drawdown"},
                    {"name": "Calmar Ratio", "id": "Calmar Ratio"},
                    {"name": "Win Rate", "id": "Win Rate"},
                    {"name": "Trades", "id": "Trades"},
                    {"name": "Exposure", "id": "Exposure"},
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
                        'if': {'filter_query': '{Sharpe Ratio} > 1.5'},
                        'backgroundColor': 'rgba(40, 167, 69, 0.3)',
                    },
                    {
                        'if': {'filter_query': '{Sharpe Ratio} > 1.0 && {Sharpe Ratio} <= 1.5'},
                        'backgroundColor': 'rgba(255, 193, 7, 0.3)',
                    },
                    {
                        'if': {'filter_query': '{Sharpe Ratio} <= 1.0'},
                        'backgroundColor': 'rgba(220, 53, 69, 0.3)',
                    }
                ],
                sort_action="native",
                filter_action="native"
            ),
            
            # Research insights
            html.Div([
                html.H6("Research Insights", className="mt-4 mb-3"),
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                html.H6("📊 Factor Analysis", className="text-info"),
                                html.P("Multi-factor strategy shows highest Sharpe", className="mb-1"),
                                html.P("Quality factor provides best risk-adjusted returns", className="mb-1"),
                                html.Small("Momentum shows highest volatility", className="text-muted")
                            ])
                        ])
                    ], width=3),
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                html.H6("🎯 Risk Analysis", className="text-warning"),
                                html.P("Low Vol strategy has lowest drawdown", className="mb-1"),
                                html.P("Value strategy shows highest volatility", className="mb-1"),
                                html.Small("Correlation analysis suggests diversification", className="text-muted")
                            ])
                        ])
                    ], width=3),
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                html.H6("🔄 Optimization", className="text-success"),
                                html.P("Portfolio optimization ongoing", className="mb-1"),
                                html.P("Risk parity approach recommended", className="mb-1"),
                                html.Small("Rebalancing frequency: Monthly", className="text-muted")
                            ])
                        ])
                    ], width=3),
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                html.H6("📈 Forward Testing", className="text-primary"),
                                html.P("Paper trading active for 3 strategies", className="mb-1"),
                                html.P("Live performance tracking enabled", className="mb-1"),
                                html.Small("Out-of-sample validation: 6 months", className="text-muted")
                            ])
                        ])
                    ], width=3),
                ])
            ])
        ])
    ], className="mb-4")
    
    return quant_card 