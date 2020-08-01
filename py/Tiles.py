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
    def __init__(self, startPos, colour):

        Tiles.__init__(self, startPos, colour)
class StartUp(Start):
    sprite = "Sprites\\Tiles\\StartUp.png"
class StartRight(Start):
    sprite = "Sprites\\Tiles\\StartRight.png"
class StartDown(Start):
    sprite = "Sprites\\Tiles\\StartDown.png"
class StartLeft(Start):
    sprite = "Sprites\\Tiles\\StartLeft.png"

class End(Tiles):

    def __init__(self, startPos, colour):

        Tiles.__init__(self, startPos, colour)
class EndUp(End):
    sprite = "Sprites\\Tiles\\EndUp.png"
class EndRight(End):
    sprite = "Sprites\\Tiles\\EndRight.png"
class EndDown(End):
    sprite = "Sprites\\Tiles\\EndDown.png"
class EndLeft(End):
    sprite = "Sprites\\Tiles\\EndLeft.png"