import pygame

class Ground(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("gfx/ground.png")
        self.rect = self.image.get_rect()
        self.rect.center = (320, 470)

    def update(self):
        pass

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def isColliding(self, sprite) -> bool:
        return self.rect.colliderect(sprite.rect)