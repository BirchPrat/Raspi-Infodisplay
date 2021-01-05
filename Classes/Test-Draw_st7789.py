#Test-Draw_st7789
import digitalio
import board
import adafruit_rgb_display.st7789 as st7789
import Draw_st7789
 

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


displ = Draw_st7789(disp)


displ.clearimage()
