#Display Test
import time
from Display import Display
from PIL import Image, ImageDraw, ImageFont

disp = Display('240x240')
disp.settup()



font_1 = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 22)

#disp.displaysettup("240x240")

while True:
    writer = [
        [f"woot", "#00b050", font_1],
        [f"test", "#00b050", font_1],
    ]


    disp.displaywrite(writer, rotation = 180)

    time.sleep(5)