import arcade

from rpg import constants
from rpg.views.loading_view import LoadingView

# --- Constantes de ventana ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "seleccion de personaje"

# --- Datos de personajes ---
CHARACTERS = [
    {
        "name": "Caballero ",
        "class": "Guerrero",
        "desc": "Antiguo defensor del reino, condenado a luchar eternamente.",
        "stats": {"Salud": 170, "Ataque": 15, "Defensa": 15, "Velocidad": 4, "Mana":100},
        "weapon": "Espadón ",
        "sprite_path": f"{constants.knight_battle_sprite}",

    },
    {
        "name": "Mago",
        "class": "Hechicero",
        "desc": "Controla las llamas oscuras de los condenados.",
        "stats": {"Salud": 120, "Ataque": 20, "Defensa": 5, "Velocidad": 6, "Mana":300},
        "weapon": "Bastón ",
        "sprite_path": f"{constants.magician_battle_sprite}",
    },
    {
        "name": "Ladron",
        "class": "Picaro",
        "desc": "Acecha entre ruinas y sombras con sigilo mortal.",
        "stats": {"Salud": 90, "Ataque": 25, "Defensa": 8, "Velocidad": 10, "Mana":100},
        "weapon": "Dagas ",
        "sprite_path": f"{constants.thief_battle_sprite}",

    }
]


class CharacterSelectView(arcade.View):
    def __init__(self):
        super().__init__()
        self.selected_index = 0
        self.title_font_size = 36
        self.option_font_size = 18
        self.margin_top = SCREEN_HEIGHT - 80
        self.bg_color = arcade.color.BLACK
        self.character_images = []
        for char in CHARACTERS:
            texture = arcade.load_texture(char['sprite_path'])
            self.character_images.append(texture)

    def on_draw(self):
        arcade.start_render()
        arcade.set_background_color(self.bg_color)

        # Título
        arcade.draw_text(" SELECCIÓN DE PERSONAJE ", SCREEN_WIDTH / 2, self.margin_top,
                         arcade.color.LIGHT_GRAY, self.title_font_size, anchor_x="center")

        # Instrucciones
        arcade.draw_text("↑ ↓ para navegar, Enter para seleccionar",
                         SCREEN_WIDTH / 2, 40, arcade.color.GRAY, 14, anchor_x="center")



        # Mostrar personajes
        y = self.margin_top - 100
        for i, char in enumerate(CHARACTERS):
            color = arcade.color.GOLD if i == self.selected_index else arcade.color.LIGHT_GRAY
            arcade.draw_text(f"{char['name']} ({char['class']})", 100, y, color, self.option_font_size)

            if i == self.selected_index:
                # Dibujar imagen del personaje seleccionado en esquina superior izquierda
                selected_texture = self.character_images[self.selected_index]
                arcade.draw_texture_rectangle(1100, SCREEN_HEIGHT - 100, 300, 300, selected_texture)
                # Descripción y stats
                arcade.draw_text(f"{char['desc']}", 120, y - 10, arcade.color.GRAY, 14, width=600)
                stats = ", ".join([f"{k}: {v}" for k, v in char['stats'].items()])
                arcade.draw_text(f"🛡  Estadísticas: {stats}", 120, y - 30, arcade.color.GRAY, 14)
                arcade.draw_text(f"⚔  Arma: {char['weapon']}", 120, y - 50, arcade.color.GRAY, 14)
               # arcade.draw_text(f"✨ Habilidad: {char['skill']}", 120, y - 90, arcade.color.GRAY, 14)

            y -= 150

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP:
            self.selected_index = (self.selected_index - 1) % len(CHARACTERS)
        elif key == arcade.key.DOWN:
            self.selected_index = (self.selected_index + 1) % len(CHARACTERS)
        elif key in (arcade.key.ENTER, arcade.key.RETURN):
            selected = CHARACTERS[self.selected_index]
            print(f"\n🧙 Has elegido: {selected['name']} ({selected['class']})\n")
            self.window.views["loading"] = LoadingView()
            self.window.views["loading"].set_load_game(load_save=False, file_name=None, selected_class=selected['name'])
            self.window.views["loading"].setup()
            self.window.show_view(self.window.views["loading"])


