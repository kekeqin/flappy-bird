import pygame
import math
from asserts import Asserts
from score import Score

H = 512
asserts = Asserts()
class Bird:
    def __init__(self, x, y, p_id):
        self.id = p_id
        
        self.images = asserts.bird_images()
        self.indx = 0
        self.current_indx = 0
        self.image = self.images[self.current_indx]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        self.y_vel = -6
        self.gravity = 0.5
        self.velocity = 0
        self.animation_speed = 0.08
        self.y_amplitude = 1.5
        self.y_frequency = 0.01
        
        self.dead =False
        
        self.score = 0

        self.is_jump = False

    def jump(self):
        self.is_jump = True
        
    def move(self):
        if not self.dead:
            if self.is_jump and self.velocity >= 0:
                self.is_jump = False
                asserts.get_audios("flap").play()
                self.velocity = self.y_vel
            self.velocity += self.gravity
            self.rect.y += self.velocity
            
            self.update_indx_state() 

            
    def update_indx_state(self):
        if self.velocity > 0:
            self.current_indx = 0
        elif self.velocity < 0:
            self.current_indx = 2
        else:
            self.current_indx = 1
            
        self.indx += self.animation_speed
        self.image = self.images[int(self.indx % len(self.images))]
        
    def fixed_draw(self, window):
        if not self.dead:
            offset = pygame.time.get_ticks() * self.y_frequency
            vertical_offset = self.y_amplitude * math.sin(offset)
            
            self.rect.y += vertical_offset

            self.update_indx_state()
            
                   
            window.blit(self.image, self.rect)
        
    def draw(self, window):
        if not self.dead:
            rotate_angle = -self.velocity * 4
            rotate_image = pygame.transform.rotate(self.image, rotate_angle)
            window.blit(rotate_image, self.rect)
        else:
            window.blit(self.image, self.rect)
            
    def check_collision(self, pipes):
        if pygame.sprite.spritecollideany(self, pipes) or self.rect.top < 0 or self.rect.bottom > 400 :
            self.dead = True
            asserts.get_audios("hit").play()
            asserts.get_audios("die").play()
            return True
        return False          
            
    def bird_score(self, pipes):
        for pipe in pipes:
            if  self.rect.left + pipe.x_vel < pipe.rect.centerx < self.rect.left:
                asserts.get_audios("score").play()
                self.score += 1
                return True
        return False
    
    def bird_dead(self):
        self.dead = True
        
    def dynamic_id(self):
        return (self.rect.x, self.rect.y - 10)
        
    