import pygame
from Settings import *

class Tile(pygame.sprite.Sprite):
    def __init__(self,pos,groups):
        super().__init__(groups)
        self.image = pygame.image.load("./graphics/stone.png").convert_alpha()
        self.image =pygame.transform.scale(self.image,(TILE_SIZE,TILE_SIZE)) 
        self.rect = self.image.get_rect(topleft = pos)