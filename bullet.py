import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    '''Class for controlling bullets fired by a ship'''

    def __init__(self, ai_game):
        '''Creates object bullet in a current position'''
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        # Creates bullet in position (0, 0) and assigned position
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop

        # Bullet position stores in FLOAT
        self.y = float(self.rect.y)

        self.settings.bullet_speed = self.settings.bullet_speed_factor
    
    def update(self):
        '''Moves bullet up the screen'''
        # Updates bullet position in FLOAT
        self.y -= self.settings.bullet_speed
        # Updates RECT position
        self.rect.y = self.y

    def draw_bullet(self):
        '''Launching a bullet on the screen'''
        pygame.draw.rect(self.screen, self.color, self.rect)

