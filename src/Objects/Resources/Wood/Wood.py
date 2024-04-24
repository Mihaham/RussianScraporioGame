from src.Objects.Resources.Resources import Resources
from src.logger.Logger import Logger


class Wood(Resources):
    id = 0

    def __init__(self) -> None:
        Wood.id += 1
        self.__id = Wood.id
        super().__init__()
        self._is_burnable = True
        self._skin = "sprites/wood.jpg"
        Logger.add_info(f"Wood is initialized with (id - {self.__id})")
