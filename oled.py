import SH1106
from PIL import Image, ImageDraw, ImageFont

def init_display():
    disp = SH1106.SH1106()
    disp.Init()
    disp.clear()
    return disp

def display_text(disp, text):
    # Create blank image for drawing.
    image = Image.new('1', (disp.width, disp.height), "WHITE")
    draw = ImageDraw.Draw(image)
    font10 = ImageFont.truetype('Font.ttf', 13)

    # Draw a rectangle and text
    draw.line([(0, 0), (127, 0)], fill=0)
    draw.line([(0, 0), (0, 63)], fill=0)
    draw.line([(0, 63), (127, 63)], fill=0)
    draw.line([(127, 0), (127, 63)], fill=0)
    draw.text((2, 1), text, font=font10, fill=0)

    # Display the image
    disp.ShowImage(disp.getbuffer(image))