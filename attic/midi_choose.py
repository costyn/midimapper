import pygame.midi

def list_midi_devices():
    pygame.midi.init()
    for i in range(pygame.midi.get_count()):
        r = pygame.midi.get_device_info(i)
        (interf, name, input, output, opened) = r
        in_out = ""
        if input:
            in_out = "(input)"
        if output:
            in_out = "(output)"
        print(f"{i}: interface: {interf}, name: {name}, opened: {opened} {in_out}")
    pygame.midi.quit()

def print_midi_data(device_id):
    pygame.midi.init()
    midi_input = pygame.midi.Input(device_id)

    print("Listening for MIDI input... (Press Ctrl+C to quit)")

    try:
        while True:
            if midi_input.poll():
                midi_events = midi_input.read(10)
                for event in midi_events:
                    data = event[0]
                    print("MIDI Data: ", data)
    except KeyboardInterrupt:
        print("\nExiting...")

    finally:
        midi_input.close()
        pygame.midi.quit()

if __name__ == "__main__":
    list_midi_devices()
    device_id = int(input("Select MIDI input device ID: "))
    print_midi_data(device_id)