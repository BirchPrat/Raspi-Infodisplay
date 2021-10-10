"Display Settup and Write Class"
import adafruit_rgb_display.st7789 as st7789
import board, digitalio, time, math
from gpiozero import OutputDevice
#drawing functions on st7789
from PIL import Image, ImageDraw, ImageFont

class Display:
    """Display Class for settup, writing and displaying pictures"""
    def __init__(self, size, type, rotate = 0, font_location = ''):
        self.size = size
        self.rotate = rotate
        self.type = type
        self.disp = self.displaysettup() # this initializes the display when object is created

        #fonts
        if font_location != '':
            self.font_1 = ImageFont.truetype(font_location, 22)
            self.font_2 = ImageFont.truetype(font_location, 30)
            self.font_clock = ImageFont.truetype(font_location, 15)
            self.font_timer = ImageFont.truetype(font_location, 80)
            self.font_pistat = ImageFont.truetype(font_location, 17)

        #setting up clock parameters
        deg_to_radians = 0.0174533

        #creating coordinates for the clock
        radius = 95 # determines how big clock is
        self.clock_x_y = []
        hours = 0
        for i in range(-60, 300, 30):
            hours += 1
            self.clock_x_y.append([math.cos(i*deg_to_radians)*radius+99, math.sin(i*deg_to_radians)*radius+110, hours])
        
        #creating coordinates for minutes
        radius_minutes = 67 #determiens how big minutes circle is
        self.minutes_x_y = []
        minutenzeiger = -1
        for i in range(-90, 330, 6):
            minutenzeiger += 1
            self.minutes_x_y.append([math.cos(i*deg_to_radians)*radius_minutes+118, math.sin(i*deg_to_radians)*radius_minutes+93, minutenzeiger])

    def displaysettup(self):
        """Setting up the st7789 Display"""
        
        if self.type == "mini":
            cs_pin = digitalio.DigitalInOut(board.CE0)
            dc_pin = digitalio.DigitalInOut(board.D25)
            backlight = digitalio.DigitalInOut(board.D22)
            reset_pin = None
            BAUDRATE = 24000000

        if self.type == "gamepad":
            cs_pin = digitalio.DigitalInOut(board.CE0)
            dc_pin = digitalio.DigitalInOut(board.D25)
            reset_pin = digitalio.DigitalInOut(board.D24)
            backlight = digitalio.DigitalInOut(board.D26)
            BAUDRATE = 24000000
      
        # Create the ST7789 display, depending on size:
        if self.size == '240x240':
            disp = st7789.ST7789(
                board.SPI(),
                cs=cs_pin,
                dc=dc_pin,
                rst=reset_pin,
                baudrate=BAUDRATE,
                height=240,
                y_offset=80,
                rotation=180
            )

        elif self.size == '240x135':
            # Create the ST7789 display:
            disp = st7789.ST7789(
                board.SPI(), 
                cs=cs_pin, 
                dc=dc_pin, 
                rst=reset_pin, 
                baudrate=BAUDRATE,
                width=135,
                height=240, 
                x_offset=53, 
                y_offset=40,
                )

        # Turn on the backlight
        backlight.switch_to_output()
        backlight.value = True

        return disp

    def displaywrite(self, infos_list, padding = 0):
        """writing text on the display"""
        #x and y starting positions
        x = 0
        y = -2
        
        height = self.disp.width   # swap height/width to rotate to landscape
        width =  self.disp.height
            
        image = Image.new('RGB', (width, height))
        draw = ImageDraw.Draw(image)

        for line in infos_list:
            draw.text((x, y), f"{line[0]}", font=line[2], fill=line[1])
            y += line[2].getsize(line[0])[1] + padding

        self.disp.image(image, self.rotate)

    def displaywrite_alt(self, infos_list, padding = 0):
        """writing text on the display"""
        #x and y starting positions
        x = 0
        y = -2
        
        height = self.disp.width   # swap height/width to rotate to landscape
        width =  self.disp.height
            
        image = Image.new('RGB', (width, height))
        draw = ImageDraw.Draw(image)

        for line in infos_list:
            draw.text((x, y), f"{line[0]}", font=line[2], fill=line[1])
            y += + padding

        self.disp.image(image, self.rotate)

    def displayclear(self):
        #Drawing the balck rectangle and displaying it
        image = Image.new('RGB', (self.disp.height, self.disp.width))
        draw = ImageDraw.Draw(image)
        draw.rectangle((0, 0, self.disp.height, self.disp.width), outline=0, fill=(0, 0, 0))
        
        self.disp.image(image, self.rotate)

    def backlight(self, status):
        # Turn on/off the backlight 
        if status == 'on':
            backlight = digitalio.DigitalInOut(board.D22)
            backlight.switch_to_output()
            backlight.value = True

        elif status == 'off':
            backlight = digitalio.DigitalInOut(board.D22)
            backlight.switch_to_output()
            backlight.value = False

    def displaypic(self, imageloc):
        image = Image.open(f"{imageloc}")
        
        # Scale the image to the smaller screen dimension
        image_ratio = image.width / image.height

        if self.size != '240x135':
            width = self.disp.width
            height = self.disp.height
        elif self.size == '240x135':
            width = self.disp.height
            height = self.disp.width
            
        screen_ratio = width / height
        if screen_ratio < image_ratio:
            scaled_width = image.width * height // image.height
            scaled_height = height
        else:
            scaled_width = width
            scaled_height = image.height * width // image.width
        image = image.resize((scaled_width, scaled_height), Image.BICUBIC)
    
        # Crop and center the image
        x = scaled_width // 2 - width // 2
        y = scaled_height // 2 - height // 2
        image = image.crop((x, y, x + width, y + height))
    
        # self.display image.
        self.disp.image(image, self.rotate)

    def display_main_simple(self, sensor_data, pistat_class, uptime):
        """Displaying temperature, pistats uptime and weather"""
        pistat = pistat_class.get_systemstats(light = 'no')

        infolist = [
            [f"{time.strftime('%b %d %H:%M:%S')}", '#00b050', self.font_1],
            [f"Innen Temp: {sensor_data[0]}°C", '#FC600A', self.font_1],
            [f"H2O Luft: {sensor_data[1]}%", "#347B98", self.font_1],
            [f" ", "#347B98", self.font_1],
            [f"{pistat[0]}", "#576675", self.font_1],
            [f"Uptime: {uptime[1]} days", '#D61A46', self.font_1],            
            [f"{pistat[1]}", "#ffc0cb", self.font_1],
            [f"{pistat[2]}", "#FC600A", self.font_1],
            [f"{pistat[3]}", "#808080", self.font_1],
            [f"{pistat[4]}", "#daa520", self.font_1],                      
            ]
        
        self.displaywrite(infolist)

    def display_pi_stats(self, pistat_class, uptime):
        """Displaying temperature, pistats uptime and weather"""
        pistat = pistat_class.get_systemstats(light = 'no')

        infolist = [
            [f"{time.strftime('%b %d %H:%M:%S')}", '#00b050', self.font_pistat],
            [f"{pistat[0]}", "#576675", self.font_pistat],
            [f"Uptime: {uptime[1]} days", '#D61A46', self.font_pistat],            
            [f"{pistat[1]}", "#ffc0cb", self.font_pistat],
            [f"{pistat[2]}", "#FC600A", self.font_pistat],
            [f"{pistat[3]}", "#808080", self.font_pistat],
            [f"{pistat[4]}", "#daa520", self.font_pistat],                      
            ]
        
        self.displaywrite(infolist)    

    def display_main_weather(self, sensor_data, pistat_class, uptime, weather):
        pistat = pistat_class.get_systemstats(light = 'no')

        """Displaying temperature, pistats uptime and weather"""
        infolist = [
            [f"{time.strftime('%b %d %H:%M:%S')}", '#00b050', self.font_1],
            [f" ", "#347B98", self.font_1],
            [f"Innen Temp: {sensor_data[0]}°", '#FC600A', self.font_1],
            [f"Außen Temp: {weather[1]}°", '#FC600A', self.font_1],
            [f"Innen H2O: {sensor_data[1]}%", "#347B98", self.font_1],
            [f"Außen H2O: {weather[2]}%", "#347B98", self.font_1],
            [f" ", "#347B98", self.font_1],
            [f"Uptime: {uptime[1]} days", '#D61A46', self.font_1],            
            [f"{pistat[1]}", "#ffc0cb", self.font_1],
            [f"{pistat[2]}", "#FC600A", self.font_1],
            ]
        
        self.displaywrite_alt(infolist, padding = 24)

    def display_weather_v1(self, temp, weather):
        '''Displaying current weather stats'''
        infolist = [
            [f"Time: {weather[6]}", "#00b050", self.font_1],
            [f"Außen Temp: {weather[1]}°C", "#FC600A", self.font_1],
            [f"Diff in Temp: {round(abs(temp[0] - weather[1]), 2)}°C", "#FC600A", self.font_1],
            [f"Außen H2O: {weather[2]}%", "#347B98", self.font_1],
            [f"Diff in H2O: {round(abs(temp[1]  - weather[2]), 2)}%", "#347B98", self.font_1],
            [f" ", "#347B98", self.font_1],
            [f"Windgesch: {weather[3]}kmh", "#6897bb", self.font_1],
            [f"Luftdruck: {weather[4]}hPa", "#3EB8C2", self.font_1],
            [f"Sonnenauf: {weather[7]}", "#FFE946", self.font_1],
            [f"Sonnenunter: {weather[8]}", "#FFA500", self.font_1],
            ]

        self.displaywrite(infolist)        

    def display_weather_v2(self, weather):
        '''Displaying current weather stats'''
        infolist = [
            [f"Time: {weather[6]}", "#00b050", self.font_1],
            [f"Außen Temp: {weather[1]}°C", "#FC600A", self.font_1],
            [f"Außen H2O: {weather[2]}%", "#347B98", self.font_1],
            [f"Range: {weather[9]}-{weather[10]}°C", "#347B98", self.font_1],
            [f" ", "#347B98", self.font_1],
            [f"Windgesch: {weather[3]}kmh", "#6897bb", self.font_1],
            [f"Luftdruck: {weather[4]}hPa", "#3EB8C2", self.font_1],
            [f"Sonnenauf: {weather[7]}", "#FFE946", self.font_1],
            [f"Sonnenunter: {weather[8]}", "#FFA500", self.font_1],
            ]

        self.displaywrite(infolist, padding = 5) 

    def display_piholedat_v1(self, pihole_dailystats, pihole_summary, time_passed, recent_blocked):
        """Displaying timer, blocked queries and last blocked"""
        infolist = [
            [f"Timer {time_passed}", "#00b050", self.font_1],
            [f" ", "#00b050", self.font_1],
            [f"Queries td: {pihole_dailystats[0]}", "#ffc0cb", self.font_1],
            [f"Blocked td: {pihole_dailystats[1]}%", "#D61A46", self.font_1],
            [f" ", "#00b050", self.font_1],                
            [f"Queries 24H: {pihole_summary['dns_queries_today']}", "#ffc0cb", self.font_1],
            [f"Blocked 24H: {pihole_summary['ads_percentage_today']}%", "#D61A46", self.font_1],
            [f" ", "#00b050", self.font_1],
            [f"Blocked Last:", "#ffc0cb", self.font_1],                                    
            [f"{recent_blocked}", "#D61A46", self.font_1],
            ]
        
        self.displaywrite(infolist)    

    def display_piholedat_tail(self, queri):
        """Displaying pihole tail"""
        infolist = [
            [f"{queri[1][0]}", "#00b050", self.font_1],
            [f"{queri[1][2]}", "#FFFF00", self.font_1],
            [f"{queri[1][3]}", "#6897bb", self.font_1],
            [f"{queri[1][-2]} {queri[1][4]}", f"{queri[1][-1]}", self.font_1],
            [f" ", "#00b050", self.font_1],                            
            [f"{queri[0][0]}", "#00b050", self.font_1],
            [f"{queri[0][2]}", "#FFFF00", self.font_1],
            [f"{queri[0][3]}", "#6897bb", self.font_1],
            [f"{queri[0][-2]} {queri[0][4]}", f"{queri[0][-1]}", self.font_1],
            ]
        
        self.displaywrite(infolist)    

    def warning_color_rgb(self, value):
        """helper function for colors (5 colors according to rain probability)"""
        if float(value) <= 0.2: 
            return  "#008000"
        elif float(value) > 0.2 and float(value) <=0.4:
            return "#2ae32a"
        elif float(value) > 0.4 and float(value) <=0.6:
            return "#FFFF00"
        elif float(value) > 0.6 and float(value) <=0.8:
            return "#ff6700"
        elif float(value) > 0.8 and float(value) <=1:
            return "#FF0000"
        else:
            return (255, 255, 255, 255)

    def display_weatherclock(self, weather, inside_temp = ''):
        """Display a weather clock"""
        try:
            #drawing the clock and hourly weather
            image = Image.new('RGB', (self.disp.height, self.disp.width))
            draw = ImageDraw.Draw(image)

            for position in self.clock_x_y:
                for weath in weather[1]:
                    if int(weath[1]) == int(position[2]):
                        colour = self.warning_color_rgb(weath[-1])
                        draw.text((position[0], position[1]), f'{str(float(weath[2]))}', font=self.font_clock, fill=colour)
                    if int(time.strftime('%I')) == int(position[2]):
                        draw.text((position[0], position[1]+12), '---------', font=self.font_clock, fill='#ffffff')
            
            #drawing minutes
            for position in self.minutes_x_y:
                    if int(time.strftime('%M')) == position[-1]:
                        draw.text((position[0], position[1]), '.', font=self.font_2, fill='#ffffff')
                    if int(time.strftime('%S')) == position[-1]:
                        draw.text((position[0], position[1]), '.', font=self.font_2, fill='#999999')
                    
            #getting the middle of the circle
            middle_x = (self.clock_x_y[2][0] + self.clock_x_y[8][0]) / 2
            middle_y = (self.clock_x_y[2][1] + self.clock_x_y[8][1]) / 2

            #drawing current weather in the middle of the clock
            if inside_temp == '':
                draw.text((middle_x-15, middle_y-15), f'{weather[0][0]}', font=self.font_clock, fill='#00b050')
                middle_y += self.font_clock.getsize(str(weather[0][0]))[1]
                draw.text((middle_x-15, middle_y-15), f'{weather[0][1]}°C', font=self.font_clock, fill='#FC600A')
                middle_y += self.font_clock.getsize(str(weather[0][0]))[1]
                draw.text((middle_x-15, middle_y-15), f'{weather[0][2]}%', font=self.font_clock, fill='#347B98')

            else:
                draw.text((middle_x-24, middle_y-16), f'{weather[0][0]}', font=self.font_clock, fill='#00b050')
                middle_y += self.font_clock.getsize(str(weather[0][0]))[1]
                draw.text((middle_x-24, middle_y-16), f'{weather[0][1]}|{inside_temp[0]}°', font=self.font_clock, fill='#FC600A')
                middle_y += self.font_clock.getsize(str(weather[0][0]))[1]
                draw.text((middle_x-24, middle_y-16), f'{weather[0][2]}|{inside_temp[1]}%', font=self.font_clock, fill='#347B98')          

            self.disp.image(image, self.rotate)
        
        except:        
            infolist = [
                [f"Failed", "#00b050", self.font_1],
                [f"Probably no internet", "#00b050", self.font_1],  
            ]

            self.displaywrite(infolist, padding=8)
        
    def display_weather_week(self, weather):
        """Displaying weather data for next week"""
        try:
            infolist = []
            colours = []
            for i, daylist in enumerate(weather[2]):
                colour = self.warning_color_rgb(weather[2][i][-1])
                colours.append(colour)
                infolist.append([f"{weather[2][i][1]}: {weather[2][i][2]['min']}-{weather[2][i][2]['max']}°C", colours[i], self.font_1])

            self.displaywrite(infolist, padding=8)
        
        except:        
            infolist = [
                [f"Failed", "#00b050", self.font_1],
                [f"Probably no internet", "#00b050", self.font_1],  
            ]

            self.displaywrite(infolist, padding=8)

    def display_timer(self, timer):
        """Displaying timer"""
        infolist = [
            [f"", "#00b050", self.font_1],
            [f"{timer}", "#00b050", self.font_timer],
            ]
        
        self.displaywrite_alt(infolist, padding = 20) 
   

class CamInterface(Display):
    """Camera-Interface for 240x240 gamepad Screen"""
    def __init__(self, size, type, rotate = 0, font_location = ''):
        super().__init__(size, type, rotate, font_location) 

    def first_layer(self, x_axis_list):
        """
        Displaying first layer interface with four options 
        x_axis are buttons showing where the selection currently is
        selection is displayed via colour
        """
        
        infolist = [
            [f"Preview", f'#00b050' if x_axis_list[0] else f'#2ae32a', self.font_1],
            [f"Timelaps Photo", f'#00b050' if x_axis_list[1] else f'#2ae32a', self.font_1],
            [f"Stil Photo", f'#00b050' if x_axis_list[2] else f'#2ae32a', self.font_1],
            [f"Video", f'#00b050' if x_axis_list[3] else f'#2ae32a', self.font_1],
            ]
        
        self.displaywrite(infolist)   



