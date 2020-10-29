import copy
import pygame
from Towers import *
from Tiles import *
from Enemies import *
from Waves import allWaves
from Colours import *
from MapList import MapList, AllMaps, AllMapProfiles

#when enabled print statements for testing purposes will show

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

class Main:
    enemyDict = {"a" : WoolLV1, "b" : WoolLV2, "c" : WoolLV3}
    towerList = [PistolCat, AngryCat, StrongCat, BombCat]
    currentWave = allWaves.pop(0)
    frameDelay = 0
    frameCache = 0
    lives = 100
    money = 200
    waveNum = -1
    upgrading = False
    currentTower = 0
    previousTower = 0
    selectedTower = None
    previousSelectedTower = None
    currentMap = ""
    updateUpgrades = False
    TowerSelectionMenuEnabled = False
    PreviousTowerSelectionMenuEnabled = False

    buttonList = []

    towerSpritesList = pygame.sprite.Group() #stores all towers placed, used to check when enemies are in range of towers
    tileSpritesList = pygame.sprite.Group() #stores all tiles that make up the map, not currently used
    collisionSpritesList = pygame.sprite.Group() #used in towerplacment, if anything in this list is touching a tower it will not be placed
    enemySpritesList = pygame.sprite.Group() #used in the movement system, everything in here will follow the path and should be enemy class
    buttonSpritesList = pygame.sprite.Group() #stores all sprite based buttons
    pausedButtonSpritesList = pygame.sprite.Group() #Stores all sprit based buttons that are needed in the pause menu
    allSpritesList = pygame.sprite.Group() #list of things to be drawn to screen

    def __init__(self):
        self.waveOngoing = False
        self.paused = False
        self.pathList = None
        self.startTilePos = None
        self.waveReward = 0
        
        #Creates permanent buttons
        towerExample = self.towerList[self.currentTower](pygame.math.Vector2(-50, -50), colours["white"], window)
        self.towerProfileButton = Button(towerExample.GetProfile(), None, pygame.math.Vector2(30, 630), self.TowerSelectionMenuToggle, tags=["Permanent"])
        self.buttonSpritesList.add(self.towerProfileButton)
        self.allSpritesList.add(self.towerProfileButton)

        #Creates permanent text boxes
        self.liveText = TextBox(str(self.lives), ((1150), (20)), size=30, tags=["Permanent"])
        self.moneyText = TextBox(str(self.money), ((1150), (50)), size=30, tags=["Permanent"])
        self.waveText = TextBox("Wave: " + str(self.waveNum + 1), ((1150), (100)), size=30, tags=["Permanent"])
        self.towerCostText = TextBox(str(towerExample.GetPrice()), ((29), (688)), size=15, tags=["Permanent"]) #We ignore this lines existance as it's horrible
        self.textBoxList = [self.liveText, self.moneyText, self.waveText, self.towerCostText]

        #Creates permanent buttons needed in the pause menu
        #Yes button
        self.pausedButtonSpritesList.add(Button("Sprites\\GUI\\Buttons\\YesHighlighted.png", "Sprites\\GUI\\Buttons\\YesUnhighlighted.png", pygame.math.Vector2(500, 425), self.ResetGame))
        #No button
        self.pausedButtonSpritesList.add(Button("Sprites\\GUI\\Buttons\\NoHighlighted.png", "Sprites\\GUI\\Buttons\\NoUnhighlighted.png", pygame.math.Vector2(790, 425), self.ResumeGame))
    
    ####################################################################################################
    #                                           - GameLoop -                                           #
    ####################################################################################################
    def GameLoop(self): #The Main game loop, called when play is clicked
        running = True
        self.paused = False
        while running:
            #Things which have to be done at the start but only when not paused
            if not self.paused:
                #clears all buttons from both button type lists
                self.buttonList = []
                #Removes unneeded sprites
                for sprite in self.buttonSpritesList:
                    tags = sprite.GetTags()
                    remove = True
                    for tag in tags:
                        if tag == "UpgradesMenu" or tag == "Permanent" or tag == "TowerSelectMenu":
                            remove = False
                    if remove:
                        sprite.kill()
                        del sprite
                
                #Removes unneeded textBoxes
                removeList = []
                for textBox in self.textBoxList:
                    tags = textBox.GetTags()
                    remove = True
                    for tag in tags:
                        if tag == "UpgradesMenu" or tag == "Permanent":
                            remove = False
                    if remove:
                        removeList.append(textBox)
                
                for item in removeList:
                    self.textBoxList.remove(item)
            
            #Things which need to be done all the time and aren't dependent on that frames actions
            #Loads Image UI
            #Lives logo
            SelectGUIImage = pygame.image.load("Sprites\\GUI\\LivesHeart.png")
            window.blit(SelectGUIImage, (1100, 10))
            #Money logo
            SelectGUIImage = pygame.image.load("Sprites\\GUI\\MoneyCoin.png")
            window.blit(SelectGUIImage, (1100, 40))

            #Calls upgrades UI
            if self.selectedTower:
                self.selectedTower.UpdateRadius() #updates drawn radius
                self.DrawRadius()

            #Calls selection menu UI
            if self.PreviousTowerSelectionMenuEnabled != self.TowerSelectionMenuEnabled:
                for sprite in self.buttonSpritesList:
                    tags = sprite.GetTags()
                    remove = False
                    for tag in tags:
                        if tag == "TowerSelectMenu":
                            remove = True
                    if remove:
                        sprite.kill()
                        del sprite
                if self.TowerSelectionMenuEnabled:

                    self.TowerSelectionMenu()
                self.PreviousTowerSelectionMenuEnabled = self.TowerSelectionMenuEnabled
            #Checks if the tower selected has changed
            if self.previousSelectedTower != self.selectedTower or self.updateUpgrades:
                #Clearing lists of now unneeded things
                #Unneeded Buttons
                for sprite in self.buttonSpritesList:
                    tags = sprite.GetTags()
                    remove = False
                    for tag in tags:
                        if tag == "UpgradesMenu":
                            remove = True
                    if remove:
                        sprite.kill()
                        del sprite
                #Unneeded Sprites
                removeList = []
                for textBox in self.textBoxList:
                    tags = textBox.GetTags()
                    remove = False
                    for tag in tags:
                        if tag == "UpgradesMenu":
                            remove = True
                    if remove:
                        removeList.append(textBox)
                
                for item in removeList:
                    self.textBoxList.remove(item)
                
                #If there is a new towers upgrade UI to make, make it
                if self.selectedTower:
                    self.UpgradesUI(self.selectedTower)

                self.updateUpgrades = False #Make it so you no longer need to update the upgrades menu
                self.previousSelectedTower = self.selectedTower #Update currently selected tower

            #Things which need to be run differently based on whether it is paused or not
            if not self.paused:
                #Adds button information to the list of buttons that dont use sprites
                #Start Button
                button = Button("Sprites\\GUI\\Buttons\\StartHighlighted.png", "Sprites\\GUI\\Buttons\\StartUnhighlighted.png", pygame.math.Vector2(1180, 660), self.StartWave)
                self.buttonSpritesList.add(button)
                self.allSpritesList.add(button)
                #Back Button
                button = Button("Sprites\\GUI\\Buttons\\BackHighlighted.png", "Sprites\\GUI\\Buttons\\BackUnhighlighted.png", pygame.math.Vector2(1235, 35), self.PauseGame)
                self.buttonSpritesList.add(button)
                self.allSpritesList.add(button)

                #Text UI
                towerExample = self.towerList[self.currentTower](pygame.math.Vector2(-50, -50), colours["white"], window)
                self.liveText.setText(str(self.lives)) #Number of lives
                self.moneyText.setText(str(self.money)) #Ammount of money
                self.waveText.setText("Wave: " + str(self.waveNum + 1)) #Wave Number
                self.towerCostText.setText(str(towerExample.GetPrice())) #Tower Cost (Bottom left)

                #Checking for events each frame while game is running
                self.EventCheck()
                
                #Checks the current selected tower is valid
                if self.currentTower < 0:
                    self.currentTower = len(self.towerList)-1
                elif self.currentTower > len(self.towerList)-1:
                    self.currentTower = 0

                #Updates the selected tower profile
                if self.currentTower != self.previousTower:
                    self.previousTower = self.currentTower
                    self.towerProfileButton.SetImage(self.towerList[self.currentTower]((-100, -100), colours["white"], window).GetProfile())

                #all towers check and attack,
                for enemy in self.enemySpritesList:
                    for tower in self.towerSpritesList:
                        self.money += tower.CheckEnemies(enemy, self.enemySpritesList)
                
                #Updates wool position and spawns new wool
                self.UpdateWool()

                #Check For end of game
                if self.lives <= 0:
                    self.lives = 0 #stop it counting down further after loss screen
                    self.GameEnd()

                #Check for end of wave
                if self.waveOngoing:
                    if len(self.enemySpritesList) == 0 and len(self.currentWave) == 0:
                        self.money += self.waveReward
                        self.waveOngoing = False
                        if allWaves == []:
                            self.GameEnd("you win!")

                #Checks if a button is hovered over(only for sprite based buttons)
                mouse = pygame.mouse.get_pos()
                hoverList = [s for s in self.buttonSpritesList if s.rect.collidepoint(mouse)]
                for button in hoverList:
                    button.OnHover()            
            elif self.paused:
                #Resets the button to not having the hover sprite
                for item in self.pausedButtonSpritesList:
                    item.FrameReset()

                #####################################################################################
                #                                 - Foreground UI -                                 #
                #####################################################################################
                #Draws Rectangles
                pygame.draw.rect(window, colours["white"], (400, 200, 500, 300)) #Menu Background
                pygame.draw.rect(window, colours["grey"], (400, 200, 500, 300), 5) #Menu Border
                
                #Draws Text
                largeText = pygame.font.SysFont("comicsansms", 25)
                textSurf, textRect = TextObjects("Are you sure you want to quit?", largeText)
                textRect.center = (650, 250)
                window.blit(textSurf, textRect)

                textSurf, textRect = TextObjects("you will lose all progress!", largeText)
                textRect.center = (650, 275)
                window.blit(textSurf, textRect)

                #####################################################################################
                #                                 - Actions/Events -                                #
                #####################################################################################
                #Checking for events each frame while game is paused
                mouse = pygame.mouse.get_pos()
                mouseOverlapList = [s for s in self.pausedButtonSpritesList if s.rect.collidepoint(mouse)]

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        quit()
                    
                    #Upon Click
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        for item in mouseOverlapList:
                            item.OnClick()

                #Checks if a button is hovered over(only for sprite based buttons)
                for button in mouseOverlapList:
                    button.OnHover()

                #Renders all pause menu sprites
                self.pausedButtonSpritesList.draw(window)
    
            #Things which need to be done all the time but are dependent on that frames actions
            #updates general button visuals
            for button in self.buttonList:
                ButtonVisuals(**button)
            
            #Draws rectangles for tower selected
            pygame.draw.rect(window, colours["bright_lavender"], (5, 665, 50, 50), 5)
            #pygame.draw.rect(window, colours["bright_lavender"], (5, 605, 50, 50), 5)

            #Things that need to be loaded when paused or not but need updating before loading
            for textBox in self.textBoxList:
                textBox.drawCall()

            #Final stuff
            pygame.display.update()
            window.fill((255, 255, 255))
            self.allSpritesList.draw(window)
            clock.tick(30)

    def UpgradesUI(self, tower): #Ran during game loop to add the upgrades UI
        #Adds the Delete Button
        button = Button("Sprites\\GUI\\Buttons\\DeleteHighlighted.png", "Sprites\\GUI\\Buttons\\DeleteUnhighlighted.png", pygame.math.Vector2(220, 680), func=[tower.RemoveExistance, self.DeleteTower], tags=["UpgradesMenu"])
        self.buttonSpritesList.add(button)
        self.allSpritesList.add(button)
        
        #Adds the Upgrade Buttons
        if len(tower.GetUpgrades()) == 2:
            #Left Hand Button
            if tower.GetUpgrades()[0]:
                #Upgrade Background
                button = Button("Sprites\\GUI\\Buttons\\UpgradeHighlighted.png", "Sprites\\GUI\\Buttons\\UpgradeUnhighlighted.png", pygame.math.Vector2(521, 660), func=self.UpgradeTower, tags=["UpgradesMenu"])
                button.SetParams({"upgradeInfo" : tower.GetUpgrades()[0]})
                self.buttonSpritesList.add(button)
                self.allSpritesList.add(button)

                #Upgrade Text
                text = TextBox(tower.GetUpgrades()[0][0], [513, 630], tags=["UpgradesMenu"]) 
                self.textBoxList.append(text)
                text = TextBox(str(tower.GetUpgrades()[0][1]), [513, 650], tags=["UpgradesMenu"])
                self.textBoxList.append(text)

            #No Upgrade Available
            else:
                button = Button("Sprites\\GUI\\Buttons\\NoRoute.png", None, pygame.math.Vector2(513, 660), tags=["UpgradesMenu"])
                self.buttonSpritesList.add(button)
                self.allSpritesList.add(button)
            
            #Right Hand Button
            if tower.GetUpgrades()[1]:
                #Upgrade Background
                button = Button("Sprites\\GUI\\Buttons\\UpgradeHighlighted.png", "Sprites\\GUI\\Buttons\\UpgradeUnhighlighted.png", pygame.math.Vector2(888, 660), func=self.UpgradeTower, tags=["UpgradesMenu"])
                button.SetParams({"upgradeInfo" : tower.GetUpgrades()[1]})
                self.buttonSpritesList.add(button)
                self.allSpritesList.add(button)

                #Upgrade Text
                text = TextBox(tower.GetUpgrades()[1][0], [888, 630], tags=["UpgradesMenu"]) 
                self.textBoxList.append(text)
                text = TextBox(str(tower.GetUpgrades()[1][1]), [888, 650], tags=["UpgradesMenu"])
                self.textBoxList.append(text)

            #No Upgrade Avaliable
            else:
                button = Button("Sprites\\GUI\\Buttons\\NoRoute.png", None, pygame.math.Vector2(888, 660), tags=["UpgradesMenu"])
                self.buttonSpritesList.add(button)
                self.allSpritesList.add(button)
        
        #upgrades maxed
        else:
            button = Button("Sprites\\GUI\\Buttons\\UpgradeMaxed.png", None, pygame.math.Vector2(695, 660), tags=["UpgradesMenu"])
            self.buttonSpritesList.add(button)
            self.allSpritesList.add(button)

    def PauseGame(self): #Ran upon button press to set the paused state to true
        self.paused = True
    
    def ResumeGame(self): #Ran upon button press to set the paused state to false
        self.paused = False
    
    def DrawRadius(self): #Ran each frame to draw the radius arround the currently selected tower
        elipseBoundries = [self.selectedTower.GetPos()[0]-(10*self.selectedTower.GetRange()), self.selectedTower.GetPos()[1]-(10*self.selectedTower.GetRange()), self.selectedTower.GetRange()*20, self.selectedTower.GetRange()*20]
        pygame.draw.ellipse(window, colours["black"], elipseBoundries, 1)

    def EventCheck(self): #Ran each frame to check current events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
                    
            #Upon Click
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()

                for button in self.buttonList:
                    AreaClick(**button)

                clicked = [s for s in self.buttonSpritesList if s.rect.collidepoint(mouse)]

                if len(clicked) >= 1:
                    for item in clicked:
                        item.OnClick()

                if 1080 > mouse[0] > 0 and 600 > mouse[1] > 0 and self.TowerSelectionMenuEnabled == False:
                    clicked = [s for s in self.towerSpritesList if s.rect.collidepoint(mouse)]
                    if len(clicked) >= 1:
                        self.selectedTower = clicked[0]
                    else:
                        if self.selectedTower:
                            self.selectedTower = None
                        else:
                            self.PlaceTower()
                        
                                
            #Upon Keypress
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.currentTower -= 1
                if event.key == pygame.K_RIGHT:
                    self.currentTower += 1

    def UpdateWool(self): #Ran each frame to move and spawn wool
        #Move Wool
        for item in self.enemySpritesList:
            self.lives += item.MoveFrame()

        #Spawn new Wool
        if self.frameDelay == 0:
            if self.currentWave:
                nextThing = self.currentWave[0]

                if isinstance(nextThing, int):
                    self.frameDelay = int(nextThing)
                
                elif isinstance(nextThing, str):
                    enemy = self.enemyDict[nextThing](self.pathList, self.startTilePos, colours["white"])
                    self.enemySpritesList.add(enemy)
                    self.allSpritesList.add(enemy)
                        
                self.currentWave.pop(0)
        else:
            self.frameDelay -= 1
   
    def StartWave(self): #Ran upon button press to summon the next wave
        if not self.waveOngoing:
            currentWaveData = allWaves.pop(0)
            self.currentWave = currentWaveData[0]
            self.waveReward = currentWaveData[1]
            self.waveOngoing = True
            self.waveNum += 1

    def PlaceTower(self): #Ran to spawn towers at the mouse position upon click
        """
        To place a tower you will need:
        A sprite (defined in the tower's class data)
        The Location of the tower (Defined by the mouse position)
        To Create an instance of that towers class
        """

        mousePositon = pygame.mouse.get_pos()
        tower = self.towerList[self.currentTower](mousePositon, colours["white"], window)

        if pygame.sprite.spritecollide(tower, self.collisionSpritesList, False) == [] and self.money >= tower.GetPrice():
            self.towerSpritesList.add(tower)
            self.collisionSpritesList.add(tower)
            self.allSpritesList.add(tower)
            self.money -= tower.GetPrice()
        else:
            tower.kill()
            del tower

        #window.blit(pygame.image.load(self.currentTower.GetSprite()), mousePositon) #Need to replace blits with sprites

    def UpgradeTower(self, upgradeInfo): #Ran uppon button press to tell the tower to upgrade
        self.updateUpgrades = True
        if upgradeInfo[1] <= self.money:
            self.money -= upgradeInfo[1]
            upgradeInfo[2]()

    def DeleteTower(self): #Ran upon button press to delete the selected tower
        self.money += self.selectedTower.GetValue()
        self.selectedTower = None

    def SetCurrentTower(self, index):
        self.currentTower = index

    def TowerSelectionMenuToggle(self):
        if self.TowerSelectionMenuEnabled:
            self.TowerSelectionMenuEnabled = False
        else:
            self.TowerSelectionMenuEnabled = True

    def TowerSelectionMenu(self):
        numOfTowers = len(self.towerList)

        pygame.draw.rect(window, colours["white"], (5, 407, 122, 183)) #Menu Background
        pygame.draw.rect(window, colours["grey"], (5, 407, 122, 183), 5) #Menu Border
    
        if numOfTowers > 20: #Lays the towers out in a 4x5 grid which is scrollable
            pass 
        
        elif numOfTowers > 16: #Lays the towers out in a 4x5 grid
            numToAdd = 20-numOfTowers
            tempTowerList = copy.deepcopy(self.towerList)
            
            #Need to make a sprite for the background of this popup
            button = Button("Sprites\\GUI\\TowerSelectionBackground(4x5).png", None, (132, 437), None, tags=["TowerSelectMenu"])
            self.buttonSpritesList.add(button)
            self.allSpritesList.add(button)

            for i in range(0, numToAdd):
                tempTowerList.append(None)

            counter = 0
            for item in tempTowerList:
                if item:
                    itemProfile = item(pygame.math.Vector2(-50, -50), colours["white"], window).GetProfile()
                    location = [((counter%4)*64)+36, ((counter//4)*63)+311]
                    button = Button(itemProfile, None, location, self.SetCurrentTower, params={"index" : counter}, tags=["TowerSelectMenu"])
                    self.buttonSpritesList.add(button)
                    self.allSpritesList.add(button)
                else:
                    location = [((counter%4)*64)+36, ((counter//4)*63)+311]
                    button = Button("Sprites\\Towers\\Profile\\NoTower.png", None, location, None, tags=["TowerSelectMenu"])
                    self.buttonSpritesList.add(button)
                    self.allSpritesList.add(button)
                counter += 1
        
        elif numOfTowers > 9: #Lays the towers out in a 3x4 grid
            numToAdd = 12-numOfTowers
            tempTowerList = copy.deepcopy(self.towerList)
            
            #Need to make a sprite for the background of this popup
            button = Button("Sprites\\GUI\\TowerSelectionBackground(3x4).png", None, (100, 470), None, tags=["TowerSelectMenu"])
            self.buttonSpritesList.add(button)
            self.allSpritesList.add(button)

            for i in range(0, numToAdd):
                tempTowerList.append(None)

            counter = 0
            for item in tempTowerList:
                if item:
                    itemProfile = item(pygame.math.Vector2(-50, -50), colours["white"], window).GetProfile()
                    location = [((counter%3)*64)+36, ((counter//3)*63)+375]
                    button = Button(itemProfile, None, location, self.SetCurrentTower, params={"index" : counter}, tags=["TowerSelectMenu"])
                    self.buttonSpritesList.add(button)
                    self.allSpritesList.add(button)
                else:
                    location = [((counter%3)*64)+36, ((counter//3)*63)+375]
                    button = Button("Sprites\\Towers\\Profile\\NoTower.png", None, location, None, tags=["TowerSelectMenu"])
                    self.buttonSpritesList.add(button)
                    self.allSpritesList.add(button)
                counter += 1
        
        else: #Lays the towers out in a 2*3 grid
            numToAdd = 6-numOfTowers
            tempTowerList = copy.deepcopy(self.towerList)

            button = Button("Sprites\\GUI\\TowerSelectionBackground(2x3).png", None, (68, 500), None, tags=["TowerSelectMenu"])
            self.buttonSpritesList.add(button)
            self.allSpritesList.add(button)

            for i in range(0, numToAdd):
                tempTowerList.append(None)

            counter = 0
            for item in tempTowerList:
                if item:
                    itemProfile = item(pygame.math.Vector2(-50, -50), colours["white"], window).GetProfile()
                    location = [((counter%2)*64)+36, ((counter//2)*63)+437]
                    button = Button(itemProfile, None, location, self.SetCurrentTower, params={"index" : counter}, tags=["TowerSelectMenu"])
                    self.buttonSpritesList.add(button)
                    self.allSpritesList.add(button)
                else:
                    location = [((counter%2)*64)+36, ((counter//2)*63)+437]
                    button = Button("Sprites\\Towers\\Profile\\NoTower.png", None, location, None, tags=["TowerSelectMenu"])
                    self.buttonSpritesList.add(button)
                    self.allSpritesList.add(button)
                counter += 1
        
    ####################################################################################################
    #                                     - Other Class Functions -                                    #
    ####################################################################################################
    def GameEnd(self, state="you lose"):
        window.fill((255, 255, 255))
        self.buttonList = []
        self.buttonList.append({"text" : "Quit!", "xPos" : 550, "yPos": 450, "width" : 100, "height" : 50, "colour" : colours["red"], "hoverColour" : colours["bright_red"], "func" : quit})
        EndText = TextBox(state, ((resolution[0]/2), (resolution[1]/2)), 115)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button in self.buttonList:
                        AreaClick(**button)
                    
            EndText.drawCall()

            for button in self.buttonList:
                ButtonVisuals(**button)
            
            pygame.display.update()
            clock.tick(30)

    def GameIntro(self): #The Menu screen Loop, called on play
        intro = True

        self.buttonList = []
        self.buttonList.append({"text" : "Play!", "xPos" : 470, "yPos" : 400, "width" : 300, "height" : 100, "colour" : colours["green"], "hoverColour" : colours["bright_green"], "func" : self.LevelSelect})
        self.buttonList.append({"text" : "Quit!", "xPos" : 570, "yPos": 530, "width" : 100, "height" : 50, "colour" : colours["red"], "hoverColour" : colours["bright_red"], "func" : quit})
        #Button(sprite hoversprive location)
        MenuText = TextBox("Angry Cats!", (resolution[0]/2, 300), 115)
    
        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button in self.buttonList:
                        AreaClick(**button)
                    
            window.fill(colours["white"])
            MenuText.drawCall()

            for button in self.buttonList:
                ButtonVisuals(**button)

            pygame.display.update()
            clock.tick(30)
    
    def LevelSelect(self): #Ran after the main menu where you select a map to play on
        largeText = pygame.font.SysFont("comicsansms", 20)

        #Local sprites lists for this section of the code
        buttonSpritesList = pygame.sprite.Group()
        allSpritesList = pygame.sprite.Group()

        window.fill(colours["white"]) #Clears window
        self.currentMap = AllMaps["Map1"] #Sets the default selected map

        #Permanent buttons
        #Play button
        button = Button("Sprites\\GUI\\Buttons\\PlayHighlighted.png", "Sprites\\GUI\\Buttons\\PlayUnhighlighted.png", pygame.math.Vector2(60, 30), self.GenerateMap, tags=["Permanent"])
        buttonSpritesList.add(button)
        allSpritesList.add(button)
        #Back button
        button = Button("Sprites\\GUI\\Buttons\\BackSmallHighlighted.png", "Sprites\\GUI\\Buttons\\BackSmallUnhighlighted.png", pygame.math.Vector2(35, 80), self.GameIntro, tags=["Permanent"])
        buttonSpritesList.add(button)
        allSpritesList.add(button)
        
        #Sets default values
        pos = 0
        mapIndex = 0
        previousMousePos = pygame.mouse.get_pos() #Needs an original value so we set random one here

        levelSelect = True #Allows while loop to start
        while levelSelect:
            #Checks if it needs to shift the buttons
            if pos >= 400:
                mapIndex -= 1
                pos -= 400
            elif pos <= -400:
                mapIndex += 1
                pos += 400

            #Checks mapIndex to see if its out of bounds
            if mapIndex >= len(MapList):
                mapIndex = 0
            elif mapIndex < 0:
                mapIndex = len(MapList)-1

            #Creates the currentMaps list
            #currentMaps is the list of the central maps and the 2 maps to either side
            if mapIndex+2 > len(MapList)-1:
                mapDifference = (mapIndex+2)-(len(MapList)-1)
                currentMaps = MapList[mapIndex-2:mapIndex+(mapDifference)+1] + MapList[:mapDifference]
            elif mapIndex-2 < 0:
                mapDifference = -(mapIndex-2)
                currentMaps = MapList[-mapDifference:] + MapList[mapIndex-(2-mapDifference):mapIndex+3]
            else:
                currentMaps = MapList[mapIndex-2:mapIndex+3]

            #Collects current mouse position
            
            #Check which buttons the mouse are over
            currentMousePos = pygame.mouse.get_pos()
            hoveredButtons = [s for s in buttonSpritesList if s.rect.collidepoint(currentMousePos)]
            
            #Resets button sprite
            for button in buttonSpritesList:
                button.FrameReset()
            #Updates button sprite if neccessary
            for button in hoveredButtons:
                button.OnHover()

            #Checks current events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                #Upon Click
                if event.type == pygame.MOUSEBUTTONDOWN:

                    if len(hoveredButtons) == 1:
                        hoveredButtons[0].OnClick()

            #Clears non-permanent buttons from the button list
            for sprite in buttonSpritesList:
                tags = sprite.GetTags()
                keep = False
                for tag in tags:
                    if tag == "Permanent":
                        keep = True
                
                if not keep:
                    sprite.kill()
                    del sprite

            #Generates the map images and names
            for i in range(5):
                if AllMaps[currentMaps[i]] == self.currentMap:
                    tempColour = "sky_blue"
                else:
                    tempColour = "bright_sky_blue"

                button = Button(AllMapProfiles[currentMaps[i]], None, pygame.math.Vector2(-200 + (420*i) + pos, 360), self.SelectMap)
                pygame.draw.rect(window, colours[tempColour], (-400 + (420*i) + pos, 250, 400, 220))

                button.SetParams({"gameMap": AllMaps[currentMaps[i]]})
                buttonSpritesList.add(button)
                allSpritesList.add(button)

                #Adds the text below the image
                textSurf, textRect = TextObjects(currentMaps[i], largeText)
                textRect.center = ((-200 + (420*i) + pos, 500))
                window.blit(textSurf, textRect)

            mouseDifference = previousMousePos[0] - currentMousePos[0]
            
            if pygame.mouse.get_pressed()[0] == 1:
                pos -= mouseDifference

            previousMousePos = currentMousePos
            allSpritesList.draw(window)
            pygame.display.update()
            window.fill(colours["white"])
            clock.tick(30)

    def GenerateMap(self): #Ran just before game loop to generate the map
        
        #for a tile key, check MapList.py

        mapFile = open(self.currentMap, "r")
        fileContents = mapFile.readlines()
        mapFile.close()
        mapString = ""
        for item in fileContents:
            mapString += item.replace("\n", "")

        typeList = {
            "#" : Ground,
            "P" : Path,
            ">" : StartRight,
            "<" : StartLeft,
            "/" : StartDown,
            "^" : StartUp,
            "," : EndLeft,
            "6" : EndDown,
            "." : EndRight,
            "?" : EndUp
        }

        counter = 0
        for char in mapString:
            try:
                nextTile = typeList[char]
            except:
                print("Error! Map tile not in typelist")
            location = [((counter%54)*20)+10, ((counter//54)*20)+10]
            tile = nextTile(location, colours["red"])

            self.allSpritesList.add(tile)
            self.tileSpritesList.add(tile)

            if nextTile != Ground:
                self.collisionSpritesList.add(tile)

            counter += 1

        self.GeneratePath()

    def GeneratePath(self): #Ran after generating the map
        #for a tile key, check MapList.py

        mapFile = open(self.currentMap, "r")
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

        
        '''
        endList = [",", ".", "6", "?"]
        listItems = [["U", -1, 0],["D", 1, 29],["L", -1, 0],["R", 1, 53]]
        path = True

        while path == True: #Starts going until the path is complete
            for i in range(4):
                if checkPos[0] != listItems[i][2]:
                    if mapArray[checkPos[0] + listItems[i][1]][checkPos[1]] == "P": #Checks for path
                        self.pathList.append(listItems[i][0])
                        mapArray[checkPos[0]][checkPos[1]] = "#"
                        checkPos[0] = checkPos[0] + listItems[i][1]
                        continue
                    else:
                        for item in endList: #Checks for end
                            if mapArray[checkPos[0] + listItems[i][1]][checkPos[1]] == item:
                                self.pathList.append(listItems[i][0])                                      
                                self.pathList.append("END")
                                path = False

        self.GameLoop()
        '''

        endList = [",", ".", "6", "?"]
        path = True

        while path: #Starts going until the path is complete
            if checkPos[0] != 0: #Checks the tile above
                if mapArray[checkPos[0]-1][checkPos[1]] == "P": #Checks for path
                    self.pathList.append("U")
                    mapArray[checkPos[0]][checkPos[1]] = "#"
                    checkPos[0] = checkPos[0]-1
                    continue
                else:
                    for item in endList: #Checks for end
                        if mapArray[checkPos[0]-1][checkPos[1]] == item:
                            self.pathList.append("U")                                      #
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
                            self.pathList.append("D")                                      #
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
                            self.pathList.append("L")                                      #
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
                            self.pathList.append("R")                                      #
                            self.pathList.append("END")
                            path = False
        self.GameLoop()

    def SelectMap(self, gameMap): #make this take a parameter of the maps location
        self.currentMap = gameMap

    def ResetGame(self): #Ran after the game is over to reset all the values to the starting ones
        self.currentWave = allWaves.pop(0)
        self.lives = 100
        self.money = 200
        self.waveNum = -1
        self.upgrading = False
        self.currentTower = 0
        self.selectedTower = None
        self.currentMap = ""
        

        self.buttonList = []

        self.towerSpritesList.empty()
        self.tileSpritesList.empty()
        self.collisionSpritesList.empty()
        self.enemySpritesList.empty() 
        self.buttonSpritesList.empty()
        self.allSpritesList.empty()
        self.GameIntro()

class Button(pygame.sprite.Sprite):
    def __init__(self, sprite, hoverSprite, location, func=None, params={}, tags=[]):
        self.func = func
        self.sprite = sprite
        self.params = params
        self.tags = tags

        #Cheking wether it needs to have a different sprite while being hovered over
        if not hoverSprite:
            self.hoverEnabled = False
        else: 
            self.hoverEnabled = True
            self.hoverSprite = hoverSprite

        #Sprite stuff
        #Call the parent class'(Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
    
        #Load the image
        self.image = pygame.image.load(sprite).convert()
    
        #Set our transparent color
        self.image.set_colorkey(colours["purple"])
        self.rect = self.image.get_rect()
        self.rect.center = location

    def SetParams(self, params):
        self.params = params

    def SetImage(self, image):
        self.image = pygame.image.load(image).convert()

    def GetTags(self):
        return self.tags

    def OnHover(self):
        if self.hoverEnabled:
            self.image = pygame.image.load(self.hoverSprite).convert()

    def FrameReset(self):
        self.image = pygame.image.load(self.sprite).convert()

    def OnClick(self):
        if self.func:
            if isinstance(self.func, list):
                for item in self.func:
                    item(**self.params)
                    
            else:
                self.func(**self.params)

class TextBox:
    def __init__(self, text, pos, size=20, textColour=colours["black"], tags=[]):
        self.text = text
        self.pos = pos
        self.size = size 
        self.colour = textColour
        self.tags = tags
        
    def drawCall(self): #called during main loop, draws the object to the screen
        textSurf = pygame.font.SysFont("comicsansms", self.size).render(self.text, True, self.colour)
        textRect = textSurf.get_rect()
        textRect.center = (self.pos) 
        window.blit(textSurf, textRect) 

    def GetTags(self):
        return self.tags

    def setText(self, toChange):
        self.text = toChange

    def setPos(self, toChange):
        self.pos = toChange

    def getText(self):
        return self.text

########################################################################################################
#                                            - Functions -                                             #
########################################################################################################

#Used for buttons with no sprites, makes standin sprites for it
def AreaClick(xPos, yPos, width, height, func, perams={}, **kwargs):
    del kwargs
    mouse = pygame.mouse.get_pos()
    if xPos+width > mouse[0] > xPos and yPos+height > mouse[1] > yPos:
        if func:
            if isinstance(func, list):
                for item in func:
                    item(**perams)
                    
            else:
                func(**perams)

def ButtonVisuals(text, xPos, yPos, width, height, colour, hoverColour, border=True, **kwargs):
    del kwargs
    mouse = pygame.mouse.get_pos()
    if xPos+width > mouse[0] > xPos and yPos+height > mouse[1] > yPos:
        pygame.draw.rect(window, colour, (xPos, yPos, width, height)) #Draws the fill
        if border:
            pygame.draw.rect(window, Darken(colour), (xPos, yPos, width, height), 5) #Draws the border

    else:
        pygame.draw.rect(window, hoverColour, (xPos, yPos, width, height)) #Draws the fill
        if border:
            pygame.draw.rect(window, Darken(hoverColour), (xPos, yPos, width, height), 5) #Draws the border

    smallText = pygame.font.SysFont("comicsansms", 20)
    textSurf, textRect = TextObjects(text, smallText)
    textRect.center = ((xPos+(width/2)), (yPos+(height/2)))
    window.blit(textSurf, textRect)

def TextObjects(text, font):
    textSurface = font.render(text, True, colours["black"])
    return textSurface, textSurface.get_rect()


########################################################################################################
#                                          - Call Functions -                                          #
########################################################################################################

main = Main()
main.GameIntro()
pygame.quit()
quit()
