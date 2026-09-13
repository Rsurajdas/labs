from zombie import *
from orge import *

zombie = Zombie(100, 5)
orge = Orge(250, 15)

# print(zombie.__type)  # This will raise an AttributeError because __type is private
print(zombie.get__type())  # This will work because get_type() is a public method
print(orge.get__type())  # This will work because get_type() is a public method

print(zombie.info())
print(orge.info())

print(zombie.attack())
print(orge.attack())

print(zombie.move_towards(orge))
print(orge.move_towards(zombie))

print(zombie.special__attack(orge))
print(orge.special__attack(zombie))
