'''
Example pytest file for runing pytest
You just start adding your test cases below
See detail explaination and example:  https://www.notion.so/pytest-examples-4ed5728b445d404494a8d10f16687421
'''
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
file = '/workspace/ECE_229_project/site/utils/'
PytestFileAdder(file)
from DirectionsUtil import *
from .plots import *
import plotly.express as px
import plotly

def test_plotSources():
    assert isinstance(plotSources(),plotly.graph_objs._figure.Figure)

obj = DirectionsClient()
def test_get_directions_json():
    jason_ins = obj.get_directions_json('ucsd','LA')
    assert all([isinstance(x,dict) for x in jason_ins])
  
