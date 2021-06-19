import json
class GameStats:
    """Track stats with for Alien Invasion"""
    def __init__(self, ai_game):
        """Initialize stats"""
        self.settings = ai_game.settings
        # start AI in active state
        self.game_active = False
        self.round_number = 0
        self.score = 0
        self.high_score = self.load_high_score()
        self.reset_stats()
        self.load_high_score()

    def reset_stats(self):
        """Initialize stats that can change during the game"""
        self.ships_left = self.settings.ship_limit
        self.round_number = 0
        self.score = 0

    def load_high_score(self):
        f_hand = 'high_score.json'
        with open(f_hand, 'r') as f:
            high_score = json.load(f)

        return high_score

