import pygame
import random

import Assets.bullet

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("gfx/Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (110, 240)
        self.Yvel = 0
        self.Xvel = 0
        self.onGround = False

        self.angle = 0

        self.HP = 100

    def update(self):
        if self.HP <= 0:
            self.kill()

        #calculate gravity
        if self.Yvel < pygame.display.get_surface().get_height() / 2 and self.onGround == False:
            self.Yvel += 0.1
            self.rect.y += self.Yvel

        #calculate movement
        #if touching left side of screen
        if self.rect.x <= 0:
            self.Xvel *= -1
        #if touching right side of screen
        if self.rect.x >= pygame.display.get_surface().get_width() - self.rect.width:
            self.Xvel *= -1

        #if touching top of screen
        if self.rect.y <= 0:
            self.Yvel *= -1
        if self.rect.y == 475 or self.rect.y >= 475:
            self.Yvel *= -1

        self.rect.x += self.Xvel

        #decaying movement
        if self.Xvel > 0:
            self.Xvel -= 0.1
        elif self.Xvel < 0:
            self.Xvel += 0.1

        #prevent movement from being too small
        if self.Xvel < 0.1 and self.Xvel > -0.1:
            self.Xvel = 0

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def isColliding(self, sprite) -> bool:
        return self.rect.colliderect(sprite.rect)

    def jump(self, doRanMovement):
        if self.onGround:
            if doRanMovement: self.Yvel = random.randint(-6, -4)
            else: self.Yvel = -5
            self.onGround = False
            self.rect.y -= 8
        else:
            if doRanMovement: self.Yvel = random.randint(-3, -2)
            else: self.Yvel = -3


    def fall(self, doRanMovement):
        if self.onGround:
            pass
        else:
            if doRanMovement: self.Yvel = random.randint(6, 4)
            else: self.Yvel = 5