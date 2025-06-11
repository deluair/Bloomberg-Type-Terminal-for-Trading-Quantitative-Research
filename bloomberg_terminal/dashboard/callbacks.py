"""
Houses all the callbacks for the Dash application.
"""

from datetime import datetime
import random
from collections import deque

from dash import dcc, html, callback_context
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go

from .app import app
from .components.market_overview import price_history, MAX_POINTS, get_real_market_data, _real_data_cache
from .components.advanced_charts import create_candlestick_chart, create_heatmap_correlation, create_volatility_surface


@app.callback(
    [
        Output("price-ticker", "children"),
        Output("price-chart", "figure"),
    ],
    [Input("price-interval", "n_intervals")],
)
def update_price(n: int):
    """Update price ticker and chart with real Yahoo Finance data."""
    symbol = "AAPL"  # Default symbol
    
    # Get real market data
    market_data = get_real_market_data(symbol)
    
    if market_data and market_data['price_history'] and len(market_data['price_history']) > 0:
        # Update price history with real data
        global price_history
        price_history.clear()
        price_history.extend(market_data['price_history'])
        
        # Format ticker text with real data
        ticker_text = f"${market_data['current_price']:.2f} @ {market_data['timestamp'].strftime('%H:%M:%S')} UTC"
        
        # Build figure with real price data
        fig = go.Figure()
        
        # Create x-axis with proper time indices
        x_values = list(range(len(price_history)))
        
        # Add price line
        fig.add_trace(go.Scatter(
            x=x_values,
            y=list(price_history), 
            mode="lines", 
            name=f"{symbol} Price",
            line=dict(color='#00d4aa', width=2),
            hovertemplate='Price: $%{y:.2f}<extra></extra>'
        ))
        
        # Add some styling for a professional look
        fig.update_layout(
            template="plotly_dark",
            margin=dict(l=20, r=20, t=30, b=20),
            height=300,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            title=f"{symbol} - Last {len(price_history)} Data Points",
            yaxis=dict(
                title="Price ($)",
                gridcolor='rgba(128,128,128,0.2)'
            ),
            xaxis=dict(
                title="Time Points",
                gridcolor='rgba(128,128,128,0.2)'
            ),
            showlegend=False
        )
        
        return ticker_text, fig
    
    else:
        # Fallback: Generate sample data when Yahoo Finance is unavailable
        if not price_history or len(price_history) == 0:
            # Initialize with sample data
            import random
            base_price = 198.50  # AAPL approximate price
            for i in range(50):
                if i == 0:
                    price_history.append(base_price)
                else:
                    # Small random walk
                    change = random.uniform(-0.5, 0.5)
                    new_price = max(0.01, price_history[-1] + change)
                    price_history.append(new_price)
        
        current_price = price_history[-1] if price_history else 198.50
        ticker_text = f"${current_price:.2f} @ {datetime.utcnow().strftime('%H:%M:%S')} UTC (Demo Data)"
        
        fig = go.Figure()
        
        # Create x-axis with proper time indices
        x_values = list(range(len(price_history)))
        
        # Add price line with demo data
        fig.add_trace(go.Scatter(
            x=x_values,
            y=list(price_history), 
            mode="lines", 
            name=f"{symbol} Price (Demo)",
            line=dict(color='#ffa500', width=2),  # Orange for demo data
            hovertemplate='Price: $%{y:.2f}<extra></extra>'
        ))
        
        fig.update_layout(
            template="plotly_dark",
            margin=dict(l=20, r=20, t=30, b=20),
            height=300,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            title=f"{symbol} - Demo Data ({len(price_history)} points)",
            yaxis=dict(
                title="Price ($)",
                gridcolor='rgba(128,128,128,0.2)'
            ),
            xaxis=dict(
                title="Time Points",
                gridcolor='rgba(128,128,128,0.2)'
            ),
            showlegend=False
        )
        
        return ticker_text, fig


@app.callback(
    Output("blotter-content", "children"),
    [Input("blotter-tabs", "active_tab")]
)
def update_blotter_content(active_tab):
    """Update the trade blotter content based on selected tab."""
    from .components.trade_blotter import generate_trade_history, generate_pending_orders
    from dash import dash_table
    
    if active_tab == "trades":
        trades_df = generate_trade_history()
        return html.Div([
            html.H6("Recent Trades (Last 50)", className="mt-3 mb-3"),
            dash_table.DataTable(
                data=trades_df.drop('Timestamp', axis=1).to_dict('records'),
                columns=[
                    {"name": col, "id": col, "type": "text"}
                    for col in trades_df.columns if col != 'Timestamp'
                ],
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
                        'if': {'filter_query': '{Side} = BUY'},
                        'backgroundColor': 'rgba(40, 167, 69, 0.2)',
                    },
                    {
                        'if': {'filter_query': '{Side} = SELL'},
                        'backgroundColor': 'rgba(220, 53, 69, 0.2)',
                    },
                    {
                        'if': {'filter_query': '{Status} = FILLED'},
                        'color': '#28a745',
                    },
                    {
                        'if': {'filter_query': '{Status} = PARTIAL'},
                        'color': '#ffc107',
                    },
                    {
                        'if': {'filter_query': '{Status} = CANCELLED'},
                        'color': '#dc3545',
                    }
                ],
                sort_action="native",
                filter_action="native",
                page_size=20,
                style_table={'height': '400px', 'overflowY': 'auto'}
            )
        ])
    
    elif active_tab == "orders":
        orders_df = generate_pending_orders()
        return html.Div([
            html.H6("Pending Orders", className="mt-3 mb-3"),
            dash_table.DataTable(
                data=orders_df.drop('Timestamp', axis=1).to_dict('records'),
                columns=[
                    {"name": col, "id": col, "type": "text"}
                    for col in orders_df.columns if col != 'Timestamp'
                ],
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
                        'if': {'filter_query': '{Side} = BUY'},
                        'backgroundColor': 'rgba(40, 167, 69, 0.2)',
                    },
                    {
                        'if': {'filter_query': '{Side} = SELL'},
                        'backgroundColor': 'rgba(220, 53, 69, 0.2)',
                    },
                    {
                        'if': {'filter_query': '{Type} = LIMIT'},
                        'color': '#17a2b8',
                    },
                    {
                        'if': {'filter_query': '{Type} = STOP'},
                        'color': '#ffc107',
                    }
                ],
                sort_action="native",
                filter_action="native",
                page_size=15,
                style_table={'height': '400px', 'overflowY': 'auto'}
            )
        ])
    
    return html.Div("Select a tab to view content")


@app.callback(
    Output("chart-content", "children"),
    [Input("chart-tabs", "active_tab"), Input("symbol-selector", "value")]
)
def update_chart_content(active_tab, selected_symbol):
    """Update the chart content based on selected tab and symbol."""
    
    if active_tab == "price-chart":
        return dcc.Graph(
            id='advanced-chart',
            figure=create_candlestick_chart(selected_symbol),
            config={'displayModeBar': True}
        )
    elif active_tab == "correlation":
        return dcc.Graph(
            id='correlation-chart',
            figure=create_heatmap_correlation(),
            config={'displayModeBar': True}
        )
    elif active_tab == "volatility":
        return dcc.Graph(
            id='volatility-chart',
            figure=create_volatility_surface(),
            config={'displayModeBar': True}
        )
    
    return html.Div("Select a chart type to view")


# Real-time update callback for enhanced components
@app.callback(
    Output("price-store", "data"),
    [Input("price-interval", "n_intervals")],
    prevent_initial_call=True
)
def update_market_data_store(n):
    """Store updated market data for use across components."""
    symbol = "AAPL"
    market_data = get_real_market_data(symbol)
    
    if market_data:
        return {
            "symbol": symbol,
            "price": market_data['current_price'],
            "change": market_data['change'],
            "change_percent": market_data['change_percent'],
            "timestamp": market_data['timestamp'].isoformat(),
            "update_count": n
        }
    
    return {"timestamp": datetime.utcnow().isoformat(), "update_count": n}





# Callbacks for component updates will be added here as components are developed.
