# -*- coding: utf-8 -*-
"""
Created on Sun May 30 22:28:14 2021

@author: srist
"""


import pandas as pd
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app

accidents = pd.read_csv("data/accidents_visualization.csv")

num_frames = len(accidents['year_month'].unique())
fig = px.choropleth(accidents,               
                  locations="State",               
                  color="counts per million",
                  hover_name="State", 
                  locationmode="USA-states",
                  animation_frame="year_month", 
                  color_continuous_scale='Plasma', 
                  range_color=(0, 60),
                  height=500,
                  scope='usa'
    )
fig.update_layout(geo_scope="usa")

States_names = list(accidents['State'].unique())
States_names.sort()
States_names.insert(0,'All')
states_dict = [{'label': state, 'value': state} for state in States_names]

layout = html.Div(id='states-screen', className='row flex-display', children=
    [
        html.Div(className="pretty_container four columns", children=
        [
            html.H4("Number of accidents for each state"),
            html.Div(className='input-field', children=
            [
                html.Div([
                    html.H5('States'),
                    dcc.Dropdown(
                        options=states_dict,
                        multi=True,
                        value=["All"],
                        id="states"
                    )  
                ]),
            ]),
            html.Div( className='input-field', children=
            [
                html.H5('Normalization'),
                dcc.RadioItems(
                    options=[
                        {'label': 'without Normalization', 'value': 'without Normalization'},
                        {'label': 'per million people', 'value': 'per million people'}
                    ],
                    value='per million people',
                    id='normalization'
                    )  
            ]),
        ]),
        html.Div(className="pretty_container eight columns", children=
        [
            dcc.Graph(id="graph",style={"height": 500}),
        ])
    ]

    # html.Div(className='nav-button-next', children=
    #     [
    #         html.A('Next', href='#conditions-screen')
    #     ]
    # )
)


@app.callback(Output("graph", "figure"), 
                        [Input('states', 'value'),
                        Input('normalization','value')])
def update_graphs(states,normalization):
    
    if not states:
        states = ["All"]
        
    if 'All' in states:
        
        df = accidents
    else:
        df = accidents[accidents['State'].isin(states)]
    if normalization=='without Normalization':
        color_column  = "counts"
        color_range = (0, 10000)
    elif normalization=='per million people':
        color_column  = "counts per million"
        
        if 'All' in states:
            color_range = (0, 60)
        else:
            color_range = (int(df['counts per million'].min()),
                           int(df['counts per million'].max()))
        
    else:
        # Default column is "counts"
        color_column  = "counts"
        color_range = (0, 10000)
        
    fig = px.choropleth(df,
                        locations="State",               
                        color=color_column,
                        hover_name="State", 
                        locationmode="USA-states",    
                        color_continuous_scale='Plasma',  
                        range_color=color_range,
                        height=500,
                        scope='usa',
                        animation_frame="year_month",
                        # category_orders = {'frames':list(range(1,num_frames+1))},
                        )
    fig.update_layout(geo_scope="usa")
    

    
    return fig 