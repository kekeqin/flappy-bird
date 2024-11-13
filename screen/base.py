import pygame

class GameScreen:
    def __init__(self, game, asserts=None):
        self.game = game
        self.running = False
        
        self.bg = self.game.bg
        self.asserts = asserts
        
    def run(self):
        clock = pygame.time.Clock()
        self.running = True
        
        while self.running:
            clock.tick(60)
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
        
    def _on_quit(self):
        self.stop()
        self.game.quit()
        
    def _stop(self):
        pass
        
        
        
            