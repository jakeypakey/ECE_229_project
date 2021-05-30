import requests as req
from pickle import load
import numpy as np
import pandas as pd
import json
from datetime import datetime
def getWeather(lat=32.8800806,lng=-117.237558):
    """fetches weather parameters for the provided latitude and longitude
    more info at https://openweathermap.org/current
    :param lat : latitude, defaults to Geisel Library latitude 
    :param lng : longitude, defaults to Geisel Library longitude 
    :raises ValueError: when invalid lat lng passed
            TypeError: when non float input
    :return: JSON with relevant weather data
    :rtype: JSON object
    """
    if not (isinstance(lat,float) and isinstance(lng,float)):
        raise TypeError
    if lat > 90 or lat <-90 or lng > 180 or lng <-180:
        raise ValueError

    url = 'http://api.openweathermap.org/data/2.5/weather'
    with open('../data/key.pkl','rb') as fi: API_KEY = load(fi)['key']
    params = {'lat' : lat,
              'lon' : lng,
              'appid' : API_KEY,
              'units' : 'imperial'}
    r = req.get(url=url,params=params)
    return r.json()
def generateExample(lat=None,lng=None,weatherDict=None):
    """Parse and transform weather dictionary from getWeather
    and use the information to create an example for inference
    :param weatherDict : dictionary with raw json
    :raises TypeError: when non dict passed to dict arg
            ValueError: when lat,lng disagrees with dict
    :return: JSON with relevant weather data
    :rtype: JSON object
    """
    if not isinstance(weatherDict,dict) and not weatherDict==None:
        raise TypeError
    if weatherDict==None:
        weatherDict = getWeather(lat,lng)
    #lat,lng in dict does not agree with coordinate in arg at all
    if not (lat==None or lng==None):
        if (np.abs(lat-weatherDict['coord']['lat']) > .1) or (np.abs(lng-weatherDict['coord']['lon']) > .1):
            raise ValueError
    else:
        if lat==None:
            lat = weatherDict['coord']['lat']
        if lng==None:
            lng = weatherDict['coord']['lon']

    #desired:
    idx = list(['Start_Lat', 'Start_Lng', 'Temperature(F)', 'Wind_Chill(F)', 'Humidity(%)', 'Pressure(in)', 'Visibility(mi)','Wind_Direction','Wind_Speed(mph)','Precipitation(in)', 'Civil_Twilight', 'Day_Of_Week', 'Time_of_Day'])


    
    #given:
    #{'coord': {'lon': -117.2376, 'lat': 32.8801}, 
    #'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01d'}], 
    #'base': 'stations', 
    #'main': {'temp': 77.56, 'feels_like': 77.68, 'temp_min': 65.48, 'temp_max': 92.98, 'pressure': 1015, 'humidity': 57},
    #'visibility': 10000, 
    #'wind': {'speed': 5.01, 'deg': 346, 'gust': 10}, 
    #'clouds': {'all': 1}, 
    #'dt': 1621973520, 
    #'sys': {'type': 2, 'id': 2005841, 'country': 'US', 'sunrise': 1621946646, 'sunset': 1621997285}, 
    #'timezone': -25200, 
    #'id': 5363943, 
    #'name': 'La Jolla', 'cod': 200}


    #provided:
    ret = {'Start_Lat':lat,'Start_Lng':lng, 'Temperature(F)':weatherDict['main']['temp'],
            'Humidity(%)':weatherDict['main']['humidity']}
    #now convert pressure hPa -> psi
    ret['Pressure(in)'] = weatherDict['main']['pressure']*.02953

    ret['Wind_Speed(mph)'] = weatherDict['wind']['speed']

    #degree to periodic
    ret['Wind_Direction'] = np.cos((np.pi/180)*weatherDict['wind']['deg'])
    if 'rain' in weatherDict:
        ret['Precipitation(in)'] = weatherDict['rain']['rain.3h']/25.4
    else:
        ret['Precipitation(in)'] = 0
    #if it isnt earlier than 20 mins before sunrise or later than 20 minutes after sunset, say its daytime
    if (weatherDict['dt'] > weatherDict['sys']['sunrise']-1200) and (weatherDict['dt'] < weatherDict['sys']['sunset']+1200):
        ret['Civil_Twilight'] = 1
    else:
        ret['Civil_Twilight'] = 0
    
    time = datetime.fromtimestamp(weatherDict['dt'])
    #to periodic
    ret['Day_Of_Week'] = np.cos(time.weekday()*(2*np.pi)/7)
    #to periodic
    ret['Time_of_Day'] = np.cos((time.hour*60 + time.minute)*(2*np.pi)/1440)
    #to periodic
    ret['Day_Of_Week'] = np.cos(time.weekday()*(2*np.pi)/7)
    #meter to mile
    ret['Visibility(mi)'] =  weatherDict['visibility']/1609
    ret['Wind_Chill(F)'] = weatherDict['main']['feels_like']

    #now windspeed

    return pd.Series(ret,index=idx)


