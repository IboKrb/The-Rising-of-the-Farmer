import os
import pygame, sys
import Settings
from debug import debug
from level import *
from pygame.locals import *

"""
Spiel ziel ist es 60 tiere zu zähmen in den man sie Füttert man hat nur begrenzt zeit und musst noch obst ernten

"""
class Game(object):  # klasse game
    def __init__(self ) -> None:
        os.environ['SDL_VIDEO_WINDOW_POS'] = "100,100"
        pygame.init()
        pygame.display.set_caption(Settings.caption)
        self.screen = pygame.display.set_mode((Settings.window_width, Settings.window_height),FULLSCREEN)	
        self.clock = pygame.time.Clock()
        self.pause_screen_main = pygame.image.load("./graphics/paus.png").convert_alpha()
        self.pause_screen = pygame.transform.scale(self.pause_screen_main,(Settings.window_width+ 80, Settings.window_height))
        self.start_screen = pygame.image.load("./graphics/startscreen.png").convert_alpha()
        self.start_screen = pygame.transform.scale(self.start_screen,(Settings.window_width, Settings.window_height))
        self.game_start = False
        self.spiel = Spiel()
        
    def pause_game(self):
        paused = True
        while paused:
            print("Paused")
            self.draw_pause_screen()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        print("Unpaused")
                        paused = False


    def draw_pause_screen(self):
        self.screen.blit(self.pause_screen, (0, 0))
        pygame.display.flip()



    def run(self):  # beim spiel start ausführen
        self.running = True
        while self.running:
            for event in pygame.event.get():
                pressed = pygame.key.get_pressed() 
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif pressed[pygame.K_ESCAPE]:
                    self.running = False
                    sys.exit()  
                elif pressed[pygame.K_p]:
                    self.pause_game()

            self.draw()
            pygame.display.update()
            self.clock.tick(Settings.fps)


    def draw(self):  
        self.screen.fill("lightBlue")
        if self.game_start == False:
            self.screen.blit(self.start_screen, (0, 0))
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_RETURN] :
            self.game_start = True
        if self.game_start :
            self.spiel.run()


if __name__ == '__main__':  # game start
    game = Game()
    game.run()
