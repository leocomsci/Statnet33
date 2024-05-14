import dash_cytoscape as cyto
from dash import dcc, html

from pages.demos import dash_reusable_components as drc

from .constants import (CATEGORICAL_ATTR, ELEMENTS, LABEL_ELEMENT_TYPES,
                        LABEL_ELEMENT_TYPES_ALL, NUMERIC_ATTR)

user_interface = html.Div(
    style={
        "height": "calc(100vh - 90px)",
        "overflow-y": "auto",
        "overflow-x": "hidden",
    },
    children=[
        drc.SectionTitle(title="Layout", size=3, color="white"),
        drc.NamedCard(
            title="Layout",
            size=4,
            children=[
                drc.NamedDropdown(
                    name="Layout",
                    id="dropdown-layout",
                    options=drc.DropdownOptionsList(
                        "random",
                        "preset",
                        "grid",
                        "circle",
                        "concentric",
                        "breadthfirst",
                        "cose",
                        "cose-bilkent", "fcose", "cola", "euler", "spread", "dagre", "klay",
                    ),
                    value="cose",
                    clearable=False,
                ),
            ],
        ),
        
        drc.SectionTitle(title="Node Styling", size=3, color="white"),
        drc.NamedCard(
            title="Content",
            size=4,
            children=[
                drc.NamedInput(
                    name="Node Display Content",
                    id="input-node-content",
                    type="text",
                    value="data(Name)",
                    placeholder="Enter the content you want for node...",
                )
            ],
        ),
        drc.NamedCard(
            title="Style by Attributes",
            size=4,
            children=[
                drc.NamedDropdown(
                    name="Select a categorical attribute to color nodes",
                    id="dropdown-attr-cat",
                    options=drc.DropdownOptionsList("None",*CATEGORICAL_ATTR),
                    value="None",
                    clearable=False,
                ),
                drc.NamedDropdown(
                    name="Select attribute/statistic to resize nodes",
                    id="dropdown-attr-num",
                    options=drc.DropdownOptionsList("None",*NUMERIC_ATTR,"Degree Centrality","Betweenness Centrality","Closeness Centrality"),
                    value="None",
                    clearable=False,
                ),
                drc.NamedDropdown(
                    name="Select color pallete",
                    id="dropdown-pallete",
                    options=drc.DropdownOptionsList("pastel","deep","muted","bright","dark","colorblind","flare","mako","viridis","cubehelix","Spectral","Set1","Set2","Set3","tab10","tab20","tab20b","tab20c"),
                    value="pastel",
                    clearable=False,
                ),
                drc.NamedInput(
                    name="Auto Resize - Node Max Size",
                    id="input-max-size",
                    type="number",
                    min=0,
                    value=50,
                    placeholder="Enter a value in pixel...",
                ),
                ],
            ),
        drc.NamedCard(
            title="Shape",
            size=4,
            children=[
                
                drc.NamedInput(
                    name="Node Width (px)",
                    id="input-node-width",
                    type="number",
                    min=0,
                    value=25,
                    placeholder="Enter a value in pixel...",
                ),
                drc.NamedInput(
                    name="Node Height (px)",
                    id="input-node-height",
                    type="number",
                    min=0,
                    value=25,
                    placeholder="Enter a value in pixel...",
                ),
                drc.NamedDropdown(
                    name="Node Shape",
                    id="dropdown-node-shape",
                    value="ellipse",
                    clearable=False,
                    options=drc.DropdownOptionsList(
                        "ellipse",
                        "triangle",
                        "rectangle",
                        "roundrectangle",
                        "bottomroundrectangle",
                        "cutrectangle",
                        "barrel",
                        "rhomboid",
                        "diamond",
                        "pentagon",
                        "hexagon",
                        "concavehexagon",
                        "heptagon",
                        "octagon",
                        "star",
                        "tag",
                        "vee",
                        "polygon",
                    ),
                ),
                
            ],
        ),
        drc.NamedCard(
            title="Colour",
            size=4,
            children=[
                drc.NamedInput(
                    name="Node Color",
                    id="input-node-color",
                    type="text",
                    placeholder="Enter Color in Hex...",
                ),
                drc.NamedSlider(
                    name="Node Opacity",
                    id="slider-node-opacity",
                    min=0,
                    max=1,
                    marks={0: "0", 1: "1"},
                    step=0.05,
                    value=1,
                ),
                drc.NamedSlider(
                    name="Node Blacken",
                    id="slider-node-blacken",
                    min=0,
                    max=1,
                    marks={0: "0", 1: "1"},
                    step=0.05,
                    value=0,
                ),
            ],
        ),
        drc.NamedCard(
            title="Border",
            size=4,
            children=[
                drc.NamedInput(
                    name="Node Border Width (px)",
                    id="input-node-border-width",
                    type="number",
                    min=0,
                    value=0,
                    placeholder="Enter a value in pixel...",
                ),
                drc.NamedDropdown(
                    name="Node Border Style",
                    id="dropdown-node-border-style",
                    value="solid",
                    clearable=False,
                    options=drc.DropdownOptionsList(
                        "null", "solid", "dotted", "dashed", "double"
                    ),
                ),
                drc.NamedInput(
                    name="Node Border Color",
                    id="input-node-border-color",
                    type="text",
                    placeholder="Input Color in Hex...",
                ),
                drc.NamedSlider(
                    name="Node Border Opacity",
                    id="slider-node-border-opacity",
                    min=0,
                    max=1,
                    marks={0: "0", 1: "1"},
                    step=0.05,
                    value=1,
                ),
            ],
        ),
        drc.NamedCard(
            title="Padding",
            size=4,
            children=[
                drc.NamedInput(
                    name="Node Padding",
                    id="input-node-padding",
                    type="text",
                    placeholder="Input value in % or px...",
                    value="0px",
                ),
                drc.NamedDropdown(
                    name="Node Padding Relative To",
                    id="dropdown-node-padding-relative-to",
                    value="width",
                    clearable=False,
                    options=drc.DropdownOptionsList(
                        "width", "height", "average", "min", "max"
                    ),
                ),
            ],
        ),
        drc.SectionTitle(title="Edges", size=3, color="white"),
        # TODO: Add options to modify (unbundled) bezier edges, haystack edges
        drc.NamedCard(
            title="Edge line",
            size=4,
            children=[
                drc.NamedInput(
                    name="Line Width (px)",
                    id="input-edge-line-width",
                    type="number",
                    min=0,
                    placeholder="Input value in px...",
                ),
                drc.NamedDropdown(
                    name="Curving Method",
                    id="dropdown-edge-curve-style",
                    value="haystack",
                    clearable=False,
                    options=drc.DropdownOptionsList(
                        "haystack",
                        "bezier",
                        "unbundled-bezier",
                        "segments",
                    ),
                ),
                drc.NamedRadioItems(
                    name="Coloring by weight",
                    id="edge-weight-coloring",
                    options=drc.DropdownOptionsList("yes", "no"),
                    value="no",
                ),
                
                drc.NamedInput(
                    name="Line Color",
                    id="input-edge-line-color",
                    type="text",
                    placeholder="Input Color in Hex...",
                ),
                
                drc.NamedRadioItems(
                    name="Line Style",
                    id="radio-edge-line-style",
                    value="solid",
                    options=drc.DropdownOptionsList("solid", "dotted", "dashed"),
                ),
            ],
        ),
        drc.NamedCard(
            title="Loop edges",
            size=4,
            children=[
                drc.NamedInput(
                    name="Direction of loop (angle degree)",
                    id="input-edge-loop-direction",
                    type="number",
                    value=-45,
                    placeholder="Input value in deg...",
                ),
                drc.NamedInput(
                    name="Loop Sweep (angle degree)",
                    id="input-edge-loop-sweep",
                    type="number",
                    value=-90,
                    placeholder="Input value in deg...",
                ),
            ],
        ),
        drc.NamedCard(
            title="Edge Arrow",
            size=4,
            children=[
                html.Div(id="div-storage-arrow-color", style={"display": "none"}),
                html.Div(id="div-storage-arrow-shape", style={"display": "none"}),
                html.Div(id="div-storage-arrow-fill", style={"display": "none"}),
                drc.NamedRadioItems(
                    name="Use Edge Arrow",
                    id="radio-use-edge-arrow",
                    options=drc.DropdownOptionsList("yes", "no"),
                    value="yes",
                ),
                drc.NamedDropdown(
                    name="Select Arrow Position",
                    id="dropdown-arrow-position",
                    options=[
                        {
                            "label": pos.capitalize(),
                            "value": pos,
                        }
                        for pos in ["mid-source", "mid-target"]
                    ],
                    value="mid-target",
                    clearable=False,
                ),
                *[
                    html.Div(
                        id={"type": "div-arrow-position", "index": pos},
                        style={"display": "block"},
                        children=[
                            drc.NamedInput(
                                name=f"Arrow Color for {pos}",
                                id=f"input-{pos}-arrow-color",
                                type="text",
                                placeholder="Input Color in Hex...",
                            ),
                            drc.NamedDropdown(
                                name=f"Arrow Shape for {pos}",
                                id=f"dropdown-{pos}-arrow-shape",
                                options=drc.DropdownOptionsList(
                                    "triangle",
                                    "triangle-tee",
                                    "triangle-cross",
                                    "triangle-backcurve",
                                    "vee",
                                    "tee",
                                    "square",
                                    "circle",
                                    "diamond",
                                    "none",
                                ),
                                clearable=False,
                                value="none",
                            ),
                            drc.NamedRadioItems(
                                name=f"Arrow Fill for {pos}",
                                id=f"radio-{pos}-arrow-fill",
                                options=drc.DropdownOptionsList("filled", "hollow"),
                                value="filled",
                            ),
                        ],
                    )
                    for pos in ["source", "mid-source", "target", "mid-target"]
                ],
                drc.NamedInput(
                    name="Scale of Arrow Size",
                    id="input-arrow-scale",
                    type="number",
                    min=0,
                    placeholder="Input numerical value...",
                ),
            ],
        ),
        drc.NamedCard(
            title="Edge Endpoints",
            size=4,
            children=[
                drc.NamedRadioItems(
                    name="Use Edge Endpoints",
                    id="radio-use-edge-endpoints",
                    options=drc.DropdownOptionsList("yes", "no"),
                    value="no",
                ),
                *[
                    html.Div(
                        id=f"div-endpoint-{side}",
                        children=[
                            drc.NamedDropdown(
                                name=f"{side.capitalize()} Endpoint Type",
                                id=f"dropdown-{side}-endpoint-type",
                                options=[
                                    {
                                        "label": "Outside to Node",
                                        "value": "outside-to-node",
                                    },
                                    {
                                        "label": "Inside to Node",
                                        "value": "inside-to-node",
                                    },
                                    {
                                        "label": "Specify Percentage (Relative) or Pixel (Absolute)",
                                        "value": "other",
                                    },
                                ],
                                value="outside-to-node",
                                clearable=False,
                            ),
                            drc.NamedInput(
                                name=f"{side.capitalize()} Endpoint Width (Relative % or Absolute px)",
                                id=f"input-{side}-endpoint-width",
                                type="text",
                                placeholder="Input value in % or px...",
                                value="0px",
                            ),
                            drc.NamedInput(
                                name=f"{side.capitalize()} Endpoint Height (Relative % or Absolute px)",
                                id=f"input-{side}-endpoint-height",
                                type="text",
                                placeholder="Input value in % or px...",
                                value="0px",
                            ),
                        ],
                    )
                    for side in ["source", "target"]
                ],
                drc.NamedInput(
                    name="Source Distance from node",
                    id="input-source-distance-from-node",
                    type="number",
                    placeholder="Input value in px...",
                    value=0,
                ),
                drc.NamedInput(
                    name="Target Distance from node",
                    id="input-target-distance-from-node",
                    type="number",
                    placeholder="Input value in px...",
                    value=0,
                ),
            ],
        ),
        drc.SectionTitle(title="Labels", size=3, color="white"),
        drc.Card(
            [
                drc.NamedRadioItems(
                    name="Use Labels",
                    id="radio-use-labels",
                    options=drc.DropdownOptionsList("yes", "no"),
                    value="no",
                ),
                drc.NamedInput(
                    name="Node Label",
                    id="input-node-label",
                    type="text",
                    placeholder="Enter your label...",
                    value="data(label)",
                ),
                drc.NamedInput(
                    name="Edge Label",
                    id="input-edge-label",
                    type="text",
                    placeholder="Enter your label...",
                    value="data(label)",
                ),
                drc.NamedInput(
                    name="Edge Source Label",
                    id="input-edge-source-label",
                    type="text",
                    placeholder="Enter your label...",
                    value="data(label)",
                ),
                drc.NamedInput(
                    name="Edge Target Label",
                    id="input-edge-target-label",
                    type="text",
                    placeholder="Enter your label...",
                    value="data(label)",
                ),
            ]
        ),
        drc.NamedCard(
            title="Font Styling",
            size=4,
            children=[
                drc.NamedDropdown(
                    name="Select an element to modify its style",
                    id="dropdown-select-element-label-styling",
                    options=[
                        {
                            "label": element.capitalize(),
                            "value": element,
                        }
                        for element in LABEL_ELEMENT_TYPES
                    ],
                    clearable=False,
                    value="node",
                ),
                *[
                    html.Div(
                        id={"type": "div-label", "index": element},
                        children=[
                            drc.NamedInput(
                                name=f"{element.capitalize()} Label Color",
                                id=f"input-{element}-label-color",
                                type="text",
                                placeholder="Enter Color in Hex...",
                            ),
                            drc.NamedSlider(
                                name=f"{element.capitalize()} Label Opacity",
                                id=f"slider-{element}-label-text-opacity",
                                min=0,
                                max=1,
                                marks={0: "0", 1: "1"},
                                step=0.05,
                                value=1,
                            ),
                            drc.NamedInput(
                                name=f"{element.capitalize()} Label Font Family",
                                id=f"input-{element}-label-font-family",
                                type="text",
                                placeholder="Enter Name of Font...",
                            ),
                            drc.NamedInput(
                                name=f"{element.capitalize()} Label Font Size",
                                id=f"input-{element}-label-font-size",
                                type="number",
                                placeholder="Enter pixel size of font...",
                            ),
                            drc.NamedDropdown(
                                name=f"{element.capitalize()} Label Font Style (CSS-like)",
                                id=f"dropdown-{element}-label-font-style",
                                options=drc.DropdownOptionsList(
                                    "normal", "italic", "oblique"
                                ),
                                clearable=False,
                                searchable=False,
                                value="normal",
                            ),
                            drc.NamedDropdown(
                                name=f"{element.capitalize()} Label Font Weight (CSS-like)",
                                id=f"dropdown-{element}-label-font-weight",
                                options=drc.DropdownOptionsList(
                                    "normal", "bold", "lighter", "bolder"
                                ),
                                clearable=False,
                                searchable=False,
                                value="normal",
                            ),
                            drc.NamedDropdown(
                                name=f"{element.capitalize()} Label Text Transform",
                                id=f"dropdown-{element}-label-text-transform",
                                options=drc.DropdownOptionsList(
                                    "none", "uppercase", "lowercase"
                                ),
                                clearable=False,
                                searchable=False,
                                value="none",
                            ),
                        ],
                    )
                    for element in LABEL_ELEMENT_TYPES
                ],
            ],
        ),
        drc.NamedCard(
            title="Text Wrapping",
            size=4,
            children=[
                drc.NamedDropdown(
                    name="Select an element to modify its text wrap",
                    id="dropdown-select-element-text-wrapping",
                    options=[
                        {
                            "label": element.capitalize(),
                            "value": element,
                        }
                        for element in LABEL_ELEMENT_TYPES
                    ],
                    clearable=False,
                    value="node",
                ),
                *[
                    html.Div(
                        id={"type": "div-text-wrapping", "index": element},
                        children=[
                            drc.NamedRadioItems(
                                name=f"{element.capitalize()} Text Wrap",
                                id=f"radio-{element}-label-text-wrap",
                                options=drc.DropdownOptionsList(
                                    "none", "wrap", "ellipsis"
                                ),
                                value="none",
                            ),
                            drc.NamedInput(
                                name=f"{element.capitalize()} Max Width (px)",
                                id=f"input-{element}-label-text-max-width",
                                type="number",
                                placeholder="Enter the maximum width in px...",
                            ),
                        ],
                    )
                    for element in LABEL_ELEMENT_TYPES
                ],
            ],
        ),
        drc.NamedCard(
            title="Label Alignment",
            size=4,
            children=[
                drc.NamedRadioItems(
                    name="Horizontal Node Label Alignment",
                    id="radio-label-text-halign",
                    options=drc.DropdownOptionsList("left", "right", "center"),
                    value="center",
                ),
                drc.NamedRadioItems(
                    name="Vertical Node Label Alignment",
                    id="radio-label-text-valign",
                    options=drc.DropdownOptionsList("top", "center", "bottom"),
                    value="center",
                ),
                drc.NamedInput(
                    name="Edge Source Label distance from node (px)",
                    id="input-label-source-text-offset",
                    type="number",
                    placeholder="Enter value in px...",
                ),
                drc.NamedInput(
                    name="Edge Target Label distance from node (px)",
                    id="input-label-target-text-offset",
                    type="number",
                    placeholder="Enter value in px...",
                ),
            ],
        ),
        drc.NamedCard(
            title="Margins",
            size=4,
            children=[
                drc.NamedDropdown(
                    name="Select an element to modify its margins",
                    id="dropdown-select-element-text-margins",
                    options=[
                        {
                            "label": element.capitalize(),
                            "value": element,
                        }
                        for element in LABEL_ELEMENT_TYPES_ALL
                    ],
                    clearable=False,
                    value="node",
                ),
                *[
                    html.Div(
                        id={"type": "div-text-margins", "index": element},
                        children=[
                            drc.NamedInput(
                                name=f"{element.capitalize()} Margin X (px)",
                                id=f"input-{element}-text-margin-x",
                                type="number",
                                placeholder="Enter a value in px...",
                            ),
                            drc.NamedInput(
                                name=f"{element.capitalize()} Margin Y(px)",
                                id=f"input-{element}-text-margin-y",
                                type="number",
                                placeholder="Enter a value in px...",
                            ),
                        ],
                    )
                    for element in LABEL_ELEMENT_TYPES_ALL
                ],
            ],
        ),
    ],
)


layout = html.Div(
    [
        html.Div(style={'display': 'flex', 'justifyContent': 'center'}, children=[
            html.H1("Specific Visualization For Deeper Research")
        ]),
        html.Div(
            className="row",
            style={"overflow": "visible"},
            children=[
                cyto.Cytoscape(
                    id="cytoscape",
                    className="eight columns",
                    layout={"name": "preset"},
                    elements=ELEMENTS,
                    style={"height": "calc(100vh - 16px)"},
                ),
                html.Div(
                    className="four columns",
                    style={
                        "height": "100vh",
                        "float": "right",
                        "background-color": "#222222",
                        "margin": "-7.8px",
                    },
                    children=dcc.Tabs(
                        id="tabs",
                        value="UI",
                        children=[
                            dcc.Tab(
                                label="Selected Item Statistics",
                                id="tab-statistics",
                                value="des-stats",
                                children=html.Div(
                                    style={
                                        "height": "calc(100vh - 90px)",
                                        "overflow": "auto",
                                    },
                                    children=html.Pre(
                                        id="tap-output",
                                        style={
                                            "color": "#d0d0d0",
                                            "margin": "5px",
                                        },
                                    ),
                                    
                                ),
                            ),
                            dcc.Tab(
                                label="Visualization Styling",
                                value="UI",
                                children=user_interface,
                            ),
                         
                            
                            # dcc.Tab(
                            #     label="Stylesheet JSON",
                            #     id="tab-display-stylesheet-json",
                            #     value="stylesheet-json",
                            #     children=html.Div(
                            #         style={
                            #             "height": "calc(100vh - 90px)",
                            #             "overflow": "auto",
                            #         },
                            #         children=html.Pre(
                            #             id="div-display-stylesheet-json",
                            #             style={
                            #                 "color": "#d0d0d0",
                            #                 "margin": "5px",
                            #             },
                            #         ),
                            #     ),
                            # ),
                            # dcc.Tab(
                            #     label="Elements JSON",
                            #     id="tab-display-elements-json",
                            #     value="elements-json",
                            #     children=html.Div(
                            #         style={
                            #             "height": "calc(100vh - 90px)",
                            #             "overflow": "auto",
                            #         },
                            #         children=html.Pre(
                            #             id="div-display-elements-json",
                            #             style={
                            #                 "color": "#d0d0d0",
                            #                 "margin": "5px",
                            #             },
                            #         ),
                            #     ),
                            # ),
                        ],
                    ),
                ),
            ],
        )
    ]
)
