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
                ),
            ]
        ),
        
        # Seção de conteúdo
        html.Section(
            className="section-cards",
            children=[
                
                
                # Cards de algoritmos
                html.Div(
                    className="algorithm-cards",
                    children=[
                        html.H2("Algoritmos Pós-Quânticos", className="section-title"),
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
                ),
                 # Título da seção de criptoanálise
                        
                        # Cards de métodos de criptoanálise
                        html.Div(
                        
                            className="algorithm-cards",
                            children=[
                                
                            html.H2("Métodos de Criptoanálise", className="section-title"),
                                # Card Redução de Gauss
                                
                                html.Div(
                                    className="algo-card",
                                    children=[
                                        html.H3("Redução de Gauss"),
                                        html.P("Método clássico para encontrar vetores curtos em reticulados bidimensionais, transformando a base em vetores ortogonais."),
                                    ]
                                ),
                                # Card LLL
                                html.Div(
                                    className="algo-card",
                                    children=[
                                        html.H3("LLL"),
                                        html.P("Algoritmo Lenstra-Lenstra-Lovász que aproxima soluções para o SVP em reticulados com complexidade polinomial."),
                                    ]
                                ),
                                # Card BKZ
                                html.Div(
                                    className="algo-card",
                                    children=[
                                        html.H3("BKZ"),
                                        html.P("Block Korkine-Zolotarev melhora o LLL trabalhando com blocos da base do reticulado para encontrar vetores mais curtos."),
                                    ]
                                )
                            ]
                        )
                
                
                ])
    ]
)