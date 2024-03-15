import time

from src.Objects.GameObject import GameObject


class Building(GameObject):
    def __init__(self):
        print("Initializing Building")
        super().__init__()
        self._skin = None
        self.active_skin = None
        self.inactive_skin = None
        self._type = "buildings"
        self.input = {}
        self.output = {}
        self.fuel = {}
        self.__input_resources = {}
        self.__output_resources = {}
        self.__alowded_fuel = []
        self.__is_active = False
        self.__start_of_active = time.time()

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

    def update(self):
        if self.__is_active:
            if self.fuel["burning_time"] < time.time() - self.__start_of_active:
                print(self)
                print(f"burning time: {time.time()}")
                self.__start_of_active = time.time()
                if self.fuel["amount"]:
                    self.fuel["amount"] -= 1
                    for resource, amount in self.__input_resources.copy().items():
                        if self.input[resource] < amount:
                            self.__is_active = False
                            self.change_skin()
                            break
                    if self.__is_active:
                        for resource, amount in self.__input_resources.items():
                            self.input[resource] -= amount
                        for resource, amount in self.__output_resources.items():
                            if resource not in self.output.keys():
                                self.output[resource] = 0
                            self.output[resource] += amount
                else:
                    self.__is_active = False
                    self.change_skin()
