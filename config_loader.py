import json

def load_config(filename='parameters.json'):
    with open(filename, 'r') as file:
        return json.load(file)