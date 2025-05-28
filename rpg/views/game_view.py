"""
Main game view
"""

import json
import math
import os
from typing import Callable

import arcade
import arcade.gui

import rpg.constants as constants
from arcade.experimental.lights import Light
from pyglet.math import Vec2


from rpg.message_box import MessageBox
from rpg.save_player_game import load_game
from rpg.sprites.player_sprite import PlayerSprite
from rpg.views.battle_view import BattleView
from rpg.entities.player import Player
from rpg.views.inventory_view import InventoryView
from rpg.views.main_menu_view import MainMenuView


class DebugMenu(arcade.gui.UIBorder, arcade.gui.UIWindowLikeMixin):
    def __init__(
        self,
        *,
        width: float,
        height: float,
        noclip_callback: Callable,
        hyper_callback: Callable,
    ):

        self.off_style = {
            "bg_color": arcade.color.BLACK,
        }

        self.on_style = {
            "bg_color": arcade.color.REDWOOD,
        }

        self.setup_noclip(noclip_callback)
        self.setup_hyper(hyper_callback)

        space = 10

        self._title = arcade.gui.UITextArea(
            text="DEBUG MENU",
            width=width - space,
            height=height - space,
            font_size=14,
            text_color=arcade.color.BLACK,
        )

        group = arcade.gui.UIPadding(
            bg_color=(255, 255, 255, 255),
            child=arcade.gui.UILayout(
                width=width,
                height=height,
                children=[
                    arcade.gui.UIAnchorWidget(
                        child=self._title,
                        anchor_x="left",
                        anchor_y="top",
                        align_x=10,
                        align_y=-10,
                    ),
                    arcade.gui.UIAnchorWidget(
                        child=arcade.gui.UIBoxLayout(
                            x=0,
                            y=0,
                            children=[
                                arcade.gui.UIPadding(
                                    child=self.noclip_button, pading=(5, 5, 5, 5)
                                ),
                                arcade.gui.UIPadding(
                                    child=self.hyper_button, padding=(5, 5, 5, 5)
                                ),
                            ],
                            vertical=False,
                        ),
                        anchor_x="left",
                        anchor_y="bottom",
                        align_x=5,
                    ),
                ],
            ),
        )

        # x and y don't seem to actually change where this is created. bug?
        # TODO: make this not appear at the complete bottom left (top left would be better?)
        super().__init__(border_width=5, child=group)

    def setup_noclip(self, callback: Callable):
        # disable player collision

        def toggle(*args):
            # toggle state on click
            self.noclip_status = True if not self.noclip_status else False
            self.noclip_button._style = (
                self.off_style if not self.noclip_status else self.on_style
            )
            self.noclip_button.clear()

            callback(status=self.noclip_status)

        self.noclip_status = False
        self.noclip_button = arcade.gui.UIFlatButton(
            text="noclip", style=self.off_style
        )
        self.noclip_button.on_click = toggle  # type: ignore

    def setup_hyper(self, callback: Callable):
        # increase player speed

        def toggle(*args):
            # toggle state on click
            self.hyper_status = True if not self.hyper_status else False
            self.hyper_button._style = (
                self.off_style if not self.hyper_status else self.on_style
            )
            self.hyper_button.clear()

            callback(status=self.hyper_status)

        self.hyper_status = False

        self.hyper_button = arcade.gui.UIFlatButton(text="hyper", style=self.off_style)
        self.hyper_button.on_click = toggle  # type: ignore


class GameView(arcade.View):
    """
    Main application class.
    """


    def __init__(self, map_list):
        super().__init__()
        self.object_list = None
        self.coin_sound = arcade.load_sound(":sounds:item-pick-up.mp3")#variable para almacenar sonido de recoger item
        self.items_collected = 0#variable para contar items recogidos
        self.time_of_day = "day"#variable para cambiar día y noche

        arcade.set_background_color(arcade.color.AMAZON)

        self.setup_debug_menu()

        self.ui_manager = arcade.gui.UIManager()
        self.ui_manager.enable()

        # Player sprite
        self.player_sprite = None
        self.player_sprite_list = None

        # Track the current state of what key is pressed
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        # Teclas pulsadas
        self.keys_held = set()

        #Inmunidad a colisiones
        self.collision_cooldown = 0.0

        # Physics engine
        self.physics_engine = None

        # Maps
        self.map_list = map_list

        # Name of map we are on
        self.cur_map_name = None

        self.message_box = None

        # Selected Items Hotbar
        self.hotbar_sprite_list = None
        self.selected_item = 1

        #Sprites Hook
        self.hook_animation_textures = [
            arcade.load_texture(":animations:" + os.path.sep + "hook" +
                                os.path.sep + f"hook_{i}.png") for i in range(9)
        ]
        self.hook_animation_index = 0
        self.hook_animating = False
        self.hook_animation_angle = 0
        self.hook_animation_pos = [0, 0]  # posición actual del gancho
        self.hook_animation_start = [0, 0]  # origen (jugador)
        self.hook_animation_end = [0, 0]  # destino (casilla hookable)
        self.hook_animation_progress = 0.0  # entre 0.0 y 1.0
        self.hook_animation_speed = 0.08  # ajustable

        f = open(".." + os.path.sep + "resources" + os.path.sep + "data" +
                 os.path.sep + "item_dictionary.json")
        self.item_dictionary = json.load(f)

        f = open(".." + os.path.sep + "resources" + os.path.sep + "data" +
                 os.path.sep + "characters_dictionary.json")
        self.enemy_dictionary = json.load(f)

        # Cameras
        self.camera_sprites = arcade.Camera(self.window.width, self.window.height)
        self.camera_gui = arcade.Camera(self.window.width, self.window.height)

        # Create a small white light
        x = 100
        y = 200
        radius = 300
        mode = "soft"
        color = arcade.csscolor.WHITE
        self.player_light = Light(x, y, radius, color, mode)

    def switch_map(self, map_name, start_x, start_y):
        """
        Switch the current map
        :param map_name: Name of map to switch to
        :param start_x: Grid x location to spawn at
        :param start_y: Grid y location to spawn at
        """
        self.cur_map_name = map_name


        try:
            self.my_map = self.map_list[self.cur_map_name]
        except KeyError:
            raise KeyError(f"Unable to find map named '{map_name}'.")

        if self.my_map.background_color:
            arcade.set_background_color(self.my_map.background_color)

        map_height = self.my_map.map_size[1]
        self.player_sprite.center_x = (
            start_x * constants.SPRITE_SIZE + constants.SPRITE_SIZE / 2
        )
        self.player_sprite.center_y = (map_height - start_y) * constants.SPRITE_SIZE - constants.SPRITE_SIZE / 2
        self.scroll_to_player(1.0)
        self.player_sprite_list = arcade.SpriteList()
        self.player_sprite_list.append(self.player_sprite)

        self.setup_physics()
        map_scene = self.map_list[self.cur_map_name].scene

        if "enemy_collisions" in map_scene.name_mapping.keys():
            for enemy in self.my_map.scene["enemy_collisions"]:
                enemy.visible = True
                enemy.defeated = False

        if self.my_map.light_layer:
            self.my_map.light_layer.resize(self.window.width, self.window.height)

    def setup_physics(self):

        if self.noclip_status:
            # make an empty spritelist so the character does not collide with anyting
            self.physics_engine = arcade.PhysicsEngineSimple(
                self.player_sprite, arcade.SpriteList()
            )
        else:
            # use the walls as normal
            self.physics_engine = arcade.PhysicsEngineSimple(
                self.player_sprite, self.my_map.scene["wall_list"]
            )



    def setup(self, load_save, file_name):
        """Set up the game variables. Call to re-start the game."""
        if load_save:
            print("Cargo el personaje anterior")
            load_game(filename = file_name, gameview = self)
        else:
            #Create the statistics of the player
            player_statistics = Player("Paco",constants.HEALTH, constants.ATTACK
                                       , constants.DEFENSE, constants.SPEED, constants.MANA,
                                       "knight")
            player_statistics.add_player_attack()
            player_statistics.add_player_magic_attack()

            self.window.views["inventory"] = InventoryView(player_statistics)
            self.window.views["inventory"].setup()

            # Create the player character
            if player_statistics.get_class_type() == "knight":
                self.player_sprite = PlayerSprite(constants.knight_sheet_name, player_statistics, scale=1.2)
            elif player_statistics.get_class_type() == "magician":
                self.player_sprite = PlayerSprite(constants.wizard_sheet_name, player_statistics, scale=1.5)
            else:
                self.player_sprite = PlayerSprite(constants.thief_sheet_name, player_statistics, scale=1.5)


            # Spawn the player
            start_x = constants.STARTING_X
            start_y = constants.STARTING_Y
            self.switch_map(constants.STARTING_MAP, start_x, start_y)
            self.cur_map_name = constants.STARTING_MAP

        # Set up the hotbar
        self.load_hotbar_sprites()



    def load_hotbar_sprites(self):
        """Load the sprites for the hotbar at the bottom of the screen.

        Loads the controls sprite tileset and selects only the number pad button sprites.
        These will be visual representations of number keypads (1️⃣, 2️⃣, 3️⃣, ..., 0️⃣)
        to clarify that the hotkey bar can be accessed through these keypresses.
        """

        first_number_pad_sprite_index = 51
        last_number_pad_sprite_index = 61

        self.hotbar_sprite_list = arcade.load_spritesheet(
            file_name=".." + os.path.sep + "resources" + os.path.sep + "tilesets" +
                      os.path.sep + "input_prompts_kenney.png",
            sprite_width=16,
            sprite_height=16,
            columns=34,
            count=816,
            margin=1,
        )[first_number_pad_sprite_index:last_number_pad_sprite_index]

    def setup_debug_menu(self):
        self.debug = False

        self.debug_menu = DebugMenu(
            width=450,
            height=200,
            noclip_callback=self.noclip,
            hyper_callback=self.hyper,
        )

        self.original_movement_speed = constants.MOVEMENT_SPEED
        self.noclip_status = False

    def enable_debug_menu(self):
        self.ui_manager.add(self.debug_menu)

    def disable_debug_menu(self):
        self.ui_manager.remove(self.debug_menu)

    def noclip(self, *args, status: bool):
        self.noclip_status = status

        self.setup_physics()

    def hyper(self, *args, status: bool):
        constants.MOVEMENT_SPEED = (
            int(self.original_movement_speed * 3.5)
            if status
            else self.original_movement_speed
        )

    def draw_inventory(self):
        capacity = 10
        vertical_hotbar_location = 40
        hotbar_height = 80
        sprite_height = 16

        field_width = self.window.width / (capacity + 1)

        x = self.window.width / 2
        y = vertical_hotbar_location

        arcade.draw_rectangle_filled(
            x, y, self.window.width, hotbar_height, arcade.color.ALMOND
        )
        for i in range(capacity):
            y = vertical_hotbar_location
            x = i * field_width + 5

            player_inventory = list(self.player_sprite.statistics.get_inventory().values())
            if len(player_inventory) > i:
                item_name = player_inventory[i]["name"]
            else:
                item_name = ""

            if i == self.selected_item - 1:
                arcade.draw_lrtb_rectangle_outline(
                    x - 6, x + field_width - 15, y + 25, y - 10, arcade.color.BLACK, 2
                )
                if item_name == "Axe":
                    self.use_axe()
            hotkey_sprite = self.hotbar_sprite_list[i]
            hotkey_sprite.draw_scaled(x + sprite_height / 2, y + sprite_height / 2, 2.0)
            # Add whitespace so the item text doesn't hide behind the number pad sprite
            text = f"{item_name}"
            arcade.draw_text(text, x, y, arcade.color.ALLOY_ORANGE, 16)


    def on_draw(self):
        """
        Render the screen.
        """
        # Borra la pantalla antes de dibujar
        arcade.start_render()

        cur_map = self.map_list[self.cur_map_name]
        map_layers = cur_map.map_layers



        # --- Capa de luces ---
        with cur_map.light_layer:


            # Cámara de sprites
            self.camera_sprites.use()

  # Grab each tile layer from the map
            map_layers = cur_map.map_layers

            # Draw scene

            for layer in cur_map.map_layers:
                self.map_list[self.cur_map_name].map_layers[layer].draw()

            for item in map_layers.get("searchable", []):
                arcade.Sprite(
                    filename=":misc:shiny-stars.png",
                    center_x=item.center_x,
                    center_y=item.center_y,
                    scale=0.8,
                ).draw()

            #for layer_name in ["bridges", "bridges2", "enemies", "characters", "walls_nonblocking"]:
            #    if layer_name in map_layers:
            #        map_layers[layer_name].draw()

            for layer in cur_map.scene.name_mapping:
                if layer not in cur_map.map_layers and layer !="wall_list":
                   cur_map.scene[layer].draw()


            # Draw the player
            self.player_sprite_list.draw()

            #Draw layers above player for deepness
            if map_layers.get("walls_nonblocking", []):
                self.map_list[self.cur_map_name].map_layers["walls_nonblocking"].draw()
            if map_layers.get("walls2_nonblocking", []):
                self.map_list[self.cur_map_name].map_layers["walls2_nonblocking"].draw()

            # Dibuja el jugador
            self.player_sprite_list.draw()

            # --- Animación del gancho ---
            if self.hook_animating:
                print("Dibujando la animación")
                texture = self.hook_animation_textures[self.hook_animation_index]

                # Vector unitario en la dirección del gancho
                dx = self.hook_animation_end[0] - self.hook_animation_start[0]
                dy = self.hook_animation_end[1] - self.hook_animation_start[1]
                length = math.hypot(dx, dy)
                angle = math.degrees(math.atan2(dy, dx))
                print("El angulo es:" + str(angle) + "\n")
                if length == 0:
                    length = 1  # evitar división por cero
                unit_x = dx / length
                unit_y = dy / length
        
                # Desplazamiento para que el pivote quede en el borde izquierdo del sprite
                offset = texture.width / 2

                draw_x = self.hook_animation_pos[0] - unit_x * offset
                draw_y = self.hook_animation_pos[1] - unit_y * offset

                # Posición ajustada para que la animación empiece en el jugador y se extienda hacia adelante
                if (angle > -30 and angle < 30) or (angle > -210 and angle < -150):
                    if self.hook_animation_start[0] > self.hook_animation_end[0]:
                        draw_x -= 40
                    else:
                        draw_x += 40
                if (angle > 60 and angle < 120) or (angle > -120 and angle < -60):
                    print("Entro en Y")
                    if self.hook_animation_start[1] > self.hook_animation_end[1]:
                        draw_y -= 40
                    else:
                        draw_y += 40
                arcade.draw_texture_rectangle(
                    draw_x,
                    draw_y,
                    texture.width,
                    texture.height,
                    texture,
                    angle=self.hook_animation_angle
                )

        # --- Dibuja la capa de luz en pantalla ---
        if cur_map.light_layer:
            if cur_map.properties and "ambient_color" in cur_map.properties:
                ambient_color = cur_map.properties["ambient_color"]
            else:
                ambient_color = arcade.color.WHITE


            cur_map.light_layer.draw(ambient_color=ambient_color)

        # --- GUI ---

        self.camera_gui.use()

        # Inventario
        self.draw_inventory()

        # Mensajes (como MessageBox)
        if self.message_box:
            self.message_box.on_draw()

        # Elementos UI
        self.ui_manager.draw()

        # Contador de ítems
        arcade.draw_text(
            f"Items: {self.items_collected}",
            10,
            self.window.height - 30,
            arcade.color.WHITE,
            18
        )



    def scroll_to_player(self, speed=constants.CAMERA_SPEED):
        """Manage Scrolling"""

        vector = Vec2(
            self.player_sprite.center_x - self.window.width / 2,
            self.player_sprite.center_y - self.window.height / 2,
        )
        self.camera_sprites.move_to(vector, speed)

    def on_show_view(self):
        # Set background color
        my_map = self.map_list[self.cur_map_name]
        if my_map.background_color:
            arcade.set_background_color(my_map.background_color)

    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        """
        if self.hook_animating:
            self.hook_animation_progress += self.hook_animation_speed
            if self.hook_animation_progress >= 1.0:
                self.hook_animation_progress = 1.0
                self.hook_animating = False

                # TELETRANSPORTAR al jugador al final del gancho
                self.player_sprite.center_x = self.hook_animation_end[0]
                self.player_sprite.center_y = self.hook_animation_end[1]

            # Calcular posición intermedia
            sx, sy = self.hook_animation_start
            ex, ey = self.hook_animation_end
            t = self.hook_animation_progress

            # Interpolación lineal de la posición actual del gancho
            self.hook_animation_pos[0] = sx + (ex - sx) * t
            self.hook_animation_pos[1] = sy + (ey - sy) * t

            # Calcular ángulo en grados para rotar la textura
            dx = ex - sx
            dy = ey - sy
            self.hook_animation_angle = math.degrees(math.atan2(dy, dx))

            # Avanzar en la animación de frames
            self.hook_animation_index += 1
            if self.hook_animation_index >= len(self.hook_animation_textures):
                self.hook_animation_index = 0

            return  # No actualizar nada más durante la animación

        # Calculate speed based on the keys pressed
        self.player_sprite.change_x = 0
        self.player_sprite.change_y = 0

        # Evaluar qué teclas están presionadas
        MOVING_UP = any(k in self.keys_held for k in constants.KEY_UP)
        MOVING_DOWN = any(k in self.keys_held for k in constants.KEY_DOWN)
        MOVING_LEFT = any(k in self.keys_held for k in constants.KEY_LEFT)
        MOVING_RIGHT = any(k in self.keys_held for k in constants.KEY_RIGHT)

        # Combinaciones diagonales
        MOVING_UP_LEFT = MOVING_UP and MOVING_LEFT
        MOVING_UP_RIGHT = MOVING_UP and MOVING_RIGHT
        MOVING_DOWN_LEFT = MOVING_DOWN and MOVING_LEFT
        MOVING_DOWN_RIGHT = MOVING_DOWN and MOVING_RIGHT

        diagonal_speed = constants.MOVEMENT_SPEED / 1.5

        if MOVING_UP:
            self.player_sprite.change_y = constants.MOVEMENT_SPEED

        if MOVING_DOWN:
            self.player_sprite.change_y = -constants.MOVEMENT_SPEED

        if MOVING_LEFT:
            self.player_sprite.change_x = -constants.MOVEMENT_SPEED

        if MOVING_RIGHT:
            self.player_sprite.change_x = constants.MOVEMENT_SPEED

        if MOVING_UP_LEFT:
            self.player_sprite.change_y = diagonal_speed
            self.player_sprite.change_x = -diagonal_speed

        if MOVING_UP_RIGHT:
            self.player_sprite.change_y = diagonal_speed
            self.player_sprite.change_x = diagonal_speed

        if MOVING_DOWN_LEFT:
            self.player_sprite.change_y = -diagonal_speed
            self.player_sprite.change_x = -diagonal_speed

        if MOVING_DOWN_RIGHT:
            self.player_sprite.change_y = -diagonal_speed
            self.player_sprite.change_x = diagonal_speed

        # Call update to move the sprite
        self.physics_engine.update()

        # Update player animation
        self.player_sprite_list.on_update(delta_time)

        self.player_light.position = self.player_sprite.position

        # Update the characters sprites
        try:
            self.map_list[self.cur_map_name].scene["characters"].on_update(delta_time)
        except KeyError:
            # no characters on map
            pass
        #Update the enemies sprites
        try:
            self.map_list[self.cur_map_name].scene["enemy_collisions"].on_update(delta_time)
        except KeyError:
            # no enemies on map
            pass


        # --- Manage doors ---
        map_layers = self.map_list[self.cur_map_name].map_layers
        map_scene = self.map_list[self.cur_map_name].scene


        # Is there as layer named 'doors'?
        if "doors" in map_layers:
            # Did we hit a door?
            doors_hit = arcade.check_for_collision_with_list(
                self.player_sprite, map_layers["doors"]
            )
            # We did!
            if len(doors_hit) > 0:
                try:
                    # Grab the info we need
                    map_name = doors_hit[0].properties["map_name"]
                    start_x = doors_hit[0].properties["start_x"]
                    start_y = doors_hit[0].properties["start_y"]



                except KeyError:
                    raise KeyError(
                        "Door objects must have 'map_name', 'start_x', and 'start_y' properties defined."
                    )

                # Swap to the new map
                self.switch_map(map_name, start_x, start_y)
            else:
                # We didn't hit a door, scroll normally
                self.scroll_to_player()
        else:
            # No doors, scroll normally
            self.scroll_to_player()

        if self.collision_cooldown > 0:
            self.collision_cooldown -= delta_time
        else:
            # Is there as layer named 'enemies'?
            if "enemy_collisions" in map_scene.name_mapping.keys():
                # Did we hit a enemy?
                enemy_hit = arcade.check_for_collision_with_list(
                    self.player_sprite, map_scene["enemy_collisions"]
                )
                alive_enemies = [e for e in enemy_hit if not getattr(e, "defeated", False)]
                # We did!
                if len(alive_enemies) > 0:
                    # Swap to the new map
                    battle_view = BattleView(player=self.player_sprite,enemy=enemy_hit[0],game_view=self)
                    self.window.show_view(battle_view)
                else:
                    # We didn't hit a character, scroll normally
                    self.scroll_to_player()
            else:
                # No character, scroll normally
                self.scroll_to_player()



    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""

        if self.message_box:
            self.message_box.on_key_press(key, modifiers)
            return

        if key in (constants.KEY_UP + constants.KEY_DOWN + constants.KEY_LEFT + constants.KEY_RIGHT):
            self.keys_held.add(key)
        elif key in constants.INVENTORY:
            inventory_view = InventoryView(self.player_sprite.statistics)
            inventory_view.setup()
            self.window.show_view(inventory_view)
        elif key == arcade.key.ESCAPE:
            pause_menu = MainMenuView(player = self.player_sprite, game_view = self)
            self.window.show_view(pause_menu)
        elif key in constants.SEARCH:
            self.search()
        elif key in constants.GANCHO:
            self.throw_claw()
        elif key == arcade.key.KEY_1:
            self.selected_item = 1
        elif key == arcade.key.KEY_2:
            self.selected_item = 2
        elif key == arcade.key.KEY_3:
            self.selected_item = 3
        elif key == arcade.key.KEY_4:
            self.selected_item = 4
        elif key == arcade.key.KEY_5:
            self.selected_item = 5
        elif key == arcade.key.KEY_6:
            self.selected_item = 6
        elif key == arcade.key.KEY_7:
            self.selected_item = 7
        elif key == arcade.key.KEY_8:
            self.selected_item = 8
        elif key == arcade.key.KEY_9:
            self.selected_item = 9
        elif key == arcade.key.KEY_0:
            self.selected_item = 10
        elif key == arcade.key.L:
            cur_map = self.map_list[self.cur_map_name]
            if self.player_light in cur_map.light_layer:
                cur_map.light_layer.remove(self.player_light)
            else:
                cur_map.light_layer.add(self.player_light)
        elif key == arcade.key.G:  # G
            # toggle debug
            self.debug = True if not self.debug else False
            if self.debug:
                self.enable_debug_menu()
            else:
                self.disable_debug_menu()

    def close_message_box(self):
        self.message_box = None

    def use_axe(self):
        print("Uso el hacha")
        map_layers = self.map_list[self.cur_map_name].map_layers
        if "axeable" not in map_layers:
            print(f"No axeable sprites on {self.cur_map_name} map layer.\n")
            return

        axeable_sprites = map_layers["axeable"]
        sprites_in_range = arcade.check_for_collision_with_list(
            self.player_sprite, axeable_sprites
        )
        for sprite in sprites_in_range:
            #arcade.play_sound(self.axe_sound)  # sonido añadido para cortar obstaculos
            sprite.remove_from_sprite_lists()

    def search(self):
        """Search for things"""

        map_layers = self.map_list[self.cur_map_name].map_layers
        if "searchable" not in map_layers:
            print(f"No searchable sprites on {self.cur_map_name} map layer.\n")
            return

        searchable_sprites = map_layers["searchable"]
        sprites_in_range = arcade.check_for_collision_with_list(
            self.player_sprite, searchable_sprites
        )
        print(f"Found {len(sprites_in_range)} searchable sprite(s) in range.\n")
        for sprite in sprites_in_range:
            if "item" in sprite.properties:
                self.message_box = MessageBox(
                    self, f"Found: {sprite.properties['item']}\n"
                )

                arcade.play_sound(self.coin_sound)#sonido añadido para buscar cosas
                self.items_collected += 1#contador de items recogidos

                sprite.remove_from_sprite_lists()
                item_key = sprite.properties["item"]
                lookup_item = self.item_dictionary[sprite.properties["item"]]
                player_inventory = self.player_sprite.statistics.get_inventory()
                if item_key in player_inventory:
                    player_inventory[item_key]["quantity"] += 1
                else:
                    # Copiar el diccionario del ítem y añadirle cantidad
                    item_copy = lookup_item.copy()
                    item_copy["quantity"] = 1
                    player_inventory[item_key] = item_copy
            else:
                print(
                    "The 'item' property was not set for the sprite. Can't get any items from this.\n"
                )

    def throw_claw(self):
        """Throw the claw """

        map_layers = self.map_list[self.cur_map_name].map_layers
        if "hookable" not in map_layers:
            print(f"No hookable sprites on {self.cur_map_name} map layer.\n")
            return
        else:
            player_sprite = self.player_sprite
            hookable_sprites = map_layers["hookable"]
            launch_zones = arcade.check_for_collision_with_list(player_sprite, hookable_sprites)
            if not launch_zones:
                print("No estás en una zona de lanzamiento.")
                return
            else:
                self.hook_animation_start = [self.player_sprite.center_x, self.player_sprite.center_y]
                self.hook_animation_progress = 0.0
                self.hook_animating = True
                self.hook_animation_index = 0

                # Buscar el sprite más cercano que NO sea el punto actual
                min_distance = float("inf")
                target_sprite = None

                for sprite in hookable_sprites:
                    if sprite not in launch_zones:
                        dist = arcade.get_distance_between_sprites(player_sprite, sprite)
                        if dist < min_distance:
                            min_distance = dist
                            target_sprite = sprite
                if target_sprite:
                    self.hook_animation_end = [target_sprite.center_x, target_sprite.center_y]
                    self.hook_animating = True
                    self.hook_animation_index = 0
                    # player_sprite.center_x, player_sprite.center_y = target_sprite.center_x, target_sprite.center_y
                    # arcade.play_sound(self.hook_sound)
                    print(f"Gancho lanzado a {target_sprite.position}")
                else:
                    print("No hay destino válido para el gancho.")

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key."""

        if key in (constants.KEY_UP + constants.KEY_DOWN + constants.KEY_LEFT + constants.KEY_RIGHT):
            self.keys_held.discard(key)

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        """Called whenever the mouse moves."""
        pass

    def on_mouse_press(self, x, y, button, key_modifiers):
        """Called when the user presses a mouse button."""
        if button == arcade.MOUSE_BUTTON_RIGHT:
            self.player_sprite.destination_point = x, y

    def on_mouse_release(self, x, y, button, key_modifiers):
        """Called when a user releases a mouse button."""
        pass

    def on_resize(self, width, height):
        """
        Resize window
        Handle the user grabbing the edge and resizing the window.
        """
        self.camera_sprites.resize(width, height)
        self.camera_gui.resize(width, height)
        cur_map = self.map_list[self.cur_map_name]
        if cur_map.light_layer:
            cur_map.light_layer.resize(width, height)

    def resume_from_battle(self, result, enemy):
        self.keys_held.clear()
        self.player_sprite.change_x = 0
        self.player_sprite.change_y = 0


        if result:
            self.player_sprite.statistics.add_xp(enemy.statistics.reward_exp)
            enemy.statistics.set_defeated(True)
            enemy.visible = False

        self.collision_cooldown = 2.0
        self.window.show_view(self.window.views["game"])

    def set_player_sprite(self, player_sprite):
        self.player_sprite = player_sprite

    def set_cur_map_name(self, cur_map_name):
        self.cur_map_name = cur_map_name

    def get_cur_map_name(self):
        return self.cur_map_name

