"""Trade blotter component for the dashboard."""
import dash_bootstrap_components as dbc
from dash import html, dcc, dash_table
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta
import random


def generate_trade_history():
    """Generate sample trade history for demonstration."""
    symbols = ["AAPL", "MSFT", "GOOGL", "AMZN", "META", "TSLA", "NVDA", "JPM", "BAC", "SPY"]
    sides = ["BUY", "SELL"]
    
    trades = []
    
    # Generate trades for the last few days
    base_time = datetime.now()
    
    for i in range(50):  # Generate 50 sample trades
        trade_time = base_time - timedelta(
            days=random.randint(0, 5),
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59)
        )
        
        symbol = random.choice(symbols)
        side = random.choice(sides)
        quantity = random.randint(10, 1000)
        price = round(random.uniform(50, 500), 2)
        
        trades.append({
            'Time': trade_time.strftime('%m/%d %H:%M:%S'),
            'Symbol': symbol,
            'Side': side,
            'Quantity': quantity,
            'Price': f"${price:.2f}",
            'Value': f"${quantity * price:,.2f}",
            'Status': random.choice(['FILLED', 'FILLED', 'FILLED', 'PARTIAL', 'CANCELLED']),
            'Order ID': f"ORD{1000 + i}",
            'Timestamp': trade_time
        })
    
    # Sort by time (most recent first)
    trades.sort(key=lambda x: x['Timestamp'], reverse=True)
    
    return pd.DataFrame(trades)


def generate_pending_orders():
    """Generate sample pending orders."""
    symbols = ["AAPL", "MSFT", "GOOGL", "AMZN", "META"]
    order_types = ["LIMIT", "STOP", "STOP_LIMIT"]
    sides = ["BUY", "SELL"]
    
    orders = []
    
    for i in range(15):  # Generate 15 pending orders
        submit_time = datetime.now() - timedelta(
            hours=random.randint(0, 24),
            minutes=random.randint(0, 59)
        )
        
        symbol = random.choice(symbols)
        side = random.choice(sides)
        quantity = random.randint(10, 500)
        order_type = random.choice(order_types)
        
        if order_type == "LIMIT":
            price = round(random.uniform(50, 500), 2)
            orders.append({
                'Time': submit_time.strftime('%m/%d %H:%M:%S'),
                'Symbol': symbol,
                'Side': side,
                'Quantity': quantity,
                'Type': order_type,
                'Price': f"${price:.2f}",
                'Status': 'PENDING',
                'Order ID': f"ORD{2000 + i}",
                'Timestamp': submit_time
            })
        elif order_type == "STOP":
            stop_price = round(random.uniform(50, 500), 2)
            orders.append({
                'Time': submit_time.strftime('%m/%d %H:%M:%S'),
                'Symbol': symbol,
                'Side': side,
                'Quantity': quantity,
                'Type': order_type,
                'Price': f"STOP @ ${stop_price:.2f}",
                'Status': 'PENDING',
                'Order ID': f"ORD{2000 + i}",
                'Timestamp': submit_time
            })
    
    # Sort by time (most recent first)
    orders.sort(key=lambda x: x['Timestamp'], reverse=True)
    
    return pd.DataFrame(orders)


def create_trade_volume_chart():
    """Create a chart showing trade volume over time."""
    # Generate hourly trade volume for the last 24 hours
    hours = pd.date_range(end=datetime.now(), periods=24, freq='h')
    volumes = [random.randint(10000, 200000) for _ in range(24)]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=hours,
        y=volumes,
        name='Trade Volume',
        marker_color='lightblue'
    ))
    
    fig.update_layout(
        title="Trade Volume (Last 24 Hours)",
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=250,
        yaxis_title="Volume ($)",
        xaxis_title="Time",
        showlegend=False
    )
    
    return fig


def create_execution_quality_chart():
    """Create a chart showing execution quality metrics."""
    symbols = ["AAPL", "MSFT", "GOOGL", "AMZN", "META"]
    slippage = [random.uniform(-0.05, 0.15) for _ in symbols]  # Slippage in %
    
    colors = ['green' if x <= 0.05 else 'orange' if x <= 0.1 else 'red' for x in slippage]
    
    fig = go.Figure(data=[
        go.Bar(
            x=symbols,
            y=[s * 100 for s in slippage],  # Convert to basis points
            marker_color=colors,
            text=[f"{s:.3f}%" for s in slippage],
            textposition='outside'
        )
    ])
    
    fig.update_layout(
        title="Average Slippage by Symbol (Today)",
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=250,
        yaxis_title="Slippage (%)",
        xaxis_title="Symbol"
    )
    
    return fig


def get_layout():
    """Return the layout for the trade blotter."""
    
    # Generate sample data
    trades_df = generate_trade_history()
    orders_df = generate_pending_orders()
    
    # Calculate summary metrics
    total_trades_today = len([t for t in trades_df.to_dict('records') 
                             if (datetime.now() - datetime.strptime(t['Time'], '%m/%d %H:%M:%S')).days == 0])
    
    pending_orders_count = len(orders_df)
    
    # Calculate total volume today
    today_trades = [t for t in trades_df.to_dict('records') 
                   if (datetime.now() - datetime.strptime(t['Time'], '%m/%d %H:%M:%S')).days == 0]
    
    total_volume_today = sum([float(t['Value'].replace('$', '').replace(',', '')) 
                             for t in today_trades])
    
    trade_blotter_card = dbc.Card([
        dbc.CardHeader(html.H5("Trade Blotter & Order Management")),
        dbc.CardBody([
            # Summary metrics row
            dbc.Row([
                dbc.Col([
                    html.H6("Trades Today", className="text-muted"),
                    html.H4(f"{total_trades_today}", className="text-primary")
                ], width=3),
                dbc.Col([
                    html.H6("Pending Orders", className="text-muted"),
                    html.H4(f"{pending_orders_count}", className="text-warning")
                ], width=3),
                dbc.Col([
                    html.H6("Volume Today", className="text-muted"),
                    html.H4(f"${total_volume_today:,.0f}", className="text-info")
                ], width=3),
                dbc.Col([
                    html.H6("Avg Fill Rate", className="text-muted"),
                    html.H4("97.8%", className="text-success")
                ], width=3),
            ], className="mb-4"),
            
            # Charts row
            dbc.Row([
                dbc.Col([
                    dcc.Graph(
                        figure=create_trade_volume_chart(),
                        config={'displayModeBar': False}
                    )
                ], width=6),
                dbc.Col([
                    dcc.Graph(
                        figure=create_execution_quality_chart(),
                        config={'displayModeBar': False}
                    )
                ], width=6),
            ], className="mb-4"),
            
            # Tabs for trades and orders
            dbc.Tabs([
                dbc.Tab(label="Recent Trades", tab_id="trades"),
                dbc.Tab(label="Pending Orders", tab_id="orders"),
            ], id="blotter-tabs", active_tab="trades"),
            
            html.Div(id="blotter-content", children=[
                # Recent Trades Table
                html.Div([
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
                ], id="trades-table"),
                
                # Pending Orders Table (initially hidden)
                html.Div([
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
                ], id="orders-table", style={'display': 'none'})
            ])
        ])
    ], className="mb-4")
    
    return trade_blotter_card 