"""
Initializes the Dash application.
"""
import dash
import dash_bootstrap_components as dbc

# Initialize the Dash app
# Using Bootstrap for styling. For more themes, visit https://bootswatch.com/
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])  # Dark theme (Cyborg) = "Bloomberg-Style Terminal"
app.title = "Bloomberg-Style Terminal"

# For multi-page apps, ensure server is explicitly defined
server = app.server

# Configuration for Dash
app.config.suppress_callback_exceptions = True
