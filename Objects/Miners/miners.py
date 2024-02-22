from const import *


class Miners:
    _resource = None
    _amount = None
    _skin = None


    def __init__(self, resource = None, amount = None, skin = None):
        self._resource = resource if resource is not None else None
        self._amount = amount if amount is not None else 0
        self._skin = skin if skin is not None else None

    def __repr__(self):
        return f"_resource {self._resource} _amount {self._amount} _skin {self._skin}"


    def get_resource(self):
        if self._amount > 0:
            self._amount -= 1
            return self._resource.copy()
        else:
            return None

    def get_skin(self):
        return self._skin


