import time

from src.Objects.buildings.Buildings import Building
from src.logger.Logger import Logger, GlobalObject
from src.Objects.Resources.Wood.Wood import Wood


class Furnace(Building):
    id : int = 0
    def __init__(self):
        Furnace.id += 1
        self.__id = Furnace.id
        super().__init__()
        self._skin : str = "sprites/furnace.png"
        self._type : str = "buildings"
        self.input : dict = {
            Wood : 100
        }
        self.output : dict[str,int] = {
        }
        self.fuel : dict[str,int | str] = {
            "name": Wood,
            "amount": 10,
            "burning_time": 1,
            "fuel_cost": 1
        }
        self.__is_active : bool = False
        self.__start_of_active : time.time = time.time()
        self.active_skin : str = "sprites/burning_furnace.png"
        self.inactive_skin : str = "sprites/furnace.png"
        Logger.add_info(f"Furnace is initialized with (id - {self.__id})")

    def __repr__(self) -> str:
        return f"Furnace with {self.input} and {self.output} and {self.fuel}"
