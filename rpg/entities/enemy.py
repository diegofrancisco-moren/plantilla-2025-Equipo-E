from rpg.entities.entity import Entity

class Enemy(Entity):
    def __init__(self, name, health, attack, defense, speed, mana, reward_exp):
        super().__init__(name, health, attack, defense, speed, mana)
        self.reward_exp = reward_exp
        'The reward after defeating an enemy. Gold? XP?, Weapons?'
