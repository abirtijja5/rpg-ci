def test_character_can_attack():
    hero = Character("Hero")
    villain = Character("Villain") 
    
    success = hero.attack(villain)
    
    self.assertTrue(success)
    self.assertEqual(villain.health, 9)
