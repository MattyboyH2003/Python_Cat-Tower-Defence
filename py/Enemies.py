import pygame
import copy

########################################################################################################
#                                           - Main Class -                                             #
########################################################################################################

class Enemy(pygame.sprite.Sprite):
    
    def __init__(self, pathData, startLocation, colour):

        #Path stuff
        self.pathData = copy.deepcopy(pathData)
        self.location = Vector2((startLocation[0]*20)+10, (startLocation[1]*20)+10)
        self.radius = 1
        
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

    def GetLocation(self):
        return self.location

    def MoveFrame(self):

        nextDict = { "D" : Vector2(0, 20), "U" : Vector2(0, -20), "L" : Vector2(-20, 0), "R" : Vector2(20, 0) , "END" : Vector2 (0, 0)}
        self.currentDirection = self.pathData[0]

        if self.currentDirection == "D":
            if self.location[1] + self.speed >= self.nextLocation[1]:
                self.location = copy.deepcopy(self.nextLocation)
                self.pathData.pop(0)
                self.nextLocation += nextDict[self.pathData[0]]
            else:
                self.location += Vector2(0, self.speed)
        
        elif self.currentDirection == "R":
            if self.location[0] + self.speed >= self.nextLocation[0]:
                self.location = copy.deepcopy(self.nextLocation)
                self.pathData.pop(0)
                self.nextLocation += nextDict[self.pathData[0]]
            else:
                self.location += Vector2(self.speed, 0)
        
        elif self.currentDirection == "L":
            if self.location[0] - self.speed <= self.nextLocation[0]:
                self.location = copy.deepcopy(self.nextLocation)
                self.pathData.pop(0)
                self.nextLocation += nextDict[self.pathData[0]]
            else:
                self.location += Vector2(-self.speed, 0)
        
        elif self.currentDirection == "U":
            if self.location[1] - self.speed <= self.nextLocation[1]:
                self.location = copy.deepcopy(self.nextLocation)
                self.pathData.pop(0)
                self.nextLocation += nextDict[self.pathData[0]]
            else:
                self.location += Vector2(0, -self.speed)
        
        elif self.currentDirection == "END":
            damageTemp = self.damage #allows us to store the damage to use in the return even after self is deleted
            self.kill()
            del self

            return(damageTemp)
            
        self.rect.center = self.location
        return(0)

    def TakeDamage(self, damage):
        if self.health <= damage:
            self.kill()
            del self
        else:
            self.health -= damage
    
    def getWorth(self):
        return(self.worth)

########################################################################################################
#                                           - Enemy Types -                                            #
########################################################################################################

class WoolLV1(Enemy):

    sprite = "Sprites\\Enemys\\Wool.png"
    health = 1
    speed = 2
    damage = -1 #dont forget to make this a minus as its added to the lives
    worth = 1

    def __init__(self, pathData, startLocation, colour):
        Enemy.__init__(self, pathData, startLocation, colour)

class WoolLV2(Enemy):

    sprite = "Sprites\\Enemys\\Wool2.png"
    health = 2
    speed = 5
    damage = -1 #dont forget to make this a minus as its added to the lives
    worth = 2

    def __init__(self, pathData, startLocation, colour):
        Enemy.__init__(self, pathData, startLocation, colour)

class WoolLV3(Enemy):

    sprite = "Sprites\\Enemys\\Wool3.png"
    health = 5
    speed = 3
    damage = -3 #dont forget to make this a minus as its added to the lives
    worth = 3

    def __init__(self, pathData, startLocation, colour):
        Enemy.__init__(self, pathData, startLocation, colour)