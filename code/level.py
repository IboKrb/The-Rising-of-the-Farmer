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
from Game import Game

class Spiel:
    def __init__(self):
        
        #get the display surface
        self.display_surface = pygame.display.get_surface()
        
        #sprite groups
        self.visible_sprites = Camera()
        self.obstacle_sprites = pygame.sprite.Group()

        self.zahl = 0
        self.zahl_lose = 0
        self.inventory = pygame.image.load("./graphics/bio.png").convert_alpha()
        self.winner = pygame.image.load("./graphics/winner.jpg").convert_alpha()
        self.floor_surface = pygame.transform.scale(self.winner,(5800,5800))

         #sprite setup
        self.create_map()

        self.spawn_x = 0
        self.spawn_y = 0

        self.timer = 10000


    def random_spawn(self):
        self.spawn_x = randint(1600,4600)
        self.spawn_y = randint(1050,4000)

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
        for i in range(0,250):
            self.random_spawn()
            self.farm_spawn = Harvest((self.spawn_x,self.spawn_y),[self.visible_sprites],self.obstacle_sprites)
    
    

    def run(self):
        self.visible_sprites.draw(self.animal)
        self.visible_sprites.draw(self.farm_spawn)
        self.visible_sprites.custom_draw(self.player)
        self.show_player_level(self.player)
        self.draw_inventory(self.player)
        self.visible_sprites.update()
        self.visible_sprites.collision(self.player,self.animal)
        self.win(self.player)
        self.lose_game(self.player)


    def draw_inventory(self,player):
        self.display_surface.blit(self.inventory,(300,200))
        font=pygame.font.SysFont(pygame.font.get_default_font(),50)
        text=font.render(f"{player.anzahl_obst}",1,pygame.Color("Black"))
        self.display_surface.blit(text,(1050,690))
        font=pygame.font.SysFont(pygame.font.get_default_font(),50)
        text=font.render("gezähmtetiere:   "f"{player.tamet_animals}",1,pygame.Color("Black"))
        self.display_surface.blit(text,(650,690))

                
    def win(self,player):
        if player.tamet_animals == 60:
            self.zahl += 1
            self.display_surface.blit(self.winner,(400,200))
            font=pygame.font.SysFont(pygame.font.get_default_font(),50)
            text=font.render("Dein Highscore:   "f"{player.tamet_animals}",1,pygame.Color("White"))
            self.display_surface.blit(text,(450,500))
            font=pygame.font.SysFont(pygame.font.get_default_font(),40)
            text=font.render("press R to restart the game",1,pygame.Color("White"))
            self.display_surface.blit(text,(430,550))
            paused = True
            while paused and self.zahl > 20:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            print("Unpaused")
                            paused = False
                            player.tamet_animals = 0
                            self.timer = 8000

        else:
            return False

    def show_player_level(self, player):
        if player.level_up_eins and player.level_up_zwei != True: 
            font=pygame.font.SysFont(pygame.font.get_default_font(),30)
            text=font.render("Player level:2",1,pygame.Color("Black"))
            self.display_surface.blit(text,(550,450))
        elif player.level_up_eins and player.level_up_zwei : 
            font=pygame.font.SysFont(pygame.font.get_default_font(),30)
            text=font.render("Player level:3",1,pygame.Color("Black"))
            self.display_surface.blit(text,(550,450))
        else:
            font=pygame.font.SysFont(pygame.font.get_default_font(),30)
            text=font.render("Player level:1",1,pygame.Color("Black"))
            self.display_surface.blit(text,(550,450))

    def draw_pause_screen(self):
        self.screen.blit(self.pause_screen, (0, 0))
        pygame.display.flip()

    def lose_game(self,player):
        self.timer -= 1	
        if self.timer >= 0:
            font=pygame.font.SysFont(pygame.font.get_default_font(),50)
            text=font.render("verbliebendezeit:"f"{self.timer}""sekunden",1,pygame.Color("White"))
            self.display_surface.blit(text,(600,10))
        if self.timer <= 0:
            self.zahl_lose += 1
            font=pygame.font.SysFont(pygame.font.get_default_font(),80)
            text=font.render("VERLOREN",1,pygame.Color("red"))
            self.display_surface.blit(text,(450,500))
            font=pygame.font.SysFont(pygame.font.get_default_font(),40)
            text=font.render("press R to restart the game",1,pygame.Color("White"))
            self.display_surface.blit(text,(430,550))
            paused = True
            while paused and self.zahl_lose > 20:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            print("Unpaused")
                            paused = False
                            player.tamet_animals = 0
                            self.timer = 10000

class Camera(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0]//2
        self.half_height = self.display_surface.get_size()[1]//2
        self.offset = pygame.math.Vector2()
        self.floor_surface = pygame.Surface((self.display_surface.get_size()))
        self.zahl = 0
        self.dirvect = pygame.math.Vector2()
        #creating the floor
        self.floor_surface = pygame.image.load("./graphics/Tiled/Map.png").convert_alpha()
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
                        if player.anzahl_obst >= 1 and player.feeding:
                            self.zahl+=1
                            player.anzahl_obst-=1
                            player.tamet_animals += 1
                            print(player.tamet_animals)	
                            object2.rect.top = randint(800,1200)
                            object2.rect.left = randint(800,1200)

                            object2.tamet = True
                            object2.dir_player = player.direction

                    if isinstance(object1, Player) and isinstance(object2, Harvest):
                        if player.havest and object2.fram_index >= 3:
                            player.anzahl_obst+=1
                            object2.fram_index = 0
                            player.havest = False#



                    