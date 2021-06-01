import pandas as pd
import plotly.express as px
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app

# load dataset
accidents = pd.read_csv("data/accidents_visualization.csv")

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

layout = html.Div(className='content-screen', children=
    [
        html.H2("Number of accidents for each state"),
        html.Div(
            [
                html.Div(
                    [
                        html.H3('States'),
                        dcc.Dropdown(
                            options=states_dict,
                            multi=True,
                            id="states"
                        )  
                    ], className="six columns"),
            ], className="container"),
    dcc.Graph(figure=fig, id="graph",style={"height": 500})
])

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
    