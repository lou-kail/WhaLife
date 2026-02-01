from dash import html, dcc, Output, Input, State, callback
import plotly.express as px
import pandas as pd
from src.components.slider import slider
from src.components.scatter_map import scatter_map
from src.components.histogram import histogram

def layout_distance(df):
    max_dist_val = df['shoredistance'].quantile(0.98)
    max_dist = int(max_dist_val)
    step = max_dist // 5
    if step == 0: step = 1
    magnitude = 10 ** (len(str(step)) - 1)
    clean_step = round(step / magnitude) * magnitude
    if clean_step == 0: clean_step = step
    return html.Div([
    html.H2("Analysis by Distance to Coast"),
    html.Label("Select Distance:"),

    html.Div([
        html.Label(f"Filter by distance (0 - {max_dist} meters):"),
        slider(0, max_dist, "m", clean_step / 10, int(clean_step), "distance-slider")
    ], style={'padding': '20px'}),
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
    if not val_range:
        min_dist, max_dist = 0, dff['shoredistance'].max()
    else:
        min_dist, max_dist = val_range

    dff = dff[(dff['shoredistance'] >= val_range[0]) & (dff['shoredistance'] <= val_range[1])]
    fig_map = scatter_map(dff, f"Locations (Distance: {min_dist}m - {max_dist}m)", 'shoredistance')
    fig_hist = histogram(dff, "shoredistance","Species Distribution by Distance", {'shoredistance': 'Distance (m)', 'count': 'Obs.'})
    fig_hist.update_yaxes(matches=None, showticklabels=True)
    fig_hist.update_xaxes(matches='x')
    fig_hist.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',  # Fond du graphique transparent
        paper_bgcolor='rgba(0,0,0,0)',  # Fond du papier transparent
        font_color='black'  # (Optionnel) assure que le texte reste lisible
    )
    return fig_map, fig_hist