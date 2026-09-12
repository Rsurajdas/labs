from enemy import *

zombie = Enemy("Zombie", 100, 5)
orge = Enemy("Orge", 250, 15)

print(zombie.info())
print(orge.info())

print(zombie.attack())
print(orge.attack())

print(zombie.move_towards(orge))
print(orge.move_towards(zombie))
