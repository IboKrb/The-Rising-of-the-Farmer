import os
import pygame, sys
import Settings
from debug import debug
from level import *
from pygame.locals import *


class Game(object):  # klasse game
    def __init__(self ) -> None:
        os.environ['SDL_VIDEO_WINDOW_POS'] = "100,100"
        pygame.init()
        pygame.display.set_caption(Settings.caption)
        self.screen = pygame.display.set_mode((Settings.window_width, Settings.window_height))	
        self.clock = pygame.time.Clock()
        self.pause_screen_main = pygame.image.load("./graphics/paus.png").convert_alpha()
        self.pause_screen = pygame.transform.scale(self.pause_screen_main,(Settings.window_width+ 80, Settings.window_height))


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

    def input(self):
        pressed = pygame.key.get_pressed() 
        if pressed[pygame.K_p]:
            self.pause_game()

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
            self.spiel.run()
            #self.sound_hintergund.play()
            pygame.display.update()
            self.clock.tick(Settings.fps)


    def draw(self):  
        self.screen.fill("lightBlue")


if __name__ == '__main__':  # game start
    game = Game()
    game.run()
