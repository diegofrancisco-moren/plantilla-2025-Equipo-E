import arcade
import arcade.gui

from rpg.views.characterselectview import CharacterSelectView
from rpg.views.loading_view import LoadingView
from rpg.views.saves_view import SavesView


class StartingMenuView(arcade.View):
    def __init__(self):
        super().__init__()
        self.manager = arcade.gui.UIManager()
        self.v_box = arcade.gui.UIBoxLayout()
        arcade.set_background_color(arcade.color.ALMOND)

        title = arcade.gui.UILabel(text="[NOMBRE DEL JUEGO]", width=637, font_size=44,
                                   text_color=arcade.color.ALLOY_ORANGE)
        self.v_box.add(title.with_space_around(bottom=80))

        new_game_button = arcade.gui.UIFlatButton(text="New Game", width=200)
        self.v_box.add(new_game_button.with_space_around(bottom=20))
        new_game_button.on_click = self.on_click_new_game

        load_game_button = arcade.gui.UIFlatButton(text="Load Game", width=200)
        self.v_box.add(load_game_button.with_space_around(bottom=20))
        load_game_button.on_click = self.on_click_load_game

        settings_button = arcade.gui.UIFlatButton(text="Settings", width=200)
        self.v_box.add(settings_button.with_space_around(bottom=20))
        settings_button.on_click = self.on_click_settings

        credits_button = arcade.gui.UIFlatButton(text="Credits", width=200)
        self.v_box.add(credits_button.with_space_around(bottom=20))
        credits_button.on_click = self.on_click_credits

        exit_button = arcade.gui.UIFlatButton(text="Exit", width=200)
        self.v_box.add(exit_button.with_space_around(bottom=20))
        exit_button.on_click = self.on_click_exit
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x", anchor_y="center_y", child=self.v_box
            )
        )
        self.window.views["starting_menu"] = self


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
        print("New game")
        self.manager.disable()
        next_view = CharacterSelectView()
        self.window.show_view(next_view)


    def on_click_load_game(self, event):
        print("Loads game")
        # Indicamos False, ya que no vamos a guardar una partida
        self.window.views["loading"] = LoadingView()
        self.window.views["loading"].setup()
        next_view = SavesView(save = False, player = None, gameview = None)
        self.window.show_view(next_view)


    def on_click_settings(self, event):
        print("Adjust the settings")
        self.window.show_view(self.window.views["settings"])
        'Have to find a way to fix the Esc button not working'

    def on_click_credits(self, event):
        print("Displays the credits")
        self.window.show_view(self.window.views["credits"])

    def on_click_exit(self, event):
        print("Exits the game")
        self.window.close()