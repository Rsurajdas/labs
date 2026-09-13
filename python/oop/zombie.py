from enemy import *

class Zombie(Enemy):
    def __init__(self, health, damage, weapon):
        super().__init__("Zombie", health, damage)
        self.weapon = weapon

    def special__attack(self, target):
        return f"{self.get__type()} is trying to bite {target.get__type()}!"