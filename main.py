import pygame.midi
import time
import traceback
from config_loader import load_config
from midi import format_midi_data, map_midi_to_parameters
from oled import init_display, display_text

def print_and_display_midi_data(device_id=3):
    pygame.midi.init()
    midi_input = pygame.midi.Input(device_id)

    disp = init_display()
    config = load_config()  # Load the JSON configuration

    print("Listening for MIDI input from device 3... (Press Ctrl+C to quit)")

    try:
        while True:
            try:
                if midi_input.poll():
                    midi_events = midi_input.read(10)
                    for event in midi_events:
                        data = event[0]
                        formatted_midi_text = format_midi_data(data)
                        print("MIDI Data: ", formatted_midi_text)
                        
                        # Map MIDI data to parameters
                        mapped_parameters = map_midi_to_parameters(data, config)
                        
                        # Display the mapped parameters on the OLED
                        if mapped_parameters:
                            print("\tMapped Parameters:", mapped_parameters)
                            parameter_name, parameter_value = next(iter(mapped_parameters.items()))
                            display_text(disp, parameter_name, parameter_value)
                time.sleep(0.001)  # Reduced sleep time
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