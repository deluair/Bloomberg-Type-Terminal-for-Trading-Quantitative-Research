"""Portfolio view component for the dashboard."""
import dash_bootstrap_components as dbc
from dash import html, dcc, dash_table
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from decimal import Decimal
from datetime import datetime
import random


def generate_sample_portfolio():
    """Generate sample portfolio data for demonstration."""
    symbols = ["AAPL", "MSFT", "GOOGL", "AMZN", "META", "TSLA", "NVDA", "JPM", "BAC", "SPY"]
    
    portfolio_data = []
    for symbol in symbols:
        if random.random() > 0.3:  # Some symbols might not have positions
            position = random.randint(-500, 1000)
            if position != 0:
                avg_price = round(random.uniform(50, 500), 2)
                current_price = round(avg_price * random.uniform(0.85, 1.15), 2)
                market_value = position * current_price
                cost_basis = position * avg_price
                pnl = market_value - cost_basis
                pnl_pct = (pnl / abs(cost_basis)) * 100 if cost_basis != 0 else 0
                
                portfolio_data.append({
                    'Symbol': symbol,
                    'Position': position,
                    'Avg Price': f"${avg_price:.2f}",
                    'Current Price': f"${current_price:.2f}",
                    'Market Value': f"${market_value:,.2f}",
                    'P&L': f"${pnl:,.2f}",
                    'P&L %': f"{pnl_pct:.2f}%",
                    'Raw P&L': pnl,  # For sorting/coloring
                })
    
    return pd.DataFrame(portfolio_data)


def create_portfolio_summary_chart():
    """Create a donut chart showing portfolio allocation."""
    try:
        df = generate_sample_portfolio()
        
        if df.empty:
            # Create empty chart with message
            fig = go.Figure()
            fig.add_annotation(
                text="No portfolio positions to display",
                xref="paper", yref="paper",
                x=0.5, y=0.5,
                showarrow=False,
                font=dict(size=14, color="white")
            )
            fig.update_layout(
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                height=300
            )
            return fig
        
        # Calculate absolute market values for allocation
        df['Abs_Value'] = df['Market Value'].str.replace('$', '').str.replace(',', '').astype(float).abs()
        
        fig = px.pie(
            df, 
            values='Abs_Value', 
            names='Symbol',
            title="Portfolio Allocation",
            hole=0.4
        )
        
        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=300,
            showlegend=True,
            legend=dict(
                orientation="v",
                yanchor="top",
                y=1,
                xanchor="left",
                x=1.01
            )
        )
        
        return fig
        
    except Exception as e:
        print(f"Error creating portfolio chart: {e}")
        # Return empty chart with error message
        fig = go.Figure()
        fig.add_annotation(
            text="Error loading portfolio data",
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            showarrow=False,
            font=dict(size=14, color="red")
        )
        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=300
        )
        return fig


def create_pnl_bar_chart():
    """Create a bar chart showing P&L by position."""
    try:
        df = generate_sample_portfolio()
        
        if df.empty:
            # Create empty chart with message
            fig = go.Figure()
            fig.add_annotation(
                text="No P&L data to display",
                xref="paper", yref="paper",
                x=0.5, y=0.5,
                showarrow=False,
                font=dict(size=14, color="white")
            )
            fig.update_layout(
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                height=300
            )
            return fig
        
        colors = ['green' if x >= 0 else 'red' for x in df['Raw P&L']]
        
        fig = go.Figure(data=[
            go.Bar(
                x=df['Symbol'],
                y=df['Raw P&L'],
                marker_color=colors,
                text=[f"${x:,.0f}" for x in df['Raw P&L']],
                textposition='outside'
            )
        ])
        
        fig.update_layout(
            title="P&L by Position",
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=300,
            yaxis_title="P&L ($)",
            xaxis_title="Symbol"
        )
        
        return fig
        
    except Exception as e:
        print(f"Error creating P&L chart: {e}")
        # Return empty chart with error message
        fig = go.Figure()
        fig.add_annotation(
            text="Error loading P&L data",
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            showarrow=False,
            font=dict(size=14, color="red")
        )
        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=300
        )
        return fig


def get_layout():
    """Return the layout for the portfolio view."""
    try:
        # Generate sample data
        df = generate_sample_portfolio()
        
        # Calculate summary metrics
        if not df.empty:
            total_market_value = sum([float(x.replace('$', '').replace(',', '')) for x in df['Market Value']])
            total_pnl = sum(df['Raw P&L'])
            total_pnl_pct = (total_pnl / (total_market_value - total_pnl)) * 100 if (total_market_value - total_pnl) != 0 else 0
        else:
            total_market_value = 0
            total_pnl = 0
            total_pnl_pct = 0
            
        # Style the data table
        styled_df = df.drop('Raw P&L', axis=1) if not df.empty else pd.DataFrame()
        
        portfolio_card = dbc.Card([
            dbc.CardHeader(html.H5("Portfolio & Positions")),
            dbc.CardBody([
                # Summary metrics row
                dbc.Row([
                    dbc.Col([
                        html.H6("Total Market Value", className="text-muted"),
                        html.H4(f"${total_market_value:,.2f}", className="text-primary")
                    ], width=3),
                    dbc.Col([
                        html.H6("Total P&L", className="text-muted"),
                        html.H4(
                            f"${total_pnl:,.2f}", 
                            className="text-success" if total_pnl >= 0 else "text-danger"
                        )
                    ], width=3),
                    dbc.Col([
                        html.H6("Total P&L %", className="text-muted"),
                        html.H4(
                            f"{total_pnl_pct:.2f}%", 
                            className="text-success" if total_pnl_pct >= 0 else "text-danger"
                        )
                    ], width=3),
                    dbc.Col([
                        html.H6("Positions", className="text-muted"),
                        html.H4(f"{len(df)}", className="text-info")
                    ], width=3),
                ], className="mb-4"),
                
                # Charts row
                dbc.Row([
                    dbc.Col([
                        dcc.Graph(
                            figure=create_portfolio_summary_chart(),
                            config={'displayModeBar': False}
                        )
                    ], width=6),
                    dbc.Col([
                        dcc.Graph(
                            figure=create_pnl_bar_chart(),
                            config={'displayModeBar': False}
                        )
                    ], width=6),
                ], className="mb-4"),
                
                # Positions table
                html.H6("Current Positions", className="mb-3"),
                dash_table.DataTable(
                    data=styled_df.to_dict('records') if not styled_df.empty else [],
                    columns=[
                        {"name": col, "id": col, "type": "text"}
                        for col in styled_df.columns
                    ] if not styled_df.empty else [],
                    style_cell={
                        'backgroundColor': 'rgba(0,0,0,0)',
                        'color': 'white',
                        'textAlign': 'center',
                        'border': '1px solid #444',
                        'fontSize': '12px',
                        'fontFamily': 'monospace'
                    },
                    style_header={
                        'backgroundColor': '#2c3e50',
                        'fontWeight': 'bold',
                        'color': 'white'
                    },
                    style_data_conditional=[
                        {
                            'if': {
                                'filter_query': '{Raw P&L} < 0',
                                'column_id': 'P&L'
                            },
                            'backgroundColor': 'rgba(220, 53, 69, 0.2)',
                            'color': '#dc3545',
                        },
                        {
                            'if': {
                                'filter_query': '{Raw P&L} > 0',
                                'column_id': 'P&L'
                            },
                            'backgroundColor': 'rgba(40, 167, 69, 0.2)',
                            'color': '#28a745',
                        }
                    ] if not styled_df.empty else [],
                    sort_action="native",
                    page_size=20,
                    style_table={'overflowX': 'auto'}
                )
            ])
        ], className="mb-4")
        
        return portfolio_card
        
    except Exception as e:
        print(f"Error creating portfolio layout: {e}")
        # Return minimal error card
        return dbc.Card([
            dbc.CardHeader(html.H5("Portfolio & Positions")),
            dbc.CardBody([
                html.Div([
                    html.H6("Error loading portfolio data", className="text-danger"),
                    html.P("Please refresh the page or check the data source.")
                ])
            ])
        ], className="mb-4") 