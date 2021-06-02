import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import plotly.express as px
import pickle
import pandas as pd
from utils.dataOverviewUtil import preprocessFeatureData


# load datasets
sources = pickle.load(open('../data/sourceDist.pkl', 'rb'))
quants = pd.Series(pickle.load(open('../data/quants.pkl', 'rb')))
feat = pickle.load(open('../data/featureImportance.pkl', 'rb'))
final = preprocessFeatureData(feat)


# process importance

layout = html.Div(id='data-overview-screen', className='', children=
    [
        html.Div(className='row flex-display', children=
        [
            html.Div(className='pretty_container six columns', children= 
            [
                dcc.Graph(id='source-distributions',
                    figure=px.bar(sources,title='Data Sources')
                ),

            ]),
            html.Div(className='pretty_container six columns', children=
            [
                dcc.Graph(id='importance',
                    figure=px.pie(final,values='Impact',names='Feature',title='Feature Importance')
                )
            ]),
        ]),
        html.Div(className='row flex-display', children=
        [
            html.Div(className='pretty_container twelve columns', children= 
            [
                dcc.Graph(id='quantiles-accident-duration',
                    figure=px.bar(quants,title='Quantiles of accident Duration')
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