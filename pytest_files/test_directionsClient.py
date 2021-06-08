import pytest
import sys
import os
from dotenv import dotenv_values
def PytestFileAdder(filename,exclude = ['__init__']):
    ''' 
    Avoiding import file error by adding files to sys search path for easier pytest

        Args:
            filename (str):path to the  file
        
        Returns: 
            package_name(list)([file] i.e import file)
    '''
    assert isinstance(filename,str)
    assert all([isinstance(x,str) for x in exclude])
    # add first pripirty search path
    package_name = []
    for root,dirc,files  in os.walk(filename):
        files = [os.path.splitext(f)[0] for f in files if os.path.splitext(f)[1] == '.py']
        for f in files:
            if f not in exclude and '.'not in f:
                package_name.append(f)
                sys.path.insert(1, root)
    return package_name
file = '../site/'
pt = PytestFileAdder(file)


from directionsClient import *

def test_invalid_env_vars():
    with pytest.raises(TypeError):
        dc = DirectionsClient([])

    with pytest.raises(KeyError):
        dc = DirectionsClient({})

def test_get_directions_json():
    config = dotenv_values('../site/.env')
    dc = DirectionsClient(config)

    res = dc.get_directions_json('ucsd', 'LA')
    assert('routes' in res)
    assert(isinstance(res['routes'], list))
    assert all([isinstance(x,dict) for x in res['routes']])
    
def test_invalid_input_to_directions():
    config = dotenv_values('../site/.env')
    dc = DirectionsClient(config)

    with pytest.raises(AssertionError):
        res = dc.get_directions_json([], {}) 

def test_parse_valid_geojson():
    config = dotenv_values('../site/.env')
    dc = DirectionsClient(config)

    res = dc.get_directions_json('ucsd', 'LA')
    poly_list = dc.get_geojson_from_route(res['routes'][0])

    assert(isinstance(poly_list, list))
    assert all(isinstance(x, tuple) for x in poly_list)

def test_invalid_route_geojson():
    config = dotenv_values('../site/.env')
    dc = DirectionsClient(config)

    with pytest.raises(AssertionError):
        dc.get_geojson_from_route([])

    with pytest.raises(AssertionError):
        dc.get_geojson_from_route({'overview_polyline': []})





