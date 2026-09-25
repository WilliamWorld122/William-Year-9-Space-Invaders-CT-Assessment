import pygame, random # Pygame to set the game, random to randomise numbers
from spaceship import Spaceship # To access the spaceship or player
from obstacle import Obstacle # Get the obstacle
from obstacle import grid # Get the grid
from alien import Alien # Get the aliens or enemies
from laser import Laser # Get the laser
from alien import MysteryShip # Get the mysteryship


class Game:
    def __init__(self, screen_width, screen_height, offset):
        # Initialise game class
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.offset = offset
        self.collision = True
        self.spaceship_group = pygame.sprite.GroupSingle()
        # Pass Game into the spaceship so it can read level settings.
        self.spaceship_group.add(
            Spaceship(self.screen_width, self.screen_height, self.offset, self)
        )

        self.obstacles = self.create_obstacles()
        self.aliens_group = pygame.sprite.Group()

        # Level starts at 1 and ends at level 3.
        self.level = 1
        self.max_level = 3

        # Each level has a starting speed and a maximum speed.
        # As aliens are destroyed, the current speed rises toward the cap.
        self.level_settings = {
            1: {
                "alien_speed": 1.0,
                "alien_speed_cap": 2.0,
                "laser_speed": 4.0,
                "laser_speed_cap": 5.0,
            },
            2: {
                "alien_speed": 1.5,
                "alien_speed_cap": 2.5,
                "laser_speed": 5.0,
                "laser_speed_cap": 7.0,
            },
            3: {
                "alien_speed": 2.0,
                "alien_speed_cap": 3.0,
                "laser_speed": 6.0,
                "laser_speed_cap": 9.0,
            },
        }

        self.aliens_direction = 1
        self.alien_lasers_group = pygame.sprite.Group()
        self.mystery_ship_group = pygame.sprite.GroupSingle()

        self.lives = 3
        self.run = True
        self.score = 0
        self.highscore = 0
        self.load_highscore()

        pygame.mixer.music.load("Sounds/music.ogg")
        pygame.mixer.music.play(-1)
        self.explosion_sound = pygame.mixer.Sound("Sounds/explosion.ogg")

        self.create_aliens()

    def get_level_settings(self):
        # Return the settings belonging to the current level.
        return self.level_settings[self.level]

    def get_speed_multiplier(self):
        """Return 0..1 depending on how many aliens have been destroyed."""
        starting_aliens = 55
        remaining_aliens = len(self.aliens_group)
        # More destroyed aliens means more speed within the current level.
        destroyed = starting_aliens - remaining_aliens
        return min(1.0, max(0.0, destroyed / starting_aliens))

    def get_alien_speed(self):
        settings = self.get_level_settings()
        progress = self.get_speed_multiplier()
        # Interpolate from the level's starting speed to its cap.
        return settings["alien_speed"] + (
            settings["alien_speed_cap"] - settings["alien_speed"]
        ) * progress

    def get_laser_speed(self):
        settings = self.get_level_settings()
        progress = self.get_speed_multiplier()
        return settings["laser_speed"] + (
            settings["laser_speed_cap"] - settings["laser_speed"]
        ) * progress

    def create_obstacles(self):
        obstacle_width = len(grid[0]) * 3
        gap = (self.screen_width - (4 * obstacle_width)) / 5
        obstacles = []

        # Four defensive obstacles are placed across the screen.
        for i in range(4):
            offset_x = (i + 1) * gap + i * obstacle_width
            obstacle = Obstacle(offset_x, self.screen_height - 100)
            obstacles.append(obstacle)

        return obstacles

    def create_aliens(self):
        for row in range(5):
            for column in range(11):
                x = 75 + column * 55
                y = 110 + row * 55

                # Level 1 = type 1, level 2 = type 2, level 3 = type 3.
                alien_type = self.level

                alien = Alien(
                    alien_type,
                    x + self.offset / 2,
                    y,
                    self.get_alien_speed,
                )
                self.aliens_group.add(alien)

    def move_aliens(self):
        # Every alien reads the current level-based speed when updating.
        self.aliens_group.update(self.aliens_direction)

        alien_sprites = self.aliens_group.sprites()

        for alien in alien_sprites:
            if alien.rect.right >= self.screen_width + self.offset / 2:
                self.aliens_direction = -1
                self.alien_move_down(2)
                break
            elif alien.rect.left <= self.offset / 2:
                self.aliens_direction = 1
                self.alien_move_down(2)
                break

    def alien_move_down(self, distance):
        if self.aliens_group:
            for alien in self.aliens_group.sprites():
                alien.rect.y += distance

    def alien_shoot_laser(self):
        if self.aliens_group.sprites():
            random_alien = random.choice(self.aliens_group.sprites())
            # Negative speed makes this laser travel downward in Laser.update().
            laser_sprite = Laser(
                random_alien.rect.center,
                -self.get_laser_speed(),
                self.screen_height,
            )
            self.alien_lasers_group.add(laser_sprite)

    def create_mystery_ship(self):
        self.mystery_ship_group.add(MysteryShip(self.screen_width, self.offset))

    def check_for_collisions(self):
        # Checks for collisions between the player's laser and alien
        if self.spaceship_group.sprite.lasers_group:
            for laser_sprite in self.spaceship_group.sprite.lasers_group:
                aliens_hit = pygame.sprite.spritecollide(
                    laser_sprite, self.aliens_group, True
                )
                # Demonstrates what will happen if the alien is hit

                if aliens_hit:
                    self.explosion_sound.play()
                    for alien in aliens_hit:
                        self.score += alien.type * 100
                        self.check_for_highscore()
                        laser_sprite.kill()

                if pygame.sprite.spritecollide(
                    laser_sprite, self.mystery_ship_group, True
                ):
                    self.collision = True
                    self.explosion_sound.play()
                    self.score += 500
                    self.check_for_highscore()
                    laser_sprite.kill()

                for obstacle in self.obstacles:
                    if pygame.sprite.spritecollide(
                        laser_sprite, obstacle.blocks_group, True
                    ):
                        laser_sprite.kill()
        # Checks if alien laser hits player
        if self.alien_lasers_group:
            
            for laser_sprite in self.alien_lasers_group:
                
                if pygame.sprite.spritecollide(
                    laser_sprite, self.spaceship_group, False
                ):
                    laser_sprite.kill()
                   # Player loses a life
                    self.lives -= 1
                    

                    if self.lives == 0:
                        self.game_over()

                for obstacle in self.obstacles:
                    if pygame.sprite.spritecollide(
                        laser_sprite, obstacle.blocks_group, True
                    ):
                        laser_sprite.kill()
        # Collision tracking alien and obstacle
        if self.aliens_group:
            for alien in self.aliens_group:
                for obstacle in self.obstacles:
                    pygame.sprite.spritecollide(
                        alien, obstacle.blocks_group, True
                    )

                if pygame.sprite.spritecollide(
                    alien, self.spaceship_group, False
                ):
                    self.game_over()

        # When every alien is destroyed, move to the next level.
        if not self.aliens_group and self.run and self.collision:
            self.advance_level()

    def advance_level(self):
        # Increases level by 1
        if self.level < self.max_level:
            self.level += 1
        else:
            # Stay at level 3 after reaching the final level.
            self.level = self.max_level

        self.aliens_group.empty()
        self.alien_lasers_group.empty()
        self.mystery_ship_group.empty()
        self.aliens_direction = 1
        self.obstacles = self.create_obstacles()
        self.create_aliens()

    def game_over(self):
        self.run = False
        self.collision = False
    def reset(self):
        self.run = True
        # Restarting always returns the player to level 1.
        self.level = 1
        self.lives = 3
        self.spaceship_group.sprite.reset()
        self.aliens_group.empty()
        self.alien_lasers_group.empty()
        self.mystery_ship_group.empty()
        self.aliens_direction = 1
        self.create_aliens()
        
    def check_for_highscore(self):
        # Check if the current score is higher than the saved highscore
        if self.score > self.highscore:
            self.highscore = self.score

        # Open the highscore file and save the new score
        with open("highscore.txt", "w") as file:
            file.write(str(self.highscore))


    def load_highscore(self):
        # Try to load the highscore from the file
        try:
            with open("highscore.txt", "r") as file:
              self.highscore = int(file.read())

        # If the file doesn't exist, start with a highscore of 0
        except FileNotFoundError:
            self.highscore = 0
