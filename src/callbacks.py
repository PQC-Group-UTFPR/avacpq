from dash import html, State, dcc, callback, no_update
import plotly.graph_objects as go
import numpy as np
from dash.dependencies import Input, Output
from lattice_based.ggh.ggh import initGGH, get_ggh_data, ggh_encrypt, ggh_decrypt
from dash.exceptions import PreventUpdate
import json


def blank_figure():
    fig = go.Figure(go.Scatter(x=[], y=[]))
    fig.update_layout(template="none", 
            paper_bgcolor="black", 
            plot_bgcolor="black",)
    return fig

def get_callbacks(app):
    # Callback para passo qualquer processo
    @app.callback(
        [Output('visualization-results', 'style'),
         Output('keygen-data', 'data', allow_duplicate=True), 
         Output('btn-next', 'disabled', allow_duplicate=True),
         Output('start', 'disabled', allow_duplicate=True)],
         Input('start', 'n_clicks'),
        [State('checklist-Algorithms', 'value'),
         State('keygen-data', 'data'),
         State('algorithm-dimension', 'value')],
        prevent_initial_call=True,
        allow_duplicate = True
    )
    def generate_keys(button_start, algorithm_selected, dados_carry, dimension):
        if button_start is None or not algorithm_selected:
            raise PreventUpdate
        
        last_selected = algorithm_selected[-1]
        # Deixar ou não?
        if last_selected == 'GGH':
            if dados_carry is None:
                dados_carry = initGGH(dados_carry, dimension)
                style = {"display": "block"}
                return style, json.dumps(dados_carry), False, True

        elif last_selected == 'LWE':
            return {"display": "none"}, json.dumps({}), True, False
        elif last_selected == 'Alkaline':
            return {"display": "none"}, json.dumps({}), True, False
        return {"display": "none"}, json.dumps({'error': 'Algoritmo não reconhecido'}), True

    @app.callback(
         [Output('visualization-results', 'children', allow_duplicate=True),
         Output('step-content', 'children', allow_duplicate=True)],
         Input('btn-next', 'n_clicks'),
         State('keygen-data', 'data'),
        prevent_initial_call=True
        )
    def Process_sign(step,dados_carry):
            if dados_carry is None:
                raise PreventUpdate
            if isinstance(dados_carry, str):
                dados_carry = json.loads(dados_carry)

            algorithm = dados_carry.get('algorithm', '')
            if algorithm == 'GGH':
                if step < 4: 
                    return get_ggh_data(step, dados_carry)
                elif step < 7:
                    return ggh_encrypt(dados_carry, step)
                else:
                    return ggh_decrypt(dados_carry,step)
            elif algorithm == 'LWE':
                return blank_figure(), html.Div("LWE selecionado")
            elif algorithm == 'Alkaline':
                return blank_figure(), html.Div("Alkaline selecionado")
            return blank_figure(), html.Div("Algoritmo desconhecido")
    
    # Dimension input
    @app.callback(
    Output('dimension-input-container', 'children'),
    Input('checklist-Algorithms', 'value'),
    prevent_initial_call=True
    )
    def show_dimension_input(algorithms_selected):
        if not algorithms_selected:
            return ''

        return html.Div([
            html.Label("Dimensão (n):"),
            dcc.Input(
                id='algorithm-dimension',
                type='number',
                min=2,
                step=1,
                value=2
            )
        ])

   
    # Reset data
    @app.callback(
    [Output('visualization-results', 'style', allow_duplicate=True),
     Output('step-content', 'children', allow_duplicate=True),
     Output('keygen-data', 'data', allow_duplicate=True),
     Output('btn-next', 'n_clicks', allow_duplicate=True),
     Output('btn-next', 'disabled'),
     Output('start', 'disabled', allow_duplicate=True),
     Output('checklist-Algorithms', 'value') ],
     Input('reset-btn', 'n_clicks'),
     prevent_initial_call=True
    )
    def ResetSystem(clicks):
        if clicks:            
            return {"display": "none"}, '', None, 0, True,False,[]

#     # Login button callback
#     @app.callback(
#     Output('login-button-container', 'children'),
#     Input('login-button', 'n_clicks'),
#     prevent_initial_call=True
# )
#     def login_button_click(n_clicks):
#         if n_clicks and n_clicks > 0:
#             return dcc.Location(pathname='/login', id='login-redirect')
        
#         return no_update
        

                
    
 

            
