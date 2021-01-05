import requests
import json
import time
import pprint

class ApiFetcher:
    """ApiFetcher Class, for fetching data from Api's"""
    def __init__(self, apikey = ''):
        self.apikey = apikey

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

    def get_piholedat(self, lasttwentyfour = 'no'):     
        """Pihole Data Gatherer"""
        api_url = 'http://localhost/admin/api.php?overTimeData10mins'
        try:
            r = requests.get(api_url)
            data = json.loads(r.text)
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


    def getweather(self, location = 'Cologne', info = False):
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
                currenttime = time.strftime("%H:%M", time.localtime(int(weather['dt'])))
                sunrise = time.strftime("%H:%M", time.localtime(int(weather['sys']['sunrise'])))
                sunset = time.strftime("%H:%M", time.localtime(int(weather['sys']['sunset'])))

                return [city, currenttemp, humidity, windspeed, pressure, clouds, currenttime, sunrise, sunset]

        except:
            currenttemp, humidity, windspeed, clouds, pressure, city, currenttime, sunrise, sunset = "F"*9

            return [city, currenttemp, humidity, windspeed, pressure, clouds, currenttime, sunrise, sunset]

       
        
        

        
