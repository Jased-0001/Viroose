import pygame

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, screen):
        super().__init__()
        self.image = pygame.image.load("gfx/bullet.png")
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction
        self.speed = 10

        screen.blit(self.image, self.rect)