#put cleaning functions in here
import numpy as np
import pandas as pd

##Jacob Pollard##
def getPandasNumeric(df):
    '''
    function drops NaN columns, and converts data to numeric (with datetime numeric)
    but keeps the unique ID objects
    '''
    originalSize = len(df)
    #add deltaT
    df['Start_Time'] = pd.to_datetime(df['Start_Time'])
    df['End_Time'] = pd.to_datetime(df['End_Time'])
    df['Total_Time'] = df["End_Time"] - df['Start_Time']
    #evaluate total time just on number of minutes
    df['Total_Time'] = df['Total_Time'].apply(lambda x: (x.total_seconds()//60))
    

    #dropped because they are strings, redundant, or catagorical with no easy way to turn numeric
    dropCols = ['TMC','End_Time','End_Lat','End_Lng','Number','Street','City',
            'State','Zipcode','Country','Timezone','Airport_Code','Weather_Timestamp',
            'Wind_Direction','Weather_Condition','Description','Source','County','Turning_Loop']

    df = df.drop(dropCols,axis=1)

    #there is only one entry with this value
    df = df.drop(df[df['Side']==' '].index)
    #right and left side of road ->tonumeric
    df  = df.replace({'Side': {'R':1, 'L':0}})

    #drop all rows with NaN ***(~55% data lost here)***
    df = df.dropna()

    #all only have day and night, switch to binary
    toBin = {'Day':1, 'Night':0}
    replaceDict = {'Sunrise_Sunset':toBin,'Civil_Twilight':toBin,'Nautical_Twilight':toBin,'Astronomical_Twilight':toBin}
    df = df.replace(replaceDict)

    df[df.select_dtypes(include='bool').columns] = df.select_dtypes(include='bool').astype('int64')
    df['Day_Of_Week'] = df['Start_Time'].dt.dayofweek
    
    #add up all the minutes of the day
    df['Time_of_Day'] = df['Start_Time'].dt.hour*60 + df['Start_Time'].dt.minute
    #now, transform time of day to reflect periodic nature (11:59pm is right before 12am)
    #period of cos((2π/1440)*x) is 1440 == num minutes in a day
    df['Time_of_Day'] = df['Time_of_Day'].apply(lambda x : np.cos(((2*np.pi)/1440)*x))
    
    #transform days of week in similar manner
    df['Day_Of_Week'] = df['Day_Of_Week'].apply(lambda x : np.cos(((2*np.pi)/7)*x))
    
    #df['Total_Time']
    
    df = df.drop('Start_Time',axis=1)
    
    
    print("After dropping NaN, we have {} % of data left".format(100*(len(df)/originalSize)))
    return df
