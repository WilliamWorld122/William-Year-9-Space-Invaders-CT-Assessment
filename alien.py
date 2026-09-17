import pygame  # Inherits Sprite base class and handles image surface loading
import random  # Randomizes left or right screen entry point for MysteryShip


class Alien(pygame.sprite.Sprite):
    def __init__(self, type, x, y):
        # Load enemy graphic variant based on tier and set its position
        super().__init__()
        self.type = type
        path = f"Graphics/alien_{type}.png"
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, direction):
        # Shift alien position horizontally according to fleet direction vector
        self.rect.x += direction


class MysteryShip(pygame.sprite.Sprite):
    def __init__(self, screen_width, offset):
        # Randomly spawn bonus ship at left or right screen edge with set speed direction
        super().__init__()
        self.screen_width = screen_width
        self.offset = offset
        self.image = pygame.image.load("Graphics/mystery.png")
        x = random.choice([self.offset / 2, screen_width + self.offset - self.image.get_width()])

        if x == self.offset / 2:
            self.speed = 3
        else:
            self.speed = -3

        self.rect = self.image.get_rect(topleft=(x, 90))

    def update(self):
        # Move ship sideways across screen and despawn once it exits play boundaries
        self.rect.x += self.speed
        if self.rect.right > self.screen_width + self.offset / 2:
            self.kill()
        elif self.rect.left < self.offset / 2:
            self.kill()
