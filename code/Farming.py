from turtle import down
import pygame 
from Settings import *
from level import *
from support import *
from random import *

class Harvest(pygame.sprite.Sprite):
    def __init__(self,pos,groups,obstacle_sprites):
        super().__init__(groups)
        self.image = pygame.image.load("./graphics/flav/flaver/idle/sprite1.png").convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        #self.image = pygame.transform.scale(self.image,(100,100))
        self.hitbox = self.rect.inflate(0,0)

        self.status= "idle"
        
        self.direction = pygame.math.Vector2()
        self.fram_index = 0

        self.import_flav()
        self.frame_index = 0
        self.zahlrauf = 0
        self.animation_speed = 0.009 
        self.randomzahl = 0
        
        self.obstacle_sprites = obstacle_sprites
    
    def zahlen(self):
        self.zahlrauf += 1

    def random_status(self):
        self.randomstatus= randint(0,1)
        if self.randomstatus == 0 and self.zahlrauf >= 200:
            self.status = "idle"
            self.zahlrauf = 0
        elif self.randomstatus == 1 and self.zahlrauf >= 200:
            self.status = "harvesting"
            self.zahlrauf = 0
            print(self.status) 
        

    def import_flav(self):
        character_path= "./graphics/flav/flaver/"
        self.animations = {"idle":[],"harvesting":[]} 

        for animation in self.animations.keys():
            full_path = character_path+animation
            self.animations[animation] = import_folder_layout(full_path)


    def random_geschwindigeit(self):
        self.randomzahl = randint(0,10)
        if self.randomzahl == 0:
            self.animation_speed = 0.001
        elif self.randomzahl == 1:
            self.animation_speed = 0.002
        elif self.randomzahl == 2:
            self.animation_speed = 0.003
        elif self.randomzahl == 3:
            self.animation_speed = 0.004

    def animate(self):
        self.random_geschwindigeit()
        self.fram_index += self.animation_speed
        self.frame_index = self.fram_index
        if self.frame_index != len(self.animations[self.status]):
            if self.frame_index >= len(self.animations[self.status]):
                    self.frame_index = len(self.animations[self.status])-1
        self.image = self.animations[self.status][int(self.frame_index)]
        self.image = pygame.transform.scale(self.image,(60,60))
    
    def delete(self):
        #if self.frame_index >= 3 and player_havest:
        self.kill()
            
        

    def update(self):
        self.random_status()
        self.animate()
        #self.delete()
        #pass

    def run(self):
        Spiel.visible_sprites.draw(self.display_surface)
        Spiel.visible_sprites.update() 

