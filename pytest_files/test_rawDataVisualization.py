# -*- coding: utf-8 -*-
"""
Created on Wed Jun  9 20:36:53 2021

@author: srist
"""




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

from rawDataVisualizationUtil import generateCleanedData
import warnings
warnings.filterwarnings("ignore")


data_processer = None
# 
def test_generateCleanedData_init_1():
    try:
        # wrong filename in data_filename
        generateCleanedData(data_filename='../data/RandomFile.csv',
                     population_filename='../data/population.xlsx',
                     statenames_filename='../data/state_name_code_mappings.csv')
        assert False
    except:
        assert True
        
def test_generateCleanedData_init_2():
    try:
        # wrong file location  in data_filename
        generateCleanedData(data_filename='../RandomFile.csv',
                     population_filename='../data/population.xlsx',
                     statenames_filename='../data/state_name_code_mappings.csv')
        assert False
    except:
        assert True
    
def test_get_processedAccidentLocationFile_1():
    global data_processer
    
    try:
        #  checking class instanciation
        warnings.filterwarnings("ignore")
        data_processer = generateCleanedData()
    except:
        assert False
    
def test_get_processedAccidentLocationFile_2():
    global data_processer
    
    try:
        # checking if the output file name is meaningful (i.e is it str?)
        data_processer.get_processedAccidentLocationFile(output_filename=999)
        assert False
    except:
        assert True
        
def test_get_processedAccidentLocationFile_3():
    global data_processer
    
    try:
        # checking if the output file is created!
        warnings.filterwarnings("ignore")
        data_processer.get_processedAccidentLocationFile(output_filename="../site/data/accidents_visualization.csv")
        assert os.path.exists("../site/data/accidents_visualization.csv")
    except:
        assert False
        
def test_get_processedComparisonFile_1():
    try:
        
        # checking if the output file is created!
        warnings.filterwarnings("ignore")
        data_processer.get_processedComparisonFile(output_filename="../site/data/comparisons.csv")
        assert os.path.exists("../site/data/comparisons.csv")
    except:
        assert False
        
    