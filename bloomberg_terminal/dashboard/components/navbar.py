"""Navigation bar component for dashboard."""
import dash_bootstrap_components as dbc
from dash import html, dcc


def get_navbar() -> dbc.Navbar:
    """Return a styled Navbar with navigation links."""
    return dbc.Navbar(
        dbc.Container([
            dbc.Row([
                dbc.Col([
                    dbc.NavbarBrand(
                        [
                            html.I(className="fas fa-chart-line me-2"),
                            "Bloomberg-Style Terminal"
                        ],
                        href="#top",
                        className="fw-bold"
                    )
                ], width="auto"),
                
                dbc.Col([
                    dbc.Nav([
                        dbc.NavItem(dbc.NavLink("Market Data", href="#market-overview", external_link=True)),
                        dbc.NavItem(dbc.NavLink("Portfolio", href="#portfolio", external_link=True)),
                        dbc.NavItem(dbc.NavLink("Risk", href="#risk-management", external_link=True)),
                        dbc.NavItem(dbc.NavLink("Charts", href="#charts", external_link=True)),
                        dbc.NavItem(dbc.NavLink("Trading", href="#trading", external_link=True)),
                        dbc.DropdownMenu([
                            dbc.DropdownMenuItem("Options Analytics", href="#options"),
                            dbc.DropdownMenuItem("Algorithmic Trading", href="#algo-trading"),
                            dbc.DropdownMenuItem("ESG & Alt Data", href="#esg"),
                            dbc.DropdownMenuItem("Quantitative Research", href="#quant"),
                            dbc.DropdownMenuItem(divider=True),
                            dbc.DropdownMenuItem("News Feed", href="#news"),
                        ], label="Advanced", nav=True),
                        dbc.DropdownMenu([
                            dbc.DropdownMenuItem("Settings", href="#settings"),
                            dbc.DropdownMenuItem("Help", href="#help"),
                            dbc.DropdownMenuItem("About", href="#about"),
                        ], label="More", nav=True)
                    ], navbar=True, className="ms-auto")
                ], width="auto")
            ], className="w-100", justify="between")
        ], fluid=True),
        color="primary",
        dark=True,
        sticky="top",
        className="shadow"
    )
