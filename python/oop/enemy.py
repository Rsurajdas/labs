class Enemy:
    def __init__(self, type, health, damage):
        self.__type: str = type
        self.__health: int = health
        self.__damage: int = damage

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

    def move_towards(self, target):
        return f"{self.__type} moves towards {target.__type}!"