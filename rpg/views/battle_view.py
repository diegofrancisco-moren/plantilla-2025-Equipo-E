"""
Battle View
"""
from contextlib import nullcontext

import arcade
import rpg.constants as constants
import random

class BattleView(arcade.View):
    def __init__(self, player, enemy, game_view):
        super().__init__()
        self.started = False
        self.inventory_open = False  # Variable para controlar si el inventario de items esta abierto
        self.attack_menu = False # Variable para controlar si el menu de ataques esta abierto
        self.magic_attack_menu = False # Variable para controlar si el menu de ataques magicos esta abierto
        self.selected_item = 0  # Índice del ítem seleccionado

        self.game_view = game_view
        self.enemy = enemy
        self.player = player
        self.items = []


        if not(self.player == None):
            for item in self.player.inventory:
                if item["usable"]:
                    self.items.append(item)
                    print(item["name"])

            self.attacks = player.statistics.attack_list
            self.magic_attacks = player.statistics.attack_magic_list

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
                if self.inventory_open:
                    self.inventory_open = False
                    print(f"Usaste {items[self.selected_item]}")
                    self.use_item(selected_item = items[self.selected_item])
                else:
                    print(f"Usaste {items[self.selected_item]}")
                    self.attack(player_selected_attack = items[self.selected_item])
                      # Cerrar inventario después de usar un ítem
                    self.magic_attack_menu = False
                    self.attack_menu = False
            elif symbol == arcade.key.B:
                self.inventory_open = False
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
                item["name"], 320, start_y - i * 35, color, 24, anchor_x="left"
            )

            arcade.draw_lrtb_rectangle_outline(
                290, 990, start_y - i * 35 + 24, start_y - i * 35 - 10, arcade.color.WHITE, 1
            )

    def use_item(self,selected_item):
        enemy_selected_attack = random.choice(self.enemy.statistics.attack_list)
        enemy_damage = (self.enemy.statistics.attack * enemy_selected_attack["atk_mod"] + enemy_selected_attack["power"]) - self.player.statistics.defense
        self.player.statistics.health_up(selected_item["heal_amount"])
        self.player.statistics.health_down(enemy_damage)

    def attack(self, player_selected_attack):
        """
        Calculo del ataque del jugador
        Los ataques tienen dos partes, un daño varaible y un daño base.
        El daño base viene definido por el ataque usado, en el campo "power"
        El daño varible se obtiene con el siguente calculo:
        player_attack * atk_mod
        Siendo "player_attack" la estadística de ataque del jugador.
        Y "atk_mod" el campo modificador de ataque que tienen todos los ataques.
        Por ultimo se resta al ataque la defensa del objetivo
        Los ataques enemigos se calcularán de la misma forma
        """
        player_damage = (self.player.statistics.attack * player_selected_attack["atk_mod"] + player_selected_attack["base_power"]) - self.enemy.statistics.defense

        """Calculo del ataque del enemigo
        El ataque que utilice el enemigo (si tiene más de un ataque) se hará de forma
        aleatoria. Utilizando random, se tomará un ataque de la lista del enemigo.
        """
        enemy_selected_attack = random.choice(self.enemy.statistics.attack_list)
        enemy_damage = (self.enemy.statistics.attack * enemy_selected_attack["atk_mod"] + enemy_selected_attack["base_power"]) - self.player.statistics.defense
        if self.player.statistics.speed >= self.enemy.statistics.speed:
            #Ataque del jugador
            self.enemy.statistics.health_down(player_damage)
            print(self.player.statistics.name + " utilizo " + player_selected_attack["name"])
            print(self.player.statistics.name + " ha inflingido " +
                  str(player_damage) + " de daño al enemigo")
            if not (self.enemy.statistics.alive()):
                # Si después del ataque el enemigo esta muerto, terminamos la batalla
                self.game_view.resume_from_battle(True, self.enemy)
                return
            #Ataque del enemigo
            self.player.statistics.health_down(enemy_damage)
            print("El enemigo utilizo " + enemy_selected_attack["name"])
            print("El enemigo ha inflingido " +
                  str(enemy_damage) + " de daño a " + self.player.statistics.name)
            if not (self.player.statistics.alive()):
                # Si después del ataque el jugador esta muerto, terminamos la batalla
                self.game_view.resume_from_battle(False, self.enemy)
                return
        else:
            #Ataque del enemigo
            self.player.statistics.health_down(enemy_damage)
            print(self.player.statistics.name + " utilizo " + player_selected_attack["name"])
            print(self.player.statistics.name + " ha inflingido " +
                  str(player_damage) + " de daño al enemigo")
            if not (self.enemy.statistics.alive()):
                # Si después del ataque el jugador esta muerto, terminamos la batalla
                self.game_view.resume_from_battle(True, self.enemy)
                return
            #Ataque del jugador
            self.enemy.statistics.health_down(player_damage)
            print("El enemigo utilizo " + enemy_selected_attack["name"])
            print("El enemigo ha inflingido " +
                  str(enemy_damage) + " de daño a " + self.player.statistics.name)
            if not (self.player.statistics.alive()):
                # Si después del ataque el enemigo esta muerto, terminamos la batalla
                self.game_view.resume_from_battle(False, self.enemy)
                return
