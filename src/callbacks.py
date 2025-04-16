import dash
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import numpy as np
import time

from lattice_based.ggh.ggh import get_ggh_data 

selected_algo = "None"
selected_method = "None"

def blank_figure():
    fig = go.Figure(go.Scatter(x=[], y=[]))
    fig.update_layout(template="plotly_dark")
    return fig

def get_callbacks(app):
    """
    Callback to update the graph based on the selected algorithm
    """

    @app.callback(
        Output("grafico-central", "figure"), 
        Input("checklist-Algorithms", "value")
    )
    def update_graph(algo):
        print(algo, flush=True)

        if len(algo) == 0:
            return blank_figure()

        #Associate the algorithm name with its corresponding function name.
        algorithm_map = {
            "GGH": get_ggh_data,  
        }

        #Verify whether the selected algorithm exists in the map.
        if algo:
            selected_algo = algo[0]  # Pega o primeiro (e único) item da lista
            if selected_algo in algorithm_map:
                # Call the function associated with the algorithm
                algorithm_function = algorithm_map[selected_algo]
                ggh_data = algorithm_function(use_random_plaintext=True, n=2)

                # Extract the steps for each value to be plotted
                plaintext = ggh_data["plaintext"]
                ciphertext = ggh_data["ciphertext"]
                error = ggh_data["error"]
                recovered_plaintext = ggh_data["recovered_plaintext"]

                # Prepare the data for plotting
                x_values = list(range(len(plaintext))) # X-axis for each step


                # Create the graph
                fig = go.Figure()

                # Plotting the different points (plaintext, error, ciphertext, etc.)
                fig.add_trace(go.Scatter(x=x_values, y=plaintext, mode='markers+lines', name='Plaintext'))

                fig.add_trace(go.Scatter(x=x_values, y=ciphertext, mode='markers+lines', name='Ciphertext'))
                

                fig.add_trace(go.Scatter(x=x_values, y=error, mode='markers+lines', name='Error'))
                

                fig.add_trace(go.Scatter(x=x_values, y=recovered_plaintext, mode='markers+lines', name='Recovered Plaintext'))
                
                fig.update_layout(
                    title="GGH Encryption Steps",
                    xaxis_title="Index",
                    yaxis_title="Value",
                    template="plotly_dark"
                )

                return fig
            else:
                # Return an empty graph if the algorithm is not mapped
                return blank_figure() 
        else:
            return blank_figure()  
