"""Point d'entrée principal du jeu RPG-CI."""
from src.character import Character
from src.battle import Battle

def main():
    """Fonction principale du jeu."""
    print("⚔️ Bienvenue dans RPG-CI ⚔️\n")
    
    # Création des personnages
    hero = Character("Héros", health=10)
    enemy = Character("Ennemi", health=10)
    
    print("Personnages créés:")
    print(f"- {hero}")
    print(f"- {enemy}\n")
    
    # Initialisation du combat
    combat = Battle(hero, enemy)
    tour = 0
    
    print("Début du combat!\n")
    
    # Boucle de combat principale
    while not combat.is_battle_over():
        tour += 1
        print(f"--- Tour {tour} ---")
        
        # Tour du héros
        if hero.is_alive():
            print(f"{hero.name} attaque {enemy.name}!")
            result = combat.execute_turn(hero, enemy)
            print(f"→ {enemy.name} perd 1 HP (reste: {enemy.health}/10)")
        
        # Tour de l'ennemi s'il est encore vivant
        if enemy.is_alive():
            print(f"{enemy.name} attaque {hero.name}!")
            result = combat.execute_turn(enemy, hero)
            print(f"→ {hero.name} perd 1 HP (reste: {hero.health}/10)")
        
        print()
    
    # Résultat final
    print("\n🏁 Combat terminé!")
    gagnant = combat.get_winner()
    if gagnant:
        print(f"🎉 {gagnant.name} remporte la victoire!")
    else:
        print("Match nul!")

if __name__ == "__main__":
    main()