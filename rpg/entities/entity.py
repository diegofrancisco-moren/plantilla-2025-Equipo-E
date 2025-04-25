
from rpg import constants

class Entity:
    def __init__(self, name, health, attack, defense, speed, mana):
        self.name = name
        self.health = health
        self.healh_max = health
        self.attack = attack
        self.defense = defense
        self.speed = speed
        self.mana = mana
        self.mana_max = mana
        self.attack_list = []
        self.attack_magic_list = []
        'The attacks can be storage at the .json file in resources > data > attacks_list'

    def alive(self):
        return self.health > 0

    def health_up(self, amount):
        new_health = amount + self.health
        if new_health > self.healh_max:
            new_health = self.healh_max

        self.health = new_health

    def health_down(self,amount):
        new_health = self.health - amount
        if new_health < 0:
            new_health = 0

        self.health = new_health

    def mana_up(self, amount):
        new_mana = amount + self.mana
        if new_mana > self.mana_max:
            new_mana = self.mana_max

        self.mana = new_mana

    def mana_down(self, amount):
        new_mana = self.health - amount
        if new_mana < 0:
            new_mana = self.mana_max

        self.mana = new_mana


    # Metodo para añadir ataques (de cualquier tipo) a los enemigos
    def add_enemy_attack(self, enemy_type):
        attack_dictionary = constants.attack_dictionary
        for attack_ref in enemy_type["attacks"]:
            attack_name = attack_ref["name"]
            if attack_name in attack_dictionary:
                attack_data = attack_dictionary[attack_name]
                self.attack_list.append(attack_data)

    def get_name(self):
        return self.name

    def get_health(self):
        return self.health

    def get_health_max(self):
        return self.healh_max

    def get_attack(self):
        return self.attack

    def get_defense(self):
        return self.defense

    def get_speed(self):
        return self.speed

    def get_mana(self):
        return self.mana

    def get_mana_max(self):
        return self.mana_max

    def set_name(self, value):
        self.name = value

    def set_health(self, value):
        self.health = value

    def set_health_max(self, value):
        self.healh_max = value

    def set_attack(self, value):
        self.attack = value

    def set_defense(self, value):
        self.defense = value

    def set_speed(self, value):
        self.speed = value

    def set_mana(self, value):
        self.mana = value

    def set_mana_max(self, value):
        self.mana_max = value

