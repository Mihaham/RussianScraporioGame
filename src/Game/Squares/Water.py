from src.Game.single_square import SingleSquare
from src.logger.Logger import Logger, GlobalObject

class Water(SingleSquare):
    id = 0
    def __init__(self):
        GlobalObject()
        self.global_id = GlobalObject.id
        GlobalObject.objects[self.global_id] = self
        Water.id += 1
        self.__id = Water.id
        super().__init__()
        self._skin = "sprites/mishaVoda.png"
        self.is_player_available = False
        Logger.add_info(f"Water is initialized with (id - {self.__id})")

