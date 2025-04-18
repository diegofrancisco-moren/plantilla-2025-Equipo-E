"""
Battle View
"""
from contextlib import nullcontext

import arcade
import rpg.constants as constants

class BattleView(arcade.View):
    def __init__(self, player, enemy, game_view):
        super().__init__()
        self.started = False
        self.inventory_open = False  # Variable para controlar si el inventario de items esta abierto
        self.attack_menu = False # Variable para controlar si el menu de ataques esta abierto
        self.magic_attack_menu = False # Variable para controlar si el menu de ataques magicos esta abierto
        self.selected_item = 0  # Índice del ítem seleccionado

        self.items = ["Poción", "Éter", "Antídoto", "Elixir"]  # Ejemplo de ítems
        self.attacks = ["Estocada", "Puñalada"]
        self.magic_attacks = ["Bola de fuego", "Rayo"]

        self.game_view = game_view
        self.enemy = enemy
        self.player = player
        if not(self.player == None):
            self.player_sprite = arcade.Sprite()
            self.player_sprite.texture = arcade.load_texture(self.player.sheet_name, x=0, y=0, width=32, height=32)

            self.enemy_sprite = arcade.Sprite()
            self.enemy_sprite.texture = self.enemy.texture
            self.enemy_sprite.texture = arcade.load_texture(self.enemy.sheet_name, x=0, y=0, width=32, height=32)

            # Posicionar los sprites en la pantalla
            self.player_sprite.center_x = 200  # Posición en X
            self.player_sprite.center_y = 500  # Posición en Y

            self.enemy_sprite.center_x = 1000  # Posición en X del enemigo
            self.enemy_sprite.center_y = 500  # Posición en Y del enemigo

            # Agregar los sprites a la lista de sprites para ser renderizados
            self.sprite_list = arcade.SpriteList()
            self.sprite_list.append(self.player_sprite)
            self.sprite_list.append(self.enemy_sprite)



        arcade.set_background_color(arcade.color.BLUE)

    def setup(self):
        pass
    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLUE)
        arcade.set_viewport(0, self.window.width, 0, self.window.height)

    def on_draw(self):#makes text apear on screen. The blue background will not draw w/o this
        arcade.start_render()
        arcade.draw_text(
            "BATTLE(WIP)",
            self.window.width / 2,
            self.window.height - 50,
            arcade.color.WHITE,
            44,
            anchor_x="center",
            anchor_y="center",
            align="center",
            width=self.window.width,
        )
        arcade.draw_text(
            "[-----------------------------------------------------------------------------------------------------------------------------]",
            self.window.width / 2,
            self.window.height - 500,
            arcade.color.WHITE,
            22,
            anchor_x="center",
            anchor_y="center",
            align="center",
            width=self.window.width,
        )
        arcade.draw_text(
            "ATTACK [A]                                  ITEMS [I]",
            self.window.width / 2,
            self.window.height - 550,
            arcade.color.WHITE,
            44,
            anchor_x="center",
            anchor_y="center",
            align="center",
            width=self.window.width,
        )
        arcade.draw_text(
            "MAGIC [M]                                  FLEE [F]",
            self.window.width / 2,
            self.window.height - 650,
            arcade.color.WHITE,
            44,
            anchor_x="center",
            anchor_y="center",
            align="center",
            width=self.window.width,
        )
        self.sprite_list.draw()
        if self.inventory_open:
            self.draw_inventory(self.items)
        elif self.attack_menu:
            self.draw_inventory(self.attacks)
        elif self.magic_attack_menu:
            self.draw_inventory(self.magic_attacks)

    def on_key_press(self, symbol: int, modifiers: int):
        # Si se presiona la tecla escape se abre el menu de pausa
        if symbol == arcade.key.ESCAPE:
            self.window.show_view(self.window.views["main_menu"])
        elif not(self.inventory_open or self.magic_attack_menu or self.magic_attack_menu):
            # Si se presiona la tecla "A" se abre el menu de ataques
            if symbol in constants.KEY_ATTACK:
                self.attack_menu = True
            #Si se presiona la tecla "M" se abre el menu de ataques magicos
            elif symbol in constants.KEY_MAGIC_ATTACK:
                self.magic_attack_menu = True
            #Si se presiona la tecla "I" se abre el inventario de items
            elif symbol in constants.INVENTORY:
                self.inventory_open = True
            #Si se presiona la tecla "F" se huye de la pelea
            elif symbol in constants.KEY_FELL:
                self.game_view.resume_from_battle(False, self.enemy)

            # Movimiento inventario de items
        if self.inventory_open or self.magic_attack_menu or self.attack_menu:
            if self.inventory_open:
                items = self.items
            elif self.magic_attack_menu:
                items = self.magic_attacks
            else:
                items = self.attacks
            if symbol in constants.KEY_UP:
                self.selected_item = (self.selected_item - 1) % len(items)
            elif symbol in constants.KEY_DOWN:
                self.selected_item = (self.selected_item + 1) % len(items)
            elif symbol == arcade.key.ENTER:
                print(f"Usaste {items[self.selected_item]}")
                self.inventory_open = False  # Cerrar inventario después de usar un ítem
                self.magic_attack_menu = False
                self.attack_menu = False

    def draw_inventory(self, items):
        inventory_width = 700
        inventory_height = 415
        x, y = self.window.width / 2, 425

        arcade.draw_rectangle_filled(x, y, inventory_width, inventory_height, arcade.color.BLACK)

        start_y = 610
        for i, item in enumerate(items):
            color = arcade.color.YELLOW if i == self.selected_item else arcade.color.WHITE
            arcade.draw_text(
                item, 320, start_y - i * 35, color, 24, anchor_x="left"
            )

            arcade.draw_lrtb_rectangle_outline(
                290, 990, start_y - i * 35 + 24, start_y - i * 35 - 10, arcade.color.WHITE, 1
            )


