from dash import html

def model_viewer(file_path):

    viewer_html = f'''
        <script type="module" src="/assets/model-viewer.min.js"></script>
        <style>body {{ margin: 0; background-color: #f4f4f4; }}</style>        
        <model-viewer 
            src="{file_path}" 
            style="width: 100vw; height: 100vh;" 
            camera-controls 
            auto-rotate>
        </model-viewer>
    '''

    return html.Iframe(
        srcDoc=viewer_html,
        style={
            'width': '100%',
            'height': '600px',
            'border': 'none'
        }
    )