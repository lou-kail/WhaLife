from dash import html, dcc, Output, Input, State, callback
import plotly.express as px
import pandas as pd


def layout_temperature(df):
    return html.Div([
        html.H2("Analysis by Temperature"),
        dcc.RangeSlider(
            id='temp-slider',
            min=df['sst'].min(),
            max=df['sst'].max(),
            value=[df['sst'].min(), df['sst'].max()],
            tooltip={"placement": "bottom", "always_visible": True}
        ),
        html.Div([
            dcc.Graph(id='graph-temp-map', style={'width': '48%', 'display': 'inline-block'}),
            dcc.Graph(id='graph-temp-hist', style={'width': '48%', 'display': 'inline-block', 'float': 'right'})
        ])
    ])


@callback(
    Output('graph-temp-map', 'figure'),
    Output('graph-temp-hist', 'figure'),
    Input('temp-slider', 'value'),
    State('main-data-store', 'data')
)
def update_temp_page(val_range, stored_data):
    if not stored_data: return px.scatter(), px.scatter()
    dff = pd.DataFrame(stored_data)
    dff = dff[(dff['sst'] >= val_range[0]) & (dff['sst'] <= val_range[1])]

    fig_map = px.scatter_map(dff, lat="latitude", lon="longitude", color="category", zoom=1,
                             map_style="open-street-map")
    fig_hist = px.histogram(dff, x="sst", color="category", title="Distribution by Temperature")
    return fig_map, fig_hist