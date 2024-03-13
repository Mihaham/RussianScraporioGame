import Objects.Something
from Objects.Miners.miners import Miners
from Objects.Resources.Resources import Resources

id = 0


class SingleSquare:
    __id = 0

    def __take_prototipe__(self, prototipe):
        self._skin = prototipe.get_skin()
        self.is_player_available = prototipe.is_player_available
        self._buildings = prototipe.get_buildings()
        self._miners = prototipe.get_miners()
        self._resources = prototipe.get_resources()

    def __init__(self, skin=None, prototipe=None):
        global id
        id += 1
        self.__id = id
        if prototipe == None:
            self._skin = skin
            self._buildings = []
            self._miners = []
            self._resources = []
        else:
            self.__take_prototipe__(prototipe)

    def __repr__(self) -> str:
        return f"Objects {self._buildings} in single square with id {self.__id} and skin {self.get_skin()}. Also has {self._miners} miners. Also has {self._resources}"

    def set_skin(self, skin=None, prototipe=None):
        self._skin = skin
        if prototipe is not None:
            self.__take_prototipe__(prototipe)

    def get_skin(self) -> str:
        return self._skin

    def add_object(self, object):
        print(f"Adding object to square with id {self.__id}")
        self._buildings.append(object)

    def get_buildings(self) -> list[Objects.Object.Something]:
        return self._buildings

    def get_miners(self) -> list[Miners]:
        return self._miners

    def copy(self):
        return SingleSquare(prototipe=self)

    def update(self):
        for object in self._buildings:
            object.update()

    def add_miner(self, miner):
        print(f"Adding miner to square with id {self.__id}")
        if self.is_player_available and len(self._miners) == 0:
            self._miners.append(miner)

    def mine(self) -> Resources:
        for i in range(len(self._miners)):
            resource = self._miners[i].get_resource()
            if resource is not None:
                return resource
            else:
                self._miners.pop(i)

    def get_resources(self) -> list[Resources]:
        return self._resources
