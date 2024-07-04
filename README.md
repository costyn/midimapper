# MIDI to OLED Display with Parameter Mapping

This project demonstrates how to connect a MIDI controller to a Raspberry Pi, read MIDI input, and display mapped parameter values on a 1.3” Waveshare OLED screen. The parameters are configured via a JSON file, allowing for customizable control and display of various settings.

## Table of Contents

- Overview
- Features
- Requirements
- Setup
- Running the Script
- Configuration
- Project Structure
- Usage
- License
- Roadmap/Todo

## Overview

This project reads MIDI input from a connected MIDI controller, maps the MIDI messages to configurable parameters, and displays the parameter names and values on an OLED screen. The parameters are categorized into three sections: global, background, and foreground, and can be of type range, toggle, or step.

## Features

    •	MIDI Input Handling: Reads MIDI input from a connected MIDI controller via USB.
    •	Parameter Mapping: Maps MIDI control change (CC) and note messages to configurable parameters.
    •	OLED Display: Displays the parameter name and value on a 1.3” Waveshare OLED screen.
    •	Configurable JSON File: Allows customization of parameters, including their types, ranges, and MIDI mappings.
    •	Real-time Updates: Updates the display in real-time as MIDI messages are received.

## Requirements

    •	Raspberry Pi (with Raspbian OS installed)
    •	MIDI Controller (USB connection)
    •	1.3” Waveshare OLED Screen (SPI connection)
    •	Python 3
    •	Pygame (for MIDI)
    •	SH1106 OLED driver (bundled with this repo)
    •	Pillow (Python Imaging Library)

## Setup

### Install Dependencies:

```shell
sudo apt-get update
sudo apt-get install python3-pil python3-numpy  python3-spidev python3-smbus python3-pygame python3-websockets
```

### Enable SPI on Raspberry Pi:

```shell
sudo raspi-config
```

- Navigate to Interfacing Options -> SPI and enable it.
- Also configure WiFi and enable SSH

### Pull up GPIO pins

```shell
echo ‘gpio=6,19,5,26,13,21,20,16=pu’ >> /boot/firmware/config.txt
```

Reboot

### Clone the Repository:

```git clone https://github.com/costyn/midimapper
cd midimapper
```

### Connect the MIDI Controller and OLED Screen:

    •	Connect the MIDI controller via USB.
    •	Connect the OLED screen to the Raspberry Pi via SPI (refer to the Waveshare documentation for wiring details).

## Running the Script

- Update the JSON Configuration:
  Modify the parameters.json file to configure your parameters. Refer to the Configuration section for details.
- Run the Main Script:

```shell
python3 main.py
```

The script will start reading MIDI input and displaying the mapped parameters on the OLED screen.

## Configuration

The parameters.json file defines the parameters and their mappings to MIDI messages. The file is structured into three sections: global, background, and foreground. Each parameter can be of type range, toggle, or step.

Example parameters.json

```json
{
  "global": {
    "brightness": {
      "min": 0,
      "max": 255,
      "default": 80,
      "description": "Global brightness setting",
      "type": "range",
      "cc": 19
    },
    "bpm": {
      "min": 0,
      "max": 260,
      "default": 80,
      "description": "System Beats per Minute",
      "type": "range",
      "cc": 23
    },
    "blendTime": {
      "min": 0,
      "max": 10000,
      "default": 4000,
      "description": "Blend time, in milliseconds",
      "type": "range",
      "cc": 27
    },
    "preset": {
      "default": 0,
      "description": "Preset preconfigured with all settings",
      "type": "step",
      "values": [0, 1, 2, 3, 4, 5],
      "cc": 26
    },
    "autoAdvancePalette": {
      "min": 0,
      "max": 1,
      "default": 1,
      "description": "Auto advance palette?",
      "type": "toggle",
      "cc": 1
    },
    "autoAdvanceDelay": {
      "min": 10,
      "max": 180,
      "default": 60,
      "description": "Auto advance delay in seconds",
      "type": "range",
      "cc": 31
    },
    "fixMode": {
      "default": "NONE",
      "description": "Animation fixed mode",
      "type": "step",
      "values": ["RADAR", "RADIATE", "PAUSE", "NONE"],
      "cc": 3
    }
  },
  "background": {
    "bgPaletteIndex": {
      "min": 0,
      "max": 60,
      "default": 0,
      "description": "Background palette index",
      "type": "range",
      "cc": 16
    },
    "bgRotSpeed": {
      "min": 0,
      "max": 255,
      "default": 85,
      "description": "Background rotation speed. 128 = stop",
      "type": "range",
      "cc": 17
    },
    "bgLineWidth": {
      "min": 1,
      "max": 15,
      "default": 4,
      "description": "Background line width. Higher = thinner lines.",
      "type": "range",
      "cc": 18
    }
  },
  "foreground": {
    "fgAnimationEnable": {
      "min": 0,
      "max": 1,
      "default": 1,
      "description": "Enable foreground animation pattern",
      "type": "toggle",
      "cc": 4
    },
    "fgPaletteIndex": {
      "min": 0,
      "max": 2,
      "default": 0,
      "description": "Foreground palette; red stripe or green stripe",
      "type": "range",
      "cc": 20
    },
    "fgRotSpeed": {
      "min": 0,
      "max": 255,
      "default": 170,
      "description": "Foreground rotation speed. 128 = stop",
      "type": "range",
      "cc": 21
    },
    "fgLineWidth": {
      "min": 1,
      "max": 14,
      "default": 8,
      "description": "Foreground line width. Higher = thinner lines.",
      "type": "range",
      "cc": 22
    }
  }
}
```

## Project Structure

- config_loader.py: Contains the function to load and parse the JSON configuration.
- midi.py: Contains functions related to MIDI data formatting and mapping.
- oled.py: Contains functions related to initializing and displaying text on the OLED.
- main.py: Main script that ties everything together and handles MIDI input and display.
- parameters.json: Configuration file for defining parameters and their MIDI mappings.

## Usage

- Customize parameters.json:
- Define your parameters and their mappings in the parameters.json file.
- Each parameter can be of type range, toggle, or step.
- Run the Main Script:
- Execute the main.py script to start reading MIDI input and displaying the mapped parameters.
- Monitor Console Output:
- The console will display the raw MIDI data and the mapped parameters for debugging and monitoring purposes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

## Roadmap / Todo
* tap tempo by midi button
* set colors of knobs
