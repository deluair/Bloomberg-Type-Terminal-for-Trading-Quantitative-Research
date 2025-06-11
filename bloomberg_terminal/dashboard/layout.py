"""
Defines the layout of the Dash application.
"""
from dash import html, dcc
import dash_bootstrap_components as dbc
from .components.market_overview import get_layout as market_overview_layout
from .components.market_overview_enhanced import get_layout as enhanced_market_layout
from .components.portfolio_view import get_layout as portfolio_layout
from .components.risk_management import get_layout as risk_layout
from .components.trade_blotter import get_layout as trade_blotter_layout
from .components.news_feed import get_layout as news_feed_layout
from .components.advanced_charts import get_layout as advanced_charts_layout
from .components.options_analytics import get_layout as options_layout
from .components.algo_trading import get_layout as algo_trading_layout
from .components.esg_alt_data import get_layout as esg_layout
from .components.quant_research import get_layout as quant_layout
from .components.navbar import get_navbar

# Enhanced layout with comprehensive Bloomberg-style components
main_layout = html.Div([
    get_navbar(),
    dbc.Container([
        # Anchor for top of page
        html.Div(id="top"),
        
        # Row 1: Enhanced Market Overview
        html.Div([
            html.A(id="market-overview"),
            dbc.Row([
                dbc.Col(enhanced_market_layout(), width=12, className="mt-4")
            ])
        ]),
        
        # Row 2: Portfolio and Risk Management (side by side)
        html.Div([
            html.A(id="portfolio"),
            html.A(id="risk-management"),
            dbc.Row([
                dbc.Col(portfolio_layout(), width=6, className="mt-4"),
                dbc.Col(risk_layout(), width=6, className="mt-4")
            ])
        ]),
        
        # Row 3: Advanced Charts (full width)
        html.Div([
            html.A(id="charts"),
            dbc.Row([
                dbc.Col(advanced_charts_layout(), width=12, className="mt-4")
            ])
        ]),
        
        # Row 4: Trade Blotter (full width)
        html.Div([
            html.A(id="trading"),
            dbc.Row([
                dbc.Col(trade_blotter_layout(), width=12, className="mt-4")
            ])
        ]),
        
                # Row 5: Options Analytics (full width)
        html.Div([
            html.A(id="options"),
            dbc.Row([
                dbc.Col(options_layout(), width=12, className="mt-4")
            ])
        ]),
        
        # Row 6: Algorithmic Trading (full width)
        html.Div([
            html.A(id="algo-trading"),
            dbc.Row([
                dbc.Col(algo_trading_layout(), width=12, className="mt-4")
            ])
        ]),
        
        # Row 7: ESG & Alternative Data (full width)
        html.Div([
            html.A(id="esg"),
            dbc.Row([
                dbc.Col(esg_layout(), width=12, className="mt-4")
            ])
        ]),
        
        # Row 8: Quantitative Research (full width)
        html.Div([
            html.A(id="quant"),
            dbc.Row([
                dbc.Col(quant_layout(), width=12, className="mt-4")
            ])
        ]),
        
        # Row 9: News Feed and Market Intelligence (full width)
        html.Div([
            html.A(id="news"),
            dbc.Row([
                dbc.Col(news_feed_layout(), width=12, className="mt-4")
            ])
        ]),
        
        # Footer to help identify end of page
        html.Div([
            html.Hr(),
            html.P("End of Bloomberg Terminal Dashboard", 
                   className="text-center text-muted mb-5",
                   style={'fontSize': '12px'})
        ])

    ], fluid=True, className="pt-4")  # Added padding-top to container
])

def create_layout(app):
    app.layout = main_layout
    return app.layout
