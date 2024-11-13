import pygame
from screen.base import GameScreen
from asserts import Asserts
from bird import Bird

asserts = Asserts()
class HomeScreen(GameScreen):
    def __init__(self, game):
        super().__init__(game)
        
        
        self.bird = Bird(x = 120, y = 120, p_id = None)
        self.window = self.game.window
        
        
    def _render(self, events, **args):
        
        super()._render(events, **args)
        
        
        
        for event in events:
            self.handle_mouse_click(event)
            
        self.blit(asserts.get_images("flappy"), (50, 50))
        self.blit(asserts.get_images("floor"), (0, 400))
        self.blit(asserts.get_images("single"), (65, 200))
        self.blit(asserts.get_images("multiplayer"), (65, 300))
        self.bird.fixed_draw(self.window)
        
                
    def handle_mouse_click(self, event): 
        if event.type == pygame.MOUSEBUTTONDOWN:
            if 65 < event.pos[0] < 200 and 200 < event.pos[1] < 260:
                self.game.screen_update("single")
            elif 65 < event.pos[0] < 200 and 300 < event.pos[1] < 360:
                self.game.screen_update("multi")       