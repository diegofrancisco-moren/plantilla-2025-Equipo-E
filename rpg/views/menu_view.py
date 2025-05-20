import arcade

from rpg.views import LoadingView


class MenuView(arcade.View):
    def __init__(self):
        super().__init__()
        self.started = False
        self.button_new_game = None
        self.button_load_game = None
        arcade.set_background_color(arcade.color.LIGHT_BLUE)

    def on_show_view(self):
        arcade.set_viewport(0, self.window.width, 0, self.window.height)
        self.setup()

    def setup(self):
        self.button_new_game = arcade.SpriteSolidColor(300, 60, arcade.color.DARK_GREEN)
        self.button_new_game.center_x = self.window.width // 2
        self.button_new_game.center_y = self.window.height // 2 + 50

        self.button_load_game = arcade.SpriteSolidColor(300, 60, arcade.color.DARK_BLUE)
        self.button_load_game.center_x = self.window.width // 2
        self.button_load_game.center_y = self.window.height // 2 - 50

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text(
            "Menú Principal",
            self.window.width / 2,
            self.window.height - 100,
            arcade.color.BLACK,
            44,
            anchor_x="center"
        )

        self.button_new_game.draw()
        arcade.draw_text(
            "Nueva Partida",
            self.button_new_game.center_x,
            self.button_new_game.center_y,
            arcade.color.WHITE,
            20,
            anchor_x="center",
            anchor_y="center"
        )

        self.button_load_game.draw()
        arcade.draw_text(
            "Cargar Partida",
            self.button_load_game.center_x,
            self.button_load_game.center_y,
            arcade.color.WHITE,
            20,
            anchor_x="center",
            anchor_y="center"
        )

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        if self.button_new_game.collides_with_point((x, y)):
            print("🎮 Nueva partida iniciada")
            next_view = LoadingView()
            next_view.set_load_game(False)
            next_view.setup()
            self.window.show_view(next_view)

        elif self.button_load_game.collides_with_point((x, y)):
            print("💾 Cargar partida")
            next_view = LoadingView()
            next_view.set_load_game(True)
            next_view.setup()
            self.window.show_view(next_view)
