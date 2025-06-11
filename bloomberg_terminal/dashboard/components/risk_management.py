"""Risk management component for the dashboard."""
import dash_bootstrap_components as dbc
from dash import html, dcc, dash_table
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random


def generate_risk_metrics():
    """Generate sample risk metrics for demonstration."""
    return {
        'var_1d': -125420.50,
        'var_10d': -396847.20,
        'expected_shortfall': -189635.40,
        'beta': 1.23,
        'volatility': 0.18,
        'sharpe_ratio': 1.42,
        'max_drawdown': -0.087,
        'correlation_spy': 0.78
    }


def generate_sector_exposure():
    """Generate sample sector exposure data."""
    sectors = ["Technology", "Healthcare", "Financial", "Consumer", "Industrial", "Energy", "Utilities", "Real Estate"]
    exposures = [random.uniform(-500000, 1500000) for _ in sectors]
    
    return pd.DataFrame({
        'Sector': sectors,
        'Exposure': exposures,
        'Percentage': [abs(exp) / sum(abs(e) for e in exposures) * 100 for exp in exposures]
    })


def generate_greeks_data():
    """Generate sample options Greeks data."""
    symbols = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]
    
    greeks_data = []
    for symbol in symbols:
        if random.random() > 0.4:  # Some symbols might have options positions
            greeks_data.append({
                'Symbol': symbol,
                'Delta': round(random.uniform(-50, 100), 2),
                'Gamma': round(random.uniform(0, 5), 3),
                'Theta': round(random.uniform(-20, -0.5), 2),
                'Vega': round(random.uniform(0, 15), 2),
                'Rho': round(random.uniform(-5, 5), 3)
            })
    
    return pd.DataFrame(greeks_data)


def create_var_timeline_chart():
    """Create a chart showing VaR over time."""
    dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
    var_values = []
    
    # Generate random walk for VaR
    current_var = -125000
    for _ in range(30):
        current_var += random.uniform(-15000, 15000)
        var_values.append(current_var)
    
    fig = go.Figure()
    
    # VaR line
    fig.add_trace(go.Scatter(
        x=dates,
        y=var_values,
        mode='lines+markers',
        name='1-Day VaR',
        line=dict(color='red', width=2),
        marker=dict(size=4)
    ))
    
    # Add threshold lines
    fig.add_hline(y=-200000, line_dash="dash", line_color="orange", 
                  annotation_text="Warning Level")
    fig.add_hline(y=-300000, line_dash="dash", line_color="red", 
                  annotation_text="Critical Level")
    
    fig.update_layout(
        title="Value at Risk (30-Day History)",
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=300,
        yaxis_title="VaR ($)",
        xaxis_title="Date",
        showlegend=True
    )
    
    return fig


def create_sector_exposure_chart():
    """Create a bar chart showing sector exposure."""
    df = generate_sector_exposure()
    
    colors = ['green' if x >= 0 else 'red' for x in df['Exposure']]
    
    fig = go.Figure(data=[
        go.Bar(
            x=df['Sector'],
            y=df['Exposure'],
            marker_color=colors,
            text=[f"${x:,.0f}" for x in df['Exposure']],
            textposition='outside'
        )
    ])
    
    fig.update_layout(
        title="Sector Exposure",
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=300,
        yaxis_title="Exposure ($)",
        xaxis_title="Sector",
        xaxis_tickangle=-45
    )
    
    return fig


def create_correlation_heatmap():
    """Create a correlation heatmap for major positions."""
    symbols = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "SPY"]
    
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
        title="Asset Correlation Matrix",
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=300
    )
    
    return fig


def get_layout():
    """Return the layout for the risk management view."""
    
    # Generate sample data
    risk_metrics = generate_risk_metrics()
    greeks_df = generate_greeks_data()
    
    risk_card = dbc.Card([
        dbc.CardHeader(html.H5("Risk Management")),
        dbc.CardBody([
            # Risk metrics summary row
            dbc.Row([
                dbc.Col([
                    html.H6("1-Day VaR (95%)", className="text-muted"),
                    html.H5(f"${risk_metrics['var_1d']:,.2f}", className="text-danger")
                ], width=3),
                dbc.Col([
                    html.H6("Expected Shortfall", className="text-muted"),
                    html.H5(f"${risk_metrics['expected_shortfall']:,.2f}", className="text-danger")
                ], width=3),
                dbc.Col([
                    html.H6("Portfolio Beta", className="text-muted"),
                    html.H5(f"{risk_metrics['beta']:.2f}", className="text-warning")
                ], width=3),
                dbc.Col([
                    html.H6("Volatility (Annualized)", className="text-muted"),
                    html.H5(f"{risk_metrics['volatility']:.1%}", className="text-info")
                ], width=3),
            ], className="mb-4"),
            
            # Additional metrics row
            dbc.Row([
                dbc.Col([
                    html.H6("Sharpe Ratio", className="text-muted"),
                    html.H5(f"{risk_metrics['sharpe_ratio']:.2f}", 
                            className="text-success" if risk_metrics['sharpe_ratio'] > 1 else "text-warning")
                ], width=3),
                dbc.Col([
                    html.H6("Max Drawdown", className="text-muted"),
                    html.H5(f"{risk_metrics['max_drawdown']:.1%}", className="text-danger")
                ], width=3),
                dbc.Col([
                    html.H6("SPY Correlation", className="text-muted"),
                    html.H5(f"{risk_metrics['correlation_spy']:.2f}", className="text-info")
                ], width=3),
                dbc.Col([
                    html.H6("10-Day VaR (95%)", className="text-muted"),
                    html.H5(f"${risk_metrics['var_10d']:,.2f}", className="text-danger")
                ], width=3),
            ], className="mb-4"),
            
            # Charts row
            dbc.Row([
                dbc.Col([
                    dcc.Graph(
                        figure=create_var_timeline_chart(),
                        config={'displayModeBar': False}
                    )
                ], width=6),
                dbc.Col([
                    dcc.Graph(
                        figure=create_sector_exposure_chart(),
                        config={'displayModeBar': False}
                    )
                ], width=6),
            ], className="mb-4"),
            
            # Second charts row
            dbc.Row([
                dbc.Col([
                    dcc.Graph(
                        figure=create_correlation_heatmap(),
                        config={'displayModeBar': False}
                    )
                ], width=6),
                dbc.Col([
                    html.H6("Options Greeks", className="mb-3"),
                    dash_table.DataTable(
                        data=greeks_df.to_dict('records') if not greeks_df.empty else [],
                        columns=[
                            {"name": col, "id": col, "type": "numeric", "format": {"specifier": ".2f"}}
                            if col != "Symbol" else {"name": col, "id": col, "type": "text"}
                            for col in greeks_df.columns
                        ] if not greeks_df.empty else [],
                        style_cell={
                            'backgroundColor': 'rgba(0,0,0,0)',
                            'color': 'white',
                            'textAlign': 'center',
                            'border': '1px solid #444',
                            'fontSize': '11px',
                            'fontFamily': 'monospace'
                        },
                        style_header={
                            'backgroundColor': '#2c3e50',
                            'fontWeight': 'bold',
                            'color': 'white'
                        },
                        style_data_conditional=[
                            {
                                'if': {'column_id': 'Delta', 'filter_query': '{Delta} < 0'},
                                'color': '#dc3545',
                            },
                            {
                                'if': {'column_id': 'Delta', 'filter_query': '{Delta} > 0'},
                                'color': '#28a745',
                            },
                            {
                                'if': {'column_id': 'Theta'},
                                'color': '#ffc107',
                            }
                        ],
                        sort_action="native",
                        page_size=10,
                        style_table={'height': '300px', 'overflowY': 'auto'}
                    ) if not greeks_df.empty else html.Div("No options positions", className="text-muted")
                ], width=6),
            ])
        ])
    ], className="mb-4")
    
    return risk_card 