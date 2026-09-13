from zombie import *
from orge import *
from enemy import *

zombie = Zombie(100, 5)
orge = Orge(250, 15)

# print(zombie.__type)  # This will raise an AttributeError because __type is private
# print(zombie.get__type())  # This will work because get_type() is a public method
# print(orge.get__type())  # This will work because get_type() is a public method

def battle(e: Enemy, target):
    return "\n".join([
        e.info(),
        e.attack()
    ])

enemys: Enemy = [zombie, orge]

def arena(enemys):
    for attacker in enemys:
        for defender in enemys:
            if attacker is not defender:
                print(battle(attacker, defender))
                
arena(enemys)
