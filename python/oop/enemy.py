class Enemy:
    def __init__(self, type, health, damage):
        self.type: str = type
        self.health: int = health
        self.damage: int = damage