import arcade
import arcade.gui

class SavesView(arcade.View):
    def __init__(self):
        super().__init__()
        self.manager = arcade.gui.UIManager()
        self.v_box = arcade.gui.UIBoxLayout()
        arcade.set_background_color(arcade.color.ALMOND)

        title = arcade.gui.UILabel(text="Load a Save File", width=450, font_size=44,
                                   text_color=arcade.color.ALLOY_ORANGE)
        self.v_box.add(title.with_space_around(bottom=80))

        save_file1_button = arcade.gui.UIFlatButton(text="Save 1", width=200)
        self.v_box.add(save_file1_button.with_space_around(bottom=20))
        save_file1_button.on_click = self.on_click_save_file1

        save_file2_button = arcade.gui.UIFlatButton(text="Save 2", width=200)
        self.v_box.add(save_file2_button.with_space_around(bottom=20))
        save_file2_button.on_click = self.on_click_save_file2

        save_file3_button = arcade.gui.UIFlatButton(text="Save 3", width=200)
        self.v_box.add(save_file3_button.with_space_around(bottom=20))
        save_file3_button.on_click = self.on_click_save_file3

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x", anchor_y="center_y", child=self.v_box
            )
        )

    def on_show_view(self):
        self.manager.enable()
        arcade.set_background_color(arcade.color.ALMOND)

    def on_hide_view(self):
        self.manager.disable()

    def setup(self):
        pass

    def on_draw(self):
        self.clear()
        self.manager.draw()

    def on_click_save_file1(self, event):
        print("Loads the save file 1")

    def on_click_save_file2(self, event):
        print("Loads the save file 2")

    def on_click_save_file3(self, event):
        print("Loads the save file 3")

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.ESCAPE:
            print("Still trying to find a way to fix the ESC button into the menu")