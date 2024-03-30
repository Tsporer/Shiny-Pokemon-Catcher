# Automatic shiny detector for pokemon ROMs
###########################################
################# STEP 1 ##################
## Install all necessary libraries used  ##
###########################################
import numpy as np
from pynput.keyboard import Key, Controller
from PIL import ImageGrab
import time
import random
import subprocess
import pyautogui
import cv2

keyboard = Controller()

###########################################
################# STEP 2 ##################
## If using Windows, comment out the     ##
## detect_window function and function   ##
## call. If using MacOS, keep this as is ##
###########################################
def activate_window(window_title="mGBA"):
    script = f'''
    tell application "System Events"
        tell application "{window_title}" to activate
    end tell
    '''
    subprocess.run(["osascript", "-e", script])
activate_window()

# def detect_window():
#     windows = pyautogui.getWindowsWithTitle("mGBA")
#     if windows:
#         game_window = windows[0]
#         game_window.activate()
#         time.sleep(2)
# detect_window()


###########################################
################# STEP 3 ##################
## Adjust these coordinates based on     ##
## where the pokemon appears. The top    ##
## left of the screen is the origin.     ##
## These coordinates should be big       ##
## enough to capture the entire pokemon. ##
## Adjust the menu_area coordinates to   ##
## something that will let the program   ##
## know a pokemon appeared in the first  ##
## place. Here, these coordinates        ##
## capture the bottom of the screen, and ##
## is used to detect the color change    ##
## when a pokemon is encountered.        ##
###########################################
x1, y1, x2, y2 = 659, 223, 1032, 533
menu_area = (600, 783, 900, 840)

###########################################
################# STEP 5 ##################
## Populate this dictionary with the     ##
## proper values. This values will be    ##
## printed from the check_shiny function ##
## (print(total)). Make sure to add      ##
## every pokemon from that route. Some   ##
## intial values are here just to show   ##
## how the dictionary is formed.         ##
## The script must be run when a pokemon ##
## is encountered.                       ##
###########################################
poke_color = {
        'azurill': 311.47,
        'minccino': 351.27,
        'riolu': 286.93
    }


###########################################
################# STEP 6 ##################
## If you want to print information from ##
## running the script, uncomment lines   ##
## 86-90, 131-134. You will have to      ##
## populate poke_encounters, similar to  ##
## populating poke_color                 ##
###########################################
# poke_encounters = {
#         'azurill': 0,
#         'minccino': 0,
#         'riolu': 0
#     }

def get_key_from_value(d, target_value):
    for key, value in d.items():
        if value == target_value:
            return key
    return None

def increment_encounter(d, key):
    d[key] += 1
    return d

def print_info(d):
    total = sum(d.values())
    for key, val in d.items():
        print(f"{key} encounters: {val}, chance: {round((val * 1.0 / total) * 100)}%")
    print(f"total: {total}")

def display_area(frame):
    cv2.imshow('Display area', frame)
    cv2.waitKey(3000)
    cv2.destroyAllWindows()

def check_shiny(pokemon_area):
    frame = np.array(pokemon_area)
    x = np.mean(frame, axis=(0, 1))

    # Comment this out if you don't want 
    # to display the area (usually when 
    # you've made sure that the pokemon_area
    # coordinates successfully capture the 
    # pokemon)
    display_area(frame)

    total = 0
    for item in x:
        total += round(item, 2)
    total = round(total, 2)
    print(total)

    if total in poke_color.values():
        # global poke_encounters
        # poke_key = get_key_from_value(poke_color, total)
        # poke_encounters = increment_encounter(poke_encounters, poke_key)
        # print_info(poke_encounters)
        return False
    else:
        return True


def quick_check():
    menu = ImageGrab.grab(bbox=menu_area)
    frame = np.array(menu)

    # Comment this out if you don't want 
    # to display the menu area
    display_area(frame)

    x = np.mean(frame, axis=(0, 1))
    total = 0
    for item in x:
        total += round(item, 2)
    total = round(total, 2)
    ###########################################
    ################# STEP 4 ##################
    ## Run the script and see what value     ##
    ## 'total' is when a pokemon is          ##
    ## encountered. Replace 592.0 with this  ##
    ## value.                                ##
    ###########################################
    print(total)
    if total == 592.0:
        return True

def movement(LR=False):
    if LR:
        keyboard.press(Key.left)
        time.sleep(0.10 + random.uniform(0, 0.1))
        keyboard.release(Key.left)
        time.sleep(0.10 + random.uniform(0, 0.1))
        keyboard.press(Key.right)
        time.sleep(0.10 + random.uniform(0, 0.1))
        keyboard.release(Key.right)
        time.sleep(0.10 + random.uniform(0, 0.1))
    else:
        keyboard.press(Key.down)
        time.sleep(0.10 + random.uniform(0, 0.1))
        keyboard.release(Key.down)
        time.sleep(0.10 + random.uniform(0, 0.1))
        keyboard.press(Key.up)
        time.sleep(0.10 + random.uniform(0, 0.1))
        keyboard.release(Key.up)
        time.sleep(0.10 + random.uniform(0, 0.1))

def keyboard_presses():
    while True:
        # If you want to encounter pokemon
        # by running left/right, set this
        # False to True
        movement(False)
        if quick_check() == True:
            break

def run():
    time.sleep(0.75)
    keyboard.press('z')
    time.sleep(1)
    keyboard.release('z')
    time.sleep(0.25)
    keyboard.press(Key.down)
    time.sleep(0.25)
    keyboard.release(Key.down)
    time.sleep(0.25)
    keyboard.press(Key.right)
    time.sleep(0.25)
    keyboard.release(Key.right)
    time.sleep(0.25)
    keyboard.press('z')
    time.sleep(0.25)
    keyboard.release('z')
    time.sleep(0.25)
    keyboard.press('z')
    time.sleep(0.25)
    keyboard.release('z')
    time.sleep(0.25)

def save_state():
    time.sleep(1)
    keyboard.press(Key.shift)
    time.sleep(1)
    keyboard.press(Key.f2)
    time.sleep(1)
    keyboard.release(Key.shift)
    keyboard.release(Key.f2)

def main_loop():
    while True:
        pokemon_area = ImageGrab.grab(bbox=(x1, y1, x2, y2))
        if check_shiny(pokemon_area):
            save_state()
            break
        else:
            run()
            keyboard_presses()
            time.sleep(0.5 + random.uniform(0, 0.1))

main_loop()
