import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    '''Class for spaceship control'''

    def __init__(self, ai_game, image) -> None:
        '''Ship and starting point initialization'''
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # Importing image of spaceship and getting rectangular
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()

        # Each new ship is spawning at the bottom of the screen
        self.rect.midbottom = self.screen_rect.midbottom

        # Storaging FLOAT coords of the ship
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        # Movement flags
        self.moving_right = False
        self.moving_left = False
        self.moving_top = False
        self.moving_bot = False

        self.settings.ship_speed = self.settings.ship_speed_factor

    def update(self):
        '''Updates the position given the flag'''
        # Updates attribute x
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        if self.moving_top and self.rect.top > self.screen_rect.top:
            self.y -= self.settings.ship_speed
        if self.moving_bot and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.ship_speed

        # Updates atribute rect using self.x
        self.rect.x = self.x
        self.rect.y = self.y

    def center_ship(self):
        '''Sets the ship in a center of the bottom side'''
        self.rect.midbottom = self.screen_rect.midbottom

        # Updates atribute rect using self.x
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
    
    def blitme(self):
        '''Painting ship in current position'''
        self.screen.blit(self.image, self.rect)