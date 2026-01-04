from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import os
from pathlib import Path

from config import TAXON_IDS

# Data Handling Utils

from src.utils.clean_data import clean_data
from src.utils.get_data import get_data

# Components

from src.components.header import header
from src.components.map import map_component
from src.components.histogram import histogram
from src.components.model_viewer import model_viewer

app = Dash(__name__, suppress_callback_exceptions=True)

data = {}
compiled_data = []

if not os.path.exists("data/cleaned"):
    os.makedirs("data/cleaned")

if not os.path.exists("data/raw"):
    os.makedirs("data/raw")

CLEANED_FILE = Path("data/cleaned/cleaned_data.csv")
RAW_DIR = Path("data/raw")

if CLEANED_FILE.exists():
    print("Loading clean data from disk...")
    df = pd.read_csv(CLEANED_FILE)
else:
    print("Clean data file not found. Fetching and cleaning data...")
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    CLEANED_FILE.parent.mkdir(parents=True, exist_ok=True)

    compiled_data = []
    for species, taxon_id in TAXON_IDS.items():
        results = get_data(taxon_id, 2500)["results"]
        df_species = pd.DataFrame(results)

        df_species.to_csv(RAW_DIR / f"{species}.csv", index=False)
        compiled_data.extend(results)

    raw_df = pd.DataFrame(compiled_data)
    raw_df.to_csv(RAW_DIR / "compiled_data.csv", index=False)

    df = clean_data(raw_df)
    df.to_csv(CLEANED_FILE, index=False)

#Page pour les espèces
layout_species = html.Div([
    html.H2("Analysis by Species"),
    html.Label("Select Species to Analyze:"),
    dcc.Dropdown(
        options=[{'label': i, 'value': i} for i in df['category'].unique()],
        value=df['category'].unique()[0],
        id='species-selection'
    ),
    html.Div([
        histogram(),
        map_component(),
        model_viewer("/assets/dolphin.glb")
    ])
])

#Page profondeur
layout_depth = html.Div([
    html.H2("Analysis by Depth"),
    html.Label("Select Depth:"),

    html.Div([
        html.Label("Filtrer par profondeur (mètres) :"),
        dcc.RangeSlider(
            min=df['bathymetry'].min(),
            max=df['bathymetry'].max(),
            step=50,
            value=[df['bathymetry'].min(), df['bathymetry'].max()],
            marks={int(i): str(int(i)) for i in range(int(df['bathymetry'].min()), int(df['bathymetry'].max()), 1000)},
            id='depth-slider'
        )
    ], style={'padding': '20px'}),
    dcc.Graph(id='graph-depth-map')
])

#Principale
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    header(),
    html.Div([
        dcc.Link(html.Button('Species'), href='/'),
        dcc.Link(html.Button('Depth'), href='/depth', style={'marginLeft': '10px'}),
    ], style={'textAlign': 'center', 'padding': '10px'}),
    html.Div(id='page-content')
])

@callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/depth':
        return layout_depth
    else:
        return layout_species

@callback(
    Output('graph-histogram', 'figure'),
    Output('graph-map', 'figure'),
    Input('species-selection', 'value')
)
def update_graphs(selected_category):
    dff = df[df['category'] == selected_category]

    print(f"Selected: {selected_category} | Rows found: {len(dff)}")

    if dff.empty:
        return px.scatter(title="No data found"), px.scatter_map(title="No data found")

    fig_hist = px.histogram(dff, x='year', title=f"Observations: {selected_category}")

    fig_map = px.scatter_map(
        dff,
        lat="latitude",
        lon="longitude",
        map_style="open-street-map",
        zoom=1,
        title=f"Locations: {selected_category}"
    )
    return fig_hist, fig_map


@callback(
    Output('graph-depth-map', 'figure'),
    Input('depth-slider', 'value')
)
def update_depth_map(depth_range):
    min_depth, max_depth = depth_range
    dff = df[(df['bathymetry'] >= min_depth) & (df['bathymetry'] <= max_depth)]
    fig = px.scatter_map(
        dff,
        lat="latitude",
        lon="longitude",
        color="category",
        size_max=15,
        zoom=1,
        map_style="open-street-map",
        title=f"Distribution by species (Depth: {min_depth}m to {max_depth}m)"
    )
    return fig

if __name__ == '__main__':
    app.run(debug=True)