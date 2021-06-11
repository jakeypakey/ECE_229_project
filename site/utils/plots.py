import plotly.express as px
import numpy as np
import pandas as pd
import pickle

def preprocessFeatureData(feat):
    """
    Preprocesses the feature in order to prepare for plotly figure

    :param feat: the feature datafrma
    :return: dictionary of features and impact
    :rtype: dict
    """
    values,labels = [x[1] for x in feat],[x[0] for x in feat]
    values/=sum(values)
    other = 0
    final = {'Feature': [],'Impact':[]}
    for k,v in zip(labels,values):
        if v < .02:
            other+=v
        else:
            final['Feature'].append(k)
            final['Impact'].append(v)
    final['Feature'].append('Others')
    final['Impact'].append(other)
    return final

def plotSources():
    """
    Plots the source pie chart from a saved pickle file
    
    :return: a plotly pie chart
    :rtype: px.pie
    """
    with open('../data/sourceDist.pkl','rb') as fi:
        sources = pickle.load(fi)
    final = {'Source':list(sources.keys()),'Count':list(sources.values())}
    #return final
    return px.pie(final,names='Source',values='Count')

def plotQuantiles():
    """
    Plots the quantiles for duration of accident from a saved pickle file

    :return: a plotly bar chart showing duration 
    :rtype: px.bar
    """
    with open('../data/quants.pkl','rb') as fi:
        quants = pd.Series(pickle.load(fi))
    return px.bar(quants,labels={'index':'Quantile','value':'Duration of accident (minutes)'})

def plotImportance(vertical=False):
    """
    Plots the ranked importance of features from a stored pickle file

    :param vertical: plot the image vertically or horizontally
    :return: plotly bar chart
    :rtype: px.bar
    """
    with open('../data/featureImportance.pkl','rb') as fi:
        feat = pickle.load(fi)
    values,labels = [x[1] for x in feat],[x[0] for x in feat]
    values/=sum(values)
    other = 0
    final = {'Feature': [],'Impact as a Percentage':[]}
    for k,v in zip(labels,values):
        if v < .03:
            other+=v
        else:
            final['Feature'].append(k.replace('_', ' ').replace('(',' (').replace('(F)','(℉)').replace('Pressure (in)','Atmospheric Pressure (inHg)'))
            final['Impact as a Percentage'].append(v*100)
    final['Feature'].append('Others')
    final['Impact as a Percentage'].append(100*other)
    if vertical:
        figB = px.bar(final,y='Feature',x='Impact as a Percentage',orientation='h')
        figB.update_xaxes(ticksuffix="%", showgrid=True)
    else:
        figB = px.bar(final,x='Feature',y='Impact as a Percentage')
    
        figB.update_yaxes(ticksuffix="%", showgrid=True)
    return figB

