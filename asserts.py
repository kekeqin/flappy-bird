import pygame
import os, random

class Asserts:
    def __init__(self):
        pygame.mixer.init()
        self.images = self._load_images()
        self.audios = self._load_audios()
        
        self.pipe_color = random.choice(["green_pipe", "red_pipe"])
        
    def _load_images(self):
        images = {}
        for file in os.listdir("./pics"):
            name, extension = os.path.splitext(file)
            if extension in [".png", ".jpg"]:
                path = os.path.join("./pics", file)
                images[name] = pygame.image.load(path)
        return images
    
    def get_images(self, name):
        return self.images[name]
    
    def bird_images(self):
        color = random.choice(["red", "yellow", "blue"])
        bird_images = [self.images[color + "_up"],
                       self.images[color + "_mid"],
                       self.images[color + "_down"]
                       ]
        return bird_images
    
    def pipe_images(self):
        pipe = self.images[self.pipe_color]
        pipe_images = [pipe, pygame.transform.flip(pipe, False, True)]
        return pipe_images
    
    def bg_images(self):
        bg_images = random.choice(["day", "night"])
        return self.images[bg_images]
    
    def _load_audios(self):
        audios = {}
        for file in os.listdir("./audio"):
            name, extension = os.path.splitext(file)
            if extension in [".wav", ".mp3"]:
                path = os.path.join("./audio", file)
                audios[name] = pygame.mixer.Sound(path)
        return audios
    
    def get_audios(self, name):
        return self.audios[name]
    