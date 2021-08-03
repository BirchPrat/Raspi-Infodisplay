

class ModuleFetcher:
    """ModuleFetcher Class, for fetching data from pi modules"""
    def __init__(self, temp_module = ''):
        self.temp_module = temp_module

    def get_temp_bme280(self):
        """Geting the data from either dht22 or bme280"""
        for attempt in range(5):
            try:
                temp = round(self.temp_module.temperature, 2)
                humid = round(self.temp_module.relative_humidity, 2)
                pressure = round(self.temp_module.pressure, 2)
                return [temp, humid, pressure]
            except:
                temp = 'NaN'
                humid = 'NaN'
                pressure = 'NaN'
        return [temp, humid, pressure]
            
    def get_temp_dht22(self):
        for attempt in range(10):
            try:
                temp = round(self.temp_module.temperature, 2)
                humid = round(self.temp_module.humidity, 2)
                pressure = 'NaN'
                return [temp, humid, pressure]
            except:
                temp = 'NaN'
                humid = 'NaN'
                pressure = 'NaN'
        return [temp, humid, pressure] 
        




