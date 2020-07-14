import pygame
from Towers import *
from Tiles import *
import time

########################################################################################################
#                                              - Setup -                                               #
########################################################################################################
if __name__ == "__main__":
    pygame.init()

    resolution = (1280, 720)
    pygame.display.set_caption("Cat Shooty Game")
    window = pygame.display.set_mode(resolution)
    windowIcon = pygame.image.load("Sprites\GUI\WindowIcon.png")
    pygame.display.set_icon(windowIcon)
    background = pygame.image.load("Sprites\Maps\map.png")

    clock = pygame.time.Clock() 
else:
    exit()

########################################################################################################
#                                              - Classes -                                             #
########################################################################################################

class Main():

    #Colours
    red = (200,0,0)
    green = (0,200,0)
    bright_red = (255,0,0)
    bright_green = (0,255,0)
    white = (255,255,255)
    black = (0,0,0)

    currentTower = PistolCat
    towers = Towers()

    towerSpritesList = pygame.sprite.Group()
    tileSpritesList = pygame.sprite.Group()
    collisionSpritesList = pygame.sprite.Group()
    allSpritesList = pygame.sprite.Group()

    def gameIntro(self): #The Menu screen Loop, called on play
        intro = True

        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                    
            window.fill(self.white)
            largeText = pygame.font.SysFont("comicsansms",115)
            TextSurf, TextRect = text_objects("Angry Cats", largeText)
            TextRect.center = ((resolution[0]/2),(resolution[1]/2))
            window.blit(TextSurf, TextRect)

            button("Play!",150,450,100,50,self.green,self.bright_green,self.GenerateMap)
            button("Quit",550,450,100,50,self.red,self.bright_red,quit)
            
            pygame.display.update()
            clock.tick(30)
    
    def GenerateMap(self): #Ran just before game loop to generate the map
        
        """
        Tile Key:
        # - Grass
        P - Path
        < - Start From Left
        > - Start From Right
        ^ - Start From Bottom
        / - Start From Top
        , - End On Left
        . - End On Right
        6 - End On Bottom
        ? - End On Top
        """

        mapFile = open("Sprites\\Maps\\map.txt", "r")
        fileContents = mapFile.readlines()
        mapString = ""
        for item in fileContents:
            mapString += item.replace("\n", "")

        counter = 0
        for char in mapString:
            if char == "#":
                nextTile = Ground
            elif char == "P":
                nextTile = Path
            elif char == "/":
                nextTile = StartDown
            elif char == "6":
                nextTile = EndDown
            location = [((counter%54)*20)+10, ((counter//54)*20)+10]
            tile = nextTile(location, self.white)

            self.allSpritesList.add(tile)
            self.tileSpritesList.add(tile)

            if nextTile != Ground:
                self.collisionSpritesList.add(tile)

            counter += 1
        
        self.gameLoop()

    def gameLoop(self): #The Main game loop, called when play is clicked  
        running = True
        while running == True:

            #Checking for events each frame
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.PlaceTower()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.currentTower = PistolCat
                    if event.key == pygame.K_RIGHT:
                        self.currentTower = AngryCat

            pygame.display.update()
            self.allSpritesList.draw(window)
            clock.tick(30)

    def PlaceTower(self): #Ran to spawn towers at the mouse position upon click
        """
        To place a tower you will need:
        A sprite (defined in the tower's class data)
        The Location of the tower (Defined by the mouse position)
        To Create an instance of that towers class
        """

        mousePositon = pygame.mouse.get_pos()
        tower = self.currentTower(mousePositon, self.white)

        if pygame.sprite.spritecollide(tower, self.collisionSpritesList, True) == []:
            self.towerSpritesList.add(tower)
            self.collisionSpritesList.add(tower)
            self.allSpritesList.add(tower)
        else:
            tower.kill()
            del tower

        #window.blit(pygame.image.load(self.currentTower.GetSprite()), mousePositon) #Need to replace blits with sprites


########################################################################################################
#                                             - Functions -                                            #
########################################################################################################

#Used in the main menu
def button(msg,x,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(window, ac,(x,y,w,h))

        if click[0] == 1 and action != None:
            action()         
    else:
        pygame.draw.rect(window, ic,(x,y,w,h))

    smallText = pygame.font.SysFont("comicsansms",20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    window.blit(textSurf, textRect)
def text_objects(text, font):
    black = (0,0,0)
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

########################################################################################################
#                                             - MainLoop -                                             #
########################################################################################################
main = Main()
main.gameIntro()
pygame.quit()
quit()