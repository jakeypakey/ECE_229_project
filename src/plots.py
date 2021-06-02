import plotly.express as px
import numpy as np
import pandas as pd
import pickle

def plotSources():
    with  open('../data/sourceDist.pkl','rb') as fi:
        sources = pickle.load(fi)
    return px.bar(sources,title='Data Sources')
def plotQuantiles():
    with open('../data/quants.pkl','rb') as fi:
        quants = pd.Series(pickle.load(fi))
    return px.bar(quants,title='Quantiles of accident Duration')
def plotImportance():
    with open('../data/featureImportance.pkl','rb') as fi:
        feat = pickle.load(fi)
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
    return px.pie(final,values='Impact',names='Feature',title='Feature Importance')
