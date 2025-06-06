
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
MOVEMENT_SPEED = 5

#Player Sprites Scale
SCALE = 1.3

# Sprite of the player
knight_sheet_name = ":characters:Player" + os.path.sep + "knight_sprite.png"
knight_battle_sprite = ":characters:Player" + os.path.sep + "knight_big.png"
knight_health = 200
knight_attack = 40
knight_defense = 10
knight_speed = 10
knight_mana = 20

magician_sheet_name = ":characters:Player" + os.path.sep + "magician_sprite.png"
magician_battle_sprite = ":characters:Player" + os.path.sep + "magician_big.png"
magician_health = 200
magician_attack = 40
magician_defense = 10
magician_speed = 10
magician_mana = 20

thief_sheet_name = ":characters:Player" + os.path.sep + "thief_sprite.png"
thief_battle_sprite = ":characters:Player" + os.path.sep + "thief_big.png"
thief_health = 200
thief_attack = 40
thief_defense = 10
thief_speed = 10
thief_mana = 20

# Statistics of the player
HEALTH = 200
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
GANCHO = [arcade.key.Q]
PLAYERINFO = [arcade.key.P]

# Key attack view
KEY_ATTACK = [arcade.key.A]
KEY_MAGIC_ATTACK = [arcade.key.M]
KEY_FELL = [arcade.key.F]

# Message box
MESSAGE_BOX_FONT_SIZE = 38
MESSAGE_BOX_MARGIN = 30

# How fast does the camera pan to the user
CAMERA_SPEED = 0.2
