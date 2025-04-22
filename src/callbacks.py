import dash
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from lattice_based.ggh.ggh import generate_keys, encrypt, decrypt  # Importação completa

# [...] (o resto do código permanece igual)
# Variáveis globais para armazenar estado entre callbacks
ggh_data = {}
public_key = None
public_key_inverse = None
plaintext = None
error = None
ciphertext = None
decrypted_plaintext = None

def blank_figure():
    fig = go.Figure(go.Scatter(x=[], y=[]))
    fig.update_layout(template="plotly_dark")
    return fig

def get_callbacks(app):
    
    # Primeiro passo: Generate Keys (mostra em step-content)
    @app.callback(
        [Output("step-content", "children"),
         Output("visualization-results", "figure", allow_duplicate=True)],
        Input("start", "n_clicks"),
        Input("dimension-input", "value"),
        prevent_initial_call=True
    )
    def generate_keys(clicks, dimension_value):
        global ggh_data, public_key, public_key_inverse, plaintext, error
        
        if clicks is None or dimension_value is None:
            return dash.no_update, blank_figure()

        # Gerar chaves GGH
        ggh_data =  generate_keys()
        
        # Armazenar valores para os próximos passos
        public_key = ggh_data.get("public_key")
        public_key_inverse = ggh_data.get("public_key_inverse")
        plaintext = ggh_data.get("plaintext")
        error = ggh_data.get("error")
        
        # Mensagem para mostrar no step-content
        message = "Chaves GGH geradas com sucesso!\n"
        message += f"Dimensão: {dimension_value}\n"
        message += f"Plaintext: {plaintext}\n"
        message += f"Error: {error}"

        return message, blank_figure()

    # Segundo e terceiro passos: Encrypt e Decrypt (mostra em step-content)
    @app.callback(
        [Output("step-content", "children"),
         Output("visualization-results", "figure", allow_duplicate=True)],
        Input("btn-next", "n_clicks"),
        prevent_initial_call=True
    )
    def process_steps(clicks):
        global ciphertext, decrypted_plaintext
        
        if clicks is None:
            return dash.no_update, dash.no_update
            
        if clicks == 1:  # Passo de encriptação
            ciphertext = encrypt(public_key, plaintext, error)
            message = f"Texto encriptado:\n{ciphertext}"
            return message, blank_figure()
            
        elif clicks == 2:  # Passo de decriptação
            decrypted_plaintext = decrypt(public_key_inverse, ciphertext)
            message = f"Texto decriptado:\n{decrypted_plaintext}"
            return message, blank_figure()
            
        elif clicks >= 3:  # Passo final - mostrar tudo no gráfico
            return create_final_visualization()

    def create_final_visualization():
        # Criar gráfico com todos os resultados
        x_values = list(range(len(plaintext)))
        
        fig = go.Figure()
        
        # Adicionar todas as trajetórias
        fig.add_trace(go.Scatter(
            x=x_values, y=plaintext, 
            mode='markers+lines', 
            name='Plaintext Original',
            line=dict(color='blue')
        ))
        
        fig.add_trace(go.Scatter(
            x=x_values, y=ciphertext, 
            mode='markers+lines', 
            name='Ciphertext',
            line=dict(color='red'))
        )
        
        fig.add_trace(go.Scatter(
            x=x_values, y=error, 
            mode='markers', 
            name='Error Vector',
            marker=dict(color='orange'))
        )
        
        fig.add_trace(go.Scatter(
            x=x_values, y=decrypted_plaintext, 
            mode='markers+lines', 
            name='Plaintext Decifrado',
            line=dict(color='green', dash='dot'))
        )
        
        fig.update_layout(
            title="Comparação Completa do Processo GGH",
            xaxis_title="Índice do Vetor",
            yaxis_title="Valor",
            template="plotly_dark",
            legend=dict(orientation="h", yanchor="bottom", y=1.02)
        )
        
        message = "Processo completo! Visualize os resultados no gráfico."
        return message, fig