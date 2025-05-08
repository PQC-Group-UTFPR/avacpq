from dash import html, State
import plotly.graph_objects as go
import numpy as np
from dash.dependencies import Input, Output
from lattice_based.ggh.ggh import initGGH, get_ggh_data, ggh_encrypt, ggh_decrypt
from dash.exceptions import PreventUpdate
import json

def blank_figure():
    fig = go.Figure(go.Scatter(x=[], y=[]))
    fig.update_layout(template="plotly_dark")
    return fig

def get_callbacks(app):
    # Callback para passo qualquer processo
    @app.callback(
        [Output('visualization-results', 'figure',allow_duplicate=True),
         Output('keygen-data', 'data'), 
         Output('btn-next', 'disabled')],
         Input('start', 'n_clicks'),
        [State('checklist-Algorithms', 'value'),
         State('keygen-data', 'data')],
        prevent_initial_call=True
    )
    def generate_keys(button_start, algorithm_selected, dados_carry):
        if button_start is None or not algorithm_selected:
            raise PreventUpdate

        last_selected = algorithm_selected[-1]
        # Deixar ou não?
        if last_selected == 'GGH':
            if dados_carry is None:
                dados_carry = initGGH(dados_carry, 2)
                return blank_figure(), json.dumps(dados_carry), False

        elif last_selected == 'LWE':
            return blank_figure(), json.dumps({}), True
        elif last_selected == 'Alkaline':
            return blank_figure(), json.dumps({})
        return blank_figure(), json.dumps({'error': 'Algoritmo não reconhecido'}), True

        
    @app.callback(
        [Output('visualization-results', 'figure'),
         Output('step-content', 'children')],
         Input('btn-next', 'n_clicks'),
         State('keygen-data', 'data'),
        prevent_initial_call=True
        )
    def Process_sign(step,dados_carry):
            if isinstance(dados_carry, str):
                dados_carry = json.loads(dados_carry)

            algorithm = dados_carry.get('algorithm', '')
            if algorithm == 'GGH':
                if step < 5: 
                    return get_ggh_data(step, dados_carry)
                elif step < 8:
                    return ggh_encrypt(dados_carry, step)
                else:
                    return ggh_decrypt(dados_carry,step)
            elif algorithm == 'LWE':
                return blank_figure(), html.Div("LWE selecionado")
            elif algorithm == 'Alkaline':
                return blank_figure(), html.Div("Alkaline selecionado")
            return blank_figure(), html.Div("Algoritmo desconhecido")

            
