from dash import html, dcc, Output, Input, State, callback
import plotly.express as px
import pandas as pd
from src.components.model_viewer import model_viewer
from src.components.map import map_component
from src.components.histogram import histogram
from config import SPECIES_INFO

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
            html.Div([
                html.Div(
                    id='model-viewer-container',
                    children=[model_viewer(f"/assets/{df['category'].unique()[0].lower().replace(' ', '_')}.glb")],
                    style={'flex': '1', 'padding': '10px'}  # flex: 1 prend 50% de l'espace
                ),
                html.Div([
                    html.H3("Description", style={'marginTop': '0'}),
                    html.Div(
                        id='species-description',
                        children=SPECIES_INFO.get(df['category'].unique()[0], "Description non disponible."),
                        style={'fontSize': '1.1em', 'lineHeight': '1.6', 'textAlign': 'justify'}
                    )
                ], style={'flex': '1', 'padding': '20px', 'backgroundColor': '#f8f9fa', 'borderRadius': '10px'})

            ], style={'display': 'flex', 'flexDirection': 'row', 'alignItems': 'center', 'margin': '20px 0'})
        ])
    ])


@callback(
    Output('graph-histogram', 'figure'),
    Output('graph-map', 'figure'),
    Output('model-viewer-container', 'children'),
    Output('species-description', 'children'),
    Input('species-selection', 'value'),
    State('main-data-store', 'data')
)
def update_species_page(selected_category, stored_data):
    if not stored_data: return px.scatter(), px.scatter(), ""

    dff = pd.DataFrame(stored_data)
    dff = dff[dff['category'] == selected_category]
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
    new_model = model_viewer(f"/assets/{selected_category.lower().replace("%20", "_").replace(" ", "_")}.glb")
    description_text = SPECIES_INFO.get(selected_category, "Description non disponible.")
    return fig_hist, fig_map, new_model, description_text
