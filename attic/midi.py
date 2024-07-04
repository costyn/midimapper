import pygame.midi

def print_midi_data(device_id=3):
    pygame.midi.init()
    midi_input = pygame.midi.Input(device_id)

    print("Listening for MIDI input from device 3... (Press Ctrl+C to quit)")

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
    print_midi_data()