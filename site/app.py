import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from datetime import datetime as dt
import numpy as np
import polyline
from dotenv import dotenv_values
config = dotenv_values('.env')
from directions import DirectionsClient
from dash.exceptions import PreventUpdate
import json

# initialize app
app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}],
)
server = app.server
directions_client = DirectionsClient()
mapbox_access_token = config['MAPBOX_KEY']
examplePolyline = 'q|sgExfmjUAu@zFBnEBnD?l@?PDTDJZl@tA~@bCh@rAPj@^lBF`ABhAAhAUnBS~@}@hCeDbJq@hBYbASz@OdAKnACt@?rADd@RrCJr@RfB@LCDAPBz@?`@CNQZWTWH]?]QWYM_@CYBi@L]HONINGFCRE|@AJAfIVh@?^IzH`@vAHbe@pBbKd@jLd@hAJfFj@~Ab@bCz@nAl@rC`BvUxNhDlBdAb@n@TxBl@bCh@v@HfALfQ~AdBBrC@fBGxBW~B[fAWbFcBtDwAzCcA`DgAzHiCrDmArCg@|B[d@E`DK`MAzIC`BGrD_@zAWlA[fAYhAe@fAc@jEkCd@_@hCgCdWoWnH}H|@_AnE}DhFmEpC{BrGkEjGkE`OuKjDkCbHsFhImGfFiDrEoCtCyAfGsCrKqEbI}DlIgEnCoAjDmAzC}@pE_AvEm@xBQxDOdEA~@?`BBvBPvCVrARlFh@`_@rDxBTvAFdB@fDQxF}@tJ}A~GmAdC_@xAY~@KtFaA~AWdLiBd@GhJ{AnIwAjUyDnDo@xCc@jBYjCg@pA_@tB_AvBqAj@e@tAqA|@iAtAsBp@cAlDqFbA_BrAeBbBgBrEwDzE_EjCgCdCaDlAeBt@oAh@eAjAyBxB}FtDmKrEeM`FeNtGwQ|@_Cr@}AxA}Bp@{@l@m@bEgDxN_MjHgGzBqBpCyBbH}FjC}B~BgBrAgAxAmAdHaGdJ}HnAgALBPAbBy@xAu@j@c@rCcDv@s@X_@hDyCbAw@~@]z@Sj@Od@UV[Vq@Dq@GcH?sDrF?nECzP?~EA'
examplePath = polyline.decode(examplePolyline, geojson=True)

app.layout = html.Div(className='site-wrapper', children=[
    html.Div(className='row title-screen', children=[
        html.Div(className="twelve columns", children=[
            html.H1('''Title Screen'''),
            html.Div([
                html.P('''Description about our project here''')
            ]),
            html.A('jump to map', href='#map-screen'),
        ])
    ]),
    html.Div(className='row content-screen first', children=[
        html.H1('''Section 1: Traffic Collisions by State and Day''')
    ]),
    html.Div(className='row content-screen second', children=[
        html.H1('''Section 2: Traffic Collisions by Condition''')
    ]),
    html.Div(id='map-screen', className='row content-screen routes', children=[
        html.Div(className="four columns div-user-controls", children=[
            html.Div(
                className="div-for-dropdown",
                children=[
                    dcc.DatePickerSingle(
                        id="date-picker",
                        min_date_allowed=dt(2014, 4, 1),
                        max_date_allowed=dt(2014, 9, 30),
                        initial_visible_month=dt(2014, 4, 1),
                        date=dt(2014, 4, 1).date(),
                        display_format="MMMM D, YYYY",
                        style={"border": "0px solid black"},
                    ),
                    html.H1('Directions with Accident-Avoidance'),
                    html.Div(dcc.Input(id='input-starting-location', type='text')),
                    html.Div(dcc.Input(id='input-ending-location', type='text')),
                    html.Button('Submit', id='btn-submit', n_clicks=0),
                    html.P(id='submit-text', children='')
                ],
            )
        ]),
        html.Div(className="eight columns div-for-charts bg-grey", children=[
            dcc.Graph(id="map-graph")
        ])
    ]),
    html.Div(className='row reference-screen', children=[
        html.H1('''References here''')
    ]),
    dcc.Store(id='routes-json'),
    ],
)

list_of_locations = {
    "Madison Square Garden": {"lat": 40.7505, "lon": -73.9934},
    "Yankee Stadium": {"lat": 40.8296, "lon": -73.9262},
    "Empire State Building": {"lat": 40.7484, "lon": -73.9857},
    "New York Stock Exchange": {"lat": 40.7069, "lon": -74.0113},
    "JFK Airport": {"lat": 40.644987, "lon": -73.785607},
    "Grand Central Station": {"lat": 40.7527, "lon": -73.9772},
    "Times Square": {"lat": 40.7589, "lon": -73.9851},
    "Columbia University": {"lat": 40.8075, "lon": -73.9626},
    "United Nations HQ": {"lat": 40.7489, "lon": -73.9680},
}

@app.callback(
    Output('routes-json', 'data'),
    [
        Input('btn-submit', 'n_clicks'),
    ],
    state=
    [   
        Input('input-starting-location', 'value'),
        Input('input-ending-location', 'value'),
    ]
)
def update_map(nclicks, start, end):
    if nclicks == 0 or not start or not end:
        raise PreventUpdate
    routes = directions_client.get_directions_json(start, end)
    return json.dumps(routes)

@app.callback(
    Output("map-graph", "figure"),
    [
        Input("routes-json", "data")
    ]
)
def update_graph(routes_json):
    routes = json.loads(routes_json)
    route_geojson = [directions_client.get_geojson_from_route(r) for r in routes]
    route_colors = ['#f1a208', '#005377', '#052f5f']

    latInitial = 32.880056457383546
    lonInitial =-117.23403033597369

    return go.Figure(
        data=[
            go.Scattermapbox(
                lat=[list_of_locations[i]["lat"] for i in list_of_locations],
                lon=[list_of_locations[i]["lon"] for i in list_of_locations],
                mode="markers",
                hoverinfo="text",
                text=[i for i in list_of_locations],
                marker=dict(size=8, color="#ffa0a0"),
            )]
            +
            [go.Scattermapbox(
                name='Example Route',
                hoverinfo='name',
                lat=np.array(route_coords)[:,1],
                lon=np.array(route_coords)[:,0],
                mode='lines',
                line=dict(width=3, color=route_colors[i])
            ) for i,route_coords in enumerate(route_geojson)]
        ,
        layout=go.Layout(
            autosize=True,
            margin=go.layout.Margin(l=0, r=35, t=0, b=0),
            showlegend=False,
            mapbox=dict(
                accesstoken=mapbox_access_token,
                center=dict(lat=latInitial, lon=lonInitial),  # 40.7272  # -73.991251
                style="dark",
                bearing=0,
                zoom=14,
            ),
        )
    )

if __name__ == '__main__':
    app.run_server(debug=True, port=8051)



