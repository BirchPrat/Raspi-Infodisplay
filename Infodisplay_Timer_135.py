"""Allrounder Infodisplay"""
#giving access to relevant paths
import sys
sys.path.insert(1, '/home/pi/Documents/Raspi-Infodisplay/Classes/')
sys.path.insert(1, '/home/pi/Documents/Raspi-Infodisplay/Functions/')
#Classes
import ModuleFetcher, SysStat, Display
#Functions
import use_func

#buttoncontrol and power
from gpiozero import Button

#import adafruit_bme280 

#other
import time
from PIL import ImageFont 

##Setting up the Display, Buttons and Temperature Reader
button_a = Button(23) #displaybutton up
button_b = Button(24) #displaybutton down
disp = Display.Display('240x135', type="mini", rotate=90, font_location = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')

#i2c = board.I2C()  # uses board.SCL and board.SDA
#bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)

##Setting up some Variables 
script_start = time.time()

##Setting up the other Class Objects
#sensorstat = ModuleFetcher.ModuleFetcher(bme280)
pistat = SysStat.SysStat()

##fonts
font_1 = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 20)

##Main Loop with all bells and whistles
if __name__ == "__main__":
    while True:
        """Main Loop, stats display"""
        uptime =  use_func.time_converter(time.time() - script_start)

        disp.display_pi_stats(pistat, uptime)

        """Button A (Displayswitch up 1. time) - 30 min timer"""
        if button_a.is_pressed:    
            disp.displayclear()
            time.sleep(0.5)

            work_start = time.time()

            while True:
                if button_b.is_pressed:
                    disp.displayclear()
                    time.sleep(0.5)
                    break
                
                work_time = time.time() - work_start 

                if work_time < 60*30:
                    display_time = use_func.time_converter(work_time)               
                    disp.display_timer(display_time[2])

                else:
                    disp.displaypic('/home/pi/Desktop/move.jpg')
                    time.sleep(10)
                    break_start = time.time()
                    
                    while True:
                        if button_b.is_pressed:
                            disp.displayclear()
                            time.sleep(0.5)
                            break

                        break_time = time.time() - break_start
                        display_time = use_func.time_converter(break_time)               
                        disp.display_timer(display_time[2])

                        if break_time > 60*5:
                            disp.displaypic('/home/pi/Desktop/end.jpg')
                            time.sleep(10)
                            work_start = time.time()
                            break

                        time.sleep(1)

                time.sleep(1)


        """Button B (Displayswitch 1. time down) - Shutdown/Reboot"""
        if button_b.is_pressed:
            disp.displayclear()
            time.sleep(0.5)
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
                    ["To quit press both 5x", "#fa9632", font_1],
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


        
              


                