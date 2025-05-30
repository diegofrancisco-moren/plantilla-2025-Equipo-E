import os
import json

from rpg import constants
from rpg.entities.player import Player
from rpg.sprites.player_sprite import PlayerSprite


def save_game(player, game_view, button_text):
    save_data = {
        # Atributos Clase Player
        "class_type": player.statistics.get_class_type(),
        "level": player.statistics.get_level(),
        "xp": player.statistics.get_xp(),
        "xp_max": player.statistics.get_xp_max(),

        # Atributos Clase Entity
        "name": player.statistics.get_name(),
        "health": player.statistics.get_health(),
        "health_max": player.statistics.get_health_max(),
        "mana": player.statistics.get_mana(),
        "mana_max": player.statistics.get_mana_max(),
        "attack": player.statistics.get_attack(),
        "defense": player.statistics.get_defense(),
        "speed": player.statistics.get_speed(),
        "inventory": player.statistics.get_inventory(),

        # Atributos clase Sprite
        "player_position": list(player.get_position()),

        # Atributos clase GameView
        "cur_map_name": game_view.get_cur_map_name(),

    }

    # El nombre del archivo JSON será el nombre del jugador
    base_file = ".." + os.path.sep + "resources" + os.path.sep + "saves" + os.path.sep
    file_name = f"save_player_{player.statistics.get_name()}"
    extension = ".json"


    # Si esta partida no tiene arhcivo de guardado se crea uno
    print(button_text)
    if button_text == "Archivo libre":
        candidate = base_file + file_name + extension
        counter = 0
        # Si el nombre del archivo ya existe, se le añade un número
        while os.path.exists(candidate):
            candidate = f"{base_file}{file_name}_{counter}{extension}"
            counter += 1

        player.statistics.save_file = candidate
    elif file_name != button_text:
        os.remove(f"{base_file}{button_text}")
        candidate = base_file + file_name + extension
        counter = 0
        # Si el nombre del archivo ya existe, se le añade un número
        while os.path.exists(candidate):
            candidate = f"{base_file}{file_name}_{counter}{extension}"
            counter += 1
        player.statistics.save_file = candidate


    with open(player.statistics.save_file, "w") as f:
        json.dump(save_data, f, indent=2)

    return player.statistics.save_file

def load_game(filename, gameview):
    filepath = (".." + os.path.sep + "resources" + os.path.sep + "saves" +
                os.path.sep + f"{filename}")
    with open(filepath, "r") as f:
        save_data = json.load(f)
    print("¡Partida cargada!")

    # Restaurar datos del jugador y sus estadísticas
    player_statistics = Player(save_data["name"], save_data["health_max"], save_data["attack"], save_data["defense"],
                               save_data["speed"], save_data["mana_max"], save_data["class_type"])
    player_statistics.set_level(save_data["level"])
    player_statistics.set_xp(save_data["xp"])
    player_statistics.set_xp_max(save_data["xp_max"])
    player_statistics.set_health(save_data["health"])
    player_statistics.set_mana(save_data["mana"])
    player_statistics.set_save_file(filename)
    player_statistics.set_inventory(save_data["inventory"])

    player_statistics.leveling_up()
    player_class = save_data["class_type"]
    if player_class == "knight":
        # Restaurar sprite del jugador, inventario, mapa y ultima posicion
        player_sprite = PlayerSprite(constants.knight_sheet_name, player_statistics,
                                     constants.knight_battle_sprite, scale=constants.SCALE)
    elif player_class == "magician":
        # Restaurar sprite del jugador, inventario, mapa y ultima posicion
        player_sprite = PlayerSprite(constants.magician_sheet_name, player_statistics,
                                     constants.magician_battle_sprite, scale=constants.SCALE)
    else:
        # Restaurar sprite del jugador, inventario, mapa y ultima posicion
        player_sprite = PlayerSprite(constants.thief_sheet_name, player_statistics,
                                     constants.thief_battle_sprite, scale=constants.SCALE)



    gameview.set_player_sprite(player_sprite)

    map_name = save_data["cur_map_name"]

    x_player, y_player = save_data["player_position"]
    x_player = (x_player / constants.SPRITE_SIZE) - 0.5
    y_player = (gameview.map_list[map_name].map_size[1] - y_player / constants.SPRITE_SIZE) - 1
    print("COORDENADA X " + str(x_player))
    print("COORDENADA Y " + str(y_player))
    gameview.switch_map(map_name, x_player, y_player)

    gameview.set_cur_map_name(map_name)







