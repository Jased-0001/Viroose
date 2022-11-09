import pygame

class Button(pygame.sprite.Sprite):
    def __init__(self,text="None",xy =(0,0),width=150,height=75,image="gfx/bttn.png",text_color=(0,0,0),text_size=16,action=lambda: print("None")):
        pygame.sprite.Sprite.__init__(self)
        #make button
        #get image
        self.image = pygame.image.load(image)

        self.rect = self.image.get_rect()
        self.rect.center = (xy[0], xy[1])
        #make text
        self.font = pygame.font.SysFont("Verdana", text_size)
        self.text_surface = self.font.render(text, True, text_color)
        self.text_rect = self.text_surface.get_rect()
        self.text_rect.center = (width/2, height/2)
        self.text = text

        #add text to button
        self.image.blit(self.text_surface, self.text_rect)

        #add action
        self.action = action

    def update(self):
        pass

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        screen.blit(self.text_surface, self.text_rect)

    def isColliding(self, sprite) -> bool:
        return self.rect.colliderect(sprite.rect)

    def doAction(self):
        self.action()