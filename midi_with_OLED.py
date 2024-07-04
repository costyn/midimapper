import pygame.midi
import SH1106
import time
import config
import traceback
from PIL import Image, ImageDraw, ImageFont

# Function to initialize the OLED display
def init_display():
    disp = SH1106.SH1106()
    disp.Init()
    disp.clear()
    return disp

# Function to display text on the OLED
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

# Function to parse and format MIDI data
def format_midi_data(data):
    status_byte = data[0]
    note = data[1]
    velocity = data[2]

    if status_byte == 144 and velocity > 0:  # Note On with non-zero velocity
        message = f"Note On: {note}, Vel: {velocity}"
    elif status_byte == 144 and velocity == 0:  # Note On with velocity zero (interpreted as Note Off)
        message = f"Note Off: {note}"
    elif status_byte == 176:  # Control Change
        message = f"CC: {note}, Value: {velocity}"
    else:
        message = f"Status: {status_byte}, Data1: {note}, Data2: {velocity}"

    return message

# Function to print and display MIDI data
def print_and_display_midi_data(device_id=3):
    pygame.midi.init()
    midi_input = pygame.midi.Input(device_id)

    disp = init_display()
    print("Listening for MIDI input from device 3... (Press Ctrl+C to quit)")

    try:
        while True:
            try:
                if midi_input.poll():
                    midi_events = midi_input.read(10)
                    for event in midi_events:
                        data = event[0]
                        midi_text = format_midi_data(data)
                        print("MIDI Data: ", midi_text)
                        display_text(disp, midi_text)
                time.sleep(0.01)
            except Exception as e:
                print(f"Error processing MIDI data: {e}")
                traceback.print_exc()
    except KeyboardInterrupt:
        print("\nExiting...")

    finally:
        midi_input.close()
        pygame.midi.quit()
        disp.RPI.module_exit()

if __name__ == "__main__":
    print_and_display_midi_data()