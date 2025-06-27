def hello_world():
    """Fonction Hello World pour tests CI de base"""
    return "Hello World from RPG CI Project!"

def add_numbers(a, b):
    """Fonction simple pour tester la CI"""
    return a + b

def multiply_numbers(a, b):
    """Fonction pour tests supplémentaires"""
    return a * b

if __name__ == "__main__":
    print(hello_world())
    print(f"2 + 3 = {add_numbers(2, 3)}")
    print(f"4 * 5 = {multiply_numbers(4, 5)}")
