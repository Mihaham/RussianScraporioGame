from Objects.Miners.miners import Miners
from Objects.Resources.Soil.Soil import Soil


class Fertile_soil(Miners):

    def __init__(self):
        super().__init__(resource=Soil(), amount=10, skin="sprites/fertile_soil.png")
