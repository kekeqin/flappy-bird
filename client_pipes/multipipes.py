from client_pipes.basepipes import BasePipes
from client_pipes.pipe import Pipe
import pygame


H = 512
W = 288
N_PAIRS = 4
DISTANCE = 200
PIPE_GAP = 120

class MultiPipes(BasePipes):
    def __init__(self, pipe_data):
        super().__init__()
        
        self.pipe_data = pipe_data
        self.pipe_data_indx = 0
        
    def init_pipes(self):
        for i in range(N_PAIRS):
            x = W + i * DISTANCE
            positions = self.pipe_data[self.pipe_data_indx]
            
            up_pipe = Pipe(x, positions[0], True)
            down_pipe = Pipe(x, positions[1], False)
            
            self.pipes.add(up_pipe)
            self.pipes.add(down_pipe)
            self.pipe_data_indx += 1
    
    def update_pipes(self):
        first_up_pipe = self.pipes.sprites()[0]
        first_down_pipe = self.pipes.sprites()[1]
        
        if first_up_pipe.rect.right < 0:
            
            x = first_up_pipe.rect.x + N_PAIRS * DISTANCE
            positions = self.pipe_data[self.pipe_data_indx]
            
            new_up_pipe = Pipe(x, positions[0], True)
            new_down_pipe = Pipe(x, positions[1], False)
            
            self.pipes.add(new_up_pipe)
            self.pipes.add(new_down_pipe)
            
            first_up_pipe.kill()
            first_down_pipe.kill()
            
            self.pipe_data_indx += 1
            
        
        