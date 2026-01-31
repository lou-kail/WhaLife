from dash import html, dcc, Output, Input, State, callback
import plotly.express as px
import pandas as pd


def layout_salinity(df):
    return html.Div([
        html.H2("Analysis by Salinity"),
        dcc.RangeSlider(
            id='sal-slider',
            min=df['sss'].min(),
            max=df['sss'].max(),
            value=[df['sss'].min(), df['sss'].max()],
            tooltip={"placement": "bottom", "always_visible": True}
        ),
        html.Div([
            dcc.Graph(id='graph-sal-map', style={'width': '48%', 'display': 'inline-block'}),
            dcc.Graph(id='graph-sal-hist', style={'width': '48%', 'display': 'inline-block', 'float': 'right'})
        ])
    ])


@callback(
    Output('graph-sal-map', 'figure'),
    Output('graph-sal-hist', 'figure'),
    Input('sal-slider', 'value'),
    State('main-data-store', 'data')
)
def update_salinity_page(val_range, stored_data):
    if not stored_data: return px.scatter(), px.scatter()
    dff = pd.DataFrame(stored_data)
    dff = dff[(dff['sss'] >= val_range[0]) & (dff['sss'] <= val_range[1])]

    fig_map = px.scatter_map(dff, lat="latitude", lon="longitude", color="category", zoom=1,
                             map_style="open-street-map")
    fig_hist = px.histogram(dff, x="sss", color="category", title="Distribution by Salinity")
    return fig_map, fig_hist