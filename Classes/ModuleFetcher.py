import Adafruit_DHT


class ModuleFetcher:
    """ModuleFetcher Class, for fetching data from pi modules"""
    def __init__(self, dht22_pin = '', dht22 = ''):
        self.dht22_pin = dht22_pin
        self.dht22 = dht22

    def tempfetcher_dht22(self):
        """Geting the data from the dht22 sensor using circuit python library"""
        try:

            humidity, temperature = self.dht22.humidity, self.dht22.temperature
                    
            humi = round(humidity,2)
            temp = round(temperature, 2)
            
        except:
            humi = "failed"
            temp = "failed"
            
        return [temp, humi]

    def tempfetcher_dht22_old(self):
        """Geting the data from the dht22 sensor using old library"""
        try:
            humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, self.dht22_pin)
                    
            humi = round(humidity,2)
            temp = round(temperature, 2)
            
        except TypeError:
            humi = "failed"
            temp = "failed"
            
        return [temp, humi]