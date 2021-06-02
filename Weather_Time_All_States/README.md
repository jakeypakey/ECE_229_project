# The Accident rate per County per State
## Create Plotly DASH plot with three dropdown menus organized as follows:  

### State 
48 States not including Hawaii and Alaska are considered  
### Weather  
6 Weather categories - Rain, Clear, Fog, Snow, Cloudy, Dust
### Time of Day  
- Day: 06:00 to 11:59
- Noon: 12:00 to 17:59
- Night: 18:00 to 05:59

### To run:  
Run All_States_Plots.ipynb  
- fip_dict_pop.pickle file included  
- fipkey_popvalue.pickle file included  
- contact scw039@ucsd.edu for processed_data_all_states.csv

### Analysis:
-Accidents generally occur at similar rates during the day and noon, and less at night

-In accidents occur the least during dusty conditions, but dust conditions have the least amount of accident data available

-Rainy conditions seems to have generally low levels of incidence. 

-Clear weather seems to generally have more accidents than any other weather condition. This seems to be true regardless of population size or location
  - For instance, in Alameda county (FIP id 06001), accidents per 1000 people go up from 2.16 in rainy condition to 13.06 in clear conditions

- Snow doesn't affect all areas equally for obvious reaons. Counties with extremely high rates of snow correlates with high incidence rate, but generally snowy areas don't seem experience a significant change in accident rate in under snowy conditions. Maine is one of the snowiest states in the US, averaging around 50-70 inches in the Coastal Division and 90 to 110 inches in the Northern Interior. However, Maine has more accidents in clear weather than in snowy weather. Under snowy conditions, for every 1000 people, Cumberland County (23005) has 0.231 accidents, but has 1.27 accidents under clear conditions. In a more extreme example, Alpine County of California averages around 192 inches of snow a year, but has up to 33 snow related accidents per 1000 people. It also has around 30 accidents per 1000 people under clear conditions.

- Counties with high accident rates in any one weather condition are likely to also have high accident rates under all weather conditions.


-Potential biases
  - Clear and cloudy weather occur more than other types of weather in general, so more instances of accidents should occur under those conditions even if they may happen at a higher rate under other weather conditions
  - Some counties have dramatically lower population than others. This is accounted for by normalizing by population, but doing this may overemphasize the significance of small, outlier data

