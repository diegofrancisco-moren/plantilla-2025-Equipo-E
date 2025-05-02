"""
Battle View
"""
from contextlib import nullcontext

import arcade
import rpg.constants as constants
import random
import os

class BattleView(arcade.View):
    def __init__(self, player, enemy, game_view):
        super().__init__()
        self.started = False
        self.inventory_open = False
        self.attack_menu = False
        self.magic_attack_menu = False
        self.selected_item = 0
        self.attacks = None
        self.magic_attacks = None

        self.game_view = game_view
        self.enemy = enemy
        self.player = player
        self.items = []

        # Preparar lista de sprites
        self.sprite_list = arcade.SpriteList()

        # Crear sprites vacíos primero
        self.player_sprite = arcade.Sprite()
        self.enemy_sprite = arcade.Sprite()


        if self.player is not None and self.enemy is not None:
            for item in self.player.inventory:
                if item["usable"]:
                    self.items.append(item)

            self.attacks = player.statistics.attack_list
            self.magic_attacks = player.statistics.attack_magic_list

            # Cargar texturas
            self.player_sprite.texture = arcade.load_texture(self.player.sheet_name, x=0, y=0, width=32, height=32)
            self.enemy_sprite.texture = arcade.load_texture(self.enemy.sheet_name, x=0, y=0, width=32, height=32)

            # Posicionar los sprites
            self.player_sprite.center_x = 200
            self.player_sprite.center_y = 500

            self.enemy_sprite.center_x = 1000
            self.enemy_sprite.center_y = 500

            # Añadirlos a la lista de sprites
            self.sprite_list.append(self.player_sprite)
            self.sprite_list.append(self.enemy_sprite)

        # Ruta base a partir del archivo actual (battle_view.py)
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../resources/misc"))

        # Cargar iconos de acciones con ruta absoluta
        self.icon_attack = arcade.load_texture(os.path.join(base_path, "sword-icon.png"))
        self.icon_magic = arcade.load_texture(os.path.join(base_path, "potion-icon.png"))
        self.icon_item = arcade.load_texture(os.path.join(base_path, "backpack-icon.png"))
        self.icon_flee = arcade.load_texture(os.path.join(base_path, "footprints-icon.png"))


    def setup(self):
        pass
    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLUE)
        arcade.set_viewport(0, self.window.width, 0, self.window.height)

    def on_draw(self):
        arcade.start_render()

        # Fondo bonito
        arcade.set_background_color(arcade.color.AIR_SUPERIORITY_BLUE)

        # Área de batalla
        battle_area_y = self.window.height * 0.6
        arcade.draw_rectangle_filled(
            self.window.width / 2,
            battle_area_y,
            self.window.width,
            self.window.height * 0.8,
            arcade.color.LIGHT_GRAY
        )

        # Área de menú de acciones
        menu_area_height = 200
        arcade.draw_rectangle_filled(
            self.window.width / 2,
            menu_area_height / 2,
            self.window.width,
            menu_area_height,
            arcade.color.DARK_BLUE_GRAY
        )

        # Sombra del título de batalla
        arcade.draw_text(
            "BATALLA",
            self.window.width / 2 + 2,  # mover un poco para dar efecto de sombra
            self.window.height - 52,
            arcade.color.BLACK,
            50,  # un poco más grande para que impacte más
            anchor_x="center"
        )

        # Texto principal del título de batalla
        arcade.draw_text(
            "BATALLA",
            self.window.width / 2,
            self.window.height - 50,
            arcade.color.WHITE,
            50,
            anchor_x="center"
        )

        # Dibujar sprites (jugador a la izquierda, enemigo a la derecha)
        self.sprite_list.draw()

        # Dibujar barras de vida
        if self.player is not None and self.enemy is not None:
            self.draw_health_bar(self.player_sprite.center_x, self.player_sprite.center_y + 50,
                                 self.player.statistics.health, self.player.statistics.max_health)
            self.draw_health_bar(self.enemy_sprite.center_x, self.enemy_sprite.center_y + 50,
                                 self.enemy.statistics.health, self.enemy.statistics.max_health, is_enemy=True)

        # Dibujar los botones (acciones)
        button_texts = ["[A] ATACAR", "[M] MAGIA", "[I] OBJETOS", "[F] HUIR"]
        button_spacing = self.window.width // (len(button_texts) + 1)
        icon_textures = [self.icon_attack, self.icon_magic, self.icon_item, self.icon_flee]

        # Generamos cada boton
        for i, (text, icon) in enumerate(zip(button_texts, icon_textures)):
            x = button_spacing * (i + 1)
            y = menu_area_height / 2
            # Dibuja el botón
            arcade.draw_rectangle_filled(x, y, 250, 60, arcade.color.WHITE_SMOKE)

            # Dibuja el icono
            arcade.draw_texture_rectangle(x - 80, y, 40, 40, icon)  # 40x40 tamaño de icono ajustable

            # Dibuja el texto
            arcade.draw_text(
                text,
                x + 20,  # Un poco a la derecha para dejar hueco al icono
                y,
                arcade.color.BLACK,
                20,
                anchor_x="center",
                anchor_y="center"
            )

        # Si algún menú (inventario o ataques) está abierto
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

    def draw_health_bar(self, x, y, current_health, max_health, is_enemy=False):
        bar_width = 120
        bar_height = 15
        health_percentage = current_health / max_health

        # Color: rojo si es enemigo, verde si es jugador
        color = arcade.color.RED if is_enemy else arcade.color.GREEN

        # Fondo de la barra (gris)
        arcade.draw_rectangle_filled(x, y, bar_width, bar_height, arcade.color.DARK_SLATE_GRAY)
        # Vida actual
        arcade.draw_rectangle_filled(x - (1 - health_percentage) * (bar_width / 2), y, bar_width * health_percentage,
                                     bar_height, color)

        # Borde de la barra
        arcade.draw_rectangle_outline(x, y, bar_width, bar_height, arcade.color.BLACK, 2)

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


