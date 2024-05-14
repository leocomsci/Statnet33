import base64
from io import BytesIO

import dash
import plotly.express as px
import rpy2.robjects as robjects
from dash import dcc, html
from dash.dependencies import Input, Output, State
from PIL import Image
from rpy2.robjects import pandas2ri

dash.register_page(
    __name__,
    path='/simulate',
    name='Model Simulation',
    title='StatNet33 - Model Simulation',
    order=4
)

# Define the layout of the app
def layout():
    return html.Div([
        html.Div(style={'display': 'flex', 'justifyContent': 'center'}, children=[
            html.H1('Model Simulation')
        ]),
        html.Div([
            html.Label('Number of Simulations'),
            dcc.Input(id='num-simulations', type='number', value=10, min=1, step=1),
            html.Button('Run Simulation', id='simulate-button', n_clicks=0),
            dcc.Dropdown(id='simulated-network-dropdown')
        ]),
        html.Div(id='observed-vs-simulated'),
        html.Div([
            html.Div([
                html.H3('Original Network'),
                dcc.Graph(id='original-network-plot', style={'height': '600px'}),
                html.Div(id='simulation-summary')
            ], style={'width': '50%', 'display': 'inline-block', 'vertical-align': 'top'}),
            html.Div([
                html.H3('Simulated Network'),
                dcc.Graph(id='individual-network-plot', style={'height': '600px'}),
                html.Div(id='individual-network-summary')
            ], style={'width': '50%', 'display': 'inline-block', 'vertical-align': 'top'})
        ])
    ])

# Callback to run the simulation
@dash.callback(
    [Output('observed-vs-simulated', 'children'),
     Output('original-network-plot', 'figure'),
     Output('simulation-summary', 'children'),
     Output('simulated-network-dropdown', 'options')],
    [Input('simulate-button', 'n_clicks')],
    [State('num-simulations', 'value')]
)
def run_simulation(n_clicks, num_simulations):
    if n_clicks == 0:
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update

    # Write the number of simulations to a text file
    with open('dump/num_simulations.txt', 'w') as file:
        file.write(str(num_simulations))

    with robjects.conversion.localconverter(robjects.default_converter + pandas2ri.converter):
        # Source the R script to run the simulation
        robjects.r.source("pages/simulate_model.R")
        
        # Read the simulated networks and summary from the RDS file
        simulated_data = robjects.r.readRDS('dump/simulated_networks.rds')
        summary_output = simulated_data["summary_output"]
        stats_df = robjects.r['as.data.frame'](simulated_data["stats_df"])
        
        # Get the base64-encoded original network plot from the R script
        base64_original_plot = robjects.r('base64_original_plot')[0]

    # Decode the base64-encoded original network plot
    original_img_data = base64.b64decode(base64_original_plot.split(',')[1])

    # Open the original network image using PIL
    original_img = Image.open(BytesIO(original_img_data))

    # Convert the original network image to RGB mode if needed
    if original_img.mode != "RGB":
        original_img = original_img.convert("RGB")

    # Create a figure with the original network plot image
    original_fig = px.imshow(original_img)

    # Customize the original figure layout
    original_fig.update_layout(
        height=600,
        xaxis=dict(showticklabels=False),
        yaxis=dict(showticklabels=False),
        margin=dict(l=0, r=0, t=50, b=0)
    )

    # Generate the dropdown options for simulated networks
    options = [{'label': f'Simulated Network {i}', 'value': i} for i in range(1, num_simulations + 1)]

    return [
        html.Div([
            html.H3('Observed vs Simulated Mean Statistics'),
            html.Table([
                html.Thead(
                    html.Tr([
                        html.Th('Statistic'),  # Column for row names
                        *[html.Th(col) for col in stats_df.columns]
                    ])
                ),
                html.Tbody([
                    html.Tr([
                        html.Td(stats_df.index[i]),  # Row name
                        *[html.Td(stats_df.iloc[i][col]) for col in stats_df.columns]
                    ])
                    for i in range(len(stats_df))
                ])
            ])
        ]),
        original_fig,
        html.Div([
            html.H3('Simulation Summary'),
            html.Pre('\n'.join(summary_output))
        ]),
        options
    ]

# Callback to update the individual network summary and plot
@dash.callback(
    [Output('individual-network-summary', 'children'),
     Output('individual-network-plot', 'figure')],
    [Input('simulated-network-dropdown', 'value')],
    prevent_initial_call=True
)
def update_individual_network(selected_network):
    if selected_network is None:
        return dash.no_update, dash.no_update
    
    with robjects.conversion.localconverter(robjects.default_converter + pandas2ri.converter):
        # Get the summary of the selected individual simulated network
        summary_output = robjects.r(f"capture.output(simulated_networks[[{selected_network}]])")
        
        # Write the number of simulations to a text file
        with open('dump/selected_network.txt', 'w') as file:
            file.write(str(selected_network))
        
        # Run the R script to generate the individual simulated network plot
        robjects.r.source("pages/plot_network.R")
        
        # Get the base64-encoded individual simulated network plot from the R script
        base64_simulated_plot = robjects.r('base64_plot')[0]
    
    # Decode the base64-encoded individual simulated network plot
    simulated_img_data = base64.b64decode(base64_simulated_plot.split(',')[1])
    
    # Open the individual simulated network image using PIL
    simulated_img = Image.open(BytesIO(simulated_img_data))
    
    # Convert the individual simulated network image to RGB mode if needed
    if simulated_img.mode != "RGB":
        simulated_img = simulated_img.convert("RGB")
    
    # Create a figure with the individual simulated network plot image
    simulated_fig = px.imshow(simulated_img)
    
    # Customize the simulated figure layout
    simulated_fig.update_layout(
        height=600,
        xaxis=dict(showticklabels=False),
        yaxis=dict(showticklabels=False),
        margin=dict(l=0, r=0, t=50, b=0)
    )
    
    return [
        html.Div([
            html.H3(f'Simulated Network {selected_network} Summary'),
            html.Pre('\n'.join(summary_output))
        ]),
        simulated_fig
    ]