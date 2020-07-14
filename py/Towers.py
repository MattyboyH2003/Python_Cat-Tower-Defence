import pygame
from pygame import *

########################################################################################################
#                                           - Main Class -                                             #
########################################################################################################

class Towers(pygame.sprite.Sprite):
    """
    Types of towers:
    Pistol Cat
    Rifler Cat
    Ranger Cat
    Angry Cat
    """

    def __init__(self):
        self.temp = 1
 
########################################################################################################
#                                           - Tower Types -                                            #
########################################################################################################

class PistolCat(Towers):

    sprite = "Sprites\Towers\PistolCatSprite.png"

    def __init__(self, startPos):
        #Variables
        self.location = pygame.math.Vector2(startPos)
        self.range = 10 # 1 range unit = 10 pixel radius
        self.damage = 1  # Damage is equal to units unravelled per attack
        #Sets sprites

        


    @classmethod
    def GetSprite(cls):
        return cls.sprite

class AngryCat(Towers):

    sprite = "Sprites\Towers\AngryCatSprite.png"

    def __init__(self):
        self.range = 2 # 1 range unit = 10 pixel radius
        self.damage = 1 # Damage is equal to units unravelled per attack
        self.location = math.Vector2()
    
    @classmethod
    def GetSprite(cls):
        return cls.sprite