"""News feed component for the dashboard."""
import dash_bootstrap_components as dbc
from dash import html, dcc
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta
import random


def generate_news_data():
    """Generate sample news data for demonstration."""
    news_templates = [
        ("BREAKING: Fed announces {rate} basis point rate {action}", ["25", "50", "75"], ["cut", "hike"]),
        ("{company} reports Q{quarter} earnings {beat_miss} expectations", ["Apple", "Microsoft", "Amazon", "Tesla"], ["3", "4", "1", "2"], ["beat", "miss"]),
        ("Oil prices {direction} {percent}% on {event}", ["surge", "fall"], ["2.5", "3.2", "1.8", "4.1"], ["OPEC news", "geopolitical tensions", "inventory data"]),
        ("{index} {direction} {percent}% in {session} trading", ["S&P 500", "Nasdaq", "Dow Jones"], ["rises", "falls"], ["1.2", "0.8", "2.1"], ["early", "late", "mid-day"]),
        ("Crypto market sees {percent}% {direction} as Bitcoin {action}", ["5.2", "3.8", "7.1"], ["rally", "selloff"], ["breaks resistance", "hits support", "consolidates"]),
        ("Tech stocks {direction} on {news}", ["rally", "decline"], ["AI breakthrough", "regulatory concerns", "earnings optimism"]),
        ("Treasury yields {direction} to {yield}% amid {factor}", ["rise", "fall"], ["4.2", "4.5", "3.8"], ["inflation data", "Fed speculation", "safe haven demand"]),
        ("{sector} sector leads market {direction} with {percent}% gain", ["Energy", "Technology", "Healthcare", "Financial"], ["higher", "lower"], ["2.3", "1.7", "3.1"]),
    ]
    
    sentiments = ["Positive", "Negative", "Neutral"]
    sources = ["Bloomberg", "Reuters", "CNBC", "MarketWatch", "Financial Times", "Wall Street Journal"]
    
    news_items = []
    
    for i in range(25):  # Generate 25 news items
        template, *options = random.choice(news_templates)
        
        # Fill in template with random options - using safe formatting
        try:
            if len(options) == 1:
                headline = template.format(random.choice(options[0]))
            elif len(options) == 2:
                headline = template.format(random.choice(options[0]), random.choice(options[1]))
            elif len(options) == 3:
                headline = template.format(random.choice(options[0]), random.choice(options[1]), random.choice(options[2]))
            elif len(options) == 4:
                headline = template.format(random.choice(options[0]), random.choice(options[1]), 
                                         random.choice(options[2]), random.choice(options[3]))
            else:
                # For templates with named placeholders, use dict format
                format_dict = {}
                if "{rate}" in template:
                    format_dict["rate"] = random.choice(["25", "50", "75"])
                if "{action}" in template:
                    format_dict["action"] = random.choice(["cut", "hike"])
                if "{company}" in template:
                    format_dict["company"] = random.choice(["Apple", "Microsoft", "Amazon", "Tesla"])
                if "{quarter}" in template:
                    format_dict["quarter"] = random.choice(["1", "2", "3", "4"])
                if "{beat_miss}" in template:
                    format_dict["beat_miss"] = random.choice(["beat", "miss"])
                if "{direction}" in template:
                    format_dict["direction"] = random.choice(["surge", "fall", "rally", "decline", "rises", "falls", "higher", "lower"])
                if "{percent}" in template:
                    format_dict["percent"] = random.choice(["1.2", "2.5", "3.2", "1.8", "4.1"])
                if "{event}" in template:
                    format_dict["event"] = random.choice(["OPEC news", "geopolitical tensions", "inventory data"])
                if "{index}" in template:
                    format_dict["index"] = random.choice(["S&P 500", "Nasdaq", "Dow Jones"])
                if "{session}" in template:
                    format_dict["session"] = random.choice(["early", "late", "mid-day"])
                if "{news}" in template:
                    format_dict["news"] = random.choice(["AI breakthrough", "regulatory concerns", "earnings optimism"])
                if "{yield}" in template:
                    format_dict["yield"] = random.choice(["4.2", "4.5", "3.8"])
                if "{factor}" in template:
                    format_dict["factor"] = random.choice(["inflation data", "Fed speculation", "safe haven demand"])
                if "{sector}" in template:
                    format_dict["sector"] = random.choice(["Energy", "Technology", "Healthcare", "Financial"])
                
                headline = template.format(**format_dict)
        except (KeyError, IndexError):
            # Fallback to simple news templates
            headline = random.choice([
                "Market volatility continues amid economic uncertainty",
                "Tech stocks show mixed performance in today's session",
                "Federal Reserve policy decision awaited by markets",
                "Energy sector leads market gains",
                "Healthcare stocks under pressure",
                "Financial sector sees increased activity"
            ])
        
        timestamp = datetime.now() - timedelta(
            hours=random.randint(0, 48),
            minutes=random.randint(0, 59)
        )
        
        news_items.append({
            'headline': headline,
            'source': random.choice(sources),
            'timestamp': timestamp,
            'time_str': timestamp.strftime('%m/%d %H:%M'),
            'sentiment': random.choice(sentiments),
            'relevance': random.uniform(0.3, 1.0)
        })
    
    # Sort by timestamp (most recent first)
    news_items.sort(key=lambda x: x['timestamp'], reverse=True)
    
    return news_items


def generate_economic_indicators():
    """Generate sample economic indicator data."""
    indicators = [
        {'name': 'GDP Growth (QoQ)', 'value': '2.1%', 'previous': '1.8%', 'forecast': '2.0%', 'impact': 'Medium'},
        {'name': 'Unemployment Rate', 'value': '3.8%', 'previous': '3.9%', 'forecast': '3.8%', 'impact': 'High'},
        {'name': 'Core CPI (YoY)', 'value': '3.2%', 'previous': '3.3%', 'forecast': '3.1%', 'impact': 'High'},
        {'name': 'Fed Funds Rate', 'value': '5.25%', 'previous': '5.00%', 'forecast': '5.25%', 'impact': 'Very High'},
        {'name': 'Consumer Confidence', 'value': '108.2', 'previous': '106.8', 'forecast': '107.5', 'impact': 'Medium'},
        {'name': 'Manufacturing PMI', 'value': '52.4', 'previous': '51.8', 'forecast': '52.0', 'impact': 'Medium'},
        {'name': 'Non-Farm Payrolls', 'value': '215K', 'previous': '201K', 'forecast': '200K', 'impact': 'High'},
        {'name': 'Retail Sales (MoM)', 'value': '0.4%', 'previous': '0.2%', 'forecast': '0.3%', 'impact': 'Medium'},
    ]
    
    return indicators


def create_sentiment_gauge():
    """Create a gauge chart showing market sentiment."""
    try:
        # Generate a sentiment score between -100 and 100
        sentiment_score = random.uniform(-30, 70)  # Slightly bullish bias for demo
        
        fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = sentiment_score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Market Sentiment"},
        delta = {'reference': 0},
        gauge = {
            'axis': {'range': [-100, 100]},
            'bar': {'color': "lightblue"},
            'steps': [
                {'range': [-100, -50], 'color': "red"},
                {'range': [-50, 0], 'color': "orange"},
                {'range': [0, 50], 'color': "lightgreen"},
                {'range': [50, 100], 'color': "green"}
            ],
            'threshold': {
                'line': {'color': "white", 'width': 4},
                'thickness': 0.75,
                'value': sentiment_score
            }
        }
    ))
    
        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=250,
            font={'color': "white", 'size': 12}
        )
        
        return fig
        
    except Exception as e:
        print(f"Error creating sentiment gauge: {e}")
        # Return simple fallback chart
        fig = go.Figure()
        fig.add_annotation(
            text="Market Sentiment<br>Data Unavailable",
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            showarrow=False,
            font=dict(size=14, color="white")
        )
        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=250
        )
        return fig


def create_news_timeline():
    """Create a timeline showing news impact throughout the day."""
    try:
        # Generate sample news impact data
        hours = range(0, 24)
        impact_scores = [random.uniform(-5, 5) for _ in hours]
        
        colors = ['red' if x < 0 else 'green' for x in impact_scores]
        
        fig = go.Figure(data=[
            go.Bar(
                x=list(hours),
                y=impact_scores,
                marker_color=colors,
                text=[f"{x:+.1f}" for x in impact_scores],
                textposition='outside'
            )
        ])
        
        fig.update_layout(
            title="News Impact Throughout Day",
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=250,
            yaxis_title="Impact Score",
            xaxis_title="Hour (24H)",
            showlegend=False
        )
        
        return fig
        
    except Exception as e:
        print(f"Error creating news timeline: {e}")
        # Return simple fallback chart
        fig = go.Figure()
        fig.add_annotation(
            text="News Timeline<br>Data Unavailable",
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            showarrow=False,
            font=dict(size=14, color="white")
        )
        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=250,
            title="News Impact Throughout Day"
        )
        return fig


def get_layout():
    """Return the layout for the news feed."""
    
    # Generate sample data
    news_items = generate_news_data()
    econ_indicators = generate_economic_indicators()
    
    # Calculate news sentiment distribution
    sentiment_counts = {'Positive': 0, 'Negative': 0, 'Neutral': 0}
    for item in news_items:
        sentiment_counts[item['sentiment']] += 1
    
    news_feed_card = dbc.Card([
        dbc.CardHeader(html.H5("News Feed & Market Intelligence")),
        dbc.CardBody([
            # Summary metrics row
            dbc.Row([
                dbc.Col([
                    html.H6("Breaking News", className="text-muted"),
                    html.H4(f"{len([n for n in news_items[:5]])}", className="text-danger")
                ], width=3),
                dbc.Col([
                    html.H6("Positive News", className="text-muted"),
                    html.H4(f"{sentiment_counts['Positive']}", className="text-success")
                ], width=3),
                dbc.Col([
                    html.H6("Negative News", className="text-muted"),
                    html.H4(f"{sentiment_counts['Negative']}", className="text-danger")
                ], width=3),
                dbc.Col([
                    html.H6("Neutral News", className="text-muted"),
                    html.H4(f"{sentiment_counts['Neutral']}", className="text-info")
                ], width=3),
            ], className="mb-4"),
            
            # Charts row
            dbc.Row([
                dbc.Col([
                    dcc.Graph(
                        figure=create_sentiment_gauge(),
                        config={'displayModeBar': False}
                    )
                ], width=6),
                dbc.Col([
                    dcc.Graph(
                        figure=create_news_timeline(),
                        config={'displayModeBar': False}
                    )
                ], width=6),
            ], className="mb-4"),
            
            # Main content row
            dbc.Row([
                dbc.Col([
                    html.H6("Latest Market News", className="mb-3"),
                    html.Div([
                        dbc.Card([
                            dbc.CardBody([
                                html.P(item['headline'], className="mb-1", 
                                      style={'fontSize': '14px', 'fontWeight': 'bold'}),
                                html.Small([
                                    html.Span(f"{item['source']} • {item['time_str']} • ", 
                                             className="text-muted"),
                                    html.Span(item['sentiment'], 
                                             className=f"text-{'success' if item['sentiment'] == 'Positive' else 'danger' if item['sentiment'] == 'Negative' else 'info'}")
                                ])
                            ])
                        ], className="mb-2", 
                           style={'backgroundColor': 'rgba(0,0,0,0.3)', 'border': '1px solid #444'})
                        for item in news_items[:10]  # Show latest 10 items
                    ], style={'height': '400px', 'overflowY': 'auto'})
                ], width=6),
                dbc.Col([
                    html.H6("Economic Indicators", className="mb-3"),
                    html.Div([
                        dbc.Card([
                            dbc.CardBody([
                                dbc.Row([
                                    dbc.Col([
                                        html.Strong(indicator['name'], style={'fontSize': '12px'}),
                                        html.Br(),
                                        html.Span(f"Current: {indicator['value']}", className="text-primary", 
                                                 style={'fontSize': '11px'})
                                    ], width=6),
                                    dbc.Col([
                                        html.Span(f"Prev: {indicator['previous']}", className="text-muted", 
                                                 style={'fontSize': '10px'}),
                                        html.Br(),
                                        html.Span(f"Forecast: {indicator['forecast']}", className="text-muted", 
                                                 style={'fontSize': '10px'})
                                    ], width=4),
                                    dbc.Col([
                                        dbc.Badge(
                                            indicator['impact'], 
                                            color="danger" if indicator['impact'] == "Very High" 
                                                  else "warning" if indicator['impact'] == "High"
                                                  else "info",
                                            className="ms-1"
                                        )
                                    ], width=2)
                                ])
                            ], className="py-2")
                        ], className="mb-2", 
                           style={'backgroundColor': 'rgba(0,0,0,0.3)', 'border': '1px solid #444'})
                        for indicator in econ_indicators
                    ], style={'height': '400px', 'overflowY': 'auto'})
                ], width=6),
            ])
        ])
    ], className="mb-4")
    
    return news_feed_card 