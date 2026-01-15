from dash import html

def header():
    #return html.H1("Dashboard", style={'textAlign': 'center'})
    return html.Div([
        html.Img(src='../images/LogoWhalife.png', alt='image'),
        html.H1("WhaLife", style={'textAlign': 'center'})
    ])