# tests/test_battle.py - Version corrigée qui marche avec ton Character existant
import pytest
from src.battle import Battle
from src.character import Character
from src.game import Game

@pytest.fixture
def sample_characters():
    """Create sample characters for testing"""
    # Utilise le constructeur comme il existe dans ton code
    char1 = Character("Alice")
    char2 = Character("Bob")
    return char1, char2

@pytest.fixture
def sample_game():
    """Create a sample game with players"""
    game = Game()
    game.add_player("Alice")
    game.add_player("Bob")
    return game

def test_duel_mechanic(sample_characters):
    """Test the duel mechanic between two characters"""
    char1, char2 = sample_characters
    battle = Battle(char1, char2)
    
    assert battle.is_valid_battle()
    winner = battle.start_duel()
    
    # One should be alive, one should be dead
    assert winner.is_alive()
    assert not (char1.is_alive() and char2.is_alive())
    
def test_team_battle(sample_characters):
    """Test team battle setup"""
    char1, char2 = sample_characters
    battle = Battle(char1, char2)
    
    # Test that battle can be initialized
    assert battle.player1 == char1
    assert battle.player2 == char2
    assert battle.turn_count == 0

def test_battle_stats(sample_characters):
    """Test battle statistics"""
    char1, char2 = sample_characters
    battle = Battle(char1, char2)
    
    stats = battle.get_battle_stats()
    
    assert 'turns' in stats
    assert 'player1_hp' in stats
    assert 'player2_hp' in stats
    assert 'battle_log' in stats
    
    assert stats['turns'] == 0  # No battle started yet
    assert stats['player1_hp'] == char1.health
    assert stats['player2_hp'] == char2.health

def test_invalid_battle():
    """Test invalid battle scenarios"""
    char1 = Character("Alice")
    char2 = Character("Bob")
    
    # Tuer le deuxième personnage
    char2.health = 0
    
    battle = Battle(char1, char2)
    assert not battle.is_valid_battle()  # Should be invalid due to dead character
    
    # Test same character battle
    battle2 = Battle(char1, char1)
    assert not battle2.is_valid_battle()  # Should be invalid - same character