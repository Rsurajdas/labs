class Enemy:
    def __init__(self, type, health, damage):
        self.type: str = type
        self.health: int = health
        self.damage: int = damage

    def info(self):
        return f"Type: {self.type}, Health: {self.health}, Damage: {self.damage}"