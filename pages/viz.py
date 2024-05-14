import dash
import dash_cytoscape as cyto
cyto.load_extra_layouts()

from pages.demos.editor.callbacks import assign_callbacks
from pages.demos.editor.layout import layout

def init_callbacks(app):
    assign_callbacks(app)