#GPIO Settup
from gpiozero import OutputDevice


def tempreader_on(gpio_pin=21):
    """Supplying the temeperature reader with GPIO pin power"""
    power = OutputDevice(gpio_pin)
    power.on()
