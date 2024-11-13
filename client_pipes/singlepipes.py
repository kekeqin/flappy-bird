import pygame
import random
from client_pipes.pipe import Pipe
from client_pipes.basepipes import BasePipes

H = 512
W = 288
N_PAIRS = 4
DISTANCE = 200
PIPE_GAP = 120

class SinglePipes(BasePipes):
    def __init__(self):
        super().__init__()
        
        
    def init_pipes(self):
        for i in range(N_PAIRS):
            
            x = W + i * DISTANCE
            up_y = random.randint(int(H * 0.3), int(H * 0.7))          
            up_pipe = Pipe(x, up_y, True)
            
            down_y = up_y - PIPE_GAP
            down_pipe = Pipe(x, down_y, False)
            
            self.pipes.add(up_pipe)
            self.pipes.add(down_pipe)
            
            
    def update_pipes(self):
        
        first_up_pipe = self.pipes.sprites()[0]
        first_down_pipe = self.pipes.sprites()[1]
        
        if first_up_pipe.rect.right < 0:
            up_y = random.randint(int(H * 0.3), int(H * 0.7))
            
            pipe_x = first_up_pipe.rect.x + N_PAIRS * DISTANCE
            new_up_pipe = Pipe(pipe_x, up_y, True)
            
            down_y = up_y - PIPE_GAP
            new_down_pipe = Pipe(pipe_x, down_y, False)
            
            self.pipes.add(new_up_pipe)
            self.pipes.add(new_down_pipe)
            
            first_up_pipe.kill()
            first_down_pipe.kill()
            

        
            
        