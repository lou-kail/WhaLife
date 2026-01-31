from dash import html, dcc, Output, Input, State, callback
import plotly.express as px
import pandas as pd


def layout_salinity(df):
    min_sal = df['sss'].min()
    max_sal = df['sss'].max()

    return html.Div([
    html.H2("Analysis by Water Salinity"),
    html.Label("Select Salinity Range (g/L):"),

    html.Div([
        html.Label(f"Filter by salinity ({int(min_sal)}g/L - {int(max_sal)}g/L):"),
        dcc.RangeSlider(
            min=min_sal,
            max=max_sal, #int(max_sal) + 1,
            step=0.5,
            value=[min_sal, max_sal],
            marks={i: f'{i}g/L' for i in range(int(min_sal), int(max_sal) + 1, 5)},
            tooltip={"placement": "bottom", "always_visible": True},
            id='sal-slider'
        )
    ], style={'padding': '20px'}),

    html.Div([
        # Carte à gauche
        dcc.Graph(id='graph-sal-map', style={'width': '48%', 'display': 'inline-block'}),
        # Histogramme à droite
        dcc.Graph(id='graph-sal-hist', style={'width': '48%', 'display': 'inline-block', 'float': 'right'})
    ])
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

    fig_map = px.scatter_map(
        dff,
        lat="latitude",
        lon="longitude",
        color="category",
        size_max=15,
        zoom=1,
        map_style="open-street-map",
        title=f"Locations (Sal: {val_range[0]}g/L - {val_range[1]}g/L)",
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