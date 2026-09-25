import pygame, random # Pygame for the game to work and random for randomising numbers


class Alien(pygame.sprite.Sprite):
    def __init__(self, type, x, y, speed_getter):
        super().__init__()
        # The type decides which alien image is loaded.
        self.type = type
        self.speed_getter = speed_getter

        path = f"Graphics/alien_{type}.png"
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, direction):
        # The Game object supplies the current level-based speed.
        self.rect.x += round(direction * self.speed_getter())


class MysteryShip(pygame.sprite.Sprite):
    def __init__(self, screen_width, offset):
        super().__init__()
        self.screen_width = screen_width
        self.offset = offset

        self.image = pygame.image.load("Graphics/mystery.png")
        # Start the mystery ship from either side at random.
        x = random.choice([
            self.offset / 2,
            screen_width + self.offset - self.image.get_width(),
        ])

        if x == self.offset / 2:
            self.speed = 3
        else:
            self.speed = -3

        self.rect = self.image.get_rect(topleft=(x, 90))

    def update(self):
        self.rect.x += self.speed

        # Remove the mystery ship once it has left the play area.
        if self.rect.right > self.screen_width + self.offset / 2:
            self.kill()
        elif self.rect.left < self.offset / 2:
            self.kill()
