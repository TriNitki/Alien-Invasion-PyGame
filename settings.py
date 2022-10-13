class Settings():
    '''Class to store all settings of Alien Invasion'''

    def __init__(self) -> None:
        '''Settings initialization'''
        # Screen options
        self.screen_width = 1200
        self.screen_hight = 800
        self.bg_color = (21, 28, 56)

        # Ship options
        self.ship_limit = 3

        # Bullet options
        self.bullet_width = 1200
        self.bullet_height = 10
        self.bullet_color = (255,0,255)
        
        # Speedup scale of the game
        self.speedup_scale = 1.15
        # Game score scale
        self.score_scale = 1.5

        self.initialize_dynamic_settings()
    
    def initialize_dynamic_settings(self):
        """Initialize settings, changes game scale"""
        self.ship_speed_factor = 3
        self.bullet_speed_factor = 4
        self.alien_speed_factor = 1.5
        self.fleet_drop_speed_factor = 10

        # Scoring
        self.alien_points = 50
        
        # fleet_direction = 1 means move right; -1 means left
        self.fleet_direction = 1
    
    def increase_speed(self):
        '''Increases speed and score scale settings'''
        self.alien_speed_factor *= self.speedup_scale
        self.fleet_drop_speed_factor *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)