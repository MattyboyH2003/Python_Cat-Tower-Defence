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

    def __init__(self, colour = None):

        #Sets sprites
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)    
    
        # Load the image
        self.image = pygame.image.load(self.sprite).convert()
    
        # Set our transparent color
        self.image.set_colorkey(colour)
        self.rect = self.image.get_rect()
        self.rect.center = self.location

        
    def GetSprite(self):
        return self.sprite

    def RemoveExistance(self):
        self.kill()
        del self
 
########################################################################################################
#                                           - Tower Types -                                            #
########################################################################################################

class PistolCat(Towers):

    sprite = "Sprites\\Towers\\PistolCatSprite.png"

    def __init__(self, startPos, colour):
        #Instance Variables
        self.location = pygame.math.Vector2(startPos)
        self.range = 10 # 1 range unit = 10 pixel radius
        self.damage = 1  # Damage is equal to units unravelled per attack

        Towers.__init__(self, colour)



class AngryCat(Towers):

    sprite = "Sprites\\Towers\\AngryCatSprite.png"

    def __init__(self, startPos, colour):
        #Instance Variables
        self.location = pygame.math.Vector2(startPos)
        self.range = 2 # 1 range unit = 10 pixel radius
        self.damage = 1  # Damage is equal to units unravelled per attack

        Towers.__init__(self, colour)
