from dash import html, dcc

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
