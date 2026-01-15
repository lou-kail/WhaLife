from dash import html

def header():
    #return html.H1("Dashboard", style={'textAlign': 'center'})
    return html.Div([
        html.Img(src='/assets/LogoWhalife.png', alt='image', style={'height': '200px', 'width': '200px'}),
        html.H1("WhaLife", style={'fontFamily':'Gluten', 'fontSize':'4rem', 'textAlign': 'center', 'marginLeft' : '15px', 'marginTop' : '80px'})
        ],
        style={
            'display': 'flex',
            'alignItems': 'center',
            'justifyContent': 'center'
        }
    )