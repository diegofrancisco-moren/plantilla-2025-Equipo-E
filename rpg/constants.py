
import json
import os

import arcade

#Json archives
f = open(".." + os.path.sep + "resources" + os.path.sep + "data"
         + os.path.sep + "attacks_list.json")
attack_dictionary = json.load(f)

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Python Community RPG"
TILE_SCALING = 1.0
SPRITE_SIZE = 32

# How fast does the player move
MOVEMENT_SPEED = 6

# Sprite of the player
player_sheet_name = ":characters:Male" + os.path.sep + "Male 02-2.png"

# Statistics of the player
HEALTH = 100
ATTACK = 40
DEFENSE = 10
SPEED = 10
MANA = 20


# How many pixels to keep as a minimum margin between the character
# and the edge of the screen.
LEFT_VIEWPORT_MARGIN = 300
RIGHT_VIEWPORT_MARGIN = 300
BOTTOM_VIEWPORT_MARGIN = 300
TOP_VIEWPORT_MARGIN = 300

# What map, and what position we start at
STARTING_MAP = "main_map"
STARTING_X = 33
STARTING_Y = 16

# Key mappings
KEY_UP = [arcade.key.UP, arcade.key.W]
KEY_DOWN = [arcade.key.DOWN, arcade.key.S]
KEY_LEFT = [arcade.key.LEFT, arcade.key.A]
KEY_RIGHT = [arcade.key.RIGHT, arcade.key.D]
INVENTORY = [arcade.key.I]
SEARCH = [arcade.key.E]

# Key attack view
KEY_ATTACK = [arcade.key.A]
KEY_MAGIC_ATTACK = [arcade.key.M]
KEY_FELL = [arcade.key.F]

# Message box
MESSAGE_BOX_FONT_SIZE = 38
MESSAGE_BOX_MARGIN = 30

# How fast does the camera pan to the user
CAMERA_SPEED = 0.1
