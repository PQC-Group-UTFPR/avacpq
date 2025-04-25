from dash import html, State
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from lattice_based.ggh.ggh import get_ggh_data
from dash.exceptions import PreventUpdate
import json

def blank_figure():
    fig = go.Figure(go.Scatter(x=[], y=[]))
    fig.update_layout(template="plotly_dark")
    return fig

def get_callbacks(app):
    # Callback para passo de geração de chaves
    @app.callback(
        [Output('visualization-results', 'figure'),
        Output('step-content', 'children'),
        Output('keygen-data', 'data')],
        [Input('start', 'n_clicks'),
         Input('btn-next', 'n_clicks')],
        [State('checklist-Algorithms', 'value'),
         State('keygen-data', 'data')],
        prevent_initial_call=True
    )
    def generate_keys(button_start, step, algorithm_selected,dados_carry):
        if button_start is None or not algorithm_selected:
            raise PreventUpdate
        
        last_selected = algorithm_selected[-1]
        if last_selected == 'GGH':
            return get_ggh_data(2, step, dados_carry)
        elif last_selected == 'LWE':
            return blank_figure(), html.Div("LWE selecionado"), json.dumps({})
        elif last_selected == 'Alkaline':
            return blank_figure(), html.Div("Alkaline selecionado"), json.dumps({})
    