#Testing ApiFetcher Class
import ApiFetcher
import sys
from datetime import datetime

#setting up keys
sys.path.insert(1, '/home/pi/Documents')
import cred
api_key = cred.pihole_key

pifetch = ApiFetcher.PiholeApi(cred.pihole_key, cred.pihole_ip)

commands = ['get_dailystats()', 'get_summary()', 'get_topitems()', 'get_topclients()', 'get_forwarddestinations()', 'get_querytypes()', 'get_allqueries("yes")']
for command in commands:
    print('\n', command)
    print(eval(f'pifetch.{command}'))


data = pifetch.get_topitems(3)

print('\n',data['top_queries'], '\n', data['top_ads'])

print('\n',pifetch.get_recentblocked())

querrytime = pifetch.get_allqueries()
print(querrytime)
print(querrytime[0], datetime.fromtimestamp(int(querrytime[0])).strftime('%Y-%m-%d %H:%M:%S'))

'''
sys.path.insert(1, '/home/pi/Desktop/PythonCode/Api_cred/')
import cred
api_key = cred.weather_key

wfeatch = ApiFetcher(apikey = str(cred.weather_key))
print(str(cred.weather_key))

weather = wfeatch.getweather(sun = True)
print(weather)
'''