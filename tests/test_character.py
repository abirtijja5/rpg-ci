import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.character import Character

class TestCharacter(unittest.TestCase):
    """Tests pour la classe Character"""
    
    def setUp(self):
        """Configuration avant chaque test"""
        self.hero = Character("Héros")
        self.villain = Character("Méchant")
    
    def test_character_creation_default_hp(self):
        """Test 1: Un personnage a 10 HP par défaut"""
        character = Character("Test")
        self.assertEqual(character.health, 10)
        self.assertEqual(character.max_health, 10)
    
    def test_character_creation_with_name(self):
        """Test 2: Un personnage a un nom"""
        character = Character("TestName")
        self.assertEqual(character.name, "TestName")
    
    def test_character_creation_custom_hp(self):
        """Test 3: Création avec HP personnalisés"""
        character = Character("Test", health=5)
        self.assertEqual(character.health, 5)
        self.assertEqual(character.max_health, 10)  # max_health reste 10
    
    def test_character_is_alive_with_positive_hp(self):
        """Test 4: Un personnage avec >0 HP est vivant"""
        self.assertTrue(self.hero.is_alive())
        self.assertFalse(self.hero.is_dead())
    
    def test_character_is_dead_with_zero_hp(self):
        """Test 5: Un personnage avec 0 HP est mort"""
        self.hero.health = 0
        self.assertFalse(self.hero.is_alive())
        self.assertTrue(self.hero.is_dead())
    
    def test_character_attack_reduces_hp(self):
        """Test 6: Une attaque retire 1 HP"""
        initial_hp = self.villain.health
        success = self.hero.attack(self.villain)
        
        self.assertTrue(success)
        self.assertEqual(self.villain.health, initial_hp - 1)
    
    def test_dead_character_cannot_attack(self):
        """Test 7: Un personnage mort ne peut pas attaquer"""
        self.hero.health = 0
        success = self.hero.attack(self.villain)
        
        self.assertFalse(success)
        self.assertEqual(self.villain.health, 10)  # Pas de dégâts
    
    def test_cannot_attack_dead_character(self):
        """Test 8: Attaquer un personnage mort ne change rien"""
        self.villain.health = 0
        initial_hp = self.villain.health
        success = self.hero.attack(self.villain)
        
        self.assertFalse(success)
        self.assertEqual(self.villain.health, initial_hp)
    
    def test_character_dies_at_zero_hp(self):
        """Test 9: Un personnage meurt à 0 HP exactement"""
        self.villain.health = 1
        self.hero.attack(self.villain)
        
        self.assertEqual(self.villain.health, 0)
        self.assertTrue(self.villain.is_dead())
        self.assertFalse(self.villain.is_alive())
    
    def test_multiple_attacks_until_death(self):
        """Test 10: Combat jusqu'à la mort"""
        attacks_needed = self.villain.health
        
        for _ in range(attacks_needed):
            if self.villain.is_alive():
                self.hero.attack(self.villain)
        
        self.assertTrue(self.villain.is_dead())
        self.assertEqual(self.villain.health, 0)
    
    def test_take_damage_with_negative_damage(self):
        """Test 11: Les dégâts négatifs lèvent une exception"""
        with self.assertRaises(ValueError):
            self.hero.take_damage(-5)
    
    def test_heal_character(self):
        """Test 12: Soigner un personnage augmente ses HP"""
        self.hero.health = 5
        self.hero.heal(3)
        self.assertEqual(self.hero.health, 8)
    
    def test_heal_cannot_exceed_max_hp(self):
        """Test 13: Les soins ne peuvent pas dépasser le maximum"""
        self.hero.health = 8
        self.hero.heal(5)
        self.assertEqual(self.hero.health, 10)  # Plafonné au maximum
    
    def test_heal_with_negative_amount(self):
        """Test 14: Les soins négatifs lèvent une exception"""
        with self.assertRaises(ValueError):
            self.hero.heal(-3)
    
    def test_character_defense_reduces_damage(self):
        """Test 15: La défense réduit les dégâts"""
        self.villain.defend()
        self.hero.attack(self.villain)
        
        # Dégâts réduits de moitié (min 1)
        self.assertEqual(self.villain.health, 9)  # 10 - max(1, 1//2) = 9
        self.assertFalse(self.villain.is_defending)  # Défense annulée après attaque
    
    def test_character_status(self):
        """Test 16: Récupération du statut du personnage"""
        status = self.hero.get_status()
        
        expected_keys = ['name', 'health', 'max_health', 'is_alive', 'is_defending']
        for key in expected_keys:
            self.assertIn(key, status)
        
        self.assertEqual(status['name'], 'Héros')
        self.assertEqual(status['health'], 10)
        self.assertTrue(status['is_alive'])
    
    def test_character_string_representation(self):
        """Test 17: Représentation string du personnage"""
        result = str(self.hero)
        self.assertIn(self.hero.name, result)
        self.assertIn(str(self.hero.health), result)
        self.assertIn("Vivant", result)
        
        # Test avec personnage mort
        self.hero.health = 0
        result = str(self.hero)
        self.assertIn("Mort", result)
