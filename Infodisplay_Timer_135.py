"""Allrounder Infodisplay"""
#giving access to relevant paths
import sys
sys.path.insert(1, '/home/pi/Documents/')
sys.path.insert(1, '/home/pi/Documents/Raspi-Infodisplay/Classes/')
sys.path.insert(1, '/home/pi/Documents/Raspi-Infodisplay/Functions/')
#Classes
import ApiFetcher, ModuleFetcher, SysStat, Display
#Functions
import use_func, vistemp

#api credentials
import cred
#buttoncontrol and power
from gpiozero import Button
from gpiozero import OutputDevice

#DHT22 sensor library
import adafruit_dht
#import adafruit_bme280 
import board

#other
import time
from PIL import ImageFont 
import threading

##Setting up the Display, Buttons and Temperature Reader
button_a = Button(24) #displaybutton up
button_b = Button(23) #displaybutton down
disp = Display.Display('240x240', type="mini", font_location = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf') #display class
#disp = Display.Display('240x240', type="gamepad", rotate = 180, font_location = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf') #display class

##Preparing sensor
temp_reader_power = OutputDevice(21) #temperature reader GPIO Pin Power
temp_reader_power.on()
dhtDevice = adafruit_dht.DHT22(board.D20, use_pulseio=False) #temperature reader data pin
time.sleep(1) #letting the sensor initialize, otherwise error may occur

#i2c = board.I2C()  # uses board.SCL and board.SDA
#bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)

#Setting up the other Class Objects
sensorstat = ModuleFetcher.ModuleFetcher(dhtDevice)
weather_api = ApiFetcher.WeatherApi(cred.weather_key)
pihole_api = ApiFetcher.PiholeApi(cred.pihole_key, cred.pihole_ip)
pistat = SysStat.SysStat()

##Setting up some Variables 
#sleeping time for 6 hours
sleepy = 6*60*60
script_start = time.time()

#concurrently running refresh functions in threads
def weather_refresh(sleeptime = 6*60*60, refreshtime = 60*10):
    '''threading function for weather refresh'''
    global weather

    while True:
        if time.strftime('%H') == '00':
                time.sleep(sleeptime)
        else:
            weather = weather_api.get_weather_onecall()
            time.sleep(refreshtime)

def temp_refresh(sleeptime = 6*60*60, refreshtime = 30):
    '''threading function for temp refresh'''
    global temp

    while True:
        if time.strftime('%H') == '00':
                time.sleep(sleeptime)
        else:
            temp = sensorstat.get_temp_dht22()
            time.sleep(refreshtime)

weather_thread = threading.Thread(target=weather_refresh)
temp_thread = threading.Thread(target=temp_refresh)

#fonts
font_1 = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 22)

#getting some initial data
temp = sensorstat.get_temp_dht22()
weather = weather_api.get_weather_onecall()

#starting updating Threads
weather_thread.start()
temp_thread.start()

##Main Loop with all bells and whistles
if __name__ == "__main__":
    while True:
        """Main Loop, Sys-Stats on Display"""
        #display sleeping for 6 hours from 0-6 am
        if time.strftime('%H') == '00':
            disp.displayclear()
            disp.backlight('off')
            time.sleep(sleepy)
            disp.backlight('on')

        #getting data to display
        uptime =  use_func.time_converter(time.time() - script_start)

        #displaying default system and temp stats
        disp.display_main_weather(temp, pistat, uptime, weather[0])

        """Button A (Displayswitch up 1. time) - weather daily clock"""
        if button_a.is_pressed:
            disp.displayclear()
            time.sleep(0.5)

            while True:
                if button_b.is_pressed:
                    disp.displayclear()
                    time.sleep(0.5)
                    break

                disp.display_weatherclock(weather, temp)
                
                time.sleep(0.5)

                """Button A (Displayswitch up 2. time) - weather weekly"""
                if button_a.is_pressed:
                    disp.displayclear()
                    #getting some initial data
                    temp = sensorstat.get_temp_dht22()

                    while True:
                        if button_b.is_pressed:
                            disp.displayclear()
                            time.sleep(0.5)
                            break              

                        disp.display_weather_week(weather)

                        time.sleep(0.5)

                        """Button A (Displayswitch up 3. time) - weather Graphs"""
                        if button_a.is_pressed:
                            disp.displayclear()
                            if button_b.is_pressed:
                                disp.displayclear()
                                time.sleep(0.5)
                                break  
                            #creating graphs
                            try:
                                vistemp.vistemp('/media/PiUSB', 'templogger.csv')
                            except:
                                pass
                            presscounter_a = 1  
                            while True:
                                if button_b.is_pressed:
                                    disp.displayclear()
                                    time.sleep(0.5)
                                    break

                                if button_a.is_pressed:    
                                    presscounter_a += 1
                                
                                if presscounter_a == 1:
                                    disp.displaypic('/media/PiUSB/hourly_temp.png')
                                elif presscounter_a == 2:
                                    disp.displaypic('/media/PiUSB/daily_temp.png')
                                elif presscounter_a == 3:
                                    disp.displaypic('/media/PiUSB/weekly_temp.png')
                                    
                                time.sleep(1)

        """Button B (Displayswitch down 1. Time) - Pihole Infos"""  
        if button_b.is_pressed:
            disp.displayclear()
            time.sleep(0.5) # to reduce double clicks
            
            start_time = time.time()

            while True:
                if button_a.is_pressed:
                    disp.displayclear()
                    time.sleep(0.5)
                    break
                
                total_time = time.time() - start_time
                display_time = use_func.time_converter(total_time)
                pihole_dailystats = pihole_api.get_dailystats()
                pihole_summary = pihole_api.get_summary()
                recent_blocked = pihole_api.get_recentblocked()

                disp.display_piholedat_v1(pihole_dailystats, pihole_summary, display_time[0], recent_blocked)
                
                """Button B (Displayswitch 2. time down) - Pihole Tail"""
                if button_b.is_pressed:
                    disp.displayclear()
                    time.sleep(0.5)
                    
                    while True:                                 
                        if button_a.is_pressed:
                            disp.displayclear()
                            time.sleep(0.5)
                            break
                    
                        disp.display_piholedat_tail(pihole_api.get_allqueries())                          
  
                        """Button B (Displayswitch 3. time down) - Shutdown/Reboot"""
                        if button_b.is_pressed:
                            shutoff_presscounter = 0
                            reboot_presscounter = 0

                            while True:
                                infolist_b3 = [
                                    ["Shutdown hold UP", "#950a24", font_1],
                                    [f"Shutdown in {10-shutoff_presscounter}", "#950a24", font_1],
                                    [f" ", "#00b050", font_1],
                                    ["Reboot hold LB", "#00b050", font_1],
                                    [f"Reboot in {10-reboot_presscounter}", "#00b050", font_1],
                                    [f" ", "#00b050", font_1],
                                    ["To quit press UP & LB 5x", "#fa9632", font_1],
                                    ]
                                disp.displaywrite(infolist_b3)
                                
                                if button_a.is_pressed:
                                    shutoff_presscounter += 1
                                elif button_b.is_pressed:
                                    reboot_presscounter += 1
                                    
                                if shutoff_presscounter == 10:
                                    infolist_b3a = [
                                        ["Shutting down!", "#ff0000", font_1],
                                        ["Good Bye :)", "#ff0000", font_1],
                                    ]
                                    disp.displaywrite(infolist_b3a)
                                    pistat.shut_down()
                                    time.sleep(15)
                                
                                if reboot_presscounter == 10:
                                    infolist_b3b = [
                                        ["Rebooting!", "#ff0000", font_1],
                                        ["See you soon :)", "#ff0000", font_1],
                                    ]
                                    disp.displaywrite(infolist_b3b)
                                    pistat.reboot()
                                    time.sleep(15)
                                
                                if reboot_presscounter >= 5 & shutoff_presscounter >= 5:
                                    break
                            
                                time.sleep(0.1)
                                
                        
                        time.sleep(1)
                
                
                time.sleep(0.5)
        
              
        time.sleep(0.5)

                