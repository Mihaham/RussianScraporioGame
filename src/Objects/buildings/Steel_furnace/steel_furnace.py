import time

from src.Objects.Resources.Wood.Wood import Wood
from src.Objects.buildings.Buildings import Building
from src.logger.Logger import Logger
from src.CONST import GameConstants


class Steel_furnace(Building):
    id: int = 0

    def __init__(self):
        """This is documentation for Steel_furnace"""
        Steel_furnace.id += 1
        self.__id = Steel_furnace.id
        super().__init__()
        self._skin: str = "sprites/furnace.png"
        self._type: str = "buildings"
        self.input: dict = {
            Wood: GameConstants.building_default_input_amount
        }
        self.output: dict[str, int] = {
        }
        self.fuel: dict[str, int | str] = {
            "name": Wood,
            "amount": GameConstants.building_default_fuel_amount,
            "burning_time": 1,
            "fuel_cost": 1
        }
        self.__is_active: bool = False
        self.__start_of_active: time.time = time.time()
        self.active_skin: str = "sprites/my_rect_sprites/steel-furnace.png"
        self.inactive_skin: str = "sprites/furnace.png"
        Logger.add_info(f"Steel Furnace is initialized with (id - {self.__id})")

    def __repr__(self) -> str:
        return f"Steel Furnace with {self.input} and {self.output} and {self.fuel}"
