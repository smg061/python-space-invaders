import pygame
import sys
from rocketship_class import Ship
from settings import Settings


class RocketShip:
    def __init__(self):
        """initialize game"""
        pygame.init()
        self.settings = Settings()
        """draw the screen"""
        self.screen = pygame.display.set_mode((720, 480))
        """set the caption"""
        pygame.display.set_caption("Rocket Ship!!")
        self.rocketship = Ship(self)

    def run_game(self):
        """Start the main loop of the game"""
        while True:
            self._check_events()
            self.rocketship.update()
            self._update_screen()

    def _check_events(self):
        """respond to keypresses and mouse events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.rocketship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.rocketship.moving_left = True
        elif event.key == pygame.K_UP:
            self.rocketship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.rocketship.moving_down = True
        elif event.key == pygame.K_q:
            sys.exit()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.rocketship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.rocketship.moving_left = False
        elif event.key == pygame.K_DOWN:
            self.rocketship.moving_down = False
        elif event.key == pygame.K_UP:
            self.rocketship.moving_up = False

    def _update_screen(self):
        """update images on the screen and flit to new screen"""
        # Redraw the screen during each pass through the loop
        self.screen.fill((240, 240, 240))
        self.rocketship.blitme()

        # Make the most recently drawn screen visible
        pygame.display.flip()


if __name__ == '__main__':
    R_ship = RocketShip()
    R_ship.run_game()
