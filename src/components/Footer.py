from dash import html, dcc

def create_footer():
    return html.Div(
        id="app-footer",
        className="app-footer",
        children=[
            html.Div(
                className="footer-container",
                children=[
                    
                    html.Div(children=[
                    html.A([
                                html.Img(
                                    src="/assets/github-logo_2.png", 
                                    className="footer-logo",
                                    style={"height": "30px", "marginRight": "5px", "backgroundColor": "transparent"}
                                ),
                                "GitHub"
                            ], 
                            href="https://github.com/PQC-Group-UTFPR/avacpq", 
                            target="_blank",
                            className="footer-link"),
                    html.A([
                                html.Img(
                                    src="/assets/logo.png",  
                                    className="footer-logo",
                                    style={"height": "30px", "marginRight": "5px"}
                                ),
                                "AVACPQ"
                            ], 
                            href="https://pqc-group-utfpr.github.io/", 
                            target="_blank", 
                            className="footer-link")
                ]),
                html.Div(
                    html.P("© 2025 PQC Group UTFPR. All rights reserved.", className="footer-text"),
                    ),
                ]
            )
        ]
    )