import numpy as np
import googlemaps
from datetime import datetime
import polyline
from dotenv import dotenv_values
import os

class DirectionsClient:
    """
    This class is a decorator class to the Google Maps Directions API.  
    """
    def __init__(self):
        """
        Loads the token and initializes the googlemaps client API
        :raises FileNotFoundError: when the .env token file does not exist
        :raises KeyError: when the GMAPS_KEY token is not set in the .env file
        """
        if not os.path.isfile('.env'):
            raise FileNotFoundError(".env file containing Google Maps API token not found")
        self.config = dotenv_values('.env')

        if 'GMAPS_KEY' not in self.config:
            raise KeyError("GMAPS_KEY not found in .env file")
        self.gmaps = googlemaps.Client(key=self.config['GMAPS_KEY'])

    def get_directions_json(self, start, destination):
        """ Makes a request to Google's Directions API to get the routes

        :param start: the starting location in string format
        :destination: the destination location in string format
        :raises TypeError: the start or destination is not in string format
        :return: dictionary that contains a list of routes returned by the google maps api
        :rtype: dictionary with one key for 'routes'
        """
        assert isinstance(start, str) and isinstance(destination, str)

        directions_result = self.gmaps.directions(start, destination, alternatives=True)
        res = {"routes": directions_result}

        return res

    def get_geojson_from_route(self, route):
        """ Given a single route object from google maps, convert the polyline retrieved to geojson format to map

        :param route: a route returned from Google Directions API
        :return: the polyline containing the longitude and latitudes
        :rtype: list of tuples
        """
        assert isinstance(route, dict)
        assert 'overview_polyline' in route
        assert 'points' in route['overview_polyline']

        route_polyline = route['overview_polyline']['points']
        geojson_list = polyline.decode(route_polyline, geojson=True)

        return geojson_list




if __name__ == '__main__':
    client = DirectionsClient()
    res = client.get_directions_json('ucsd', 'san diego')