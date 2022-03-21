from dash import html
from dash import dcc
from blogapp.dashapp.utils import *

layout = html.Div(id = 'parent', children = [
    html.H1(id = 'H1', children = 'Regional Volcano Activities Look-Up tool', style = {'textAlign':'center',\
                                   'marginTop':40,'marginBottom':40}),
        # drop down value to select different regions
        dcc.Dropdown(id = 'dropdown',
        options = [{'label':'All', 'value':'ALL' }] + region_options,
        value = 'ALL'),
        dcc.Graph(id = 'abacus_plot'),
        dcc.Graph(id = 'geo_plot')
    ])