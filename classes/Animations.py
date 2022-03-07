import pygame
import os

class Animations():
    def __init__(self):
        path_file = os.path.dirname(os.path.abspath(__file__))
        path_image = os.path.join(path_file, "images")