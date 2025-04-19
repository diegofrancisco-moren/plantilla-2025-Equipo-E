import json


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

    def add_attack(self, player):
        with open("../resources/data/attacks_list.json") as f:
            attack_dictionary = json.load(f)
        for attack_data in attack_dictionary.values():
            if attack_data["type"] == "physic":
                if attack_data["class"] == player.class_type or attack_data["class"] == "all":
                    if attack_data["level"] == player.level:
                        self.attack_list.append(attack_data)


    def add_magic_attack(self, player):
        with open("../resources/data/attacks_list.json") as f:
            attack_dictionary = json.load(f)
        for attack_data in attack_dictionary.values():
            if attack_data["type"] == "magic":
                if attack_data["class"] == player.class_type or attack_data["class"] == "all":
                    if attack_data["level"] == player.level:
                        self.attack_list.append(attack_data)