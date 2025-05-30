import arcade


class CreditsView(arcade.View):
    def __init__(self, last_window):
        super().__init__()
        arcade.set_background_color(arcade.color.ALMOND)
        self.last_window = last_window

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
        # Lista de nombres y roles
        credits_lines = [
            "Diego Francisco Moreno - Jefe de Proyecto | Programador",
            "Miguel Arcas Morcillo - Programador",
            "Rubén Tostón Carrero - Diseño de Niveles | Diseño Gráfico",
            "Yulen García Sacedo - Diseño Gráfico | Programador",
            "David Martínez Sánchez - Diseño Gráfico | Creación Sprites",
            "Maxim Sazonov - Diseño de Niveles | Diseño Gráfico",
            "Mario Fernández - Programador | Diseño Gráfico",
        ]

        start_y = self.window.height - 120  # Empieza un poco debajo del título
        font_size = 24
        line_spacing = 40  # Espacio entre líneas

        for i, line in enumerate(credits_lines):
            arcade.draw_text(
                line,
                self.window.width / 2,
                start_y - i * line_spacing,
                arcade.color.ALLOY_ORANGE,
                font_size,
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
                self.window.show_view(self.last_window)
