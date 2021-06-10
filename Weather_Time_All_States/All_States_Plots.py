#!/usr/bin/env python
# coding: utf-8

# In[1]:


import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from urllib.request import urlopen
import json
import pandas as pd
import plotly.express as px
import numpy as np
from collections import Counter
import pickle


# In[2]:


# Data Loader
# processed_data = pd.read_csv('processed_data_all_states.csv', usecols = ['ID','Start_Time','Weather_Condition','Start_Lat','Start_Lng','County',                                       'Time of Day','State','FIP'])

# with open('fip_dict_pop.pickle', 'rb') as handle:
#     fip_dict_pop = pickle.load(handle)
# with open('fipkey_popvalue.pickle', 'rb') as handle:
#     fipkey_popvalue = pickle.load(handle)


# In[3]:


def population_norm(histogram, fipkey_popvalue):
    '''Normalize histogram by population per 1000 people  
    
    :param histogram: Unnormalized histogram
    :type histogram: np.array
    :param fipkey_popvalue: FIP keys to number of accidents values
    :type fipkey_popvalue: dict
    '''
    if histogram == {}:
        return {}
    raw_id = list(histogram.keys())[0]
    state_key = ('0'*(5-len(str(raw_id))) + str(raw_id))[:2]
    st_dict = {key: value for key, value in fipkey_popvalue.items() if key[:2] == state_key}
    for key, value in histogram.items():
        str_key = '0'*(5-len(str(key))) + str(key)
        histogram[key] = value / st_dict[str_key] * 1000
    return histogram


# In[4]:


def processing_data(processed_data, CA_fip_dict,fipkey_popvalue):
    '''Converts the csv file into dataframe of categories vs accidents.
    
    :param processed_data: pandas dataframe of data
    :type processed_data: pd.df
    :param CA_fip_dict: all FIP values
    :type CA_fip_dict: dict
    :param fipkey_popvalue: FIP keys to number of accidents values
    :type fipkey_popvalue: dict
    '''
    # Sort data into weather
    processed_data = np.array(processed_data)
    data_rain = processed_data[processed_data[:,2] == 'Rain']
    data_clear = processed_data[processed_data[:,2] == 'Clear']
    data_fog = processed_data[processed_data[:,2] == 'Fog']
    data_snow = processed_data[processed_data[:,2] == 'Snow']
    data_cloudy = processed_data[processed_data[:,2] == 'Cloudy']
    data_dust = processed_data[processed_data[:,2] == 'Dust']
    # Initialize the 18 data matrices
    data_rain_day, data_rain_noon, data_rain_night = [], [], []
    data_clear_day, data_clear_noon, data_clear_night = [], [], []
    data_fog_day, data_fog_noon, data_fog_night = [], [], []
    data_snow_day, data_snow_noon, data_snow_night = [], [], []
    data_cloudy_day, data_cloudy_noon, data_cloudy_night = [], [], []
    data_dust_day, data_dust_noon, data_dust_night = [], [], []
    for i in range(data_rain.shape[0]):
        if data_rain[i,6] == 'day':
            data_rain_day.append(data_rain[i])
        elif data_rain[i,6] == 'noon':
            data_rain_noon.append(data_rain[i])
        else:
            data_rain_night.append(data_rain[i])
    for i in range(data_clear.shape[0]):
        if data_clear[i,6] == 'day':
            data_clear_day.append(data_clear[i])
        elif data_clear[i,6] == 'noon':
            data_clear_noon.append(data_clear[i])
        else:
            data_clear_night.append(data_clear[i])
    for i in range(data_fog.shape[0]):
        if data_fog[i,6] == 'day':
            data_fog_day.append(data_fog[i])
        elif data_fog[i,6] == 'noon':
            data_fog_noon.append(data_fog[i])
        else:
            data_fog_night.append(data_fog[i])
    for i in range(data_snow.shape[0]):
        if data_snow[i,6] == 'day':
            data_snow_day.append(data_snow[i])
        elif data_snow[i,6] == 'noon':
            data_snow_noon.append(data_snow[i])
        else:
            data_snow_night.append(data_snow[i])
    for i in range(data_cloudy.shape[0]):
        if data_cloudy[i,6] == 'day':
            data_cloudy_day.append(data_cloudy[i])
        elif data_cloudy[i,6] == 'noon':
            data_cloudy_noon.append(data_cloudy[i])
        else:
            data_cloudy_night.append(data_cloudy[i])
    for i in range(data_dust.shape[0]):
        if data_dust[i,6] == 'day':
            data_dust_day.append(data_dust[i])
        elif data_dust[i,6] == 'noon':
            data_dust_noon.append(data_dust[i])
        else:
            data_dust_night.append(data_dust[i])

    # Rain Data FIPs
    rain_fips_day = np.array(data_rain_day)[:,-1]
    rain_fips_noon = np.array(data_rain_noon)[:,-1]
    rain_fips_night = np.array(data_rain_night)[:,-1]

    # Clear Data FIPs
    clear_fips_day = np.array(data_cloudy_day)[:,-1]
    clear_fips_noon = np.array(data_cloudy_noon)[:,-1]
    clear_fips_night = np.array(data_cloudy_night)[:,-1]
    # Fog Data FIPs
    fog_fips_day = np.array(data_fog_day)[:,-1]
    fog_fips_noon = np.array(data_fog_noon)[:,-1]
    fog_fips_night = np.array(data_fog_night)[:,-1]
    # Snow Data FIPs
    snow_fips_day = np.array(data_snow_day)[:,-1]
    snow_fips_noon = np.array(data_snow_noon)[:,-1]
    snow_fips_night = np.array(data_snow_night)[:,-1]
    # Cloudy Data FIPs
    cloudy_fips_day = np.array(data_cloudy_day)[:,-1]
    cloudy_fips_noon = np.array(data_cloudy_noon)[:,-1]
    cloudy_fips_night = np.array(data_cloudy_night)[:,-1]
    # Dust Data FIPs
    if len(data_dust_day) == 0:
        dust_fips_day = []
    else:   
        dust_fips_day = np.array(data_dust_day)[:,-1]
    if len(data_dust_noon) == 0:
        dust_fips_noon = []
    else:
        dust_fips_noon = np.array(data_dust_noon)[:,-1]
    if len(data_dust_night) == 0:
        dust_fips_night = []
    else:
        dust_fips_night = np.array(data_dust_night)[:,-1]
    # Create Count of Accidents for Weather / Time of Day
    rain_day_fip_hist = population_norm(Counter(rain_fips_day),fipkey_popvalue)
    rain_noon_fip_hist = population_norm(Counter(rain_fips_noon),fipkey_popvalue)
    rain_night_fip_hist = population_norm(Counter(rain_fips_night),fipkey_popvalue)
    clear_day_fip_hist = population_norm(Counter(clear_fips_day),fipkey_popvalue)
    clear_noon_fip_hist = population_norm(Counter(clear_fips_noon),fipkey_popvalue)
    clear_night_fip_hist = population_norm(Counter(clear_fips_night),fipkey_popvalue)
    fog_day_fip_hist = population_norm(Counter(fog_fips_day),fipkey_popvalue)
    fog_noon_fip_hist = population_norm(Counter(fog_fips_noon),fipkey_popvalue)
    fog_night_fip_hist = population_norm(Counter(fog_fips_night),fipkey_popvalue)
    snow_day_fip_hist = population_norm(Counter(snow_fips_day),fipkey_popvalue)
    snow_noon_fip_hist = population_norm(Counter(snow_fips_noon),fipkey_popvalue)
    snow_night_fip_hist = population_norm(Counter(snow_fips_night),fipkey_popvalue)
    cloudy_day_fip_hist = population_norm(Counter(cloudy_fips_day),fipkey_popvalue)
    cloudy_noon_fip_hist = population_norm(Counter(cloudy_fips_noon),fipkey_popvalue)
    cloudy_night_fip_hist = population_norm(Counter(cloudy_fips_night),fipkey_popvalue)
    dust_day_fip_hist = population_norm(Counter(dust_fips_day),fipkey_popvalue)
    dust_noon_fip_hist = population_norm(Counter(dust_fips_noon),fipkey_popvalue)
    dust_night_fip_hist = population_norm(Counter(dust_fips_night),fipkey_popvalue)

    # Combine all of them together
    fip_hist = [rain_day_fip_hist,rain_noon_fip_hist,rain_night_fip_hist, clear_day_fip_hist, clear_noon_fip_hist, 
                clear_night_fip_hist,fog_day_fip_hist,fog_noon_fip_hist,fog_night_fip_hist,snow_day_fip_hist,
                snow_noon_fip_hist,snow_night_fip_hist,cloudy_day_fip_hist,cloudy_noon_fip_hist,
                cloudy_night_fip_hist,dust_day_fip_hist,dust_noon_fip_hist,dust_night_fip_hist]

    # Push to Key and Value Pairs for Data matching
    rain_day_fip_vals, rain_day_values = list(rain_day_fip_hist.keys()),list(rain_day_fip_hist.values())
    rain_noon_fip_vals, rain_noon_values = list(rain_noon_fip_hist.keys()),list(rain_noon_fip_hist.values())
    rain_night_fip_vals, rain_night_values = list(rain_night_fip_hist.keys()),list(rain_night_fip_hist.values())
    clear_day_fip_vals, clear_day_values = list(clear_day_fip_hist.keys()),list(clear_day_fip_hist.values())
    clear_noon_fip_vals, clear_noon_values = list(clear_noon_fip_hist.keys()),list(clear_noon_fip_hist.values())
    clear_night_fip_vals, clear_night_values = list(clear_night_fip_hist.keys()),list(clear_night_fip_hist.values())
    fog_day_fip_vals, fog_day_values = list(fog_day_fip_hist.keys()),list(fog_day_fip_hist.values())
    fog_noon_fip_vals, fog_noon_values = list(fog_noon_fip_hist.keys()),list(fog_noon_fip_hist.values())
    fog_night_fip_vals, fog_night_values = list(fog_night_fip_hist.keys()),list(fog_night_fip_hist.values())
    snow_day_fip_vals, snow_day_values = list(snow_day_fip_hist.keys()),list(snow_day_fip_hist.values())
    snow_noon_fip_vals, snow_noon_values = list(snow_noon_fip_hist.keys()),list(snow_noon_fip_hist.values())
    snow_night_fip_vals, snow_night_values = list(snow_night_fip_hist.keys()),list(snow_night_fip_hist.values())
    cloudy_day_fip_vals, cloudy_day_values = list(cloudy_day_fip_hist.keys()),list(cloudy_day_fip_hist.values())
    cloudy_noon_fip_vals, cloudy_noon_values = list(cloudy_noon_fip_hist.keys()),list(cloudy_noon_fip_hist.values())
    cloudy_night_fip_vals, cloudy_night_values = list(cloudy_night_fip_hist.keys()),list(cloudy_night_fip_hist.values())
    dust_day_fip_vals, dust_day_values = list(dust_day_fip_hist.keys()),list(dust_day_fip_hist.values())
    dust_noon_fip_vals, dust_noon_values = list(dust_noon_fip_hist.keys()),list(dust_noon_fip_hist.values())
    dust_night_fip_vals, dust_night_values = list(dust_night_fip_hist.keys()),list(dust_night_fip_hist.values())
    
    FIP, pop = zip(*list(CA_fip_dict.values()))
    keyList = list(set(FIP))
    # Create the Dictionary splitting into weather 
    CA_dict = {key: [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] for key in keyList}
    for num, dictionary in enumerate(fip_hist):
        for key in dictionary:
            str_key = '0'*(5-len(str(key))) + str(key)
            CA_dict[str_key][num] = dictionary[key]
    CA_dict_df = pd.DataFrame.from_dict(CA_dict, orient='index', columns = ['Rain+Day','Rain+Noon','Rain+Night', 
                                                                            'Clear+Day','Clear+Noon','Clear+Night',
                                                                            'Fog+Day','Fog+Noon','Fog+Night',
                                                                            'Snow+Day','Snow+Noon','Snow+Night',
                                                                            'Cloudy+Day','Cloudy+Noon','Cloudy+Night',
                                                                            'Dust+Day','Dust+Noon','Dust+Night'])
    CA_dict_df['FIP'] = [str(fip) for fip in CA_dict_df.index]
    # Add Weather Only Columns
    CA_dict_df.insert(0,'Rain', list(CA_dict_df["Rain+Day"]+CA_dict_df["Rain+Noon"]+CA_dict_df["Rain+Night"]), True)
    CA_dict_df.insert(0,'Clear', list(CA_dict_df["Clear+Day"]+CA_dict_df["Clear+Noon"]+CA_dict_df["Clear+Night"]), True)
    CA_dict_df.insert(0,'Fog', list(CA_dict_df["Fog+Day"]+CA_dict_df["Fog+Noon"]+CA_dict_df["Fog+Night"]), True)
    CA_dict_df.insert(0,'Snow', list(CA_dict_df["Snow+Day"]+CA_dict_df["Snow+Noon"]+CA_dict_df["Snow+Night"]), True)
    CA_dict_df.insert(0,'Cloudy', list(CA_dict_df["Cloudy+Day"]+CA_dict_df["Cloudy+Noon"]+CA_dict_df["Cloudy+Night"]), True)
    CA_dict_df.insert(0,'Dust', list(CA_dict_df["Dust+Day"]+CA_dict_df["Dust+Noon"]+CA_dict_df["Dust+Night"]), True)
    # Add Time of Day Only Columns
    CA_dict_df.insert(0,'Day', list(CA_dict_df["Rain+Day"]+CA_dict_df["Clear+Day"]+CA_dict_df["Fog+Day"]+CA_dict_df["Snow+Day"]+CA_dict_df["Cloudy+Day"]+CA_dict_df["Dust+Day"])
    , True)
    CA_dict_df.insert(0,'Noon', list(CA_dict_df["Rain+Noon"]+CA_dict_df["Clear+Noon"]+CA_dict_df["Fog+Noon"]+CA_dict_df["Snow+Noon"]+CA_dict_df["Cloudy+Noon"]+CA_dict_df["Dust+Noon"])
    , True)
    CA_dict_df.insert(0,'Night', list(CA_dict_df["Rain+Night"]+CA_dict_df["Clear+Night"]+CA_dict_df["Fog+Night"]+CA_dict_df["Snow+Night"]+CA_dict_df["Cloudy+Night"]+CA_dict_df["Dust+Night"])
    , True)
    # Add an All Column
    CA_dict_df.insert(0,'All', list(CA_dict_df["Day"]+CA_dict_df["Noon"]+CA_dict_df["Night"]), True)
    CA_dict_df.index = range(len(CA_dict_df))
    
    return CA_dict_df


# In[5]:


def get_counties(starter_fip):
    '''Get the geojson dictionary necessary for DASH plot
    
    :param starter_fip: state abbreviation
    :type starter_fip: string
    '''
    with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
        counties = json.load(response)
    CA_counties = {'type':'FeatureCollection','features':[]}
    for info in counties['features']:
        if info['properties']['STATE'] == starter_fip:
            CA_counties['features'].append(info)
    return CA_counties


# In[6]:


def plot_double_dropdown_chloropleth(processed_data,fip_dict, fipkey_popvalue):
    '''Dash interface - plots heatmap of california vehicle accidents given weather and time.
    
    :param processed_data: pandas dataframe of data
    :type processed_data: pd.df 
    :param fip_dict: all FIP values
    :type fip_dict: dict
    :param fipkey_popvalue: FIP keys to number of accidents values
    :type fipkey_popvalue: dict

    '''
    county_state = processed_data['County'] + ' ' + processed_data['State']
    fip = []
    for fip_id in processed_data['FIP']:
        fip.append('0'*(5-len(str(fip_id)))+str(fip_id))
    processed_data['FIP'] = fip
    app = dash.Dash()

    fig_names = ["AL", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA", 
          "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", 
          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", 
          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]
    fig_names2 = ['Rain', 'Clear','Fog','Snow','Cloudy','Dust', 'All Weather']
    fig_names3 = ['Day','Noon','Night', 'All Times of Day']
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
        )]), html.Div([
        dcc.Dropdown(
            id='fig_dropdown3',
            options=[{'label': x, 'value': x} for x in fig_names3],
            value=None
        )]) ]) #new

    fig_plot = html.Div(id='fig_plot')
    app.layout = html.Div([fig_dropdown, fig_plot])

    @app.callback(dash.dependencies.Output('fig_plot', 'children'), [dash.dependencies.Input('fig_dropdown', 'value'),                                                                     dash.dependencies.Input('fig_dropdown2', 'value'),                                                                     dash.dependencies.Input('fig_dropdown3', 'value')])

    def update_output(fig_name,fig_name2, fig_name3):
        return name_to_figure(fig_name,fig_name2, fig_name3)
    
    def name_to_figure(fig_name,fig_name2, fig_name3):
        state_dict = {}
        state = fig_name
        for key in fip_dict:
            if key.split(' ')[-1] == state:
                state_dict[key] = fip_dict[key]

        # Filter processed_data by state
        state_processed_data = processed_data[processed_data['State'] == state]
        CA_dict_df = processing_data(state_processed_data, state_dict, fipkey_popvalue)
        state_code_start = np.array(CA_dict_df)[0,-1][:2]
        CA_counties = get_counties(state_code_start) 
        
        # Rain Weather
        if fig_name2 == 'Rain' and fig_name3 == 'Day':
            figure = px.choropleth(CA_dict_df, geojson=CA_counties, color='Rain+Day',
                        locations="FIP", featureidkey="id",
                        projection="mercator"
                        ).update_geos(fitbounds="locations", visible=False)

        elif fig_name2 == 'Rain' and fig_name3 == 'Noon': 
            figure = px.choropleth(CA_dict_df, geojson=CA_counties, color='Rain+Noon',
                        locations="FIP", featureidkey="id",
                        projection="mercator"
                        ).update_geos(fitbounds="locations", visible=False)

        elif fig_name2 == 'Rain' and fig_name3 == 'Night': 
            figure = px.choropleth(CA_dict_df, geojson=CA_counties, color='Rain+Night',
                        locations="FIP", featureidkey="id",
                        projection="mercator"
                        ).update_geos(fitbounds="locations", visible=False)
        elif fig_name2 == 'Rain' and fig_name3 == 'All Times of Day': 
            figure = px.choropleth(CA_dict_df, geojson=CA_counties, color='Rain',
                        locations="FIP", featureidkey="id",
                        projection="mercator"
                        ).update_geos(fitbounds="locations", visible=False)    
        # Clear Weather
        elif fig_name2 == 'Clear' and fig_name3 == 'Day': 
            figure = px.choropleth(CA_dict_df, geojson=CA_counties, color='Clear+Day',
                        locations="FIP", featureidkey="id",
                        projection="mercator"
                        ).update_geos(fitbounds="locations", visible=False)
        elif fig_name2 == 'Clear' and fig_name3 == 'Noon': 
            figure = px.choropleth(CA_dict_df, geojson=CA_counties, color='Clear+Noon',
                        locations="FIP", featureidkey="id",
                        projection="mercator"
                        ).update_geos(fitbounds="locations", visible=False)
        elif fig_name2 == 'Clear' and fig_name3 == 'Night': 
            figure = px.choropleth(CA_dict_df, geojson=CA_counties, color='Clear+Night',
                        locations="FIP", featureidkey="id",
                        projection="mercator"
                        ).update_geos(fitbounds="locations", visible=False)
        elif fig_name2 == 'Clear' and fig_name3 == 'All Times of Day': 
            figure = px.choropleth(CA_dict_df, geojson=CA_counties, color='Clear',
                        locations="FIP", featureidkey="id",
                        projection="mercator"
                        ).update_geos(fitbounds="locations", visible=False)
        # Fog Weather
        elif fig_name2 == 'Fog' and fig_name3 == 'Day': 
            figure = px.choropleth(CA_dict_df, geojson=CA_counties, color='Fog+Day',
                        locations="FIP", featureidkey="id",
                        projection="mercator"
                        ).update_geos(fitbounds="locations", visible=False)
        elif fig_name2 == 'Fog' and fig_name3 == 'Noon': 
            figure = px.choropleth(CA_dict_df, geojson=CA_counties, color='Fog+Noon',
                        locations="FIP", featureidkey="id",
                        projection="mercator"
                        ).update_geos(fitbounds="locations", visible=False)
        elif fig_name2 == 'Fog' and fig_name3 == 'Night': 
            figure = px.choropleth(CA_dict_df, geojson=CA_counties, color='Fog+Night',
                        locations="FIP", featureidkey="id",
                        projection="mercator"
                        ).update_geos(fitbounds="locations", visible=False)
        elif fig_name2 == 'Fog' and fig_name3 == 'All Times of Day': 
            figure = px.choropleth(CA_dict_df, geojson=CA_counties, color='Fog',
                        locations="FIP", featureidkey="id",
                        projection="mercator"
                        ).update_geos(fitbounds="locations", visible=False)
        # Snow Weather
        elif fig_name2 == 'Snow' and fig_name3 == 'Day': 
            figure = px.choropleth(CA_dict_df, geojson=CA_counties, color='Snow+Day',
                        locations="FIP", featureidkey="id",
                        projection="mercator"
                        ).update_geos(fitbounds="locations", visible=False)
        elif fig_name2 == 'Snow' and fig_name3 == 'Noon': 
            figure = px.choropleth(CA_dict_df, geojson=CA_counties, color='Snow+Noon',
                        locations="FIP", featureidkey="id",
                        projection="mercator"
                        ).update_geos(fitbounds="locations", visible=False)
        elif fig_name2 == 'Snow' and fig_name3 == 'Night': 
            figure = px.choropleth(CA_dict_df, geojson=CA_counties, color='Snow+Night',
                        locations="FIP", featureidkey="id",
                        projection="mercator"
                        ).update_geos(fitbounds="locations", visible=False)
        elif fig_name2 == 'Snow' and fig_name3 == 'All Times of Day': 
            figure = px.choropleth(CA_dict_df, geojson=CA_counties, color='Snow',
                        locations="FIP", featureidkey="id",
                        projection="mercator"
                        ).update_geos(fitbounds="locations", visible=False)
        # Cloudy Weather
        elif fig_name2 == 'Cloudy' and fig_name3 == 'Day': 
            figure = px.choropleth(CA_dict_df, geojson=CA_counties, color='Cloudy+Day',
                        locations="FIP", featureidkey="id",
                        projection="mercator"
                        ).update_geos(fitbounds="locations", visible=False)
        elif fig_name2 == 'Cloudy' and fig_name3 == 'Noon': 
            figure = px.choropleth(CA_dict_df, geojson=CA_counties, color='Cloudy+Noon',
                        locations="FIP", featureidkey="id",
                        projection="mercator"
                        ).update_geos(fitbounds="locations", visible=False)
        elif fig_name2 == 'Cloudy' and fig_name3 == 'Night': 
            figure = px.choropleth(CA_dict_df, geojson=CA_counties, color='Cloudy+Night',
                        locations="FIP", featureidkey="id",
                        projection="mercator"
                        ).update_geos(fitbounds="locations", visible=False)
        elif fig_name2 == 'Cloudy' and fig_name3 == 'All Times of Day': 
            figure = px.choropleth(CA_dict_df, geojson=CA_counties, color='Cloudy',
                        locations="FIP", featureidkey="id",
                        projection="mercator"
                        ).update_geos(fitbounds="locations", visible=False)
        # Dust Weather
        elif fig_name2 == 'Dust' and fig_name3 == 'Day': 
            figure = px.choropleth(CA_dict_df, geojson=CA_counties, color='Dust+Day',
                        locations="FIP", featureidkey="id",
                        projection="mercator"
                        ).update_geos(fitbounds="locations", visible=False)
        elif fig_name2 == 'Dust' and fig_name3 == 'Noon': 
            figure = px.choropleth(CA_dict_df, geojson=CA_counties, color='Dust+Noon',
                        locations="FIP", featureidkey="id",
                        projection="mercator"
                        ).update_geos(fitbounds="locations", visible=False)
        elif fig_name2 == 'Dust' and fig_name3 == 'Night': 
            figure = px.choropleth(CA_dict_df, geojson=CA_counties, color='Dust+Night',
                        locations="FIP", featureidkey="id",
                        projection="mercator"
                        ).update_geos(fitbounds="locations", visible=False)
        elif fig_name2 == 'Dust' and fig_name3 == 'All Times of Day': 
            figure = px.choropleth(CA_dict_df, geojson=CA_counties, color='Dust',
                        locations="FIP", featureidkey="id",
                        projection="mercator"
                        ).update_geos(fitbounds="locations", visible=False)
        # For All time of Day
        elif fig_name2 == 'All Weather' and fig_name3 == 'Day': 
            figure = px.choropleth(CA_dict_df, geojson=CA_counties, color='Day',
                        locations="FIP", featureidkey="id",
                        projection="mercator"
                        ).update_geos(fitbounds="locations", visible=False)
        elif fig_name2 == 'All Weather' and fig_name3 == 'Noon': 
            figure = px.choropleth(CA_dict_df, geojson=CA_counties, color='Noon',
                        locations="FIP", featureidkey="id",
                        projection="mercator"
                        ).update_geos(fitbounds="locations", visible=False)
        elif fig_name2 == 'All Weather' and fig_name3 == 'Night': 
            figure = px.choropleth(CA_dict_df, geojson=CA_counties, color='Night',
                        locations="FIP", featureidkey="id",
                        projection="mercator"
                        ).update_geos(fitbounds="locations", visible=False)
        elif fig_name2 == 'All Weather' and fig_name3 == 'All Times of Day': 
            figure = px.choropleth(CA_dict_df, geojson=CA_counties, color='All',
                        locations="FIP", featureidkey="id",
                        projection="mercator"
                        ).update_geos(fitbounds="locations", visible=False)
        return dcc.Graph(figure=figure)
    app.run_server(debug=False, use_reloader=False)


# In[7]:


# plot_double_dropdown_chloropleth(processed_data,fip_dict_pop,fipkey_popvalue)


# In[ ]:




