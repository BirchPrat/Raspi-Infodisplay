# Weather Display##
###################

# Importing necessary python libraries
import time
import json
import subprocess
import requests
from random import choice

import sys
sys.path.insert(1, '/home/pi/Desktop/PythonCode/Api_cred/')
import cred

import digitalio
import board

#Import for the temperature reader
from gpiozero import OutputDevice
import Adafruit_DHT 

# Import Python Imaging Library
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789

##### Temperature Reader Settup
#Supplying the temeperature reader with GPIO pin power
GPIO_PIN = 21
power = OutputDevice(GPIO_PIN)
power.on()

#Data input pin
DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 20

#temperature fetcher function
def tempfetcher():
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    
    humi = round(humidity,2)
    temp = round(temperature, 2)
    
    return [temp, humi]
 
#### Pihole settup
#apiurl for pihole stats
api_url = 'http://localhost/admin/api.php?overTimeData10mins'
def get_piholedatv1():
    try:
        r = requests.get(api_url)
        data = json.loads(r.text)
        DNSQUERIES = sum(data['domains_over_time'].values())
        ADS = sum(data['ads_over_time'].values())
        ADSBLOCKED = round((ADS/DNSQUERIES)*100, 2)
    except KeyError:
        pass
     
    return [DNSQUERIES, ADSBLOCKED, ADS]

def dayquerrycalc(dnsdic):
    dayquerry = 0
    date = int(time.strftime('%d'))
    for key,value in dnsdic.items():
        keyint = int(time.strftime("%d", time.gmtime(int(key))))
        valueint = int(value)
        if keyint == date:
            dayquerry = valueint + dayquerry        
    return(dayquerry)

def get_piholedatv2():
    try:
        r = requests.get(api_url)
        data = json.loads(r.text)
        DNSQUERIES = dayquerrycalc(data['domains_over_time'])
        ADS = dayquerrycalc(data['ads_over_time'])
        try:
            ADSBLOCKED = round((ADS/DNSQUERIES)*100, 2)
        except ZeroDivisionError:
            ADSBLOCKED = 0
    except KeyError:
        pass
     
    return [DNSQUERIES, ADSBLOCKED, ADS]

#### System Stats Settup
# Shell scripts for system monitoring:
def get_systemstats():
    #cmd = "top -bn1 | grep load | awk '{printf \"%.2f\", $(NF-2)}'"
    #CPU = subprocess.check_output(cmd, shell=True).decode("utf-8")
    #cmd = "free -m | awk 'NR==2{printf \"%s/%s\", $3,$2,$3*100/$2 }'"
    #MemUsage = subprocess.check_output(cmd, shell=True).decode("utf-8")
    cmd = "cat /sys/class/thermal/thermal_zone0/temp |  awk '{printf \"%.1f\", $(NF-0) / 1000}'"  # pylint: disable=line-too-long
    Temp = subprocess.check_output(cmd, shell=True).decode("utf-8")
    
    return [Temp]

# Uptime
def get_uptime(): 
    with open('/proc/uptime', 'r') as f:
        uptime_seconds = float(f.readline().split()[0])
        uptime_minutes = uptime_seconds/60
        uptime_hours = uptime_minutes/60
        uptime_days = uptime_hours/24
        return uptime_days

#### Weather API Settup
#getting the api_key
api_key = cred.weather_key

#Api fetch function
def get_weather(api_key, location):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&units=metric&appid={api_key}"
    r = requests.get(url)
    return r.json()

#Weatheroutput function
def weatherout():
    
    try:
        weather = get_weather(api_key, "Cologne")

        currenttemp = weather['main']['temp']
        humidity = weather['main']['humidity']
        windspeed = weather['wind']['speed']
        clouds = weather['clouds']['all']
        pressure = weather['main']['pressure']
        city = weather['name']
        
        return [city, currenttemp, humidity, windspeed, pressure, clouds]
    
    except KeyError or OSError:
        problem = "Api Failed"
        
        return [problem]

#food suggest function
foodlist = ["Hamburger", "Geschnetzeltes", "Bolognese", 
	"Korean Chicken", "Bulgogi", "Wraps", 
	"Curry", "Lasagne", "Flammkuchen", 
	"Pizza", "Gefüllte Paprika", "Gemüsesuppe"]


def foodchoice(foodlist):
    food = choice(foodlist).title()
    return food

#####Display Settup
# Configuration for CS and DC pins (these are FeatherWing defaults on M0/M4):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = None

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 64000000

# Setup SPI bus using hardware SPI:
spi = board.SPI()

# Create the ST7789 display:
disp = st7789.ST7789(spi, cs=cs_pin, dc=dc_pin, rst=reset_pin, baudrate=BAUDRATE,
                     width=135, height=240, x_offset=53, y_offset=40)

# Create blank image for drawing.
# Make sure to create image with mode 'RGB' for full color.
height = disp.width   # we swap height/width to rotate it to landscape!
width = disp.height
image = Image.new('RGB', (width, height))
rotation = 90

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
disp.image(image, rotation)
# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height-padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0

# Alternatively load a TTF font.  Make sure the .ttf font file is in the
# same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 22)
font2 = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 45)

# Turn on the backlight
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True

# Add buttons as inputs
buttonA = digitalio.DigitalInOut(board.D23)
buttonA.switch_to_input()

buttonB = digitalio.DigitalInOut(board.D24)
buttonB.switch_to_input()

#####Main Loop Running Constantly
while True:
    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)
    y = top
    
    timeofday = time.strftime('%H')
    date = time.strftime('%d')
    
    if timeofday == '00': #display sleeping for 6 hours from 0-6 am
        backlight.value = False
        hoursasleep = 6
        sleepy = hoursasleep*60*60
        time.sleep(sleepy)
        backlight.value = True
    
    elif not buttonA.value:  # just button A pressed
        weather = weatherout()
        
        if len(weather) > 1:
        
            #return [city, currenttemp, humidity, windspeed, winddirection, clouds]
            draw.text((x, y), "Stadt: {}".format(str(weather[0])), font=font, fill="#D85930")
            y += font.getsize(str(weather[0]))[1]
            
            draw.text((x, y), "Außen Temp: {}C".format(str(weather[1])), font=font, fill="#E06565")
            y += font.getsize(str(weather[1]))[1]
     
            draw.text((x, y), "H2O Luft: {}%".format(str(weather[2])), font=font, fill="#145FA7")
            y += font.getsize(str(weather[2]))[1]
            
            draw.text((x, y), "Windgesch: {}kmh".format(str(weather[3])), font=font, fill="#3EB8C2")
            y += font.getsize(str(weather[3]))[1]      
            
            draw.text((x, y), "Luftdruck: {}hPa".format(str(weather[4])), font=font, fill="#37AEC3")
            y += font.getsize(str(weather[4]))[1]
            
            draw.text((x, y), "Wolkendichte: {}%".format(str(weather[5])), font=font, fill="#B2BBA7")
            y += font.getsize(str(weather[5]))[1]
           
           # Display image.
            disp.image(image, rotation)
            time.sleep(30)
            
        else:
            draw.text((x, y), "{}".format(str(weather[0])), font=font, fill="#D85930")
            y += font.getsize(str(weather[0]))[1]
            
             # Display image.
            disp.image(image, rotation)
            time.sleep(5)
        
    
    elif not buttonB.value: # just button B pressed
        
        msg = "I <3 Batzi"
        
        draw.text((x, y), msg, font=font2, fill="#ff0000")
        y += font2.getsize(str(msg))[1]

        #uptime = round(get_uptime(), 2)
        #draw.text((x, y), f"Uptime in Days: {uptime}", font=font, fill="#B2BBA7")
        
        food = foodchoice(foodlist)
        draw.text((x, y), f"{food}?", font=font, fill="#B2BBA7")
        
        # Display image.
        disp.image(image, rotation)
        time.sleep(5)       
     
    else:
        roomtemp = tempfetcher()
        sysstats = get_systemstats()
        pystats = get_piholedatv2()
           
        draw.text((x, y), "{}".format(time.strftime('%b %d %H:%M:%S')), font=font, fill="#D61A46")
        y += font.getsize(str(roomtemp[0]))[1]
  
        draw.text((x, y), "Innen Temp: {}C".format(str(roomtemp[0])), font=font, fill="#FC600A")
        y += font.getsize(str(roomtemp[0]))[1]
        
        draw.text((x, y), "H2O Luft: {}%".format(str(roomtemp[1])), font=font, fill="#347B98")
        y += font.getsize(str(roomtemp[1]))[1]
        
        draw.text((x, y), "CPU Temp: {}C".format(str(sysstats[0])), font=font, fill="#FB9902")
        y += font.getsize(str(sysstats[0]))[1]
       
        draw.text((x, y), "DNS Queries: {}".format(str(pystats[0])), font=font, fill="#9BD770")
        y += font.getsize(str(pystats[0]))[1]
        
        draw.text((x, y), "Ads Blocked: {}%".format(str(pystats[1])), font=font, fill="#66B032")
        y += font.getsize(str(pystats[1]))[1]

        """
        draw.text((x, y), "{}".format(time.strftime('%b %d %Y %H:%M:%S')), font=font, fill="#FF0000")
        y += font.getsize(str(roomtemp[0]))[1]
  
        draw.text((x, y), "Innen Temp: {}C".format(str(roomtemp[0])), font=font, fill="#FF7F00")
        y += font.getsize(str(roomtemp[0]))[1]
        
        draw.text((x, y), "H2O Luft: {}%".format(str(roomtemp[1])), font=font, fill="#FFFF00")
        y += font.getsize(str(roomtemp[1]))[1]
        
        draw.text((x, y), "CPU Temp: {}C".format(str(sysstats[0])), font=font, fill="#00cc1a")
        y += font.getsize(str(sysstats[0]))[1]
       
        draw.text((x, y), "DNS Queries: {}".format(str(pystats[0])), font=font, fill="#0000FF")
        y += font.getsize(str(pystats[0]))[1]
        
        draw.text((x, y), "Ads Blocked: {}%".format(str(pystats[1])), font=font, fill="#7700cc")
        y += font.getsize(str(pystats[1]))[1]
        """
         # Display image.
        disp.image(image, rotation)
        time.sleep(1)

   
