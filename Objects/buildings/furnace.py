import time

from Objects.Object import Object

class Furnace(Object):
    _skin = "sprites/furnace.png"
    _type = "buildings"
    input = {
        "cuprum ore" : 1000
    }
    output = {
    }
    fuel = {
        "name" : "coal",
        "amount" : 100,
        "burning_time": 1
    }
    __input_resources = {
        "cuprum ore" : 1
    }
    __output_resources = {
        "cuprum" : 1
    }
    __alowded_fuel = ["coal"]
    __is_active = False
    __start_of_active = time.time()

    def __init__(self):
        print("Initializing Furnace")
        super().__init__()
        self.__input_resources["cuprum ore"] = 1
        self.__output_resources["cuprum"] = 1
        self._type = "buildings"

    def __repr__(self):
        return f"Furnace with {self.input} and {self.output} and {self.fuel}"

    def change_active(self):
        self.__is_active = not self.__is_active
        self.change_skin()

    def change_skin(self):
        if self.__is_active:
            self._skin = "sprites/burning_furnace.png"
        else:
            self._skin = "sprites/furnace.png"


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


