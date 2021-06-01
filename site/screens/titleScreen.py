import dash_html_components as html

from app import app

layout = html.Div(className='row title-screen', children=
    [
        html.Div(className="twelve columns", children=[
            html.H1('''Title Screen'''),
            html.Div([
                html.P('''Description about our project here''')
            ]),
            html.A('jump to map', href='#map-screen'),
        ])
    ])