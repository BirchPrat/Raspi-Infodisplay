#drawing functions on st7789
from PIL import Image, ImageDraw, ImageFont

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



