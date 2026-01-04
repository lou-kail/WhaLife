from dash import Dash, html, dcc, Output, Input
import plotly.express as px
import pandas as pd
import os
from pathlib import Path

from config import TAXON_IDS

from src.utils.clean_data import clean_data
from src.utils.get_data import get_data

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

# Page Espece
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

# Page Profondeur
max_depth = int(df['bathymetry'].max())
step_marks_depth = max_depth // 5

layout_depth = html.Div([
    html.H2("Analysis by Depth"),
    html.Label("Select Depth:"),

    html.Div([
        html.Label("Filter by depth (meters) :"),
        dcc.RangeSlider(
            min=df['bathymetry'].min(),
            max=df['bathymetry'].max(),
            step=50,
            value=[df['bathymetry'].min(), df['bathymetry'].max()],
            marks={i: f'{i}m' for i in range(0, max_depth + 1, step_marks_depth)},
            tooltip={"placement": "bottom", "always_visible": True},
            id='depth-slider'
        )
    ], style={'padding': '20px'}),
    html.Div([
        dcc.Graph(id='graph-depth-map', style={'width': '48%', 'display': 'inline-block'}),
        dcc.Graph(id='graph-depth-hist', style={'width': '48%', 'display': 'inline-block', 'float': 'right'})
    ])
])

# Page Distance des Cotes
max_dist_val = df['shoredistance'].quantile(0.98)
max_dist = int(max_dist_val)
step = max_dist // 5
if step == 0: step = 1
magnitude = 10 ** (len(str(step)) - 1)
clean_step = round(step / magnitude) * magnitude
if clean_step == 0: clean_step = step

layout_distance = html.Div([
    html.H2("Analysis by Distance to Coast"),
    html.Label("Select Distance:"),

    html.Div([
        html.Label(f"Filter by distance (0 - {max_dist} meters):"),
        dcc.RangeSlider(
            min=0,
            max=max_dist,
            step=clean_step / 10,  # Permet un ajustement fin
            value=[0, max_dist],
            # Génération des marques lisibles toutes les X étapes
            marks={i: f'{i}m' for i in range(0, max_dist + 1, int(clean_step))},
            tooltip={"placement": "bottom", "always_visible": True},
            id='distance-slider'
        )
    ], style={'padding': '20px'}),
    html.Div([
        dcc.Graph(id='graph-distance-map', style={'width': '48%', 'display': 'inline-block'}),
        dcc.Graph(id='graph-distance-hist', style={'width': '48%', 'display': 'inline-block', 'float': 'right'})
    ])
])

# Layout Principal
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    header(),
    html.Div([
        dcc.Link(html.Button('Species'), href='/'),
        dcc.Link(html.Button('Depth'), href='/depth', style={'marginLeft': '10px'}),
        dcc.Link(html.Button('Distance'), href='/distance', style={'marginLeft': '10px'}),
    ], style={'textAlign': 'center', 'padding': '10px'}),
    html.Div(id='page-content')
])


# --- Callbacks ---

@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/depth':
        return layout_depth
    elif pathname == '/distance':
        return layout_distance
    else:
        return layout_species


@app.callback(
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


@app.callback(
    Output('graph-depth-map', 'figure'),
    Output('graph-depth-hist', 'figure'),
    Input('depth-slider', 'value')
)
def update_depth(depth_range):
    if not depth_range: return px.scatter(), px.histogram()  # Sécurité

    min_depth, max_depth = depth_range
    dff = df[(df['bathymetry'] >= min_depth) & (df['bathymetry'] <= max_depth)]

    fig_map = px.scatter_map(
        dff,
        lat="latitude",
        lon="longitude",
        color="category",
        size_max=15,
        zoom=1,
        map_style="open-street-map",
        title=f"Distribution by species (Depth: {min_depth}m to {max_depth}m)",
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
    return fig_map, fig_hist


@app.callback(
    Output('graph-distance-map', 'figure'),
    Output('graph-distance-hist', 'figure'),
    Input('distance-slider', 'value')
)
def update_distance(distance_range):
    if not distance_range:
        min_dist, max_dist = 0, df['shoredistance'].max()
    else:
        min_dist, max_dist = distance_range
    dff = df[(df['shoredistance'] >= min_dist) & (df['shoredistance'] <= max_dist)]
    fig_map = px.scatter_map(
        dff,
        lat="latitude",
        lon="longitude",
        color="category",
        size_max=15,
        zoom=1,
        map_style="open-street-map",
        title=f"Locations (Distance: {min_dist}m - {max_dist}m)",
        hover_data=['shoredistance']
    )
    fig_hist = px.histogram(
        dff,
        x="shoredistance",
        color="category",
        facet_col="category",
        facet_col_wrap=2,
        title="Species Distribution by Distance",
        labels={'shoredistance': 'Distance (m)', 'count': 'Obs.'},
        nbins=20
    )
    fig_hist.update_yaxes(matches=None, showticklabels=True)
    fig_hist.update_xaxes(matches='x')

    return fig_map, fig_hist


if __name__ == '__main__':
    app.run(debug=True)