# old code, don't use. will remove in a couple commits
# refactored into screen files and index.py
'''
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
from dash.exceptions import PreventUpdate
import json
import plotly.express as px

from directions import DirectionsClient

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

# screen 1 code
fig = px.choropleth(accidents,               
                  locations="State",               
                  color="counts",
                  hover_name="State", 
                  locationmode="USA-states",
                  animation_frame="year_month",    
                  color_continuous_scale='Plasma',  
                  height=600,
                  scope='usa'
    )
fig.update_layout(geo_scope="usa")

States_names = list(accidents['State'].unique())
States_names.sort()
States_names.insert(0,'All')
states_dict = [{'label': state, 'value': state} for state in States_names]


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
        html.H1('''Section 1: Traffic Collisions by State and Day'''),
        html.Div([
            html.H3('States'),
            dcc.Dropdown(
                options=states_dict,
                multi=True,
                id="states"
            )  
        ]),
        dcc.Graph(figure=fig, id="graph",style={"height": 500})
    ]),
    html.Div(className='row content-screen second', children=[
        html.H1('''Section 2: Traffic Collisions by Condition''')
    ]),
    html.Div(id='map-screen', className='row content-screen routes', children=[
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

@app.callback(Output("graph", "figure"), 
                       [Input('states', 'value')])
def update_graphs(rows):
    if not rows:
        rows = ["All"]

    if 'All' in rows:
        df = accidents
    else:
        df = accidents[accidents['State'].isin(rows)]

    fig = px.choropleth(df,
                        locations="State",               
                        color="counts",
                        hover_name="State", 
                        locationmode="USA-states",    
                        animation_frame="year_month",
                        color_continuous_scale='Plasma',  
                        height=500,
                        scope='usa'
                        )
    fig.update_layout(geo_scope="usa")
    
    fig.layout.sliders[0]['active'] = 0 #len(fig.frames) - 1  # slider
    fig.update_traces(z=fig.frames[0].data[0].z) 
    
    
    return fig #[dcc.Graph(figure=fig,style={"height": 500})]


if __name__ == '__main__':
    app.run_server(debug=True, port=8051)



'''