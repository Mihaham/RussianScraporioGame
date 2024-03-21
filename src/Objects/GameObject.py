from collections.abc import Callable
from typing import Optional
from src.logger.Logger import Logger

class GameObject:

    def __get_prototipe(self, prototipe) -> None:
        self._skin = prototipe.get_skin()
        self._type = prototipe.get_type()
        Logger.add_info("Object got by prototipe")

    def __init__(self, skin : Optional[str]="sprites/furnace.png", type : Optional[str] =None, prototype : Optional=None):
        self._skin = skin
        self._type = type

        if prototype is not None:
            self.__get_prototipe(prototipe=prototype)
        Logger.add_info("GameObject created with skin and type")

    def get_skin(self) -> str:
        return self._skin

    def get_type(self) -> str:
        return self._type
