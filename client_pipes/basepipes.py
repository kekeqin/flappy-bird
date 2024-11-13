import pygame

class BasePipes:
    def __init__(self):
        self.pipes = pygame.sprite.Group()
        
    def init_pipes(self):
        raise NotImplementedError
    
    def update_pipes(self):
        raise NotImplementedError
    
    def draw_and_update(self, window):
        self.pipes.draw(window)
        self.pipes.update()