from src.Objects.Resources.Resources import Resources
from src.logger.Logger import Logger, GlobalObject

class Soil(Resources):
    id : int = 0
    def __init__(self) -> None:
        GlobalObject()
        self.global_id = GlobalObject.id
        GlobalObject.objects[self.global_id] = self
        Soil.id += 1
        self.__id = Soil.id
        super().__init__()
        self._is_burnable = False
        self._skin = "sprites/soil.png"
        Logger.add_info(f"Soil is initialized with (id - {self.__id})")
