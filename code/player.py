import pygame
from Settings import *
from level import *

class Player(pygame.sprite.Sprite):
    def __init__(self,pos,groups):
        super().__init__(groups)
        self.image = pygame.image.load("./graphics/Player.png").convert_alpha()
        self.image =pygame.transform.scale(self.image,(TILE_SIZE,TILE_SIZE)) 
        self.rect = self.image.get_rect(topleft = pos)
    
        self.direction = pygame.math.Vector2()
        self.speed = 5
    
    def input(self):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_LEFT]:
            self.direction.x = -1
        elif pressed[pygame.K_RIGHT]:
            self.direction.x = 1
        elif pressed[pygame.K_UP]:
            self.direction.y = -1
        elif pressed[pygame.K_DOWN]:
            self.direction.y = 1
        else:
            self.direction.x = 0
            self.direction.y = 0
    
    def move(self):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        self.rect.center += self.direction * self.speed

    def update(self):
        self.input()
        self.move()
        
    def run(self):
        level.visible_sprites.draw(self.display_surface)
        level.visible_sprites.update()
