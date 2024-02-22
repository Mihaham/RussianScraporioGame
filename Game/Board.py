from random import randint

from Game.Squares.Ground import Ground
from Game.Squares.Water import Water
from Game.single_square import SingleSquare
from const import *
from Objects.buildings.furnace import Furnace
from Objects.Miners.Trees.Tree import Tree


class Board:
    __grid = None
    __game_pos_x = 0
    __game_pos_y = 0
    __cat_box = (300, 150)

    def __init__(self):
        self.__grid = [[None for i in range(field)] for j in range(field)]
        for i in range(field):
            for j in range(field):
                self.__grid[i][j] = SingleSquare(prototipe=Ground())

        for k in range(water_amount):
            x = randint(0, field - water_size)
            y = randint(0, field - water_size)

            for i in range(water_size):
                for j in range(water_size):
                    self.__grid[x + i][y + j].set_skin(prototipe=Water())




        self.__grid[1][2].add_miner(Tree())

        self.__grid[1][1].add_object(Furnace())

    def __repr__(self):
        for i in range(field):
            for j in range(field):
                print(self.__grid[i][j])
        return ""

    def increase_coordinates(self, x, y):
        self.update_cordinates(self.__game_pos_x + x, self.__game_pos_y + y)

    def update_cordinates(self, new_x, new_y):
        self.__game_pos_x = new_x
        self.__game_pos_y = new_y

    def get_grid(self):
        return self.__grid

    def get_grid_size(self):
        return field

    def get_cat_box(self):
        return self.__cat_box

    def set_grid(self, new_grid):
        self.__grid = new_grid

    def set_cat_box(self, new_cat):
        self.__cat_box = new_cat

    def get_game_pos(self):
        return (self.__game_pos_x, self.__game_pos_y)

    def get_game_pos_x(self):
        return self.__game_pos_x

    def get_game_pos_y(self):
        return self.__game_pos_y

    def update(self):
        for i in range(field):
            for j in range(field):
                self.__grid[i][j].update()
