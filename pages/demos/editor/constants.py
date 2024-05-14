import json
import os
import random

import networkx as nx
import pandas as pd

#######################################

def createpath(path_name):
    dirname = os.path.dirname(__file__)
    path = os.path.join(dirname, path_name)
    return path

# Read edge data
path1 = createpath('../../data/network_edges.csv')
data = pd.read_csv(path1)

# Add weights to the edges if not present
if 'Weight' not in data.columns:
    # weight is a random number from 0 to 1
    data['Weight'] = [random.random() for i in range(len(data))]


#Read node data
path2 = createpath('../../data/network_data.csv')
attr = pd.read_csv(path2)
#if no ID column, add it
if 'ID' not in attr.columns:
    attr['ID'] = attr.index


#Create Networkx graph
DG = nx.DiGraph()
for i in range(len(data)):
    DG.add_edge(str(data['Source'][i]), str(data['Target'][i]), weight=data['Weight'][i])
    
for index, row in attr.iterrows():
    node_id = str(row['ID'])
    attributes = row
    DG.add_node(node_id, **attributes)
        

#Get attribute list
numeric_attributes = []
categorical_attributes = []

for att in attr.columns.to_list():
    #if is numeric
    if pd.api.types.is_numeric_dtype(attr[att]):
        numeric_attributes.append(att)
    elif pd.api.types.is_string_dtype(attr[att]):
        categorical_attributes.append(att)
attr_list = numeric_attributes + categorical_attributes
    

#################################################################    

ELEMENTS = nx.cytoscape_data(DG)['elements']
ARROW_POSITIONS = ("source", "mid-source", "target", "mid-target")
LABEL_ELEMENT_TYPES = ("node", "edge")
LABEL_ELEMENT_TYPES_ALL = ("node", "edge", "source", "target")
DF_NODES = attr
DF_EDGES = data
NUMERIC_ATTR = numeric_attributes
CATEGORICAL_ATTR = categorical_attributes
NETWORKX_DATA = DG
