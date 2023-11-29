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

def description_card():
    """
    :return: A Div containing dashboard logo.
    """
    return html.Div(
        id="description-card",
        children=[
            html.Img(src="assets/logo.png", className="responsiveimg"),     
        ],
    )


def generate_control_card():
    """
    :return: A Div containing controls for graphs.
    """
    return html.Div(
        id="control-card",
        children=[
            html.Br(),            
            html.P("Algoritmos:"),
            dcc.Checklist(id="checklist-Algorithms",
                          options={
                              'LWE (1 bit)': 'LWE (1 bit)',
                              'GGH': 'GGH',
                              'Alkaline': 'Alkaline',
                          },
                          ),
            html.Br(),
            html.P("Métodos de Criptoanálise:"),
            dcc.Checklist(id="checklist-Methods",
                          options={
                              'method1': 'Redução de Gauss',
                              'method2': 'LLL',
                              'method3': 'BKZ',
                          },
                          ),
            html.Br(),
            html.Div(
                id="reset-btn-outer",
                children=  [# html.Button(id="reset-btn", children="Reset", n_clicks=0),
                html.Button(id="start", children="Iniciar!", n_clicks=0),
                html.Button(id="reset-btn", children="Reset", n_clicks=0)
                ]
            ),
        ],
    )


"""
---------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------
Main
---------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------
"""
app.layout = html.Div(
    id="app-container",
    children=[        
        #estrutura em duas colunas
        html.Div(
            id="left-column",
            className="two columns",
            children=[description_card(), generate_control_card()]
            + [
                html.Div(
                    ["initial child"], id="output-clientside", style={"display": "none"}
                )
            ],
        ),
        # Right column
        html.Div(
            id="right-column",
            className="nine columns",
            children=[
                html.Br(),
                html.Div(
                    id="tela_gráfico",
                    children=[                        
                        dcc.Graph(
                            id='grafico-central',
                            responsive=True, style={                                
                                # 'display': 'inline-block'
                                'display': 'block',
                                #'height': '450px'
                            },
                            figure=blank_figure()
                        ),
                        html.Br(),
                        html.H6(
                            "Resultados (Passo a passo):"),
                        #dash_table.DataTable(
                        #    id="statistics",
                        #    style_as_list_view=True,
                        #    columns=[{"id": "mean_size", "name": "Mean HS Size (bytes)"}, {"id": "stdev_size", "name": "STDEV HS Size (bytes)"}, {"id": "mean_time", "name": "Mean HS Time (ms)"}, {"id": "stdev_time", "name": "STDEV HS Time (ms)"}],
                        #    data=[],
                        #    style_header={
                         #       'backgroundColor': '#222222',
                         #       'color': 'white',
                         #       'textAlign': 'left',
                         
                         #   },
                         #   style_data={
                         #       'backgroundColor':  '#222222',
                         #                           'color': 'white',
                         #       'textAlign': 'left',
                         
                        #    },
                        #),
                        html.Br(),
                                                
                        
                        #html.H6(
                        #    "Performance Information:"),
                        #dash_table.DataTable(
                        #    id="summary_tls",
                        #    columns=[{'id': "hs_id", 'name': "Handshake (HS) Number"},
                        #             {'id': "hs_size",
                        #              'name': "HS Size (bytes)"},
                        #             {'id': "hs_time",
                        #              'name': "HS Time (ms)"},
                        #             ],
                        #    data=[],
                        #    tooltip_header={
                        #        'hs_id': 'Sequential number of the Handshake',
                        #        'hs_size': 'Handshake size is computed by the sum of KEX and Authentication messages',
                        #        'hs_time': 'Handshake time is computed starting from the Client Hello message timestamp (provided by pcap file) until the client receives the Finished message from the Server. Note that this is the handshake time under the perspective of the client (the server also receives a finished message that ends the handshake).',
                        #    },
                        #    css=[{
                        #        'selector': '.dash-table-tooltip',
                        #        'rule': 'background-color: grey; font-family: monospace; color: white'
                         #   }],
                         #   tooltip_duration=9000,
                         #   style_as_list_view=False,
                         #   style_header={
                         #       'backgroundColor': '#222222',
                         #       'color': 'white',
                         #       'textAlign': 'left',
                         #   },
                         #   style_data={
                         #       'backgroundColor':  '#222222',
                         #                           'color': 'white',
                         #                           'textAlign': 'left'
                         #   },
                         #   style_data_conditional=[
                         #       {
                         #           "if": {"state": "selected"},
                         #           "backgroundColor": "inherit !important",
                         #           "border": "inherit !important",
                         #       }
                         #   ]
                        #),
                    ],
                ),                
                html.Div(id='hidden-div-checklist', style={'display': 'none'}),
            ],
        ),
    ],
)

if __name__ == '__main__':
    app.run(debug=True)
