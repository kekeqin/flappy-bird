from screen.base import GameScreen
from client_pipes.multipipes import MultiPipes
import pygame
from channel import Channel
from asserts import Asserts
from bird import Bird
from event import Event, PLAYER_LIST, QUIT, PIPE_DATA, JUMP, DEAD
from score import Score


asserts = Asserts()
class MultiGame(GameScreen):
    def __init__(self, game):
        super().__init__(game, asserts)
        self.window = self.game.window
        self.dead = False
        self.all_dead = False
        
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
        elif event.is_event(DEAD):
            self.handle_dead_event(event)
        elif event.is_event(SCORE):
            score = event.data["score"]
            self.game.update_context("multiplayer_mode_pid_score", score)
            self.game.get_context("multiplayer_mode_pid_score", True)
            self.handle_score_event(event)
            
    def handle_score_event(self, event):
        pid = event.data["pid"]
        current_pid = self.game.get_context("multiplayer_mode_pid", True)
        if pid == current_pid:
            bird = self.birds[pid]
            if bird.bird_score(self.pipes.pipes):
                self.score.update(1)
            
    def handle_dead_event(self,event):
        pid = event.data["pid"]
        current_pid = self.game.get_context("multiplayer_mode_pid", True)
        if pid == current_pid:
            bird = self.birds[pid]
            bird.bird_dead()


    def build_birds_from_player_list(self, player_list):
        birds = {}
        for player in player_list:
            pid = player["pid"]
            birds[pid] = Bird(x=60, y=200, p_id=player["pid"])

        return birds
    
    def check_all_birds_dead(self):
        for bird in self.birds.values():
            if not bird.dead:
                return False
        self.all_dead = True
        return True

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
                    dead_event = Event(id=DEAD, data={"pid": self.pid})
                    self.game.channel.send(data=dead_event.to_dict())
                    if bird.id == self.pid:
                        self.all_dead = self.check_all_birds_dead()
                        
                if bird.bird_score(self.pipes.pipes):
                    self.score.update(1)
                self.score.render_score(self.window)
            else:
                if bird.id == self.pid:
                    self.score.render_score(self.window)
                    font = pygame.font.SysFont("Arial", 28)
                    dead_text = font.render("YOU DEAD!", True, (250, 250, 250))
                    self.blit(dead_text, (65, 150))
                    score_text = font.render(f"Score: {bird.score}", True, (255, 255, 255))
                    self.blit(score_text, (65, 200))
     
    def _render(self, events, **args):
        self.handle_events(events)
        self.blit(asserts.get_images("day"), (0, 0))
        self.blit(asserts.get_images("floor"), (0, 400))
        self.pipes.update_pipes()
        self.pipes.draw_and_update(self.window)
        self.update_floor()

        if not self.all_dead:
            self.render_birds()
            self.check_all_birds_dead()
            
        else:
            self.render_game_over(events)
            
    def render_game_over(self, events, **args):
        self.handle_click(events)
        self.score.render_score(self.window)
        self.blit(asserts.get_images("gameover"), (45, 20))
        self.blit(asserts.get_images("key"), (85, 330))
        
        if self.all_dead:
            bird_scores = [(pid, bird.score) for pid, bird in self.birds.items()]
            sorted_scores = sorted(bird_scores, key=lambda x: x[1], reverse=True)

            font = pygame.font.SysFont("Arial", 20)
            rank_y_pos = 150  
            for rank, (pid, score) in enumerate(sorted_scores, 1):
                rank_text = font.render(f"Rank {rank}: {pid} - Score: {score}", True, (255, 255, 255))
                self.blit(rank_text, (50, rank_y_pos))
                rank_y_pos += 30
            self.disconnect()
    
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                event_data = {"pid": self.pid}
                self.game.channel.send(data=Event(id=JUMP, data=event_data).to_dict())
                
    def handle_click(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 85 < event.pos[0] < 200 and 330 < event.pos[1] < 400:
                    self.game.screen_update("home")
                    
    def disconnect(self):
        if self.game.channel != None:
            self.game.channel.send(data=Event(id=QUIT, data=None).to_dict())
            self.game.channel.close()
            self.game.channel = None
    
    def update_floor(self):
        self.floor_x -= 2
        if self.floor_x <= - (self.floor_image.get_width() - 288):
            self.floor_x = 0
        self.window.blit(self.floor_image, (self.floor_x, 400))
        
            
