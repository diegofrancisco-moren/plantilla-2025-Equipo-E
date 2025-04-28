import arcade
import arcade.gui
from rpg.views.loading_view import LoadingView
from rpg.views.game_view import GameView

class StartingMenuView(arcade.View):
    def __init__(self):
        super().__init__()
        self.progress = 0
        self.manager = arcade.gui.UIManager()
        self.v_box = arcade.gui.UIBoxLayout()

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

    def on_click_load_game(self, event):
        print("Loads game")
        LoadingView.on_draw(self)
        LoadingView.setup(self)


    def on_click_settings(self, event):
        print("Adjust the settings")
        self.window.show_view(self.window.view["settings"])

    def on_click_exit(self, event):
        print("Exits the game")
        self.window.close()