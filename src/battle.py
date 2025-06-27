class Battle:
    def __init__(self, player1, player2):
        """
        Initialize a battle between two players.
        
        Args:
            player1: First player/character
            player2: Second player/character
        """
        self.player1 = player1
        self.player2 = player2
        self.turn_count = 0
        self.battle_log = []
    
    def start_duel(self):
        """Start a duel between the two players."""
        self.battle_log.append(f"Duel started between {self.player1.name} and {self.player2.name}")
        
        while self.player1.is_alive() and self.player2.is_alive():
            self.turn_count += 1
            
            # Player 1's turn
            if self.player1.is_alive():
                damage = self.player1.attack(self.player2)
                self.battle_log.append(f"Turn {self.turn_count}: {self.player1.name} attacks {self.player2.name} for {damage} damage")
            
            # Player 2's turn
            if self.player2.is_alive():
                damage = self.player2.attack(self.player1)
                self.battle_log.append(f"Turn {self.turn_count}: {self.player2.name} attacks {self.player1.name} for {damage} damage")
        
        winner = self.player1 if self.player1.is_alive() else self.player2
        self.battle_log.append(f"Battle ended! Winner: {winner.name}")
        return winner
    
    def get_battle_stats(self):
        """Get battle statistics."""
        return {
            'turns': self.turn_count,
            'player1_hp': self.player1.health,
            'player2_hp': self.player2.health,
            'battle_log': self.battle_log
        }
    
    def is_valid_battle(self):
        """Check if the battle setup is valid."""
        return (self.player1 is not None and 
                self.player2 is not None and 
                self.player1.is_alive() and 
                self.player2.is_alive() and
                self.player1 != self.player2)