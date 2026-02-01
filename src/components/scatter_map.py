import plotly.express as px

def scatter_map(dff, title, hover_data):
    return px.scatter_map(
        dff,
        lat="latitude",
        lon="longitude",
        color="category",
        size_max=15,
        zoom=1,
        map_style="open-street-map",
        title=title,
        hover_data=[hover_data]
    )