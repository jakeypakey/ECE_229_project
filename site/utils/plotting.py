import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def plotSeverity(df,other='Precipitation(in)'):
    '''
    Adapted from Dyuthi
    Plot severity with field `other`
    '''    
    assert(other in df.columns.tolist())
    colors = ['r','g','b','k','c']
    df_temp = pd.DataFrame()
    df_temp['color'] = df['Severity'].apply(lambda x: colors[x])
    df_temp['Severity'] = df['Severity']
    df_temp[other] = df[other]
                       
    df_temp = df_temp.dropna()
             
    df_temp.plot.scatter(x=other,y='Severity',c=df_temp['color'])                               
