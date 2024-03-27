import time

from src.Objects.buildings.Buildings import Building
from src.logger.Logger import Logger, GlobalObject


class Furnace(Building):
    id : int = 0
    def __init__(self):
        Furnace.id += 1
        self.__id = Furnace.id
        super().__init__()
        self._skin : str = "sprites/furnace.png"
        self._type : str = "buildings"
        self.input : dict = {
            "cuprum ore": 1000
        }
        self.output : dict[str,int] = {
        }
        self.fuel : dict[str,int | str] = {
            "name": "coal",
            "amount": 100,
            "burning_time": 1,
            "fuel_cost": 1
        }
        self.__input_resources : dict[str,int] = {
            "cuprum ore": 1
        }
        self.__output_resources : dict[str,int] = {
            "cuprum": 1
        }
        self.__alowded_fuel : list[str] = ["coal"]
        self.__is_active : bool = False
        self.__start_of_active : time.time = time.time()
        self.active_skin : str = "sprites/burning_furnace.png"
        self.inactive_skin : str = "sprites/furnace.png"
        self.input_resources : dict[str, int] = {
            "cuprum ore": 5
        }
        self.output_resources : dict[str,int] = {
            "cuprum": 10
        }
        Logger.add_info(f"Furnace is initialized with (id - {self.__id})")

    def __repr__(self) -> str:
        return f"Furnace with {self.input} and {self.output} and {self.fuel}"
