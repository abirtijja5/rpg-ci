import random
from .character import Character
from .game import Game

class Battle:
    """Classe pour gérer les combats entre personnages"""
    
    def __init__(self, player1, player2):
        """
        Initialise un combat entre deux joueurs
        
        Args:
            player1 (Character): Premier combattant
            player2 (Character): Second combattant
        """
        self.player1 = player1
        self.player2 = player2
        self.turn_count = 0
        self.battle_log = []
        self.winner = None
    
    def is_battle_over(self):
        """Vérifie si le combat est terminé"""
        return self.player1.is_dead() or self.player2.is_dead()
    
    def get_winner(self):
        """Retourne le gagnant du combat"""
        if not self.is_battle_over():
            return None
        
        if self.player1.is_alive():
            return self.player1
        elif self.player2.is_alive():
            return self.player2
        return None  # Match nul (théoriquement impossible)
    
    def execute_turn(self, attacker, defender):
        """
        Exécute un tour de combat
        
        Args:
            attacker (Character): L'attaquant
            defender (Character): Le défenseur
            
        Returns:
            dict: Résultat du tour
        """
        if self.is_battle_over():
            return {"success": False, "message": "Le combat est terminé"}
        
        initial_health = defender.health
        success = attacker.attack(defender)
        
        result = {
            "success": success,
            "attacker": attacker.name,
            "defender": defender.name,
            "damage": initial_health - defender.health if success else 0,
            "defender_health": defender.health,
            "defender_died": defender.is_dead(),
            "turn": self.turn_count + 1
        }
        
        self.battle_log.append(result)
        self.turn_count += 1
        
        if self.is_battle_over():
            self.winner = self.get_winner()
            result["battle_over"] = True
            result["winner"] = self.winner.name if self.winner else "Aucun"
        
        return result
    
    def simulate_battle(self):
        """
        Simule un combat complet automatiquement
        
        Returns:
            dict: Résultat final du combat
        """
        current_attacker = self.player1
        current_defender = self.player2
        
        while not self.is_battle_over() and self.turn_count < 100:  # Limite de sécurité
            self.execute_turn(current_attacker, current_defender)
            
            # Changer de tour
            current_attacker, current_defender = current_defender, current_attacker
        
        return {
            "winner": self.winner.name if self.winner else "Aucun",
            "turns": self.turn_count,
            "battle_log": self.battle_log,
            "final_state": {
                "player1": self.player1.get_status(),
                "player2": self.player2.get_status()
            }
        }