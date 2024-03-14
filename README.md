# Shiny Pokémon Detector
This Python script automates the process of finding shiny Pokémon in Pokémon games running on an emulator. It uses image processing techniques to detect the presence of shiny Pokémon.

## Features
Automatically detects shiny Pokémon by analyzing game image grabs.
Configurable settings to adapt to different Pokémon games and emulators.
Saves the game state upon finding a shiny Pokémon.

## Prerequisites
Before running this script, you need to have:
Python installed on your machine.
The following Python libraries: cv2, numpy, pyautogui, pynput, PIL.
A game emulator (like mGBA) with a Pokémon ROM loaded.

## Installation
Clone the repository:
git clone https://github.com/Tsporer/Shiny-Pokemon-Catcher.git
Install the required Python libraries:
pip install opencv-python numpy pyautogui pynput Pillow

## Configuration
Update the emulator window name in detect_window function.
Set the correct coordinates for the game window in the script.
Populate the sprite_totals, high_names, low_names, and thin_names lists with appropriate values for your specific Pokémon game.
You will have to run the script for each Pokemon you encounter on a route to obtain these values. They are printed in the 
check_shiny function. 

## Usage
Start your Pokémon game in the emulator.
Run the script:
python shiny.py
The script will automatically interact with the game to find shiny Pokémon.

## Customization
You can customize the script by modifying the coordinate values and the lists of color totals to match your specific game and emulator setup.
