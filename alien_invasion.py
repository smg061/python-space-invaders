import sys
import pygame
from bullet import Bullet
from settings import Settings
from ship import Ship
from alien import Alien
from alien_bullet import AlienBullet
from time import sleep
from button import Button
from game_stats import GameStats
from scoreboard import Scoreboard


class AlienInvasion:
    def __init__(self):
        """Initialize game, and create game resources"""
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invaders! ")
        self.ship = Ship(self)
        self.stats = GameStats(self)
        # the group class stores the bullets and draws them to the screen
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.alien_bullets = pygame.sprite.Group()
        self._create_fleet()
        # make the play button
        self.play_button = Button(self, "Play!")
        self.sb = Scoreboard(self)
        self.round_number = 0


    def run_game(self):
        """Start the main loop of the game"""
        while True:
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            self._update_screen()

    def _check_events(self):
        """respond to keypresses and mouse events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.sb.record_high_score()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_p and not self.stats.game_active:
            self._start_game()
        elif event.key == pygame.K_m:
            choice = 'n'
            while choice != 'm':
                choice = input("Type 'm' to continue: ")
                sleep(1)
        elif event.key == pygame.K_q:
            print("Ending game!")
            sys.exit()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False
        elif event.key == pygame.K_UP:
            self.ship.moving_up = False

    def _check_play_button(self, mouse_pos):
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self._start_game()

    def _start_game(self):
        # hide the cursor
        pygame.mouse.set_visible(False)
        # rest the game stats
        self.stats.reset_stats()
        self.settings.reset_speed_settings()
        self.stats.game_active = True
        self.sb.prep_score()
        # get rid of any remaining alines and bullets
        self.aliens.empty()
        self.bullets.empty()

        # create new fleet
        self._create_fleet()
        self.ship.center_ship()
        self.round_number = 0

    def _fire_bullet(self):
        if len(self.bullets) < self.settings.bullets_allowed and self.stats.game_active:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        # update bullet position
        self.bullets.update()
        # get rid of offscreen bullets
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        # check for any bullets that hit aliens and remove them
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if collisions:
            for aliens in collisions.values():
                self.stats.score += int(self.settings.alien_points * len(aliens) * (self.round_number + 0.5))
            self.sb.prep_score()
            self.sb.check_high_score()
        if not self.aliens:
            # destroy bullets and create new fleet
            self.bullets.empty()
            self._create_fleet()
            self.round_number += 1
            self.settings.alien_speed += (self.round_number * 0.25 )
            self.settings.bullet_speed += (self.round_number * 0.25 )


    def _create_fleet(self):
        """Create alien fleet"""
        # make an alien and find the number of alines in a row
        # spacing between aliens is one alien width
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        ship_height = self.ship.rect.height
        available_space_x = self.settings.screen_width - (2 * alien_width)
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        # since we're placing the space of one alien between aliens, you divide the available space
        # by twice the width of an alie
        number_aliens_x = available_space_x // (2 * alien_width)

        # create the first row of aliens:
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """Create an alien and place it in the row"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + (2 * alien_width * alien_number)
        alien.y = alien.rect.height + (2 * alien.rect.height * row_number)
        alien.rect.x = alien.x
        alien.rect.y = alien.y
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """Respond appropiately if any aliens have reached the edge"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_aliens(self):
        self._check_fleet_edges()
        self.aliens.update()
        # look for alien-ship collisions
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        self._check_aliens_bottom()

    def _check_aliens_bottom(self):
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

    def _ship_hit(self):
        """respond to the ship being hit by an alien"""
        if self.stats.ships_left > 0:
            # decrement ships_left
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            # get tid of any remaining alines and bullets
            self.aliens.empty()
            self.bullets.empty()
            self._create_fleet()
            self.ship.center_ship()
            # Pause
            sleep(0.5)

        else:
            self.stats.game_active = False
            self.settings.reset_speed_settings()
            pygame.mouse.set_visible(True)
            self.round_number = 0

    def _update_screen(self):
        """update images on the screen and flit to new screen"""
        # Redraw the screen during each pass through the loop
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        self.sb.show_score()
        if not self.stats.game_active:
            self.play_button.draw_button()
        # Make the most recently drawn screen visible
        pygame.display.flip()


if __name__ == '__main__':
    # Make instance and run the game
    ai = AlienInvasion()
    ai.run_game()
