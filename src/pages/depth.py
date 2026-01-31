from dash import html, dcc, Output, Input, State, callback
import plotly.express as px
import pandas as pd


def layout_depth(df):
    clean_depth = df['bathymetry'].dropna()
    min_v = int(clean_depth.min())
    max_v = int(clean_depth.max())
    return html.Div([
        dcc.RangeSlider(
            id='depth-slider',
            min=min_v,
            max=max_v,
            value=[min_v, max_v],
            step=50,
            marks={i: f'{i}m' for i in range(min_v, max_v + 1, (max_v-min_v)//5)},
            tooltip={"placement": "bottom", "always_visible": True}
        ),
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
    if not stored_data: return px.scatter(), px.scatter()
    dff = pd.DataFrame(stored_data)
    dff = dff[(dff['bathymetry'] >= val_range[0]) & (dff['bathymetry'] <= val_range[1])]

    fig_map = px.scatter_map(dff, lat="latitude", lon="longitude", color="category", zoom=1,
                             map_style="open-street-map")
    fig_hist = px.histogram(dff, x="bathymetry", color="category", title="Distribution by Depth")
    return fig_map, fig_hist