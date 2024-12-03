import pygame

class GameScreen:
    def __init__(self, game, asserts=None, bg=None):
        self.game = game
        self.running = False
        
        self.bg = self.game.bg
        self.asserts = asserts
        self.clock = pygame.time.Clock()
        
    def run(self):
        self.running = True
        
        while self.running:
            events = []
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._on_quit()
                    return
                else:
                    events.append(event)

            self.blit(self.bg, (0, 0))
            self._render(events)
            pygame.display.update()
            self.clock.tick(120)
            
    def _render(self, events, **args):
        pass
    
    def blit(self, image, args):
        self.game.window.blit(image, args)
        
    def blit_image(self, image_name, args):
        image = self.asserts.get_images(image_name)
        self.blit(image, args)
        
    def stop(self):
        self._stop()
        self.running = False

    def handle_channel_event(self, event):
        self._handle_channel_event(event)
        
    def _on_quit(self):
        self.stop()
        self.game.quit()
        
    def _stop(self):
        pass

    def _handle_channel_event(self):
        pass
        
        
        
            