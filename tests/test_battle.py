import pytest
from src.game import Game
from src.battle import Battle
from src.character import Character

@pytest.fixture
def sample_game():
    game = Game()
    game.add_player("Warrior")
    game.add_player("Mage")
    game.add_player("Archer")
    game.add_player("Healer", health=15)
    return game

def test_duel_mechanic(sample_game):
    battle = Battle(sample_game)
    results = battle.duel("Warrior", "Mage")
    
    assert results['rounds'] > 0
    assert results['winner'] in ["Warrior", "Mage"]
    assert results['loser'] in ["Warrior", "Mage"]
    assert results['winner'] != results['loser']
    
    winner = sample_game.get_player(results['winner'])
    assert winner.is_alive() is True

def test_team_battle(sample_game):
    battle = Battle(sample_game)
    results = battle.team_battle(
        ["Warrior", "Mage"],
        ["Archer", "Healer"]
    )
    
    assert results['rounds'] > 0
    assert results['winner_team'] in ['A', 'B']
    assert len(results['survivors']) > 0
    
    for survivor in results['survivors']:
        assert sample_game.get_player(survivor).is_alive()

def test_battle_stats(sample_game):
    battle = Battle(sample_game)
    battle.duel("Warrior", "Mage")
    battle.team_battle(["Warrior"], ["Archer", "Healer"])
    
    stats = battle.get_battle_stats()
    assert stats['total_battles'] == 2
    assert stats['total_rounds'] > 0
    assert len(stats['duels']) == 1
    assert len(stats['team_battles']) == 1

def test_invalid_battle(sample_game):
    battle = Battle(sample_game)
    
    with pytest.raises(ValueError):
        battle.duel("Invalid", "Warrior")
    
    with pytest.raises(ValueError):
        battle.duel("Warrior", "Invalid")