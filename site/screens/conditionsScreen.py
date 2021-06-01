import dash_html_components as html
import pickle
from app import app
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import plotly.express as px
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
    # Rain Weather
    if fig_name == 'Rain' and fig_name2 == 'Day':
        figure = px.choropleth(CA_dict_df, geojson=CA_counties, color='Rain+Day',
                    locations="FIP", featureidkey="id",
                    projection="mercator"
                    ).update_geos(fitbounds="locations", visible=False)

    elif fig_name == 'Rain' and fig_name2 == 'Noon': 
        figure = px.choropleth(CA_dict_df, geojson=CA_counties, color='Rain+Noon',
                    locations="FIP", featureidkey="id",
                    projection="mercator"
                    ).update_geos(fitbounds="locations", visible=False)

    elif fig_name == 'Rain' and fig_name2 == 'Night': 
        figure = px.choropleth(CA_dict_df, geojson=CA_counties, color='Rain+Night',
                    locations="FIP", featureidkey="id",
                    projection="mercator"
                    ).update_geos(fitbounds="locations", visible=False)
    elif fig_name == 'Rain' and fig_name2 == 'All Times of Day': 
        figure = px.choropleth(CA_dict_df, geojson=CA_counties, color='Rain',
                    locations="FIP", featureidkey="id",
                    projection="mercator"
                    ).update_geos(fitbounds="locations", visible=False)    
    # Clear Weather
    elif fig_name == 'Clear' and fig_name2 == 'Day': 
        figure = px.choropleth(CA_dict_df, geojson=CA_counties, color='Clear+Day',
                    locations="FIP", featureidkey="id",
                    projection="mercator"
                    ).update_geos(fitbounds="locations", visible=False)
    elif fig_name == 'Clear' and fig_name2 == 'Noon': 
        figure = px.choropleth(CA_dict_df, geojson=CA_counties, color='Clear+Noon',
                    locations="FIP", featureidkey="id",
                    projection="mercator"
                    ).update_geos(fitbounds="locations", visible=False)
    elif fig_name == 'Clear' and fig_name2 == 'Night': 
        figure = px.choropleth(CA_dict_df, geojson=CA_counties, color='Clear+Night',
                    locations="FIP", featureidkey="id",
                    projection="mercator"
                    ).update_geos(fitbounds="locations", visible=False)
    elif fig_name == 'Clear' and fig_name2 == 'All Times of Day': 
        figure = px.choropleth(CA_dict_df, geojson=CA_counties, color='Clear',
                    locations="FIP", featureidkey="id",
                    projection="mercator"
                    ).update_geos(fitbounds="locations", visible=False)
    # Fog Weather
    elif fig_name == 'Fog' and fig_name2 == 'Day': 
        figure = px.choropleth(CA_dict_df, geojson=CA_counties, color='Fog+Day',
                    locations="FIP", featureidkey="id",
                    projection="mercator"
                    ).update_geos(fitbounds="locations", visible=False)
    elif fig_name == 'Fog' and fig_name2 == 'Noon': 
        figure = px.choropleth(CA_dict_df, geojson=CA_counties, color='Fog+Noon',
                    locations="FIP", featureidkey="id",
                    projection="mercator"
                    ).update_geos(fitbounds="locations", visible=False)
    elif fig_name == 'Fog' and fig_name2 == 'Night': 
        figure = px.choropleth(CA_dict_df, geojson=CA_counties, color='Fog+Night',
                    locations="FIP", featureidkey="id",
                    projection="mercator"
                    ).update_geos(fitbounds="locations", visible=False)
    elif fig_name == 'Fog' and fig_name2 == 'All Times of Day': 
        figure = px.choropleth(CA_dict_df, geojson=CA_counties, color='Fog',
                    locations="FIP", featureidkey="id",
                    projection="mercator"
                    ).update_geos(fitbounds="locations", visible=False)
    # Snow Weather
    elif fig_name == 'Snow' and fig_name2 == 'Day': 
        figure = px.choropleth(CA_dict_df, geojson=CA_counties, color='Snow+Day',
                    locations="FIP", featureidkey="id",
                    projection="mercator"
                    ).update_geos(fitbounds="locations", visible=False)
    elif fig_name == 'Snow' and fig_name2 == 'Noon': 
        figure = px.choropleth(CA_dict_df, geojson=CA_counties, color='Snow+Noon',
                    locations="FIP", featureidkey="id",
                    projection="mercator"
                    ).update_geos(fitbounds="locations", visible=False)
    elif fig_name == 'Snow' and fig_name2 == 'Night': 
        figure = px.choropleth(CA_dict_df, geojson=CA_counties, color='Snow+Night',
                    locations="FIP", featureidkey="id",
                    projection="mercator"
                    ).update_geos(fitbounds="locations", visible=False)
    elif fig_name == 'Snow' and fig_name2 == 'All Times of Day': 
        figure = px.choropleth(CA_dict_df, geojson=CA_counties, color='Snow',
                    locations="FIP", featureidkey="id",
                    projection="mercator"
                    ).update_geos(fitbounds="locations", visible=False)
    # Cloudy Weather
    elif fig_name == 'Cloudy' and fig_name2 == 'Day': 
        figure = px.choropleth(CA_dict_df, geojson=CA_counties, color='Cloudy+Day',
                    locations="FIP", featureidkey="id",
                    projection="mercator"
                    ).update_geos(fitbounds="locations", visible=False)
    elif fig_name == 'Cloudy' and fig_name2 == 'Noon': 
        figure = px.choropleth(CA_dict_df, geojson=CA_counties, color='Cloudy+Noon',
                    locations="FIP", featureidkey="id",
                    projection="mercator"
                    ).update_geos(fitbounds="locations", visible=False)
    elif fig_name == 'Cloudy' and fig_name2 == 'Night': 
        figure = px.choropleth(CA_dict_df, geojson=CA_counties, color='Cloudy+Night',
                    locations="FIP", featureidkey="id",
                    projection="mercator"
                    ).update_geos(fitbounds="locations", visible=False)
    elif fig_name == 'Cloudy' and fig_name2 == 'All Times of Day': 
        figure = px.choropleth(CA_dict_df, geojson=CA_counties, color='Cloudy',
                    locations="FIP", featureidkey="id",
                    projection="mercator"
                    ).update_geos(fitbounds="locations", visible=False)
    # Dust Weather
    elif fig_name == 'Dust' and fig_name2 == 'Day': 
        figure = px.choropleth(CA_dict_df, geojson=CA_counties, color='Dust+Day',
                    locations="FIP", featureidkey="id",
                    projection="mercator"
                    ).update_geos(fitbounds="locations", visible=False)
    elif fig_name == 'Dust' and fig_name2 == 'Noon': 
        figure = px.choropleth(CA_dict_df, geojson=CA_counties, color='Dust+Noon',
                    locations="FIP", featureidkey="id",
                    projection="mercator"
                    ).update_geos(fitbounds="locations", visible=False)
    elif fig_name == 'Dust' and fig_name2 == 'Night': 
        figure = px.choropleth(CA_dict_df, geojson=CA_counties, color='Dust+Night',
                    locations="FIP", featureidkey="id",
                    projection="mercator"
                    ).update_geos(fitbounds="locations", visible=False)
    elif fig_name == 'Dust' and fig_name2 == 'All Times of Day': 
        figure = px.choropleth(CA_dict_df, geojson=CA_counties, color='Dust',
                    locations="FIP", featureidkey="id",
                    projection="mercator"
                    ).update_geos(fitbounds="locations", visible=False)
    # For All time of Day
    elif fig_name == 'All Weather' and fig_name2 == 'Day': 
        figure = px.choropleth(CA_dict_df, geojson=CA_counties, color='Day',
                    locations="FIP", featureidkey="id",
                    projection="mercator"
                    ).update_geos(fitbounds="locations", visible=False)
    elif fig_name == 'All Weather' and fig_name2 == 'Noon': 
        figure = px.choropleth(CA_dict_df, geojson=CA_counties, color='Noon',
                    locations="FIP", featureidkey="id",
                    projection="mercator"
                    ).update_geos(fitbounds="locations", visible=False)
    elif fig_name == 'All Weather' and fig_name2 == 'Night': 
        figure = px.choropleth(CA_dict_df, geojson=CA_counties, color='Night',
                    locations="FIP", featureidkey="id",
                    projection="mercator"
                    ).update_geos(fitbounds="locations", visible=False)
    elif fig_name == 'All Weather' and fig_name2 == 'All Times of Day': 
        figure = px.choropleth(CA_dict_df, geojson=CA_counties, color='All',
                    locations="FIP", featureidkey="id",
                    projection="mercator"
                    ).update_geos(fitbounds="locations", visible=False)
    return dcc.Graph(figure=figure)