from Game.single_square import SingleSquare


class Ground(SingleSquare):
    def __init__(self):
        super().__init__()
        self.skin = "sprites/mishaZemlya.png"
        self.is_player_available = True
