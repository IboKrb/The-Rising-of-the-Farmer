import pygame
from Settings import *
from level import *
from support import *
from Animals import *
from Farming import *

class Player(pygame.sprite.Sprite):
    def __init__(self,pos,groups,obstacle_sprites):
        super().__init__(groups)
        self.image = pygame.image.load("./graphics/spritemaps/Char/down/sprite1.png").convert_alpha()
        self.image =pygame.transform.scale(self.image,(Player_size,Player_size))
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0,-30)

    
        self.import_player_assets()
        self.status= "down"

        #self.camera = Camera()

        self.direction = pygame.math.Vector2()
        self.speed = 4
        self.anzahl_obst = 0

        self.frame_index = 0
        self.animation_speed = 0.10

        self.harvesting = False
        self.harvest_cooldown = 400
        self.harvest_time = None

        self.obstacle_sprites = obstacle_sprites

    def import_player_assets(self):
        character_path= "./graphics/spritemaps/Char/"
        self.animations = {"up":[],"down":[],"left":[],"right":[],
        "upidle":[],"downidle":[],"leftidle":[],"rightidle":[],
        "downharvesting":[],"upharvesting":[],"rightharvesting":[],"leftharvesting":[]}

        for animation in self.animations.keys():
            full_path = character_path+animation
            self.animations[animation] = import_folder_layout(full_path)

    def input(self):
        pressed = pygame.key.get_pressed() 
        if pressed[pygame.K_LEFT]:
            self.direction.x = -1
            self.status = "left"
        elif pressed[pygame.K_RIGHT]:
            self.direction.x = 1
            self.status	= "right"
        elif pressed[pygame.K_UP]:
            self.direction.y = -1
            self.status = "up"
        elif pressed[pygame.K_DOWN]:
            self.direction.y = 1
            self.status = "down"
        else:
            self.direction.x = 0
            self.direction.y = 0

        #harvesting
        if pressed[pygame.K_SPACE]and not self.harvesting:
            self.harvesting = True
            self.harvest_time = pygame.time.get_ticks()    
            #Camera.collision_player_harvest()
            
            
            print("harvesting")
        
        #feeding
        if pressed[pygame.K_f]and not self.harvesting:
            self.harvesting = True
            print("feeding")
        #catch
        if pressed[pygame.K_c]and not self.harvesting:
            self.harvesting = True
            print("catch")
    
    def get_status(self):
        if self.direction.x == 0 and self.direction.y == 0:
            if not "idle" in self.status and not "harvesting"in self.status:
                self.status = self.status + "idle"
        
        if self.harvesting:
            self.direction.x = 0
            self.direction.y = 0
            if not "harvesting" in self.status:
                if "idle" in self.status:
                    self.status = self.status.replace("idle","harvesting")
                else:
                    self.status = self.status + "harvesting"
        else:
            if "harvesting" in self.status:
                self.status = self.status.replace("harvesting","idle")

    def cooldonws(self):
        current_Time = pygame.time.get_ticks()	

        if self.harvesting:
            if current_Time - self.harvest_time >= self.harvest_cooldown:
                self.harvesting = False
                 
    def move(self):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * self.speed
        self.collision("horizontal")
        self.hitbox.y += self.direction.y * self.speed
        self.collision("vertical")
        self.rect.center = self.hitbox.center
        
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

        #overlap_sprites= pygame.sprite.spritecollide(self.obstacle_sprites,self.animals,True)    
        #if overlap_sprites:
         #   print("hit")

    def animate(self):
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
                self.frame_index = 0
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)

    def update(self):
        self.input()
        self.move()
        self.cooldonws()
        self.get_status()
        self.animate()

        
    def run(self):
        Spiel.visible_sprites.draw(self.display_surface)
        Spiel.visible_sprites.update()
