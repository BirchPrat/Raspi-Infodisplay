#Module Fetcher test
from ModuleFetcher import ModuleFetcher
from gpiozero import OutputDevice
import adafruit_dht
import board
import time
#import adafruit_bme280 


"""Powering DHT22 with provided pin number """
#power = OutputDevice(21)
#power.on()

"""Setting up the data pin for dht22"""
dhtDevice = adafruit_dht.DHT22(board.D20, use_pulseio=False)

time.sleep(1) #letting the sensor initialize


dht22 = ModuleFetcher(dhtDevice)


temp = dht22.get_temp_dht22()
print(temp)

'''

##Preparation
i2c = board.I2C()  # uses board.SCL and board.SDA
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)

print(f'{bme280}')

sensorstat = ModuleFetcher(bme280)

temp = sensorstat.get_temp_bme280()

print(temp)
'''