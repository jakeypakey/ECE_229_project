import dash_html_components as html
import pickle
from app import app
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import json
from urllib.request import urlopen
def get_counties(starter_fip):
    '''
    Function: Get the geojson dictionary necessary for DASH plot
    Input: Starter 2 digit value of FIP for a specific state (i.e. '06' for California)
    Output: Dictionary needed for plotting
    '''
    with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
        counties = json.load(response)
    CA_counties = {'type':'FeatureCollection','features':[]}
    for info in counties['features']:
        if info['properties']['STATE'] == starter_fip:
            CA_counties['features'].append(info)
    return CA_counties
def load_obj(name ):
    with open('./data/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)
all_state_dict = load_obj('all_state_dict')
fig_names = ['AL', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY',
                 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND',
                 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']
fig_names2 = ['Rain', 'Clear','Fog','Snow','Cloudy', 'All Weather']
fig_names3 = ['Day','Noon','Night', 'All Times of Day']

layout = html.Div(id='conditions-screen', className='row flex-display', children=
    [
        html.Div(className='pretty_container eight columns', children=
            [
                html.Div(id='fig_plot'),
            ]
        ),
        html.Div(className='pretty_container four columns', children=
            [
                html.Div(
                    [
                        dcc.Dropdown(
                            id='fig_dropdown',
                            options=[{'label': x, 'value': x} for x in fig_names],
                            value='CA'
                        )
                    ]
                ), 
                html.Div(
                    [
                        dcc.Dropdown(
                            id='fig_dropdown2',
                            options=[{'label': x, 'value': x} for x in fig_names2],
                            value='All Weather'
                        )
                    ]
                ), 
                html.Div(
                    [
                        dcc.Dropdown(
                            id='fig_dropdown3',
                            options=[{'label': x, 'value': x} for x in fig_names3],
                            value='All Times of Day'
                        )
                    ]
                ) 
            ]
        ),
        # html.Div(className='nav-button-next', children=
        #     [
        #         html.A('Next', href='#map-screen')
        #     ]
        # )
    ])


@app.callback(dash.dependencies.Output('fig_plot', 'children'), [dash.dependencies.Input('fig_dropdown', 'value'),\
                                                                 dash.dependencies.Input('fig_dropdown2', 'value'),\
                                                                 dash.dependencies.Input('fig_dropdown3', 'value')])


def update_output(fig_name,fig_name2, fig_name3):
    return name_to_figure(fig_name,fig_name2, fig_name3)

def name_to_figure(fig_name,fig_name2, fig_name3):
    if fig_name == None or 'All' in fig_name:
        fig_name = 'CA'
    if fig_name2 == None or 'All' in fig_name2:
        fig_name2 = 'All'
    if fig_name3 == None or  'All' in fig_name3:
        fig_name3 = ''
    elif 'All' in fig_name2:
        fig_name2 = ''
    else:
        fig_name3 = '+' + fig_name3
    CA_dict_df = all_state_dict[fig_name]
    state_code_start = np.array(CA_dict_df)[0,-1][:2]
    CA_counties = get_counties(state_code_start) 
    color_name = fig_name2 + fig_name3
    quantile75 = CA_dict_df[color_name].median() *3
    quantile0 = CA_dict_df[color_name].min()
    figure = px.choropleth(CA_dict_df, geojson=CA_counties, color=color_name,
                locations="FIP", featureidkey="id",
                projection="mercator",range_color=(quantile0, quantile75)
                ).update_geos(fitbounds="locations", visible=False,    resolution=50,
                    showcoastlines=True, coastlinecolor="RebeccaPurple",
                    showland=True, landcolor="lightslategray",
                    showocean=True, oceancolor="LightGrey",
                    showcountries =True)
    figure.update_layout(margin={"r":0,"t":0,"l":0,"b":0},paper_bgcolor = "#ffffff")
    return dcc.Graph(figure=figure)
