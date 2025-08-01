from dash import html, dcc

def create_footer():
    return html.Div(
        id="app-footer",
        className="app-footer",
        children=[
            html.Div(
                className="footer-container",
                children=[
                    html.Div(
                    html.P("© 2025 AVACPQ", className="footer-text"),
                    ),
                    html.Div(children=[
                    html.A([
                                html.Img(
                                    src="/assets/github-logo_2.png", 
                                    className="footer-logo",
                                    style={"height": "30px", "marginRight": "5px"}
                                ),
                                "GitHub"
                            ], 
                            href="https://github.com/PQC-Group-UTFPR/avacpq", 
                            target="_blank",
                            className="footer-link"),
                    html.A([
                                html.Img(
                                    src="/assets/utfpr-logo.png",  
                                    className="footer-logo",
                                    style={"height": "20px", "marginRight": "5px"}
                                ),
                                "COENC"
                            ], 
                            href="https://coenc.td.utfpr.edu.br/", 
                            target="_blank", 
                            className="footer-link")
                ]),
                ]
            )
        ]
    )