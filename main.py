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

app = Dash(__name__)

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

app.layout = html.Div([
    header(),
    html.Label("Select Species to Analyze:"),
    dcc.Dropdown(
        options=[{'label': i, 'value': i} for i in df['category'].unique()],
        value=df['category'].unique()[0],
        id='species-selection'
    ),

    html.Div([
        histogram(),
        map_component()
    ])
])


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


if __name__ == '__main__':
    app.run(debug=True)