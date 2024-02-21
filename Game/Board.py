from random import randint

from Game.single_square import SingleSquare

from Game.Squares.Ground import Ground
from Game.Squares.Water import Water

from const import *


class Board:
    grid = None
    game_pos_x = 0
    game_pos_y = 0
    cat_box = (50, 50)

    def __init__(self):
        line = [None] * field
        self.grid = []
        for i in range(field):
            self.grid.append(line.copy())

        for i in range(field):
            for j in range(field):
                self.grid[i][j] = SingleSquare(prototipe=Ground())

        for k in range(water_amount):
            x = randint(0, field - water_size)
            y = randint(0, field - water_size)

            for i in range(water_size):
                for j in range(water_size):
                    self.grid[x + i][y + j].set_skin(prototipe=Water())

    def draw(self, surface):
        for x in range(len(self.grid)):
            for y in range(len(self.grid[x])):
                self.grid[x][y].draw(surface, x * scale, y * scale, self.game_pos_x, self.game_pos_y)

    def increase_coordinates(self, x, y):
        self.update_cordinates(self.game_pos_x + x, self.game_pos_y + y)
    def update_cordinates(self, new_x, new_y):
        self.game_pos_x = new_x
        self.game_pos_y = new_y
