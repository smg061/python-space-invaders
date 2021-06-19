import pygame.font
from pygame.sprite import Group
from ship import Ship
import json
class Scoreboard:
    """Initialize scorekeeping attributes"""
    def __init__(self, ai_game):
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        # Font settings and color
        self.text_color = (30,30,30)
        self.font = pygame.font.SysFont(None, 48)

        # prepare initial score image
        self.prep_score()
        self.prep_high_score()
        self.prep_ships()

    def prep_score(self):
        score_str = "Score: " + str(self.stats.score)
        self.score_image = self.font.render(score_str, True, self.text_color,self.settings.bg_color)
        # display the score on top of the screen
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20


    def prep_high_score(self):
        high_score = round(self.stats.high_score, -1)
        high_score_str = "High score: {:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.settings.bg_color)
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top


    def prep_ships(self):
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_game)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)

    def check_high_score(self):
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()

    def record_high_score(self):
        f_hand = './high_score.json'
        with open(f_hand, 'w') as f:
            score = self.stats.high_score
            json.dump(score, f)

    def show_score(self):
        """"draw score to screen"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.ships.draw(self.screen)