import pygame
from pygame import *
#from Towers import *

#Setup
if __name__ == "__main__":
    pygame.init()
    #Screen Resolution
    resolution = (1280, 720)
    pygame.display.set_caption("Cat Shooty Game")
    window = pygame.display.set_mode(resolution)
    background = pygame.image.load("Sprites\Towers\AngryCatSprite.png")
    clock = pygame.time.Clock()
    running = True

#towers = Towers()

def PlaceTower():
    pass
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
    
    window.blit(background, [0, 0])
    pygame.display.update()
    clock.tick(30)
    
pygame.quit()