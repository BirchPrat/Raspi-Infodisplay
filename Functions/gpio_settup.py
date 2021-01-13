#GPIO Settup
import adafruit_rgb_display.st7789 as st7789
import board, digitalio
from gpiozero import OutputDevice

def displaysettup(init = 'yes', backlight = 'nothing'):
    """Setting up the st7789 Display"""
    if init == 'yes':
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

        # Turn on the backlight
        backlight = digitalio.DigitalInOut(board.D22)
        backlight.switch_to_output()
        backlight.value = True

        return disp
    
    if backlight == 'on':
        # Turn on the backlight 
        backlight = digitalio.DigitalInOut(board.D22)
        backlight.switch_to_output()
        backlight.value = True
        
    if backlight == 'off':
        # Turn off the backlight
        backlight = digitalio.DigitalInOut(board.D22)
        backlight.switch_to_output()
        backlight.value = False


def tempreader_on(gpio_pin=21):
    """Supplying the temeperature reader with GPIO pin power"""
    power = OutputDevice(gpio_pin)
    power.on()