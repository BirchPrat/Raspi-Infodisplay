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
    
def displaywrite(disp, infos_dic, landscape='no', rotation = 90):
    #x and y starting positions
    x = 0
    y = -2
    
    if landscape == 'no':
        height = disp.width   # swap height/width to rotate to landscape
        width = disp.height
    else:
        height = disp.height   # swap height/width to rotate to landscape
        width = disp.width
        
    image = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(image)

    for info,text in infos_dic.items():
        draw.text((x, y), f"{text[0]} {info}", font=text[2], fill=text[1])
        y += text[2].getsize(info)[1]


    disp.image(image, rotation)

def displaypic(disp, imageloc):
    image = Image.open(f"{imageloc}")
    
    # Scale the image to the smaller screen dimension
    image_ratio = image.width / image.height
    screen_ratio = disp.width / disp.height
    if screen_ratio < image_ratio:
        scaled_width = image.width * disp.height // image.height
        scaled_height = disp.height
    else:
        scaled_width = disp.width
        scaled_height = image.height * disp.width // image.width
    image = image.resize((scaled_width, scaled_height), Image.BICUBIC)
    
    # Crop and center the image
    x = scaled_width // 2 - disp.width // 2
    y = scaled_height // 2 - disp.height // 2
    image = image.crop((x, y, x + disp.width, y + disp.height))
    
    # Display image.
    disp.image(image)



    
    
    
    
    
    
    
    
    
    


