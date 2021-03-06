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
           
    def get_weather(self, location = 'Cologne', info = False):
        """Weatheroutput function"""
        try:
            url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&units=metric&appid={self.apikey}"
            r = requests.get(url)
            weather = json.loads(r.text)
            
            if info:
                pprint.pprint(weather)
            
            else:
                currenttemp = weather['main']['temp']
                humidity = weather['main']['humidity']
                windspeed = weather['wind']['speed']
                clouds = weather['clouds']['all']
                pressure = weather['main']['pressure']
                city = weather['name']
                currenttime = time.strftime("%b %d %H:%M", time.localtime(int(weather['dt'])))
                sunrise = time.strftime("%H:%M", time.localtime(int(weather['sys']['sunrise'])))
                sunset = time.strftime("%H:%M", time.localtime(int(weather['sys']['sunset'])))

                return [city, currenttemp, humidity, windspeed, pressure, clouds, currenttime, sunrise, sunset]

        except:
            currenttemp, humidity, windspeed, clouds, pressure, city, currenttime, sunrise, sunset = "F"*9

            return [city, currenttemp, humidity, windspeed, pressure, clouds, currenttime, sunrise, sunset]
        
        
        
        
        
        

        
