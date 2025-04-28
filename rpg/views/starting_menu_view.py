import arcade
import arcade.gui
from rpg.views.loading_view import LoadingView
from rpg.views.settings_view import SettingsView


class StartingMenuView(arcade.View):
    def __init__(self):
        super().__init__()
        self.manager = arcade.gui.UIManager()
        self.v_box = arcade.gui.UIBoxLayout()

        title = arcade.gui.UILabel(text="[NOMBRE ORIGINAL]", width=270, font_size=20, text_color=arcade.color.MAGENTA)
        self.v_box.add(title.with_space_around(bottom=20))

        new_game_button = arcade.gui.UIFlatButton(text="New Game", width=200)
        self.v_box.add(new_game_button.with_space_around(bottom=20))
        new_game_button.on_click = self.on_click_new_game

        load_game_button = arcade.gui.UIFlatButton(text="Load Game", width=200)
        self.v_box.add(load_game_button.with_space_around(bottom=20))
        load_game_button.on_click = self.on_click_load_game

        settings_button = arcade.gui.UIFlatButton(text="Settings", width=200)
        self.v_box.add(settings_button.with_space_around(bottom=20))
        settings_button.on_click = self.on_click_settings

        exit_button = arcade.gui.UIFlatButton(text="Exit", width=200)
        self.v_box.add(exit_button.with_space_around(bottom=20))
        exit_button.on_click = self.on_click_exit
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

    def on_click_new_game(self, event):
        print("Loads game")
        self.manager.disable()
        load_game = LoadingView()
        load_game.setup()
        self.window.show_view(load_game)

    def on_click_load_game(self, event):
        print("Loads game")
        self.manager.disable()
        load_game = LoadingView()
        load_game.setup()
        self.window.show_view(load_game)


    def on_click_settings(self, event):
        print("Adjust the settings")
        settings_menu = SettingsView()
        settings_menu.setup()
        self.window.show_view(settings_menu)
        'Have to find a way to fix the Esc button not working'

    def on_click_exit(self, event):
        print("Exits the game")
        self.window.close()