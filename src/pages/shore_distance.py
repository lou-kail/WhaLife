from dash import html, dcc

def layout_distance(df):
    max_dist_val = df['shoredistance'].quantile(0.98)
    max_dist = int(max_dist_val)
    step = max_dist // 5
    if step == 0: step = 1
    magnitude = 10 ** (len(str(step)) - 1)
    clean_step = round(step / magnitude) * magnitude
    if clean_step == 0: clean_step = step

    return html.Div([
        html.H2("Analysis by Distance to Coast"),
        html.Label("Select Distance:"),

        html.Div([
            html.Label(f"Filter by distance (0 - {max_dist} meters):"),
            dcc.RangeSlider(
                min=0,
                max=max_dist,
                step=clean_step / 10,
                value=[0, max_dist],
                marks={i: f'{i}m' for i in range(0, max_dist + 1, int(clean_step))},
                tooltip={"placement": "bottom", "always_visible": True},
                id='distance-slider'
            )
        ], style={'padding': '20px'}),
        html.Div([
            dcc.Graph(id='graph-distance-map', style={'width': '48%', 'display': 'inline-block'}),
            dcc.Graph(id='graph-distance-hist', style={'width': '48%', 'display': 'inline-block', 'float': 'right'})
        ])
    ])
