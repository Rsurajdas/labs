# Q3
class Enemy:
    def __init__(self, name, health):
        self.name = name
        self.health = health

    def talk(self):
        return f"{self.name} says nothing."

    def take_damage(self, amount):
        self.health -= amount
        return self.health


class Zombie(Enemy):
    def __init__(self, health):
        super().__init__("Zombie", health)

    def talk(self):
        return "Grrr..."


z = Zombie(50)
e = Enemy("Goblin", 30)

print(z.talk())
print(e.talk())
print(z.take_damage(15))
print(z.health, e.health)
print(z.name)

# "Grrr..."
# "Goblin says nothing."
# "35"
# "35, 30"
# "Zombie"


# Q10
class Wapon:
    def __init__(self, name, damage):
        self.name = name
        self.damage = damage


class Enemy:
    def __init__(self, name, health):
        self.name = name
        self.health = health

    def take_damage(self, amount):
        self.health = self.health - amount
        if self.health < 0:
            self.health = 0
        return max(self.health, 0)

    def is_alive(self):
        return self.health > 0


class Ogre(Enemy):
    def __init__(self, health, wapon):
        super().__init__("Ogre", health)
        self.wapon = wapon

    def attack(self, target):
        target.take_damage(self.wapon.damage)
        return f"Ogre hits {target.name} with {self.wapon.name} for {self.wapon.damage} damage"


arsenal = {
    "club": Wapon("club", 20),
    "axe": Wapon("axe", 35),
}

ogre = Ogre(50, arsenal["club"])
goblin = Enemy("Goblin", 50)

while goblin.is_alive():
    print(ogre.attack(goblin))
    print(f"Goblin current health: {goblin.health}")
