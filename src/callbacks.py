import dash
#import plotly.graph_objs as go
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State

"""
---------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------
Global settings
---------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------
"""
selected_algo = "None"
selected_method = "None"

"""
---------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------
Callbacks and imported functions
---------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------
"""

def blank_figure():
    fig = go.Figure(go.Scatter(x=[], y=[]))
    fig.update_layout(template="plotly_dark")
    return fig



def get_callbacks(app):
    """        
        Using this so main.py is free of callback's code
    """

    """
        Callback to set user options
    """
    #@app.callback(
    #    Output("hidden-div-checklist", "children"),
    #    Input("checklist", "value"),
    #)
    #def update_checklist_selection(check_values):
    #    global selected_algo
    #    global selected_method
    #    if not 'None' in check_values:
    #        selected_algo = value        


    @app.callback(
        Output("grafico-central", "figure"), 
        Input("checklist-Algorithms", "value")
    )
    def update_graph(algo):
       
        print(algo, flush=True)

        if len(algo) == 0:
            return blank_figure()

        data = {"x": [1,2,3,4,5], "y": [2,3,4,5,6], "colors": ["darkblue"], "years": []}
        fig = go.Figure(
            data=[
                go.Scatter(
                    x0=0,
                    y0=0,
                    x=data["x"],
                    y=data["y"],
                    mode="markers+lines",
                    marker=dict(
                        symbol="arrow",
                        color="royalblue",
                        size=16,
                        angleref="previous",
                        standoff=8,
                    )                  
                )
            ]
        )
        fig.update_xaxes(rangemode="tozero")
        fig.update_yaxes(rangemode="tozero")

        fig.update_xaxes(title='X')
        fig.update_yaxes(title='Y')

        fig.update_layout(legend_title=dict(text=algo[0],
                                     font=dict(family="sans-serif",
                                     size = 18,
                                     color="white")))


        fig.update_layout(template="plotly_dark")                          
        return fig


