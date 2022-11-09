import pygame
import os
import sys

class Enemy(pygame.sprite.Sprite):
    #enemy comes in from the right side of the screen and moves left
    #it hits the floor and bounces up until it hits the left side of the screen
    #then it dies
    def __init__(self, X=0, Y=0, Xvel=0, Yvel=0):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("gfx/enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (X, Y)
        self.Xvel = Xvel
        self.Yvel = Yvel
        self.onGround = False

        self.angle = 0

        self.HP = 100
    
    def update(self):
        if self.HP <= 0:
            #is dead
            self.kill()
            #spawn a collectable
            #Assets.collectable.Collectable(self.rect.center)

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
        if self.HP <= 0:
            return False
        else:
            return self.rect.colliderect(sprite.rect)