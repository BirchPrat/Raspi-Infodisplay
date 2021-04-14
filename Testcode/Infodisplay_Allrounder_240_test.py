"""Allrounder Infodisplay"""
#giving access to relevant paths
import sys
sys.path.insert(1, '/home/pi/Documents/')
sys.path.insert(1, '/home/pi/Documents/Raspi-Infodisplay/Classes/')
sys.path.insert(1, '/home/pi/Documents/Raspi-Infodisplay/Functions/')
#Classes
import ApiFetcher, FunStuff, SysStat
#Functions
import draw_st7789, gpio_settup, use_func, vistemp 
#api credentials
import cred
#buttoncontrol and power
from gpiozero import Button
from gpiozero import OutputDevice

#other
import time
from PIL import Image, ImageDraw, ImageFont 

##Setting up the Display, Buttons and Temperature Reader
button_a = Button(23) #displaybutton up
button_b = Button(24) #displaybutton down

disp = gpio_settup.displaysettup()
draw_st7789.clearimage(disp)

#Setting up the Class Objects
weather_api = ApiFetcher.WeatherApi(cred.weather_key)
pihole_api = ApiFetcher.PiholeApi(cred.pihole_key, cred.pihole_ip)
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

##Main Loop with all bells and whistles
if __name__ == "__main__":
    while True:
        """Main Loop, Sys-Stats on Display"""
        timeinhours = time.strftime('%H')
        timeinseconds =  int(time.strftime('%S'))
        date = time.strftime('%d')
        shutoff_presscounter = 0
        reboot_presscounter = 0
        pihole = pihole_api.get_dailystats()
        statnow = pistat.get_systemstats(light = 'no')

        if timeinhours == '00': #display sleeping for 6 hours from 0-6 am
            gpio_settup.displaysettup(init = 'no', backlight = 'off')
            draw_st7789.clearimage(disp)
            time.sleep(sleepy)
            gpio_settup.displaysettup(init = 'no', backlight = 'on')
            
        if timeinseconds in refreshratelist_tempreader:
            temp = [1, 2]
        try:
            infosdic = {
                time.strftime('%b %d %H:%M:%S'):["", "#D61A46", font_1],
                f"{temp[0]}°C":[" Innen Temp:", "#FC600A", font_1],
                f"{temp[1]}%":[" H2O Luft:", "#347B98", font_1],
                f"{statnow[0]}":["", "#FFFFFF", font_1],
                f"{statnow[1]}":["", "#FFFF00", font_1],
                f"{statnow[2]}":["", "#00FF00", font_1],
                f"{statnow[3]}":["", "#0000FF", font_1],
                f"{statnow[4]}":["", "#FF00FF", font_1],
                }

            draw_st7789.displaywrite(disp, infosdic, rotation=180)
        
        except:
            pass
        
        """Button A (Displayswitch up) - weather"""
        if button_a.is_pressed:
            draw_st7789.clearimage(disp)


            print("Getting Weather:", time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime()))
            weather = weather_api.get_weather()
            
            infosdic_a = {
                time.strftime(f"{weather[0]} {weather[6]}"):["Stadt:", "#D85930", font_1],
                f"{weather[1]}°C":["Außen Temp:", "#E06565", font_1],
                f"{weather[2]}%":["H2O Luft:", "#145FA7", font_1],
                f"{weather[3]}kmh":["Windgesch:", "#3EB8C2", font_1],
                f"{weather[7]}":["Sonnenauf:", "#FFE946", font_1],
                f"{weather[8]}":["Sonnenunter:", "#FFA500", font_1],
                }

            draw_st7789.displaywrite(disp, infosdic_a, rotation = 180)
            
            vistemp.vistemp('/home/pi/Documents/Templog', 'templogger.csv')               
            
            presscounter_a = 0
            
            while True:
                
                if button_a.is_pressed:    
                    presscounter_a += 1
                    
                if button_b.is_pressed:
                    draw_st7789.clearimage(disp)
                    time.sleep(0.5)
                    break
                

                if presscounter_a == 1:
                    draw_st7789.displaypic(disp, '/home/pi/Documents/Templog/hourly_temp.png')
                elif presscounter_a == 2:
                    draw_st7789.displaypic(disp, '/home/pi/Documents/Templog/daily_temp.png')
                elif presscounter_a == 3:
                    draw_st7789.displaypic(disp, '/home/pi/Documents/Templog/weekly_temp.png')
                    
                time.sleep(0.5)

        """Button B (Displayswitch down) - misc"""  
        if button_b.is_pressed:
            draw_st7789.clearimage(disp)
            
            start_time = time.time()

            while True:
                statnow = pistat.get_systemstats(light = 'no')
                uptime = pistat.get_uptime()
                total_time = time.time() - start_time

                infosdic_b = {
                    f"{use_func.time_converter(total_time)}":[" Start Time", "#00b050", font_1],
                    f"{statnow[0]}":["", "#FFFFFF", font_1],
                    f"{statnow[1]}":["", "#FFFF00", font_1],
                    f"{statnow[2]}":["", "#00FF00", font_1],
                    f"{statnow[3]}":["", "#0000FF", font_1],
                    f"{statnow[4]}":["", "#FF00FF", font_1],
                    }

                draw_st7789.displaywrite(disp, infosdic_b, rotation = 180)                
                          
                if button_a.is_pressed:
                    draw_st7789.clearimage(disp)
                    time.sleep(0.5)
                    break
                
                """Button B (Displayswitch down again) - Shutdown/Reboot"""
                if button_b.is_pressed:
                    
                    while True:
                        infosdic_c = {
                            "Shutdown hold UP":["", "#950a24", font_1],
                            f"Shutdown in {10-shutoff_presscounter}":["", "#950a24", font_1],
                            "Reboot hold LB":["", "#00b050", font_1],
                            f"Reboot in {10-reboot_presscounter}":["", "#00b050", font_1],
                            "To quit press UP & LB 5x":["", "#fa9632", font_1],
                        }
                        draw_st7789.displaywrite(disp, infosdic_c, rotation = 180)
                        if button_a.is_pressed:
                            shutoff_presscounter += 1
                        elif button_b.is_pressed:
                            reboot_presscounter += 1
                            
                        if shutoff_presscounter == 10:
                            infosdic_c = {
                                "Shutting down!":["", "#ff0000", font_1],
                                "Good Bye :)":["", "#ff0000", font_1],
                            }
                            draw_st7789.displaywrite(disp, infosdic_c, rotation = 180)
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
                        
                        if reboot_presscounter == 5 & shutoff_presscounter == 5:
                            break
                    
                        time.sleep(0.1)                        
                
                
                time.sleep(0.5)
        
              
        time.sleep(0.5)


                