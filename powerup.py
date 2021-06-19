import pygame
import random
from pygame.sprite import Sprite


class PowerUp(Sprite):
    """A class to manage ship bullets"""

    def __init__(self, ai_game):
        """creater a bullet object in the ship's current pos"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = ai_game.settings.bullet_color
        self.powerup_type = random.choice(('ship_speed', 'bullet_size', 'bullet_number', 'shield'))
        # Create a bullet rect at (0,0) and then set correct position
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.midtop = self.screen.midtop
        self.y = float(self.rect.y)

    def give_powerup(self):
        choice = random.randint(75, 100)
        return choice > 75

    def update(self):
        self.y += 0.3
        self.rect.y = self.y

    def draw_powerup(self):
        """draw bullet to the screen"""
        pygame.draw.rect(self.screen, self.color, self.rect)


class Shield(PowerUp):
    def __init__(self, ai_game):
        super().__init__()


