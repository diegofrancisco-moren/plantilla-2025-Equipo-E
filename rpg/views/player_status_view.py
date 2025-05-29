import arcade
from pathlib import Path
from rpg.entities.player import Player

class PlayerStatusView(arcade.View, Player):
    def __init__(self, player):
        super().__init__()
        self.player = player
        project_root = Path(__file__).resolve().parents[2]
        sprite_path = project_root / "resources" / "characters" / "Player" / "knight_big.png"
        self.player_sprite = arcade.Sprite(str(sprite_path), scale=0.5, center_x=150, center_y=350)
        arcade.set_background_color(arcade.color.ALMOND)

    def on_draw(self):
        arcade.set_background_color(arcade.color.ALMOND)
        arcade.start_render()
        self.player_sprite.draw()

        stats_x = 500
        stats_y = 400
        spacing = 25

        # Estadísticas del jugador
        stats = [
            f'Level: {self.player.level}',
            f"XP: {self.player.xp}/{self.player.xp_max}",
            f"Health: {self.player.health}/{self.player.health_max}",
            f"Attack Stat: {self.player.attack}",
            f"Defense Stat: {self.player.defense}",
            f"Speed Stat: {self.player.speed}",
        ]

        for i, line in enumerate(stats):
            arcade.draw_text(line, stats_x, stats_y - i * spacing, arcade.color.WHITE, 16)

    def on_key_press(self, symbol, modifiers):
        # Volver a la vista anterior si se pulsa ESC
        if symbol == arcade.key.ESCAPE:
            self.window.show_view(self.window.previous_view)