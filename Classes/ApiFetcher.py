import requests
import json
import time
import pprint
from datetime import datetime

class PiholeApi:
    """Pihole Api data gatherer"""
    def __init__(self, apikey = '', ipadress = 'localhost'):
        self.apikey = apikey
        self.ipadress = ipadress
        self.api_url = f'http://{self.ipadress}/admin/api.php'
        self.auth = f'&auth={self.apikey}'

    #Helper Function:
    def piholedat(self, query, authreq = 'no'):
        if authreq == 'no':
            data = requests.get(self.api_url + query)
        else:
            data = requests.get(self.api_url + query + self.auth)

        return json.loads(data.text)
    
    def dayquerrycalc(self, dnsdic):
        """Calculating ads per 24h cycle within pihole api"""
        dayquerry = 0
        date = int(time.strftime('%d'))
        for key,value in dnsdic.items():
            keyint = int(time.strftime("%d", time.localtime(int(key))))
            valueint = int(value)
            if keyint == date:
                dayquerry = valueint + dayquerry         
        return(dayquerry)

    #Data Getters
    def get_dailystats(self, lasttwentyfour = 'no'):     
        """Pihole Data Gatherer"""
        try:
            data = self.piholedat('?overTimeData10mins')
            if lasttwentyfour == 'yes':
                DNSQUERIES = sum(data['domains_over_time'].values())
                ADS = sum(data['ads_over_time'].values())
                ADSBLOCKED = round((ADS/DNSQUERIES)*100, 2)
            else:
                DNSQUERIES = self.dayquerrycalc(data['domains_over_time'])
                ADS = self.dayquerrycalc(data['ads_over_time'])
                try:
                    ADSBLOCKED = round((ADS/DNSQUERIES)*100, 2)
                except ZeroDivisionError:
                    ADSBLOCKED = 0
        
            return [DNSQUERIES, ADSBLOCKED, ADS]

        except:
            DNSQUERIES = None
            ADSBLOCKED = None
            ADS = None
            return [DNSQUERIES, ADSBLOCKED, ADS]
        
    def get_summary(self):
        return self.piholedat('?summary')
    
    def get_topitems(self, itemnum = '10'):
        return self.piholedat(f'?topItems={itemnum}', 'yes')
    
    def get_topclients(self):
        return self.piholedat('?topClients', 'yes')

    def get_forwarddestinations(self):
        return self.piholedat('?getForwardDestinations', 'yes')
    
    def get_querytypes(self):
        return self.piholedat('?getQueryTypes', 'yes')
    
    def get_allqueries(self, mostrecent = 'yes'):
        if mostrecent == 'yes':
            queries = self.piholedat('?getAllQueries', 'yes')
            mostrecent = queries['data'][-3:-1]
            
            for i in mostrecent:
                i[0] = datetime.fromtimestamp(int(i[0])).strftime('%b %d %H:%M:%S')
                
                #queri type color coding
                if int(i[4]) == 0:
                    i.append('Unknown')
                    i.append('#808080')
                elif int(i[4]) in range(2,4):
                    i.append('Allowed')
                    i.append('#00FF00')
                elif int(i[4]) >=12:
                    i.append('Allowed')
                    i.append('#00FF00')
                else:
                    i.append('Blocked')
                    i.append('#FF0000')
            
            return mostrecent
                    
        return self.piholedat('?getAllQueries', 'yes')
    
    def get_recentblocked(self):
        r = requests.get(self.api_url + '?recentBlocked' + self.auth)
        return r.text
    
    def pi_enable(self):
        requests.get(self.api_url + '?enable' + self.auth)
        return None
    
    def pi_disable(self, time='15'):
        requests.get(self.api_url + '?disable' + self.auth)
        return None
    
      
class WeatherApi:
    """ApiFetcher Class, for fetching data from Api's"""
    def __init__(self, apikey = ''):
        self.apikey = apikey
           
    def get_weather(self, latitude = '50.96', longitude = '7.00', info = False):
        print('getting current weather')
        """Current weather data"""
        try:
            url = f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&units=metric&appid={self.apikey}"
            r = requests.get(url)
            weather = json.loads(r.text)
            
            if info:
                pprint.pprint(weather)
            
            else:
                currenttemp = weather['main']['temp']
                temp_max = weather['main']['temp_max']
                temp_min = weather['main']['temp_min']
                humidity = weather['main']['humidity']
                windspeed = weather['wind']['speed']
                clouds = weather['clouds']['all']
                pressure = weather['main']['pressure']
                city = weather['name']
                currenttime = time.strftime("%b %d %H:%M", time.localtime(int(weather['dt'])))
                sunrise = time.strftime("%H:%M", time.localtime(int(weather['sys']['sunrise'])))
                sunset = time.strftime("%H:%M", time.localtime(int(weather['sys']['sunset'])))

                return [city, currenttemp, humidity, windspeed, pressure, clouds, currenttime, sunrise, sunset, temp_min, temp_max]

        except:
            currenttemp, humidity, windspeed, clouds, pressure, city, currenttime, sunrise, sunset = "F"*9

            return [city, currenttemp, humidity, windspeed, pressure, clouds, currenttime, sunrise, sunset]
        
        
    def get_weather_onecall(self, latitude = '50.96', longitude = '7.00', info = False):
        print('getting weather onecall')
        """Current and future weather data"""
        try:
            url = f"https://api.openweathermap.org/data/2.5/onecall?lat={latitude}&lon={longitude}&units=metric&exclude=minutely,alerts&appid={self.apikey}"
            r = requests.get(url)
            weather = json.loads(r.text)
        
            if info:
                pprint.pprint(weather)
            
            else:
                #hourly weather
                hourly_weather = []
                for num in range(0,12):
                    time_detailed = time.strftime("%b %d %H:%M", time.localtime(int(weather['hourly'][num]['dt'])))
                    time_hour = time.strftime("%I", time.localtime(int(weather['hourly'][num]['dt'])))
                    temp = weather['hourly'][num]['temp']
                    humidity = weather['hourly'][num]['humidity']
                    clouds = weather['hourly'][num]['clouds']
                    pressure = weather['hourly'][num]['pressure']
                    rain_prob = weather['hourly'][num]['pop']


                    list_now = [time_detailed, time_hour, temp, humidity, clouds, pressure, rain_prob]

                    hourly_weather.append(list_now)

                #current weather
                temp = weather['current']['temp']
                humidity = weather['current']['humidity']
                windspeed = weather['current']['wind_speed']
                clouds = weather['current']['clouds']
                pressure = weather['current']['pressure']
                currenttime = time.strftime("%b %d %H:%M", time.localtime(int(weather['current']['dt'])))
                sunrise = time.strftime("%H:%M", time.localtime(int(weather['current']['sunrise'])))
                sunset = time.strftime("%H:%M", time.localtime(int(weather['current']['sunset'])))

                current_weather = [currenttime, temp, humidity, windspeed, clouds, pressure, sunrise, sunset]
                
                #daily weather
                daily_weather = []
                for num in range(8):
                    time_detailed = time.strftime("%b %d %H:%M", time.localtime(int(weather['daily'][num]['dt'])))
                    time_day = time.strftime("%a", time.localtime(int(weather['daily'][num]['dt'])))
                    temp = weather['daily'][num]['temp']
                    humidity = weather['daily'][num]['humidity']
                    clouds = weather['daily'][num]['clouds']
                    pressure = weather['daily'][num]['pressure']
                    rain_prob = weather['daily'][num]['pop']


                    list_now = [time_detailed, time_day, temp, humidity, clouds, pressure, rain_prob]

                    daily_weather.append(list_now)  

                return [current_weather, hourly_weather, daily_weather]

        except:
            hourly_weather = []
            for num in range(1,13):
                time_detailed, time_hour, temp, humidity, clouds, pressure, rain_prob = "F"*7
                list_now = [time_detailed, time_hour, temp, humidity, clouds, pressure, rain_prob]
                hourly_weather.append(list_now)

            daily_weather = []
            for num in range(8):
                time_detailed, time_day, temp, humidity, clouds, pressure, rain_prob = 'F'*7
                list_now = [time_detailed, time_day, temp, humidity, clouds, pressure, rain_prob]
                daily_weather.append(list_now)

            currenttime, temp, humidity, clouds, pressure, sunrise, sunset = "F"*7
            current_weather = [currenttime, temp, humidity, clouds, pressure, sunrise, sunset]

            return [current_weather, hourly_weather, daily_weather]

    def get_weather_daily(self, latitude = '50.96', longitude = '7.00', info = False):
        print('getting weekly weather')
        try:
            url = f"https://api.openweathermap.org/data/2.5/onecall?lat={latitude}&lon={longitude}&units=metric&exclude=minutely,hourly,alerts&appid={self.apikey}"
            r = requests.get(url)
            weather = json.loads(r.text)
        
            if info:
                pprint.pprint(weather)   
            else:
                daily_weather = []
                for num in range(8):
                    time_detailed = time.strftime("%b %d %H:%M", time.localtime(int(weather['daily'][num]['dt'])))
                    time_day = time.strftime("%a", time.localtime(int(weather['daily'][num]['dt'])))
                    temp = weather['daily'][num]['temp']
                    humidity = weather['daily'][num]['humidity']
                    clouds = weather['daily'][num]['clouds']
                    pressure = weather['daily'][num]['pressure']
                    rain_prob = weather['daily'][num]['pop']


                    list_now = [time_detailed, time_day, temp, humidity, clouds, pressure, rain_prob]

                    daily_weather.append(list_now)  
            return daily_weather

        except:
            daily_weather = []
            for num in range(8):
                time_detailed, time_day, temp, humidity, clouds, pressure, rain_prob = "F"*7
                list_now = [time_detailed, time_day, temp, humidity, clouds, pressure, rain_prob]
                daily_weather.append(list_now)
            return daily_weather


