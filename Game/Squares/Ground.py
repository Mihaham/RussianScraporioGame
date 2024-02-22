from Game.single_square import SingleSquare


class Ground(SingleSquare):
    def __init__(self):
        print(f"Initializing Ground")
        super().__init__()
        self._skin = "sprites/mishaZemlya.png"
        self.is_player_available = True
