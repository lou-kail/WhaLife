from dash import html, dcc
from src.components.map import map_component
from src.components.histogram import histogram
from src.components.model_viewer import model_viewer

def layout_species(df):
        return html.Div([
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
            html.Div([model_viewer(f"/assets/{df['category'].unique()[0].lower().replace("%20","_")}.glb")]
            ,"model-viewer-container")
        ])
    ])
