from enemy import *

class Orge(Enemy):
    def __init__(self, health, damage):
        super().__init__("Orge", health, damage)

    def special__attack(self, target):
        return f"{self.get__type()} is trying to smash {target.get__type()}!"