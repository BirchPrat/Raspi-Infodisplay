"""Allrounder Infodisplay"""
#giving access to relevant paths
import sys
sys.path.insert(1, '/home/pi/Desktop/PythonCode/Api_cred/')
sys.path.insert(1, '/home/pi/Desktop/PythonCode/Display/Classes/')
sys.path.insert(1, '/home/pi/Desktop/PythonCode/Display/Functions/')
#Classes
import ApiFetcher, FunStuff, ModuleFetcher, SysStat
#Functions
import draw_st7789, gpio_settup, use_func 
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
button_a = Button(23)
button_b = Button(24)
#button_c = Button(13)
#button_d = Button(5)
disp = gpio_settup.displaysettup()
draw_st7789.clearimage(disp)
temp_reader_power = OutputDevice(21) #temperature reader GPIO Pin Power
temp_reader_power.on()
dhtDevice = adafruit_dht.DHT22(board.D20, use_pulseio=False) #temperature reader data pin
time.sleep(1) #letting the sensor initialize, otherwise error may occur

#Setting up the Class Objects
dht22 = ModuleFetcher.ModuleFetcher(dht22 = dhtDevice)
apidat = ApiFetcher.ApiFetcher(apikey = str(cred.weather_key))
fun = FunStuff.FunStuff()
pistat = SysStat.SysStat()

##Setting up some Variables 
#sleeping time between 0 and hoursasleep
hoursasleep = 6
sleepy = hoursasleep*60*60
#refreshrate
refreshrate_tempreader = 30 #because it is slow
refreshratelist_tempreader = list(range(0,61,refreshrate_tempreader))
#fonts
font_1 = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 22)
font_2 = ImageFont.truetype('/home/pi/Desktop/PythonCode/Fonts/Filxgirl.TTF', 25)

##Main Loop with all bells and whistles
if __name__ == "__main__":
    while True:
        """Main Loop, Sys-Stats on Display"""
        timeinhours = time.strftime('%H')
        timeinseconds =  int(time.strftime('%S'))
        date = time.strftime('%d')
        shutoff_presscounter = 0
        reboot_presscounter = 0
        pihole = apidat.get_piholedat()
        statnow = pistat.get_systemstats()        

        if timeinhours == '00': #display sleeping for 6 hours from 0-6 am
            draw_st7789.clearimage(disp)
            time.sleep(sleepy)
            
        if timeinseconds in refreshratelist_tempreader:
            temp = dht22.tempfetcher_dht22()

        try:
            infosdic = {
                time.strftime('%b %d %H:%M:%S'):["", "#D61A46", font_1],
                f"{temp[0]}°C":["Innen Temp:", "#FC600A", font_1],
                f"{temp[1]}%":["H2O Luft:", "#347B98", font_1],
                f"{statnow}°C":["CPU Temp:", "#FB9902", font_1],
                f"{pihole[0]}":["DNS Queries:", "#9BD770", font_1],
                f"{pihole[1]}%":["Ads Blocked:", "#66B032", font_1]
                }

            draw_st7789.displaywrite(disp, infosdic)
        
        except:
            pass
        
        """Button A (Displayswitch up) - weather"""
        if button_a.is_pressed:
            draw_st7789.clearimage(disp)
            
            while True: 
                if button_a.is_pressed:
                    print("Getting Weather:", time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime()))
                    weather = apidat.getweather()

                    infosdic_a = {
                        time.strftime(f"{weather[0]} {weather[6]}"):["Stadt:", "#D85930", font_1],
                        f"{weather[1]}°C":["Außen Temp:", "#E06565", font_1],
                        f"{weather[2]}%":["H2O Luft:", "#145FA7", font_1],
                        f"{weather[3]}kmh":["Windgesch:", "#3EB8C2", font_1],
                        f"{weather[7]}":["Sonnenauf:", "#FFE946", font_1],
                        f"{weather[8]}":["Sonnenunter:", "#FFA500", font_1],
                        }

                    draw_st7789.displaywrite(disp, infosdic_a)
            
                if button_b.is_pressed:
                    draw_st7789.clearimage(disp)
                    time.sleep(0.5)
                    break
                
                time.sleep(0.5)

        """Button B (Displayswitch down) - misc"""  
        if button_b.is_pressed:
            draw_st7789.clearimage(disp)

            while True:
                if button_b.is_pressed:
                    food = fun.foodchoice()
                    
                    infosdic_b = {
                        "I <3 Batzi":["", "#ff0000", font_2],
                        f"{food}":["", "#B2BBA7", font_1],
                        }

                    draw_st7789.displaywrite(disp, infosdic_b)
                
                if button_a.is_pressed:
                    draw_st7789.clearimage(disp)
                    time.sleep(0.5)
                    break
                
                time.sleep(0.5)
        
        """
        #Button C (MX-Switch right) - Shutdown/Reboot
        if button_c.is_pressed:
            draw_st7789.clearimage(disp)
            
            while True:
                
                infosdic_c = {
                    "Shutdown hold RB":["", "#950a24", font_1],
                    f"Shutdown in {10-shutoff_presscounter}":["", "#950a24", font_1],
                    "Reboot hold LB":["", "#00b050", font_1],
                    f"Reboot in {10-reboot_presscounter}":["", "#00b050", font_1],
                    "To quit press else":["", "#fa9632", font_1],
                }
                draw_st7789.displaywrite(disp, infosdic_c)
                if button_c.is_pressed:
                    shutoff_presscounter += 1
                elif button_d.is_pressed:
                    reboot_presscounter += 1
                    
                if shutoff_presscounter == 10:
                    infosdic_c = {
                        "Shutting down!":["", "#ff0000", font_1],
                        "Good Bye :)":["", "#ff0000", font_1],
                    }
                    draw_st7789.displaywrite(disp, infosdic_c)
                    pistat.shut_down()
                    time.sleep(15)
                
                if reboot_presscounter == 10:
                    infosdic_c = {
                        "Rebooting!":["", "#ff0000", font_1],
                        "See you soon :)":["", "#ff0000", font_1],
                    }
                    draw_st7789.displaywrite(disp, infosdic_c)
                    pistat.reboot()
                    time.sleep(15)
                
                if button_a.is_pressed or button_b.is_pressed:
                    break
            
                time.sleep(0.1)
                
        #Button D (MX-Switch Left) - Timer 
        if button_d.is_pressed:
            draw_st7789.clearimage(disp)            
            
            start_time = time.time()
            last_time = start_time
            last_lap = 0
            
            while True:
                
                lap_time = time.time() - last_time
                total_time = time.time() - start_time
                
                
                infosdic_d = {
                    "Start Time":[f"{use_func.time_converter(total_time)}", "#448D76", font_1],
                    f"Lap Time":[f"{use_func.time_converter(lap_time)}", "#B2D732", font_1],
                    f"Last Lap":[f"{use_func.time_converter(last_lap)}", "#8EAF18", font_1],
                    "Exit with RB":["", "#FF0516", font_1],
                }
                draw_st7789.displaywrite(disp, infosdic_d)
                
                if button_d.is_pressed:
                    last_lap = time.time() - last_time 
                    last_time = time.time()
                    
                if button_c.is_pressed:
                    break
                
                time.sleep(0.1)
        """
    
        
        
        time.sleep(0.5)


                