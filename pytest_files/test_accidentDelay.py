import pytest
import sys
import os
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
from utils.accidentDelay import AccidentDelay
def test_constructor():
    with pytest.raises(TypeError):
        ad = AccidentDelay(None,None)

    with pytest.raises(FileNotFoundError):
        ad = AccidentDelay('thisisntaFile.txt')
def test_functions():
    ad = AccidentDelay()
    with pytest.raises(TypeError):
        ad.orderRoutes([1,2,3])

    with pytest.raises(TypeError):
        ad.orderRoutes("chicken")
    with pytest.raises(TypeError):
        ad.getWeather(12334,2342343)
    with pytest.raises(ValueError):
        ad.getWeather(-400.0,268.3333)
    assert isinstance(ad.getWeather(),dict)
    with pytest.raises(TypeError):
        ad.generateExample(-122.0,23.4,['python is my favorite'])
    with pytest.raises(TypeError):
        ad.distance(12,12)
    with pytest.raises(TypeError):
        ad.rateRoute(42)

