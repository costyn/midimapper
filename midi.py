import pygame.midi

def initialize_midi_output():
    output_id = 2  # For Akai MidiMix
    midi_out = pygame.midi.Output(output_id)
    return midi_out

def turn_on_led(midi_out, note_number):
    midi_out.note_on(note_number, 127)  # Turn on LED

def turn_off_led(midi_out, note_number):
    midi_out.note_on(note_number, 0)  # Turn off LED

def close_midi_output(midi_out):
    midi_out.close()
    pygame.midi.quit()

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

def map_midi_to_parameters(midi_data, config):
    status_byte, note_or_cc, velocity = midi_data[0], midi_data[1], midi_data[2]
    mapped_parameters = {}

    for section in config.values():
        for parameter_name, details in section.items():
            if status_byte == 176 and details.get('cc') == note_or_cc:  # CC messages
                if details['type'] == 'range':
                    min_value = details['min']
                    max_value = details['max']
                    value_range = max_value - min_value
                    parameter_value = min_value + (velocity / 127.0) * value_range
                    mapped_parameters[parameter_name] = round(parameter_value)
                
                elif details['type'] == 'toggle':
                    # Toggle value
                    mapped_parameters[parameter_name] = 1 if details['default'] == 0 else 0
                    # Update default for future toggling
                    details['default'] = mapped_parameters[parameter_name]

                elif details['type'] == 'step':
                    # Step through the values
                    current_value = details['default']
                    values = details['values']
                    next_index = (values.index(current_value) + 1) % len(values)
                    parameter_value = values[next_index]
                    mapped_parameters[parameter_name] = parameter_value
                    # Update default for future stepping
                    details['default'] = parameter_value

            elif status_byte == 144 and details.get('cc') == note_or_cc:  # Note On messages for toggles and steps
                if details['type'] == 'toggle':
                    # Toggle value
                    mapped_parameters[parameter_name] = 1 if details['default'] == 0 else 0
                    # Update default for future toggling
                    details['default'] = mapped_parameters[parameter_name]

                elif details['type'] == 'step':
                    # Step through the values
                    current_value = details['default']
                    values = details['values']
                    next_index = (values.index(current_value) + 1) % len(values)
                    parameter_value = values[next_index]
                    mapped_parameters[parameter_name] = parameter_value
                    # Update default for future stepping
                    details['default'] = parameter_value

    return mapped_parameters