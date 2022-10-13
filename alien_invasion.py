import sys

import pygame
import json

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from scoreboard import Scoreboard
from botton import Botton

from time import sleep

class AlienInvasion:
    '''Class for game resource control'''

    def __init__(self) -> None:
        '''Game initialization'''

        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_hight))
        pygame.display.set_caption('Zalupa Online')

        self.clock = pygame.time.Clock()

        # Image paths
        self.ship_link = 'alien_invasion/images/ship.bmp'
        self.small_ship_link = 'alien_invasion/images/small_ship.bmp'

        # High score file path
        self.hs_filename = 'alien_invasion/record.json'

        # Creates instance for stats and result panel storaging
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self, self.ship_link)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        # Creates Play botton
        self.play_botton = Botton(self, 'Play', -0.5, (0, 255, 0))
        self.hard_botton = Botton(self, 'Hard', 1, (255, 0, 0))
        self.medium_botton = Botton(self, 'Medium', 2, (255, 164, 0))
        self.easy_botton = Botton(self, 'Easy', 3, (0, 255, 0))


    '''Run game functions'''
    def run_game(self):
        '''Running the main game loop'''

        while True:
            self._check_events()

            # Checks if the game is active
            if self.stats.game_active:
                self.ship.update()
                self._update_aliens()
                self._update_bullets()
                self._update_framerate()

            self._update_screen()
    
    '''Imput events functions'''
    def _check_events(self):
        '''Mouse and keyboard tracking'''

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit_game()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_botton(mouse_pos)
    
    def _check_keydown_events(self, event):
        '''Checks for KEYDOWN events'''

        if event.key == pygame.K_d:
            self.ship.moving_right = True
        elif event.key == pygame.K_a:
            self.ship.moving_left = True
        elif event.key == pygame.K_w:
            self.ship.moving_top = True
        elif event.key == pygame.K_s:
            self.ship.moving_bot = True
        
        elif event.key == pygame.K_p:
            if not self.stats.game_active:
                self._continue_game()

        elif event.key == pygame.K_SPACE and self.stats.game_active == True:
            self._fire_bullet()

        elif event.key == pygame.K_ESCAPE:
            self.exit_game()

    def _check_keyup_events(self, event):
        '''Checks for KEYUP events'''

        if event.key == pygame.K_d:
            self.ship.moving_right = False
        elif event.key == pygame.K_a:
            self.ship.moving_left = False
        elif event.key == pygame.K_w:
            self.ship.moving_top = False
        elif event.key == pygame.K_s:
            self.ship.moving_bot = False

    '''Aliens functions'''
    def _create_alien(self, alien_number, row_number):

        # Creates an alien and set him in the row
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)
    
    def _update_aliens(self):
        '''Updates position of all aliens in a fleet'''
        self.aliens.update()
        self._check_fleet_edges()
        
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        
        # Сhecks if they have moved to the bot edge of the screen
        self._check_aliens_bottom()
    
    '''Fleet functions'''
    def _create_fleet(self):
        '''Creates enemys fleet'''
        # Creates an alien and calculates amount of aliens in a linr
        # The interval between neighboring aliens is equal to the width of the alien
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = round(available_space_x / (2 * alien_width))

        # Defines amount of lines
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_hight - (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        # Creates fleet
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _check_fleet_edges(self):
        '''Reacts on edge of the dcreen touching'''
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    
    def _change_fleet_direction(self):
        
        '''Lowers the fleet and changes direction'''
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed_factor
        self.settings.fleet_direction *= -1

    '''Bullets functions'''
    def _fire_bullet(self):
        '''Creates new bullet and includes in a group "bullets" '''

        new_bullet = Bullet(self)
        self.bullets.add(new_bullet)

    def _update_bullets(self):
        self.bullets.update()

        # Delites bullets, which are out of screen
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        
        self._check_bullet_alien_collosions()

    '''Collision functions'''
    def _ship_hit(self):
        """Process collisions of ship with an alien"""
        if self.stats.ships_left > 0:
            # Decreases ships_left and updates score board
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            # Clear lists of aliens and bullets
            self.aliens.empty()
            self.bullets.empty()

            # Creates new fleet and placec ship in the center
            self.ship.center_ship()
            self._create_fleet()

            # Pouse
            sleep(0.2)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)
    
    def _check_bullet_alien_collosions(self):
        '''Processes collisions of bullets with aliens'''
        # If detectes hit, deletes bullet and alien
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
                self.sb.prep_score()
        
        if not self.aliens:
            # Creates new fleet, if there is no any aliens
            self.ship.center_ship()
            self._create_fleet()
            self.bullets.empty()
            self.settings.increase_speed()

            # Increases level
            self.stats.level += 1
            self.sb.prep_level()
    
    def _check_aliens_bottom(self):
        '''Сhecks if they have moved to the bot edge of the screen'''
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                '''Gets hit'''
                self._ship_hit()
                break

    '''Botton functions'''
    def _check_play_botton(self, mouse_pos):
        '''Starts new game if botton Play is pressed'''
        play_botton_clicked = self.play_botton.rect.collidepoint(mouse_pos)
        hard_botton_clicked = self.hard_botton.rect.collidepoint(mouse_pos)
        medium_botton_clicked = self.medium_botton.rect.collidepoint(mouse_pos)
        easy_botton_clicked = self.easy_botton.rect.collidepoint(mouse_pos)

        if play_botton_clicked and not self.stats.game_active:
            self.play_botton.draw_border()
            pygame.display.flip()
            sleep(0.5)
            self._continue_game()
        
        elif hard_botton_clicked and not self.stats.game_active:
            self.settings.speedup_scale = 1.25
        elif medium_botton_clicked and not self.stats.game_active:
            self.settings.speedup_scale = 1.15
        elif easy_botton_clicked and not self.stats.game_active:
            self.settings.speedup_scale = 1.05

    def _draw_bottons(self):
        # Play botton is active only if the game in inactive
        if not self.stats.game_active:
            self.play_botton.draw_botton()
            self.hard_botton.draw_botton()
            self.medium_botton.draw_botton()
            self.easy_botton.draw_botton()

            # Drawes border depends of speedup_scale
            if self.settings.speedup_scale == 1.25:
                self.hard_botton.draw_border()
            elif self.settings.speedup_scale == 1.15:
                self.medium_botton.draw_border()
            elif self.settings.speedup_scale == 1.05:
                self.easy_botton.draw_border()
    '''Game update functions'''
    def _update_framerate(self):
        '''Updates game framerate'''
        self.framerate = self.clock.tick(120)

    def _continue_game(self):
        # Resets game settings
        self.settings.initialize_dynamic_settings()

        # Resets game stats
        self.stats.game_active = True
        self.sb.check_high_score()
        self.stats.reset_stats()
        self.sb.prep_score()
        self.sb.prep_level()
        self.sb.prep_ships()

        # Wipes lists of aliens and bullets
        self.aliens.empty()
        self.bullets.empty()

        # Creates new fleet and places ship in the center
        self._create_fleet()
        self.ship.center_ship()

        # Mouse hides
        pygame.mouse.set_visible(False)
    
    def _update_screen(self):
        '''Updating screen and displaying new BG color'''
        
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        
        self.aliens.draw(self.screen)

        # Outputs information about score
        self.sb.show_score()

        self._draw_bottons()

        # Displaying of the last rendered screen
        pygame.display.flip()

    def exit_game(self):
        '''Exits the game'''
        # Saves high score in a file
        with open(self.hs_filename, 'w') as f:
            json.dump(self.stats.high_score, f)
        sys.exit()
    

if __name__ == '__main__':
    # Instantiation and starting the game
    ai = AlienInvasion()
    ai.run_game()