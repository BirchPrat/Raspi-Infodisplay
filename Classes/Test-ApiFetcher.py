#Testing ApiFetcher Class
from ApiFetcher import ApiFetcher
import sys 
pihfetch = ApiFetcher()

pidat = pihfetch.get_piholedat()
print(pidat)


sys.path.insert(1, '/home/pi/Desktop/PythonCode/Api_cred/')
import cred
api_key = cred.weather_key

wfeatch = ApiFetcher(apikey = str(cred.weather_key))
print(str(cred.weather_key))

weather = wfeatch.getweather(sun = True)
print(weather)
