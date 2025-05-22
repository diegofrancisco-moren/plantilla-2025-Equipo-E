
from rpg.entities.entity import Entity
from rpg import constants

class Player(Entity):
    def __init__(self, name, health, attack, defense, speed, mana, class_type):
        super().__init__(name, health, attack, defense, speed, mana)
        self.xp = 0
        self.xp_max = 100
        self.level = 1
        self.class_type = class_type
        self.save_file = None
        self.inventory = {}


    def leveling_up(self):
        while self.xp >= self.xp_max:
            self.xp = self.xp - self.xp_max
            self.level += 1
            self.xp_max += (self.xp_max * 0.1)
            self.health += (self.health * 0.1)
            self.attack += (self.attack * 0.1)
            self.defense += (self.defense * 0.1)
            self.speed +=  (self.speed * 0.1)
            print(self.name + " ha subido al nivel " + str(self.level) + "\n")
        self.add_player_attack()
        self.add_player_magic_attack()
        print("\n")

    def add_xp(self, amount):
        self.xp += amount
        self.leveling_up()

    # Metodo para añadir ataques físicos al jugador
    def add_player_attack(self):
        attack_dictionary = constants.attack_dictionary
        for attack_data in attack_dictionary.values():
            if attack_data["type"] == "physic":
                if attack_data["class"] == self.class_type or attack_data["class"] == "all":
                    if attack_data["level"] <= self.level:
                        if not(attack_data["learned"]):
                            self.attack_list.append(attack_data)
                            print(self.name + " aprendió " + attack_data["name"])
                            attack_data["learned"] = True

    # Metodo para añadir ataques mágicos al jugador
    def add_player_magic_attack(self):
        attack_dictionary = constants.attack_dictionary
        for attack_data in attack_dictionary.values():
            if attack_data["type"] == "magic":
                if attack_data["class"] == self.class_type or attack_data["class"] == "all":
                    if attack_data["level"] <= self.level:
                        if not (attack_data["learned"]):
                            self.attack_magic_list.append(attack_data)
                            print(self.name + " aprendió " + attack_data["name"])
                            attack_data["learned"] = True

    def get_xp(self):
        return self.xp

    def get_xp_max(self):
        return self.xp_max

    def get_level(self):
        return self.level

    def get_class_type(self):
        return self.class_type

    def get_save_file(self):
        return self.save_file

    def set_xp(self, value):
        self.xp = value

    def set_xp_max(self, value):
        self.xp_max = value

    def set_level(self, value):
        self.level = value

    def set_save_file(self, save_file):
        self.save_file = save_file

    def get_inventory(self):
        return self.inventory

    def set_inventory(self, inventory):
        self.inventory = inventory

    def del_item_inventory(self, item_name):
        del self.inventory[item_name]
