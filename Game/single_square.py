import pygame

from const import *
from Objects.buildings.furnace import Furnace

id = 0

class SingleSquare:
    _skin = None
    is_player_available = None
    _objects = []

    __id = 0

    def __take_prototipe__(self, prototipe):
        self._skin = prototipe.get_skin()
        self.is_player_available = prototipe.is_player_available
        self._objects = prototipe.get_objects()

    def __init__(self, skin=None, prototipe=None):
        global id
        id+=1
        self.__id = id
        print("Initializing SingleSquare")
        if prototipe == None:
            self._skin = skin
            self._objects = []
        else:
            self.__take_prototipe__(prototipe)

    def __repr__(self):
        return f"Objects {self._objects} in single square with id {self.__id} and skin {self.get_skin()}"

    def set_skin(self, skin=None, prototipe=None):
        self._skin = skin
        if prototipe is not None:
            self.__take_prototipe__(prototipe)

    def get_skin(self):
        return self._skin

    def add_object(self, object):
        print(f"Adding object to square with id {self.__id}")
        self._objects.append(object)

    def get_objects(self):
        return self._objects

    def copy(self):
        return SingleSquare(prototipe=self)
