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

    for parameter_name, details in config.items():
        if details['type'] == 'cc' and status_byte == 176 and details['cc'] == note_or_cc:
            # Handle CC messages
            min_value = details['min']
            max_value = details['max']
            value_range = max_value - min_value
            parameter_value = min_value + (velocity / 127.0) * value_range
            mapped_parameters[parameter_name] = round(parameter_value)
        
        elif details['type'] == 'note' and status_byte == 144 and details['note'] == note_or_cc:
            # Handle Note On messages for push buttons (toggle)
            current_value = details['default']
            new_value = 1 if current_value == 0 else 0
            mapped_parameters[parameter_name] = new_value

    return mapped_parameters