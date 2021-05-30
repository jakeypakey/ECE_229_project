import numpy as np
import pandas as pd
import json
from sklearn.ensemble import RandomForestRegressor
import pickle 
import polyline
from weather import generateExample
def distance(x,y):
    """calculates the distance between x,y in kilometers
    using the Haversine formula:
    https://en.wikipedia.org/wiki/Haversine_formula
    :param x : lat,lng in degrees
    :param y : lat,lng in degrees
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




def rateRoute(routeDict,model):    
    """provides a rating of the time of an accident given
    one occurs along the route on the route specified
    :param routeDict : the route as a dict
    :param model : sklearn model for inference
    :raises TypeError: when non dictionary input
    :return: value pertaining to time rating
    :rtype: float
    """
    if not isinstance(routeDict,dict):
        raise TypeError
 
    print('finding sample points')
    line = routeDict['overview_polyline']['points']
    #get distance in kilometers
    totalDistance = routeDict['legs'][0]['distance']['value']/1000
    points = polyline.decode(line)
    distances= [distance(points[i-1],points[i]) for i in range(1,len(points))]

    #we sample at the starting point, then we sample at equal spots once every kilometer (or so)
    #unless the overall routes is more than 20 kilometers, in which case we sample at 20 (almost)
    #equidistance points along the route

    if totalDistance <15:
        cutoff=1
    else:
        cutoff = totalDistance/15

    samples = [generateExample(lat=points[0][0],lng=points[1][0])]
    legDistance =0
    for i in range(len(distances)):
        legDistance += distances[i]
        if legDistance >=cutoff:
            samples.append(generateExample(lat=points[i+1][0],lng=points[i+1][1]))
            legDistance = 0
        
    print('inference start')
    siz = sum(model.predict(pd.DataFrame(samples).to_numpy()))/len(samples)
    return siz

def orderRoutes(routeJSON, model):
    """rates the routes accident time score
    :param routeJSON : raw json from googlemaps
    :param model : sklearn model for inference
    :raises TypeError: when non dictionary input
    :return: value pertaining to time rating
    :rtype: float
    """
    if not isinstance(routeJSON,dict):
        raise TypeError
    scores = []
    for route in routeJSON['routes']:
        scores.append(rateRoute(route,model))
    return scores



print('model loaded')

model = None
with open('../data/trainedModelNationwide.pkl','rb') as fi:
    model = pickle.load(fi)
print('model loaded')

with open('../data/multi_route.json') as fi:
    route = json.load(fi)
print(orderRoutes(route,model))
