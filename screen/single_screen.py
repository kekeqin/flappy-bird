from screen.base import GameScreen
from asserts import Asserts
from bird import Bird
import pygame

asserts = Asserts()
class SingleScreen(GameScreen):
    def __init__(self, game):
        super().__init__(game)
        
        self.bird = Bird(x = 100, y = 200, p_id = None)
        self.window = self.game.window
        
        asserts.get_audios("bgsound").play(-1)
        
    def _render(self, events, **args):
        
        super()._render(events, **args)
        
        for event in events:
            self.handle_space(event)
        
        self.blit(asserts.get_images("flappy"), (50, 50))
        self.blit(asserts.get_images("floor"), (0, 400))
        self.bird.fixed_draw(self.window)
        
    def handle_space(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                asserts.get_audios("bgsound").stop()
                self.game.screen_update("single_game")