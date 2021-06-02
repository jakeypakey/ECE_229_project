
def preprocessFeatureData(feat):
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