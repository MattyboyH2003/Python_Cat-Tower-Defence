import pygame
from pygame import *

########################################################################################################
#                                           - Main Class -                                             #
########################################################################################################

class Enemy(pygame.sprite.Sprite):
    
    def __init__(self):

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


    #do not use
    def FrameMove(self, endPos, speed = 1):
        
        #((speed * 20)/30) = 
        
        numOfIterations = 30
        startPos = self.rect.center
        distance = 1/ numOfIterations
        for i in range(numOfIterations):
            self.rect.center = startPos.lerp(endPos, distance * i)
        
        
########################################################################################################
#                                           - Enemy Types -                                            #
########################################################################################################

class WoolLV1(Enemy):

    sprite = "Sprites\\Enemys\\Wool.png"

    def __init__(self, startPos, colour):
        #Instance Variables
        self.health = 1
        #could add speed later
        Enemy.__init__(self, colour)
