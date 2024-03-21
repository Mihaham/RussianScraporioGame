from src.Objects.GameObject import GameObject
from typing import Optional
from src.logger.Logger import Logger

class Resources(GameObject):

    def __from_prototipe(self, prototipe) -> None:
        self._skin = prototipe.get_skin()
        self._is_burnable = prototipe.get_is_burnable()
        Logger.add_info("Getting Resources from prototipe")

    def __init__(self, prototipe : Optional =None):
        if prototipe:
            self.__from_prototipe(prototipe)
        Logger.add_info("Resource is initialized")

    def get_skin(self) -> str:
        return self._skin

    def get_is_burnable(self) -> bool:
        return self._is_burnable

    def copy(self):
        return Resources(prototipe=self)
