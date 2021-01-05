#Module Fetcher test
from ModuleFetcher import ModuleFetcher
from gpiozero import OutputDevice
import adafruit_dht
import board
import time

"""Powering DHT22 with provided pin number """
power = OutputDevice(21)
power.on()

"""Setting up the data pin for dht22"""
dhtDevice = adafruit_dht.DHT22(board.D20, use_pulseio=False)

time.sleep(1) #letting the sensor initialize


dht22 = ModuleFetcher(dht22 = dhtDevice)


temp = dht22.tempfetcher_dht22()
print(temp)