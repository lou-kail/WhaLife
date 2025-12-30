from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv')

app = Dash(__name__)

app.layout = html.Div([
    html.H1("Dashboard", style={'textAlign': 'center'}),
    dcc.Dropdown(df.country.unique(), 'Canada', id='dropdown-selection'),

    html.Div([
        dcc.Graph(id='graph-histogram', style={'width': '48%', 'display': 'inline-block'}),
        dcc.Graph(id='graph-map', style={'width': '48%', 'display': 'inline-block'})
    ])
])


@callback(
    Output('graph-histogram', 'figure'),
    Output('graph-map', 'figure'),
    Input('dropdown-selection', 'value')
)
def update_graphs(country_value):
    dff = df[df.country == country_value]

    fig_hist = px.bar(dff, x='year', y='pop', title=f"Population : {country_value}")

    fig_map = px.choropleth(
        dff,
        locations="country",
        locationmode="country names",
        color="lifeExp",
        title="Localisation"
    )

    return fig_hist, fig_map


if __name__ == '__main__':
    app.run(debug=True)