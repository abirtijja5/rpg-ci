from .character import Character

class Game:
    """
    Classe principale pour gérer une partie de RPG
    
    Permet de :
    - Ajouter des joueurs
    - Gérer les tours de jeu
    - Déterminer le gagnant
    """
    
    def __init__(self):
        """Initialise une nouvelle partie"""
        self.players = []
        self.turn_count = 0
        self.game_over = False
        self.winner = None
        self.history = []
    
    def add_player(self, name, health=None):
        """
        Ajoute un joueur à la partie
        
        Args:
            name (str): Nom du joueur
            health (int, optional): HP initiaux
            
        Returns:
            Character: Le personnage créé
            
        Raises:
            ValueError: Si le nom est invalide
        """
        if not name or not isinstance(name, str):
            raise ValueError("Le nom du joueur doit être une chaîne non vide")
        
        # Vérifier que le nom n'existe pas déjà
        if any(player.name == name for player in self.players):
            raise ValueError(f"Un joueur nommé '{name}' existe déjà")
        
        player = Character(name, health)
        self.players.append(player)
        
        self.history.append({
            'turn': self.turn_count,
            'action': 'player_added',
            'player': name,
            'details': f"{name} rejoint la partie avec {player.health} HP"
        })
        
        return player
    
    def get_player(self, name):
        """
        Récupère un joueur par son nom
        
        Args:
            name (str): Nom du joueur
            
        Returns:
            Character or None: Le joueur trouvé
        """
        return next((player for player in self.players if player.name == name), None)
    
    def get_alive_players(self):
        """Retourne la liste des joueurs vivants"""
        return [player for player in self.players if player.is_alive()]
    
    def get_dead_players(self):
        """Retourne la liste des joueurs morts"""
        return [player for player in self.players if player.is_dead()]
    
    def is_game_over(self):
        """Vérifie si la partie est terminée"""
        alive_players = self.get_alive_players()
        return len(alive_players) <= 1
    
    def get_winner(self):
        """
        Détermine le gagnant de la partie
        
        Returns:
            Character or None: Le gagnant ou None si pas de gagnant
        """
        if not self.is_game_over():
            return None
        
        alive_players = self.get_alive_players()
        return alive_players[0] if alive_players else None
    
    def execute_action(self, player_name, action, target_name=None, amount=None):
        """
        Exécute une action pour un joueur
        
        Args:
            player_name (str): Nom du joueur qui agit
            action (str): Type d'action ('attack', 'defend', 'heal')
            target_name (str, optional): Nom de la cible (pour attack)
            amount (int, optional): Montant (pour heal)
            
        Returns:
            dict: Résultat de l'action
        """
        if self.is_game_over():
            return {
                'success': False,
                'message': 'La partie est terminée',
                'game_over': True
            }
        
        # Trouver le joueur
        player = self.get_player(player_name)
        if not player or player.is_dead():
            return {
                'success': False,
                'message': f'{player_name} ne peut pas agir (mort ou inexistant)'
            }
        
        result = {
            'success': True,
            'turn': self.turn_count + 1,
            'player': player_name,
            'action': action
        }
        
        # Exécuter l'action
        if action == 'attack':
            if not target_name:
                return {'success': False, 'message': 'Cible requise pour attaquer'}
            
            target = self.get_player(target_name)
            if not target:
                return {'success': False, 'message': f'Cible {target_name} introuvable'}
            
            if target.is_dead():
                return {'success': False, 'message': f'{target_name} est déjà mort'}
            
            if target_name == player_name:
                return {'success': False, 'message': 'Impossible de s\'attaquer soi-même'}
            
            old_health = target.health
            attack_success = player.attack(target)
            
            result.update({
                'target': target_name,
                'damage_dealt': old_health - target.health if attack_success else 0,
                'target_health': target.health,
                'target_died': target.is_dead(),
                'attack_success': attack_success
            })
            
        elif action == 'defend':
            player.defend()
            result['message'] = f'{player_name} se met en position défensive'
            
        elif action == 'heal':
            old_health = player.health
            healed = player.heal(amount)
            result.update({
                'health_restored': healed,
                'current_health': player.health,
                'was_at_full_health': old_health == player.max_health
            })
            
        else:
            return {'success': False, 'message': f'Action inconnue: {action}'}
        
        # Incrémenter le compteur de tours
        self.turn_count += 1
        
        # Ajouter à l'historique
        self.history.append(result.copy())
        
        # Vérifier fin de partie
        if self.is_game_over():
            self.game_over = True
            self.winner = self.get_winner()
            result['game_over'] = True
            result['winner'] = self.winner.name if self.winner else None
        
        return result
    
    def get_game_state(self):
        """
        Retourne l'état complet de la partie
        
        Returns:
            dict: État de la partie
        """
        return {
            'turn_count': self.turn_count,
            'total_players': len(self.players),
            'alive_players': len(self.get_alive_players()),
            'dead_players': len(self.get_dead_players()),
            'players': [player.get_status() for player in self.players],
            'game_over': self.is_game_over(),
            'winner': self.get_winner().name if self.get_winner() else None,
            'history_length': len(self.history)
        }
    
    def get_leaderboard(self):
        """
        Retourne le classement des joueurs par HP
        
        Returns:
            list: Joueurs triés par HP décroissant
        """
        return sorted(self.players, key=lambda p: p.health, reverse=True)
