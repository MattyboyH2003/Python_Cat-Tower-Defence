import pygame
from Towers import *
from Tiles import *
from Waves import allWaves
from Enemies import *

########################################################################################################
#                                              - Setup -                                               #
########################################################################################################

if __name__ == "__main__":
    pygame.init()

    resolution = (1280, 720)
    pygame.display.set_caption("Cat Shooty Game")
    window = pygame.display.set_mode(resolution)
    windowIcon = pygame.image.load("Sprites\\GUI\\WindowIcon.png")
    pygame.display.set_icon(windowIcon)

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
    lavender = (150, 150, 200)
    bright_lavender = (150, 150, 255)
    bright_red = (255,0,0)
    bright_green = (0,255,0)
    white = (255,255,255)
    black = (0,0,0)

    enemyDict = {"a" : WoolLV1, "b" : WoolLV2, "c" : WoolLV3}
    currentTower = PistolCat
    currentWave = allWaves.pop(0)
    frameDelay = 0
    frameCache = 0
    lives = 100
    money = 200
    waveNum = 0
    deleting = False

    buttonList = []

    towerSpritesList = pygame.sprite.Group() # stores all towers placed, used to check when enemies are in range of towers
    tileSpritesList = pygame.sprite.Group() # stores all tiles that make up the map, not currently used
    collisionSpritesList = pygame.sprite.Group() #used in towerplacment, if anything in this list is touching a tower it will not be placed
    enemySpritesList = pygame.sprite.Group() #used in the movement system, everything in here will follow the path and should be enemy class
    allSpritesList = pygame.sprite.Group() #list of things to be drawn to screen
    
    def gameLoop(self): #The Main game loop, called when play is clicked
        self.running = True
        self.waveOngoing = False
        self.buttonList = []
        
        #Adds button information to the list of buttons
        self.buttonList.append({"text" : "Start!", "xPos" : 1080, "yPos" : 600, "width" : 200, "height" : 120, "colour" : self.lavender, "hoverColour" : self.bright_lavender, "func" : self.StartWave})
        self.buttonList.append({"text" : "Back!", "xPos" : 1230, "yPos" : 0, "width" : 50, "height" : 50, "colour" : self.red, "hoverColour" : self.bright_red, "func" : self.BackToMenu})
        self.buttonList.append({"text" : "Delete", "xPos" : 0, "yPos" : 600, "width" : 50, "height" : 50, "colour" : self.red, "hoverColour" : self.bright_red, "func" : self.toggleDelete})

        while self.running == True:

            #Image UI
            SelectGUIImage = pygame.image.load("Sprites\\GUI\\Outline.png")
            window.blit(SelectGUIImage, (1080,0))

            SelectGUIImage = pygame.image.load("Sprites\\GUI\\LivesHeart.png")
            window.blit(SelectGUIImage, (1157,15))

            #Text UI
            largeText = pygame.font.SysFont("comicsansms",30)
            TextSurf, TextRect = text_objects(str(self.lives), largeText)
            TextRect.center = ((1204),(25))
            window.blit(TextSurf, TextRect)

            largeText = pygame.font.SysFont("comicsansms",30)
            TextSurf, TextRect = text_objects(str(self.money), largeText)
            TextRect.center = ((1120),(25))
            window.blit(TextSurf, TextRect)

            largeText = pygame.font.SysFont("comicsansms",30)
            TextSurf, TextRect = text_objects("Wave "+ str(self.waveNum), largeText)
            TextRect.center = ((540),(700))
            window.blit(TextSurf, TextRect)


            #Checking for events each frame
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.deleting == True:
                        pos = pygame.mouse.get_pos()
                        clicked = [s for s in self.towerSpritesList if s.rect.collidepoint(pos)]
                        if len(clicked) >= 1:
                            self.money += clicked[0].getPrice()
                            clicked[0].kill()
                            del clicked[0]
                        self.deleting = False
                    else:
                        for button in self.buttonList:
                            AreaClick(**button)
                        mouse = pygame.mouse.get_pos()
                        if 1080 > mouse[0] > 0 and 600 > mouse[1] > 0:
                            self.PlaceTower()

                    
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.currentTower = PistolCat
                    if event.key == pygame.K_RIGHT:
                        self.currentTower = AngryCat

            #updates buttons
            for button in self.buttonList:
                ButtonVisuals(**button)
            
            #all towers check and attack, currently prints when detects nearby towers
            for enemy in self.enemySpritesList:
                for tower in self.towerSpritesList:
                    self.money += tower.CheckEnemies(enemy)
            
            #Move Wool
            for item in self.enemySpritesList:
                self.lives += item.MoveFrame()

            #Spawn Wool
            if self.frameDelay == 0:
                if len(self.currentWave) > 0:
                    nextThing = self.currentWave[0]

                    if type(nextThing) == type(1):
                        self.frameDelay = int(nextThing)
                    
                    elif type(nextThing) == type("a"):
                        enemy = self.enemyDict[nextThing](self.pathList, self.startTilePos, self.white)
                        self.enemySpritesList.add(enemy)
                        self.allSpritesList.add(enemy)
                    

                    self.currentWave.pop(0)
            else:
                self.frameDelay -= 1

            #Check For end of game
            if self.lives <= 0:
                self.lives = 0 #stop it counting down further after loss screen
                self.gameEnd()

            #Check for end of wave
            if self.waveOngoing:
                if len(self.enemySpritesList) <= 0 and len(self.currentWave) <= 0:
                    self.money += self.waveReward
                    self.waveOngoing = False
                    if len(allWaves) <= 0:
                        self.gameEnd("you win!")

            #Final stuff
            pygame.display.update()
            window.fill((255, 255, 255))
            self.allSpritesList.draw(window)
            clock.tick(30)

    def gameEnd(self, state = "you lose"):
        
        self.buttonList = []
        self.buttonList.append({"text" : "Quit!", "xPos" : 550, "yPos": 450, "width" : 100, "height" : 50, "colour" : self.red, "hoverColour" : self.bright_red, "func" : quit})

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button in self.buttonList:
                        AreaClick(**button)
                    
            window.fill(self.white)
            largeText = pygame.font.SysFont("comicsansms",115)
            TextSurf, TextRect = text_objects(state, largeText)
            TextRect.center = ((resolution[0]/2),(resolution[1]/2))
            window.blit(TextSurf, TextRect)

            for button in self.buttonList:
                ButtonVisuals(**button)
            
            pygame.display.update()
            clock.tick(30)

    def gameIntro(self): #The Menu screen Loop, called on play
        intro = True

        self.buttonList = []
        self.buttonList.append({"text" : "Play!", "xPos" : 150, "yPos" : 450, "width" : 100, "height" : 50, "colour" : self.green, "hoverColour" : self.bright_green, "func" : self.GenerateMap})
        self.buttonList.append({"text" : "Quit!", "xPos" : 550, "yPos": 450, "width" : 100, "height" : 50, "colour" : self.red, "hoverColour" : self.bright_red, "func" : quit})
        
        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button in self.buttonList:
                        AreaClick(**button)
                    
            window.fill(self.white)
            largeText = pygame.font.SysFont("comicsansms",115)
            TextSurf, TextRect = text_objects("Angry Cats", largeText)
            TextRect.center = ((resolution[0]/2),(resolution[1]/2))
            window.blit(TextSurf, TextRect)

            for button in self.buttonList:
                ButtonVisuals(**button)

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

        mapFile = open("Data\\Maps\\map.txt", "r")
        fileContents = mapFile.readlines()
        mapFile.close()
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
            tile = nextTile(location, self.red)

            self.allSpritesList.add(tile)
            self.tileSpritesList.add(tile)

            if nextTile != Ground:
                self.collisionSpritesList.add(tile)

            counter += 1

        self.GeneratePath()

    def GeneratePath(self): #Ran after generating the map
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

        mapFile = open("Data\\Maps\\map.txt", "r")
        fileContents = mapFile.readlines()
        mapFile.close()

        mapArray = []
        for item in fileContents:
            tempList = []
            for char in item:
                if char != "\n":
                    tempList.append(char)
            mapArray.append(tempList)
        
        """
        Path Array format:
        U - Go Up
        L - Go Left
        R - Go right
        D - Go Down
        """

        self.pathList = []
        
        row = 0
        column = 0

        startList = ["^", "<", ">", "/"]
        for layer in mapArray:
            for tile in layer:
                for item in startList:
                    if tile == item:
                        self.startTilePos = [column, row]
                        checkPos = [row, column]

                column += 1
            column = 0
            row += 1

        print("Located start tile position, it is: {}".format(str(checkPos)))

        endList = [",", ".", "6", "?"]
        path = True
        while path == True: #Starts going until the path is complete
            if checkPos[0] != 0: #Checks the tile above
                if mapArray[checkPos[0]-1][checkPos[1]] == "P": #Checks for path
                    self.pathList.append("U")
                    mapArray[checkPos[0]][checkPos[1]] = "#"
                    checkPos[0] = checkPos[0]-1
                    continue
                else:
                    for item in endList: #Checks for end
                        if mapArray[checkPos[0]-1][checkPos[1]] == item:
                            self.pathList.append("U")
                            self.pathList.append("END")
                            path = False
            
            if checkPos[0] != 29: #Checks the tile below
                if mapArray[checkPos[0]+1][checkPos[1]] == "P": #Checks for path
                    self.pathList.append("D")
                    mapArray[checkPos[0]][checkPos[1]] = "#"
                    checkPos[0] = checkPos[0]+1
                    continue
                else:
                    for item in endList: #Checks for end
                        if mapArray[checkPos[0]+1][checkPos[1]] == item:
                            self.pathList.append("D")
                            self.pathList.append("END")
                            path = False
            
            if checkPos[1] != 0: #Checks the tile to the left
                if mapArray[checkPos[0]][checkPos[1]-1] == "P": #Checks for path
                    self.pathList.append("L")
                    mapArray[checkPos[0]][checkPos[1]] = "#"
                    checkPos[1] = checkPos[1]-1
                    continue
                else:
                    for item in endList: #Checks for end
                        if mapArray[checkPos[0]][checkPos[1]-1] == item:
                            self.pathList.append("L")
                            self.pathList.append("END")
                            path = False
            
            if checkPos[1] != 53: #Checks the tile to the right
                if mapArray[checkPos[0]][checkPos[1]+1] == "P": #Checks for path
                    self.pathList.append("R")
                    mapArray[checkPos[0]][checkPos[1]] = "#"
                    checkPos[1] = checkPos[1]+1
                    continue
                else:
                    for item in endList: #Checks for end
                        if mapArray[checkPos[0]][checkPos[1]+1] == item:
                            self.pathList.append("R")
                            self.pathList.append("END")
                            path = False
        self.gameLoop()

    def BackToMenu(self):
        self.buttonList = []
        self.buttonList.append({"text" : "Play!", "xPos" : 150, "yPos" : 450, "width" : 100, "height" : 50, "colour" : self.green, "hoverColour" : self.bright_green, "func" : self.GenerateMap})
        self.buttonList.append({"text" : "Quit!", "xPos" : 550, "yPos": 450, "width" : 100, "height" : 50, "colour" : self.red, "hoverColour" : self.bright_red, "func" : quit})
        self.running = False

    def StartWave(self):
        if not self.waveOngoing:
            currentWaveData = allWaves.pop(0)
            self.currentWave = currentWaveData[0]
            self.waveReward = currentWaveData[1]
            self.waveOngoing = True
            self.waveNum += 1

    def toggleDelete(self):
        self.deleting = True

    def PlaceTower(self): #Ran to spawn towers at the mouse position upon click
        """
        To place a tower you will need:
        A sprite (defined in the tower's class data)
        The Location of the tower (Defined by the mouse position)
        To Create an instance of that towers class
        """

        mousePositon = pygame.mouse.get_pos()
        self.tower = self.currentTower(mousePositon, self.white, window)

        if pygame.sprite.spritecollide(self.tower, self.collisionSpritesList, False) == [] and self.money >= self.tower.getPrice():
            self.towerSpritesList.add(self.tower)
            self.collisionSpritesList.add(self.tower)
            self.allSpritesList.add(self.tower)
            self.money -= self.tower.getPrice()
        else:
            self.tower.kill()
            del self.tower

        #window.blit(pygame.image.load(self.currentTower.GetSprite()), mousePositon) #Need to replace blits with sprites

########################################################################################################
#                                            - Functions -                                             #
########################################################################################################

#Used in the main menu
def AreaClick(xPos, yPos, width, height, func, **kwargs):
    mouse = pygame.mouse.get_pos()
    if xPos+width > mouse[0] > xPos and yPos+height > mouse[1] > yPos:
        func()

def ButtonVisuals(text, xPos, yPos, width, height , colour, hoverColour, **kwargs):
    mouse = pygame.mouse.get_pos()
    if xPos+width > mouse[0] > xPos and yPos+height > mouse[1] > yPos:
        pygame.draw.rect(window, colour,(xPos,yPos,width,height))
    else:
        pygame.draw.rect(window, hoverColour,(xPos,yPos,width,height))

    smallText = pygame.font.SysFont("comicsansms",20)
    textSurf, textRect = text_objects(text, smallText)
    textRect.center = ( (xPos+(width/2)), (yPos+(height/2)) )
    window.blit(textSurf, textRect)

def text_objects(text, font):
    black = (0,0,0)
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

########################################################################################################
#                                          - Call Functions -                                           #
########################################################################################################
main = Main()
main.gameIntro()
pygame.quit()
quit()