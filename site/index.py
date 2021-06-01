import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from screens import titleScreen, statesScreen, conditionsScreen, mapScreen

app.layout = html.Div(id='page-content', children=
[
    titleScreen.layout,
    statesScreen.layout,
    conditionsScreen.layout,
    mapScreen.layout
])

if __name__ == '__main__':
    app.run_server(debug=True)