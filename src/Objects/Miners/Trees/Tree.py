from src.Objects.Miners.miners import Miners
from src.Objects.Resources.Wood.Wood import Wood
from src.logger.Logger import Logger

class Tree(Miners):

    def __init__(self):
        super().__init__(resource=Wood, amount=10, skin="sprites/tree.png")
        Logger.add_info("Tree is initialized")
