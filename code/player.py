import pygame
from Settings import *
from level import *

class Player(pygame.sprite.Sprite):
    def __init__(self,pos,groups,obstacle_sprites):
        super().__init__(groups)
        self.image = pygame.image.load("./graphics/Player.png").convert_alpha()
        self.image =pygame.transform.scale(self.image,(TILE_SIZE,TILE_SIZE)) 
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0,-30)

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
                  
    def update(self):
        self.input()
        self.move()
        
    def run(self):
        level.visible_sprites.draw(self.display_surface)
        level.visible_sprites.update()
