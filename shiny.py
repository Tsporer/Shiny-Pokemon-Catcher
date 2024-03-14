import cv2
import numpy as np
import pyautogui
from pynput.keyboard import Key, Controller
import time
from PIL import ImageGrab
import random
# You will have to install Python as well as some of these libraries

keyboard = Controller()

# Populate these. You can make more names lists if you want to check
# different areas
sprite_totals = []
high_names = []
low_names = []
thin_names = []

def detect_window():
    # Replace "mGBA" with your emulator.
    windows = pyautogui.getWindowsWithTitle("mGBA")
    if windows:
      game_window = windows[0]
      game_window.activate()
      time.sleep(2)

# Coordinates that we will check. Each coordinate is (x1, y1, x2, y2).
# The origin is the top left of the window. You will have to change each
# based on the location of your game window and your pokemon ROM.

# Coordinates for the name of the pokemon
name_coords = (300, 250, 350, 300)
# Coordinates for a box shaped image grab (default)
box_coords = (1050, 425, 1165, 441)
# Coordinates for a low image grab
low_coords = (1060, 450, 1100, 490)
# Coordinates for a high image grab
high_coords = (1060, 450, 1100, 490)
# Coordinates for a thin image grab
thin_coords = (1060, 450, 1100, 490)


# Obtains the mean color values for the image area
# and totals it. Checks if that total is in 
# box_sprites, high_sprites, low_sprites, or thin_sprites.
# If it is, returns False and continues the loop. If not,
# the pokemon is shiny! and returns True.
def check_shiny(pokemon_area, name_area):
  pokemon_area, name_total = check_name(pokemon_area, name_area)
  # Convert the image to numpy array
  frame = np.array(pokemon_area)
  
  # Show the name and pokemon area being checked
  cv2.imshow('Checking Name Area', np.array(name_area))
  cv2.waitKey(3000)
  cv2.destroyAllWindows()
  cv2.imshow('Checking Sprite Area', frame)
  cv2.waitKey(3000)
  cv2.destroyAllWindows()

  avg_color = np.mean(frame, axis=(0, 1))

  sprite_total = 0
  for channel in avg_color:
      sprite_total += round(channel, 2)
  sprite_total = round(sprite_total, 2)

  # Find these for each pokemon, and then populate the lists on
  # lines 14 through 17
  print(f"sprite total: {sprite_total}, name: {name_total}")

  if sprite_total in sprite_totals:
    return False
  else:
    return True

# Checks the name of the pokemon, and changes
# the pokemon checking area if needed
def check_name(pokemon_area, name_area):
  name_frame = np.array(name_area)
  name_mean = np.mean(name_frame, axis=(0, 1))
  name_total = 0
  for item in name_mean:
    name_total += round(item, 2)
  name_total = round(name_total, 2)

  if name_total in low_names:
    pokemon_area = ImageGrab.grab(bbox=low_coords)
  elif name_total in high_names:
    pokemon_area = ImageGrab.grab(bbox=high_coords)
  elif name_total in thin_names:
    pokemon_area = ImageGrab.grab(bbox=thin_coords)

  return pokemon_area, name_total


def quick_check(pokemon_area, name_area):
    pokemon_area, _ = check_name(pokemon_area, name_area)

    frame = np.array(pokemon_area)
    avg_color = np.mean(frame, axis=(0, 1))
    sprite_total = 0
    for channel in avg_color:
      sprite_total += round(channel, 2)
    sprite_total = round(sprite_total, 2)
    if sprite_total in sprite_totals:
      return 'found'
    else:
      return None


# Basic movement function that makes the player move down
# and then up. If LR flag is True, the player will move
# left and right.
def movement(LR=False):
  if LR:
    keyboard.press(Key.left)
    time.sleep(0.25 + random.uniform(0, 0.2))
    keyboard.release(Key.left)
    time.sleep(0.10 + random.uniform(0, 0.2))
    keyboard.press(Key.right)
    time.sleep(0.25 + random.uniform(0, 0.2))
    keyboard.release(Key.right)
    time.sleep(0.10 + random.uniform(0, 0.2))
  else:
    keyboard.press(Key.down)
    time.sleep(0.25 + random.uniform(0, 0.2))
    keyboard.release(Key.down)
    time.sleep(0.10 + random.uniform(0, 0.2))
    keyboard.press(Key.up)
    time.sleep(0.25 + random.uniform(0, 0.2))
    keyboard.release(Key.up)
    time.sleep(0.10 + random.uniform(0, 0.2))


# Constantly checks if there is a pokemon in view. If there is,
# it returns back to the main loop where it can check for a shiny.
# If not, it keeps making the player move around.
def move_and_check():
  start = time.time()
  while True:
    cur_check = quick_check(ImageGrab.grab(bbox=box_coords), ImageGrab.grab(bbox=name_coords))
    if cur_check == 'found':
      break
    # If you want the player to move left and right (as opposed to up and down),
    # add True to the LR flag in the movement call
    # example: movement(True)
    movement()

    end = time.time()
    # if too much time has gone on, breaks the loop
    if end - start >= 300:
      save_state()
      break


# Saves the state of the game. You will have to change this
# based on what emulator you use.
def save_state():
  keyboard.press(Key.shift)
  time.sleep(1)
  keyboard.press(Key.f7)
  time.sleep(1)
  keyboard.release(Key.shift)
  keyboard.release(Key.f7)

# Runs from pokemon. You will have to change this based on
# what emulator you use, and the pokemon ROM you are playing.
def run():
  time.sleep(0.25)
  keyboard.press('z')
  time.sleep(1.5)
  keyboard.release('z')
  keyboard.press('z')
  time.sleep(0.25)
  keyboard.release('z')
  keyboard.press(Key.down)
  time.sleep(0.25)
  keyboard.release(Key.down)
  keyboard.press(Key.right)
  time.sleep(0.25)
  keyboard.release(Key.right)
  keyboard.press('z')
  time.sleep(0.25)
  keyboard.release('z')
  time.sleep(0.25)
  keyboard.press('z')
  time.sleep(0.25)
  keyboard.release('z')
  time.sleep(0.25)


# Main loop, checks if the current pokemon is shiny, if it
# is then it saves the state of the game and breaks the loop.
# If not, it keeps searching for the shiny pokemon.
def main():
  while True: 
    pokemon_area = ImageGrab.grab(bbox=box_coords)
    name_area = ImageGrab.grab(bbox=name_coords)
    # Check if the Pokémon is shiny
    if check_shiny(pokemon_area, name_area):
      save_state()
      break
    else:
      run()
      move_and_check()
    
    # Delay before the next screen capture
    time.sleep(1 + random.uniform(0, 0.2))

if __name__ == '__main__':
  main()
