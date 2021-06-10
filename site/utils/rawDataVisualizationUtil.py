# -*- coding: utf-8 -*-

import os,sys
import pandas as pd
# import numpy as np
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer

# cur_directory = os.getcwd()

class generateCleanedData():
    """
    This class cleans and organises the original data for the ease of 
    fast retrival while fetching values in real time during the usage of Dashboard 
    for visualization of accident data in each location and for comparison bar plots. 
    
    :param data_filename: excel or csv filename which contains the accident data. Dataset can be downlaoded from https://www.kaggle.com/sobhanmoosavi/us-accidents
    :type data_filename: str 
    :param population_filename: excel or csv filename which contains the population of each state in US. Data can be downloaded from https://www.census.gov/data/tables/time-series/dec/density-data-text.html
    :type population_filename: str 
    :param statenames_filename: excel or csv filename which contains state names and the corresponding code names. Data can be downloaded from https://worldpopulationreview.com/states/state-abbreviations
    :type statenames_filename: str 
        
    """
    def __init__(self,data_filename='../data/US_Accidents_Dec20.csv',
                 population_filename='../data/population.xlsx',
                 statenames_filename='../data/state_name_code_mappings.csv'):
        
        assert isinstance(data_filename,str)
        assert isinstance(population_filename,str)
        assert isinstance(statenames_filename,str)
        
        assert os.path.exists(data_filename)
        assert os.path.exists(population_filename)
        assert os.path.exists(statenames_filename)
        
        def is_csv(filename):
            return filename.split(".")[-1]=='csv'
        def is_excel(filename):
            return filename.split(".")[-1]=='xlsx'
        
        assert is_csv(data_filename) or is_excel(data_filename)
        assert is_csv(population_filename) or is_excel(population_filename)
        assert is_csv(statenames_filename) or is_excel(statenames_filename)
        
        try:
            if is_csv(data_filename):
                self.data = pd.read_csv(data_filename)
            elif is_excel(data_filename):
                self.data = pd.read_excel(data_filename)
        except Exception as e:
            print(e)
            sys.exit(1)
            
        try:
            if is_csv(population_filename):
                self.population = pd.read_csv(population_filename)
            elif is_excel(population_filename):
                self.population = pd.read_excel(population_filename)
        except Exception as e:
            print(e)
            sys.exit(1)
        
        try:
            if is_csv(statenames_filename):
                self.state_name_mappings = pd.read_csv(statenames_filename)
            elif is_excel(statenames_filename):
                self.state_name_mappings = pd.read_excel(statenames_filename)
        except Exception as e:
            print(e)
            sys.exit(1)
        
        self.data['End_Time'] = pd.to_datetime(self.data['End_Time'])
        self.data['Start_Time'] = pd.to_datetime(self.data['Start_Time'])
        self.data['year_month'] = self.data['Start_Time'].dt.strftime('%Y-%m')
        self.data['DayOfWeek'] = self.data['Start_Time'].dt.day_name()
        self.data['TimeOfDay'] = self.data['Start_Time'].dt.hour
        
            
    
    def get_processedAccidentLocationFile(self,output_filename="../data/accidents_visualization.csv"):
        """
        This function takes the original data and counts the number of accidents that occured 
        in each state during each month. 
        Also it takes the population information and computed the number of accidents occured per million people.
    
        :param output_filename: csv filename in which the processed data has to be stored
        :type output_filename: str 
        :return: None
        """
        
        assert isinstance(output_filename,str)
        if output_filename.split(".")[-1]!="csv":
            raise ValueError
                    
        state_counts_2 = self.data.groupby(["State","year_month"]).size().reset_index()
        state_counts_2 = state_counts_2.rename(columns={0:"counts"})
        
        all_dates = pd.DataFrame(pd.date_range('2016-02', state_counts_2["year_month"].max(), freq='M'),columns=['year_month'])
        all_states = pd.DataFrame(self.data["State"].unique(),columns=['State'])
        
        index = pd.MultiIndex.from_product([all_states['State'], all_dates['year_month']], names = ["State", "year_month"])
        temp = pd.DataFrame(index = index).reset_index()
        temp['year_month'] = pd.to_datetime(temp['year_month']).dt.strftime('%Y-%m')
        accidents = pd.merge(temp,state_counts_2,how="left",on=['State','year_month'])
        accidents['counts'] = accidents['counts'].fillna(0)

        self.population = self.population[['U.S. Department of Commerce','Unnamed: 1']].loc[4:54].rename(columns={'U.S. Department of Commerce': 'State','Unnamed: 1':'Census'})
        self.population = self.population.merge(self.state_name_mappings, how='left', on='State')[['Code','Census']]
        self.population = self.population.rename(columns={'Code':'State'})
        self.population['Census'] = self.population['Census'].astype(float)
        accidents = accidents.merge(self.population, how='left', on='State')
        accidents['counts per million'] = accidents['counts']/accidents['Census']*100000
        accidents = accidents[accidents["year_month"]<"2020-01"]
        accidents = accidents[accidents["year_month"] >= "2016-05"]
        
        # save the cleaned data into csv file
        accidents.to_csv(output_filename)
        
    def get_processedComparisonFile(self,output_filename="../data/comparisons.csv"):
        """
        This function takes the original data and counts the number of accidents that occured 
        in each state during each month when a particular feature takes a specific value. 
        For example: Number of accidents occured in CA in 2017-01 when DayOfWeek is Monday.
        
        :param output_filename: csv filename in which the processed data has to be stored
        :type output_filename: str
        :return: None. Stores the generated pandas dataframe into output_filename
        """

        assert isinstance(output_filename,str)
        assert output_filename.split(".")[-1]=="csv"
        
        self.fillnabyDataImputation()
            
        self.convert2levels()
        
        
        columns = ['DayOfWeek','TimeOfDay','Severity','AccidentDuration','Pressure','Temperature','Humidity','WindSpeed']

        state_count_day = None
        feature_columns = ["year_month"]
        for column in columns:
            
            unique_values = list(self.data[column].unique())
            unique_values.sort()
            unique_values = [value for value in unique_values]
            for value in unique_values:
                value_data = self.data[self.data[column]==value]
                temp = value_data.groupby(["State","year_month"]).agg({column:'count'}).reset_index()
                temp = temp.rename(columns={column:column+"_"+str(value)})
                feature_columns.append(column+"_"+str(value))
                    
                if state_count_day is None:
                    state_count_day = temp
                else:
                    state_count_day = pd.merge(state_count_day,temp,how='left',on=['State','year_month'])
        
        all_dates = pd.DataFrame(pd.date_range('2016-01', self.data["year_month"].max(), freq='M'),columns=['year_month'])
        all_states = pd.DataFrame(self.data["State"].unique(),columns=['State'])
        index = pd.MultiIndex.from_product([all_states['State'], all_dates['year_month']], names = ["State", "year_month"])
        all_states_dates = pd.DataFrame(index = index).reset_index()
        all_states_dates['year_month'] = pd.to_datetime(all_states_dates['year_month']).dt.strftime('%Y-%m')
            
        state_count_day = pd.merge(all_states_dates,state_count_day,how="left",on=['State','year_month'])
        state_count_day['Month'] = pd.to_datetime(state_count_day['year_month']).dt.strftime('%m')
        state_count_day['Year'] = pd.to_datetime(state_count_day['year_month']).dt.strftime('%Y')
        state_count_day = state_count_day[state_count_day["Year"]<"2020"]
        state_count_day = state_count_day.fillna(0)
        
        all_states_count = state_count_day[feature_columns].groupby("year_month").sum()
        all_states_count['Month'] = pd.to_datetime(all_states_count.index).month
        all_states_count['Year'] = pd.to_datetime(all_states_count.index).year
        all_states_count = all_states_count.reset_index()
        all_states_count["State"] = 'All'
        
        state_count_day = pd.concat([state_count_day,all_states_count],axis=0)
        
        state_count_day.to_csv(output_filename,index=False)
        
    
    def fillnabyDataImputation(self,):
        """
        This function uses Imputation function from sklearn to fill in the Nan values in the data.

        :return: None
        """
        # Imputation
        imp = IterativeImputer(max_iter=10, random_state=0)
        fill_coloumns = ['Severity','Start_Lat', 'Start_Lng', 'Distance(mi)',
                    'Temperature(F)','Wind_Chill(F)','Humidity(%)', 'Pressure(in)','Visibility(mi)',
                    'Wind_Speed(mph)','Precipitation(in)']
        imp.fit(self.data[fill_coloumns])
        self.data[fill_coloumns] = pd.DataFrame(imp.transform(self.data[fill_coloumns]),columns=fill_coloumns)
        
    def convert2levels(self,):
        """
        This function converts specific features with continuous values to discrete level.
        For example: Pressure is quantized to 3 discrete levels (Low: <29.5,Moderate: 29.5-30.2,High: >30.2) and
        TimeOfDay is quantized to 3 discrete levels (Day: 6:00-11:59,Noon: 12:00-17:59,Night: 18:00-5:59) etc.,
    
        :return: None
        """
        
        thres_category = {'Pressure':{'thresolds':[29.5,30.2],
                              'category':['Low','Moderate','High']},
                  'AccidentDuration':{'thresolds':[35,50,70,90],
                              'category':['Very Low','Low','Moderate','High','Very High']},
                  'Temperature':{'thresolds':[0,30,60,80,100],
                              'category':['VeryVeryLow','VeryLow','Low','Moderate','High','VeryHigh']},
                  'WindSpeed':{'thresolds':[8,13,19,25],
                              'category':['Calm','GentleBreeze','ModerateBreeze','FreshBreeze','StrongBreeze']},
                  'Humidity':{'thresolds':[30,50],
                              'category':['Low','Moderate','High']},
                  'TimeOfDay':{'thresolds':[6,12,18],
                              'category':['Night','Day','Noon','Night']},
                 }


        def apply_func(x,thresolds=[29.5,30.2],category=['Low','Moderate','High']):
            
            for idx,thres in enumerate(thresolds):
                if x<thresolds[idx]:
                    return category[idx]
            return category[-1]
        
        self.data['AccidentDuration'] = (self.data['End_Time']-self.data['Start_Time']).dt.total_seconds()/60
        
        
        self.data['Pressure'] = self.data['Pressure(in)'].apply(lambda x: apply_func(x,
                                                                           thresolds=thres_category['Pressure']['thresolds'],
                                                                           category=thres_category['Pressure']['category']
                                                                           ))
        self.data['AccidentDuration'] = self.data['AccidentDuration'].apply(lambda x: apply_func(x,
                                                                               thresolds=thres_category['AccidentDuration']['thresolds'],
                                                                               category = thres_category['AccidentDuration']['category']
                                                                               ))
        self.data['Temperature'] = self.data['Temperature(F)'].apply(lambda x: apply_func(x,
                                                                               thresolds=thres_category['Temperature']['thresolds'],
                                                                               category = thres_category['Temperature']['category']))        
        self.data['WindSpeed'] = self.data['Wind_Speed(mph)'].apply(lambda x: apply_func(x,
                                                                               thresolds=thres_category['WindSpeed']['thresolds'],
                                                                               category = thres_category['WindSpeed']['category']
                                                                               ))
        self.data['Humidity'] = self.data['Humidity(%)'].apply(lambda x: apply_func(x,
                                                                       thresolds=thres_category['Humidity']['thresolds'],
                                                                       category = thres_category['Humidity']['category']
                                                                       ))
        self.data['TimeOfDay'] = self.data['TimeOfDay'].apply(lambda x: apply_func(x,
                                                                       thresolds=thres_category['TimeOfDay']['thresolds'],
                                                                       category = thres_category['TimeOfDay']['category']
                                                                       ))
     

if __name__ == '__main__':
    
    data_processer = generateCleanedData()
    
    data_processer.get_processedAccidentLocationFile()
    
    data_processer.get_processedComparisonFile()
    
    
    
