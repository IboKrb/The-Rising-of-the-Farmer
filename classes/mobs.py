import pygame
from Animations import *

class Lebewesen():
    def __init__(self,gesundheit,name,lvl,typ,stärker):
        self.gesundheit = gesundheit
        self.name = name
        self.lvl = lvl
        self.typ = typ
        self.stärker = stärker

class Player(Lebewesen):
    def __init__(self,inventory,gesundheit,name,lvl,typ,stärker):
        super().__init__(gesundheit,name,lvl,typ,stärker)
        self.inventory = inventory
        
        
class Dämonen(Lebewesen):
    def __init__(self,gesundheit,name,lvl,typ,stärker):
        super().__init__(gesundheit,name,lvl,typ,stärker)
        
        
class Tiere (Lebewesen):
    def __init__(self,gesundheit,name,lvl,typ,stärker):
        super().__init__(gesundheit,name,lvl,typ,stärker)


        
