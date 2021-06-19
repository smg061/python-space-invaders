import pygame
import random
from pygame.sprite import Sprite


class AlienBullet(Sprite):
    """A class to manage ship bullets"""
    def __init__(self, ai_game, alien):
        """creater a bullet object in the ship's current pos"""
        super().__init__()
        self.screen = ai_game.screen
        self.alien = alien
        self.settings = ai_game.settings
        self.color = ai_game.settings.bullet_color
        self.round_num = ai_game.round_number

        # Create a bullet rect at (0,0) and then set correct position
        self.rect = pygame.Rect(0,0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.midbottom = self.alien.rect.midbottom
        self.y = float(self.rect.y)

    def bullet_decision(self):
        num = random.randint(0, 100)
        return num > 95

    def draw_bullet(self):
        if self.bullet_decision():
            """draw bullet to the screen"""
            pygame.draw.rect(self.screen, self.color, self.rect)

    def update_alien_bullet(self):
        self.y += self.settings.bullet_speed
        self.rect.y = self.y
