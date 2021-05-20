import requests as req
from pickle import load
def getWeather(lat=32.8800806,lng=-117.237558):
    """fetches weather parameters for the provided latitude and longitude
    more info at https://openweathermap.org/current
    :param lat : latitude, defaults to Geisel Library latitude 
    :param lng : longitude, defaults to Geisel Library longitude 
    :raises ValueError: when invalid lat lng passed
            AssertionError: when non float input
    :return: JSON with relevant weather data
    :rtype: JSON object
    """
    assert isinstance(lat,float) and isinstance(lng,float)
    if lat > 90 or lat <-90 or lng > 180 or lng <-180:
        raise ValueError

#api.openweathermap.org/data/2.5/weather?lat=33.568483&lon=-117.731516&appid=d078ff41af2f9943ddea5b49d24e6c27
    url = 'http://api.openweathermap.org/data/2.5/weather'
    with open('../data/key.pkl','rb') as fi:
        API_KEY = load(fi)['key']
        print(API_KEY)
    params = {'lat' : lat,
              'lon' : lng,
              'appid' : API_KEY}
    r = req.get(url=url,params=params)
    print(r.json())
getWeather()
