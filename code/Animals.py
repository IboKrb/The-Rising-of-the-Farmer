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
        self.hitbox = self.rect.inflate(0,0)

        self.status= "down"
         
        self.direction = pygame.math.Vector2()

        self.fram_index = 0
        self.import_animal()

        self.speed= 1

        self.small_tile_size = 26
        self.big_tile_size = 65

        self.tamet = False

        self.zahlrauf = 0
        self.animation_speed = 0.05
        
        self.randomzahl = 0
        self.dir_player = pygame.math.Vector2()
        self.obstacle_sprites = obstacle_sprites
    
    def random_animal(self):
        self.animals_path = ["./graphics/sprites_tiere/Schaf/Braun/",
        "./graphics/sprites_tiere/Schaf/Weiss/",
        "./graphics/sprites_tiere/Wolf/Braun/",
        "./graphics/sprites_tiere/Wolf/BraunWeiss/",
        "./graphics/sprites_tiere/Wolf/Dunkelgrau/",
        "./graphics/sprites_tiere/Wolf/Grau/",
        "./graphics/sprites_tiere/Wolf/Schwarz/",
        "./graphics/sprites_tiere/Wolf/Weiss/",
        "./graphics/sprites_tiere/Baren/Hellbraun/",
        "./graphics/sprites_tiere/Baren/Braun/",
        "./graphics/sprites_tiere/Baren/Schwarz/",
        "./graphics/sprites_tiere/Hamster/Grau/",
        "./graphics/sprites_tiere/Hamster/weiß/",
        "./graphics/sprites_tiere/Hamster/Braun/"]
        
    def import_animal(self):
        self.random_animal()
        self.animal_number= randint(0,13)
        self.animal_path= self.animals_path[self.animal_number]
        self.animations = {"up":[],"down":[],"left":[],"right":[],"idle":[]}
        
        for animation in self.animations.keys():
            full_path = self.animal_path+animation
            self.animations[animation] = import_folder_layout(full_path)      
            

    def zahlen(self):
        self.zahlrauf += 1
    
    def random_choice(self):
        self.zahlen()
        if self.zahlrauf == 60:
            self.randomzahl = randint(1,150)
            self.zahlrauf = 0
            
    def angriff(self):
        #if self.animal_number 
        pass

    def random_move(self):
        self.random_choice()
        
        if self.randomzahl <= 10 :
            self.direction.x = 1
            self.status = "right"

        elif self.randomzahl >= 11 and self.randomzahl <= 20 :
            self.direction.x = -1
            self.status = "left"
    
        elif self.randomzahl  >= 21 and self.randomzahl <= 30 :
            self.direction.y = 1
            self.status = "down"
       
        elif self.randomzahl >= 31 and self.randomzahl <= 40 :
            self.direction.y = -1
            self.status = "up"
            
        elif self.randomzahl >= 41 and self.randomzahl <= 150:
            self.status = "idle"
            self.direction.x = 0
            self.direction.y = 0

    def move(self):
        self.random_move()
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        self.hitbox.x += self.direction.x * self.speed
        self.collision("horizontal")
        self.hitbox.y += self.direction.y * self.speed
        self.collision("vertical")
        self.rect.center = self.hitbox.center
    
    def movement(self):
        if self.tamet == False:
            self.move()
        else:
            self.move_to_player()

    def move_to_player(self):
        if self.dir_player.x > self.direction.x:
            self.direction.x -= 15
        elif self.dir_player.x < self.direction.x:
            self.direction.x += 15
        if self.dir_player.y > self.direction.y:
            self.direction.y -= 15
        elif self.dir_player.y < self.direction.y:
            self.direction.y += 15

    def animate(self):
        animation = self.animations[self.status]
        self.fram_index += self.animation_speed
        if self.fram_index >= len(animation):
                self.fram_index = 0
        self.image = animation[int(self.fram_index)]
        
        #self.image =pygame.transform.scale(self.image,(TILE_SIZE,TILE_SIZE))

        if self.animal_number >= 11 :
            self.image =pygame.transform.scale(self.image,(self.small_tile_size,self.small_tile_size))
        elif self.animal_number <= 7:
            self.image = pygame.transform.scale(self.image,(TILE_SIZE,TILE_SIZE))
        elif self.animal_number == 8 or 9 or 10 or 11:
            self.image = pygame.transform.scale(self.image,(self.big_tile_size,self.big_tile_size))


    def collision(self,direction):

        if direction == "horizontal":
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0: #moving right
                        self.hitbox.right = sprite.hitbox.left
                    elif self.direction.x < 0: #moving left
                        self.hitbox.left = sprite.hitbox.right

        if direction == "vertical":
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0: #moving down
                        self.hitbox.bottom = sprite.hitbox.top
                    elif self.direction.y < 0: #moving up
                        self.hitbox.top = sprite.hitbox.bottom    

       


    def update(self):
        self.animate()
        self.movement()
    
    def run(self):
        Spiel.visible_sprites.draw(self.display_surface)
        Spiel.visible_sprites.update() 

