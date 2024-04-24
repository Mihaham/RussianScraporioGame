from src.Objects.Miners.miners import Miners
from src.Objects.Resources.Wood.Wood import Wood
from src.logger.Logger import Logger
from src.CONST import GameConstants

class Tree(Miners):
    id: int = 0

    def __init__(self):
        Tree.id += 1
        self.__id = Tree.id
        super().__init__(resource=Wood, amount=GameConstants.tree_amount, skin="sprites/tree.png")
        Logger.add_info(f"Tree is initialized with (id - {self.__id})")
