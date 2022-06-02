import os
import pygame, sys
import Settings
from debug import debug
from level import *


class Game(object):  # klasse game
    def __init__(self ) -> None:
        os.environ['SDL_VIDEO_WINDOW_POS'] = "100,100"

        pygame.init()
        pygame.display.set_caption(Settings.caption)
        self.screen = pygame.display.set_mode((Settings.window_width, Settings.window_height))
        self.clock = pygame.time.Clock()
        self.Level = Level()

    def run(self):  # beim spiel start ausführen
        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()  

            self.draw()
            self.Level.run()
            
            pygame.display.update()
            self.clock.tick(Settings.fps)

    def draw(self):  
        self.screen.fill("lightBlue")
        

if __name__ == '__main__':  # game start
    game = Game()
    game.run()
