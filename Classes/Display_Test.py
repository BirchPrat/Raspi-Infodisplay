#Display Test
import time
from Display import Display
from PIL import Image, ImageDraw, ImageFont

disp = Display('240x240', type = "gamepad", rotate = 180)
#disp.settup()

font_1 = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 22)

while True:
    writer = [
        [f"woot", "#00b050", font_1],
        [f"test", "#00b050", font_1],
    ]

    disp.displaywrite(writer)
    
    time.sleep(2)

    disp.displayclear()

    time.sleep(1)

    disp.displaypic('/home/pi/Desktop/image.jpg')
    #disp.displaypic('/media/SAVE/hourly_temp.png')

    time.sleep(5)

    disp.backlight('off')
    time.sleep(1)
    disp.backlight('on')