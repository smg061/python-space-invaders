class Settings:
    """A class to store settings for Alien Invasion"""
    def __init__(self):
        """initialize game settings"""
        # screen settings
        self.screen_width = 1080
        self.screen_height = 720
        self.bg_color = (230,230,230)
        # Ship settings
        self.ship_speed = 1.5
        self.ship_limit = 3
        # Bullet settings
        self.bullet_speed = 2.0
        self.bullet_width = 10
        self.bullet_height = 15
        self.bullet_color = (60,60,60)
        self.bullets_allowed = 3
        # alien settings
        self.alien_speed = 1.0
        self.fleet_drop_speed = 10
        # fleet direction of 1 is right, -1 is left
        self.fleet_direction = 1
        self.alien_points = 50
        self.score_scale = 1.5
        self.round_number = 0


    def reset_speed_settings(self):
        self.fleet_drop_speed = 10
        self.bullet_speed = 2.0
        self.alien_speed = 1.0




