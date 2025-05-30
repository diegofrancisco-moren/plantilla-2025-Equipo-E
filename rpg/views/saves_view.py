import arcade
import arcade.gui
import os
from rpg.save_player_game import save_game


SAVE_FOLDER = ".." + os.path.sep + "resources" + os.path.sep + "saves" + os.path.sep
MAX_SAVES = 3  # Número máximo de archivos de guardado

class SavesView(arcade.View):
    def __init__(self, save, player, gameview):
        super().__init__()
        self.manager = arcade.gui.UIManager()
        self.v_box = arcade.gui.UIBoxLayout()
        arcade.set_background_color(arcade.color.ALMOND)

        self.save = save
        self.player = player
        self.gameview = gameview
        title = arcade.gui.UILabel(text="Load a Save File", width=450, font_size=44,
                                   text_color=arcade.color.ALLOY_ORANGE)
        self.v_box.add(title.with_space_around(bottom=80))

        # Lista para guardar botones y sus callbacks
        self.save_buttons = []
        for i in range(1, MAX_SAVES + 1):
            button = arcade.gui.UIFlatButton(text=f"Archivo libre", width=240)
            button.on_click = getattr(self, f"on_click_save_file{i}")
            self.v_box.add(button.with_space_around(bottom=20))
            self.save_buttons.append(button)

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x", anchor_y="center_y", child=self.v_box
            )
        )

        # Actualizar nombres de botones
        self.update_save_buttons()

    def update_save_buttons(self):
        # Asegurarse de que el directorio exista
        if not os.path.exists(SAVE_FOLDER):
            os.makedirs(SAVE_FOLDER)

        archivos = os.listdir(SAVE_FOLDER)
        json_files = [f for f in archivos if f.endswith(".json")]
        json_files.sort()  # Ordena alfabéticamente para consistencia

        for i in range(MAX_SAVES):
            if i < len(json_files):
                nombre_archivo = json_files[i]
                self.save_buttons[i].text = nombre_archivo
            else:
                self.save_buttons[i].text = "Archivo libre"

    def on_show_view(self):
        self.manager.enable()
        arcade.set_background_color(arcade.color.ALMOND)

    def on_hide_view(self):
        self.manager.disable()

    def on_draw(self):
        self.clear()
        self.manager.draw()

    def on_click_save_file1(self, event):
        if self.save :
            print("Save the file 1")
            save_game(self.player, self.gameview, self.save_buttons[0].text)
            self.window.show_view(self.window.views["main_menu"])
        else:
            if self.save_buttons[0].text == "Archivo libre":
                pass
            else:
                print("Loads the save file 1")
                self.window.views["loading"].set_load_game(True, self.save_buttons[0].text, None)
                self.window.show_view(self.window.views["loading"])

    def on_click_save_file2(self, event):
        if self.save:
            print("Save the file 2")
            save_game(self.player, self.gameview, self.save_buttons[1].text)
            self.window.show_view(self.window.views["main_menu"])
        else:
            if self.save_buttons[1].text == "Archivo libre":
                pass
            else:
                print("Loads the save file 2")
                self.window.views["loading"].set_load_game(True, self.save_buttons[1].text, None)
                self.window.show_view(self.window.views["loading"])

    def on_click_save_file3(self, event):
        if self.save:
            print("Save the file 3")
            save_game(self.player, self.gameview, self.save_buttons[2].text)
            self.window.show_view(self.window.views["loading"])
        else:
            if self.save_buttons[2].text == "Archivo libre":
                pass
            else:
                print("Loads the save file 3")
                self.window.views["loading"].set_load_game(True, self.save_buttons[2].text, None)
                self.window.views["loading"].setup()

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.ESCAPE:
            print("show game view")
            self.window.show_view(self.window.views["starting_menu"])
