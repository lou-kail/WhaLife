from dash import html, dcc, Output, Input, State, callback
import plotly.express as px
import pandas as pd


def layout_depth(df):
    max_depth = int(df['bathymetry'].max())
    step_marks_depth = max_depth // 5
    return html.Div([
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


@callback(
    Output('graph-depth-map', 'figure'),
    Output('graph-depth-hist', 'figure'),
    Input('depth-slider', 'value'),
    State('main-data-store', 'data')
)
def update_depth_page(val_range, stored_data):
    if not stored_data: return px.scatter(), px.histogram()
    dff = pd.DataFrame(stored_data)
    dff = dff[(dff['bathymetry'] >= val_range[0]) & (dff['bathymetry'] <= val_range[1])]

    fig_map = px.scatter_map(
        dff,
        lat="latitude",
        lon="longitude",
        color="category",
        size_max=15,
        zoom=1,
        map_style="open-street-map",
        title=f"Distribution by species (Depth: {val_range[0]}m to {val_range[1]}m)",
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