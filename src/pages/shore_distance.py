from dash import html, dcc, Output, Input, State, callback
import plotly.express as px
import pandas as pd


def layout_distance(df):
    return html.Div([
        html.H2("Analysis by Shore Distance"),
        dcc.RangeSlider(
            id='distance-slider',
            min=0,
            max=df['shoredistance'].max(),
            value=[0, df['shoredistance'].max()],
            tooltip={"placement": "bottom", "always_visible": True}
        ),
        html.Div([
            dcc.Graph(id='graph-distance-map', style={'width': '48%', 'display': 'inline-block'}),
            dcc.Graph(id='graph-distance-hist', style={'width': '48%', 'display': 'inline-block', 'float': 'right'})
        ])
    ])


@callback(
    Output('graph-distance-map', 'figure'),
    Output('graph-distance-hist', 'figure'),
    Input('distance-slider', 'value'),
    State('main-data-store', 'data')
)
def update_dist_page(val_range, stored_data):
    if not stored_data: return px.scatter(), px.scatter()
    dff = pd.DataFrame(stored_data)
    dff = dff[(dff['shoredistance'] >= val_range[0]) & (dff['shoredistance'] <= val_range[1])]

    fig_map = px.scatter_map(dff, lat="latitude", lon="longitude", color="category", zoom=1,
                             map_style="open-street-map")
    fig_hist = px.histogram(dff, x="shoredistance", color="category", title="Distribution by Distance")
    return fig_map, fig_hist