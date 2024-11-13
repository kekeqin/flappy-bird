import pygame
import sys
from channel import Channel
from event import Event, PLAYER_LIST, QUIT, PIPE_DATA, START, READY, PID
from screen.home_screen import HomeScreen
from screen.single_screen import SingleScreen
from screen.single_game import SingleGame
from screen.multi_screen import MultiScreen
from screen.multi_game import MultiGame
from screen.game_over import GameOverScreen

from asserts import Asserts

class GameScreen:
    def __init__(self):
        self.running = True
        self.screen = None
        # 上下文
        self.context = {}
        self.window = self.init_window()
        
        self.asserts = Asserts()
        self.bg = self.asserts.bg_images()

        self.channel = None
        
    def init_window(self):
        pygame.init()
        pygame.display.set_caption("flybird")
        return pygame.display.set_mode((288, 512))

    def start(self):
        self.screen_update("home")
        self.asserts.get_audios("start").play()

        while self.running:
            self.screen.run()
            
    def connect_channel(self):
        if self.channel == None:
            print("connting to server...")
            self.channel = Channel(self.handle_channel_events)
            self.channel.recv()
        
    def handle_channel_events(self, event):
        if event.is_event(PID):
            pid = event.data["pid"]
            print("recive pid: ", pid)
            self.update_context("multiplayer_mode_pid", pid)
        else:
            self.screen.handle_channel_event(event)
                      
    def screen_update(self, name, final_score = None):
        current_screen = self.screen
        match name:
            case "home":
                self.screen = HomeScreen(self)
            case "single":
                self.screen = SingleScreen(self)
            case "single_game":
                self.screen = SingleGame(self)
            case "multi":
                self.connect_channel()
                self.screen = MultiScreen(self)
            case "multi_game":
                self.screen = MultiGame(self)
            case "game_over":
                if current_screen and isinstance(current_screen, SingleGame): # 获取SingleGame的得分
                    final_score = current_screen.get_final_score()
                self.screen = GameOverScreen(self, final_score) # 传递得分
                # self.screen = GameOverScreen(self)
                
        if current_screen is not None:
            current_screen.stop()
    

    def get_context(self, key, is_remove = False):
        value = self.context.get(key)
        if is_remove:
            self.remove_context_item(key)
        return value

    def update_context(self, key, value):
        self.context[key] = value

    def remove_context_item(self, key):
        if key in self.context:
            self.context.pop(key)

    def clean_context(self):
        self.context = {}

    def quit(self):
        self.runing = False
        if self.channel:
            self.channel.send(data=Event(id=QUIT, data=None).to_dict())
            self.channel.close()
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = GameScreen()
    game.start()