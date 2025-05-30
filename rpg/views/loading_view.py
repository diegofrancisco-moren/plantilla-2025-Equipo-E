"""
Loading screen
"""
import arcade
from rpg.draw_bar import draw_bar
from rpg.load_game_map import load_maps
from rpg.views.battle_view import BattleView
from rpg.views.game_view import GameView
from rpg.views.main_menu_view import MainMenuView
from rpg.views.settings_view import SettingsView


class LoadingView(arcade.View):
    def __init__(self):
        super().__init__()
        self.started = False
        self.progress = 0
        self.map_list = None
        self.load_save = False
        self.file_name = None
        self.selected_class = None
        arcade.set_background_color(arcade.color.ALMOND)


    def on_draw(self):
        arcade.start_render()
        arcade.draw_text(
            "Loading...",
            self.window.width / 2,
            self.window.height / 2,
            arcade.color.ALLOY_ORANGE,
            44,
            anchor_x="center",
            anchor_y="center",
            align="center",
            width=self.window.width,
        )
        self.started = True
        draw_bar(
            current_amount=self.progress,
            max_amount=100,
            center_x=self.window.width / 2,
            center_y=20,
            width=self.window.width,
            height=10,
            color_a=arcade.color.BLACK,
            color_b=arcade.color.WHITE,
        )

    def setup(self):
        pass

    def on_update(self, delta_time: float):
        # Dictionary to hold all our maps
        if self.started:
            done, self.progress, self.map_list = load_maps()
            if done:
                self.window.views["game"] = GameView(self.map_list)
                self.window.views["game"].setup(self.load_save, self.file_name, self.selected_class)
                self.window.views["main_menu"] = MainMenuView(None, None)
                self.window.views["settings"] = SettingsView(None)
                self.window.views["settings"].setup()
                self.window.views["battle"] = BattleView(None,None,None)
                self.window.views["battle"].setup()


                self.window.show_view(self.window.views["game"])

    def set_load_game(self, load_save, file_name, selected_class):
        self.load_save = load_save
        self.file_name = file_name
        self.selected_class = selected_class