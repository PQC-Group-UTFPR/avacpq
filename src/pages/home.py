from dash import html, dcc, register_page

register_page(__name__, path='/', title='AVACPQ - Página Inicial')


layout = html.Div(
    className="home-container",
    children=[
        html.Div(
            className="home-container-card",
            children=[
                html.Img(
                    src="/assets/home-background-3.png",
                    className="home-background-image",
                    alt="Imagem de fundo da página inicial"),
                html.Div(
            className="home-card",
            children=[  
                html.H1("Aprendizado do funcionamento de algoritmos baseado em reticulados", 
                       className="banner-title"),
                html.P("Visualização do processo de encriptação e decriptação dos algoritmos.",
                      className="banner-subtitle"),
                      # Botão posicionado no final do segundo card
                html.Div(
                    className="card-button-container",
                    children=[
                        dcc.Link(
                            html.Button("Explorar Algoritmos", className="banner-button"),
                            href="/algoritmos"
                        )
                    ]
                )
            ]
        ),]

        ),
        
        
    
                html.Div(
    className="algorithm-cards",
    children=[
        # Card GGH
        html.Div(
            className="algo-card",
            children=[
                html.H3("GGH"),
                html.P("Baseado em reticulados, o GGH usa a dificuldade de encontrar o vetor mais curto (SVP). "),
            ]
        ),

        # Card LWE
        html.Div(
            className="algo-card",
            children=[
                html.H3("LWE"),
                html.P("Baseado em reticulados, o LWE baseia-se na resolução equações com pequenos erros aleatórios."),
            ]
        ),

        # Card Alkaline
        html.Div(
            className="algo-card",
            children=[
                html.H3("Alkaline"),
                html.P("Baseado em estruturas algébricas, o Alkaline é difícil porque combina várias operações matemáticas complexas."),
            ]
        )
    ]
)

            ]
        )
