from dash import Dash, html, dcc, page_container
import os
from callbacks import get_callbacks 
from components.Header import create_header

app = Dash(
    __name__,
    use_pages=True,
    prevent_initial_callbacks=False,
    assets_folder='assets',
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)


app.title = "AVACPQ: Artifícios Visuais para Aprendizado de Criptografia Pós-Quântica"
app.config.suppress_callback_exceptions = True
get_callbacks(app)
app.layout = html.Div(
    className="app-container",
    children=[
        create_header(), 
        
        page_container
    ]
)


if __name__ == '__main__':
    app.run(debug=True, dev_tools_hot_reload=True)