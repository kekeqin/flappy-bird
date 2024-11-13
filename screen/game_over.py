from screen.base import GameScreen
from asserts import Asserts
from bird import Bird
import pygame
from score import Score


asserts = Asserts()
class GameOverScreen(GameScreen):
    def __init__(self, game, final_score):
        super().__init__(game)
        
        self.bird = Bird(x = 60, y = 370, p_id = None)
        
        self.window = self.game.window
        
        self.score = Score()
        
        self.final_score = final_score
        
    def _render(self, events, **args):
        
        super()._render(events, **args)
        
        for event in events:
            self.handle_click(event)
        
        self.blit(asserts.get_images("gameover"), (50, 20))
        self.blit(asserts.get_images("floor"), (0, 400))
        self.blit(asserts.get_images("grade"), (26, 140))
        self.blit(asserts.get_images("key"), (85, 280))
        
        self.bird.draw(self.window)
        
        self.score.set_score(self.final_score)
        self.score.render_score(self.window)
        
        if self.final_score < 5:
            medal = asserts.get_images("white")
        elif self.final_score < 10:
            medal = asserts.get_images("silver")
        elif self.final_score < 10:
            medal = asserts.get_images("bronze")
        else:
            medal = asserts.get_images("gold")
            
        self.blit(medal, (60, 185))
        self.score.show_highscore(self.window, self.final_score)
        self.score.show_score(self.window)
                      
    def handle_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if 85 < event.pos[0] < 200 and 280 < event.pos[1] < 350:
                self.game.screen_update("home")