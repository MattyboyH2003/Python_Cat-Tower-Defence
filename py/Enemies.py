import pygame
from pygame import *
import copy

########################################################################################################
#                                           - Main Class -                                             #
########################################################################################################

class Enemy(pygame.sprite.Sprite):
    
    def __init__(self, pathData, startLocation, colour):

        #Path stuff
        self.pathData = copy.deepcopy(pathData)
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

    def MoveFrame(self):

        self.currentDirection = self.pathData[0]

        print(self.location)
        print(self.nextLocation)
        print(self.currentDirection)
        print("\n")

        if self.currentDirection == "D":
            if self.location[1] + self.speed >= self.nextLocation[1]:
                self.location = copy.deepcopy(self.nextLocation)
                self.pathData.pop(0)
                if self.pathData[0] == "U":
                    self.nextLocation += Vector2(0, -20)
                elif self.pathData[0] == "L":
                    self.nextLocation += Vector2(-20, 0)
                elif self.pathData[0] == "R":
                    self.nextLocation += Vector2(20, 0)
                elif self.pathData[0] == "D":
                    self.nextLocation += Vector2(0, 20)
            else:
                self.location += Vector2(0, self.speed)
        
        elif self.currentDirection == "R":
            if self.location[0] + self.speed >= self.nextLocation[0]:
                self.location = copy.deepcopy(self.nextLocation)
                self.pathData.pop(0)
                if self.pathData[0] == "U":
                    self.nextLocation += Vector2(0, -20)
                elif self.pathData[0] == "L":
                    self.nextLocation += Vector2(-20, 0)
                elif self.pathData[0] == "R":
                    self.nextLocation += Vector2(20, 0)
                elif self.pathData[0] == "D":
                    self.nextLocation += Vector2(0, 20)
            else:
                self.location += Vector2(self.speed, 0)
        
        elif self.currentDirection == "L":
            if self.location[0] - self.speed <= self.nextLocation[0]:
                self.location = copy.deepcopy(self.nextLocation)
                self.pathData.pop(0)
                if self.pathData[0] == "U":
                    self.nextLocation += Vector2(0, -20)
                elif self.pathData[0] == "L":
                    self.nextLocation += Vector2(-20, 0)
                elif self.pathData[0] == "R":
                    self.nextLocation += Vector2(20, 0)
                elif self.pathData[0] == "D":
                    self.nextLocation += Vector2(0, 20)
            else:
                self.location += Vector2(-self.speed, 0)
        
        elif self.currentDirection == "U":
            if self.location[1] - self.speed <= self.nextLocation[1]:
                self.location = copy.deepcopy(self.nextLocation)
                self.pathData.pop(0)
                if self.pathData[0] == "U":
                    self.nextLocation += Vector2(0, -20)
                elif self.pathData[0] == "L":
                    self.nextLocation += Vector2(-20, 0)
                elif self.pathData[0] == "R":
                    self.nextLocation += Vector2(20, 0)
                elif self.pathData[0] == "D":
                    self.nextLocation += Vector2(0, 20)
            else:
                self.location += Vector2(0, -self.speed)
        
        self.rect.center = self.location

########################################################################################################
#                                           - Enemy Types -                                            #
########################################################################################################

class WoolLV1(Enemy):

    sprite = "Sprites\\Enemys\\Wool.png"

    def __init__(self, pathData, startLocation, colour):
        #Instance Variables
        self.health = 1
        self.speed = 2
        #could add speed later
        Enemy.__init__(self, pathData, startLocation, colour)
