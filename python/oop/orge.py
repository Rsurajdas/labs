from enemy import *

class Orge(Enemy):
    def __init__(self, health, damage, weapon):
        super().__init__("Orge", health, damage)
        self.weapon = weapon

    def special__attack(self, target):
        return f"{self.get__type()} is trying to smash {target.get__type()}!"