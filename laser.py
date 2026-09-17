import pygame  # Inherits Sprite base class and builds dynamic Surface projectile rectangles

class Laser(pygame.sprite.Sprite):
    def __init__(self, position, speed, screen_height):
        # Create a yellow laser surface sprite and position it on screen
        super().__init__()
        self.image = pygame.Surface((4, 15))
        self.image.fill((243, 216, 63))
        self.rect = self.image.get_rect(center=position)
        self.speed = speed
        self.screen_height = screen_height

    def update(self):
        # Move projectile along y-axis and remove when out of vertical screen bounds
        self.rect.y -= self.speed
        if self.rect.y > self.screen_height + 15 or self.rect.y < 0:
            self.kill()
