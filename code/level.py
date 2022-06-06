import pygame
from Settings import *
from tile import *
from player import Player
from debug import debug
from support import *
from random import choice
from Animals import Animals
from random import *
from Farming import Harvest

class Spiel:
    def __init__(self):
        
        #get the display surface
        self.display_surface = pygame.display.get_surface()
        
        #sprite groups
        self.visible_sprites = Camera()
        self.obstacle_sprites = pygame.sprite.Group()

    
         #sprite setup
        self.create_map()

        self.spawn_x = 0
        self.spawn_y = 0

    def random_spawn(self):
        self.spawn_x = randint(1600,4600)
        self.spawn_y = randint(1000,4000)

    def create_map(self):
        layout = {
            "boundary": import_csv_layout("./map/Map_ausen.csv"),
            "baumhaus": import_csv_layout("./map/Map_BAUMHaus.csv")


        }
        graphics = {
            "objects": import_folder_layout("./graphics/Tiled/Tilesets"),
        }

        for style,layout in layout.items():
            for row_index,row in enumerate(layout):
                for col_index,col in enumerate(row):
                    if col !=  '-1':
                        x = col_index * 55
                        y = row_index * 55
                        x += 200
                        y += 100

                        if style == "boundary":
                            Tile((x,y),[self.obstacle_sprites],"invisible")

                        #if style == "baumhaus":
                        #   Tile((x,y),[self.visible_sprites],"invisible")
                    
        """"
                if col == 'x':
                    Tile((x,y),[self.visible_sprites,self.obstacle_sprites])
                if col == 'p':
        """
        self.player = Player((1000,800),[self.visible_sprites],self.obstacle_sprites)
        self.random_animal_spawn()
        self.random_flav_spawn()

        
    def random_animal_spawn(self):
        for i in range(0,50):
            self.random_spawn()
            self.animal = Animals((self.spawn_x,self.spawn_y),[self.visible_sprites],self.obstacle_sprites)
    
    def random_flav_spawn(self):
        for i in range(0,200):
            self.random_spawn()
            self.farm_spawn = Harvest((self.spawn_x,self.spawn_y),[self.visible_sprites],self.obstacle_sprites)
    
    

    def run(self):
        self.visible_sprites.draw(self.animal)
        self.visible_sprites.draw(self.farm_spawn)
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        self.visible_sprites.collision(self.player,self.animal)
        self.visible_sprites.collision_player_harvest(self.player)

        #self.collision()
        debug(self.player.status)

                

class Camera(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0]//2
        self.half_height = self.display_surface.get_size()[1]//2
        self.offset = pygame.math.Vector2()
        self.floor_surface = pygame.Surface((self.display_surface.get_size()))
        self.zahl = 0

        #creating the floor
        self.floor_surface = pygame.image.load("./graphics/Tiled/Map.png").convert()
        self.floor_surface = pygame.transform.scale(self.floor_surface,(5800,5800))
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
    
    def draw(self,ani):
       for sprite in sorted(self.sprites(),key=lambda sprite:sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image,offset_pos)

    def collision(self,player,animal):
        self.object = self.sprites()        
        for i, object1 in enumerate(self.object):
            for object2 in self.object[i+1:]:
                if pygame.sprite.collide_rect(object1, object2):
                    if isinstance(object1, Player) and isinstance(object2,  Animals):
                        self.zahl+=1
                        print("collision tier",self.zahl)

    def collision_player_harvest(self,player,):
        self.object = self.sprites()        
        for i, object1 in enumerate(self.object):
            for object2 in self.object[i+1:]:
                if pygame.sprite.collide_rect(object1, object2):
                    if isinstance(object1, Player) and isinstance(object2, Harvest):
                        player.anzahl_obst+=1
                        print("collision",player.anzahl_obst)
                        object2.status = "harvesting"
                     
                    # if player == object1 or player == object2 and  animal == object2 or animal == object1:
                        #self.zahl += 1
                        #print("collision", self.zahl)
                        #print(type(object1),type(object2))
                    
                    