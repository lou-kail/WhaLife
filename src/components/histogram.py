import plotly.express as px

def histogram(dff, x, title, labels):
    return px.histogram(
        dff,
        x=x,
        color="category",
        facet_col="category",
        facet_col_wrap=2,
        title=title,
        labels=labels,
        nbins=20
    )