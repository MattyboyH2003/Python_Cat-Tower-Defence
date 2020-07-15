import pygame
from pygame import *

class Tiles(pygame.sprite.Sprite):
    def __init__(self, startPos, colour):
        pygame.sprite.Sprite.__init__(self)
    
        # Load the image
        self.image = pygame.image.load(self.sprite).convert()
    
        # Set our transparent color
        self.image.set_colorkey(colour)
        self.rect = self.image.get_rect()
        self.rect.center = startPos

class Ground(Tiles):
    sprite = "Sprites\\Tiles\\Grass.png"
        
class Path(Tiles):
    sprite = "Sprites\\Tiles\\Path.png"

class Start(Tiles):
    pass
class StartUp(Start):
    pass
class StartRight(Start):
    pass
class StartDown(Start):
    sprite = "Sprites\\Tiles\\StartDown.png"
class StartLeft(Start):
    pass

class End(Tiles):
    pass
class EndUp(End):
    pass
class EndRight(End):
    pass
class EndDown(End):
    sprite = "Sprites\\Tiles\\EndDown.png"
class EndLeft(End):
    pass