import time
from typing import Optional

import src.Menu
from src.Objects.GameObject import GameObject
from src.Objects.Resources.Soil.Soil import Soil
from src.Objects.Resources.Wood.Wood import Wood
from src.Objects.buildings.Recipe import Recipe
from src.logger.Logger import Logger


class Building(GameObject):
    id: int = 0

    def __init__(self) -> None:
        Building.id += 1
        self.__id = Building.id
        super().__init__()
        self._skin: Optional[str] = None
        self.active_skin: Optional[str] = None
        self.inactive_skin: Optional[str] = None
        self._type: str = "buildings"
        self.input: dict = {}
        self.output: dict = {}
        self.fuel = {}
        self.__is_active: bool = False
        self.__start_of_active: time.time = time.time()
        self.is_active_menu = False
        self.Menu = src.Menu.BuildingMenu(200, 150, 1500, 500, self,
                                          [Recipe(input={Wood: 1}, output={Soil: 20}),
                                           Recipe(input={Wood: 1}, output={Soil: 1}),
                                           Recipe(input={Wood: 1, Soil: 100}, output={Soil: 1}),
                                           Recipe(input={Soil: 1}, output={Wood: 1})],
                                          self.change_menu)
        self.has_active_recipe = False
        self.active_recipe = None
        self.active_player = None
        Logger.add_info(f"Building is initialized with (id - {self.__id})")

    def add_fuel(self, item, amount=1):
        self.fuel["amount"] += amount

    def add_input(self, item, amount=1):
        if item not in self.input.keys():
            self.input[item] = 0
        self.input[item] += amount

    def activate_recipe(self, recipe):
        self.has_active_recipe = True
        self.active_recipe = recipe
        print(self.active_recipe)

    def delete_recipe(self):
        self.has_active_recipe = False
        self.active_recipe = None
        self.__is_active = False
        self.change_skin()

    def __repr__(self) -> str:
        return f"Building with {self.input} and {self.output}"

    def change_menu(self, player=None) -> None:
        self.is_active_menu = not self.is_active_menu
        self.active_player = player

    def change_active(self) -> None:
        if self.active_recipe == None:
            Logger.add_warnings(
                f"Trying to activate a building with id {self.__id} without a recipe")
            self.__is_active: bool = False
            self.change_skin()
            return None
        if self.fuel["amount"] < self.fuel["fuel_cost"]:
            Logger.add_warnings(
                f"Trying to activate a building with id {self.__id} without enough fuel")
            self.__is_active: bool = False
            self.change_skin()
            return None
        for item, amount in self.active_recipe.input_resources.items():
            if item not in self.input.keys():
                Logger.add_warnings(
                    f"We don`t have resource {item} in building input with id {self.__id}")
                self.__is_active: bool = False
                self.change_skin()
                return None
            if self.input[item] < amount:
                Logger.add_warnings(
                    f"We don`t have enough resource {item} in building with id {self.__id}")
                self.__is_active: bool = False
                self.change_skin()
                return None
        self.__is_active = not self.__is_active
        self.change_skin()

    def change_skin(self) -> None:
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
                if self.fuel["amount"] >= self.fuel["fuel_cost"]:
                    self.fuel["amount"] -= self.fuel["fuel_cost"]
                    for resource, amount in self.active_recipe.input_resources.items():
                        if self.input[resource] < amount:
                            self.__is_active = False
                            self.change_skin()
                            break
                    if self.__is_active:
                        for resource, amount in self.active_recipe.input_resources.items():
                            self.input[resource] -= amount
                        for resource, amount in self.active_recipe.output_resources.items():
                            if resource not in self.output.keys():
                                self.output[resource] = 0
                            self.output[resource] += amount
                else:
                    self.__is_active = False
                    self.change_skin()

    def get_skin(self) -> str:
        return self._skin

    def get_type(self) -> str:
        return self._type
