class Character:
    """
    Classe représentant un personnage du RPG-ci 
    
    Chaque personnage a :
    - 10 points de vie maximum
    - Capacité d'attaquer (1 dégât par attaque)
    - Capacité de se défendre ou se soigner
    """
    
    MAX_HEALTH = 10
    ATTACK_DAMAGE = 1
    HEAL_AMOUNT = 2
    
    def __init__(self, name, health=None):
        """
        Initialise un nouveau personnage
        
        Args:
            name (str): Nom du personnage
            health (int, optional): Points de vie initiaux (défaut: MAX_HEALTH)
        """
        if not name or not isinstance(name, str):
            raise ValueError("Le nom doit être une chaîne non vide")
            
        self.name = name
        self.health = health if health is not None else self.MAX_HEALTH
        self.max_health = self.MAX_HEALTH
        self.is_defending = False
    
    def is_alive(self):
        """Vérifie si le personnage est vivant"""
        return self.health > 0
    
    def is_dead(self):
        """Vérifie si le personnage est mort"""
        return self.health <= 0
    
    def take_damage(self, damage):
        """
        Fait subir des dégâts au personnage
        
        Args:
            damage (int): Montant des dégâts
            
        Raises:
            ValueError: Si les dégâts sont négatifs
        """
        if damage < 0:
            raise ValueError("Les dégâts ne peuvent pas être négatifs")
        
        if self.is_alive():
            # Réduction des dégâts si en défense
            actual_damage = max(1, damage // 2) if self.is_defending else damage
            self.health = max(0, self.health - actual_damage)
            # Réinitialiser la défense après avoir pris des dégâts
            self.is_defending = False
    
    def attack(self, target):
        """
        Attaque un autre personnage
        
        Args:
            target (Character): Le personnage à attaquer
            
        Returns:
            bool: True si l'attaque réussit, False sinon
        """
        # Vérifications de base
        if self.is_dead():
            return False
        
        if target is None or target.is_dead():
            return False
        
        # Exécuter l'attaque
        target.take_damage(self.ATTACK_DAMAGE)
        
        # Annuler la défense de l'attaquant
        self.is_defending = False
        
        return True
    
    def heal(self, amount=None):
        """
        Soigne le personnage
        
        Args:
            amount (int, optional): Montant des soins (défaut: HEAL_AMOUNT)
            
        Raises:
            ValueError: Si le montant est négatif
        """
        heal_amount = amount if amount is not None else self.HEAL_AMOUNT
        
        if heal_amount < 0:
            raise ValueError("Les soins ne peuvent pas être négatifs")
        
        if self.is_alive():
            old_health = self.health
            self.health = min(self.max_health, self.health + heal_amount)
            return self.health - old_health
        return 0
    
    def defend(self):
        """Met le personnage en position défensive"""
        if self.is_alive():
            self.is_defending = True
    
    def get_status(self):
        """
        Retourne le statut complet du personnage
        
        Returns:
            dict: Informations sur le personnage
        """
        return {
            'name': self.name,
            'health': self.health,
            'max_health': self.max_health,
            'is_alive': self.is_alive(),
            'is_defending': self.is_defending,
            'health_percentage': (self.health / self.max_health) * 100
        }
    
    def __str__(self):
        """Représentation string du personnage"""
        status = "Vivant" if self.is_alive() else "Mort"
        defense = " (Défense)" if self.is_defending else ""
        return f"{self.name}: {self.health}/{self.max_health} HP - {status}{defense}"
    
    def __repr__(self):
        return f"Character(name='{self.name}', health={self.health})"