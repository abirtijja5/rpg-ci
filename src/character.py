class Character:
    MAX_HEALTH = 10
    
    def __init__(self, name):
        self.name = name
        self.health = self.MAX_HEALTH
    
    def is_alive(self):
        return self.health > 0
    
    def is_dead(self):
        return self.health <= 0
    
    def take_damage(self, damage):
        if damage < 0:
            raise ValueError("Damage cannot be negative")
        if self.is_alive():
            self.health = max(0, self.health - damage)
    
    def attack(self, target):
        if self.is_dead() or target is None or target.is_dead():
            return False
        target.take_damage(1)
        return True
    
    def heal(self, amount):
        if amount < 0:
            raise ValueError("Heal amount cannot be negative")
        if self.is_alive():
            self.health = min(self.MAX_HEALTH, self.health + amount)