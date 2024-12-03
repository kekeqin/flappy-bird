import pygame
from asserts import Asserts

asserts = Asserts()
class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, upwards = True):
        pygame.sprite.Sprite.__init__(self)
        
        self.images = asserts.pipe_images()
        
        if upwards:
            self.image = self.images[0]
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.top = y
            
        else:
            self.image = self.images[1]
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.bottom = y
            
        self.x_vel = -1.01
        
    def update(self):
        self.rect.x += self.x_vel