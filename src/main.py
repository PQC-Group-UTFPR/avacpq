from dash import Dash, html

app = Dash(__name__)

app.layout = html.Div([
    html.Div(children='Hello World, AVACPQ!')
])

if __name__ == '__main__':
    app.run(debug=True)
