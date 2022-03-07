import os
import pygame

class Settings(object):
    window_width = 800
    window_height = 600    
    caption = "Game"
    fps = 60

class Game(object):  # klasse game
    def __init__(self, ) -> None:
        os.environ['SDL_VIDEO_WINDOW_POS'] = "100,100"

        pygame.init()
        pygame.display.set_caption(Settings.caption)
        self.screen = pygame.display.set_mode((Settings.window_width, Settings.window_height))
        self.clock = pygame.time.Clock()
        
    def run(self):  # beim spiel start ausführen
        self.running = True
        while self.running:
            self.clock.tick(Settings.fps)
        pygame.quit()

if __name__ == '__main__':  # game start
    game = Game()
    game.run()
