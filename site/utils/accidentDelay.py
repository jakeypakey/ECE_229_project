import os
import numpy as np
import pandas as pd
import requests as req
import pickle
import polyline
import json
from sklearn.ensemble import RandomForestRegressor
from datetime import datetime
class AccidentDelay(object):
    """
    This class wraps a model which provides an esitmate of the time delay
    given an accident occured at a given location

    :param model: the model
    :type model: sklearn.ensemble.RandomForestRegressor model
    :param key: openweather api key
    :type model: string
    """

    def __init__(self,modelFile='../data/trainedModelNationwide.pkl',apiKeyFile='../data/key.pkl'):
        """
        Loads the api key and model into memory

        :param routeJSON: raw json from googlemaps
        :param model: sklearn model for inference
        :raises TypeError: when non strings input
        :raises FileNotFoundError: when file does not exist
        :return: None
        """
        if not isinstance(modelFile,str) or not isinstance(apiKeyFile,str):
            raise TypeError
        if not os.path.isfile(modelFile) or not os.path.isfile(apiKeyFile):
            raise FileNotFoundError
        with open(modelFile,'rb') as fi:
            self.model = pickle.load(fi)
        with open(apiKeyFile,'rb') as fi:
            self.key = pickle.load(fi)['key']

    ##THIS IS THE ONLY FUNCTION THAT SHOULD NEEED TO BE CALLED ONCE OBJECT IS CONSTRUCTED
    def orderRoutes(self,routeJSON,getAll=False):
        """
        Rates the routes accident time score

        :param routeJSON: raw json from googlemaps
        :param getAll: true if all points and values desired
        :raises TypeError: when non dictionary input
        :return: values pertaining to time rating in the order that the routes were ordered inside the routeJSON
        :rtype: list of floats, and values if desired
        """
        if not isinstance(routeJSON,dict):
            raise TypeError
        scores = []
        for route in routeJSON['routes']:
            scores.append(self.rateRoute(route,getAll))
        return scores
        

    def getWeather(self,lat=32.8800806,lng=-117.237558):
        """
        Fetches weather parameters for the provided latitude and longitude more info at https://openweathermap.org/current

        :param lat: latitude, defaults to Geisel Library latitude 
        :param lng: longitude, defaults to Geisel Library longitude 
        :raises ValueError: when invalid lat lng passed
        :raises TypeError: when non float input
        :return: JSON with relevant weather data
        :rtype: JSON object
        """
        if not (isinstance(lat,float) and isinstance(lng,float)):
            raise TypeError
        if lat > 90 or lat <-90 or lng > 180 or lng <-180:
            raise ValueError

        url = 'http://api.openweathermap.org/data/2.5/weather'
        params = {'lat' : lat,
                'lon' : lng,
                'appid' : self.key,
                'units' : 'imperial'}
        r = req.get(url=url,params=params)
        return r.json()

    def generateExample(self,lat=None,lng=None,weatherDict=None):
        """
        Parse and transform weather dictionary from getWeather and use the information to create an example for inference

        :param weatherDict: dictionary with raw json
        :raises TypeError: when non dict passed to dict arg
        :raises ValueError: when lat,lng disagrees with dict
        :return: JSON with relevant weather data
        :rtype: JSON object
        """
        if not isinstance(weatherDict,dict) and not weatherDict==None:
            raise TypeError
        if weatherDict==None:
            weatherDict = self.getWeather(lat,lng)
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

        return pd.Series(ret,index=idx)

    def distance(self,x,y):
        """
        Calculates the distance between x,y in kilometers using the Haversine formula: https://en.wikipedia.org/wiki/Haversine_formula

        :param x: lat,lng in degrees
        :param y: lat,lng in degrees
        :raises TypeError: points not input
        :return: distnace in kilometers
        :rtype: float
        """
        if not(len(x)==2 and len(y)==2):
            raise TypeError
        elif not(isinstance(x[0],float) and isinstance(x[1],float) and isinstance(y[0],float) and isinstance(y[1],float)):
            raise TypeError

        lat1,lng1 = np.radians(x[0]),np.radians(x[1])
        lat2,lng2 = np.radians(y[0]),np.radians(y[1])
        deltaLat = lat2 - lat1
        deltaLng = lng2 - lng1
        return 2*6367*np.arcsin(np.sqrt(np.sin(deltaLat/2)**2 + np.cos(lat1)*np.cos(lat2)*np.sin(deltaLng/2)**2))

    def rateRoute(self,routeDict,getAll=False):    
        """
        Provides a rating of the time of an accident given one occurs along the route on the route specified

        :param routeDict: the route as a dict
        :param model: sklearn model for inference
        :param getAll: returns all sample points, along with normalized scores
        :raises TypeError: when non dictionary input
        :return: value pertaining to time rating and all scored points if desired
        :rtype: (scores,allPoints)
        """
        if not isinstance(routeDict,dict):
            raise TypeError
        if not isinstance(getAll,bool):
            raise TypeError
 
        line = routeDict['overview_polyline']['points']
        #get distance in kilometers
        totalDistance = routeDict['legs'][0]['distance']['value']/1000
        points = polyline.decode(line)
        distances= [self.distance(points[i-1],points[i]) for i in range(1,len(points))]

        #we sample at the starting point, then we sample at equal spots once every kilometer (or so)
        #unless the overall routes is more than 20 kilometers, in which case we sample at 20 (almost)
        #equidistance points along the route

        if totalDistance <15:
            cutoff=1
        else:
            cutoff = totalDistance/15

        samples = [self.generateExample(lat=points[0][0],lng=points[1][0])]
        legDistance =0
        for i in range(len(distances)):
            legDistance += distances[i]
            if legDistance >=cutoff:
                samples.append(self.generateExample(lat=points[i+1][0],lng=points[i+1][1]))
                legDistance = 0
        ratings = self.model.predict(pd.DataFrame(samples).to_numpy())
        #parallel arrays returned
        if getAll:
            return (sum(ratings)/len(ratings),(ratings,points))
            
        else:
            return sum(ratings)/len(ratings)

#Example usage
#this is the JSON from google maps
#with open('../data/multi_route.json') as fi:
#    route = json.load(fi)

#constructor loads model
#a = AccidentDelay()
#return ratings for each route
#use getAll=True if you want ALL samples
#print(a.orderRoutes(route,True))

if __name__ == "__main__":
    with open('../data/multi_route.json') as fi:
        route = json.load(fi)

    print(datetime.now())
    a = AccidentDelay()
    print(datetime.now())
    print(a.orderRoutes(route))
    print(datetime.now())

