import pygame.midi
import time
import traceback
from config_loader import load_config
from midi import format_midi_data, map_midi_to_parameters, initialize_midi_output, turn_on_led, turn_off_led, close_midi_output
from oled import init_display, display_text

def print_and_display_midi_data(device_id=3):
    pygame.midi.init()
    midi_input = pygame.midi.Input(device_id)
    midi_output = initialize_midi_output()

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
                        status_byte, note_or_cc, velocity = data[0], data[1], data[2]
                        formatted_midi_text = format_midi_data(data)
                        print("MIDI Data: ", formatted_midi_text)
                        
                        # Map MIDI data to parameters
                        mapped_parameters = map_midi_to_parameters(data, config)
                        print("\tMapped Parameters:", mapped_parameters)
                        
                        # Display the mapped parameters on the OLED
                        if mapped_parameters:
                            parameter_name, parameter_value = next(iter(mapped_parameters.items()))
                            display_text(disp, parameter_name, parameter_value)
                            
                            # Handle LEDs for toggles and steps
                            for section in config.values():
                                for param_name, details in section.items():
                                    if details['type'] == 'toggle' and details.get('cc') == note_or_cc:
                                        if parameter_value == 1:
                                            turn_on_led(midi_output, note_or_cc)
                                        else:
                                            turn_off_led(midi_output, note_or_cc)
                                    elif details['type'] == 'step' and details.get('cc') == note_or_cc:
                                        if status_byte == 144 and velocity > 0:  # Note On with velocity > 0
                                            turn_on_led(midi_output, note_or_cc)
                        # else:
                        #     if status_byte == 128 and velocity == 127:  # Note On with velocity 0
                        #         turn_off_led(midi_output, note_or_cc)
                time.sleep(0.001)  # Reduced sleep time
            except Exception as e:
                print(f"Error processing MIDI data: {e}")
                traceback.print_exc()
    except KeyboardInterrupt:
        print("\nExiting...")

    finally:
        midi_input.close()
        close_midi_output(midi_output)
        disp.RPI.module_exit()

if __name__ == "__main__":
    print_and_display_midi_data()