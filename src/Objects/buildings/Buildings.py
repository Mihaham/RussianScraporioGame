import time

from src.Objects.GameObject import GameObject
from src.Objects.Resources.Resources import Resources
from typing import Optional
from src.logger.Logger import Logger

class Building(GameObject):
    id : int = 0
    def __init__(self) -> None:
        Building.id += 1
        self.__id = Building.id
        super().__init__()
        self._skin : Optional[str] = None
        self.active_skin : Optional[str] = None
        self.inactive_skin : Optional[str] = None
        self._type : str = "buildings"
        self.input : dict = {}
        self.output : dict = {}
        self.fuel : dict = {}
        self.input_resources : dict = {}
        self.output_resources : dict = {}
        self.__alowded_fuel : list[Optional[Resources]] = []
        self.__is_active : bool = False
        self.__start_of_active : time.time = time.time()
        Logger.add_info(f"Building is initialized with (id - {self.__id})")

    def __repr__(self) -> str:
        return f"Building with {self.input} and {self.output} and {self.fuel}"

    def change_active(self):
        self.__is_active = not self.__is_active
        self.change_skin()

    def change_skin(self):
        if self.__is_active:
            self._skin = self.active_skin
        else:
            self._skin = self.inactive_skin

    def update(self) -> None:
        if self.__is_active:
            if self.fuel["burning_time"] < time.time() - self.__start_of_active:
                print(self)
                print(f"burning time: {time.time()}")
                self.__start_of_active = time.time()
                if self.fuel["amount"]:
                    self.fuel["amount"] -= self.fuel["fuel_cost"]
                    for resource, amount in self.input_resources.copy().items():
                        if self.input[resource] < amount:
                            self.__is_active = False
                            self.change_skin()
                            break
                    if self.__is_active:
                        for resource, amount in self.input_resources.items():
                            self.input[resource] -= amount
                        for resource, amount in self.output_resources.items():
                            if resource not in self.output.keys():
                                self.output[resource] = 0
                            self.output[resource] += amount
                else:
                    self.__is_active = False
                    self.change_skin()
