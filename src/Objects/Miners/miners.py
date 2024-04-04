from src.Objects.GameObject import GameObject
from src.Objects.Resources.Resources import Resources
from typing import Optional
from src.logger.Logger import Logger, GlobalObject

class Miners(GameObject):
    id : int = 0
    def __init__(self, resource : Optional[Resources]=None, amount : Optional[int]=0, skin : Optional[str]=None):
        Miners.id += 1
        self._type = "miners"
        self.__id = Miners.id
        self._resource : Optional[resource] = resource
        self._amount : int = amount
        self._skin : Optional[str] = skin
        Logger.add_info(f"Miner is initialized with (id - {self.__id})")

    def __repr__(self) -> str:
        return f"_resource {self._resource} _amount {self._amount} _skin {self._skin}"

    def get_resource(self) -> Optional[Resources]:
        if self._amount > 0:
            self._amount -= 1
            return self._resource
        else:
            return None

    def get_skin(self) -> str:
        return self._skin
