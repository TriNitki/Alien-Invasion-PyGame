import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    '''Class for one alien'''

    def __init__(self, ai_game) -> None:
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Loades image and creates attribute 'rect'
        self.image = pygame.image.load('alien_invasion/images/alien.bmp')
        self.rect = self.image.get_rect()

        # Each new alien appeares in left top corner of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Stores exact position of the alien
        self.x = float(self.rect.x)

        self.settings.alien_speed = self.settings.alien_speed_factor

    def check_edges(self):
        '''Returnes True if aliens touches a screen border'''
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True
    
    def update(self):
        '''Moves aliens right'''
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = self.x
