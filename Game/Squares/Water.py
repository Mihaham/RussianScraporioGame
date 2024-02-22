from Game.single_square import SingleSquare


class Water(SingleSquare):
    def __init__(self):
        print("Initializing Water")
        super().__init__()
        self._skin = "sprites/mishaVoda.png"
        self.is_player_available = False
