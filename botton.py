import pygame.font

class Botton():

    def __init__(self, ai_game, msg, coord, bot_color) -> None:
        '''Initialize attributes of bottom'''
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.coord = coord

        # Set bottom size and properties
        self.width, self.height = 200, 50
        self.bottom_color = bot_color
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        # Creates object rect of bottom and align to the center of screen
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = (self.screen_rect.center[0], self.screen_rect.center[1] + self.coord * 1.5 * self.height)

        # Botton messages creates only one time
        self._prep_msg(msg)
    
    def _prep_msg(self, msg):
        '''Transforms msg in rectangular and align text to the center'''
        self.msg_image = self.font.render(msg, True, self.text_color, self.bottom_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center
    
    def draw_botton(self):
        '''Drawes blanck botton and display a message'''
        self.screen.fill(self.bottom_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
    
    def draw_border(self):
        self.rect_border_top = pygame.Rect(0, 0, self.width + 20, self.height - 45)
        self.rect_border_top.center = (self.screen_rect.center[0], self.rect.top - 10)

        self.rect_border_bot = pygame.Rect(0, 0, self.width + 20, self.height - 45)
        self.rect_border_bot.center = (self.screen_rect.center[0], self.rect.bottom + 10 )

        self.rect_border_left = pygame.Rect(0, 0, self.width - 195, self.height + 25)
        self.rect_border_left.center = (self.rect.left - 10 , self.rect.center[1])

        self.rect_border_right = pygame.Rect(0, 0, self.width - 195, self.height + 25)
        self.rect_border_right.center = (self.rect.right + 10, self.rect.center[1])

        self.screen.fill(self.bottom_color, self.rect_border_top)
        self.screen.fill(self.bottom_color, self.rect_border_bot)
        self.screen.fill(self.bottom_color, self.rect_border_left)
        self.screen.fill(self.bottom_color, self.rect_border_right)