#drawing on st7789 test
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789
import board
import digitalio

def displaysettup():
    """Configuration for CS and DC pins (these are FeatherWing defaults on M0/M4)"""
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
    return disp

disp = displaysettup()


def clearimage(disp, landscape='no'):
    if landscape == 'no':
        height = disp.width   # swap height/width to rotate to landscape
        width = disp.height
    else:
        height = disp.height   # swap height/width to rotate to landscape
        width = disp.width
        
    rotation = 90
    image = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(image)

    #Drawing the balck rectangle and displaying it
    draw.rectangle((0, 0, disp.width, disp.height), outline=0, fill=(0, 0, 0))
    disp.image(image, rotation)
    
clearimage(disp)

def displaywrite(disp, infos_dic, landscape='no'):
    #x and y starting positions
    x = 0
    y = -2
    
    if landscape == 'no':
        height = disp.width   # swap height/width to rotate to landscape
        width = disp.height
    else:
        height = disp.height   # swap height/width to rotate to landscape
        width = disp.width
        
    rotation = 90
    image = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(image)

    for info,text in infos_dic.items():
        draw.text((x, y), f"{text[0]} {info}", font=text[2], fill=text[1])
        y += text[2].getsize(info)[1]


    disp.image(image, rotation)

font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 22)
font2 = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 40)

infosdic = {
    "Info 1":["Info 1 text", "#D85930", font],
    "Info 2":["Info 2 text", "#E06565", font2] ,
    "Info 3":["Info 3 text", "#145FA7", font],
    }

displaywrite(disp, infosdic)

