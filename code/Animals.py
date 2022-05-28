from turtle import down
import pygame 
from Settings import *
from level import *
from support import *
from random import *

class Animals(pygame.sprite.Sprite):
    def __init__(self,pos,groups,obstacle_sprites):
        super().__init__(groups)
        self.image = pygame.image.load("./graphics/sprites_tiere/Schaf/Braun/down/sprite1.png").convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0,-30)

        self.import_animal()
        self.status= "down"
        
        self.fram_index = 0

        self.speed_y= 0
        self.speed_x = 0
        
        self.zahlrauf = 0
        self.animation_speed = 0.05
        
        self.randomzahl = 0
        
       
        
        self.obstacle_sprites = obstacle_sprites

        
    def import_animal(self):
        animal_path= "./graphics/sprites_tiere/Schaf/Braun/"
        self.animations = {"up":[],"down":[],"left":[],"right":[],"idle":[]}
        
        for animation in self.animations.keys():
            full_path = animal_path+animation
            self.animations[animation] = import_folder_layout(full_path)      
            
                
    def zahlen(self):
        self.zahlrauf += 1
    
    def random_choice(self):
        self.zahlen()
        if self.zahlrauf == 30:
            self.randomzahl = randint(1,100)
            self.zahlrauf = 0
            

    def random_move(self):
        self.random_choice()
        
        if self.randomzahl <= 10 :
            self.status = "right"
            self.speed_x = 1
 

            
        elif self.randomzahl >= 11 and self.randomzahl <= 20 :
            self.status = "left"
            self.speed_x = -1
    

        
        elif self.randomzahl  >= 21 and self.randomzahl <= 30 :
            self.status = "down"
            self.speed_y = 1
  
            
        elif self.randomzahl >= 31 and self.randomzahl <= 40 :
            self.status = "up"
            self.speed_y = -1
            
        elif self.randomzahl >= 41 and self.randomzahl <= 100:
            self.status = "idle"
            self.speed_y = 0
            self.speed_x = 0



    def movement(self):
        self.random_move()
        if self.status == "left" :
            self.rect.move_ip(self.speed_x, 0)
            self.collision("horizontal")
        if self.status == "right"  :
            self.rect.move_ip(self.speed_x,0)
            self.collision("horizontal")
        if self.status == "down" :
            self.rect.move_ip(0, self.speed_y)
            self.collision("vertical")
        if self.status == "up" :
            self.rect.move_ip(0,self.speed_y)
            self.collision("vertical")


    

    def animate(self):
        animation = self.animations[self.status]
        self.fram_index += self.animation_speed
        if self.fram_index >= len(animation):
                self.fram_index = 0
        self.image = animation[int(self.fram_index)]
        self.image =pygame.transform.scale(self.image,(TILE_SIZE,TILE_SIZE))

    def collision(self,direction):
        if direction == "horizontal":
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.speed_x > 0: #moving right
                        self.hitbox.right = sprite.hitbox.left
                    elif self.speed_x.x < 0: #moving left
                        self.hitbox.left = sprite.hitbox.right

        if direction == "vertical":
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.speed_y > 0: #moving down
                        self.hitbox.bottom = sprite.hitbox.top
                    elif self.speed_y < 0: #moving up
                        self.hitbox.top = sprite.hitbox.bottom
        
    def update(self):
        self.animate()
       # self.collision()
        self.movement()
    
    def run(self):
        level.visible_sprites.draw(self.display_surface)
        level.visible_sprites.update() 