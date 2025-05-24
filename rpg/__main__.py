"""
Python Arcade Community RPG

An open-source RPG
"""
import os
import arcade

from rpg.constants import SCREEN_HEIGHT, SCREEN_TITLE, SCREEN_WIDTH
from rpg.views.starting_menu_view import StartingMenuView


class MyWindow(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, resizable=True)
        self.views = {}

        arcade.resources.add_resource_handle("characters", ".." +
                                             os.path.sep + "resources" +
                                             os.path.sep + "characters" +
                                             os.path.sep)
        arcade.resources.add_resource_handle("maps", ".." +
                                             os.path.sep + "resources" +
                                             os.path.sep + "maps" +
                                             os.path.sep)
        arcade.resources.add_resource_handle("data", ".." +
                                             os.path.sep + "resources" +
                                             os.path.sep + "data" +
                                             os.path.sep)
        arcade.resources.add_resource_handle("sounds", ".." +
                                             os.path.sep + "resources" +
                                             os.path.sep + "sounds" +
                                             os.path.sep)
        arcade.resources.add_resource_handle("animations", ".." +
                                             os.path.sep + "resources" +
                                             os.path.sep + "animations" +
                                             os.path.sep)
        arcade.resources.add_resource_handle("misc", ".." +
                                             os.path.sep + "resources" +
                                             os.path.sep + "misc" +
                                             os.path.sep)
        arcade.resources.add_resource_handle("enemies",".." +
                                             os.path.sep + "resources" +
                                             os.path.sep + "characters" +
                                             os.path.sep)

def main():
    """Main method"""
    window = MyWindow()
    window.center_window()
    start_view = StartingMenuView()
    start_view.setup()
    window.show_view(start_view)
    arcade.run()


if __name__ == "__main__":
    main()
