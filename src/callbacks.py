from dash import html, State, dcc, callback, no_update
import plotly.graph_objects as go
import numpy as np
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import json
from flask_login import current_user
from lattice_based.algorithms import BaseAlgorithm
from lattice_reduction.methods import LatticeBasedMethod

# Graph with no data
def blank_figure():
    fig = go.Figure(go.Scatter(x=[], y=[]))
    fig.update_layout(template="none", 
            paper_bgcolor="black", 
            plot_bgcolor="black",)
    return fig
# Function to return a message when an algorithm/ method is not supported
def not_supported(algorithm_selected):
    return (  html.Div(className = "not-supported",
                       children = [
                        html.H3(f"Algoritmo '{algorithm_selected}' ainda não suportado."),
                        html.P("Em breve, este algoritmo estará disponível para visualização.")
                    ]),
                    None,
                    True,
                    False)

def get_callbacks(app):

    # Handles the initialization of the algorithm or method based on user selection.
    # It updates the 'visualization-results' with a blank figure and initializes 'dados_carry'
    # with the selected algorithm or method's data.
    # If no algorithm or method is selected, it returns a message
    # indicating that the selection is invalid.
    @app.callback(
        [Output('visualization-results', 'children'),
        Output('keygen-data', 'data', allow_duplicate=True), 
        Output('btn-next', 'disabled', allow_duplicate=True),
        Output('start', 'disabled', allow_duplicate=True)],
        Input('start', 'n_clicks'),
        [State('checklist-Algorithms', 'value'),
        State('checklist-Methods', 'value'),
        State('keygen-data', 'data'),
        State('algorithm-dimension', 'value')],
        prevent_initial_call=True,
        allow_duplicate=True
        )
    def generate_data(n_clicks, algorithm_selected, method_selected, dados_carry, dimension):
        if n_clicks is None:
            raise PreventUpdate

        if algorithm_selected:
            algorithm = BaseAlgorithm.get_algorithm_by_name(algorithm_selected, dimension)
            if algorithm:
                # Dados_carry is a dictionary of data
                # Is essential the field ('algorithm' or 'method') and 'dimension' to be present
                dados_carry = algorithm.initialize(dimension)
                return '', json.dumps(dados_carry), False, True
            else:
                return not_supported(algorithm_selected)

        if method_selected:
            method = LatticeBasedMethod.get_method_by_name(method_selected, dimension)
            if method:
                dados_carry = method.initialize(dimension)
                return '', json.dumps(dados_carry), False, True
            else:
                return not_supported(method_selected)

        return '', None, True, False

    # Handles the step-by-step execution of the algorithm demonstration.
    # On each step, this callback:
    # 1. Processes the main data ('dados_carry') based on the algorithm and step number.
    # 2. Updates the 'visualization-results' with a graph or text.
    # 3. Updates the 'step-content' with a description of the current action.
    @app.callback(
         [Output('visualization-results', 'children', allow_duplicate=True),
         Output('step-content', 'children', allow_duplicate=True),
         Output('btn-next', 'n_clicks', allow_duplicate=True)],
         Input('btn-next', 'n_clicks'),
         State('keygen-data', 'data'),
        prevent_initial_call=True
        )
    def Process_sign(step,dados_carry):
            if dados_carry is None:
                raise PreventUpdate
            if isinstance(dados_carry, str):
                dados_carry = json.loads(dados_carry)

            dimension = dados_carry.get('dimension', 2)
            if dados_carry.get('algorithm', ''):
                algorithm_name = dados_carry.get('algorithm', '')
                algorithm_instance = BaseAlgorithm.get_algorithm_by_name(algorithm_name, dimension)
            else:
                method_name = dados_carry.get('method','')
                method_instance = LatticeBasedMethod.get_method_by_name(method_name, dimension)

            # With the algorithm/method name selected, we can process the step
            # Entire process is done in the algorithm/method class
            # The result of function process_step is a tuple 
            # with the figure and the step description
            if algorithm_instance:
                result = algorithm_instance.process_step(step, dados_carry)
                max_step = algorithm_instance.get_max_steps()
                if step >= max_step:
                    return result[0], result[1], 0
                else:
                    return result[0], result[1], step
            elif method_instance:
                result = method_instance.process_step(step, dados_carry)
                max_step = method_instance.get_max_steps()
                if step >= max_step:
                    return result[0], result[1], 0
                else:
                    return result[0], result[1], step
            else:
                return blank_figure(), "Algoritmo ou método não encontrado.", 0

            
    # Both callbacks below are used to disable the checklist of algorithms or methods
    # when the other is selected. This is to ensure that the user can only select one at a time.
    @app.callback(
    Output('checklist-methods-wrapper', 'style'),
    Input('checklist-Algorithms', 'value')
    )
    def disable_methods_if_algorithm_selected(algos):
        if algos:
            return {"pointerEvents": "none", "opacity": 0.5}
        return {"pointerEvents": "auto", "opacity": 1}
    
    @app.callback(
    Output('checklist-algorithms-wrapper', 'style'),
    Input('checklist-Methods', 'value')
    )
    def disable_methods_if_algorithm_selected(algos):
        if algos:
            return {"pointerEvents": "none", "opacity": 0.5}
        return {"pointerEvents": "auto", "opacity": 1}


    # Dimension input for the algorithm and methods
    @app.callback(
    Output('dimension-input-container', 'children'),
    Input('checklist-Algorithms', 'value'),
    Input('checklist-Methods', 'value'),
    prevent_initial_call=True
    )
    def show_dimension_input(algorithms_selected, methods_selected):
        if not algorithms_selected and not methods_selected:
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
    [Output('visualization-results', 'children', allow_duplicate=True),
     Output('step-content', 'children', allow_duplicate=True),
     Output('keygen-data', 'data', allow_duplicate=True),
     Output('btn-next', 'n_clicks', allow_duplicate=True),
     Output('btn-next', 'disabled'),
     Output('start', 'disabled', allow_duplicate=True),
     Output('checklist-Algorithms', 'value'),
     Output('checklist-methods-wrapper', 'style',allow_duplicate=True),
     Output('checklist-algorithms-wrapper', 'style',allow_duplicate=True),
    ],
     Input('reset-btn', 'n_clicks'),
     prevent_initial_call=True
    )
    def ResetSystem(clicks):
        if clicks:            
            return '', '', None, 0, True,False,None,{"pointerEvents": "auto", "opacity": 1},{"pointerEvents": "auto", "opacity": 1}

    # Callback for user status
    @app.callback(
        Output('user-status', 'children'),
        Input('url', 'pathname'),  # ← Usa o dcc.Location
        prevent_initial_call=True
    )
    def update_login_status(pathname):
        if current_user.is_authenticated:
            return html.Div(className="user-status", children=[
                html.Img(src=current_user.profile_pic,className="profile-pic"),
                html.A("Logout", href="/logout", className="login-button")
            ])
        else:
            return html.A("Login", href="/login", className="login-button")
        

                
    
 

            
