import entity

class Enemy(entity):
    def __init__(self, name, health, attack, defense, speed, mana, reward):
        super().__init__(name, health, attack, defense, speed, mana)
        self.reward = reward
        'The reward after defeating an enemy. Gold? XP?, Weapons?'
