from dash import html, dcc, Output, Input, State, callback
import plotly.express as px
import pandas as pd
from src.components.slider import slider
from src.components.scatter_map import scatter_map
from src.components.histogram import histogram

def layout_temperature(df):
    min_temp = df['sst'].min()
    max_temp = df['sst'].max()
    return html.Div([
    html.H2("Analysis by Water Temperature"),
    html.Label("Select Temperature Range (°C):"),

    html.Div([
        html.Label(f"Filter by temperature ({int(min_temp)}°C - {int(max_temp)}°C):"),
        slider(int(min_temp), int(max_temp) + 1, 0.5, 5, "temp-slider")
    ], style={'padding': '20px'}),

    html.Div([
        # Carte à gauche
        dcc.Graph(id='graph-temp-map', style={'width': '48%', 'display': 'inline-block'}),
        # Histogramme à droite
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
    fig_map = scatter_map(dff, f"Locations (Temp: {val_range[0]}°C - {val_range[1]}°C)", 'sst')
    fig_hist = histogram(dff, "sst", "Species Distribution by Temperature", {'sst': 'Temperature (°C)', 'count': 'Obs.'})
    fig_hist.update_yaxes(matches=None, showticklabels=True)
    fig_hist.update_xaxes(matches='x')
    fig_hist.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',  # Fond du graphique transparent
        paper_bgcolor='rgba(0,0,0,0)',  # Fond du papier transparent
        font_color='black'  # (Optionnel) assure que le texte reste lisible
    )
    return fig_map, fig_hist