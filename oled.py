import SH1106
from PIL import Image, ImageDraw, ImageFont

def init_display():
    disp = SH1106.SH1106()
    disp.Init()
    disp.clear()
    return disp

def display_text(disp, parameter_name, parameter_value):
    # Create blank image for drawing.
    image = Image.new('1', (disp.width, disp.height), "WHITE")
    draw = ImageDraw.Draw(image)
    font_small = ImageFont.truetype('Font.ttf', 13)
    font_large = ImageFont.truetype('Font.ttf', 24)

    # Clear previous content
    draw.rectangle((0, 0, disp.width-1, disp.height-1), outline=0, fill="WHITE")

    # Draw the parameter name at the top
    draw.text((2, 1), parameter_name, font=font_small, fill=0)

    # Draw the parameter value in the center
    value_width, value_height = draw.textsize(str(parameter_value), font=font_large)
    x_position = (disp.width - value_width) // 2
    y_position = (disp.height - value_height) // 2
    draw.text((x_position, y_position), str(parameter_value), font=font_large, fill=0)

    # Display the image
    disp.ShowImage(disp.getbuffer(image))