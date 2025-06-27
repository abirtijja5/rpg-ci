
import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.game import Game
from src.character import Character

class TestGame(unittest.TestCase):
    """Tests pour la classe Game"""
    
    def setUp(self):
        """Configuration avant chaque test"""
        self.game = Game()
    
    def test_game_creation(self):
        """Test 18: Création d'un jeu vide"""
        self.assertEqual(len(self.game.players), 0)
        self.assertEqual(self.game.turn_count, 0)
        self.assertFalse(self.game.game_over)
        self.assertIsNone(self.game.winner)
    
    def test_add_player_success(self):
        """Test 19: Ajout réussi d'un joueur"""
        player = self.game.add_player("Alice")
        
        self.assertEqual(len(self.game.players), 1)
        self.assertEqual(player.name, "Alice")
        self.assertIn(player, self.game.players)
    
    def test_add_player_invalid_name(self):
        """Test 20: Ajout d'un joueur avec nom invalide"""
        with self.assertRaises(ValueError):
            self.game.add_player("")
        
        with self.assertRaises(ValueError):
            self.game.add_player(None)
        
        with self.assertRaises(ValueError):
            self.game.add_player(123)
    
    def test_get_alive_players(self):
        """Test 21: Récupération des joueurs vivants"""
        player1 = self.game.add_player("Alice")
        player2 = self.game.add_player("Bob")
        
        alive = self.game.get_alive_players()
        self.assertEqual(len(alive), 2)
        
        # Tuer un joueur
        player1.health = 0
        alive = self.game.get_alive_players()
        self.assertEqual(len(alive), 1)
        self.assertEqual(alive[0], player2)
    
    def test_get_dead_players(self):
        """Test 22: Récupération des joueurs morts"""
        player1 = self.game.add_player("Alice")
        player2 = self.game.add_player("Bob")
        
        dead = self.game.get_dead_players()
        self.assertEqual(len(dead), 0)
        
        # Tuer un joueur
        player1.health = 0
        dead = self.game.get_dead_players()
        self.assertEqual(len(dead), 1)
        self.assertEqual(dead[0], player1)
    
    def test_game_over_condition(self):
        """Test 23: Condition de fin de jeu"""
        player1 = self.game.add_player("Alice")
        player2 = self.game.add_player("Bob")
        
        # Jeu en cours avec 2 joueurs vivants
        self.assertFalse(self.game.is_game_over())
        
        # Tuer un joueur - jeu terminé
        player1.health = 0
        self.assertTrue(self.game.is_game_over())
    
    def test_get_winner(self):
        """Test 24: Détermination du gagnant"""
        player1 = self.game.add_player("Alice")
        player2 = self.game.add_player("Bob")
        
        # Pas de gagnant si jeu en cours
        self.assertIsNone(self.game.get_winner())
        
        # Gagnant quand un seul reste
        player1.health = 0
        winner = self.game.get_winner()
        self.assertEqual(winner, player2)
    
    def test_simulate_turn_attack(self):
        """Test 25: Simulation d'un tour d'attaque"""
        self.game.add_player("Alice")
        self.game.add_player("Bob")
        
        result = self.game.simulate_turn("Alice", "Bob", "attack")
        
        self.assertTrue(result["success"])
        self.assertEqual(result["action"], "attack")
        self.assertEqual(result["attacker"], "Alice")
        self.assertEqual(result["target"], "Bob")
        self.assertEqual(result["damage_dealt"], 1)
        self.assertEqual(result["target_health"], 9)
    
    def test_simulate_turn_defense(self):
        """Test 26: Simulation d'un tour de défense"""
        self.game.add_player("Alice")
        
        result = self.game.simulate_turn("Alice", None, "defend")
        
        self.assertTrue(result["success"])
        self.assertEqual(result["action"], "defend")
        self.assertTrue(self.game.players[0].is_defending)
    
    def test_simulate_turn_heal(self):
        """Test 27: Simulation d'un tour de soin"""
        player = self.game.add_player("Alice")
        player.health = 5  # Blesser le joueur
        
        result = self.game.simulate_turn("Alice", None, "heal")
        
        self.assertTrue(result["success"])
        self.assertEqual(result["action"], "heal")
        self.assertEqual(result["health_restored"], 2)
        self.assertEqual(result["current_health"], 7)
    
    def test_simulate_turn_invalid_attacker(self):
        """Test 28: Tour avec attaquant invalide"""
        self.game.add_player("Alice")
        
        result = self.game.simulate_turn("Bob", "Alice", "attack")
        
        self.assertFalse(result["success"])
        self.assertIn("ne peut pas agir", result["message"])
    
    def test_game_state(self):
        """Test 29: État du jeu"""
        self.game.add_player("Alice")
        self.game.add_player("Bob")
        
        state = self.game.get_game_state()
        
        expected_keys = ['turn_count', 'total_players', 'alive_players', 
                        'dead_players', 'players', 'game_over', 'winner',
                        'history_length']
        for key in expected_keys:
            self.assertIn(key, state)
        
        self.assertEqual(state['total_players'], 2)
        self.assertEqual(state['alive_players'], 2)
        self.assertEqual(state['dead_players'], 0)
        self.assertFalse(state['game_over'])
        self.assertIsNone(state['winner'])