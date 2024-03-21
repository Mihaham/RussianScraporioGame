from src.Objects.Miners.miners import Miners
from src.Objects.Resources.Soil.Soil import Soil
from src.logger.Logger import Logger

class Fertile_soil(Miners):

    def __init__(self):
        super().__init__(resource=Soil, amount=10, skin="sprites/fertile_soil.png")
        Logger.add_info("Fertile_soil is initialized")
