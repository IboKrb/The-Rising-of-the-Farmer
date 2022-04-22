import pygame
from Settings import *
from level import *

class Player(pygame.sprite.Sprite):
    def __init__(self,pos,groups,obstacle_sprites):
        super().__init__(groups)
        self.image = pygame.image.load("./graphics/Player.png").convert_alpha()
        self.image =pygame.transform.scale(self.image,(TILE_SIZE,TILE_SIZE)) 
        self.rect = self.image.get_rect(topleft = pos)
    
        self.direction = pygame.math.Vector2()
        self.speed = 5
        self.obstacle_sprites = obstacle_sprites
    
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

        self.rect.x += self.direction.x * self.speed
        self.collision("horizontal")
        self.rect.y += self.direction.y * self.speed
        self.collision("vertical")
        #self.rect.center += self.direction * self.speed
        
    
    def collision(self,direction):
        if direction == "horizontal":
            for sprite in self.obstacle_sprites:
                if sprite.rect.colliderect(self.rect):
                    if self.direction.x > 0: #moving right
                        self.rect.right = sprite.rect.left
                    elif self.direction.x < 0: #moving left
                        self.rect.left = sprite.rect.right

        if direction == "vertical":
            for sprite in self.obstacle_sprites:
                if sprite.rect.colliderect(self.rect):
                    if self.direction.y > 0: #moving down
                        self.rect.bottom = sprite.rect.top
                    elif self.direction.y < 0: #moving up
                        self.rect.top = sprite.rect.bottom
                  

    def update(self):
        self.input()
        self.move()
        
    def run(self):
        level.visible_sprites.draw(self.display_surface)
        level.visible_sprites.update()
