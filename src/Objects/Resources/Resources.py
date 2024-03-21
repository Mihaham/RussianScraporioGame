from src.Objects.GameObject import GameObject
from typing import Optional
from src.logger.Logger import Logger

class Resources(GameObject):
    id : int = 0

    def __from_prototipe(self, prototipe) -> None:
        self._skin = prototipe.get_skin()
        self._is_burnable = prototipe.get_is_burnable()
        Logger.add_info("Getting Resources from prototipe")

    def __init__(self, prototipe : Optional =None):
        Resources.id += 1
        self.__id = Resources.id
        if prototipe:
            self.__from_prototipe(prototipe)
        Logger.add_info(f"Resource is initialized with (id - {self.__id})")

    def get_skin(self) -> str:
        return self._skin

    def get_is_burnable(self) -> bool:
        return self._is_burnable

    def copy(self):
        return Resources(prototipe=self)
