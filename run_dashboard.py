"""
Main entry point to run the Dash dashboard application.
"""
from bloomberg_terminal.dashboard.app import app
from bloomberg_terminal.dashboard.layout import create_layout
# Import callbacks if they are defined in a separate module and need to be registered
# from bloomberg_terminal.dashboard import callbacks 

# Setup the layout
create_layout(app)

if __name__ == '__main__':
    # You can adjust host and port as needed
    # debug=True enables hot-reloading and error reporting in the browser
    app.run(debug=True, host='0.0.0.0', port=8050)
