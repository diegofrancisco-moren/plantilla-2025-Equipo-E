import arcade

from rpg.sprites.character_sprite import CharacterSprite
from rpg.entities.player import Player

class PlayerSprite(CharacterSprite):

    def __init__(self, sheet_name, statistics, scale):
        super().__init__(sheet_name, scale = scale)
        self.sound_update = 0
        self.footstep_sound = None
        self.sheet_name = sheet_name
        self.statistics = statistics

    def on_update(self, delta_time):
        super().on_update(delta_time)

        if not self.change_x and not self.change_y:
            self.sound_update = 0
            return

        if self.should_update > 3:
            self.sound_update += 1

        if self.sound_update >= 3:
            arcade.play_sound(self.footstep_sound)
            self.sound_update = 0
