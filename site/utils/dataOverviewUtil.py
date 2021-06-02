import plotly.express as px

def drawImportanceChart(feat):
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
    figB = px.bar(final,x='Feature',y='Impact as a Percentage')
    
    figB.update_yaxes(ticksuffix="%", showgrid=True)
    return figB

