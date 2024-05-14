# pylint: disable=W0612,R1705
import json
import random

import networkx as nx
import numpy as np
import pandas as pd
import seaborn as sns
from colour import Color
from dash import MATCH, Input, Output, State, callback

from .constants import ARROW_POSITIONS, DF_NODES, ELEMENTS, NETWORKX_DATA

current_tap_data = None


def rgb_to_hex(rgb_code):
    #print data type of rgb_code
    r = int(rgb_code[0] * 255)
    g = int(rgb_code[1] * 255)
    b = int(rgb_code[2] * 255)
    hex_code = '#%02x%02x%02x' % (r,g,b)
    return hex_code


def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


def get_ids(elements):
    ids = []
    for n in range(len(elements)):
        curr_id = elements[n].get("data").get("id")
        if curr_id:
            ids.append(curr_id)
    return ids


def validate_positive(value):
    return min(0, value)


def validate_color(color, default="#999999"):
    """
    Check if a color is valid, if so returns the color, else return a default color
    :param color: The color to validate
    :param default: The default color
    :return: A string representing a color
    """
    if not color:
        return default

    try:
        # Converting 'deep sky blue' to 'deepskyblue'
        color = color.replace(" ", "")

        if color.startswith("rgb"):
            values = color.replace("rgb(", "").replace(")", "").split(",")

            if len(values) == 3 and all(0 <= int(v) <= 255 for v in values):
                return color

            return default

        Color(color)
        # if everything goes fine then return True
        return color
    except:  # noqa
        return default


def validate_px_percentage(value, default="0px"):
    if not value:
        return default
    elif "px" in value and is_float(value.replace("px", "")):
        return value
    elif "%" in value and is_float(value.replace("%", "")):
        return value
    else:
        return default


def assign_callbacks(app):
    # ############################## HIDING ###################################
    

    @app.callback(
        Output({"type": "div-arrow-position", "index": MATCH}, "style"),
        Input("dropdown-arrow-position", "value"),
        State({"type": "div-arrow-position", "index": MATCH}, "id"),
    )
    def hide_div_arrow_position(current_pos_selected, div_id):
        if current_pos_selected != div_id["index"]:
            return {"display": "none"}
        else:
            return {"display": "block"}

    @app.callback(
        Output({"type": "div-label", "index": MATCH}, "style"),
        Input("dropdown-select-element-label-styling", "value"),
        State({"type": "div-label", "index": MATCH}, "id"),
    )
    def hide_div_label_element(current_element_selected, div_id):
        if current_element_selected != div_id["index"]:
            return {"display": "none"}
        else:
            return {"display": "block"}

    @app.callback(
        Output({"type": "div-text-wrapping", "index": MATCH}, "style"),
        Input("dropdown-select-element-text-wrapping", "value"),
        State({"type": "div-text-wrapping", "index": MATCH}, "id"),
    )
    def hide_div_text_wrapping(current_element_selected, div_id):
        if current_element_selected != div_id["index"]:
            return {"display": "none"}
        else:
            return {"display": "block"}

    @app.callback(
        Output({"type": "div-text-margins", "index": MATCH}, "style"),
        Input("dropdown-select-element-text-margins", "value"),
        State({"type": "div-text-margins", "index": MATCH}, "id"),
    )
    def hide_div_text_margins(current_element_selected, div_id):
        if current_element_selected != div_id["index"]:
            return {"display": "none"}
        else:
            return {"display": "block"}

    # @app.callback(
    #     Output("div-display-stylesheet-json", "children"),
    #     Input("cytoscape", "stylesheet"),
    # )
    # def update_json_stylesheet_output(stylesheet):
    #     return json.dumps(stylesheet, indent=2)
    
    @app.callback(
        Output("tap-output", "children"),
        [Input("cytoscape", "tapNodeData"),
        Input("cytoscape", "tapEdgeData")]
    )
    def displayTapNodeData(tap_node_data, tap_edge_data):
        global current_tap_data
        def get_node_data(node_id):
            node_atrr = ''
            for key in NETWORKX_DATA.nodes[node_id].keys():
                node_atrr += str(key) + ': ' + str(NETWORKX_DATA.nodes[node_id][key]) + "\n"
            return node_atrr
        
        if (tap_node_data) and (current_tap_data != tap_node_data):
            node = tap_node_data['id']
            result =( "You recently clicked/tapped the node: " + tap_node_data['id'].upper() + "\n" +
                     "========================================================="+ "\n" +
                    "NODE DEGREE: " + str(NETWORKX_DATA.degree()[node]) +"\n"+"(Total connection count)" +"\n"+ "\n" +
                    "NODE IN-DEGREE: " + str(NETWORKX_DATA.in_degree()[node]) + "\n" +"(Incoming connection count)" + "\n" + "\n" +
                    "NODE OUT-DEGREE: "+ str(NETWORKX_DATA.out_degree()[node]) + "\n" +"(Outgoing connection count)" + "\n" + "\n" +
                    "NODE CLUSTERING COEFFICIENT: " + str(nx.clustering(NETWORKX_DATA)[node]) + "\n" +"(How tightly-knit the neighbors are)" +"\n"+ "\n" +
                    "NODE TRIANGLES FORMED: " + str(nx.triangles(NETWORKX_DATA.to_undirected())[node]) + "\n" +"(Only applied for undirected network)"+"\n" + "\n" +
                    "NODE DEGREE CENTRALITY: "+ str(nx.degree_centrality(NETWORKX_DATA)[node]) + "\n" +"(Node's importance based on its connections)" +"\n" +"\n" +
                    "NODE BETWEENNESS CENTRALITY: "+ str(nx.betweenness_centrality(NETWORKX_DATA)[node]) + "\n" +"(How often a node appears on shortest paths between other nodes)" +"\n" +"\n" +
                    "NODE CLOSENESS CENTRALITY: " + str(nx.closeness_centrality(NETWORKX_DATA)[node]) + "\n" +"(How quickly information spreads to other nodes)" +"\n"+"\n" +
                    "NODE SINGLE SOURCE SHORTEST PATH LENGTHS: "+"\n"+"(Lengths of shortest paths from this node to other nodes)" + "\n"
                    + str(nx.single_source_shortest_path_length(NETWORKX_DATA, node)) + "\n" 
                    + "========================================================="+ "\n"
                    + "NODE ATTRIBUTES: " + "\n"
                    + get_node_data(node) 
                    )
            current_tap_data = tap_node_data
            return result
        elif tap_edge_data:
            source = str(tap_edge_data['source'])
            target = str(tap_edge_data['target'])
            result = ("You recently clicked/tapped the edge between "
                    + source.upper() + " and " + target.upper() + "\n" 
                    + "========================================================="+ "\n" 
                    + "EDGE WEIGHT: "+ str(NETWORKX_DATA[source][target]['weight']) + "\n"+ "(Strength of the connection)" + "\n" +"\n" 
                    + "EDGE BETWEENNESS CENTRALITY: " + str(nx.edge_betweenness_centrality(NETWORKX_DATA)[(source,target)]) + "\n"+ "(The importance in connecting different parts of the network)" + "\n"+ "\n" 
                    + "========================================================="+ "\n"
                    + "Source Attributes: " + "\n"
                    + get_node_data(source) + "\n"
                  
                    + "Target Attributes: " + "\n"
                    + get_node_data(target)            
            )
            return result
                                            
        else:
            return "Click to a node or edge to see the data here."
        
    

    @app.callback(
        Output("div-display-elements-json", "children"),
        Input("cytoscape", "elements"),
    )
    def update_json_elements_output(stylesheet):
        return json.dumps(stylesheet, indent=2)

    # ############################## STORING ##################################


    @app.callback(
        Output("div-storage-arrow-color", "children"),
        [Input(f"input-{pos}-arrow-color", "value") for pos in ARROW_POSITIONS],
    )
    def update_arrow_color_storage(*args):
        args = [validate_color(color) for color in args]
        return json.dumps(
            dict(zip([f"{pos}-arrow-color" for pos in ARROW_POSITIONS], args))
        )

    @app.callback(
        Output("div-storage-arrow-shape", "children"),
        [Input(f"dropdown-{pos}-arrow-shape", "value") for pos in ARROW_POSITIONS],
    )
    def update_arrow_shape_storage(*args):
        return json.dumps(
            dict(zip([f"{pos}-arrow-shape" for pos in ARROW_POSITIONS], args))
        )

    @app.callback(
        Output("div-storage-arrow-fill", "children"),
        [Input(f"radio-{pos}-arrow-fill", "value") for pos in ARROW_POSITIONS],
    )
    def update_arrow_fill_storage(*args):
        return json.dumps(
            dict(zip([f"{pos}-arrow-fill" for pos in ARROW_POSITIONS], args))
        )

    # ############################## DISABLING ################################


    @app.callback(
        Output("input-source-endpoint-width", "disabled"),
        Input("dropdown-source-endpoint-type", "value"),
    )
    def disable_source_endpoint_width(value):
        return value != "other"

    @app.callback(
        Output("input-target-endpoint-width", "disabled"),
        Input("dropdown-target-endpoint-type", "value"),
    )
    def disable_target_endpoint_width(value):
        return value != "other"

    @app.callback(
        Output("input-source-endpoint-height", "disabled"),
        Input("dropdown-source-endpoint-type", "value"),
    )
    def disable_source_endpoint_height(value):
        return value != "other"

    @app.callback(
        Output("input-target-endpoint-height", "disabled"),
        Input("dropdown-target-endpoint-type", "value"),
    )
    def disable_target_endpoint_height(value):
        return value != "other"

    # ############################## CYTOSCAPE ################################
    @app.callback(Output("cytoscape", "layout"), Input("dropdown-layout", "value"))
    def update_layout(name):
        return {"name": name, 'animate': True}

    @app.callback(
        Output("cytoscape", "stylesheet"),
        
        [Input("cytoscape", "tapNodeData"),
        Input("cytoscape", "tapEdgeData")]
        +
        [
            Input(component, "value")
            for component in [
                # Node Body
                "input-node-content",
                "input-node-width",
                "input-node-height",
                "dropdown-node-shape",
                "input-node-color",
                "slider-node-opacity",
                "slider-node-blacken",
                "input-node-border-width",
                "dropdown-node-border-style",
                "input-node-border-color",
                "slider-node-border-opacity",
                "input-node-padding",
                "dropdown-node-padding-relative-to",
            ]
        ]
   
        + [
            Input(component, "value")
            for component in [
                "input-edge-line-width",
                "dropdown-edge-curve-style",
                "edge-weight-coloring",
                "input-edge-line-color",
                "radio-edge-line-style",
                "input-edge-loop-direction",
                "input-edge-loop-sweep",
                "radio-use-edge-arrow",
            ]
        ]
        + [
            Input(div, "children")
            for div in [
                "div-storage-arrow-color",
                "div-storage-arrow-shape",
                "div-storage-arrow-fill",
            ]
        ]
        + [
            Input(component, "value")
            for component in [
                "input-arrow-scale",
                "radio-use-edge-endpoints",
                "dropdown-source-endpoint-type",
                "input-source-endpoint-width",
                "input-source-endpoint-height",
                "dropdown-target-endpoint-type",
                "input-target-endpoint-width",
                "input-target-endpoint-height",
                "input-source-distance-from-node",
                "input-target-distance-from-node",
                # Components for Labels
                "radio-use-labels",
                "input-node-label",
                "input-edge-label",
                "input-edge-source-label",
                "input-edge-target-label",
                # Label Font Styling
                "input-node-label-color",
                "slider-node-label-text-opacity",
                "input-node-label-font-family",
                "input-node-label-font-size",
                "dropdown-node-label-font-style",
                "dropdown-node-label-font-weight",
                "dropdown-node-label-text-transform",
                "input-edge-label-color",
                "slider-edge-label-text-opacity",
                "input-edge-label-font-family",
                "input-edge-label-font-size",
                "dropdown-edge-label-font-style",
                "dropdown-edge-label-font-weight",
                "dropdown-edge-label-text-transform",
                # Label Text Wrapping
                "radio-node-label-text-wrap",
                "input-node-label-text-max-width",
                "radio-edge-label-text-wrap",
                "input-edge-label-text-max-width",
                # Label Alignment
                "radio-label-text-halign",
                "radio-label-text-valign",
                "input-label-source-text-offset",
                "input-label-target-text-offset",
                # Text Margins
                "input-node-text-margin-x",
                "input-node-text-margin-y",
                "input-edge-text-margin-x",
                "input-edge-text-margin-y",
                "input-source-text-margin-x",
                "input-source-text-margin-y",
                "input-target-text-margin-x",
                "input-target-text-margin-y",
                #Atrribute
                "dropdown-attr-cat",
                "dropdown-attr-num",
                "input-max-size",
                "dropdown-pallete"
            ]
        ],
    )
    def update_stylesheet(
        tap_node_data,
        tap_edge_data,
        node_content,
        node_width,
        node_height,
        node_shape,
        node_color,
        node_opacity,
        node_blacken,
        node_border_width,
        node_border_style,
        node_border_color,
        node_border_opacity,
        node_padding,
        node_padding_relative_to,
        edge_line_width,
        edge_curve_style,
        edge_weight_coloring,
        edge_line_color,
        edge_line_style,
        edge_loop_direction,
        edge_loop_sweep,
        use_edge_arrow,
        storage_arrow_color,
        storage_arrow_shape,
        storage_arrow_fill,
        arrow_scale,
        use_edge_endpoints,
        source_endpoint_type,
        source_endpoint_width,
        source_endpoint_height,
        target_endpoint_type,
        target_endpoint_width,
        target_endpoint_height,
        source_distance_from_node,
        target_distance_from_node,
        use_labels,
        node_label,
        edge_label,
        edge_source_label,
        edge_target_label,
        node_label_color,
        node_label_text_opacity,
        node_label_font_family,
        node_label_font_size,
        node_label_font_style,
        node_label_font_weight,
        node_label_text_transform,
        edge_label_color,
        edge_label_text_opacity,
        edge_label_font_family,
        edge_label_font_size,
        edge_label_font_style,
        edge_label_font_weight,
        edge_label_text_transform,
        node_label_text_wrap,
        node_label_text_max_width,
        edge_label_text_wrap,
        edge_label_text_max_width,
        label_text_halign,
        label_text_valign,
        label_source_text_offset,
        label_target_text_offset,
        node_text_margin_x,
        node_text_margin_y,
        edge_text_margin_x,
        edge_text_margin_y,
        source_text_margin_x,
        source_text_margin_y,
        target_text_margin_x,
        target_text_margin_y,
        chosen_attr_cat,
        chosen_attr_num,
        node_max_size,
        color_palette,
    ):
        def update_style(stylesheet, selector, addition):
            for style in stylesheet:
                if style["selector"] == selector:
                    style["style"].update(addition)
                    
        def addselector_tostylesheet(stylesheet, selector, addition):
            stylesheet.append({
                "selector": selector,
                "style": addition
            })

        # Validating Input
        node_color = validate_color(node_color)
        node_border_color = validate_color(node_border_color)
        node_padding = validate_px_percentage(node_padding)
        edge_line_color = validate_color(edge_line_color)

        stylesheet = [
            {
                "selector": "node",
                "style": {
                    "content": node_content,
                    "width": node_width,
                    "height": node_height,
                    "background-color": node_color,
                    "background-blacken": node_blacken,
                    "background-opacity": node_opacity,
                    "shape": node_shape,
                    "border-width": node_border_width,
                    "border-style": node_border_style,
                    "border-color": node_border_color,
                    "border-opacity": node_border_opacity,
                    "padding": node_padding,
                    "padding-relative-to": node_padding_relative_to,
                    "compound-sizing-wrt-labels": 'include',
                    "min-width": 0,
                    "min-width-bias-left": 0,
                    "min-width-bias-right": 0,
                    "min-height": 0,
                    "min-height-bias-top": 0,
                    "min-height-bias-bottom": 0,
                },
            },
            {
                "selector": "edge",
                "style": {
                    "width": edge_line_width,
                    "curve-style": edge_curve_style,
                    "line-color": edge_line_color,
                    "line-style": edge_line_style,
                    "loop-direction": f"{edge_loop_direction}deg",
                    "loop-sweep": f"{edge_loop_sweep}deg", 
                },
            },
        ]

        
        ############# Style by Attribute ################
        def style_by_stat(chosen_stat, node_max_size=50):
            max_key = max(chosen_stat, key=chosen_stat.get)
            max_value = chosen_stat[max_key]
            if max_value == 0:
                weight = 1
            else:
                weight = node_max_size/max_value
            for key in chosen_stat.keys():
                slt = f'[ID = {key}]'
                size = chosen_stat[key]*weight
                addselector_tostylesheet(
                    stylesheet=stylesheet,
                    selector=slt,
                    addition={
                        "width": size,
                        "height": size,
                        "background-color": "#736899"
                    },
                )
        
        if chosen_attr_num != "None":
            if chosen_attr_num == "Degree Centrality":
                style_by_stat(nx.degree_centrality(NETWORKX_DATA),node_max_size)
            elif chosen_attr_num == "Betweenness Centrality":
                style_by_stat(nx.betweenness_centrality(NETWORKX_DATA),node_max_size)
            elif chosen_attr_num == "Closeness Centrality":
                style_by_stat(nx.closeness_centrality(NETWORKX_DATA),node_max_size)
            else:            
                max_value = DF_NODES[chosen_attr_num].max()
                if max_value == 0:
                    weight = 1
                else:
                    weight = node_max_size/max_value
        
                for value in DF_NODES[chosen_attr_num].unique():
                    slt = f'[{chosen_attr_num} = "{value}"]'
                    #node size set to value
                    if pd.notna(value):
                        slt = f'[{chosen_attr_num} = {value}]'
                        addselector_tostylesheet(
                            stylesheet=stylesheet,
                            selector=slt,
                            addition={
                                "width": value*weight,
                                "height": value*weight,
                                "background-color": "#736899"
                            },
                        )

        if chosen_attr_cat != "None":
            palette = sns.color_palette(color_palette, DF_NODES[chosen_attr_cat].nunique())
            color_id = 0
            for value in DF_NODES[chosen_attr_cat].unique():
                color_rgb = palette[color_id]
                color = rgb_to_hex(color_rgb)
                                
                if pd.notna(value):
                    slt = f'[{chosen_attr_cat} = "{value}"]'
                    addselector_tostylesheet(
                        stylesheet=stylesheet,
                        selector=slt,
                        addition={
                            "background-color": color,
                        },
                    )
                    color_id += 1


        if use_edge_arrow == "yes":
            arrow_color = json.loads(storage_arrow_color)
            arrow_shape = json.loads(storage_arrow_shape)
            arrow_fill = json.loads(storage_arrow_fill)

            update_style(
                stylesheet=stylesheet,
                selector="edge",
                addition={
                    "arrow-scale": arrow_scale,
                    **arrow_color,
                    **arrow_shape,
                    **arrow_fill,
                },
            )

        if use_edge_endpoints == "yes":
            if source_endpoint_type == "other":
                source_endpoint_width = validate_px_percentage(source_endpoint_width)
                source_endpoint_height = validate_px_percentage(source_endpoint_height)
                source_endpoint = f"{source_endpoint_width} {source_endpoint_height}"
            else:
                source_endpoint = source_endpoint_type

            if target_endpoint_type == "other":
                target_endpoint_width = validate_px_percentage(target_endpoint_width)
                target_endpoint_height = validate_px_percentage(target_endpoint_height)
                target_endpoint = f"{target_endpoint_width} {target_endpoint_height}"
            else:
                target_endpoint = target_endpoint_type

            update_style(
                stylesheet=stylesheet,
                selector="edge",
                addition={
                    "source-endpoint": source_endpoint,
                    "target-endpoint": target_endpoint,
                    "source-distance-from-node": source_distance_from_node,
                    "target-distance-from-node": target_distance_from_node,
                },
            )

        if use_labels == "yes":
            node_label_color = validate_color(node_label_color, default="black")
            edge_label_color = validate_color(edge_label_color, default="black")

            update_style(
                stylesheet=stylesheet,
                selector="node",
                addition={
                    "label": node_label,
                    # Font Styling
                    "color": node_label_color,
                    "text-opacity": node_label_text_opacity,
                    "font-family": node_label_font_family,
                    "font-size": node_label_font_size,
                    "font-style": node_label_font_style,
                    "font-weight": node_label_font_weight,
                    "text-transform": node_label_text_transform,
                    # Text Wrapping
                    "text-wrap": node_label_text_wrap,
                    "text-max-width": node_label_text_max_width,
                    # Label Alignment
                    "text-halign": label_text_halign,
                    "text-valign": label_text_valign,
                    # Text Margin
                    "text-margin-x": node_text_margin_x,
                    "text-margin-y": node_text_margin_y,
                },
            )

            update_style(
                stylesheet=stylesheet,
                selector="edge",
                addition={
                    "label": edge_label,
                    "source-label": edge_source_label,
                    "target-label": edge_target_label,
                    # Font Styling
                    "color": edge_label_color,
                    "text-opacity": edge_label_text_opacity,
                    "font-family": edge_label_font_family,
                    "font-size": edge_label_font_size,
                    "font-style": edge_label_font_style,
                    "font-weight": edge_label_font_weight,
                    "text-transform": edge_label_text_transform,
                    # Text Wrapping
                    "text-wrap": edge_label_text_wrap,
                    "text-max-width": edge_label_text_max_width,
                    # Label Alignment
                    "source-text-offset": label_source_text_offset,
                    "target-text-offset": label_target_text_offset,
                    # Text Margin
                    "text-margin-x": edge_text_margin_x,
                    "text-margin-y": edge_text_margin_y,
                    "source-text-margin-x": source_text_margin_x,
                    "source-text-margin-y": source_text_margin_y,
                    "target-text-margin-x": target_text_margin_x,
                    "target-text-margin-y": target_text_margin_y,
                },
            )
            
            
        
                
        ############ Style Edge by weight ###############
        def generate_color(rgb, weight):
            rgb = tuple((elem*255 + (255-elem*255)*(1-weight))/255 for elem in rgb)
            hex = rgb_to_hex(rgb)
            return hex
        
        if edge_weight_coloring == "yes":
            default_color = "#003319"
            if edge_line_color != "#999999":
                default_color = edge_line_color
            rgb_default = Color(default_color).rgb
            max_weight = max([data['weight'] for source, target, data in NETWORKX_DATA.edges(data=True)])
            min_weight = min([data['weight'] for source, target, data in NETWORKX_DATA.edges(data=True)])
            if max_weight != min_weight:
                for source, target, data in NETWORKX_DATA.edges(data=True):
                    color_strength = (data['weight'] - min_weight)/(max_weight - min_weight)
                    edge_color = generate_color(rgb_default, color_strength)
                    addselector_tostylesheet(
                        stylesheet=stylesheet,
                        selector=f'edge[source = "{source}"][target = "{target}"]',
                        addition={
                            "line-color": edge_color,
                        },
                    )
 

        ############# Style Tap data ################
        if tap_node_data:
            node_id = tap_node_data['id']
            addselector_tostylesheet(
                stylesheet=stylesheet,
                selector=f'node[id = "{node_id}"]',
                addition={
                    "border-width": 4,
                    "border-color": "red",
                },
            )
            
        if tap_edge_data:
            source = str(tap_edge_data['source'])
            target = str(tap_edge_data['target'])
            addselector_tostylesheet(
                stylesheet=stylesheet,
                selector=f'edge[source = "{source}"][target = "{target}"]',
                addition={
                    "line-color": "red",
                },
            )
            
            



        return stylesheet
