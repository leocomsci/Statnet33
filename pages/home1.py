
import base64
import io
import json
import os

import dash
import matplotlib
import networkx as nx

matplotlib.use('Agg')  # Use Agg backend

import json
import os

import matplotlib.pyplot as plt
import pandas as pd
from dash import Input, Output, State, callback, dash_table, dcc, html

dash.register_page(
    __name__,
    path='/',
    name='Home',
    title='StatNet33',
    order=0
)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


def layout():
    return html.Div([
        html.Div(style={'display': 'flex', 'justifyContent': 'center'}, children=[
            html.H1("CSV and JSON File Processor")
        ]),
        html.Div([
            html.Div([
                html.P("Welcome to the File Processing Tool. Upload your file according to the specified formats below. The tool will process your file and provide downloadable links for the output.", className="lead"),
            ], className="jumbotron mb-4"),
            html.Div([
                html.Div([
                    html.Div([
                        html.P("Please upload a CSV or JSON file and it must contain these following attributes:", className="card-text"),
                        html.Ul([
                            html.Li("ID: Unique identifier for each entry."),
                            html.Li("Name: The name of the individual."),
                            html.Li("Relationship: IDs of related individuals, separated by semicolons (;)."),
                        ]),
                        html.P("The output will include:"),
                        html.Ul([
                            html.Li("A data file containes nodes and its main attributes"),
                            html.Li("An edgelist file showing relationships, suitable for network analysis."),
                        ])
                    ], className="card-body"),
                ], className="card shadow-sm mb-4"),
            ]),
            html.Div([
                dcc.Upload(
                    id='upload-data',
                    children=html.Button('Select Files', id="upload-button", n_clicks=0, className="btn btn-primary mt-3 mb-3"),
                    multiple=False,
                    accept='.csv, .json'  # Accept CSV and JSON files
                ),
                html.Div(id='output-file-upload', className="mt-3"),
                html.Div(id='link-to-download', className="mt-3")
            ])
        ])

        
    ])

@callback(
    Output('output-file-upload', 'children'),
    Output('link-to-download', 'children'),
    Input('upload-data', 'contents'),
    State('upload-data', 'filename')
)
def update_output(contents, filename):
    if not contents:
        return (html.Div("No file uploaded."), html.Div())

    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)

    # Process CSV files
    if filename.endswith('.csv'):
        df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
    # Process JSON files
    elif filename.endswith('.json'):
        df = pd.DataFrame(json.loads(decoded.decode('utf-8')))
    else:
        return (html.Div("Unsupported file type."), html.Div())

    try:
        data_df, edgelist_df,message = process_dataframe(df)
        
        base_filename = filename.split('.')[0]
        data_filepath = os.path.join('pages/data', f'{base_filename}_data.csv')
        edgelist_filepath = os.path.join('pages/data', f'{base_filename}_edgelist.csv')
        
        data_df.to_csv(data_filepath, index=False)
        edgelist_df.to_csv(edgelist_filepath, index=False)

        return (html.Div(["Files processed and saved.", html.P(message)]),
                html.Div([
                    html.A("Download Data File", href=f'/download/{os.path.basename(data_filepath)}', className="btn btn-primary"),
                    html.A("Download Edgelist File", href=f'/download/{os.path.basename(edgelist_filepath)}', className="btn btn-secondary")
                ]))
    except Exception as e:
        return (html.Div(f"Error processing file: {str(e)}"), html.Div())

def process_dataframe(df):
    duplicates_before = df.duplicated(subset=['ID']).sum()
    df.drop_duplicates(subset=['ID'], keep='first', inplace=True)
    duplicates_after = df.duplicated(subset=['ID']).sum()
    null_ids_count = df['ID'].isnull().sum()
    df.dropna(subset=['ID'], inplace=True)
    null_other_count = df.drop(['ID', 'Relationship'], axis=1).isnull().any(axis=1).sum()

    data_df = df.drop('Relationship', axis=1)  # Drop the 'Relationship' column for the data file
    rows = []
    for index, row in df.iterrows():
        source_id = row['ID']
        if pd.notna(row['Relationship']):
            targets = str(row['Relationship']).split(';')
            for target in targets:
                rows.append({'Source': source_id, 'Target': int(target)})
    edgelist_df = pd.DataFrame(rows)

    messages = []
    if null_ids_count > 0:
        messages.append(f"Dropped {null_ids_count} row(s) with null 'ID'.")
    if duplicates_before > duplicates_after:
        messages.append(f"Dropped {duplicates_before - duplicates_after} duplicate row(s).")
    if null_other_count > 0:
        messages.append(f"{null_other_count} row(s) have null values in columns except 'ID' and 'Relationship'.")
    message_paragraphs = [html.P(msg) for msg in messages]

    return data_df, edgelist_df, message_paragraphs
