import os

import dash
from dash import dcc, html
from flask import send_from_directory

from pages.viz import init_callbacks
from pages.viz import layout as viz_layout

external_stylesheets = ['assets/base.css', 'assets/fonts.css']

app = dash.Dash('Group 33', use_pages=True, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)
server = app.server 
# Define the directory where files will be stored and served
FILE_DIRECTORY = 'pages/data'
os.makedirs(FILE_DIRECTORY, exist_ok=True)  # Ensure directory exists

@server.route('/download/<path:filename>')
def download_file(filename):
    """Serve a file from the file system."""
    return send_from_directory(FILE_DIRECTORY, filename, as_attachment=True)

dash.register_page('visualization', layout=viz_layout, path='/visualization', name='Visualization', title='StatNet33 - Visualization', order=2)

app.layout = html.Div([
    html.Div(className='navbar', children=[
        html.H1('StatNet33', style={'color': 'white', 'margin': '0', 'padding': '15px', 'text-align': 'center'}),
        html.Div(style={'display': 'flex', 'justify-content': 'center'}, children=[
            dcc.Link(f"{page['name']}", href=page["relative_path"], style={'margin-right': '10px'})
            for page in dash.page_registry.values()
        ])
    ]),
    dash.page_container
])

# Initialize the callbacks for the visualization page
init_callbacks(app)

if __name__ == '__main__':
    app.run_server(debug=True, host='127.0.0.1', port=8050)
