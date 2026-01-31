from dash import html, dcc, Output, Input, State, callback
import plotly.express as px
import pandas as pd
import math  # Nécessaire pour l'arrondi


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
            dcc.RangeSlider(
                min=slider_min,
                max=slider_max,
                step=step,
                value=[slider_min, slider_max],
                marks={i: f'{i}m' for i in range(int(slider_min), int(slider_max) + 1, step_marks_depth)},
                tooltip={"placement": "bottom", "always_visible": True},
                id='depth-slider'
            )
        ], style={'padding': '20px'}),
        html.Div([
            dcc.Graph(id='graph-depth-map', style={'width': '48%', 'display': 'inline-block'}),
            dcc.Graph(id='graph-depth-hist', style={'width': '48%', 'display': 'inline-block', 'float': 'right'})
        ])
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

    fig_map = px.scatter_map(
        dff,
        lat="latitude",
        lon="longitude",
        color="category",
        size_max=15,
        zoom=1,
        map_style="open-street-map",
        title=f"Distribution by species (Depth: {val_range[0]}m to {val_range[1]}m)",
        hover_data=['bathymetry']
    )
    fig_hist = px.histogram(
        dff,
        x="bathymetry",
        color="category",
        facet_col="category",
        facet_col_wrap=2,
        title="Species Distribution by Depth",
        labels={'bathymetry': 'Depth (m)', 'count': 'Obs.'},
        nbins=20
    )
    fig_hist.update_yaxes(matches=None, showticklabels=True)
    fig_hist.update_xaxes(matches='x')
    fig_hist.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='black'
    )
    return fig_map, fig_hist