from screen.base import GameScreen
import pygame
from channel import Channel
from asserts import Asserts
from event import Event, PLAYER_LIST, QUIT, PIPE_DATA, START, READY
from bird import Bird


asserts = Asserts()
class MultiScreen(GameScreen):
    def __init__(self, game):
        super().__init__(game, asserts)
        
        self.bird = Bird(x = 120, y = 130, p_id = None)
        self.window = self.game.window
        
        self.player_list = []
        self.birds = []
        self.is_ready = False
        self.all_player_ready = False
        
        asserts.get_audios("bgsound").play(-1)
        
        
    def handle_channel_event(self, event):
        if event.is_event(PLAYER_LIST):
            self.player_list = event.data
            self.birds = self.get_birds_images(event.data)
            self.game.update_context("player_list", event.data)
        elif event.is_event(START):
            asserts.get_audios("bgsound").stop()
            self.game.screen_update("multi_game")
        elif event.is_event(READY):
            self.is_ready =True
        elif event.is_event(PIPE_DATA):
            self.game.update_context("pipe_data", event.data)


        # waiting for pipe data and then update scrren 
        #  
            

    def get_birds_images(self, birds):
        bird_list = []
        gap = 10
        n = len(birds)
        y0 = self.game.window.get_height() - 150
        x0 = (self.game.window.get_width() - 34 * n - ( n - 1 ) * gap ) / 2
        for i, bird in enumerate(birds):
            x = x0 + i * (34 + gap)
            x_pid = x + 12
            bird_list.append({
                "image": asserts.get_images("red_mid"),
                "position": (x, y0),
                "pid": bird["pid"],
                "pid_position": (x_pid - 2, y0 - 18)
            })
        
        return bird_list
        
    def _render(self, events, **args):
        
        self.blit_image("day", (0, 0))
        
        for event in events:
            self.handle_space(event)
            self.handle_click(event)
        
        self.blit_image("flappy", (50, 50))
        self.blit(asserts.get_images("floor"), (0, 400))
        
        if self.is_ready is True:
            # if len(self.birds) != 0:
                for bird in self.birds:               
                    self.blit(bird["image"],bird["position"])
                    font = pygame.font.SysFont("Arial", 14)
                    pid_text = font.render(bird["pid"], True, (0, 0, 0))
                    self.blit(pid_text, bird["pid_position"])
            
        else:      
            self.blit_image("ready", (50, 230))
            self.bird.fixed_draw(self.window)
            for bird in self.birds:               
                    self.blit(bird["image"],bird["position"])
                    font = pygame.font.SysFont("Arial", 14)
                    pid_text = font.render(bird["pid"], True, (0, 0, 0))
                    self.blit(pid_text, bird["pid_position"])
           
    def handle_space(self, event):
        if self.is_ready is True:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.game.channel.send(data=Event(id=START, data=None).to_dict())

            
    def handle_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if 50 < event.pos[0] < 200 and 230 < event.pos[1] < 300:
                self.is_ready = True
                self.game.channel.send(data=Event(id=READY, data=None).to_dict())
                

