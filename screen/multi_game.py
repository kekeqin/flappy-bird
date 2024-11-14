from screen.base import GameScreen
from client_pipes.multipipes import MultiPipes
import pygame
from channel import Channel
from asserts import Asserts
from bird import Bird
from event import Event, PLAYER_LIST, QUIT, PIPE_DATA, JUMP
from score import Score


asserts = Asserts()
class MultiGame(GameScreen):
    def __init__(self, game):
        super().__init__(game, asserts)
        self.window = self.game.window
        self.dead = False
        
        self.floor_image = asserts.get_images("floor")
        self.floor_x = 0
         
        self.score = Score()
        
        self.birds = self.build_birds_from_player_list(game.get_context("player_list", True))

        self.pipes = MultiPipes(game.get_context("pipe_data", True))
        self.pipes.init_pipes()

        self.pid = game.get_context("multiplayer_mode_pid", True)
        
    def handle_channel_event(self, event):
        if event.is_event(JUMP):
            pid = event.data["pid"]
            bird = self.birds[pid]
            bird.jump()


    def build_birds_from_player_list(self, player_list):
        birds = {}
        for player in player_list:
            pid = player["pid"]
            birds[pid] = Bird(x=60, y=200, p_id=player["pid"])

        return birds

    def render_birds(self):
        for pid, bird in self.birds.items():
            if not bird.dead:
                font = pygame.font.SysFont("Arial", 14)
                id_text = font.render(pid, True, (255, 255, 255))
                self.blit(id_text, bird.dynamic_id())
                bird.move()
                bird.draw(self.window)
                if bird.check_collision(self.pipes.pipes):
                    bird.dead = True

        
    def _render(self, events, **args):
        self.handle_events(events)

        if not self.dead:
            self.blit(asserts.get_images("day"), (0, 0))
            self.blit(asserts.get_images("floor"), (0, 400))
            self.pipes.update_pipes()
            self.pipes.draw_and_update(self.window)
            self.update_floor()

            self.render_birds()
            
        else:
            self.blit(asserts.get_images("day"), (0, 0))
            self.blit(asserts.get_images("floor"), (0, 400))
            self.pipes.update_pipes()
            self.pipes.draw_and_update(self.window)
            self.update_floor()
            # self.bird.draw(self.window)
            self.score.render_score(self.window)
            font = pygame.font.SysFont("Arial", 28)
            dead_text = font.render("YOU DEAD!", True, (250, 250, 250))
            
            self.blit(dead_text, (65, 150))
    
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                event_data = {"pid": self.pid}
                self.game.channel.send(data=Event(id=JUMP, data=event_data).to_dict())
    
    def update_floor(self):
        self.floor_x -= 2
        if self.floor_x <= - (self.floor_image.get_width() - 288):
            self.floor_x = 0
        self.window.blit(self.floor_image, (self.floor_x, 400))
        
            
