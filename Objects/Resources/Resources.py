import Objects.Something


class Resources(Objects.Object.Something):
    _skin = None
    _is_burnable = None

    def __from_prototipe(self, prototipe):
        self._skin = prototipe.get_skin()
        self._is_burnable = prototipe.get_is_burnable()

    def __init__(self, prototipe=None):
        if prototipe:
            self.__from_prototipe(prototipe)

    def get_skin(self) -> str:
        return self._skin

    def get_is_burnable(self) -> bool:
        return self._is_burnable

    def copy(self):
        return Resources(prototipe=self)
