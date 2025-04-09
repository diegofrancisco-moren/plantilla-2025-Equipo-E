class Entity:
    def __init__(self, name, health, attack, defense, speed, mana):
        self.name = name
        self.health = health
        self.attack = attack
        self.defense = defense
        self.speed = speed
        self.mana = mana
        self.attack_list = []
        'The attacks can be storage at the .json file in resources > data > attacks_list'

    def alive(self):
        return self.health > 0
