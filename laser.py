import pygame # To set up the game


class Laser(pygame.sprite.Sprite):
    def __init__(self, position, speed, screen_height):
        super().__init__()
        self.image = pygame.Surface((4, 15))
        # The laser uses the same yellow colour as the other game elements.
        self.image.fill((243, 216, 63))
        self.rect = self.image.get_rect(center=position)
        self.speed = speed
        self.screen_height = screen_height

    def update(self):
        # Negative speed makes an alien laser move down because of this formula.
        self.rect.y -= self.speed

        if self.rect.y > self.screen_height + 15 or self.rect.y < 0:
            self.kill()
