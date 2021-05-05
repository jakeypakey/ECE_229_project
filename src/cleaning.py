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
    print("After dropping NaN, we have {} % of data left".format(100*(len(df)/originalSize)))
    return df


