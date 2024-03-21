from src.Objects.Resources.Resources import Resources
from src.logger.Logger import Logger

class Wood(Resources):
    def __init__(self) -> None:
        super().__init__()
        self._is_burnable = True
        self._skin = "sprites/wood.jpg"
        Logger.add_info("Wood is initialized")
