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

comparisons_df = pd.read_csv("comparisons.csv")

thres_category = {'Pressure':{'thresolds':[29.5,30.2],
                              'category':['Low','Moderate','High']},
                  'TrafficStuckTime':{'thresolds':[35,50,70,90],
                              'category':['VeryLow','Low','Moderate','High','VeryHigh']},
                  'Temperature':{'thresolds':[0,30,60,80,100],
                              'category':['VeryVeryLow','VeryLow','Low','Moderate','High','VeryHigh']},}



columns = list(comparisons_df.keys())
features = list(comparisons_df.keys())
for column in ['State', 'year_month','Month', 'Year']:
    features.remove(column)
features = np.unique([column.split("_")[0] for column in features] ) 
features_dict = [{'label': feature, 'value': feature} for feature in features]

columns_mapping = {}
for feature in features:
    if feature not in thres_category.keys():
        columns_mapping[feature] = [column for column in columns if feature in column]
    else:
        columns_mapping[feature] = [feature+'_'+value for value in thres_category[feature]['category']]
        


years = comparisons_df['Year'].unique()
years.sort()

States_names = list(comparisons_df['State'].unique())
States_names.remove('All')
States_names.sort()
States_names.insert(0,'All')
states_dict = [{'label': state, 'value': state} for state in States_names]


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

        html.Div([
            # html.H3('Normalization'),
            html.Div([
                html.H3('Feature 1'),
                dcc.Dropdown(
                    options=features_dict,
                    multi=False,
                    value="Severity",
                    id="feature1"
                ) , ]),
            html.Div([
                html.H3('Feature 2'),
                dcc.Dropdown(
                    options=features_dict,
                    multi=False,
                    value="TrafficStuckTime",
                    id="feature2"
                )  ])
            

        ],className="six columns"),
        
        
        
        
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

# 'width':800,'margin-left': '5px' 'display': 'flex', , 'justify-content': 'center' 'align-items': 'center'
@app.callback(Output("graph", "figure"), 
                       [Input('states', 'value'),
                        Input('Year','value'),
                        Input('feature1','value'),
                        Input('feature2','value')])
def update_graphs(State,year,feature1,feature2):
    
    if not State:
        State = "All"
     
    df = comparisons_df[comparisons_df['State']==State]
    
    fig = make_subplots(rows=2, cols=1, subplot_titles = (feature1, feature2))
    
    
    for i,feature in enumerate([feature1,feature2]):
        for column in columns_mapping[feature]:
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
    
    
    fig.update_layout(color_discrete_sequence=px.colors.qualitative.G10)
    
    return fig 




