"Display Settup and Write Class"
import adafruit_rgb_display.st7789 as st7789
import board, digitalio
from gpiozero import OutputDevice
#drawing functions on st7789
from PIL import Image, ImageDraw, ImageFont

class Display:
    """Display Class for settup, writing and displaying pictures"""
    def __init__(self, size, rotate = 0):
        self.size = size
        self.disp = self.displaysettup()
        self.rotate = rotate

    def settup(self):
        self.disp

    def displaysettup(self):
        """Setting up the st7789 Display"""
        cs_pin = digitalio.DigitalInOut(board.CE0)
        dc_pin = digitalio.DigitalInOut(board.D25)
        reset_pin = None

        # Config for display baudrate (default max is 24mhz):
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
                y_offset=40)

        # Turn on the backlight
        backlight = digitalio.DigitalInOut(board.D22)
        backlight.switch_to_output()
        backlight.value = True

        return disp


    def displaywrite(self, infos_list):
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
            y += line[2].getsize(line[0])[1]    

        self.disp.image(image, self.rotate)

    def displayclear(self):
        #Drawing the balck rectangle and displaying it
        image = Image.new('RGB', (self.disp.width, self.disp.height))
        draw = ImageDraw.Draw(image)

        draw.rectangle((0, 0, self.disp.width, self.disp.height), outline=0, fill=(0, 0, 0))
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
        screen_ratio = self.disp.width / self.disp.height
        if screen_ratio < image_ratio:
            scaled_width = image.width * self.disp.height // image.height
            scaled_height = self.disp.height
        else:
            scaled_width = self.disp.width
            scaled_height = image.height * self.disp.width // image.width
        image = image.resize((scaled_width, scaled_height), Image.BICUBIC)
        
        # Crop and center the image
        x = scaled_width // 2 - self.disp.width // 2
        y = scaled_height // 2 - self.disp.height // 2
        image = image.crop((x, y, x + self.disp.width, y + self.disp.height))
        
        # self.display image.
        self.disp.image(image, self.rotate)






