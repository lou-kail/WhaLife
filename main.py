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

if CLEANED_FILE.exists():
    print("Loading clean data from disk...")
    df = pd.read_csv(CLEANED_FILE)
else:
    print("Clean data file not found. Fetching and cleaning data...")
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    CLEANED_FILE.parent.mkdir(parents=True, exist_ok=True)

    compiled_data = []
    for species, taxon_id in TAXON_CONFIG.items():
        results = get_data(taxon_id, 2500)["results"]
        df_species = pd.DataFrame(results)

        df_species.to_csv(RAW_DIR / f"{species}.csv", index=False)
        compiled_data.extend(results)

    raw_df = pd.DataFrame(compiled_data)
    raw_df.to_csv(RAW_DIR / "compiled_data.csv", index=False)

    df = clean_data(raw_df)
    df.to_csv(CLEANED_FILE, index=False)

menu_button_style = {
    'backgroundColor': '#007bff', 'color': 'white', 'border': 'none',
    'borderRadius': '20px', 'padding': '10px 20px', 'cursor': 'pointer',
    'fontSize': '16px', 'fontWeight': 'bold'
}

<<<<<<< HEAD
SPECIES_INFO = {
    "Humpback Whale": (
        "The humpback whale (Megaptera novaeangliae) is a large baleen whale known for its spectacular breaches "
        "and long, complex songs produced mainly by males during the breeding season. "
        "These songs typically last between 5 and 20 minutes and are repeated in sequences that can carry over tens "
        "of kilometers through the water. "
        "Humpback whales undertake extensive annual migrations between cold, nutrient‑rich feeding grounds in "
        "temperate or polar waters and warm tropical or subtropical breeding areas, often traveling thousands of "
        "kilometers each year. "
        "They feed primarily on small schooling prey such as krill and small fish, using techniques like bubble‑net "
        "feeding in which groups cooperate to trap prey in rising curtains of bubbles. "
        "Despite their massive size, humpbacks are generally considered gentle giants and play an important role in "
        "marine ecosystems by redistributing nutrients through their movements and feeding behavior. "
    ),

    "Blue Whale": (
        "The blue whale (Balaenoptera musculus) is the largest animal known to have ever lived, with adults commonly "
        "reaching 25–30 meters in length and weighing well over 100 tons. "
        "Blue whales are baleen whales and feed almost exclusively on tiny crustaceans called krill, which they filter "
        "from seawater using hundreds of baleen plates suspended from the upper jaw. "
        "During feeding seasons in cold polar or subpolar waters, a single individual can consume several tons of krill "
        "per day through powerful lunge‑feeding dives that may exceed 200 meters in depth. "
        "Most populations migrate between high‑latitude summer feeding grounds and lower‑latitude winter breeding areas, "
        "though some individuals show more flexible or partial migration patterns. "
        "Blue whales communicate using extremely low‑frequency vocalizations that can travel over vast distances in the "
        "ocean, and all recognized subspecies are currently considered endangered due to historical commercial whaling "
        "and ongoing human‑related threats. "
    ),

    "Orca": (
        "The orca or killer whale (Orcinus orca) is the largest member of the dolphin family and an apex predator found "
        "in all the world’s oceans, from polar seas to temperate and some tropical regions. "
        "Orcas live in highly social, matrilineal family groups called pods, often composed of multiple generations led "
        "by an older female, and these pods can form larger social structures such as clans and communities. "
        "Different populations specialize in distinct types of prey, ranging from fish and squid to seals, sharks, and even "
        "large whales, and they use coordinated hunting strategies that require precise communication and cooperation. "
        "Each pod has a characteristic set of vocalizations or dialect, consisting of clicks, whistles, and pulsed calls, " 
        "which function in both communication and echolocation and are culturally transmitted across generations. "
        "Because of their intelligence, complex social behavior, and top‑predator role, orcas are considered key indicators "
        "of the health and balance of marine ecosystems. "
    ),

    "Dolphin": (
        "Dolphins are highly intelligent toothed whales (odontocetes) that inhabit coastal and offshore waters worldwide, "
        "with species adapted to a broad variety of marine and, in some cases, freshwater environments. "
        "They live in social groups called pods, which can range from a few individuals to large, dynamic communities, and "
        "they engage in complex social behaviors such as cooperative hunting, play, and providing care to injured or sick "
        "members of their group."
        "Dolphins communicate using a rich repertoire of clicks, whistles, and body movements, and many species show evidence "
        "of individual “signature whistles” that function somewhat like names."
        "They use echolocation by emitting focused click sounds and interpreting returning echoes to detect prey, navigate in "
        "murky waters, and investigate objects with remarkable precision. "
        "Numerous studies highlight their advanced problem‑solving skills, cultural traditions, and capacity for innovation, "
        "which make dolphins a model group for research on animal cognition and social learning. "
    )
}

# Layout Principal
=======
>>>>>>> 749188d (feat(pages): fully modularized pages (layout + callback) added store logic (client cache))
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
<<<<<<< HEAD
        return species


@app.callback(
    Output('graph-histogram', 'figure'),
    Output('graph-map', 'figure'),
    Output('model-viewer-container', 'children'),
    Output('species-description', 'children'),
    Input('species-selection', 'value')
)
def update_graphs(selected_category):
    dff = df[df['category'] == selected_category].copy()

    dff = dff.dropna(subset=['year'])
    dff['year'] = dff['year'].astype(int)

    dff_counts = dff.groupby('year').size().reset_index(name='counts')
    dff_counts = dff_counts.sort_values('year')

    print(f"Selected: {selected_category} | Rows found: {len(dff)}")

    if dff.empty:
        return px.scatter(title="Pas de données"), px.scatter_map(title="Pas de données"), ""

    fig_hist = px.bar(
        dff_counts,
        x=dff_counts['year'].astype(str),
        y='counts',
        color='year',
        title=f"Observations: {selected_category}",
        color_continuous_scale='Blues'
    )

    fig_hist.update_traces(
        marker_line_width=0,
        opacity=1
    )

    fig_hist.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        bargap=0.1,
        yaxis_title="Nombre d'observations",
        xaxis_title=None,
        coloraxis_showscale=False,
        xaxis={'type': 'category'}
    )
    fig_map = px.scatter_map(
        dff,
        lat="latitude",
        lon="longitude",
        map_style="open-street-map",
        zoom=1,
        title=f"Locations: {selected_category}"
    )
    new_model = model_viewer(f"/assets/{selected_category.lower().replace("%20","_").replace(" ","_")}.glb")
    description_text = SPECIES_INFO.get(selected_category, "Description non disponible.")
    return fig_hist, fig_map, new_model, description_text


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
    fig_hist.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',  # Fond du graphique transparent
        paper_bgcolor='rgba(0,0,0,0)',  # Fond du papier transparent
        font_color='black'  # (Optionnel) assure que le texte reste lisible
    )
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
    fig_hist.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',  # Fond du graphique transparent
        paper_bgcolor='rgba(0,0,0,0)',  # Fond du papier transparent
        font_color='black'  # (Optionnel) assure que le texte reste lisible
    )
    return fig_map, fig_hist

@app.callback(
    Output('graph-temp-map', 'figure'),
    Output('graph-temp-hist', 'figure'),
    Input('temp-slider', 'value')
)
def update_temperature(temp_range):
    if not temp_range:
        current_min, current_max = min_temp, max_temp
    else:
        current_min, current_max = temp_range

    dff = df[(df['sst'] >= current_min) & (df['sst'] <= current_max)]

    fig_map = px.scatter_map(
        dff,
        lat="latitude",
        lon="longitude",
        color="category",
        size_max=15,
        zoom=1,
        map_style="open-street-map",
        title=f"Locations (Temp: {current_min}°C - {current_max}°C)",
        hover_data=['sst']
    )
    fig_hist = px.histogram(
        dff,
        x="sst",
        color="category",
        facet_col="category",
        facet_col_wrap=2,
        title="Species Distribution by Temperature",
        labels={'sst': 'Temperature (°C)', 'count': 'Obs.'},
        nbins=20
    )
    fig_hist.update_yaxes(matches=None, showticklabels=True)
    fig_hist.update_xaxes(matches='x')
    fig_hist.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',  # Fond du graphique transparent
        paper_bgcolor='rgba(0,0,0,0)',  # Fond du papier transparent
        font_color='black'  # (Optionnel) assure que le texte reste lisible
    )
    return fig_map, fig_hist

@app.callback(
    Output('graph-sal-map', 'figure'),
    Output('graph-sal-hist', 'figure'),
    Input('sal-slider', 'value')
)
def update_salinity(sal_range):
    if not sal_range:
        current_min, current_max = min_sal, max_sal
    else:
        current_min, current_max = sal_range

    dff = df[(df['sss'] >= current_min) & (df['sss'] <= current_max)]

    fig_map = px.scatter_map(
        dff,
        lat="latitude",
        lon="longitude",
        color="category",
        size_max=15,
        zoom=1,
        map_style="open-street-map",
        title=f"Locations (Sal: {current_min}g/L - {current_max}g/L)",
        hover_data=['sss']
    )
    fig_hist = px.histogram(
        dff,
        x="sss",
        color="category",
        facet_col="category",
        facet_col_wrap=2,
        title="Species Distribution by Salinity",
        labels={'sss': 'Salinity (g/L)', 'count': 'Obs.'},
        nbins=20
    )
    fig_hist.update_yaxes(matches=None, showticklabels=True)
    fig_hist.update_xaxes(matches='x')
    fig_hist.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',  # Fond du graphique transparent
        paper_bgcolor='rgba(0,0,0,0)',  # Fond du papier transparent
        font_color='black'  # (Optionnel) assure que le texte reste lisible
    )
    return fig_map, fig_hist
=======
        return layout_species(df)
>>>>>>> 749188d (feat(pages): fully modularized pages (layout + callback) added store logic (client cache))

if __name__ == '__main__':
    app.run(debug=True)