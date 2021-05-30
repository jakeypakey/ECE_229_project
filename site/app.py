import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objects as go
from dash.dependencies import Input, Output

# initialize app
app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}],
)
server = app.server
mapbox_access_token = "pk.eyJ1IjoiZ2F0ZXN6ZW5nIiwiYSI6ImNrcDliejM3cDBnM2QycG9mdWc3ZWljY2UifQ.P1Q1hqynW5TOWMLbKnL54A"


app.layout = html.Div(children=[
    html.Div(className='row title-screen', children=[
        html.Div(className="twelve columns", children=[
            html.H1('''Title Screen'''),
            html.Div([
                html.P('''Description about our project here''')
            ])
        ])
    ]),
    html.Div(className='row content-screen first', children=[
        html.H1('''Section 1: Traffic Collisions by State and Day''')
    ]),
    html.Div(className='row content-screen second', children=[
        html.H1('''Section 2: Traffic Collisions by Condition''')
    ]),
    html.Div(className='row content-screen routes', children=[
        html.Div(className="four columns div-user-controls", children=[
            html.H1('''Section 3a: Enter directions here''')
        ]),
        html.Div(className="eight columns div-for-charts bg-grey", children=[
            html.H1('''Section 3b: Map''')
        ])
    ]),
    html.Div(className='row reference-screen', children=[
        html.H1('''References here''')
    ]),

])

if __name__ == '__main__':
    app.run_server(debug=True)



