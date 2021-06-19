import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """A class to manage ship bullets"""
    def __init__(self, ai_game):
        """creater a bullet object in the ship's current pos"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = ai_game.settings.bullet_color

        # Create a bullet rect at (0,0) and then set correct position
        self.rect = pygame.Rect(0,0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop
        self.y = float(self.rect.y)

    def update(self):
        self.y -= self.settings.bullet_speed
        self.rect.y = self.y

    def draw_bullet(self):
        """draw bullet to the screen"""
        pygame.draw.rect(self.screen, self.color, self. rect)

    def update_alien_bullet(self):
        self.y += self.settings.bullet_speed
        self.rect.y = self.y
