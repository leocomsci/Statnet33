import base64
import io

import dash
import matplotlib

matplotlib.use('Agg')  # Use Agg backend
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
from dash import dcc, html
from dash.dependencies import Input, Output

dash.register_page(
    __name__,
    path='/general-metrics',
    name='General Metrics',
    title='StatNet33 - General Metrics',
    order=1
)

# Read CSV file containing edges and nodes data
edges_df = pd.read_csv("pages/data/network_edges.csv")
nodes_df = pd.read_csv("pages/data/network_data.csv")

#Create a graph from the edge list
G = nx.from_pandas_edgelist(edges_df, source="Source", target="Target")

# Compute graph metrics
density = nx.density(G)
avg_degree = sum(dict(G.degree()).values()) / len(G)
degree_distribution = dict(G.degree())
num_nodes = len(G.nodes)
num_edges = len(G.edges)
try:
    diameter = nx.diameter(G)
except nx.NetworkXError:
    diameter = "Graph is not connected."
try:
    avg_path_length = nx.average_shortest_path_length(G)
except nx.NetworkXError:
    avg_path_length = "Graph is not connected."
clustering_coefficient = nx.average_clustering(G)
avg_node_clustering = nx.clustering(G)
transitivity = nx.transitivity(G)
assortativity = nx.degree_assortativity_coefficient(G)

# Draw the graph and convert to base64 for displaying in Dash
buffer = io.BytesIO()
plt.figure(figsize=(8, 6))
nx.draw(G, with_labels=False, node_color='skyblue', node_size=100, edge_color='gray')
plt.savefig(buffer, format='png')
plt.close()
graph_image = base64.b64encode(buffer.getvalue()).decode('utf-8')

def layout():
    return html.Div([
        html.Div(style={'display': 'flex', 'justifyContent': 'center'}, children=[
            html.H1("Graph Metrics and Visualization Dashboard")
        ]),
        html.Div(style={'display': 'flex', 'flexDirection': 'row', 'flexWrap': 'wrap'}, children=[
            html.Div(style={'flex': '0 0 60%', 'maxWidth': '60%'}, children=[
                html.Img(src='data:image/png;base64,{}'.format(graph_image), style={'width': '100%'})
            ]),
            html.Div(style={'flex': '0 0 40%', 'maxWidth': '40%', 'height': '90vh', 'overflowY': 'auto'}, children=[
                html.Div([
                    html.H3("Density"),
                    html.P("Density quantifies the number of edges in the graph relative to the number of possible edges."),
                    html.Pre(id="density", children=str(density))
                ]),
                html.Div([
                    html.H3("Number of Nodes"),
                    html.P("Total number of nodes in the graph."),
                    html.Pre(id="num-nodes", children=str(num_nodes))
                ]),
                html.Div([
                    html.H3("Number of Edges"),
                    html.P("Total number of edges in the graph."),
                    html.Pre(id="num-edges", children=str(num_edges))
                ]),
                html.Div([
                    html.H3("Average Degree"),
                    html.P("Average degree of the nodes in the graph."),
                    html.Pre(id="average-degree", children=str(avg_degree))
                ]),
                html.Div([
                    html.H3("Degree Distribution"),
                    html.P("Distribution of degrees across all nodes in the graph."),
                    html.Pre(id="degree-distribution", children=str(degree_distribution))
                ]),
                html.Div([
                    html.H3("Network Diameter"),
                    html.P("Longest shortest path between any pair of nodes in the graph."),
                    html.Pre(id="network-diameter", children=str(diameter))
                ]),
                html.Div([
                    html.H3("Average Path Length"),
                    html.P("Average shortest path length between all pairs of nodes in the graph."),
                    html.Pre(id="average-path-length", children=str(avg_path_length))
                ]),
                html.Div([
                    html.H3("Global Clustering Coefficient"),
                    html.P("Average clustering coefficient over all nodes in the graph."),
                    html.Pre(id="clustering-coefficient", children=str(clustering_coefficient))
                ]),
                html.Div([
                    html.H3("Average Node Clustering Coefficients"),
                    html.P("Clustering coefficient for each node averaged over all nodes."),
                    html.Pre(id="avg-node-clustering", children=str(avg_node_clustering))
                ]),
                html.Div([
                    html.H3("Transitivity"),
                    html.P("Transitivity quantifies the tendency for nodes to cluster together."),
                    html.Pre(id="transitivity", children=str(transitivity))
                ]),
                html.Div([
                    html.H3("Assortativity Coefficient"),
                    html.P("Assortativity coefficient measures the similarity of connections in the graph with respect to the node degrees."),
                    html.Pre(id="assortativity", children=str(assortativity))
                ])
            ])
        ])
    ])


# Define the callback to switch pages
@dash.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")]
)
def display_page(pathname):
    if pathname == "/graph-metrics":
        return layout()
    else:
        return html.Div("Page not found")
    


