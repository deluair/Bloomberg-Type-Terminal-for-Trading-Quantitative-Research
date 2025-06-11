"""ESG and Alternative Data component for comprehensive ESG analysis and alternative data insights."""
import dash_bootstrap_components as dbc
from dash import html, dcc, dash_table
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random


def generate_esg_scores():
    """Generate ESG scores for major companies."""
    companies = [
        {'Symbol': 'AAPL', 'Company': 'Apple Inc.', 'E_Score': 85, 'S_Score': 92, 'G_Score': 88, 'ESG_Total': 88.3, 'ESG_Rating': 'A+', 'Carbon_Footprint': 'Low'},
        {'Symbol': 'MSFT', 'Company': 'Microsoft Corp.', 'E_Score': 90, 'S_Score': 89, 'G_Score': 91, 'ESG_Total': 90.0, 'ESG_Rating': 'A+', 'Carbon_Footprint': 'Very Low'},
        {'Symbol': 'GOOGL', 'Company': 'Alphabet Inc.', 'E_Score': 82, 'S_Score': 78, 'G_Score': 75, 'ESG_Total': 78.3, 'ESG_Rating': 'A', 'Carbon_Footprint': 'Low'},
        {'Symbol': 'AMZN', 'Company': 'Amazon.com Inc.', 'E_Score': 68, 'S_Score': 71, 'G_Score': 82, 'ESG_Total': 73.7, 'ESG_Rating': 'B+', 'Carbon_Footprint': 'High'},
        {'Symbol': 'TSLA', 'Company': 'Tesla Inc.', 'E_Score': 95, 'S_Score': 72, 'G_Score': 65, 'ESG_Total': 77.3, 'ESG_Rating': 'A-', 'Carbon_Footprint': 'Very Low'},
        {'Symbol': 'META', 'Company': 'Meta Platforms', 'E_Score': 71, 'S_Score': 58, 'G_Score': 68, 'ESG_Total': 65.7, 'ESG_Rating': 'B', 'Carbon_Footprint': 'Medium'},
        {'Symbol': 'NVDA', 'Company': 'NVIDIA Corp.', 'E_Score': 78, 'S_Score': 84, 'G_Score': 86, 'ESG_Total': 82.7, 'ESG_Rating': 'A', 'Carbon_Footprint': 'Medium'},
        {'Symbol': 'JPM', 'Company': 'JPMorgan Chase', 'E_Score': 62, 'S_Score': 76, 'G_Score': 88, 'ESG_Total': 75.3, 'ESG_Rating': 'B+', 'Carbon_Footprint': 'Medium'},
        {'Symbol': 'JNJ', 'Company': 'Johnson & Johnson', 'E_Score': 88, 'S_Score': 91, 'G_Score': 89, 'ESG_Total': 89.3, 'ESG_Rating': 'A+', 'Carbon_Footprint': 'Low'},
        {'Symbol': 'XOM', 'Company': 'Exxon Mobil', 'E_Score': 32, 'S_Score': 58, 'G_Score': 72, 'ESG_Total': 54.0, 'ESG_Rating': 'C', 'Carbon_Footprint': 'Very High'},
    ]
    
    return pd.DataFrame(companies)


def generate_sustainability_metrics():
    """Generate sustainability and climate-related metrics."""
    return {
        'carbon_emissions': {
            'scope_1': 125000,  # Direct emissions (tons CO2)
            'scope_2': 89000,   # Indirect emissions from energy
            'scope_3': 450000,  # Value chain emissions
            'total': 664000,
            'reduction_target': 0.5,  # 50% reduction by 2030
            'progress': 0.23  # 23% achieved
        },
        'renewable_energy': {
            'current_percentage': 72,
            'target_percentage': 100,
            'solar_capacity': 850,  # MW
            'wind_capacity': 1200,  # MW
            'hydro_capacity': 300   # MW
        },
        'water_management': {
            'consumption': 15.2,  # Million gallons
            'recycled_percentage': 68,
            'efficiency_improvement': 0.15  # 15% improvement YoY
        },
        'waste_management': {
            'total_waste': 45000,  # Tons
            'recycled_percentage': 84,
            'landfill_diversion': 0.92  # 92% diverted from landfill
        }
    }


def generate_alternative_data():
    """Generate alternative data metrics."""
    return {
        'satellite_data': {
            'parking_lots': {'AAPL': 85, 'AMZN': 92, 'TSLA': 78, 'WMT': 88},  # Occupancy %
            'oil_storage': {'XOM': 76, 'CVX': 82, 'BP': 74},  # Storage levels %
            'retail_traffic': {'TGT': 94, 'HD': 91, 'COST': 96}  # Foot traffic index
        },
        'social_sentiment': {
            'brand_mentions': {'AAPL': 15420, 'TSLA': 23890, 'META': 8760},
            'sentiment_score': {'AAPL': 0.72, 'TSLA': 0.68, 'META': 0.34},
            'engagement_rate': {'AAPL': 0.045, 'TSLA': 0.089, 'META': 0.023}
        },
        'supply_chain': {
            'shipping_volume': {'AMZN': 125, 'FDX': 98, 'UPS': 102},  # Index vs baseline
            'port_congestion': {'LAX': 7.2, 'LGB': 4.8, 'SFO': 3.1},  # Days delay
            'commodity_flows': {'Semiconductors': 89, 'Rare_Earths': 76, 'Lithium': 112}  # Supply index
        },
        'credit_card_spending': {
            'retail': {'YoY_Growth': 0.08, 'Category_Share': 0.32},
            'travel': {'YoY_Growth': 0.15, 'Category_Share': 0.18},
            'restaurants': {'YoY_Growth': 0.12, 'Category_Share': 0.24}
        }
    }


def create_esg_scores_chart():
    """Create ESG scores visualization."""
    df = generate_esg_scores()
    
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('ESG Total Scores', 'E-S-G Components', 'ESG Ratings', 'Carbon Footprint'),
        specs=[[{"type": "bar"}, {"type": "scatter"}],
               [{"type": "pie"}, {"type": "bar"}]]
    )
    
    # ESG Total Scores
    colors = ['green' if x >= 80 else 'orange' if x >= 70 else 'red' for x in df['ESG_Total']]
    fig.add_trace(
        go.Bar(x=df['Symbol'], y=df['ESG_Total'], marker_color=colors, name="ESG Total"),
        row=1, col=1
    )
    
    # E-S-G Component Scatter
    fig.add_trace(
        go.Scatter(x=df['E_Score'], y=df['S_Score'], mode='markers+text',
                  text=df['Symbol'], textposition="top center",
                  marker=dict(size=df['G_Score']/5, color=df['ESG_Total'], 
                            colorscale='RdYlGn', showscale=True),
                  name="E vs S (G=size)"),
        row=1, col=2
    )
    
    # ESG Rating Distribution
    rating_counts = df['ESG_Rating'].value_counts()
    fig.add_trace(
        go.Pie(labels=rating_counts.index, values=rating_counts.values, name="ESG Ratings"),
        row=2, col=1
    )
    
    # Carbon Footprint
    footprint_counts = df['Carbon_Footprint'].value_counts()
    footprint_colors = {'Very Low': 'green', 'Low': 'lightgreen', 'Medium': 'orange', 'High': 'red', 'Very High': 'darkred'}
    colors_fp = [footprint_colors.get(x, 'gray') for x in footprint_counts.index]
    fig.add_trace(
        go.Bar(x=footprint_counts.index, y=footprint_counts.values, 
               marker_color=colors_fp, name="Carbon Footprint"),
        row=2, col=2
    )
    
    fig.update_layout(
        title="ESG Scores & Sustainability Metrics",
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=600,
        showlegend=False
    )
    
    return fig


def create_sustainability_dashboard():
    """Create sustainability metrics dashboard."""
    metrics = generate_sustainability_metrics()
    
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Carbon Emissions by Scope', 'Renewable Energy Progress', 'Water & Waste Management', 'Emissions Reduction Progress'),
        specs=[[{"type": "pie"}, {"type": "bar"}],
               [{"type": "bar"}, {"type": "scatter"}]]
    )
    
    # Carbon emissions pie
    emissions = metrics['carbon_emissions']
    fig.add_trace(
        go.Pie(labels=['Scope 1', 'Scope 2', 'Scope 3'],
               values=[emissions['scope_1'], emissions['scope_2'], emissions['scope_3']],
               name="Emissions"),
        row=1, col=1
    )
    
    # Renewable energy
    renewable = metrics['renewable_energy']
    fig.add_trace(
        go.Bar(x=['Solar', 'Wind', 'Hydro'],
               y=[renewable['solar_capacity'], renewable['wind_capacity'], renewable['hydro_capacity']],
               marker_color=['gold', 'lightblue', 'blue'],
               name="Renewable Capacity (MW)"),
        row=1, col=2
    )
    
    # Water & Waste
    water = metrics['water_management']
    waste = metrics['waste_management']
    fig.add_trace(
        go.Bar(x=['Water Recycled %', 'Waste Recycled %', 'Landfill Diversion %'],
               y=[water['recycled_percentage'], waste['recycled_percentage'], waste['landfill_diversion']*100],
               marker_color=['lightblue', 'green', 'brown'],
               name="Sustainability %"),
        row=2, col=1
    )
    
    # Emissions reduction progress
    progress_years = list(range(2020, 2031))
    baseline = 100
    target_line = [baseline * (1 - emissions['reduction_target'] * (year - 2020) / 10) for year in progress_years]
    actual_line = [baseline * (1 - emissions['progress'] * (year - 2020) / 3) if year <= 2024 else None for year in progress_years]
    
    fig.add_trace(
        go.Scatter(x=progress_years, y=target_line, mode='lines', name='Target', line=dict(dash='dash')),
        row=2, col=2
    )
    fig.add_trace(
        go.Scatter(x=progress_years[:5], y=[x for x in actual_line if x is not None], 
                  mode='lines+markers', name='Actual', line=dict(color='green')),
        row=2, col=2
    )
    
    fig.update_layout(
        title="Corporate Sustainability Dashboard",
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=600,
        showlegend=False
    )
    
    return fig


def create_alternative_data_dashboard():
    """Create alternative data visualization."""
    alt_data = generate_alternative_data()
    
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Satellite Data - Parking Occupancy', 'Social Sentiment Analysis', 'Supply Chain Metrics', 'Credit Card Spending Trends'),
        specs=[[{"type": "bar"}, {"type": "scatter"}],
               [{"type": "bar"}, {"type": "bar"}]]
    )
    
    # Satellite data - parking lots
    parking_data = alt_data['satellite_data']['parking_lots']
    fig.add_trace(
        go.Bar(x=list(parking_data.keys()), y=list(parking_data.values()),
               marker_color='lightblue', name="Parking Occupancy %"),
        row=1, col=1
    )
    
    # Social sentiment
    sentiment_data = alt_data['social_sentiment']
    fig.add_trace(
        go.Scatter(x=list(sentiment_data['brand_mentions'].values()),
                  y=list(sentiment_data['sentiment_score'].values()),
                  mode='markers+text',
                  text=list(sentiment_data['brand_mentions'].keys()),
                  textposition="top center",
                  marker=dict(size=[x*1000 for x in sentiment_data['engagement_rate'].values()],
                            color=list(sentiment_data['sentiment_score'].values()),
                            colorscale='RdYlGn', showscale=True),
                  name="Sentiment vs Mentions"),
        row=1, col=2
    )
    
    # Supply chain
    supply_data = alt_data['supply_chain']['shipping_volume']
    fig.add_trace(
        go.Bar(x=list(supply_data.keys()), y=list(supply_data.values()),
               marker_color='orange', name="Shipping Volume Index"),
        row=2, col=1
    )
    
    # Credit card spending
    cc_data = alt_data['credit_card_spending']
    categories = list(cc_data.keys())
    growth_rates = [cc_data[cat]['YoY_Growth'] * 100 for cat in categories]
    fig.add_trace(
        go.Bar(x=categories, y=growth_rates,
               marker_color='green', name="YoY Growth %"),
        row=2, col=2
    )
    
    fig.update_layout(
        title="Alternative Data Intelligence Dashboard",
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=600,
        showlegend=False
    )
    
    return fig


def create_esg_investment_performance():
    """Create ESG investment strategy performance chart."""
    dates = pd.date_range(start=datetime.now() - timedelta(days=365), end=datetime.now(), freq='D')
    
    # Simulate performance data
    np.random.seed(42)
    esg_fund = [100]
    traditional_fund = [100]
    benchmark = [100]
    
    for i in range(1, len(dates)):
        esg_fund.append(esg_fund[-1] * (1 + np.random.normal(0.0008, 0.012)))
        traditional_fund.append(traditional_fund[-1] * (1 + np.random.normal(0.0006, 0.015)))
        benchmark.append(benchmark[-1] * (1 + np.random.normal(0.0007, 0.013)))
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=dates, y=esg_fund, mode='lines', name='ESG Fund',
        line=dict(color='green', width=2)
    ))
    fig.add_trace(go.Scatter(
        x=dates, y=traditional_fund, mode='lines', name='Traditional Fund',
        line=dict(color='blue', width=2)
    ))
    fig.add_trace(go.Scatter(
        x=dates, y=benchmark, mode='lines', name='S&P 500',
        line=dict(color='gray', width=2, dash='dash')
    ))
    
    fig.update_layout(
        title="ESG vs Traditional Investment Performance (1 Year)",
        xaxis_title="Date",
        yaxis_title="Normalized Performance",
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=400,
        legend=dict(x=0.02, y=0.98)
    )
    
    return fig


def get_layout():
    """Return the layout for ESG and alternative data."""
    
    esg_df = generate_esg_scores()
    alt_data = generate_alternative_data()
    
    # Calculate summary metrics
    avg_esg_score = esg_df['ESG_Total'].mean()
    high_esg_count = len(esg_df[esg_df['ESG_Total'] >= 80])
    low_carbon_count = len(esg_df[esg_df['Carbon_Footprint'].isin(['Very Low', 'Low'])])
    
    esg_card = dbc.Card([
        dbc.CardHeader(html.H5("ESG & Alternative Data Analytics")),
        dbc.CardBody([
            # Summary metrics row
            dbc.Row([
                dbc.Col([
                    html.H6("Average ESG Score", className="text-muted"),
                    html.H4(f"{avg_esg_score:.1f}", className="text-success")
                ], width=3),
                dbc.Col([
                    html.H6("High ESG Companies", className="text-muted"),
                    html.H4(f"{high_esg_count}/10", className="text-primary")
                ], width=3),
                dbc.Col([
                    html.H6("Low Carbon Companies", className="text-muted"),
                    html.H4(f"{low_carbon_count}/10", className="text-info")
                ], width=3),
                dbc.Col([
                    html.H6("ESG Data Coverage", className="text-muted"),
                    html.H4("98.5%", className="text-warning")
                ], width=3),
            ], className="mb-4"),
            
            # ESG Investment Strategies
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H6("ESG Momentum Strategy", className="text-success"),
                            html.P("YTD Return: +12.4%", className="mb-1"),
                            html.P("ESG Score Improvement: +8.2%", className="mb-0 small text-muted")
                        ])
                    ], className="text-center")
                ], width=3),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H6("Carbon Transition Fund", className="text-info"),
                            html.P("YTD Return: +15.8%", className="mb-1"),
                            html.P("Carbon Reduction: -32%", className="mb-0 small text-muted")
                        ])
                    ], className="text-center")
                ], width=3),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H6("Social Impact Portfolio", className="text-warning"),
                            html.P("YTD Return: +9.7%", className="mb-1"),
                            html.P("Social Score: 85+", className="mb-0 small text-muted")
                        ])
                    ], className="text-center")
                ], width=3),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H6("Governance Leaders", className="text-primary"),
                            html.P("YTD Return: +11.2%", className="mb-1"),
                            html.P("Governance Score: 90+", className="mb-0 small text-muted")
                        ])
                    ], className="text-center")
                ], width=3),
            ], className="mb-4"),
            
            # Charts tabs
            dbc.Tabs([
                dbc.Tab(label="ESG Scores", tab_id="esg-scores"),
                dbc.Tab(label="Sustainability", tab_id="sustainability"),
                dbc.Tab(label="Alternative Data", tab_id="alt-data"),
                dbc.Tab(label="ESG Performance", tab_id="esg-performance"),
            ], id="esg-tabs", active_tab="esg-scores"),
            
            html.Div(id="esg-content", children=[
                # Default ESG scores chart
                dcc.Graph(
                    figure=create_esg_scores_chart(),
                    config={'displayModeBar': True}
                )
            ], className="mt-3"),
            
            # ESG Companies Table
            html.H6("ESG Scores by Company", className="mt-4 mb-3"),
            dash_table.DataTable(
                data=esg_df.to_dict('records'),
                columns=[
                    {"name": "Symbol", "id": "Symbol"},
                    {"name": "Company", "id": "Company"},
                    {"name": "E Score", "id": "E_Score"},
                    {"name": "S Score", "id": "S_Score"},
                    {"name": "G Score", "id": "G_Score"},
                    {"name": "ESG Total", "id": "ESG_Total"},
                    {"name": "ESG Rating", "id": "ESG_Rating"},
                    {"name": "Carbon Footprint", "id": "Carbon_Footprint"},
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
                        'if': {'filter_query': '{ESG_Total} >= 85'},
                        'backgroundColor': 'rgba(40, 167, 69, 0.3)',
                    },
                    {
                        'if': {'filter_query': '{ESG_Total} >= 75 && {ESG_Total} < 85'},
                        'backgroundColor': 'rgba(255, 193, 7, 0.3)',
                    },
                    {
                        'if': {'filter_query': '{ESG_Total} < 65'},
                        'backgroundColor': 'rgba(220, 53, 69, 0.3)',
                    },
                    {
                        'if': {'filter_query': '{Carbon_Footprint} = "Very High"'},
                        'color': '#ff6b6b',
                    }
                ],
                sort_action="native",
                filter_action="native"
            ),
            
            # Alternative Data Insights
            html.Div([
                html.H6("Alternative Data Insights", className="mt-4 mb-3"),
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                html.H6("🛰️ Satellite Intelligence", className="text-info"),
                                html.P("Retail foot traffic up 8.5% WoW", className="mb-1"),
                                html.P("Oil storage at 76% capacity", className="mb-1"),
                                html.Small("Updated: 2 hours ago", className="text-muted")
                            ])
                        ])
                    ], width=3),
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                html.H6("📱 Social Sentiment", className="text-success"),
                                html.P("AAPL sentiment: 72% positive", className="mb-1"),
                                html.P("TSLA mentions surge +45%", className="mb-1"),
                                html.Small("Real-time monitoring", className="text-muted")
                            ])
                        ])
                    ], width=3),
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                html.H6("🚢 Supply Chain", className="text-warning"),
                                html.P("Port congestion easing", className="mb-1"),
                                html.P("Semiconductor supply +12%", className="mb-1"),
                                html.Small("Global tracking active", className="text-muted")
                            ])
                        ])
                    ], width=3),
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                html.H6("💳 Spending Data", className="text-primary"),
                                html.P("Travel spending +15% YoY", className="mb-1"),
                                html.P("Retail growth steady at 8%", className="mb-1"),
                                html.Small("Credit card analytics", className="text-muted")
                            ])
                        ])
                    ], width=3),
                ])
            ])
        ])
    ], className="mb-4")
    
    return esg_card 