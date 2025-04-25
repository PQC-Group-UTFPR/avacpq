from dash import Dash, html, dcc
from callbacks import blank_figure
from callbacks import get_callbacks

"""
---------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------
Dash settings 
---------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------
"""

app = Dash(    
    __name__,
    prevent_initial_callbacks=True,
    assets_folder='assets', 
    meta_tags=[{"name": "viewport",
                "content": "width=device-width, initial-scale=1"}],
)
app.title = "AVACPQ: Artifícios Visuais para Aprendizado de Criptografia Pós-Quântica"
app.config.suppress_callback_exceptions = True




get_callbacks(app)



"""
---------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------
Layout functions and definitions
---------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------
"""

def create_header():
    return html.Div(
        id="app-header",
        className="app-header",
        children=[
            # Logo and Title
            html.Div(
                className="header-left",
                children=[
                    html.Img(src="assets/logo.png", className="header-logo"),
                    html.H1("AVACPQ", className="app-title")
                ]
            ),
            
            # Login Button 
            html.Div(
                className="header-right",
                children=[
                    html.Button(
                        "Login",
                        id="login-button",
                        className="login-button",
                        n_clicks=0
                    )
                ]
            )
        ]
    )

def generate_control_card():
    """
    :return: A Div containing controls for graphs.
    """
    return html.Div(
        id="control-card",
        className="control-card",  # opcional se quiser estilizar tudo
        children=[
            # Div separada para os checklists
            html.Div(
                className="checklist-container",
                children=[
                    html.P("Algoritmos:"),
                    dcc.Checklist(
                        id="checklist-Algorithms",
                        options={
                            'LWE (1 bit)': 'LWE (1 bit)',
                            'GGH': 'GGH',
                            'Alkaline': 'Alkaline',
                        },
                    ),
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
                    html.Button(id="reset-btn", children="Reset", n_clicks=0)
                ]
            )
        ],
    )

def step_navigation():
    return html.Div([
        html.H4("Passo a Passo", className="steps-title"),
        dcc.Store(id='keygen-data') , 
        html.Div(id="step-content", className="step-content"),
        dcc.Store(id='current-step', data={'step': 0}),
        html.Div([
            html.Button("Próximo", id="btn-next", n_clicks=0, className="btn-nav")
        ], className="nav-buttons")
    ], className="steps-card")

def visualization_Results():
    return html.Div([
        html.H4("Visualização", className="vizu-title"),
        # Table or graph here
        dcc.Graph(id='visualization-results'),
    ], className="vizu-card")


"""
---------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------
Main
---------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------
"""
app.layout = html.Div(
    className="app-container",
    children=[
        create_header(),  # header
        
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

if __name__ == '__main__':
    app.run(debug=True, dev_tools_hot_reload=True)