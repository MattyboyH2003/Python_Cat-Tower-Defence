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

    towers = Towers()
    
    TowersList = []

    #Colours
    red = (200,0,0)
    green = (0,200,0)
    bright_red = (255,0,0)
    bright_green = (0,255,0)
    white = (255,255,255)
    black = (0,0,0)
else:
    exit()

########################################################################################################
#                                             - Functions -                                            #
########################################################################################################

def PlaceTower(currentTower):
    mousePositon = pygame.mouse.get_pos()

    window.blit(pygame.image.load(currentTower.GetSprite()), mousePositon)
    """
    To place a tower you will need:
    A sprite (defined in the tower's class data)
    The Location of the tower (Defined by the mouse position)
    To Create an instance of that towers class
    """

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
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

#Main Menu
def game_intro():
    
    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        window.fill(white)
        largeText = pygame.font.SysFont("comicsansms",115)
        TextSurf, TextRect = text_objects("Angry Cats", largeText)
        TextRect.center = ((resolution[0]/2),(resolution[1]/2))
        window.blit(TextSurf, TextRect)

        button("Play!",150,450,100,50,green,bright_green,GenerateMap)
        button("Quit",550,450,100,50,red,bright_red,quit)
        
        pygame.display.update()
        clock.tick(30)

def GenerateMap():

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
            nextTile = pygame.image.load("Sprites\Tiles\Grass.png")
        elif char == "P":
            nextTile = pygame.image.load("Sprites\Tiles\Path.png")
        elif char == "/":
            nextTile = pygame.image.load("Sprites\Tiles\StartDown.png")
        elif char == "6":
            nextTile = pygame.image.load("Sprites\Tiles\EndDown.png")
        location = [(counter%54)*20, (counter//54)*20]
        window.blit(nextTile, location)

        counter += 1
    
    gameLoop()

########################################################################################################
#                                             - MainLoop -                                             #
########################################################################################################
def gameLoop():
    time.sleep(1)
    currentTower = PistolCat
    running = True
    while running == True:

        #Checking for events each frame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONUP:
                PlaceTower(currentTower)
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    currentTower = PistolCat
                if event.key == pygame.K_RIGHT:
                    currentTower = AngryCat

        #window.blit(background, [0, 0])
        pygame.display.update()
        clock.tick(30)

game_intro()

pygame.quit()
quit()