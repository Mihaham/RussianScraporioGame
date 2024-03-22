from src.Game.single_square import SingleSquare
from src.logger.Logger import Logger, GlobalObject

class Ground(SingleSquare):
    id = 0
    def __init__(self):
        GlobalObject()
        self.global_id = GlobalObject.id
        GlobalObject.objects[self.global_id] = self
        Ground.id += 1
        self.__id = Ground.id
        super().__init__()
        self._skin = "sprites/mishaZemlya.png"
        self.is_player_available = True
        Logger.add_info(f"Ground is initialized with (id - {self.__id})")
