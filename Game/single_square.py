import pygame

from const import *
from Objects.buildings.furnace import Furnace

id = 0

class SingleSquare:
    __id = 0

    def __take_prototipe__(self, prototipe):
        self._skin = prototipe.get_skin()
        self.is_player_available = prototipe.is_player_available
        self._buildings = prototipe.get_buildings()
        self._miners = prototipe.get_miners()
        self._resources = prototipe.get_resources()

    def __init__(self, skin=None, prototipe=None):
        global id
        id+=1
        self.__id = id
        if prototipe == None:
            self._skin = skin
            self._buildings = []
            self._miners = []
            self._resources = []
        else:
            self.__take_prototipe__(prototipe)

    def __repr__(self):
        return f"Objects {self._buildings} in single square with id {self.__id} and skin {self.get_skin()}. Also has {self._miners} miners. Also has {self._resources}"

    def set_skin(self, skin=None, prototipe=None):
        self._skin = skin
        if prototipe is not None:
            self.__take_prototipe__(prototipe)

    def get_skin(self):
        return self._skin

    def add_object(self, object):
        print(f"Adding object to square with id {self.__id}")
        self._buildings.append(object)

    def get_buildings(self):
        return self._buildings

    def get_miners(self):
        return self._miners

    def copy(self):
        return SingleSquare(prototipe=self)

    def update(self):
        for object in self._buildings:
            object.update()

    def add_miner(self, miner):
        print(f"Adding miner to square with id {self.__id}")
        if self.is_player_available:
            self._miners.append(miner)

    def mine(self):
        for i in range(len(self._miners)):
            resource = self._miners[i].get_resource()
            if resource is not None:
                self._resources.append(self._miners[i].get_resource())
            else:
                self._miners.pop(i)


    def get_resources(self):
        return self._resources