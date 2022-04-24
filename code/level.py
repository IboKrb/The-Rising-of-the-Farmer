import pygame
from Settings import *
from tile import *
from player import Player
from debug import debug
from support import *
from random import choice
class level:
    def __init__(self):
        
        #get the display surface
        self.display_surface = pygame.display.get_surface()
        
        #sprite groups
        self.visible_sprites = YsortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
    
        #sprite setup
        self.create_map()

    def create_map(self):
        layout = {
            "boundary": import_csv_layout("./map/Map_ausen.csv"),
            "objects": import_csv_layout("./map/Map_BAUMHaus.csv")

        }
        graphics = {
            "objects": import_folder_layout("./graphics/Tiled/Tilesets"),
        }

        for style,layout in layout.items():
            for row_index,row in enumerate(layout):
                for col_index,col in enumerate(row):
                    if col !=  '-1':
                        x = col_index * TILE_SIZE 
                        y = row_index * TILE_SIZE 
                        x += 150
                        y += 50 
                        if style == "boundary":
                            Tile((x,y),[self.obstacle_sprites],"invisible")
                        if style == "baumhaus":
                            surf = graphics["objects"][int(col)]
                            Tile((x,y),[self.visible_sprites,self.obstacle_sprites],"object",surf)
        """"
                if col == 'x':
                    Tile((x,y),[self.visible_sprites,self.obstacle_sprites])
                if col == 'p':
        """
        self.player = Player((1000,800),[self.visible_sprites],self.obstacle_sprites)

    def run(self):
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()

class YsortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0]//2
        self.half_height = self.display_surface.get_size()[1]//2
        self.offset = pygame.math.Vector2()
        self.floor_surface = pygame.Surface((self.display_surface.get_size()))

        #creating the floor
        self.floor_surface = pygame.image.load("./graphics/Tiled/Map.png").convert()
        self.floor_rect = self.floor_surface.get_rect(topleft =	(TILE_SIZE,TILE_SIZE))
    
    def custom_draw(self,player):

        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height
        
        #drawing the floor
        floor_offset_pos =self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surface,floor_offset_pos)

        #draw sprites
        for sprite in sorted(self.sprites(),key=lambda sprite:sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image,offset_pos)
