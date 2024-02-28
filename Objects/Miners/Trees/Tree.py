from Objects.Miners.miners import Miners
from Objects.Resources.Wood.Wood import Wood


class Tree(Miners):

    def __init__(self):
        super().__init__(resource=Wood(), amount=10, skin="sprites/tree.png")
