from dash import Dash, html, dcc, Output, Input
import pandas as pd
import os
from pathlib import Path

from config import TAXON_CONFIG

from src.utils.clean_data import clean_data
from src.utils.get_data import get_data

from src.components.header import header

from src.pages.salinity import layout_salinity
from src.pages.shore_distance import layout_distance
from src.pages.species import layout_species
from src.pages.temperature import layout_temperature
from src.pages.depth import layout_depth

app = Dash(__name__, suppress_callback_exceptions=True)

app.title = "WhaLife"
data = {}
compiled_data = []
if not os.path.exists("data/cleaned"):
    os.makedirs("data/cleaned")

if not os.path.exists("data/raw"):
    os.makedirs("data/raw")

CLEANED_FILE = Path("data/cleaned/cleaned_data.csv")
RAW_DIR = Path("data/raw")
FALLBACK_CSV = Path("data/fallback_data.csv")

def load_data():
    if CLEANED_FILE.exists():
        print("✅ Loading clean data from disk...")
        return pd.read_csv(CLEANED_FILE)

    try:
        print("🌐 Clean data not found. Attempting to fetch from API...")
        RAW_DIR.mkdir(parents=True, exist_ok=True)
        CLEANED_FILE.parent.mkdir(parents=True, exist_ok=True)
        compiled_data = []

        for species, taxon_id in TAXON_CONFIG.items():
            results = get_data(taxon_id, 2500)["results"]
            df_species = pd.DataFrame(results)
            df_species.to_csv(RAW_DIR / f"{species}.csv", index=False)
            compiled_data.extend(results)

        raw_df = pd.DataFrame(compiled_data)
        df_final = clean_data(raw_df)

        CLEANED_FILE.parent.mkdir(parents=True, exist_ok=True)
        df_final.to_csv(CLEANED_FILE, index=False)
        return df_final

    except Exception as e:
        print(f"⚠️ Fetch failed (No internet or API error): {e}")
        if FALLBACK_CSV.exists():
            print(f"💾 Using local fallback: {FALLBACK_CSV}")
            fallback = pd.read_csv(FALLBACK_CSV, low_memory=False)
            return fallback
        else:
            print("❌ Error: No clean data, no internet, and no fallback data found.")
            return pd.DataFrame(
                columns=['category', 'bathymetry', 'sst', 'sss', 'shoredistance', 'latitude', 'longitude', 'year'])

df = load_data()

menu_button_style = {
    'backgroundColor': '#007bff', 'color': 'white', 'border': 'none',
    'borderRadius': '20px', 'padding': '10px 20px', 'cursor': 'pointer',
    'fontSize': '16px', 'fontWeight': 'bold'
}

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),

    dcc.Store(id='main-data-store', data=df.to_dict('records')),

    header(),

    html.Div([
        dcc.Link(html.Button('Species', style=menu_button_style), href='/'),
        dcc.Link(html.Button('Depth', style=menu_button_style), href='/depth', style={'marginLeft': '10px'}),
        dcc.Link(html.Button('Distance', style=menu_button_style), href='/distance', style={'marginLeft': '10px'}),
        dcc.Link(html.Button('Temperature', style=menu_button_style), href='/temperature',
                 style={'marginLeft': '10px'}),
        dcc.Link(html.Button('Salinity', style=menu_button_style), href='/salinity', style={'marginLeft': '10px'}),
    ], style={'textAlign': 'center', 'padding': '10px'}),

    html.Div(id='page-content')
])

@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)
def display_page(pathname):
    if pathname == '/depth':
        return layout_depth(df)
    elif pathname == '/distance':
        return layout_distance(df)
    elif pathname == '/temperature':
        return layout_temperature(df)
    elif pathname == '/salinity':
        return layout_salinity(df)
    else:
        return layout_species(df)

if __name__ == '__main__':
    app.run(debug=True)