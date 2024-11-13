import pygame
from asserts import Asserts
import json


W = 288
H = 512

asserts = Asserts()
class Score:
    def __init__(self):
        self.score = 0
        self.highscore = self._load_highscore()
    
    def update(self, increment):
        self.score += increment
    
    def render_score(self, game):
        str_score = str(self.score)
        n = len(str_score)
        w = asserts.get_images("0").get_width() * 1.1
        x = (W - n * w) / 2
        y = H * 0.15
        for number in str_score:
            game.blit(asserts.get_images(number), (x, y))
            x += w
    
    def set_score(self, score):
        self.score = score

    
    def save_highscore(self, score):
        if self.score > self.highscore:
            self.highscore = self.score
            with open('data.json', 'w') as file:
                json.dump({'highscore': self.highscore}, file, indent=4)

    def _load_highscore(self):
        try:
            with open('data.json', 'r') as file:
                return json.load(file)['highscore']
        except:
            return 0
        
    def show_highscore(self, game, highscore):
        highscore = self.highscore
        str_highscore = str(highscore)
        n = len(str_highscore)
        w = asserts.get_images("0_small").get_width() * 1.1
        x = (W - n * w) / 2 + 75
        y = 220
        for number in str_highscore:
            game.blit(asserts.get_images(f"{number}_small"), (x, y))
            x += w    
    
        
    def show_score(self, game):
        str_score = str(self.score)
        n = len(str_score)
        w = asserts.get_images("0_small").get_width() * 1.1
        x = (W - n * w) / 2 + 72
        y = 176
        for number in str_score:
            game.blit(asserts.get_images(f"{number}_small"), (x, y))
            x += w
        