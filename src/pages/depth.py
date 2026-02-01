from dash import html, dcc, Output, Input, State, callback
import plotly.express as px
import pandas as pd
import math  # Nécessaire pour l'arrondi
from src.components.slider import slider
from src.components.scatter_map import scatter_map
from src.components.histogram import histogram

def layout_depth(df):
    real_max = df['bathymetry'].max()
    real_min = df['bathymetry'].min()
    step = 50
    slider_max = math.ceil(real_max / step) * step
    slider_min = math.floor(real_min / step) * step
    step_marks_depth = int(slider_max // 5)
    if step_marks_depth == 0: step_marks_depth = 1

    return html.Div([
        html.H2("Analysis by Depth"),
        html.Label("Select Depth:"),

        html.Div([
            html.Label("Filter by depth (meters) :"),
            slider(slider_min, slider_max, "m", step, step_marks_depth, "depth-slider")
        ], style={'padding': '20px'}),
        dcc.Loading(
            id="loading-temperature",
            type="circle",
            color="#007bff",
            children= html.Div([
                dcc.Graph(id='graph-depth-map', style={'width': '48%', 'display': 'inline-block'}),
                dcc.Graph(id='graph-depth-hist', style={'width': '48%', 'display': 'inline-block', 'float': 'right'})
            ])
        )
    ])


@callback(
    Output('graph-depth-map', 'figure'),
    Output('graph-depth-hist', 'figure'),
    Input('depth-slider', 'value'),
    State('main-data-store', 'data')
)
def update_depth_page(val_range, stored_data):
    if not stored_data: return px.scatter(), px.histogram()
    dff = pd.DataFrame(stored_data)

    dff = dff[(dff['bathymetry'] >= val_range[0]) & (dff['bathymetry'] <= val_range[1])]
    fig_map = scatter_map(dff, f"Distribution by species (Depth: {val_range[0]}m to {val_range[1]}m)", 'bathymetry')
    fig_hist = histogram(dff, "bathymetry","Species Distribution by Depth", {'bathymetry': 'Depth (m)', 'count': 'Obs.'})
    fig_hist.update_yaxes(matches=None, showticklabels=True)
    fig_hist.update_xaxes(matches='x')
    fig_hist.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='black'
    )
    return fig_map, fig_hist