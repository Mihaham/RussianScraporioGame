from src.Objects.Resources.Resources import Resources


class Soil(Resources):
    def __init__(self):
        super().__init__()
        self._is_burnable = False
        self._skin = "sprites/soil.png"
