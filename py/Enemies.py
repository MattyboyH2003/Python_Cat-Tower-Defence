import pygame
from pygame import *

########################################################################################################
#                                           - Main Class -                                             #
########################################################################################################

class Enemy(pygame.sprite.Sprite):
    
    def __init__(self, pathData, startLocation, colour):

        #Path stuff
        self.pathData = pathData
        self.location = Vector2((startLocation[0]*20)+10, (startLocation[1]*20)+10)
        
        if self.pathData[0] == "U":
            self.nextLocation = self.location + Vector2(0, -20)
        elif self.pathData[0] == "L":
            self.nextLocation = self.location + Vector2(-20, 0)
        elif self.pathData[0] == "R":
            self.nextLocation = self.location + Vector2(20, 0)
        elif self.pathData[0] == "D":
            self.nextLocation = self.location + Vector2(0, 20)
        else:
            print(self.pathData[0])

        #Sprite stuff
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

    """
    def MoveFrame(self):
        print(self.pathData)
        if self.pathData[0] == "U":
            if self.location[1]-self.speed <= self.nextLocation[1]:
                self.location = self.nextLocation
                self.pathData.pop(0)
                if self.pathData[0] == "U":
                    self.nextLocation = self.location + Vector2(0, -20)
                elif self.pathData[0] == "L":
                    self.nextLocation = self.location + Vector2(-20, 0)
                elif self.pathData[0] == "R":
                    self.nextLocation = self.location + Vector2(20, 0)
                elif self.pathData[0] == "D":
                    self.nextLocation = self.location + Vector2(0, 20)
            else:
                self.location += Vector2(0, -self.speed)
        
        elif self.pathData[0] == "L":
            if self.location[0]-self.speed <= self.nextLocation[0]:
                self.location = self.nextLocation
                self.pathData.pop(0)
                if self.pathData[0] == "U":
                    self.nextLocation = self.location + Vector2(0, -20)
                elif self.pathData[0] == "L":
                    self.nextLocation = self.location + Vector2(-20, 0)
                elif self.pathData[0] == "R":
                    self.nextLocation = self.location + Vector2(20, 0)
                elif self.pathData[0] == "D":
                    self.nextLocation = self.location + Vector2(0, 20)
            else:
                self.location = self.location + Vector2(-self.speed, 0)
        
        elif self.pathData[0] == "R":
            if self.location[0]+self.speed >= self.nextLocation[0]:
                self.location = self.nextLocation
                self.pathData.pop(0)
                if self.pathData[0] == "U":
                    self.nextLocation = self.location + Vector2(0, -20)
                elif self.pathData[0] == "L":
                    self.nextLocation = self.location + Vector2(-20, 0)
                elif self.pathData[0] == "R":
                    self.nextLocation = self.location + Vector2(20, 0)
                elif self.pathData[0] == "D":
                    self.nextLocation = self.location + Vector2(0, 20)
            else:
                self.location = self.location + Vector2(self.speed, 0)
        
        elif self.pathData[0] == "D":
            if self.location[1]+self.speed >= self.nextLocation[1]:
                self.location = self.nextLocation
                self.pathData.pop(0)
                if self.pathData[0] == "U":
                    self.nextLocation = self.location + Vector2(0, -20)
                elif self.pathData[0] == "L":
                    self.nextLocation = self.location + Vector2(-20, 0)
                elif self.pathData[0] == "R":
                    self.nextLocation = self.location + Vector2(20, 0)
                elif self.pathData[0] == "D":
                    self.nextLocation = self.location + Vector2(0, 20)
            else:
                self.location = self.location + Vector2(0, self.speed)
        
        self.rect.center = self.location
        """

        def MoveFrame(self):
            
########################################################################################################
#                                           - Enemy Types -                                            #
########################################################################################################

class WoolLV1(Enemy):

    sprite = "Sprites\\Enemys\\Wool.png"

    def __init__(self, pathData, startLocation, colour):
        #Instance Variables
        self.health = 1
        self.speed = 1
        #could add speed later
        Enemy.__init__(self, pathData, startLocation, colour)
