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

    def __init__(self, colour, window):

        #Sets sprites
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)    
        
        self.window = window
    
        # Load the image
        self.image = pygame.image.load(self.sprite).convert()
    
        # Set our transparent color
        self.image.set_colorkey(colour)

        #set up rectangle locations
        self.rect = self.image.get_rect()
        self.rect.center = self.location

        #radius for collisions
        self.radius = self.range*10

        self.timeCache = 0

    def CheckEnemies(self, enemy):
        if pygame.sprite.collide_circle(self, enemy):
            if pygame.time.get_ticks() >= self.timeCache: # get_ticks will give us the amount of milliseconds since program started running
                self.Attack(enemy) 
                self.timeCache = pygame.time.get_ticks() + self.delay
                return (enemy.getWorth())
        return(0)
        
    def GetSprite(self):
        return self.sprite

    def getPrice(self):
        return(self.price)

    def RemoveExistance(self):
        self.kill()
        del self
 
########################################################################################################
#                                           - Tower Types -                                            #
########################################################################################################

class PistolCat(Towers): #mid range slow shooting

    sprite = "Sprites\\Towers\\PistolCatSprite.png"
    damage = 1  # Damage is equal to units unravelled per attack
    delay = 500
    price = 150

    def __init__(self, startPos, colour, window):
        #Instance Variables
        self.location = pygame.math.Vector2(startPos)
        self.range = 5 # 1 range unit = 10 pixel radius
        
        Towers.__init__(self, colour, window)

    def Attack(self, enemy):
        pygame.draw.line(self.window, (255, 255, 255), self.rect.center, enemy.rect.center, 5)

        enemy.TakeDamage(self.damage)

class AngryCat(Towers): # cheap, low damage, fast attack, very close range, needs to be directly next to a path to attack

    sprite = "Sprites\\Towers\\AngryCatSprite.png"
    damage = 0.5 # Damage is equal to units unravelled per attack
    delay = 200
    price = 200

    def __init__(self, startPos, colour, window):
        #Instance Variables
        self.location = pygame.math.Vector2(startPos)
        self.range = 2 # 1 range unit = 10 pixel radius

        Towers.__init__(self, colour, window)

    def Attack(self, enemy):
        pygame.draw.line(self.window, (255, 255, 255), self.rect.center, enemy.rect.center, 5)

        enemy.TakeDamage(self.damage)

class StrongCat(Towers): # very expensive, high damage, short range, average attack speed, punches wool with his fists!

    sprite = "Sprites\\Towers\\StrongCatSprite.png"
    damage = 10 # Damage is equal to units unravelled per attack
    delay = 700
    price = 1500

    def __init__(self, startPos, colour, window):
        #Instance Variables
        self.location = pygame.math.Vector2(startPos)
        self.range = 2 # 1 range unit = 10 pixel radius

        Towers.__init__(self, colour, window)

    def Attack(self, enemy):
        pygame.draw.line(self.window, (255, 255, 255), self.rect.center, enemy.rect.center, 5)

        enemy.TakeDamage(self.damage)

class AOECat(Towers): # weak area of effect damage on all balloons around balloon attacked, main balloon takes alot of damage, very slow attack          

    sprite = "Sprites\\Towers\\StrongCatSprite.png"
    damage = 1 # Damage is equal to units unravelled per attack
    delay = 700
    price = 200

    def __init__(self, startPos, colour, window):
        #Instance Variables
        self.location = pygame.math.Vector2(startPos)
        self.range = 2 # 1 range unit = 10 pixel radius

        Towers.__init__(self, colour, window)

    def CheckEnemies(self, enemy, enemyList):
        if pygame.sprite.collide_circle(self, enemy):
            if pygame.time.get_ticks() >= self.timeCache: # get_ticks will give us the amount of milliseconds since program started running
                self.Attack(enemy, enemyList)
                self.timeCache = pygame.time.get_ticks() + self.delay  
                return (enemy.getWorth())

        return(0)

    def Attack(self, enemy, enemyList):
        enemiesInArea = []
        for item in enemyList:
            if pygame.sprite.collide_circle(enemy, item):
                enemiesInArea.append(item)
        print("damaging all items in list:", enemiesInArea)
        pygame.draw.line(self.window, (255, 255, 255), self.rect.center, enemy.rect.center, 5)
        enemy.TakeDamage(10)
        for item in enemiesInArea:
            item.TakeDamage(1)
        




 