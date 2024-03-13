class Something:
    _skin = None
    _type = None

    def __get_prototipe(self, prototipe):
        self._skin = prototipe.get_skin()
        self._type = prototipe.get_type()

    def __init__(self, skin="sprites/furnace.png", type=None, prototype=None):
        self._skin = skin
        self._type = type

        if prototype is not None:
            self.__get_prototipe(prototipe=prototype)

    def get_skin(self) -> str:
        return self._skin

    def get_type(self) -> str:
        return self._type
