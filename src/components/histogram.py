from dash import dcc

def histogram():
    return dcc.Graph(id='graph-histogram', style={'width': '48%', 'display': 'inline-block'})
