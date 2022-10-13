import json

class GameStats():
    '''Tracks statistics for the Alien Invasion game'''

    def __init__(self, ai_game) -> None:
        '''Initializes statistics'''
        self.settings = ai_game.settings
        self.reset_stats()
        # The game AI starts with active state
        self.game_active = False
        # Record can't be reseted
        with open(ai_game.hs_filename) as f:
            self.high_score = json.load(f)
    
    def reset_stats(self):
        '''Initializes statistics that change during the game'''
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1