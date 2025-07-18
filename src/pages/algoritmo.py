from dash import html, dcc, register_page, callback
import plotly.graph_objects as go

from dash.dependencies import Input, Output, State

register_page(__name__, path='/algoritmos', title='AVACPQ - Algoritmos')

def generate_control_card():
    """
    :return: A Div containing controls for graphs.
    """
    return html.Div(
        id="control-card",
        className="control-card",  
        children=[
            # Div separada para os checklists
            html.Div(
                className="checklist-container",
                children=[
                    html.H3("Algoritmos"),
                    dcc.Checklist(
                        id="checklist-Algorithms",
                       options = [
                        {'label': 'LWE (1 bit)', 'value': 'LWE'},
                        {'label': 'GGH', 'value': 'GGH'},
                        {'label': 'Alkaline', 'value': 'Alkaline'}
                        ]
                    ),
                    html.Div(id='dimension-input-container',className='dimension-input-container'),
                    html.Br(),
                    html.P("Métodos de Criptoanálise:"),
                    dcc.Checklist(
                        id="checklist-Methods",
                        options={
                            'method1': 'Redução de Gauss',
                            'method2': 'LLL',
                            'method3': 'BKZ',
                        },
                    ),
                ]
            ),
            # buttons
            html.Div(
                className="button_control",
                children=[
                    html.Button(id="start", children="Iniciar", n_clicks=0),
                    html.Div([
                    html.Button("Próximo", id="btn-next", n_clicks=0, className="btn-nav", disabled=True)
                    ], className="nav-buttons"),
                    html.Button(id="reset-btn", children="Reset", n_clicks=0)
                ]
            )
        ],
    )

def step_navigation():
    return html.Div([
        
        dcc.Store(id='keygen-data') , 
        html.Div(id="step-content", className="step-content"),
        
        dcc.Store(id='current-step', data={'step': 0})
        
    ], className="steps-card")

def visualization_Results():
    return html.Div(
        # Table or graph here
        html.Div(id="visualization-results")
        , className="vizu-card")

"""
---------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------
Main
---------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------
"""
layout = html.Div(
    className="app-container",
    children=[
        
        # Layout with 3 columns: control, step-by-step, and visualization
        html.Div(
            className="app-body",
            children=[
                html.Div(
                    className="three-column-layout",
                    children=[
                        html.Div([generate_control_card()], className="column controls-column"),
                        html.Div([step_navigation()], className="column steps-column"),
                        html.Div([visualization_Results()], className="column vizu-column")
                    ]
                )
            ]
        )
    ]
)
