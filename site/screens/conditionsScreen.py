import dash_html_components as html
import pickle
from app import app
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import plotly.express as px
import sys
def load_obj(name ):
    with open('./' + name + '.pkl', 'rb') as f:
        return pickle.load(f)
CA_name = 'CA'
CA_counties_name = 'CA_county' 
CA_dict_df = load_obj(CA_name)
CA_counties = load_obj(CA_counties_name)
fig_names = ['Rain', 'Clear','Fog','Snow','Cloudy','Dust', 'All Weather']
fig_names2 = ['Day','Noon','Night', 'All Times of Day']     
fig_dropdown = html.Div([html.Div([
    dcc.Dropdown(
        id='fig_dropdown',
        options=[{'label': x, 'value': x} for x in fig_names],
        value=None
    )]), html.Div([
    dcc.Dropdown(
        id='fig_dropdown2',
        options=[{'label': x, 'value': x} for x in fig_names2],
        value=None
    )]) ]) #new

fig_plot = html.Div(id='fig_plot')
app.layout = html.Div([fig_dropdown, fig_plot])
layout = html.Div(className='row content-screen second', children=
    [
        html.H1('''Section 2: Traffic Collisions by Condition'''),
        fig_dropdown,
        fig_plot
        
    ]
)


@app.callback(dash.dependencies.Output('fig_plot', 'children'), [dash.dependencies.Input('fig_dropdown', 'value'),dash.dependencies.Input('fig_dropdown2', 'value')])

def update_output(fig_name,fig_name2):
    return name_to_figure(fig_name,fig_name2)

def name_to_figure(fig_name,fig_name2):
    
    if fig_name == None or 'All' in fig_name:
        fig_name = 'All'
    if fig_name2 == None or  'All' in fig_name2:
        fig_name2 = ''
    else:
        fig_name2 = '+' + fig_name2
        
    color_name = fig_name + fig_name2
    figure = px.choropleth(CA_dict_df, geojson=CA_counties, color=color_name,
                    locations="FIP", featureidkey="id",
                    projection="mercator"
                    ).update_geos(fitbounds="locations", visible=False)

    return dcc.Graph(figure=figure)