import pygame
from Colours import colours

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

    def UpdateRadius(self):
        self.radius = self.range*10

    def CheckEnemies(self, enemy, enemyList):
        if pygame.sprite.collide_circle(self, enemy):
            if pygame.time.get_ticks() >= self.timeCache: # get_ticks will give us the amount of milliseconds since program started running
                self.Attack(enemy, enemyList) 
                self.timeCache = pygame.time.get_ticks() + self.delay
                return (enemy.getWorth())
        return(0)
    
    def CalculateValueIncrease(self, price):
        price = price/5

        price = str(price).split(".")[0]

        return int(price)

    def GetSprite(self):
        return (self.sprite)

    def GetProfile(self):
        return (self.profile)

    def GetUpgrades(self):
        return self.upgrades

    def GetPrice(self):
        return(self.price)

    def GetRange(self):
        return self.range

    def GetPos(self):
        return self.location

    def GetValue(self):
        return self.value

    def RemoveExistance(self):
        self.kill()
        del self
    
    def __del__(self):
        self = None

########################################################################################################
#                                           - Tower Types -                                            #
########################################################################################################

class PistolCat(Towers): #mid range slow shooting

    sprite = "Sprites\\Towers\\Towers\\PistolCatSprite.png"
    profile = "Sprites\\Towers\\Profile\\PistolCatProfile.png"
    damage = 1  # Damage is equal to units unravelled per attack
    delay = 500
    price = 150

    def __init__(self, startPos, colour, window):
        #Instance Variables
        self.upgrades = [["Level 1", 200, self.Upgrade1], None]
        self.location = pygame.math.Vector2(startPos)
        self.range = 5 # 1 range unit = 10 pixel radius
        self.value = 75
        
        Towers.__init__(self, colour, window)

    def Attack(self, enemy, enemyList):
        pygame.draw.line(self.window, (255, 255, 255), self.rect.center, enemy.rect.center, 5)

        enemy.TakeDamage(self.damage)
    
    def Upgrade1(self):
        self.delay = 333
        self.range += 2
        self.value += self.CalculateValueIncrease(self.upgrades[0][1])

        self.upgrades = [["Level 2", 400, self.Upgrade2], None]

    def Upgrade2(self):
        self.damage += 1
        self.value += self.CalculateValueIncrease(self.upgrades[0][1])

        self.upgrades = [["Level 3", 550, self.Upgrade3], None]

    def Upgrade3(self):
        self.damage += 1
        self.range += 3
        self.value += self.CalculateValueIncrease(self.upgrades[0][1])

        self.upgrades = [["Minigun", 1100, self.Special1], ["Sniper", 900, self.Special2]]

    def Special1(self): #Minigun
        self.delay = 100
        self.value += self.CalculateValueIncrease(self.upgrades[0][1])

        self.upgrades = [["Master Minigun", 8000, self.Master1], None]

    def Special2(self): #Sniper
        self.damage += 2
        self.delay = 750
        self.range = 25
        self.value += self.CalculateValueIncrease(self.upgrades[1][1])

        self.upgrades = [None, ["Master Sniper", 7500, self.Master2]]

    def Master1(self): #Master Minigun
        self.delay = 35
        self.range += 5
        self.value += self.CalculateValueIncrease(self.upgrades[0][1])

        self.upgrades = []

    def Master2(self): #Master Sniper
        self.damage += 5
        self.delay =  500
        self.range = 50
        self.value += self.CalculateValueIncrease(self.upgrades[0][1])

        self.upgrades = []

class AngryCat(Towers): # cheap, low damage, fast attack, very close range, needs to be directly next to a path to attack

    sprite = "Sprites\\Towers\\Towers\\AngryCatSprite.png"
    profile = "Sprites\\Towers\\Profile\\AngryCatProfile.png"
    damage = 0.5 # Damage is equal to units unravelled per attack
    delay = 200
    price = 200

    def __init__(self, startPos, colour, window):
        #Instance Variables
        self.location = pygame.math.Vector2(startPos)
        self.range = 3 # 1 range unit = 10 pixel radius
        self.upgrades = [["Level 1", 200, self.Upgrade1], None]
        self.value = 40

        Towers.__init__(self, colour, window)

    def Attack(self, enemy, enemyList):
        pygame.draw.line(self.window, (255, 255, 255), self.rect.center, enemy.rect.center, 5)

        enemy.TakeDamage(self.damage)
    
    def Upgrade1(self):
        
        self.upgrades = [["Level 2", 400, self.Upgrade2], None]

    def Upgrade2(self):

        self.upgrades = [["Level 3", 550, self.Upgrade3], None]

    def Upgrade3(self):

        self.upgrades = [["Special 1", 1100, self.Special1], ["Special 2", 900, self.Special2]]

    def Special1(self):

        self.upgrades = [["Master 1", 8000, self.Master1], None]

    def Special2(self):

        self.upgrades = [None, ["Master 2", 7500, self.Master2]]

    def Master1(self):

        self.upgrades = []

    def Master2(self):

        self.upgrades = []

class StrongCat(Towers): #very expensive, high damage, short range, average attack speed, punches wool with his fists!

    sprite = "Sprites\\Towers\\Towers\\StrongCatSprite.png"
    profile = "Sprites\\Towers\\Profile\\StrongCatProfile.png"
    damage = 10 # Damage is equal to units unravelled per attack
    delay = 700
    price = 1500

    def __init__(self, startPos, colour, window):
        #Instance Variables
        self.location = pygame.math.Vector2(startPos)
        self.range = 2 # 1 range unit = 10 pixel radius
        self.upgrades = []
        self.value = 300

        Towers.__init__(self, colour, window)

    def Attack(self, enemy, enemyList):
        pygame.draw.line(self.window, (255, 255, 255), self.rect.center, enemy.rect.center, 5)

        enemy.TakeDamage(self.damage)

    def Attack(self, enemy, enemyList):
        pygame.draw.line(self.window, (255, 255, 255), self.rect.center, enemy.rect.center, 5)

        enemy.TakeDamage(self.damage)
    
    def Upgrade1(self):

        self.upgrades = []

    def Upgrade2(self):

        self.upgrades = []

    def Upgrade3(self):

        self.upgrades = []

    def Special1(self):

        self.upgrades = []

    def Special2(self):

        self.upgrades = []

    def Master1(self):

        self.upgrades = []

    def Master2(self):

        self.upgrades = []

class BombCat(Towers): # equivalent to single use spikes in bloons, returns no reward to player for pops       

    sprite = "Sprites\\Towers\\Towers\\BombCatSprite.png"
    profile = "Sprites\\Towers\\Profile\\BombCatProfile.png"
    damage = 1 # Damage is equal to units unravelled per attack
    price = 20

    def __init__(self, startPos, colour, window):
        #Instance Variables
        self.location = pygame.math.Vector2(startPos)
        self.range = 2 # 1 range unit = 10 pixel radius
        self.upgrades = []
        self.value = 4

        Towers.__init__(self, colour, window)

    def CheckEnemies(self, enemy, enemyList):
        if pygame.sprite.collide_circle(self, enemy):
            self.Attack(enemy)
        return(0)


    def Attack(self, enemy):
        enemy.kill()
        del(enemy)
        self.kill()
        del(self)
    
    def Upgrade1(self):

        self.upgrades = []

    def Upgrade2(self):

        self.upgrades = []

    def Upgrade3(self):

        self.upgrades = []

    def Special1(self):

        self.upgrades = []

    def Special2(self):

        self.upgrades = []

    def Master1(self):

        self.upgrades = []

    def Master2(self):

        self.upgrades = []

        
