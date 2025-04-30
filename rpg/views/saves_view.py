import arcade
import arcade.gui

class SavesView(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.ALMOND)
        self.manager = arcade.gui.UIManager()
        self.v_box = arcade.gui.UIBoxLayout()
