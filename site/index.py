import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from dotenv import dotenv_values
config = dotenv_values('.env')

from app import app, server
from screens import dataOverviewScreen, comparisonScreen, titleScreen, statesScreen, conditionsScreen, mapScreen

app.layout = html.Div(className='page-content container', children=
[
    titleScreen.layout,
    dataOverviewScreen.layout,
    statesScreen.layout,
    comparisonScreen.layout,
    conditionsScreen.layout,
    mapScreen.layout
])

if __name__ == '__main__':
    # to run dev server
    # python index.py
    app.run_server(debug=True)

# to start production server
# gunicorn index:server -b :8000