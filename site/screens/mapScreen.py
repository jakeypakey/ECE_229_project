import numpy as np
import pandas as pd
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from datetime import datetime as dt
from dotenv import dotenv_values
config = dotenv_values('.env')
from dash.exceptions import PreventUpdate
import json

from app import app
from utils.DirectionsUtil import DirectionsClient

# intialization
directions_client = DirectionsClient()
mapbox_access_token = config['MAPBOX_KEY']
latInitial = 32.880056457383546
lonInitial =-117.23403033597369

# dataset loading
us_cities = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/us-cities-top-1k.csv")

# screen layout
layout = html.Div(id='map-screen', className='row content-screen routes', children=
    [
        html.Div(className="four columns div-user-controls", children=[
            html.Div(
                className="div-for-dropdown",
                children=[
                    html.H1('Directions with Accident-Avoidance'),
                    html.Div(dcc.Input(id='input-starting-location', type='text')),
                    html.Div(dcc.Input(id='input-ending-location', type='text')),
                    html.Button('Submit', id='btn-submit', n_clicks=0),
                    html.P(id='submit-text', children='')
                ],
            )
        ]),
        html.Div(className="eight columns div-for-charts bg-grey", children=
            [
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
            ]
        ),
        dcc.Store(id='routes-json', data=[]),
    ]
)

# callbacks
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