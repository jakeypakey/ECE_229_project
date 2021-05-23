'''
use case
data = pd.read_csv("../input/us-accidents/US_Accidents_Dec20_Updated.csv")
data = data.dropna()
find_best_reg(clean_data(data)[0])

view hist and heatmap
fig = plt.figure(figsize = (25,30))
ax = fig.gca()
clean_data(data)[0].hist(ax  =ax,bins = 50)

import seaborn as sns
import matplotlib.pyplot as plt
plt.figure(figsize=(12,5))
heatmap = sns.heatmap(clean_data(data)[0].corr(), cmap="RdYlGn", cbar_kws = dict(use_gridspec=False, location="top", label='Correlation'), yticklabels=3, xticklabels=6, annot=False, linewidths=2)
plt.xticks(rotation=0) 
plt.show()
'''
import pandas as pd
from sklearn.model_selection import cross_validate as cv
from sklearn import linear_model
from sklearn.metrics import r2_score
from sklearn import svm
from sklearn.neighbors import KNeighborsRegressor
from sklearn import tree
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.pipeline import Pipeline
drop_list = ['duration','End_Time','Description','Number','Street','Side',
                          'City','County','State','Zipcode','Country','Timezone','Airport_Code','Wind_Direction','Weather_Condition']
def clean_data(data,frac = 0.01):
    '''
    Sample the given data and return cleaned sample data
    input:
        data:(panda data frame) input us accident data
    return:
        cleaned_data: covered time value to hours and map 'objest' to its unique value
    '''
    assert isinstance(data, pd.core.frame.DataFrame)
    df_sample = data.sample(frac=frac, replace=True, random_state=1)
    cleaned_data = df_sample.drop(['ID'],axis =1)
    maped_class = []
    for x in cleaned_data.columns:
        try:
            cleaned_data[x] = cleaned_data[x].astype(float)
        except:
            if cleaned_data[x].dtypes== 'O' and '_Time' in x: # time object
                cleaned_data[x] = pd.to_datetime(cleaned_data[x]).dt.hour  +pd.to_datetime(cleaned_data[x]).dt.minute /60
            else:
                maped_class.append(dict(zip(cleaned_data[x].unique(),range(len(cleaned_data[x].unique())))))
                cleaned_data[x] = cleaned_data[x].map(maped_class[-1])
    cleaned_data['duration'] =   cleaned_data['End_Time'] - cleaned_data['Start_Time']
    return cleaned_data,maped_class
def find_best_reg(cleaned_data,drop_list = ['duration']):
    '''
    Given data report evaluation
    cleaned_data:(pd.core.frame.DataFrame) cleaned training data 
    '''
    assert cleaned_data.isna().sum() == 0
    assert 'O' not in cleaned_data.dtypes.tolist()
    y =cleaned_data['duration']
    x = cleaned_data.drop(drop_list,axis =1)
    classifiers = [
        linear_model.Ridge(alpha=.5,normalize=True),
        linear_model.Lasso(alpha=0.01,normalize=True),
        linear_model.BayesianRidge(normalize=True),
        MLPRegressor(random_state=1, max_iter=1000),
        GradientBoostingRegressor(n_estimators=100, learning_rate=0.1,max_depth=1, random_state=0, loss='ls'),
        RandomForestRegressor(max_depth=2, random_state=0),
        tree.DecisionTreeRegressor(),
        KNeighborsRegressor(n_neighbors=5),
        ]
    for classifier in classifiers:
        pipe = Pipeline(steps=[('classifier', classifier)])
        scores = cv(pipe, x, y, cv=5,
                                scoring=('r2', 'neg_mean_squared_error'),
                                return_train_score=True)
        print(pipe)
        print(scores['test_neg_mean_squared_error'].mean(),scores['test_r2'].mean())
