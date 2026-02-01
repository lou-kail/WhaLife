from dash import dcc

def slider(slider_min, slider_max, step, step_marks_depth, id_):
    return dcc.RangeSlider(
                min=slider_min,
                max=slider_max,
                step=step,
                value=[slider_min, slider_max],
                marks={i: f'{i}m' for i in range(int(slider_min), int(slider_max) + 1, step_marks_depth)},
                tooltip={"placement": "bottom", "always_visible": True},
                id=id_
            )