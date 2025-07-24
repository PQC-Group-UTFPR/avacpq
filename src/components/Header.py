from dash import html, dcc

def create_header():
    return html.Div(
        id="app-header",
        className="app-header",
        children=[
            html.Div(
                className="header-container",
                children=[
                    html.Div(
                        className="header-left",
                        children=[
                            html.Img(src="/assets/logo.png", className="header-logo"),
                            html.H1("AVACPQ", className="app-title")
                        ]
                    ),
                    
                    html.Div(
                        className="header-center",
                        children=[
                            dcc.Link("Home", href="/", className="nav-link"),
                            dcc.Link("Algoritmos", href="/algoritmos", className="nav-link"),
                        ]
                    ),
                    
                    html.Div(
                        className="header-right",
                        children=[
                            html.Div(id="user-status") 
                        ]
                    )
                ]
            )
        ]
    )