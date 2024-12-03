import pygame
from screen.base import GameScreen
from bird import Bird
from asserts import Asserts
from client_pipes.singlepipes import SinglePipes
from score import Score
import json


asserts = Asserts()
class SingleGame(GameScreen):
    def __init__(self, game):
        super().__init__(game)
        
        self.bird = Bird(x = 60, y = 150, p_id = None)
        
        self.window = self.game.window
        
        self.dead = False
        
        self.floor_image = asserts.get_images("floor")
        self.floor_x = 0
        
        self.pipes = SinglePipes()
        self.pipes.init_pipes()
        
        self.score = Score()
        self.current_score = 0
        
    def _render(self, events, **args):
        self.handle_events(events)
    
        if not self.dead:   
            self.pipes.update_pipes()          
            self.pipes.draw_and_update(self.window)
            self.blit(self.floor_image, (0, 400))
            self.update_floor()
            self.bird.move()
            self.bird.draw(self.window)
            self.dead = self.bird.check_collision(self.pipes.pipes)
            
            if self.bird.bird_score(self.pipes.pipes):       
                self.score.update(1)
                self.current_score += 1
            # if self.current_score > self.score.highscore:
            self.score.save_highscore(self.current_score)
            self.score.render_score(self.window)    
            
        else:
            self.game.screen_update("game_over")
        
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.bird.jump()


    def get_final_score(self):
        return self.current_score
        
    def update_floor(self):
        self.floor_x -= 1
        if self.floor_x <= - (self.floor_image.get_width() - 288):
            self.floor_x = 0
        self.window.blit(self.floor_image, (self.floor_x, 400))