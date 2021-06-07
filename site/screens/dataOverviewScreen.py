import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import plotly.express as px
import pickle
import pandas as pd
from utils.dataOverviewUtil import drawImportanceChart 

# load datasets
sources = pickle.load(open('../data/sourceDist.pkl', 'rb'))
quants = pd.Series(pickle.load(open('../data/quants.pkl', 'rb')))
feat = pickle.load(open('../data/featureImportance.pkl', 'rb'))
figure_importance = drawImportanceChart(feat)
data_sources= {'Source':list(sources.keys()),'Count':list(sources.values())}

layout = html.Div(id='data-overview-screen', className='', children=
    [
        html.Div(className='row flex-display', children=
        [
            html.Div(className='pretty_container six columns', children= 
            [
                html.H4('Data Sources'),
                dcc.Graph(id='source-distributions',
                    figure=px.pie(data_sources, names='Source',values='Count')
                ),

            ]),
            html.Div(className='pretty_container six columns', children=
            [
                html.H4('Features Impacting Accident Duration'),
                dcc.Graph(id='importance',
                    figure=figure_importance
                )
            ]),
        ]),
        html.Div(className='row flex-display', children=
        [
            html.Div(className='pretty_container twelve columns', children= 
            [
                html.H4('Distribution of Accident Duration'),
                dcc.Graph(id='quantiles-accident-duration',
                    figure=px.bar(quants,labels={'index':'Quantile','value':'Duration of accident (minutes)'})
                ),
            ]),
        ])
        # html.Div(className='nav-button-next', children=
        #     [
        #         html.A('Next', href='#states-screen')
        #     ]
        # )
    ]
)