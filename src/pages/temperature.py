from dash import html, dcc

def layout_temperature(df):
    min_temp = df['sst'].min()
    max_temp = df['sst'].max()
    return html.Div([
        html.H2("Analysis by Water Temperature"),
        html.Label("Select Temperature Range (°C):"),

        html.Div([
            html.Label(f"Filter by temperature ({int(min_temp)}°C - {int(max_temp)}°C):"),
            dcc.RangeSlider(
                min=int(min_temp),
                max=int(max_temp) + 1,
                step=0.5,
                value=[int(min_temp), int(max_temp)],
                marks={i: f'{i}°C' for i in range(int(min_temp), int(max_temp) + 1, 5)},
                tooltip={"placement": "bottom", "always_visible": True},
                id='temp-slider'
            )
        ], style={'padding': '20px'}),

        html.Div([
            # Carte à gauche
            dcc.Graph(id='graph-temp-map', style={'width': '48%', 'display': 'inline-block'}),
            # Histogramme à droite
            dcc.Graph(id='graph-temp-hist', style={'width': '48%', 'display': 'inline-block', 'float': 'right'})
        ])
    ])


