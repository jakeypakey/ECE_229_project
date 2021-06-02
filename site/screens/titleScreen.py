import dash_html_components as html

from app import app

layout = html.Div(id='title-screen', className='row center-title', children=
    [
        html.Div(className="twelve columns pretty_container title-screen", children=[
            html.H1('''US Traffic Accident Analysis'''),
            html.P('''by Group 2''')
        ]),
        # html.Div(className='nav-button-next', children=
        #     [
        #         html.A('Next', href='#data-overview-screen')
        #     ]
        # )

    ])