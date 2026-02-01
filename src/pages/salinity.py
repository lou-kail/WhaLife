from dash import html, dcc, Output, Input, State, callback
import plotly.express as px
import pandas as pd
from src.components.slider import slider
from src.components.scatter_map import scatter_map
from src.components.histogram import histogram

def layout_salinity(df):
    min_sal = df['sss'].min()
    max_sal = df['sss'].max()

    return html.Div([
    html.H2("Analysis by Water Salinity"),
    html.Label("Select Salinity Range (g/L):"),

    html.Div([
        html.Label(f"Filter by salinity ({int(min_sal)}g/L - {int(max_sal)}g/L):"),
        slider(min_sal, max_sal, "g/L", 0.5, 5, "sal-slider")
    ], style={'padding': '20px'}),
        dcc.Loading(
            id="loading-salinity",
            type="circle",
            color="#007bff",
            children=html.Div([
            # Carte à gauche
            dcc.Graph(id='graph-sal-map', style={'width': '48%', 'display': 'inline-block'}),
            # Histogramme à droite
            dcc.Graph(id='graph-sal-hist', style={'width': '48%', 'display': 'inline-block', 'float': 'right'})
            ])
        )
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

    fig_map = scatter_map(dff, f"Locations (Sal: {val_range[0]}g/L - {val_range[1]}g/L)", 'sss')
    fig_hist = histogram(dff, 'sss', "Species Distribution by Salinity", {'sss': 'Salinity (g/L)', 'count': 'Obs.'})
    fig_hist.update_yaxes(matches=None, showticklabels=True)
    fig_hist.update_xaxes(matches='x')
    fig_hist.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',  # Fond du graphique transparent
        paper_bgcolor='rgba(0,0,0,0)',  # Fond du papier transparent
        font_color='black'  # (Optionnel) assure que le texte reste lisible
    )
    return fig_map, fig_hist