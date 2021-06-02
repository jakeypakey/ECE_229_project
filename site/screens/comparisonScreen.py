# -*- coding: utf-8 -*-
"""
Created on Tue Jun  1 17:37:49 2021

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

comparisons_df = pd.read_csv("comparisons_impute.csv")

comparisons_df = comparisons_df.rename(columns={'Severity_1.0':'Severity_1',
 'Severity_2.0':'Severity_2',
 'Severity_3.0':'Severity_3',
 'Severity_4.0':'Severity_4'})

comparisons_df_normalize = pd.read_csv("comparisons_impute_normalize.csv")
comparisons_df_normalize = comparisons_df_normalize.rename(columns={'Severity_1.0':'Severity_1',
 'Severity_2.0':'Severity_2',
 'Severity_3.0':'Severity_3',
 'Severity_4.0':'Severity_4'})

thres_category = {'Pressure':{'thresolds':[29.5,30.2],
                              'category':['Low','Moderate','High']},
                  'AccidentDuration':{'thresolds':[35,50,70,90],
                              'category':['Very Low','Low','Moderate','High','Very High']},
                  'Temperature':{'thresolds':[0,30,60,80,100],
                              'category':['VeryVeryLow','VeryLow','Low','Moderate','High','VeryHigh']},
                  'WindSpeed':{'thresolds':[8,13,19,25],
                              'category':['Calm','GentleBreeze','ModerateBreeze','FreshBreeze','StrongBreeze']},
                  'Humidity':{'thresolds':[30,50],
                              'category':['Low','Moderate','High']},
                  'TimeOfDay':{'thresolds':[6,12,18],
                              'category':['Night','Day','Noon','Night']},
                 }
thres_category['TimeOfDay']['category'] = ['Day','Noon','Night']

thres_category['DayOfWeek'] = {'thresolds':[],
                               'category':["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]}

columns = list(comparisons_df.keys())
features = list(comparisons_df.keys())
for column in ['State', 'year_month','Month', 'Year']:
    features.remove(column)
features = np.unique([column.split("_")[0] for column in features] ) 
features_dict = [{'label': feature, 'value': feature} for feature in features]

columns_mapping = {}
for feature in features:
    # columns_mapping[feature] = [column for column in columns if feature in column]
    if feature not in thres_category.keys():
        columns_mapping[feature] = [column for column in columns if feature in column]
    else:
        columns_mapping[feature] = [feature+'_'+value for value in thres_category[feature]['category']]
        
# print(features_dict)




legend_names = {}
for feature in columns_mapping:
    
    if feature not in thres_category or feature=="DayOfWeek":
        for col in columns_mapping[feature]:
            legend_names[col] = col.replace(feature+"_","")
    else:
        if feature=="TimeOfDay":
            legend_names["TimeOfDay_Day"] = "Day (6:00-11:59)"
            legend_names["TimeOfDay_Noon"] = "Noon (12:00-17:59)"
            legend_names["TimeOfDay_Night"] = "Night (18:00-5:59)"
            
        else:
            for idx,col in enumerate(columns_mapping[feature]):
                if idx==0:
                    legend_names[col] = col.replace(feature+"_","")+" (<"+str(thres_category[feature]['thresolds'][0])+")"
                elif idx==len(feature)-1:
                    legend_names[col] = col.replace(feature+"_","")+" (>"+str(thres_category[feature]['thresolds'][-1])+")"
                else:
                    legend_names[col] = col.replace(feature+"_","")+" ("+str(thres_category[feature]['thresolds'][idx-1])+"-"+str(thres_category[feature]['thresolds'][idx-1])+")"


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


    # ], className="container"),
    
    html.Div([
        # html.Div([
        #     html.H3('States'),
        #     dcc.Dropdown(
        #         options=states_dict,
        #         multi=False,
        #         value="All",
        #         id="states"
        #     )  
        # ], className="six columns"),
        
        html.Div([
            # html.H3('Normalization'),
            html.Div([
                html.H3('States'),
                dcc.Dropdown(
                    options=states_dict,
                    multi=False,
                    value="All",
                    id="states"
                ) , ]),
            html.Div([
                html.H3('y-axis'),
                dcc.RadioItems(
                options=[
                    {'label': '#Accidents', 'value': '#Accidents'},
                    {'label': 'percentage', 'value': 'percentage'}
                ],
                value='#Accidents',
                id='normalization'
                )  
                ]) ]),
        
        # html.Div([
        #     html.H3('Date'),
        #     dcc.RangeSlider(
        #                     id='rangeslider',
        #                     min=0,
        #                     max=accidents['year_month'].nunique()-1,
        #                     value=[0, accidents['year_month'].nunique()-1],
        #                     allowCross=False
        #                     )
        # ], className="six columns"),
        
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
                    value="AccidentDuration",
                    id="feature2"
                )  ])
            
            # dcc.RadioItems(
            #     options=[
            #         {'label': 'without Normalization', 'value': 'without Normalization'},
            #         {'label': 'per million people', 'value': 'per million people'}
            #     ],
            #     value='per million people',
            #     id='normalization'
            #     )  
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
                        Input('feature2','value'),
                        Input('normalization','value')])
def update_graphs(State,year,feature1,feature2,normalization):
    
    if not State:
        State = "All"
    
    if normalization=='#Accidents': 
        df = comparisons_df[comparisons_df['State']==State]
        
    elif normalization=='percentage':
        df = comparisons_df_normalize[comparisons_df['State']==State]
    
    fig = make_subplots(rows=2, cols=1, subplot_titles = (feature1, feature2))
    
    
    for i,feature in enumerate([feature1,feature2]):
        for column in columns_mapping[feature]:
            fig.add_trace(go.Bar(
                y=df[df['Year']==year][column],
                x=list(range(1,13)),
                name=column.replace(feature+"_",""), #legend_names[column],#
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
    max_range = df[columns_mapping['TimeOfDay']].sum(axis=1).max()
    fig.update_yaxes(title_text=normalization,range=[0,max_range])

    return fig 



# app.run_server(d