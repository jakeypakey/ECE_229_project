import numpy as np
import googlemaps
from datetime import datetime
import polyline
from dotenv import dotenv_values

class DirectionsClient:
    def __init__(self):
        self.config = dotenv_values('.env')
        self.gmaps = googlemaps.Client(key=self.config['GMAPS_KEY'])

    def get_directions_json(self, start, destination):
        ''' Makes a request to Google's Directions API to get the routes

        Args:
            start (str): the starting location in string format
            destination (str): the destination location in string format
        
        Returns: 
            list of routes (1-3 routes)
        '''
        assert isinstance(start, str)
        assert isinstance(destination, str)

        directions_result = self.gmaps.directions(start, destination, alternatives=True)
        res = {"routes": directions_result}

        return res

    def get_geojson_from_route(self, route):
        ''' Given a single route object from google maps, convert the polyline retrieved to geojson format to map

        Args:
            route (dict): a route returned from Google Directions API

        Returns:
            list of (lon, lat)
        '''
        assert isinstance(route, dict)
        assert 'overview_polyline' in route

        route_polyline = route['overview_polyline']['points']
        geojson_list = polyline.decode(route_polyline, geojson=True)

        return geojson_list




if __name__ == '__main__':
    client = DirectionsClient()
    res = client.get_directions_json('ucsd', 'san diego')