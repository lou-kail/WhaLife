from dash import html, dcc, Output, Input, State, callback
import plotly.express as px
import pandas as pd
from src.components.model_viewer import model_viewer
from src.components.map import map_component
from src.components.histogram import histogram


def layout_species(df):
    return html.Div([
        html.H2("Analysis by Species"),
        html.Label("Select Species:"),
        dcc.Dropdown(
            id='species-selection',
            options=[{'label': i, 'value': i} for i in sorted(df['category'].unique())],
            value=sorted(df['category'].unique())[0]
        ),
        html.Div([
            histogram(),
            map_component(),
            html.Div(id="model-viewer-container")
        ])
    ])


@callback(
    Output('graph-histogram', 'figure'),
    Output('graph-map', 'figure'),
    Output('model-viewer-container', 'children'),
    Input('species-selection', 'value'),
    State('main-data-store', 'data')
)
def update_species_page(selected_category, stored_data):
    if not stored_data: return px.scatter(), px.scatter(), ""

    dff = pd.DataFrame(stored_data)
    dff = dff[dff['category'] == selected_category]

    fig_hist = px.histogram(dff, x='year', title=f"Observations: {selected_category}")
    fig_map = px.scatter_map(dff, lat="latitude", lon="longitude", zoom=1, map_style="open-street-map")

    clean_name = selected_category.lower().replace(" ", "_").replace("%20", "_")
    new_model = html.Div(
        model_viewer(f"/assets/{clean_name}.glb"),
        key=f"model-{clean_name}"
    )

    return fig_hist, fig_map, new_model