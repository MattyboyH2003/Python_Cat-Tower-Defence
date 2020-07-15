import pygame
from pygame import *

########################################################################################################
#                                           - Main Class -                                             #
########################################################################################################

class Enemy:
    
    def __init__(self):
        
########################################################################################################
#                                           - Enemy Types -                                            #
########################################################################################################

class PistolCat(Enemy):

    sprite = ""

    def __init__(self, startPos, colour):
        #Instance Variables
        self.location = pygame.math.Vector2(startPos)
        self.range = 10 # 1 range unit = 10 pixel radius
        self.damage = 1  # Damage is equal to units unravelled per attack

        Towers.__init__(self, colour)
