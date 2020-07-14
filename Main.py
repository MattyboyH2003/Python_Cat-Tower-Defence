import pygame
from pygame import *
from Towers import *

#Setup
if __name__ == "__main__":
    pygame.init()
    resolution = (1280, 720)
    pygame.display.set_caption("Cat Shooty Game")
    window = pygame.display.set_mode(resolution)
    #pygame.display.set_icon(surface)
    background = pygame.image.load("Sprites\Towers\AngryCatSprite.png")
    clock = pygame.time.Clock()
    running = True

    currentTower = PistolCat
    TowersList = []
else:
    exit()

#towers = Towers()
def PlaceTower():
    mousePositon = pygame.mouse.get_pos()

    window.blit(pygame.image.load(currentTower.GetSprite()), mousePositon)
    """
    To place a tower you will need:
    A sprite (defined in the tower's class data)
    The Location of the tower (Defined by the mouse position)
    The Screen to place it on
    """

#MainLoop
while running == True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONUP:
            PlaceTower()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                currentTower = PistolCat
            if event.key == pygame.K_RIGHT:
                currentTower = AngryCat




    window.blit(background, [0, 0])
    pygame.display.update()
    clock.tick(30)
    
pygame.quit()