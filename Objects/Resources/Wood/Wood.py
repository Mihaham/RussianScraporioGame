from Objects.Resources.Resources import Resources


class Wood(Resources):
    def __init__(self):
        super().__init__()
        self._is_burnable = True
        self._skin = "sprites/wood.jpg"
