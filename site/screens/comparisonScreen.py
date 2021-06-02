# -*- coding: utf-8 -*-
"""
Created on Tue Jun  1 22:55:23 2021

@author: srist
"""



import numpy as np
import pandas as pd
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from plotly.subplots import make_subplots

from app import app

# load dataset
comparisons_df = pd.read_csv("data/comparisons.csv")

columns = list(comparisons_df.keys())
features = list(comparisons_df.keys())
for column in ['State', 'year_month','Month', 'Year']:
    features.remove(column)
features = np.unique([column.split("_")[0] for column in features] ) 
columns_mapping = {}
for feature in features:
    columns_mapping[feature] = [column for column in columns if feature in column]

years = comparisons_df['Year'].unique()
years.sort()

States_names = list(comparisons_df['State'].unique())
States_names.remove('All')
States_names.sort()
States_names.insert(0,'All')
states_dict = [{'label': state, 'value': state} for state in States_names]


# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
# app = dash.Dash(__name__, external_stylesheets=external_stylesheets) 

layout = html.Div([
    html.H2("Comparisons"),
    html.Div([
        html.Div([
            html.H3('States'),
            dcc.Dropdown(
                options=states_dict,
                multi=False,
                value="All",
                id="states"
            )  
        ], className="six columns"),


    ], className="container"),

    
    
    dcc.Graph(id="graph",style={"height": 500}),
    

    html.Div(children=[dcc.Slider(
        min=2016,
        max=2019,
        step=1,
        marks={
            2016: '2016',
            2017: '2017',
            2018: '2018',
            2019: '2019'
        },
        value=2016,
        id='Year')],style={'width': '70%', 'padding-left': '15%','padding-right': '15%' } 
        )
    
])

@app.callback(Output("graph", "figure"), 
                       [Input('states', 'value'),
                        Input('Year','value')])
def update_graphs(State,year):
    
    if not State:
        State = "All"
     
    df = comparisons_df[comparisons_df['State']==State]
    
    fig = make_subplots(rows=2, cols=1, subplot_titles = (features[0], features[1]))

    for i in [0,1]:
        for column in columns_mapping[features[i]]:
            fig.add_trace(go.Bar(
                y=df[df['Year']==year][column],
                x=list(range(1,13)),
                name=column,
                legendgroup = str(i+1)
                ),row=i+1, col=1)

    fig.update_layout(barmode='stack')
    fig.update_layout(xaxis = dict(
                    tickmode = 'array',
                    tickvals = list(range(1,13)),
                    ticktext = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'June','July','Aug','Sep','Oct','Nov','Dec']
                    ),
                      xaxis2 = dict(
                    tickmode = 'array',
                    tickvals = list(range(1,13)),
                    ticktext = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'June','July','Aug','Sep','Oct','Nov','Dec']
                    ),
                      legend_tracegroupgap = 100,)

    return fig 





