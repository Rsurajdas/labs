class Enemy:
    def __init__(self, type, health, damage, weapon):
        self.__type: str = type
        self.__health: int = health
        self.__damage: int = damage
        self.__weapon = weapon

    def get__type(self):
        return self.__type

    def get__health(self):
        return self.__health

    def get__damage(self):
        return self.__damage

    def info(self):
        return f"Type: {self.__type}, Health: {self.__health}, Damage: {self.__damage}"

    def attack(self):
        return f"{self.__type} attacks for {self.__damage} damage!"

    def move__towards(self, target):
        return f"{self.__type} moves towards {target.__type}!"
    
    def special__attack(self):
        pass
    
    def weapon__attack(self):
        return f"{self.get__type()} attacks with {self.__weapon.get__type()} for {self.__weapon.get__damage()} damage!"