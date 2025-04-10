import entity

class Enemy(entity):
    def __init__(self, name, health, attack, defense, speed, mana):
        super().__init__(name, health, attack, defense, speed, mana)
        self.xp = 0
        self.xp_max = 100
        self.level = 1

    def leveling_up(self):
        if self.xp >= self.xp_max:
            self.xp = self.xp - self.xp_max
            self.level += 1
            self.xp_max += (self.xp_max * 0.1)
            self.health += (self.health * 0.1)
            self.attack += (self.attack * 0.1)
            self.defense += (self.defense * 0.1)
            self.speed +=  (self.speed * 0.1)
