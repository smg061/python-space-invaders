import pygame


class Ship:
    def __init__(self, Rship):
        self.screen = Rship.screen
        self.screen_rect = Rship.screen.get_rect()
        self.settings = Rship.settings

        # load the ship image and get its rect
        self.image = pygame.image.load('images/rocketship.bmp')
        self.rect = self.image.get_rect()
        self.rect.midleft = self.screen_rect.midleft

        # store a decimal value for the ship's horizontal position
        self.y = float(self.rect.y)

        # Start each new ship at the bottom center of the screen
        self.moving_down = False
        self.moving_up = False

    def blitme(self):
        """Draw the ship at its current location"""
        self.screen.blit(self.image, self.rect)

    def update(self):
        """Update the ship's position based on the movement flag"""
        # update the ship's x value, not the rect
        if self.moving_down and self.rect.bottom < self.settings.screen_height:
            self.y += self.settings.ship_speed

        if self.moving_up and self.rect.top > 0:
            self.y -= self.settings.ship_speed

        # update rec object from rec self
        self.rect.y = self.y
