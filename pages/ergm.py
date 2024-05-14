# Description: This script is used to run an ERGM model in R and display the results in a Dash web application.
# Can print formula, coefficients and goodness-of-fit assessment. Coefficients are displayed in a table and a bar chart.
# Layout is styled with CSS.
# Now with dynamic attribute checklist generation based on the data.

import os

import dash
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
import rpy2.robjects as robjects
from dash import dcc, html
from dash.dependencies import Input, Output, State
from rpy2.robjects import pandas2ri

# Set R_HOME
# os.environ['R_HOME'] = 'C:\\Program Files\\R\\R-4.3.3'
# # Set R_LIBS
# os.environ['R_LIBS'] = 'C:\\Program Files\\R\\R-4.3.3\\library'

dash.register_page(
    __name__,
    path='/ergm',
    name='ERGM Model',
    title='StatNet33 - ERGM Model',
    order=3
)

# Read, extract, and generate the options for the attribute checklist
attr_data = pd.read_csv("pages/data/network_data.csv")
attr_names = attr_data.columns.tolist()[2:]
def generate_attr_options(attr_names):
    options = []
    for attr_name in attr_names:
        if attr_data[attr_name].dtype == 'object':
            options.extend([
                {'label': f'{attr_name} (nodefactor)', 'value': f'nodefactor("{attr_name.lower()}")'},
                {'label': f'{attr_name} (nodematch)', 'value': f'nodematch("{attr_name.lower()}")'},
                {'label': f'{attr_name} (nodemix)', 'value': f'nodemix("{attr_name.lower()}")'}
            ])
        else:
            options.append({'label': f'{attr_name} (nodecov)', 'value': f'nodecov("{attr_name.lower()}")'})
    return options

# Define the app layout
def layout():
    return html.Div([
    html.Div(style={'display': 'flex', 'justifyContent': 'center'}, children=[
            html.H1("ERGM Model Results")
        ]),
    html.Div([
        html.H3('Select ERGM Terms'),
        dcc.Checklist(
            id='term-checklist',
            options=[
                {'label': 'Edges', 'value': 'edges'},
                {'label': 'Triangles', 'value': 'triangles'},
                {'label': 'Mutual', 'value': 'mutual'},
                {'label': 'Transitive Triads', 'value': 'ttriple'},
                {'label': 'Cyclic Triads', 'value': 'ctriple'},
                {'label': 'Intransitive Triads', 'value': 'intransitive'},
                {'label': 'Isolates', 'value': 'isolates'},
            ],
            value=['edges'], style={'marginBottom': '10px'}
        ),
        html.Div([
            html.Label('In-degree Terms'),
            dcc.Dropdown(
                id='indegree-dropdown',
                options=[{'label': f'In-degree({i})', 'value': f'idegree({i})'} for i in range(50)],
                value=[],
                multi=True
            )
        ]),
        html.Div([
            html.Label('Out-degree Terms'),
            dcc.Dropdown(
                id='outdegree-dropdown',
                options=[{'label': f'Out-degree({i})', 'value': f'odegree({i})'} for i in range(50)],
                value=[],
                multi=True
            )
        ]),
        
        html.H3('Select Node Attributes'),
        dcc.Checklist(
            id='attr-checklist',
            options=generate_attr_options(attr_names),
            value=[]
        ),

        html.Div(id='warning-message', style={'marginTop': '10px'}),

        html.Div([
            html.H3('Additional ERGM Terms'),
            dcc.Textarea(
                id='additional-terms',
                placeholder='Enter additional ERGM terms, separated by commas, e.g., m2star, absdiff("age")',
                style={'width': '100%', 'height': '80px'}
            )
        ]),
        
        html.Button('Run ERGM', id='run-button', n_clicks=0, style={'marginTop': '10px'}),
        html.Div([
        html.H3('ERGM Term Descriptions'),
        dcc.Dropdown(
            id='term-description-dropdown',
            options=[
                {'label': 'Edges', 'value': 'edges'},
                {'label': 'Triangles', 'value': 'triangles'},
                {'label': 'Mutual', 'value': 'mutual'},
                {'label': 'Transitive Triads (ttriple)', 'value': 'ttriple'},
                {'label': 'Cyclic Triads (ctriple)', 'value': 'ctriple'},
                {'label': 'Intransitive Triads (intransitive)', 'value': 'intransitive'},
                {'label': 'Isolates', 'value': 'isolates'},
                {'label': 'In-degree', 'value': 'idegree'},
                {'label': 'Out-degree', 'value': 'odegree'},
                {'label': 'Nodecov', 'value': 'nodecov'},
                {'label': 'Nodefactor', 'value': 'nodefactor'},
                {'label': 'Nodematch', 'value': 'nodematch'},
                {'label': 'Nodemix', 'value': 'nodemix'}
            ],
            placeholder='Select an ERGM term for description'
        ),
        html.Div(id='term-description-output', style={'marginTop': '10px', 'marginBottom': '20px'})
    ], style={'width': '300px', 'float': 'left', 'marginRight': '20px', 'marginTop': '10px'})
    
    ], style={'width': '300px', 'float': 'left', 'marginRight': '20px'}),
    
    html.Div(id='output-container', children=[
    html.Div(
        html.P('''    ERGM (Exponential Random Graph Models) are a class of statistical models used to analyze and understand the structure and formation of social networks. When you fit an ERGM to a network, the model estimates the parameters that best explain the observed network structure based on the specified network configurations or terms included in the model. On this page, you can:
    1. Select various ERGM terms to include in the model, such as edges, triangles, mutual ties, and node attributes.
    2. Specify the degree distribution for both incoming and outgoing ties in directed networks.
    3. Choose node attributes to incorporate into the model, including numerical (nodecov) and categorical (nodefactor) attributes, as well as homophily (nodematch) and heterophily (nodemix) effects.
    4. Enter additional ERGM terms in the text box to include in the model formula.
    5. Run the ERGM model on their network data and view the model results, including the model formula, coefficient estimates, and goodness-of-fit assessments.
    6. Access descriptions and explanations of the different ERGM terms to help interpret the model results and understand the underlying network processes.''',
        id='description-text', style={'fontSize': '18px', 'marginBottom': '20px', 'whiteSpace': 'pre-wrap'}
        ),
        style={
            'border': '1px solid #ccc',
            'borderRadius': '5px',
            'padding': '10px',
            'backgroundColor': '#f9f9f9',
            'width': '80%',
            'margin': '0 auto',
            'color': '#333',
        }
    )
], style={'marginTop': '30px', 'overflow': 'auto'}),

], style={'maxWidth': '1200px', 'margin': '0 auto', 'padding': '20px'})

@dash.callback(Output('warning-message', 'children'),
              [Input('attr-checklist', 'value')])
def update_warning_message(selected_attrs):
    has_nodemix = any('nodemix' in attr for attr in selected_attrs)
    has_nodefactor = any('nodefactor' in attr for attr in selected_attrs)
    has_nodematch = any('nodematch' in attr for attr in selected_attrs)

    if has_nodemix and (has_nodefactor or has_nodematch):
        return html.Div([
            html.I(className="fas fa-exclamation-triangle", style={'marginRight': '5px', 'color': '#FFC107'}),
            "⚠️ Warning: Selecting nodemix with either nodefactor or nodematch of the same attribute can cause linear dependence and model identifiability issues. If you suspect that nodes with different attribute values have a higher probability of forming ties, consider using nodemix with two different attributes."
        ], className="alert alert-warning", style={'fontSize': '14px'})
    else:
        return None

# Callback function to update the descriptions based on the selected terms
@dash.callback(
    Output('term-description-output', 'children'),
    [Input('term-description-dropdown', 'value')]
)
def update_term_description(selected_term):
    if selected_term == 'edges':
        return dbc.Alert([
            html.Strong('Edges: '),
            '''Baseline probability of an edge (tie) forming between any two nodes, irrespective of node attributes or other structural properties.
            You would want to always include this term as it forms the basis of modelling the network.'''
        ], color='info')
    elif selected_term == 'triangles':
        return dbc.Alert([
            html.Strong('Triangles: '),
            '''Tendency for triangles to form in the network, i.e., three nodes that are all connected to each other.'''
        ], color='info')
    elif selected_term == 'mutual':
        return dbc.Alert([
            html.Strong('Mutual: '),
            '''Tendency for reciprocated ties in the network, i.e., ties that go both ways between two nodes.
            You would want to include this term if you suspect that reciprocated ties are more likely to form than non-reciprocated ties.'''
        ], color='info')
    elif selected_term == 'ttriple':
        return dbc.Alert([
            html.Strong('Transitive Triads: '),
            '''Tendency for transitive triads to form in the network, i.e., three nodes where two are connected to a third node.
            For example, node A has a tie to node B, and node B has a tie to node C, then node A also has a tie to node C.'''
        ], color='info')
    elif selected_term == 'ctriple':
        return dbc.Alert([
            html.Strong('Cyclic Triads: '),
            '''Tendency for cyclic triads to form in the network, i.e., three nodes where each node is connected to the next node.
            For example, a circular pattern of ties among three nodes (A -> B -> C -> A)'''
        ], color='info')
    elif selected_term == 'intransitive':
        return dbc.Alert([
            html.Strong('Intransitive Triads: '),
            '''Tendency for intransitive triads to form in the network, i.e., three nodes where two are connected to a third node, but not to each other.
            For example, node A has a tie to node B, and node B has a tie to node C, but node A does not have a tie to node C.'''
        ], color='info')
    elif selected_term == 'isolates':
        return dbc.Alert([
            html.Strong('Isolates: '),
            '''Tendency for nodes to have no ties.
            You would want to include this term if you suspect that nodes with no ties are more likely to form than nodes with ties.'''
        ], color='info')
    elif selected_term == 'idegree':
        return dbc.Alert([
            html.Strong('In-degree: '),
            '''Tendency for nodes to have a specific number of incoming ties. 
            For example, idegree(1) captures the number of nodes with an in-degree of 1 (i.e., nodes receiving exactly one incoming tie).
            You would want to include this term if you suspect that the number of incoming ties to a node has an effect on the probability of edge formation.'''
        ], color='info')
    elif selected_term == 'odegree':
        return dbc.Alert([
            html.Strong('Out-degree: '),
            '''Tendency for nodes to have a specific number of outgoing ties. 
            For example, odegree(1) captures the number of nodes with an out-degree of 1 (i.e., nodes sending exactly one outgoing tie).
            You would want to include this term if you suspect that the number of outgoing ties from a node has an effect on the probability of edge formation.'''
        ], color='info')
    elif selected_term == 'nodecov':
        return dbc.Alert([
            html.Strong('Nodecov: '),
            '''Effect of a numerical node attribute on tie formation. 
            For example, nodecov("age") captures the effect of node age on the probability of edge formation.'''
        ], color='info')
    elif selected_term == 'nodefactor':
        return dbc.Alert([
            html.Strong('Nodefactor: '),
            '''Effect of a categorical node attribute on the probability of edge formation.
            This term can be used to answer questions such as "Do nodes of a certain type have a higher probability of forming ties?".'''
        ], color='info')
    elif selected_term == 'nodematch':
        return dbc.Alert([
            html.Strong('Nodematch: '),
            '''Effect of homophily, i.e., the tendency for nodes with the same attribute value to form ties.
            This term can be used to answer questions such as "Do nodes with the same attribute value have a higher probability of forming ties?".'''
        ], color='info')
    elif selected_term == 'nodemix':
        return dbc.Alert([
            html.Strong('Nodemix: '),
            '''Effect of heterophily, i.e., the tendency for nodes with different attribute values to form ties. Best used with categorical attribute.
            This term can be used to answer questions such as "Do nodes with different attribute values have a higher probability of forming ties?".'''        ], color='info')
    else:
        return ''
    

# Function to generate explanations for each coefficient
def generate_coefficient_explanations(coef_df):
    # Generate explanations for each coefficient
    detailed_explanation_list = []
    for index, row in coef_df.iterrows():
        term = row['Term']
        estimate = row['Estimate']
        error = row['Std. Error']
        z_value = row['Z-value']
        attr_name = term.split('.')[-1] if '.' in term else term
        sign = 'positive' if estimate > 0 else 'negative'

        # Skip coefficients with NaN estimates
        if error == 0:
            continue

        explanation = ""

        # Handle edge cases
        if term == 'edges':
            explanation = (f"The {sign} estimation value of {estimate:.4f} for edges indicates a {'higher' if sign == 'positive' else 'lower'} likelihood of additional ties forming "
                           f"as the number of edges in the network increases. "
                           f"This finding is {'statistically significant' if abs(z_value) > 1.96 else 'not statistically significant'}, "
                           f"with a Z-value of {z_value:.2f}.")

        # Handle node covariates
        elif 'nodecov' in term:
            explanation =(f"The {sign} coefficient ({estimate:.4f}) with a Z-value of {z_value:.2f} suggests that '{attr_name}' is "
                          f"{'statistically significant' if abs(z_value) > 1.96 else 'not statistically significant associated with the degree. '} "
                          f"Specially, for every unit increase in '{attr_name}', the log odds of having an additional tie increase by ({estimate:.4f}), when "
                          f"holding everything else constant.")
            
        elif 'nodefactor' in term:
            explanation = (f"Individuals with attribute '{attr_name}' are {'more' if sign == 'positive' else 'less'} likely "
                           f"to form connections, with an estimate of {estimate:.4f}. "
                           f"This effect is {'statistically significant' if abs(z_value) > 1.96 else 'not statistically significant'}, "
                           f"with a Z-value of {z_value:.2f}.")
                    # Handle node factors and node matches, which have similar explanations
        elif 'nodematch' in term:
            explanation = (f"Individuals with attribute '{attr_name}' are {'more' if sign == 'positive' else 'less'} likely "
                           f"to form connections with each other, with an estimate of {estimate:.4f}. "
                           f"This effect is {'statistically significant' if abs(z_value) > 1.96 else 'not statistically significant'}, "
                           f"with a Z-value of {z_value:.2f}.")
        elif 'mix' in term:
            # Split attributes for nodemix terms if applicable
            attrs = term.split('.')
            if len(attrs) > 1:
                explanation = (f"The interaction between '{attrs[1]}' and '{attrs[2]}' has a {sign} effect on the likelihood of forming connections, with an estimate of {estimate:.4f}. "
                               f"This indicates that different groups based on '{attrs[1]}' and '{attrs[2]}' interact {'more frequently' if sign == 'positive' else 'less frequently'} in forming ties. "
                               f"This effect is {'statistically significant' if abs(z_value) > 1.96 else 'not statistically significant'}, "
                               f"with a Z-value of {z_value:.2f}.")

        # Append the detailed explanation to the list
        detailed_explanation_list.append(html.Li(f"'{term}': {explanation}"))

    return html.Ul(detailed_explanation_list)

# Function to generate explanations for each GOF measure
def generate_gof_explanations(gof_data, term_names):
    explanations = []
    for i, term in enumerate(term_names):
        obs = round(gof_data['obs.model'][i], 2)
        mean = round(gof_data['summary.model'][i, 2], 2)
        min_val = round(gof_data['summary.model'][i, 1], 2)
        max_val = round(gof_data['summary.model'][i, 3], 2)
        mc_p_value = round(gof_data['pval.model'][i, 4], 2)

         # Skip terms where observed values are zero
        if obs == 0:
            continue

        explanation = f"For the term '{term}', the observed value is {obs}, with an expected simulation mean of {mean} and a range of {min_val} to {max_val}. "
        # Adjust explanation based on the Monte Carlo p-value
        if mc_p_value >= 0.05:
            explanation += f"This suggests the model fits the observed data well, as the Monte Carlo p-value of {mc_p_value} indicates a statistically insignificant difference."
        else:
            explanation += f"This suggests a potential model fit issue, as the Monte Carlo p-value of {mc_p_value} indicates a statistically significant difference."

        # explanation += " Generally, p-values closer to 0.5 indicate a better fit, with values near 0 or 1 highlighting more significant discrepancies."

        explanations.append(html.Li(explanation))

    return html.Ul(explanations)

# Callback function to run the R script and update the output
@dash.callback(Output('output-container', 'children'),
              [Input('run-button', 'n_clicks')],
              [State('term-checklist', 'value'),
               State('indegree-dropdown', 'value'),
               State('outdegree-dropdown', 'value'),
               State('attr-checklist', 'value'),
               State('additional-terms', 'value')])
def run_ergm(n_clicks, selected_terms, selected_indegree_terms, selected_outdegree_terms, selected_attrs, additional_terms):
    if n_clicks == 0:
        return dash.no_update
    else:
        try:
            # Construct the formula string
            formula_components = selected_terms + selected_indegree_terms + selected_outdegree_terms + selected_attrs
            
            # Include additional terms from the textbox
            if additional_terms:
                additional_terms_list = [term.strip() for term in additional_terms.split(',')]
                formula_components.extend(additional_terms_list)
            
            if formula_components:
                formula_str = ' + '.join(formula_components)
            else:
                # Set an empty formula string if no terms or attributes are selected
                formula_str = ''
            
            # Save the formula string to a file
            with open("dump/formula.txt", "w") as file:
                file.write(formula_str)
            
            print("Formula string saved to file:", formula_str)
            
            with robjects.conversion.localconverter(robjects.default_converter + pandas2ri.converter):
                # Execute the R script
                robjects.r.source("pages/ergm_script2.R")
                
                # Load the results from the RDS file
                results = robjects.r.readRDS("dump/ergm_results.rds")

                # Extract relevant information from the results
                model_formula = str(results['model_formula'])
                model_coefficients = np.array(results['model_coefficients'])
                term_names = list(results['term_names'])
                model_gof = results['model_gof']

                # gof_explanations
                if 'summary.model' in model_gof:
                    gof_explanations = generate_gof_explanations(model_gof, term_names)

                # Convert model coefficients to a DataFrame
                coef_df = pd.DataFrame(model_coefficients, columns=['Estimate', 'Std. Error', 'MCMC%', 'Z-value', 'Pr(>|z|)'])
                coef_df.insert(0, 'Term', term_names)

                # Create the coefficient table
                coef_table = html.Div([
                    html.Table([
                        html.Thead(html.Tr([html.Th(col, style={'padding': '10px', 'backgroundColor': '#f2f2f2', 'fontWeight': 'bold', 'border': '1px solid #ddd', 'textAlign': 'left'}) for col in coef_df.columns])),
                        html.Tbody([
                            html.Tr([
                                html.Td(coef_df.iloc[i][col], style={'padding': '10px', 'border': '1px solid #ddd', 'textAlign': 'left'}) for col in coef_df.columns
                            ], style={'backgroundColor': '#f9f9f9' if i % 2 == 0 else 'white'}) for i in range(len(coef_df))
                        ])
                    ], style={'width': '100%', 'borderCollapse': 'collapse', 'border': '1px solid #ddd'})
                ], style={'overflowX': 'auto'})

                # Generate explanations for each coefficient
                coefficient_explanations = generate_coefficient_explanations(coef_df)

                # Create tables for each GOF measure
                gof_tables = []
                
            #     # In-degree GOF table
            # if 'summary.ideg' in model_gof:
            #     gof_tables.append(html.Div([
            #         html.H3('Goodness-of-fit for in-degree'),
            #         html.Table([
            #             html.Thead(html.Tr([html.Th(col) for col in ['', 'obs', 'min', 'mean', 'max', 'MC p-value']])),
            #             html.Tbody([
            #                 html.Tr([
            #                     html.Td('idegree' + str(i)),
            #                     html.Td(round(model_gof['summary.ideg'][i, 0], 2)),
            #                     html.Td(round(model_gof['summary.ideg'][i, 1], 2)),
            #                     html.Td(round(model_gof['summary.ideg'][i, 2], 2)),
            #                     html.Td(round(model_gof['summary.ideg'][i, 3], 2)),
            #                     html.Td(round(model_gof['summary.ideg'][i, 4], 2))
            #                 ]) for i in range(model_gof['summary.ideg'].shape[0])
            #             ])
            #         ])
            #     ]))

            # # Out-degree GOF table
            # if 'summary.odeg' in model_gof:
            #     gof_tables.append(html.Div([
            #         html.H3('Goodness-of-fit for out-degree'),
            #         html.Table([
            #             html.Thead(html.Tr([html.Th(col) for col in ['', 'obs', 'min', 'mean', 'max', 'MC p-value']])),
            #             html.Tbody([
            #                 html.Tr([
            #                     html.Td('odegree' + str(i)),
            #                     html.Td(round(model_gof['summary.odeg'][i, 0], 2)),
            #                     html.Td(round(model_gof['summary.odeg'][i, 1], 2)),
            #                     html.Td(round(model_gof['summary.odeg'][i, 2], 2)),
            #                     html.Td(round(model_gof['summary.odeg'][i, 3], 2)),
            #                     html.Td(round(model_gof['summary.odeg'][i, 4], 2))
            #                 ]) for i in range(model_gof['summary.odeg'].shape[0])
            #             ])
            #         ])
            #     ]))

            # # Edgewise shared partner GOF table
            # if 'summary.espart' in model_gof:
            #     gof_tables.append(html.Div([
            #         html.H3('Goodness-of-fit for edgewise shared partner'),
            #         html.Table([
            #             html.Thead(html.Tr([html.Th(col) for col in ['', 'obs', 'min', 'mean', 'max', 'MC p-value']])),
            #             html.Tbody([
            #                 html.Tr([
            #                     html.Td('esp.OTP' + str(i)),
            #                     html.Td(round(model_gof['summary.espart'][i, 0], 2)),
            #                     html.Td(round(model_gof['summary.espart'][i, 1], 2)),
            #                     html.Td(round(model_gof['summary.espart'][i, 2], 2)),
            #                     html.Td(round(model_gof['summary.espart'][i, 3], 2)),
            #                     html.Td(round(model_gof['summary.espart'][i, 4], 2))
            #                 ]) for i in range(model_gof['summary.espart'].shape[0])
            #             ])
            #         ])
            #     ]))

            # # Minimum geodesic distance GOF table
            # if 'summary.dist' in model_gof:
            #     gof_tables.append(html.Div([
            #         html.H3('Goodness-of-fit for minimum geodesic distance'),
            #         html.Table([
            #             html.Thead(html.Tr([html.Th(col) for col in ['', 'obs', 'min', 'mean', 'max', 'MC p-value']])),
            #             html.Tbody([
            #                 html.Tr([
            #                     html.Td(str(i+1)),
            #                     html.Td(round(model_gof['summary.dist'][i, 0], 2)),
            #                     html.Td(round(model_gof['summary.dist'][i, 1], 2)),
            #                     html.Td(round(model_gof['summary.dist'][i, 2], 2)),
            #                     html.Td(round(model_gof['summary.dist'][i, 3], 2)),
            #                     html.Td(round(model_gof['summary.dist'][i, 4], 2))
            #                 ]) for i in range(model_gof['summary.dist'].shape[0]-1)
            #             ] + [
            #                 html.Tr([
            #                     html.Td('Inf'),
            #                     html.Td(round(model_gof['summary.dist'][-1, 0], 2)),
            #                     html.Td(round(model_gof['summary.dist'][-1, 1], 2)),
            #                     html.Td(round(model_gof['summary.dist'][-1, 2], 2)),
            #                     html.Td(round(model_gof['summary.dist'][-1, 3], 2)),
            #                     html.Td(round(model_gof['summary.dist'][-1, 4], 2))
            #                 ])
            #             ])
            #         ])
            #     ]))

            # Model statistics GOF table
            if 'summary.model' in model_gof:
                gof_tables.append(html.Div([
                    html.H3('Goodness-of-fit for model statistics'),
                    html.Table([
                        html.Thead(html.Tr([html.Th(col) for col in ['Statistic', 'obs', 'min', 'mean', 'max', 'MC p-value']])),
                        html.Tbody([
                            html.Tr([
                                html.Td(term),
                                html.Td(round(model_gof['obs.model'][i], 2)),
                                html.Td(round(model_gof['summary.model'][i, 1], 2)),
                                html.Td(round(model_gof['summary.model'][i, 2], 2)),
                                html.Td(round(model_gof['summary.model'][i, 3], 2)),
                                html.Td(round(model_gof['pval.model'][i, 4], 2))
                            ]) for i, term in enumerate(term_names)
                        ])
                    ])
                ]))

                # Create the graph with term names on the x-axis
                graph = dcc.Graph(
                    figure={
                        'data': [{'x': coef_df['Term'], 'y': coef_df['Estimate'], 'type': 'bar'}],
                        'layout': {
                            'title': 'Coefficient Estimates',
                            'xaxis': {
                                'title': 'Model Statistic',
                                'tickangle': -30,  # Rotate x-axis labels for better readability
                                'automargin': True  # Automatically adjust margins to accommodate labels
                            },
                            'yaxis': {
                                'title': 'Estimate',
                                'automargin': True  # Automatically adjust margins to accommodate labels
                            },
                            'hovermode': 'closest',
                            'margin': {'b': 120}  # Increase bottom margin to make space for x-axis labels
                        }
                    },
                    style={'width': '100%', 'height': 'calc(500px + 20px * {})'.format(len(coef_df))},
                    responsive=True
                )

                # Return the results as HTML with CSS styles
                return html.Div([
                    html.H2('ERGM Model Formula', style={'fontSize': '20px', 'marginBottom': '10px'}),
                    html.Pre(model_formula, style={'backgroundColor': '#f5f5f5', 'padding': '10px', 'borderRadius': '5px'}),
                    html.H2('ERGM Model Coefficients', style={'fontSize': '20px', 'marginBottom': '10px', 'marginTop': '30px'}),
                    coef_table,
                    html.H3('Coefficient Explanations', style={'fontSize': '20px', 'marginBottom': '10px', 'marginTop': '30px'}),
                    coefficient_explanations,
                    graph,
                    html.Div(gof_tables),
                    html.H3('Goodness-of-Fit Explanations', style={'fontSize': '20px', 'marginBottom': '10px', 'marginTop': '30px'}),
                    gof_explanations
                ])
        except robjects.rinterface.embedded.RRuntimeError as e:
            error_message = str(e)
            if "Illegal value of coef passed to simulate functions" in error_message:
                return html.Div([
                    html.H3("Error: Illegal Coefficient Values", className="text-danger"),
                    html.P("The ERGM model encountered illegal coefficient values during the simulation process."),
                    html.P("Suggestions:"),
                    html.Ul([
                        html.Li("Check your network data to ensure that there are observations for all the combinations of the selected terms."),
                        html.Li("Simplify the model by removing or combining problematic terms that have non-varying statistics or are involved in linear combinations."),
                        html.Li("Increase the sample size or collect more diverse data to ensure sufficient variation in the observed statistics for all attribute combinations."),
                        html.Li("Consider using a different model specification or a simpler model with fewer terms to avoid nonidentifiability and improve model convergence.")
                    ]),
                    html.P("If the issue persists, please consult with a statistician or a subject matter expert for further assistance.")
                ], className="alert alert-danger")
            else:
                # Handle other types of errors
                return html.Div([
                    html.H3("Error Occurred", className="text-danger"),
                    html.P(f"An error occurred while running the ERGM model: {error_message}"),
                    html.P("Please check your model specification and input data.")
                ], className="alert alert-danger")