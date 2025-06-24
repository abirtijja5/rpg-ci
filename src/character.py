class Character:
    def __init__(self, name):
        self.name = name
        self.health = 10
    
    def attack(self, target):
        if target:
            target.health -= 1
            return True
        return False
