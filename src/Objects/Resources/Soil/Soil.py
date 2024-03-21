from src.Objects.Resources.Resources import Resources
from src.logger.Logger import Logger

class Soil(Resources):
    def __init__(self) -> None:
        super().__init__()
        self._is_burnable = False
        self._skin = "sprites/soil.png"
        Logger.add_info("Soil is initialized")
