"""Allrounder Infodisplay"""
#giving access to relevant paths
import sys
sys.path.insert(1, '/home/pi/Documents/')
sys.path.insert(1, '/home/pi/Documents/Raspi-Infodisplay/Classes/')
sys.path.insert(1, '/home/pi/Documents/Raspi-Infodisplay/Functions/')
#Classes
import ApiFetcher, FunStuff, ModuleFetcher, SysStat, Display
#Functions
import gpio_settup, use_func, vistemp

#api credentials
import cred
#buttoncontrol and power
from gpiozero import Button
from gpiozero import OutputDevice
#DHT22 sensor library
import adafruit_dht
import board
#other
import time
from PIL import Image, ImageDraw, ImageFont 

##Setting up the Display, Buttons and Temperature Reader
button_a = Button(24) #displaybutton up
button_b = Button(23) #displaybutton down
disp = Display.Display('240x240', type="mini") #display class

temp_reader_power = OutputDevice(21) #temperature reader GPIO Pin Power
temp_reader_power.on()
dhtDevice = adafruit_dht.DHT22(board.D20, use_pulseio=False) #temperature reader data pin
time.sleep(1) #letting the sensor initialize, otherwise error may occur

#Setting up the other Class Objects
dht22 = ModuleFetcher.ModuleFetcher(dhtDevice)
weather_api = ApiFetcher.WeatherApi(cred.weather_key)
pihole_api = ApiFetcher.PiholeApi(cred.pihole_key, cred.pihole_ip)
fun = FunStuff.FunStuff()
pistat = SysStat.SysStat()

##Setting up some Variables 
#sleeping time between 0 and hoursasleep
hoursasleep = 6
sleepy = hoursasleep*60*60
temp = [1, 2]
script_start = time.time()
#refreshrate
refreshrate_tempreader = 30 #because it is slow
refreshratelist_tempreader = list(range(0,61,refreshrate_tempreader))
#fonts
font_1 = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 22)
font_small = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 12)
seperator = '+'*1000


##Main Loop with all bells and whistles
if __name__ == "__main__":
    while True:
        """Main Loop, Sys-Stats on Display"""
        timeinhours = time.strftime('%H')
        timeinseconds =  int(time.strftime('%S'))
        date = time.strftime('%d')
        pihole = pihole_api.get_dailystats()
        statnow = pistat.get_systemstats(light = 'no')
        uptime =  use_func.time_converter(time.time() - script_start)

        if timeinhours == '00': #display sleeping for 6 hours from 0-6 am
            disp.displayclear()
            disp.backlight('off')
            time.sleep(sleepy)
            disp.backlight('on')
            
        if timeinseconds in refreshratelist_tempreader:
            temp = dht22.get_temp_dht22()
        
        infolist_main = [
            [f"{time.strftime('%b %d %H:%M:%S')}", '#00b050', font_1],
            [f"Innen Temp: {temp[0]}°C", '#FC600A', font_1],
            [f"H2O Luft: {temp[1]}%", "#347B98", font_1],
            [f" ", "#347B98", font_1],
            [f"{statnow[0]}", "#576675", font_1],
            [f"Uptime: {uptime[1]} days", '#D61A46', font_1],            
            [f"{statnow[1]}", "#ffc0cb", font_1],
            [f"{statnow[2]}", "#FC600A", font_1],
            [f"{statnow[3]}", "#808080", font_1],
            [f"{statnow[4]}", "#daa520", font_1],                      
            ]
        
        disp.displaywrite(infolist_main)
     
        """Button A (Displayswitch up 1. time) - weather"""
        if button_a.is_pressed:
            disp.displayclear()
            weather = weather_api.get_weather()
            
            infolist_a = [
                [f"Time: {weather[6]}", "#00b050", font_1],
                [f"Außen Temp: {weather[1]}°C", "#FC600A", font_1],
                [f"Diff in Temp: {round(abs(temp[0] - weather[1]), 2)}°C", "#FC600A", font_1],
                [f"Außen H2O: {weather[2]}%", "#347B98", font_1],
                [f"Diff in H2O: {round(abs(temp[1]  - weather[2]), 2)}%", "#347B98", font_1],
                [f" ", "#347B98", font_1],
                [f"Windgesch: {weather[3]}kmh", "#6897bb", font_1],
                [f"Luftdruck: {weather[4]}hPa", "#3EB8C2", font_1],
                [f"Sonnenauf: {weather[7]}", "#FFE946", font_1],
                [f"Sonnenunter: {weather[8]}", "#FFA500", font_1],
                ]

            disp.displaywrite(infolist_a)

            try:
                vistemp.vistemp('/media/PiUSB', 'templogger.csv')
            except:
                pass

            presscounter_a = 0

            time.sleep(0.5)
    
            while True:
                """Button A (Displayswitch up 2. time) - weather Graphs"""
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
                total_time = time.time() - start_time
                display_time = use_func.time_converter(total_time)
                dailystats = pihole_api.get_dailystats()
                #top_clients = pihole_api.topclients()
                #top_queries = pihole_api.topitems()
                stat24 = pihole_api.get_summary()

                infolist_b1 = [
                    [f"Timer {display_time[0]}", "#00b050", font_1],
                    [f" ", "#00b050", font_1],
                    [f"Queries td: {dailystats[0]}", "#ffc0cb", font_1],
                    [f"Blocked td: {dailystats[1]}%", "#D61A46", font_1],
                    [f" ", "#00b050", font_1],                
                    [f"Queries 24H: {stat24['dns_queries_today']}", "#ffc0cb", font_1],
                    [f"Blocked 24H: {stat24['ads_percentage_today']}%", "#D61A46", font_1],
                    [f" ", "#00b050", font_1],
                    [f"Blocked Last:", "#ffc0cb", font_1],                                    
                    [f"{pihole_api.get_recentblocked()}", "#D61A46", font_1],
                    ]

                disp.displaywrite(infolist_b1)               
                          
                if button_a.is_pressed:
                    disp.displayclear()
                    time.sleep(0.5)
                    break
                
                """Button B (Displayswitch 2. time down) - Pihole Tail"""
                if button_b.is_pressed:
                    disp.displayclear()
                    shutoff_presscounter = 0
                    reboot_presscounter = 0
                    time.sleep(0.5)
                    
                    while True:
                        queri = pihole_api.get_allqueries()
                                
                        infolist_b2 = [
                            [f"{queri[1][0]}", "#00b050", font_1],
                            [f"{queri[1][2]}", "#FFFF00", font_1],
                            [f"{queri[1][3]}", "#6897bb", font_1],
                            [f"{queri[1][-2]} {queri[1][4]}", f"{queri[1][-1]}", font_1],
                            [f" ", "#00b050", font_1],                            
                            [f"{queri[0][0]}", "#00b050", font_1],
                            [f"{queri[0][2]}", "#FFFF00", font_1],
                            [f"{queri[0][3]}", "#6897bb", font_1],
                            [f"{queri[0][-2]} {queri[0][4]}", f"{queri[0][-1]}", font_1],
                            ]
                        
                        disp.displaywrite(infolist_b2)                          
                  
                        if button_a.is_pressed:
                            disp.displayclear()
                            time.sleep(0.5)
                            break
  
                        """Button B (Displayswitch 3. time down) - Shutdown/Reboot"""
                        if button_b.is_pressed:
                            
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


                