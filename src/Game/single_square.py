from src.Objects.GameObject import GameObject
from src.Objects.Miners.miners import Miners
from src.Objects.Resources.Resources import Resources
from src.Objects.buildings.Buildings import Building
from typing import Optional
from src.logger.Logger import Logger


class SingleSquare:
    id : int = 0

    def __take_prototipe__(self, prototipe) -> None:
        self._skin : Optional[str] = prototipe.get_skin()
        self.is_player_available : bool = prototipe.is_player_available
        self._buildings : list[Building] = prototipe.get_buildings()
        self._miners : list[Miners] = prototipe.get_miners()
        self._resources : list[Resources] = prototipe.get_resources()
        Logger.add_info("Got info for Single Square from prototipe")

    def __init__(self, skin : Optional[str] = None, prototipe =None):
        SingleSquare.id += 1
        self.__id : int = SingleSquare.id
        if prototipe == None:
            self._skin : Optional[str] = skin
            self._buildings : list[Building] = []
            self._miners : list[Miners] = []
            self._resources : list[Resources] = []
        else:
            self.__take_prototipe__(prototipe)
        Logger.add_info("SingleSquare is initialized")

    def __repr__(self) -> str:
        return f"Objects {self._buildings} in single square with id {self.__id} and skin {self.get_skin()}. Also has {self._miners} miners. Also has {self._resources}"

    def set_skin(self, skin : Optional[str]=None, prototipe=None):
        self._skin : Optional[str] = skin
        if prototipe is not None:
            self.__take_prototipe__(prototipe)

    def get_skin(self) -> str:
        return self._skin

    def add_building(self, object : Building) -> None:
        Logger.add_info(f"Adding building for SingleSquare with id {self.__id}")
        self._buildings.append(object)

    def get_buildings(self) -> list[Building]:
        return self._buildings

    def get_miners(self) -> list[Miners]:
        return self._miners

    def copy(self):
        return SingleSquare(prototipe=self)

    def update(self) -> None:
        for object in self._buildings:
            object.update()

    def add_miner(self, miner : Miners) -> None:
        Logger.add_info(f"Adding miner for SingleSquare with id {self.__id}")
        if self.is_player_available and len(self._miners) == 0:
            self._miners.append(miner)

    def mine(self) -> Optional[Resources]:
        Logger.add_info(f"Mining resources in SingleSquare with id {self.__id}")
        for i in range(len(self._miners)):
            resource = self._miners[i].get_resource()
            if resource is not None:
                return resource
            else:
                self._miners.pop(i)

    def get_resources(self) -> list[Resources]:
        return self._resources
