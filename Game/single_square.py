import random

import pygame

from const import *


class SingleSquare:
    skin = None
    is_player_available = None

    def __take_prototipe__(self, prototipe):
        self.skin = prototipe.skin
        self.is_player_available = prototipe.is_player_available

    def __init__(self, skin=None, prototipe=None):
        if prototipe == None:
            self.skin = skin
        else:
            self.__take_prototipe__(prototipe)

    def draw(self, surface=None, position_x=None, position_y=None):
        square_skin = pygame.image.load(self.skin)
        square_skin = pygame.transform.scale(square_skin, (scale, scale))
        square_rect = square_skin.get_rect(topleft=(position_x, position_y), width=scale)
        surface.blit(square_skin, square_rect)

    def set_skin(self, skin = None, prototipe = None):
        if prototipe == None:
            self.skin = skin
        else:
            self.__take_prototipe__(prototipe)
