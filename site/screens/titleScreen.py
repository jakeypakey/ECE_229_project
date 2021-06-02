import dash_html_components as html

from app import app

layout = html.Div(id='title-screen', className='row title-screen', children=
    [
        html.Div(className="twelve columns", children=[
            html.H1('''Title Screen'''),
            html.Div([
                html.P('''Description about our project here''')
            ]),
        ]),
        html.Div(className='nav-button-next', children=
            [
                html.A('Next', href='#data-overview-screen')
            ]
        )

    ])