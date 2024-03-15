import time

from src.Objects.buildings.Buildings import Building

class Furnace(Building):
    def __init__(self):
        print("Initializing Furnace")
        super().__init__()
        self._skin = "sprites/furnace.png"
        self._type = "buildings"
        self.input = {
            "cuprum ore": 1000
        }
        self.output = {
        }
        self.fuel = {
            "name": "coal",
            "amount": 100,
            "burning_time": 1
        }
        self.__input_resources = {
            "cuprum ore": 1
        }
        self.__output_resources = {
            "cuprum": 1
        }
        self.__alowded_fuel = ["coal"]
        self.__is_active = False
        self.__start_of_active = time.time()
        self.active_skin = "sprites/furnace.png"
        self.inactive_skin = "sprites/burning_furnace.png"

    def __repr__(self) -> str:
        return f"Furnace with {self.input} and {self.output} and {self.fuel}"
