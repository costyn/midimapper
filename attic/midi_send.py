import pygame.midi
import time

def initialize_midi_output():
    pygame.midi.init()
    midi_out = pygame.midi.Output(2)
    return midi_out

def turn_on_led(midi_out, note_number):
    midi_out.note_on(note_number, 127)  # Turn on LED

def turn_off_led(midi_out, note_number):
    midi_out.note_on(note_number, 0)  # Turn off LED

def close_midi_output(midi_out):
    midi_out.close()
    pygame.midi.quit()

if __name__ == "__main__":
    midi_out = initialize_midi_output()

    try:
        # Example: Turn on LED for button note 36
        turn_on_led(midi_out, 6)
        time.sleep(1) 
        # Example: Turn off LED for button note 36
        turn_off_led(midi_out, 6)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        close_midi_output(midi_out)