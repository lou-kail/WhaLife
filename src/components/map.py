from dash import dcc

def map_component():
    return dcc.Graph(id='graph-map', style={'width': '48%', 'display': 'inline-block'})
