from src.Objects.Miners.miners import Miners
from src.Objects.Resources.Soil.Soil import Soil
from src.logger.Logger import Logger
from src.CONST import GameConstants


class Fertile_soil(Miners):
    id: int = 0

    def __init__(self):
        super().__init__(resource=Soil, amount=GameConstants.miner_fertile_soil_amount, skin="sprites/fertile_soil.png")
        Fertile_soil.id += 1
        self.__id = Fertile_soil.id
        Logger.add_info(f"Fertile_soil is initialized with (id - {self.__id})")
