import arcade

class CreditsView(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.ALMOND)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text(
            "Credits",
            self.window.width / 2,
            self.window.height - 50,
            arcade.color.ALLOY_ORANGE,
            44,
            anchor_x="center",
            anchor_y="center",
            align="center",
            width=self.window.width,
        )

    def setup(self):
        pass

    def on_show_view(self):
        arcade.set_background_color(arcade.color.ALMOND)
        arcade.set_viewport(0, self.window.width, 0, self.window.height)

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.ESCAPE:
                print("show game view")
                self.window.show_view(self.window.views["starting_menu"])