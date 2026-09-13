class Weapon:
    def __init__(self, type, damage):
        self.__type = type
        self.__damage = damage
        
    def get__type(self):
        return self.__type
    
    def get__damage(self):
        return self.__damage