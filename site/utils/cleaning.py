#put cleaning functions in here
import numpy as np
import pandas as pd
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

##Jacob Pollard##
#socal box
#[[-118.4843415454,32.5589092648],[-115.62921702,32.5589092648],[-115.62921702,34.4611013421],[-118.4843415454,34.4611013421],[-118.4843415454,32.5589092648]]
def getPandasNumeric(df,box=None):
    """
    cleans raw data for training
    :param df: DataFrame
    :param  box: bounding box, if points are to be limited to a single area
    :raises TypeError: non dataframe input
    :return: cleaned DataFrame
    :rtype: DataFrame
    """
    if not isinstance(df,pd.DataFrame):
        raise TypeError


    originalSize = len(df)
    #add deltaT
    df['Start_Time'] = pd.to_datetime(df['Start_Time'])
    df['End_Time'] = pd.to_datetime(df['End_Time'])
    df['Total_Time'] = df["End_Time"] - df['Start_Time']
    #evaluate total time just on number of minutes
    df['Total_Time'] = df['Total_Time'].apply(lambda x: (x.total_seconds()//60))
    #drop outlier accidents longer than 8 hours
    df = df[df['Total_Time'] <= 480]
    notPercip = ['Clear','Overcast','Mostly Cloudy','Partly Cloudy','Scattered Clouds',
    'Fair','Haze','Fog','Cloudy','Smoke','Patches of Fog','Fair / Windy','Cloudy / Windy',
    'Mostly Cloudy / Windy','Partly Cloudy / Windy']
    df.loc[df['Weather_Condition'].isin(notPercip) & df['Precipitation(in)'].isna(),'Precipitation(in)'] = 0
    

    #dropped because they are strings, redundant, or catagorical with no easy way to turn numeric
    dropCols = ['TMC','End_Time','End_Lat','End_Lng','Number','Street','City',
            'State','Zipcode','Country','Timezone','Airport_Code','Weather_Timestamp',
            'Weather_Condition','Description','Source','County','Turning_Loop',
            'Side','Sunrise_Sunset', 'Crossing', 'Junction',
            'Astronomical_Twilight', 'Station', 'Nautical_Twilight', 'Traffic_Signal',
            'Amenity', 'Give_Way', 'No_Exit', 'Bump', 'Roundabout', 'Traffic_Calming',
            'Stop', 'Railway', 'Severity', 'Distance(mi)']

    df = df.drop(dropCols,axis=1)





    #drop all rows with NaN ***(~55% data lost here)***
    df = df.dropna()

    if not box==None:
        lats = list(map(lambda x: x[1],box))
        lngs = list(map(lambda x: x[0],box))
        box = Polygon(np.column_stack((lats,lngs)))
        df['inBox'] = df.apply(lambda x: box.contains(Point(x['Start_Lat'],x['Start_Lng'])),axis=1)
        print(df.head())
        df = df[df['inBox']]
        df = df.drop('inBox',axis=1)

    #all only have day and night, switch to binary
    toBin = {'Day':1, 'Night':0}
    replaceDict = {'Civil_Twilight':toBin}
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

    #Wind direction also needs to be made periodic
    #first map to degrees
    windDict = {'CALM':360,
                'Calm':360,
                'SSW': 205,
                'WNW': 295,
                'NW': 315,
                'SW': 225,
                'SSE': 155,
                'WSW': 245,
                'NNW': 335,
                'South': 180,
                'West': 270,
                'SE': 135,
                'North': 360,
                'S':180,
                'NE':45, 
                'NNE':25,
                'ENE':65,
                'ESE':115,
                'W':270,
                'Variable':np.nan,
                'N':360,
                'East':90,
                'E':90,
                'VAR':np.nan}
    
    df['Wind_Direction'] = df['Wind_Direction'].replace(windDict)
    #now to cosine
    df['Wind_Direction'] = df['Wind_Direction'].apply(lambda x: np.cos(((np.pi)/180)*x))
                
    
    #df['Total_Time']
    df = df.dropna() 
    df = df.drop('Start_Time',axis=1)
    
    
    print("After dropping NaN, we have {} % of data left".format(100*(len(df)/originalSize)))
    return df
