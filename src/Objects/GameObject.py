from collections.abc import Callable
from typing import Optional
from src.logger.Logger import Logger

class GameObject:
    id = 0

    def __get_prototipe(self, prototipe) -> None:
        self._skin = prototipe.get_skin()
        self._type = prototipe.get_type()
        Logger.add_info("Object got by prototipe")

    def __init__(self, skin : Optional[str]="sprites/furnace.png", type : Optional[str] =None, prototype : Optional=None):
        GameObject.id += 1
        self.__id = GameObject.id
        self._skin = skin
        self._type = type

        if prototype is not None:
            self.__get_prototipe(prototipe=prototype)
        Logger.add_info(f"GameObject created with skin and type with (id - {self.__id})")

    def get_skin(self) -> str:
        return self._skin

    def get_type(self) -> str:
        return self._type
