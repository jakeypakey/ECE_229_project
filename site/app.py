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

# load the datasets
latInitial = 32.880056457383546
lonInitial =-117.23403033597369
accidents = pd.read_csv("../data/accidents_visualization.csv")
us_cities = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/us-cities-top-1k.csv")

# set the site layout
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
            dcc.Graph(id="map-graph",
                figure=go.Figure(
                    data=[
                        go.Scattermapbox(
                            customdata=us_cities,
                            lat=us_cities["lat"], 
                            lon=us_cities["lon"], 
                            hoverinfo='text',
                            text=us_cities['City']
                        )
                    ],
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
            )
        ])
    ]),
    html.Div(className='row reference-screen', children=[
        html.H1('''References here''')
    ]),
    dcc.Store(id='routes-json', data=[]),
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
    print('mapview updated')

    latInitial = 32.880056457383546
    lonInitial =-117.23403033597369

    route_data = [
            go.Scattermapbox(
                customdata=us_cities,
                lat=us_cities["lat"], 
                lon=us_cities["lon"], 
                hoverinfo='text',
                text=us_cities['City']
            )
        ]+[
            go.Scattermapbox(
                name='Route #{}'.format(i+1),
                hoverinfo='name',
                lat=np.array(route_coords)[:,1],
                lon=np.array(route_coords)[:,0],
                mode='lines',
                line=dict(width=3, color=route_colors[i])
            ) for i,route_coords in enumerate(route_geojson)
        ]
    route_data.reverse()

    return go.Figure(
        data=route_data,
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



