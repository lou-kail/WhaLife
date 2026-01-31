from dash import html, dcc

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