import unittest
from hello_world import hello_world, add_numbers

class TestHelloWorld(unittest.TestCase):
    def test_true_equals_true(self):
        self.assertTrue(True == True)
    
    def test_hello_world(self):
        result = hello_world()
        self.assertIn("Hello World", result)
    
    def test_add_numbers(self):
        self.assertEqual(add_numbers(2, 3), 5)